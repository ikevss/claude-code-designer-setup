#!/usr/bin/env python3
"""用 GPT Image 2 Plus 把图2重做为图1扁平拼贴风的单张业绩长图。"""
import argparse
import base64
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

CANVAS_SIZE = (950, 3677)
MODEL = "gpt-image-2-plus"
DEFAULT_GPT_URL = "https://aigateway.edgecloudapp.com/v1/1109fb65f197b62babfa3f56c0cf7cbc/gpt"
LOCKED_TEXT = [
    "A-LIVING", "雅生活", "呵护一生·温暖一城", "一图读懂·雅生活", "2025全年业绩概览",
    "基本盘稳健", "现金流向好", "截至2025年12月31日止12个月", "货币单位：人民币/元",
    "总收入", "128.9亿元", "毛利", "毛利率", "16.8亿元", "13.0%", "经调整净利润¹",
    "经调整净利润率", "7.84亿元", "6.1%", "-其中，非周期性业务²",
    "收入规模128.0亿元  占总收入99.3%", "周期性业务同比显著下降", "业务可持续性进一步提升",
    "1 剔除收并购带来无形资产摊销、商誉减值亏损、处置股权之损益、借款利息开支，以及公允价值计量且变动计入损益的金融资产的损益变动、利息收入、金融资产减值损失净额、预付款项减值亏损后归属于本公司股东之经调整净利润",
    "2 非周期业务板块为物业服务、业主增值服务、城市服务三个业务板块",
]


def load_env():
    path = Path(__file__).parent.parent / ".env"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.lstrip().startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


def error(stage, message, code=1):
    print(json.dumps({"status": "error", "stage": stage, "error": message}, ensure_ascii=False), file=sys.stderr)
    raise SystemExit(code)


def data_url(path):
    suffix = path.suffix.lower()
    mime = "image/png" if suffix == ".png" else "image/jpeg"
    raw = path.read_bytes()
    return f"data:{mime};base64," + base64.b64encode(raw).decode("ascii")


def extract_image(result):
    choices = result.get("choices", [])
    content = choices[0].get("message", {}).get("content", "") if choices else ""
    if isinstance(content, list):
        content = " ".join(str(part.get("text", part)) for part in content)
    if isinstance(content, dict):
        content = json.dumps(content)
    content = str(content)
    match = re.search(r"data:image/[^;]+;base64,([A-Za-z0-9+/=]+)", content)
    if match:
        return base64.b64decode(match.group(1))
    url_match = re.search(r"https?://[^\s\"'<>]+", content)
    if url_match:
        image_url = url_match.group(0).rstrip(").,;。")
        with urllib.request.urlopen(image_url, timeout=120) as response:
            return response.read()
    for key in ("b64_json", "image_base64"):
        match = re.search(rf'"{key}"\s*:\s*"([A-Za-z0-9+/=]+)"', content)
        if match:
            return base64.b64decode(match.group(1))
    preview = content[:500].replace("\n", " ")
    raise RuntimeError(f"GPT Image response has no image payload; keys={list(result)[:8]}; content={preview}")


def generate_long_image(style_ref, content_ref, api_size):
    api_key = os.environ.get("GPT_IMAGE_API_KEY")
    if not api_key:
        raise RuntimeError("未配置 GPT_IMAGE_API_KEY")
    prompt = """Redesign the second attached image into a single vertical long infographic using ONLY the visual language of the first attached image.

HARD RULES:
- Output exactly ONE single connected long image. Do not output grids, panels, small multiples, or separated cards.
- Keep the original reading order from the second image: top brand area, slogan, two-line title, city-life hero scene, dark green conclusion banner, date/currency note, total revenue block, two-column KPI pairs, non-cyclical business summary, bottom summary banner, and footnotes.
- Keep the original composition and asset relationships of the hero scene: mountains, city buildings, winding road, cyclist, walking people, dog, car, trees, clouds. Reinterpret them in the flat 2D collage-papercut style of the first image: white background, cyan sky, dark green outlines, grass/mint green, teal blue, bright yellow accents, rounded geometric slices, simple community characters, and eco/tech icons.
- Keep all original Chinese text, numbers, units, superscripts and footnotes EXACTLY as they appear in the second image. Do not translate, rewrite, omit or invent any text.
- Do not add photography, 3D, wood-paper texture, dark background, heavy shadow, glowing lines, unrelated decorations, or any new text.
- The final result must be a clean flat-vector corporate IR long infographic that looks like the second image restyled by the first image."""
    payload = {
        "model": MODEL, "size": api_size,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": data_url(style_ref)}},
            {"type": "image_url", "image_url": {"url": data_url(content_ref)}},
        ]}],
    }
    body = json.dumps(payload).encode("utf-8")
    url = os.environ.get("GPT_IMAGE_API_URL", DEFAULT_GPT_URL)
    last_error = None
    for attempt in range(3):
        request = urllib.request.Request(url, data=body, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=600) as response:
                return extract_image(json.loads(response.read().decode("utf-8")))
        except urllib.error.HTTPError as exc:
            last_error = f"GPT Image HTTP {exc.code}"
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise RuntimeError(last_error)
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = f"GPT Image connection failed: {exc}"
            if attempt == 2:
                raise RuntimeError(last_error)
        time.sleep((1, 3)[min(attempt, 1)])
    raise RuntimeError(last_error)


def validate_text(content_spec):
    source = content_spec.read_text(encoding="utf-8")
    normalized = source.replace("🟢", "").replace(" ", "").replace("\n", "")
    missing = [value for value in LOCKED_TEXT if value.replace(" ", "") not in normalized]
    if missing:
        raise ValueError("内容规格缺少锁定文本：" + "、".join(missing[:3]))


def main():
    parser = argparse.ArgumentParser(description="使用 GPT Image 2 Plus 生成单张中文业绩长图（不生成PPT）")
    parser.add_argument("--style-ref", required=True, type=Path)
    parser.add_argument("--content-ref", required=True, type=Path)
    parser.add_argument("--content-spec", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--api-size", default="1024x1536")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    load_env()
    try:
        for path in (args.style_ref, args.content_ref, args.content_spec):
            if not path.exists(): raise ValueError(f"输入文件不存在：{path}")
        if args.output.suffix.lower() != ".png": raise ValueError("输出文件必须为 PNG")
        if args.output.exists() and not args.overwrite: raise ValueError(f"输出已存在，请使用 --overwrite：{args.output}")
        Image.open(args.style_ref).convert("RGB"); Image.open(args.content_ref).convert("RGB"); validate_text(args.content_spec)
    except (ValueError, RuntimeError) as exc:
        error("input_validation", str(exc), 2)
    try:
        raw = generate_long_image(args.style_ref, args.content_ref, args.api_size)
        image = Image.open(io.BytesIO(raw)).convert("RGB")
        image.save(args.output, "PNG", optimize=True)
        with Image.open(args.output) as result:
            width, height = result.size
            if result.format != "PNG":
                raise RuntimeError("输出文件不是 PNG")
        print(json.dumps({"status": "success", "backend": "gpt", "model": MODEL, "output": str(args.output), "output_size_px": {"width": width, "height": height}, "target_size_px": {"width": 950, "height": 3677}, "locked_text_count": len(LOCKED_TEXT)}, ensure_ascii=False))
    except Exception as exc:
        error("gpt_generation", str(exc))

if __name__ == "__main__":
    main()
