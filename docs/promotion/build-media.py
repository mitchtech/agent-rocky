"""Build labeled promotional previews from the committed clips, not host recordings."""

import hashlib
import json
import subprocess
import wave
from array import array
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "promotion"
OUT.mkdir(parents=True, exist_ok=True)
SIZE, FPS, RATE = 1080, 15, 32000
# The site's Night palette: deep space, Petrova orange, Tau Ceti gold, xenonite teal.
BG, INK, MUTED, GOLD, PETROVA = (11, 13, 18), (232, 230, 225), (169, 165, 157), (255, 213, 138), (255, 122, 69)
VIEWPORT, GRID, EDGE = (6, 8, 13), (159, 201, 196, 30), (42, 48, 64)
FONTS = ROOT / "site" / "fonts"
TITLE = FONTS / "space-grotesk-latin-700-normal.woff2"
BODY = FONTS / "ibm-plex-sans-latin-400-normal.woff2"
LABEL = FONTS / "ibm-plex-mono-latin-400-normal.woff2"


def samples(clip):
    with wave.open(str(ROOT / f"audio/{clip}.wav")) as source:
        assert (source.getframerate(), source.getnchannels(), source.getsampwidth()) == (RATE, 1, 2)
        data = array("h", source.readframes(source.getnframes()))
    if sys.byteorder == "big":
        data.byteswap()
    return data


def little_endian(data):
    copy = array("h", data)
    if sys.byteorder == "big":
        copy.byteswap()
    return copy.tobytes()


