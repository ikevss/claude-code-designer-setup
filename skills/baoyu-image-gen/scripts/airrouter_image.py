#!/usr/bin/env python3
"""airrouter 网关的 GPT Image 2 Plus 生图脚本（Chat-Completions 协议）。"""
import argparse
import base64
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

MODEL = "gpt-image-2-plus"
DEFAULT_API_URL = "https://airouter.cloud/v1/chat/completions"
MAX_RETRIES = 2
RETRY_DELAY = 3


def load_env():
    for path in [
        Path.home() / ".baoyu-skills/baoyu-image-gen/.env",
        Path(__file__).parent.parent / ".env",
    ]:
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.lstrip().startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())


def find_curl():
    """优先使用 Git 自带的 curl（OpenSSL 后端），避免 Windows schannel 的 SSL 问题。"""
    candidates = [
        r"D:\Program Files\Git\mingw64\bin\curl.exe",
        r"C:\Program Files\Git\mingw64\bin\curl.exe",
    ]
    for path in candidates:
        if Path(path).exists():
            return path
    # 尝试从 PATH 中查找 git 目录下的 curl
    for path_dir in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(path_dir) / "curl.exe"
        if candidate.exists() and "git" in str(candidate).lower():
            return str(candidate)
    return "curl"


def curl_post(url, payload, api_key):
    """通过 curl 发起 HTTPS 请求，规避 Python urllib 的 SSL 兼容问题。"""
    import tempfile
    curl_bin = find_curl()
    # 将 payload 写入临时文件，避免命令行过长
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(payload, f)
        payload_file = f.name
    try:
        cmd = [
            curl_bin, "--silent", "--show-error", "--fail",
            "--max-time", "600",
            "--request", "POST",
            "--header", f"Authorization: Bearer {api_key}",
            "--header", "Content-Type: application/json",
            "--data", f"@{payload_file}",
            "--noproxy", "*",
            url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
    finally:
        os.unlink(payload_file)
    if result.returncode != 0:
        raise RuntimeError(f"curl 请求失败 (code={result.returncode}): {result.stderr[:300]}")
    return json.loads(result.stdout)


def error(stage, message, code=1):
    print(json.dumps({"status": "error", "stage": stage, "error": message}, ensure_ascii=False), file=sys.stderr)
    raise SystemExit(code)


def data_url(path):
    suffix = Path(path).suffix.lower()
    mime = "image/png" if suffix == ".png" else "image/jpeg"
    image = Image.open(path).convert("RGB")
    # 压缩参考图，避免 payload 过大
    max_side = 1024
    if max(image.size) > max_side:
        ratio = max_side / max(image.size)
        image = image.resize((int(image.size[0] * ratio), int(image.size[1] * ratio)), Image.Resampling.LANCZOS)
    buffer = io.BytesIO()
    image.save(buffer, "JPEG", quality=70)
    return f"data:{mime};base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


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
    preview = content[:300].replace("\n", " ")
    raise RuntimeError(f"GPT Image response has no image payload; keys={list(result)[:6]}; content={preview}")


def generate(prompt, refs, size, api_key, api_url):
    api_key = api_key or os.environ.get("AIRROUTER_IMAGE_API_KEY")
    if not api_key:
        raise RuntimeError("未配置 AIRROUTER_IMAGE_API_KEY")
    content_parts = [{"type": "text", "text": prompt}]
    for ref in refs:
        content_parts.append({"type": "image_url", "image_url": {"url": data_url(ref)}})
    payload = {"model": MODEL, "size": size, "messages": [{"role": "user", "content": content_parts}]}
    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            if attempt > 0:
                print(f"🔄 第 {attempt} 次重试 airrouter...", file=sys.stderr)
                time.sleep(RETRY_DELAY * attempt)
            result = curl_post(api_url, payload, api_key)
            return extract_image(result)
        except RuntimeError as exc:
            message = str(exc)
            last_error = message
            if "HTTP 401" in message or "HTTP 403" in message or attempt == MAX_RETRIES:
                raise
            if "HTTP 429" not in message and "HTTP 500" not in message and "HTTP 502" not in message and "HTTP 503" not in message and "HTTP 504" not in message and "失败" not in message:
                raise
    raise RuntimeError(last_error)


def main():
    parser = argparse.ArgumentParser(description="airrouter 网关 GPT Image 2 Plus 生图")
    parser.add_argument("--prompt", required=True, help="图像生成提示词")
    parser.add_argument("--ref", action="append", default=[], help="参考图路径（可重复）")
    parser.add_argument("--output", required=True, type=Path, help="输出文件路径")
    parser.add_argument("--size", default="1024x1536", help="请求尺寸")
    parser.add_argument("--api-key", default="", help="API Key")
    parser.add_argument("--api-url", default="", help="API 端点")
    args = parser.parse_args()
    load_env()
    api_url = args.api_url or os.environ.get("AIRROUTER_IMAGE_API_URL", DEFAULT_API_URL)
    try:
        if not args.prompt.strip():
            raise ValueError("提示词不能为空")
        for ref in args.ref:
            if not Path(ref).exists():
                raise ValueError(f"参考图不存在：{ref}")
        if args.output.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            raise ValueError("输出格式仅支持 PNG/JPG/WebP")
        if args.output.exists():
            raise ValueError(f"输出已存在：{args.output}")
    except ValueError as exc:
        error("input_validation", str(exc), 2)
    try:
        raw = generate(args.prompt, args.ref, args.size, args.api_key, api_url)
        image = Image.open(io.BytesIO(raw)).convert("RGB")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        image.save(args.output, optimize=True)
        with Image.open(args.output) as result:
            width, height = result.size
        print(json.dumps({
            "status": "success",
            "backend": "airrouter",
            "model": MODEL,
            "output": str(args.output),
            "output_size_px": {"width": width, "height": height},
            "refs_used": len(args.ref),
        }, ensure_ascii=False))
    except Exception as exc:
        error("generation", str(exc))


if __name__ == "__main__":
    main()
