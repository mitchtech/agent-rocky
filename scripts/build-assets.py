"""Derive previews from committed clips and pet art; never change their sources."""

import math
import sys
import tempfile
import wave
from array import array
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageSequence

ROOT = Path(__file__).resolve().parent.parent
AUDIO = ROOT / "audio"
PREVIEWS = ROOT / "assets" / "previews"
FONTS = ROOT / "site" / "fonts"
# --check renders elsewhere and compares pixels: PNG bytes vary with each platform's zlib.
CHECK = "--check" in sys.argv[1:]
OUT = Path(tempfile.mkdtemp()) if CHECK else PREVIEWS
OUT.mkdir(parents=True, exist_ok=True)
# The site's Night and Day palettes. The spectrum viewport stays dark in both, like the site.
DARK = {"bg": (11, 13, 18), "surface": (20, 23, 32), "ink": (232, 230, 225), "muted": (169, 165, 157), "accent": (255, 122, 69),
        "gold": (255, 213, 138), "edge": (42, 48, 64), "star": (232, 230, 225)}
LIGHT = {"bg": (244, 240, 232), "surface": (251, 248, 242), "ink": (30, 32, 38), "muted": (87, 83, 76), "accent": (168, 63, 22),
         "gold": (125, 90, 18), "edge": (200, 192, 178), "star": (30, 32, 38)}
VIEWPORT = (6, 8, 13)
CARAPACE = (138, 127, 114)
TAU_CETI = (255, 213, 138)
PETROVA = (255, 122, 69)
ASTROPHAGE = (255, 92, 69)
XENONITE = (159, 201, 196)
HEADLINE_CLIPS = [
    ("amaze-amaze-amaze", "Amaze! Amaze! Amaze!", TAU_CETI),
    ("fist-my-bump", "Fist my bump.", TAU_CETI),
    ("we-die", "We die. We die. We die.", ASTROPHAGE),
    ("not-enough", "Not enough. Not enough.", PETROVA),
    ("how-much-astrophage", "How much Astrophage, question?", PETROVA),
    ("eridian-question", "(Eridian question)", XENONITE),
]
DISPLAY = "space-grotesk-latin-700-normal.woff2"
BODY = "ibm-plex-sans-latin-400-normal.woff2"
BOLD = "ibm-plex-sans-latin-600-normal.woff2"
MONO = "ibm-plex-mono-latin-400-normal.woff2"


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size, layout_engine=ImageFont.Layout.BASIC)