def peaks(data, columns):
    step = max(1, len(data) // columns)
    values = [max((abs(v) for v in data[i * step:(i + 1) * step]), default=0) for i in range(columns)]
    top = max(values) or 1
    return [value / top for value in values]


def text(draw, y, content, size=42, color=INK, face=BODY):
    font = ImageFont.truetype(str(face), size)
    for line in content.split("\n"):
        width = draw.textlength(line, font=font)
        if width > 940:
            raise ValueError(f"Caption exceeds safe width: {line}")
        draw.text(((SIZE - width) / 2, y), line, font=font, fill=color)
        y += size * 1.25


def card(title, subtitle, footer, command=None):
    image = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((24, 24, SIZE - 25, SIZE - 25), radius=36, outline=EDGE, width=3)
    text(draw, 90, "AGENT ROCKY", 30, GOLD, LABEL)
    text(draw, 150, title, 76, INK, TITLE)
    text(draw, 270, subtitle, 38)
    if command:
        text(draw, 790, command, 32, GOLD, LABEL)
    text(draw, 870, "github.com/mitchtech/agent-rocky", 32, PETROVA, LABEL)
    text(draw, 944, footer, 26, MUTED)
    return image


def scope(values, reveal, color=GOLD):
    """A 720 x 360 spectrum viewport with the clip's loudness swept in as bars up to `reveal` (0-1)."""
    width, height = 720, 360
    screen = Image.new("RGBA", (width, height), VIEWPORT + (255,))
    draw = ImageDraw.Draw(screen)
    for i in range(1, 6):
        draw.line((0, height * i / 6, width, height * i / 6), fill=GRID, width=1)
    bars = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    lines = ImageDraw.Draw(bars)
    shown = int(len(values) * reveal)
    gap = (width - 20) / len(values)
    for index, value in enumerate(values):
        x = 10 + index * gap
        level = value if index < shown else 0.02
        h = max(2, level * height * 0.8)
        lines.rounded_rectangle((x + gap * 0.18, height * 0.92 - h, x + gap * 0.82, height * 0.92), radius=gap * 0.3, fill=color + (255 if index < shown else 90,))
    screen.alpha_composite(bars.filter(ImageFilter.GaussianBlur(6)))
    screen.alpha_composite(bars)
    ImageDraw.Draw(screen).rounded_rectangle((0, 0, width - 1, height - 1), radius=18, outline=EDGE, width=4)
    return screen


# (start, end, title, subtitle, command, cue clip or None)
sound_scenes = [
    (0, 4, "Session started", '"Hello, Grace friend."', None, "hello-grace-friend"),
    (4, 8, "Approval needed", '"What problem, question?"', None, "what-problem"),
    (8, 13, "Destructive command", '"We die. We die. We die."', "$ git push --force origin main", "we-die"),
    (13, 17, "Turn finished", '"Amaze! Amaze! Amaze!"', None, "amaze-amaze-amaze"),
    (17, 22, "Usage limit reached", '"Not enough. Not enough."', None, "not-enough"),
    (22, 27, "Fist my bump.", "Local audio. No telemetry.\nNever approves or blocks anything.", None, "fist-my-bump"),
]
CUE_OFFSET = 0.5


def build(name, scenes, footer):
    duration = scenes[-1][1]
    temporary = ROOT / "dist/promotion/render"
    temporary.mkdir(parents=True, exist_ok=True)
    video = temporary / f"{name}.mp4"
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
               "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{SIZE}x{SIZE}",
               "-framerate", str(FPS), "-i", "pipe:0",
               "-frames:v", str(duration * FPS), "-c:v", "libx264", "-threads", "2",
               "-preset", "fast", "-crf", "26", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(video)]
    cards = [card(scene[2], scene[3], footer, scene[4]) for scene in scenes]
    clips = {scene[5]: samples(scene[5]) for scene in scenes if scene[5]}
    waves = {clip: peaks(data, 180) for clip, data in clips.items()}
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for tick in range(duration * FPS):
            second = tick / FPS
            index = next(i for i, scene in enumerate(scenes) if scene[0] <= second < scene[1])
            start, clip = scenes[index][0], scenes[index][5]
            image = cards[index].copy()
            reveal = min(1.0, max(0.0, (second - start - CUE_OFFSET) / (len(clips[clip]) / RATE))) if clip else 1.0
            if clip:
                screen = scope(waves[clip], reveal)
            else:
                screen = scope([0.01] * 180, 1.0)
            image.paste(screen.convert("RGB"), (180, 400))
            process.stdin.write(image.tobytes())
            if tick == FPS * 3:
                image.save(OUT / f"{name}.png")
    finally:
        process.stdin.close()
    if process.wait():
        raise RuntimeError(f"ffmpeg failed for {name}")
    track = bytearray(duration * RATE * 2)
    for scene in scenes:
        start, clip = scene[0], scene[5]
        if clip:
            data = little_endian(clips[clip])
            offset = int((start + CUE_OFFSET) * RATE) * 2
            track[offset:offset + len(data)] = data
    audio = temporary / f"{name}.wav"
    with wave.open(str(audio), "wb") as destination:
        destination.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        destination.writeframes(bytes(track))
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video), "-i", str(audio),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                    "-t", str(duration), "-movflags", "+faststart", str(OUT / f"{name}.mp4")], check=True)

    def timestamp(second):
        return f"00:{second // 60:02d}:{second % 60:02d},000"

    subtitles = [f"{index}\n{timestamp(start)} --> {timestamp(end)}\n{title}\n{subtitle}\n{footer}\n"
                 for index, (start, end, title, subtitle, *_) in enumerate(scenes, 1)]
    (OUT / f"{name}.srt").write_text("\n".join(subtitles))
    return sorted(clips)


used = build("sound-preview", sound_scenes, "Illustrated sound preview - not a live host recording")
sources = [ROOT / f"audio/{clip}.wav" for clip in sorted(set(used))] + [TITLE, BODY, LABEL]


def record(path):
    return {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


manifest = {
    "kind": "illustrated-previews", "dimensions": [SIZE, SIZE], "fps": FPS,
    "sources": [record(path) for path in sources],
    "artifacts": [record(path) for path in sorted(OUT.iterdir()) if path.suffix in (".mp4", ".png", ".srt")],
    "tools": {"Pillow": __import__("PIL").__version__, "ffmpeg": subprocess.check_output(
        ["ffmpeg", "-version"], text=True).splitlines()[0]},
    "credentials_used": [],
    "limitations": ["Not a live host or physical audio recording.",
                     "No claim of hook execution in these videos.",
                     "Audio is assembled from the bundled, separately noticed Project Hail Mary clips."],
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Built the captioned sound preview in {OUT.relative_to(ROOT)}")
