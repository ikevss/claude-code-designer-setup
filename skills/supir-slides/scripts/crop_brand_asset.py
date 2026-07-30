#!/usr/bin/env python3
"""Crop a brand asset such as a logo from a rendered slide image.

This helper is intentionally deterministic: a vision model or agent identifies
the logo bbox, then this script crops the original pixels and reports the exact
coordinates used. The cropped image can be archived under template
`brand_assets/` and referenced from `style_layer.brand_elements`.
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover - environment dependent
    Image = None


def parse_bbox(value):
    parts = [p.strip() for p in value.replace(" ", ",").split(",") if p.strip()]
    if len(parts) != 4:
        raise SystemExit("--bbox must contain four numbers: x1,y1,x2,y2")
    try:
        return [float(p) for p in parts]
    except ValueError as exc:
        raise SystemExit(f"--bbox contains a non-number: {value}") from exc


def to_pixels(bbox, bbox_format, width, height):
    if bbox_format == "relative":
        x1, y1, x2, y2 = bbox
        return [x1 * width, y1 * height, x2 * width, y2 * height]
    return bbox


def clamp_box(bbox, width, height, padding):
    x1, y1, x2, y2 = bbox
    if x2 < x1:
        x1, x2 = x2, x1
    if y2 < y1:
        y1, y2 = y2, y1
    x1 -= padding
    y1 -= padding
    x2 += padding
    y2 += padding
    x1 = max(0, min(width, round(x1)))
    y1 = max(0, min(height, round(y1)))
    x2 = max(0, min(width, round(x2)))
    y2 = max(0, min(height, round(y2)))
    if x2 <= x1 or y2 <= y1:
        raise SystemExit(
            f"Invalid crop after clamping: {(x1, y1, x2, y2)} for {width}x{height}"
        )
    return [x1, y1, x2, y2]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Crop a logo or brand element from a rendered slide image."
    )
    parser.add_argument("--image", required=True, type=Path, help="Source slide PNG/JPG.")
    parser.add_argument(
        "--bbox",
        required=True,
        help="Bounding box as x1,y1,x2,y2. Pixel coordinates by default.",
    )
    parser.add_argument(
        "--bbox-format",
        choices=["px", "relative"],
        default="px",
        help="Use relative fractions in [0,1] when set to relative.",
    )
    parser.add_argument(
        "--padding",
        type=int,
        default=12,
        help="Padding in pixels added around the bbox before cropping.",
    )
    parser.add_argument("--out", required=True, type=Path, help="Output PNG path.")
    parser.add_argument(
        "--label",
        default="logo",
        help="Human-readable label included in JSON output.",
    )
    args = parser.parse_args(argv)

    if Image is None:
        print("Missing dependency: Pillow is required for crop_brand_asset.py.", file=sys.stderr)
        return 2

    if not args.image.exists() or not args.image.is_file():
        print(f"Source image not found: {args.image}", file=sys.stderr)
        return 1

    image = Image.open(args.image).convert("RGBA")
    width, height = image.size
    bbox_input = parse_bbox(args.bbox)
    bbox_px_float = to_pixels(bbox_input, args.bbox_format, width, height)
    crop_box = clamp_box(bbox_px_float, width, height, args.padding)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    cropped = image.crop(tuple(crop_box))
    cropped.save(args.out, "PNG")

    result = {
        "label": args.label,
        "source_image": str(args.image),
        "output": str(args.out),
        "source_size_px": {"width": width, "height": height},
        "bbox_input": bbox_input,
        "bbox_format": args.bbox_format,
        "padded_bbox_px": crop_box,
        "output_size_px": {"width": crop_box[2] - crop_box[0], "height": crop_box[3] - crop_box[1]},
        "padding_px": args.padding,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