def peaks(clip, columns):
    with wave.open(str(AUDIO / f"{clip}.wav")) as audio:
        samples = array("h", audio.readframes(audio.getnframes()))
    if sys.byteorder == "big":
        samples.byteswap()
    step = max(1, len(samples) // columns)
    values = [max((abs(value) for value in samples[i * step:(i + 1) * step]), default=0) / 32768 for i in range(columns)]
    top = max(values) or 1
    return [value / top for value in values]


def space(width, height, palette):
    """Background with a deterministic star field so --check stays reproducible."""
    canvas = Image.new("RGBA", (width, height), palette["bg"] + (255,))
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((width * 0.55, -height * 0.6, width * 1.3, height * 0.6), fill=palette["accent"] + (34,))
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(height // 4)))
    draw = ImageDraw.Draw(canvas, "RGBA")
    seed = 7
    for _ in range(width * height // 2600):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        x, y = seed % width, (seed >> 11) % height
        alpha = 40 + (seed >> 5) % 90
        radius = 1 if (seed >> 9) % 5 else 1.6
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=palette["star"] + (alpha,))
    return canvas


def pentagon(cx, cy, r, rotation=-90):
    return [(cx + r * math.cos(math.radians(rotation + 72 * i)), cy + r * math.sin(math.radians(rotation + 72 * i))) for i in range(5)]


def mark(canvas, center, radius, edge, bars=TAU_CETI):
    """The Eridian mark: a stone pentagon carapace holding a four-note chord."""
    draw = ImageDraw.Draw(canvas, "RGBA")
    cx, cy = center
    draw.polygon(pentagon(cx, cy, radius), fill=CARAPACE + (255,), outline=edge + (255,), width=max(2, radius // 14))
    unit = radius / 6.5
    for index, height in enumerate((1.6, 3.0, 3.8, 2.2)):
        x = cx + (index - 1.5) * unit * 1.25 - unit * 0.32
        draw.rounded_rectangle((x, cy - height * unit * 0.55 + unit * 0.5, x + unit * 0.64, cy + height * unit * 0.55 + unit * 0.5), radius=unit * 0.32, fill=bars + (255,))


def spectrum(size, clip, reveal=1.0, color=TAU_CETI):
    """A dark viewport with the clip's loudness drawn as glowing bars, swept in up to `reveal`."""
    width, height = size
    canvas = Image.new("RGBA", size, VIEWPORT + (255,))
    draw = ImageDraw.Draw(canvas, "RGBA")
    for i in range(1, 6):
        y = height * i / 6
        draw.line((0, y, width, y), fill=XENONITE + (20,), width=1)
    columns = max(8, (width - 16) // 9)
    values = peaks(clip, columns)
    shown = int(columns * reveal)
    gap = (width - 16) / columns
    bars = Image.new("RGBA", size, (0, 0, 0, 0))
    lines = ImageDraw.Draw(bars)
    for index in range(columns):
        x = 8 + index * gap
        level = values[index] if index < shown else 0.02
        h = max(2, level * height * 0.8)
        alpha = 255 if index < shown else 70
        lines.rounded_rectangle((x + gap * 0.18, height * 0.92 - h, x + gap * 0.82, height * 0.92), radius=gap * 0.3, fill=color + (alpha,))
    canvas.alpha_composite(bars.filter(ImageFilter.GaussianBlur(5)))
    canvas.alpha_composite(bars)
    return canvas


def framed(canvas, box, clip, palette, color=TAU_CETI):
    left, top, right, bottom = box
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rounded_rectangle((left - 12, top - 12, right + 12, bottom + 12), radius=22, fill=palette["surface"] + (255,), outline=palette["edge"] + (255,), width=2)
    panel = spectrum((right - left, bottom - top), clip, color=color)
    rounded = Image.new("L", panel.size, 0)
    ImageDraw.Draw(rounded).rounded_rectangle((0, 0, panel.width - 1, panel.height - 1), radius=12, fill=255)
    canvas.paste(panel, (left, top), rounded)


def eyebrow(canvas, xy, size, palette):
    draw = ImageDraw.Draw(canvas, "RGBA")
    x, y = xy
    draw.polygon(pentagon(x + 8, y + size * 0.6, 9), fill=palette["gold"])
    draw.text((x + 26, y), "AGENT ROCKY", font=font(MONO, size), fill=palette["gold"])


def headline(canvas, xy, size, limit, palette):
    draw = ImageDraw.Draw(canvas, "RGBA")
    words = ["Amaze.", "Amaze.", "Amaze."]
    # Shrink to fit beside the panel rather than running under it.
    while draw.textlength(" ".join(words), font=font(DISPLAY, size)) > limit:
        size -= 2
    display = font(DISPLAY, size)
    x, y = xy
    for word, fill in zip(words, (palette["ink"], palette["accent"], palette["gold"])):
        draw.text((x, y), word, font=display, fill=fill)
        x += draw.textlength(f"{word} ", font=display)


# Waveform previews: a sweep that reveals each clip, then holds.
label_font = font(BOLD, 17)
corners = Image.new("L", (240, 126), 0)
ImageDraw.Draw(corners).rounded_rectangle((0, 0, 239, 125), radius=12, fill=255)
for clip, line, color in HEADLINE_CLIPS:
    frames = []
    steps = 14
    base = space(288, 200, DARK)
    framed(base, (24, 24, 264, 150), clip, DARK, color)
    for step in range(steps + 1):
        canvas = base.copy()
        canvas.paste(spectrum((240, 126), clip, reveal=step / steps, color=color), (24, 24), corners)
        draw = ImageDraw.Draw(canvas)
        width = draw.textlength(line, font=label_font)
        draw.text(((288 - width) / 2, 168), line, font=label_font, fill=DARK["ink"] if step == steps else DARK["muted"])
        frames.append(canvas.convert("RGB"))
    durations = [70] * steps + [1600]
    frames[0].save(OUT / f"{clip}.gif", save_all=True, append_images=frames[1:], duration=durations, loop=0, disposal=2)

# Fonts are the site's self-hosted OFL faces, so the cards match the page on every OS.
card = space(1200, 630, DARK)
draw = ImageDraw.Draw(card, "RGBA")
eyebrow(card, (88, 92), 22, DARK)
headline(card, (84, 140), 104, 600, DARK)
draw.text((90, 290), "Your coding agent, with an", font=font(DISPLAY, 40), fill=DARK["ink"])
draw.text((90, 340), "Eridian engineer's enthusiasm.", font=font(DISPLAY, 40), fill=DARK["ink"])
for row, text in enumerate(["Project Hail Mary sound cues for", "Claude Code, Codex, and Gemini CLI"]):
    draw.text((90, 466 + row * 38), text, font=font(BODY, 30), fill=DARK["muted"])
framed(card, (760, 170, 1110, 450), "amaze-amaze-amaze", DARK)
mark(card, (935, 100), 46, DARK["ink"])
draw.text((760, 494), "SOUND CUES FOR CODING AGENTS", font=font(MONO, 22), fill=PETROVA)
card.convert("RGB").save(OUT / "social.png")

# GitHub picks the README banner by color scheme, so both themes get one.
for name, palette in (("banner-dark", DARK), ("banner-light", LIGHT)):
    banner = space(1280, 440, palette)
    draw = ImageDraw.Draw(banner, "RGBA")
    eyebrow(banner, (92, 84), 22, palette)
    headline(banner, (88, 124), 112, 640, palette)
    draw.text((94, 244), "Rocky's lines from Project Hail Mary", font=font(BODY, 32), fill=palette["muted"])
    draw.text((94, 288), "as sound cues for coding agents.", font=font(BODY, 32), fill=palette["muted"])
    framed(banner, (800, 120, 1180, 360), "amaze-amaze-amaze", palette)
    mark(banner, (990, 66), 36, palette["ink"])
    banner.convert("RGB").save(OUT / f"{name}.png")

touch = Image.new("RGBA", (180, 180), DARK["bg"] + (255,))
draw = ImageDraw.Draw(touch, "RGBA")
draw.rounded_rectangle((6, 6, 173, 173), radius=28, fill=DARK["surface"] + (255,), outline=PETROVA + (255,), width=4)
mark(touch, (90, 96), 64, DARK["ink"])
touch.convert("RGB").save(OUT / "touch-icon.png")

# The plugin listing icon: the touch icon's mark at the 512 px the Claude plugin validator asks for.
listing = Image.new("RGBA", (512, 512), DARK["bg"] + (255,))
draw = ImageDraw.Draw(listing, "RGBA")
draw.rounded_rectangle((17, 17, 494, 494), radius=80, fill=DARK["surface"] + (255,), outline=PETROVA + (255,), width=11)
mark(listing, (256, 273), 182, DARK["ink"])
listing.convert("RGB").save(OUT / "icon.png")

# Pet previews come from the active v2 atlas, at the site's 160 ms frame rate.
sheet_path = ROOT / "pets" / "rocky" / "spritesheet.webp"
if sheet_path.exists():
    with Image.open(sheet_path) as source:
        sheet = source.convert("RGBA")
    for name, row, count in [("idle", 0, 6), ("working", 7, 6), ("waiting", 6, 6), ("review", 8, 6), ("failure", 5, 8)]:
        frames = []
        for column in range(count):
            canvas = Image.new("RGBA", (192, 208), DARK["surface"] + (255,))
            canvas.alpha_composite(sheet.crop((column * 192, row * 208, (column + 1) * 192, (row + 1) * 208)))
            frames.append(canvas.convert("RGB"))
        frames[0].save(OUT / f"pet-{name}.gif", save_all=True, append_images=frames[1:], duration=160, loop=0, disposal=2)
    sheet.crop((0, 0, 192, 208)).save(OUT / "pet-idle.png")


def frames_of(path):
    with Image.open(path) as image:
        return [(item.convert("RGBA"), item.info.get("duration")) for item in ImageSequence.Iterator(image)]


if CHECK:
    stale = []
    for built in sorted(OUT.iterdir()):
        committed = PREVIEWS / built.name
        if not committed.exists():
            stale.append(built.name)
            continue
        expected, actual = frames_of(committed), frames_of(built)
        if len(expected) != len(actual) or any(a[1] != b[1] or ImageChops.difference(a[0], b[0]).getbbox(alpha_only=False) for a, b in zip(expected, actual)):
            stale.append(built.name)
    if stale:
        sys.exit(f"Preview assets are stale; run python3 scripts/build-assets.py: {', '.join(stale)}")
    print("Preview assets match the current clips and fonts")
else:
    print(f"Built preview assets in {OUT}")
