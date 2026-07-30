#!/usr/bin/env python3
"""
GPT Image 2 生图脚本 — aigateway.edgecloudapp.com
=================================================
独立脚本，不依赖任何 skill 框架。任何 AI 助手读取本文件即可使用。

## API 协议摘要

| 项目 | 值 |
|------|-----|
| 网关 URL | https://aigateway.edgecloudapp.com/v1/YOUR_GATEWAY_ID/gpt |
| 文生图 | POST {base}/images/generations |
| 参考图生图 | POST {base}/images/edits |
| Content-Type | application/json（不支持 multipart） |
| 模型 | gpt-image-2 |
| 返回格式 | data[0].b64_json（纯 base64，无 data URL 前缀） |

### 文生图请求体
{"model":"gpt-image-2","prompt":"...","size":"1024x1024","n":1}

### 参考图生图请求体（关键：image 是纯 base64，非 data URL）
{"model":"gpt-image-2","prompt":"...","image":"<raw_base64>","size":"1024x1792","n":1}

### curl 示例
```bash
# 文生图
curl -X POST {base}/images/generations \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"gpt-image-2","prompt":"...","size":"1024x1024","n":1}'

# 参考图生图
curl -X POST {base}/images/edits \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"gpt-image-2","prompt":"...","image":"<b64>","size":"1024x1792","n":1}'
```

## 环境变量
- AIGATEWAY_IMAGE_API_KEY：API 密钥
- AIGATEWAY_IMAGE_API_URL：网关基础 URL（可选，默认值如上）
"""

import argparse
import base64
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("需要安装 Pillow: pip install Pillow", file=sys.stderr)
    sys.exit(1)

API_KEY = "your-aigateway-jwt-token-here"
BASE_URL = "https://aigateway.edgecloudapp.com/v1/YOUR_GATEWAY_ID/gpt"
MODEL = "gpt-image-2"
MAX_RETRIES = 3
RETRY_DELAY = 5


def find_curl():
    """优先使用 Git 自带的 curl（OpenSSL 后端），避免 Windows schannel SSL 问题。"""
    for p in [
        r"D:\Program Files\Git\mingw64\bin\curl.exe",
        r"C:\Program Files\Git\mingw64\bin\curl.exe",
    ]:
        if Path(p).exists():
            return p
    return "curl"


def load_env():
    """从多个路径加载环境变量，不覆盖已有值。"""
    paths = [
        Path.home() / ".baoyu-skills/baoyu-image-gen/.env",
        Path(__file__).parent / ".env",
        Path.home() / ".aigateway-image.env",
    ]
    for path in paths:
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


def call_api(endpoint, payload, timeout=300):
    """通过 curl 调用 API，返回解析后的 JSON。"""
    curl_bin = find_curl()
    api_key = os.environ.get("AIGATEWAY_IMAGE_API_KEY", API_KEY)
    base = os.environ.get("AIGATEWAY_IMAGE_API_URL", BASE_URL)
    url = f"{base.rstrip('/')}/{endpoint.lstrip('/')}"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(payload, f)
        filepath = f.name

    try:
        cmd = [
            curl_bin, "--silent", "--show-error", "--fail",
            "--max-time", str(timeout),
            "--request", "POST",
            "--header", f"Authorization: Bearer {api_key}",
            "--header", "Content-Type: application/json",
            "--data", f"@{filepath}",
            "--noproxy", "*",
            url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
    finally:
        os.unlink(filepath)

    if result.returncode != 0:
        raise RuntimeError(f"curl failed (code={result.returncode}): {result.stderr[:500]}")
    resp = json.loads(result.stdout)
    if "error" in resp:
        raise RuntimeError(f"API error: {resp['error']}")
    return resp


def encode_ref_image(path, max_side=1536, quality=80):
    """将参考图压缩并编码为纯 base64 字符串（非 data URL）。"""
    img = Image.open(path).convert("RGB")
    if max(img.size) > max_side:
        ratio = max_side / max(img.size)
        img = img.resize(
            (int(img.size[0] * ratio), int(img.size[1] * ratio)),
            Image.Resampling.LANCZOS,
        )
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def decode_and_save(b64_data, output_path):
    """解码 base64 并保存为图片。"""
    raw = base64.b64decode(b64_data)
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, optimize=True)
    return img.size


def generate(prompt, output, size, ref=None):
    """
    核心生成函数。
    - ref: 参考图路径（可选），如果提供则走 /images/edits
    """
    if ref:
        if not Path(ref).exists():
            raise FileNotFoundError(f"参考图不存在: {ref}")
        image_b64 = encode_ref_image(ref)
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "image": image_b64,  # 纯 base64，非 data URL
            "size": size,
            "n": 1,
        }
        endpoint = "images/edits"
    else:
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "size": size,
            "n": 1,
        }
        endpoint = "images/generations"

    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            if attempt > 0:
                print(f"[retry {attempt}/{MAX_RETRIES}]", file=sys.stderr)
                time.sleep(RETRY_DELAY * attempt)
            resp = call_api(endpoint, payload)
            data = resp.get("data", [])
            if not data:
                raise RuntimeError(f"响应无 data 字段: {list(resp.keys())}")
            item = data[0]
            if "b64_json" in item:
                w, h = decode_and_save(item["b64_json"], output)
                return {"status": "success", "output": str(output), "size": f"{w}x{h}", "ref_used": ref is not None}
            elif "url" in item:
                import urllib.request
                with urllib.request.urlopen(item["url"], timeout=120) as r:
                    raw = r.read()
                img = Image.open(io.BytesIO(raw)).convert("RGB")
                Path(output).parent.mkdir(parents=True, exist_ok=True)
                img.save(output, optimize=True)
                return {"status": "success", "output": str(output), "size": f"{img.size[0]}x{img.size[1]}", "ref_used": ref is not None}
            raise RuntimeError(f"未知响应格式: {list(item.keys())}")
        except Exception as e:
            last_error = str(e)
            if "401" in last_error or "403" in last_error:
                break
    raise RuntimeError(last_error or "生成失败")


def main():
    parser = argparse.ArgumentParser(
        description="GPT Image 2 生图 (aigateway.edgecloudapp.com)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 文生图
  python aigateway_image.py -p "A cat" -o cat.png --size 1024x1024

  # 参考图生图（风格迁移）
  python aigateway_image.py -p "Make it blue" -r style.png -o result.png --size 1024x1792

  # 从文件读取提示词
  python aigateway_image.py -p "@prompt.txt" -o out.png
        """,
    )
    parser.add_argument("-p", "--prompt", required=True, help="提示词文本，或以 @ 开头从文件读取")
    parser.add_argument("-o", "--output", required=True, type=Path, help="输出图片路径 (.png/.jpg)")
    parser.add_argument("-r", "--ref", default=None, help="参考图路径（可选，用于风格迁移）")
    parser.add_argument("--size", default="1024x1024", help="输出尺寸 (默认 1024x1024)")
    args = parser.parse_args()

    load_env()

    # 支持 @filepath 从文件读取 prompt
    prompt = args.prompt
    if prompt.startswith("@"):
        prompt_path = Path(prompt[1:])
        if not prompt_path.exists():
            print(f"ERROR: 提示词文件不存在: {prompt_path}", file=sys.stderr)
            sys.exit(1)
        prompt = prompt_path.read_text(encoding="utf-8").strip()

    if args.output.exists():
        print(f"ERROR: 输出已存在: {args.output}", file=sys.stderr)
        sys.exit(1)

    try:
        result = generate(prompt, args.output, args.size, args.ref)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
