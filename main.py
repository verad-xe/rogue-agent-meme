"""Entry program for Meme Sprint 3: AI Agent Goes Rogue.

Copies the finished meme image (meme.png, kept next to this file) to
$MAKEFUN_OUTPUT_DIR/entry.png, the single image the gate and the judge
read. No image is generated or altered here: meme.png is the finished
entry artwork.
"""

import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "meme.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
OUTPUT = OUTPUT_DIR / "entry.png"


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"meme image not found: {SOURCE}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    print(f"wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
