#!/usr/bin/env python3
"""AI 图像生成脚本 - 双 API 自动切换，含进度和重试"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


# 从 .env 文件读取配置
def load_env():
    """从 .env 文件加载环境变量"""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())

load_env()

# API 配置
DEFAULT_AGNES_URL = "https://apihub.agnes-ai.com/v1/images/generations"
DEFAULT_GPT_URL = "https://aigateway.edgecloudapp.com/v1/YOUR_GATEWAY_ID/gpt"

# 重试配置
MAX_RETRIES = 2
RETRY_DELAY = 3


def generate_with_agnes(prompt, size="1920x1080", api_key=None):
    """使用 Agnes Image API 生成图片"""
    api_url = os.environ.get("AGNES_API_URL", DEFAULT_AGNES_URL)
    api_key = api_key or os.environ.get("AGNES_API_KEY")

    if not api_key:
        raise ValueError("未配置 AGNES_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "agnes-image-2.1-flash",
        "prompt": prompt,
        "size": size,
        "return_base64": True
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(api_url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"Agnes API 错误 {e.code}: {body}") from e
    except Exception as e:
        raise RuntimeError(f"Agnes API 连接失败: {e}") from e

    if "data" in result and len(result["data"]) > 0:
        b64_data = result["data"][0].get("b64_json")
        if b64_data:
            return base64.b64decode(b64_data)
        url = result["data"][0].get("url")
        if url:
            with urllib.request.urlopen(url, timeout=60) as img_resp:
                return img_resp.read()

    raise RuntimeError(f"Agnes API 返回异常: {json.dumps(result, ensure_ascii=False)}")


def generate_with_gpt_image(prompt, size="1920x1080", api_key=None):
    """使用 GPT Image API 生成图片"""
    api_url = os.environ.get("GPT_IMAGE_API_URL", DEFAULT_GPT_URL)
    api_key = api_key or os.environ.get("GPT_IMAGE_API_KEY")

    if not api_key:
        raise ValueError("未配置 GPT_IMAGE_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-image-2-plus",
        "messages": [
            {"role": "user", "content": f"Generate an image: {prompt}"}
        ]
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(api_url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"GPT Image API 错误 {e.code}: {body}") from e
    except Exception as e:
        raise RuntimeError(f"GPT Image API 连接失败: {e}") from e

    if "choices" in result and len(result["choices"]) > 0:
        content = result["choices"][0].get("message", {}).get("content", "")
        if "data:image" in content:
            b64_part = content.split("base64,")[1].split('"')[0]
            return base64.b64decode(b64_part)

    raise RuntimeError(f"GPT Image API 返回异常: {json.dumps(result, ensure_ascii=False)}")


def generate_with_retry(func, prompt, size, api_key, backend_name):
    """带重试的生成函数"""
    last_error = None

    for attempt in range(MAX_RETRIES + 1):
        try:
            if attempt > 0:
                print(f"🔄 第 {attempt} 次重试 {backend_name}...", file=sys.stderr)
                time.sleep(RETRY_DELAY)

            image_data = func(prompt, size, api_key)
            return image_data

        except Exception as e:
            last_error = e
            print(f"⚠️ {backend_name} 失败: {e}", file=sys.stderr)

    raise last_error


def generate_with_auto_switch(prompt, size="1920x1080", api_key=None):
    """自动切换 API：Agnes 优先，GPT Image 备用"""
    errors = []

    # 尝试 Agnes
    try:
        print("🔄 尝试 Agnes Image API...", file=sys.stderr)
        image_data = generate_with_retry(generate_with_agnes, prompt, size, api_key, "Agnes")
        print("✅ Agnes Image 生成成功", file=sys.stderr)
        return image_data, "agnes"
    except Exception as e:
        errors.append(f"Agnes: {e}")

    # 尝试 GPT Image
    try:
        print("🔄 切换到 GPT Image API...", file=sys.stderr)
        image_data = generate_with_retry(generate_with_gpt_image, prompt, size, api_key, "GPT Image")
        print("✅ GPT Image 生成成功", file=sys.stderr)
        return image_data, "gpt"
    except Exception as e:
        errors.append(f"GPT Image: {e}")

    # 都失败
    raise RuntimeError(f"所有 API 都失败:\n" + "\n".join(errors))


def generate_batch(prompts, size="1920x1080", output_dir=".", backend="auto"):
    """批量生成图片，带进度提示"""
    total = len(prompts)
    results = []
    errors = []

    for i, prompt_data in enumerate(prompts, 1):
        prompt = prompt_data if isinstance(prompt_data, str) else prompt_data.get("prompt", "")
        output_file = prompt_data.get("output", f"slide-{i:02d}.png") if isinstance(prompt_data, dict) else f"slide-{i:02d}.png"
        output_path = os.path.join(output_dir, output_file)

        print(f"\n🔄 正在生成第 {i}/{total} 页...", file=sys.stderr)

        try:
            if backend == "agnes":
                image_data = generate_with_retry(generate_with_agnes, prompt, size, None, "Agnes")
                backend_used = "agnes"
            elif backend == "gpt":
                image_data = generate_with_retry(generate_with_gpt_image, prompt, size, None, "GPT Image")
                backend_used = "gpt"
            else:
                image_data, backend_used = generate_with_auto_switch(prompt, size)

            with open(output_path, "wb") as f:
                f.write(image_data)

            results.append({
                "page": i,
                "output": output_path,
                "status": "success"
            })

            print(f"✅ 第 {i}/{total} 页生成完成", file=sys.stderr)

        except Exception as e:
            errors.append({
                "page": i,
                "error": str(e)
            })
            print(f"❌ 第 {i}/{total} 页生成失败: {e}", file=sys.stderr)

    return results, errors


def main():
    parser = argparse.ArgumentParser(description="AI 图像生成（双 API 自动切换，含进度和重试）")
    parser.add_argument("--prompt", help="图像生成提示词（单页模式）")
    parser.add_argument("--prompts-file", help="提示词列表文件（批量模式）")
    parser.add_argument("--size", default="1920x1080", help="输出尺寸")
    parser.add_argument("--output", default="output.png", help="输出文件路径（单页模式）")
    parser.add_argument("--output-dir", default=".", help="输出目录（批量模式）")
    parser.add_argument("--backend", choices=["agnes", "gpt", "auto"], default="auto",
                        help="图像生成后端 (默认: auto)")
    parser.add_argument("--api-key", default="", help="API Key (可选)")
    args = parser.parse_args()

    # 批量模式
    if args.prompts_file:
        try:
            with open(args.prompts_file, "r", encoding="utf-8") as f:
                prompts = [line.strip() for line in f if line.strip()]

            results, errors = generate_batch(prompts, args.size, args.output_dir, args.backend)

            output = {
                "status": "completed",
                "total": len(prompts),
                "success": len(results),
                "failed": len(errors),
                "results": results,
                "errors": errors
            }
            print(json.dumps(output, ensure_ascii=False))
            return 0 if not errors else 1

        except Exception as e:
            print(json.dumps({"status": "error", "error": str(e)}), file=sys.stderr)
            return 1

    # 单页模式
    if not args.prompt:
        print("错误：需要提供 --prompt 或 --prompts-file", file=sys.stderr)
        return 1

    print(f"🔄 正在生成图片...", file=sys.stderr)

    try:
        if args.backend == "agnes":
            image_data = generate_with_retry(generate_with_agnes, args.prompt, args.size, args.api_key, "Agnes")
            backend_used = "agnes"
        elif args.backend == "gpt":
            image_data = generate_with_retry(generate_with_gpt_image, args.prompt, args.size, args.api_key, "GPT Image")
            backend_used = "gpt"
        else:
            image_data, backend_used = generate_with_auto_switch(args.prompt, args.size, args.api_key)

        with open(args.output, "wb") as f:
            f.write(image_data)

        print("✅ 生成完成", file=sys.stderr)

        result = {
            "status": "success",
            "output": args.output,
            "backend": backend_used,
            "size": len(image_data)
        }
        print(json.dumps(result))
        return 0

    except Exception as e:
        print(f"❌ 生成失败: {e}", file=sys.stderr)
        result = {"status": "error", "error": str(e)}
        print(json.dumps(result), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
