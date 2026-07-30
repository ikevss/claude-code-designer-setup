#!/usr/bin/env python3
"""Create numbered thumbnail overview images from rendered slide PNG files.

This script is intentionally small: `render_png.py` owns PPT/PPTX rendering,
while this script only tiles the resulting `slide_*.png` files so an agent can
inspect the whole template before selecting representative reference pages.
"""

import argparse
import math
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover - environment dependent
    print(
        "Missing dependency: Pillow is required for tile_pages.py. "
        "Install pillow in the runtime image or use the existing PPTX renderer.",
        file=sys.stderr,
    )
    raise SystemExit(2)

try:
    RESAMPLE_LANCZOS = Image.Resampling.LANCZOS
except AttributeError:  # Pillow < 9
    RESAMPLE_LANCZOS = Image.LANCZOS


SLIDE_RE = re.compile(r"(\d+)")


def natural_key(path: Path):
    parts = SLIDE_RE.split(path.name)
    return [int(p) if p.isdigit() else p.lower() for p in parts]


def load_font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def discover_images(input_dir: Path, sort: str):
    images = sorted(input_dir.glob("slide_*.png"), key=natural_key if sort == "natural" else lambda p: p.name)
    if not images:
        images = sorted(input_dir.glob("*.png"), key=natural_key if sort == "natural" else lambda p: p.name)
    return images


def resize_to_width(path: Path, thumb_width: int):
    image = Image.open(path).convert("RGB")
    ratio = thumb_width / image.width
    size = (thumb_width, max(1, int(round(image.height * ratio))))
    return image.resize(size, RESAMPLE_LANCZOS)


def output_path(base: Path, page_count: int, page_index: int):
    if page_count == 1:
        return base
    return base.with_name(f"{base.stem}-{page_index + 1}{base.suffix}")


def render_page(paths, all_count: int, page_index: int, page_count: int, args):
    thumbs = [resize_to_width(p, args.thumb_width) for p in paths]
    max_thumb_h = max(t.height for t in thumbs)
    rows = math.ceil(len(thumbs) / args.cols)

    margin = 32
    gutter = args.gutter
    title_h = 64
    label_h = 30
    footer_h = 42
    cell_w = args.thumb_width
    cell_h = label_h + max_thumb_h

    width = margin * 2 + args.cols * cell_w + (args.cols - 1) * gutter
    height = margin * 2 + title_h + rows * cell_h + (rows - 1) * gutter + footer_h
    canvas = Image.new("RGB", (width, height), args.background)
    draw = ImageDraw.Draw(canvas)

    title_font = load_font(26, bold=True)
    label_font = load_font(22, bold=True)
    footer_font = load_font(16)
    border = (210, 218, 230)
    ink = (20, 28, 42)
    muted = (95, 105, 120)

    title = f"Slide Overview ({all_count} pages)"
    if page_count > 1:
        title += f" - batch {page_index + 1}/{page_count}"
    draw.text((margin, margin), title, fill=ink, font=title_font)

    y0 = margin + title_h
    start_number = page_index * args.max_pages + 1
    for i, thumb in enumerate(thumbs):
        row = i // args.cols
        col = i % args.cols
        x = margin + col * (cell_w + gutter)
        y = y0 + row * (cell_h + gutter)
        slide_num = start_number + i
        label = f"{slide_num}"
        label_box = draw.textbbox((0, 0), label, font=label_font)
        label_w = label_box[2] - label_box[0]
        draw.text((x + (cell_w - label_w) / 2, y), label, fill=ink, font=label_font)
        img_y = y + label_h
        draw.rectangle(
            [x - 1, img_y - 1, x + cell_w + 1, img_y + thumb.height + 1],
            outline=border,
            width=1,
        )
        canvas.paste(thumb, (x, img_y))

    footer = f"Total: {all_count} pages | thumbnails: {args.thumb_width}px wide | source: {args.input_dir}"
    draw.text((margin, height - margin - 20), footer, fill=muted, font=footer_font)
    return canvas


def main(argv=None):
    parser = argparse.ArgumentParser(description="Tile rendered slide PNGs into numbered overview images.")
    parser.add_argument("--input-dir", required=True, type=Path, help="Directory containing slide_*.png files.")
    parser.add_argument("--output", required=True, type=Path, help="Output overview PNG path.")
    parser.add_argument("--cols", type=int, default=4, help="Number of thumbnail columns.")
    parser.add_argument("--thumb-width", type=int, default=400, help="Thumbnail width in pixels.")
    parser.add_argument("--max-pages", type=int, default=20, help="Maximum slides per overview image.")
    parser.add_argument("--gutter", type=int, default=16, help="Gap between thumbnails in pixels.")
    parser.add_argument("--sort", choices=["natural", "name"], default="natural", help="Sort order for input images.")
    parser.add_argument("--background", default="#FFFFFF", help="Canvas background color.")
    args = parser.parse_args(argv)

    if args.cols < 1 or args.thumb_width < 80 or args.max_pages < 1:
        print("--cols, --thumb-width, and --max-pages must be positive values.", file=sys.stderr)
        return 2

    images = discover_images(args.input_dir, args.sort)
    if not images:
        print(f"No PNG files found in {args.input_dir}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    page_count = math.ceil(len(images) / args.max_pages)
    outputs = []
    for page_index in range(page_count):
        batch = images[page_index * args.max_pages : (page_index + 1) * args.max_pages]
        tiled = render_page(batch, len(images), page_index, page_count, args)
        out = output_path(args.output, page_count, page_index)
        tiled.save(out)
        outputs.append(out)

    for out in outputs:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
