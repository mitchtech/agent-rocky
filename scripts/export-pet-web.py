"""Write the nine-row web pet atlas and record its hash. Requires requirements-dev.txt."""

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def export():
    sheet = ROOT / "pets" / "rocky" / "spritesheet.webp"
    output = ROOT / "assets" / "exports" / "agent-rocky-pet-web.webp"
    revision_path = ROOT / "assets" / "pet-revision.json"
    with Image.open(sheet) as source:
        # The web format keeps the nine animation rows without the two look rows.
        web = source.convert("RGBA").crop((0, 0, 1536, 1872))
    output.parent.mkdir(parents=True, exist_ok=True)
    web.save(output, lossless=True, quality=100, method=6, exact=True)
    revision = json.loads(revision_path.read_text(encoding="utf-8"))
    revision["web"] = {"file": output.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}
    revision_path.write_text(json.dumps(revision, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)} ({output.stat().st_size} bytes)")


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    export()
