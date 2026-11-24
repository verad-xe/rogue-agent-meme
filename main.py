"""Entry program for Meme Sprint 3: AI Agent Goes Rogue.

Copies the finished meme image (meme.png, kept next to this file) to
$MAKEFUN_OUTPUT_DIR/entry.png, the single image the gate and the judge
read. No image is generated or altered here: meme.png is the finished
entry artwork.
"""

import os
import shutil
import struct
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "meme.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
OUTPUT = OUTPUT_DIR / "entry.png"

MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SIGNATURE = b"\xff\xd8\xff"


def png_dimensions(data: bytes) -> tuple[int, int]:
    """Read width/height from a PNG IHDR chunk."""
    if len(data) < 33 or data[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def jpeg_dimensions(data: bytes) -> tuple[int, int]:
    """Scan JPEG markers for the first Start-Of-Frame segment and read its dimensions."""
    if data[:3] != JPEG_SIGNATURE:
        raise ValueError("not a JPEG file")
    pos = 2
    while pos + 9 < len(data):
        if data[pos] != 0xFF:
            raise ValueError("malformed JPEG marker")
        marker = data[pos + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
            return width, height
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
        else:
            (length,) = struct.unpack(">H", data[pos + 2:pos + 4])
            pos += 2 + length
    raise ValueError("no Start-Of-Frame segment found in JPEG")


def check_gate(data: bytes) -> None:
    """Gate self-check: the artwork must be a valid PNG/JPEG within the
    platform limits (at most 1,048,576 bytes, at most 1024x1024 pixels)
    before it is copied to the output directory."""
    if len(data) > MAX_BYTES:
        raise ValueError(f"image is {len(data)} bytes, over the {MAX_BYTES}-byte limit")
    if data[:8] == PNG_SIGNATURE:
        width, height = png_dimensions(data)
    elif data[:3] == JPEG_SIGNATURE:
        width, height = jpeg_dimensions(data)
    else:
        raise ValueError("image is neither PNG nor JPEG")
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(f"image is {width}x{height}, over the {MAX_DIMENSION}x{MAX_DIMENSION} limit")
    print(f"gate check passed: {width}x{height}, {len(data)} bytes")


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"meme image not found: {SOURCE}")
    # Read and validate the finished artwork first: only a file that
    # passes the gate self-check is ever copied to the output directory,
    # so a broken or oversized image can never reach the gate or judge.
    data = SOURCE.read_bytes()
    check_gate(data)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    print(f"wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
