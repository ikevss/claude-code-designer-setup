#!/usr/bin/env python3
"""image2 (gpt-image-2) 图像生成脚本 - 单后端，含进度、重试与尺寸探测"""
import argparse, base64, json, os, ssl, sys, time, urllib.request, urllib.error
from pathlib import Path

# ── 从 .env 加载 ──────────────────────────────────────────
def load_env():
    for candidate in [
        Path(__file__).resolve().parent.parent / ".env",
        Path(os.path.expanduser("~")) / ".claude" / "skills" / "supir-slides" / ".env",
    ]:
        if candidate.exists():
            with open(candidate, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip())

load_env()

API_KEY = os.environ["GPT_IMAGE_API_KEY"]
BASE_URL = os.environ.get("GPT_IMAGE_API_URL", "https://aigateway.edgecloudapp.com/v1/1109fb65f197b62babfa3f56c0cf7cbc/gpt")
MODEL = os.environ.get("GPT_IMAGE_MODEL", "gpt-image-2")
GEN_URL = BASE_URL.rstrip("/") + "/images/generations"

RETRIES = 2
RETRY_DELAY = 3

# 16:9 尺寸表，按像素量降序（image2 要求宽高均被 16 整除）
SIZE_CANDIDATES = [
    "1792x1024",   # 16:9, 最高像素, image2 验证通过
    "1536x864",    # 16:9, 备用
]


def _ssl_ctx():
    ctx = ssl.create_default_context()
    return ctx


def _call(prompt, size, timeout=300):
    """返回 (image_bytes, backend_label) 或 raise"""
    payload = {"model": MODEL, "prompt": prompt, "size": size}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        GEN_URL, data=data,
        headers={"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx()) as r:
            result = json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise RuntimeError("HTTP %d: %s" % (e.code, body[:500])) from e

    d = result.get("data", [{}])[0]
    b64 = d.get("b64_json")
    if b64:
        return base64.b64decode(b64), MODEL
    url = d.get("url")
    if url:
        with urllib.request.urlopen(url, timeout=120, context=_ssl_ctx()) as ir:
            return ir.read(), MODEL
    raise RuntimeError("响应无图片数据: " + json.dumps(result, ensure_ascii=False)[:300])


def generate(prompt, size=None, output=None):
    """
    单张生成。size 为空时自动探测首个可用的 16:9 尺寸。
    返回 (image_bytes, size_used, backend) 三元组。
    """
    if size:
        sizes = [size]
    else:
        sizes = SIZE_CANDIDATES

    last_err = None
    for sz in sizes:
        for attempt in range(RETRIES + 1):
            if attempt > 0:
                time.sleep(RETRY_DELAY)
            try:
                img, backend = _call(prompt, sz)
                print("image2 OK  %s  %d KB" % (sz, len(img) // 1024), file=sys.stderr)
                if output:
                    with open(output, "wb") as f:
                        f.write(img)
                return img, sz, backend
            except Exception as e:
                last_err = e
                print("image2 %s attempt %d fail: %s" % (sz, attempt + 1, e), file=sys.stderr)
    raise RuntimeError("所有尺寸与重试均失败。最后错误: %s" % last_err)


def generate_batch(prompts, output_dir=".", size=None):
    """
    批量生成。prompts: [{"prompt":..., "output":"slide-01.png"}, ...] 或纯字符串列表。
    支持断点续传：已存在且 >30KB 跳过。
    """
    total = len(prompts)
    results, errors = [], []
    for i, p in enumerate(prompts, 1):
        if isinstance(p, str):
            prompt, out_fn = p, "slide-%02d.png" % i
        else:
            prompt = p.get("prompt", p.get("text", ""))
            out_fn = p.get("output", "slide-%02d.png" % i)
        out_path = os.path.join(output_dir, out_fn)

        if os.path.exists(out_path) and os.path.getsize(out_path) > 30000:
            results.append({"page": i, "output": out_path, "size_used": "(cached)", "status": "cached"})
            print("[%d/%d] %s (cached)" % (i, total, out_fn), file=sys.stderr)
            continue

        print("\n[%d/%d] %s" % (i, total, out_fn), file=sys.stderr)
        try:
            _, sz_used, backend = generate(prompt, size=size, output=out_path)
            results.append({"page": i, "output": out_path, "size_used": sz_used, "backend": backend, "status": "success"})
        except Exception as e:
            errors.append({"page": i, "error": str(e)})
            print("FAIL [%d/%d] %s" % (i, total, e), file=sys.stderr)
    return results, errors


def main():
    p = argparse.ArgumentParser(description="image2 (gpt-image-2) 图像生成")
    p.add_argument("--prompt", help="单页提示词")
    p.add_argument("--prompts-file", help="提示词列表文件（批量模式，每行一个 JSON 或纯文本）")
    p.add_argument("--size", default=None, help="输出尺寸，空=自动探测（默认自动探测 16:9）")
    p.add_argument("--output", default="output.png", help="输出路径（单页）")
    p.add_argument("--output-dir", default=".", help="输出目录（批量）")
    p.add_argument("--probe-sizes", action="store_true", help="探测所有支持的 16:9 尺寸")
    args = p.parse_args()

    if args.probe_sizes:
        print("探测 16:9 尺寸...", file=sys.stderr)
        for sz in SIZE_CANDIDATES + ["1920x1080"]:
            try:
                _call("a solid blue square on white, no text", sz)
                print(sz, "→ OK", file=sys.stderr)
            except Exception as e:
                print(sz, "→ FAIL:", str(e)[:120], file=sys.stderr)
        return 0

    if args.prompts_file:
        with open(args.prompts_file, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
        prompts = []
        for ln in lines:
            try:
                prompts.append(json.loads(ln))
            except json.JSONDecodeError:
                prompts.append({"prompt": ln})
        results, errors = generate_batch(prompts, args.output_dir, args.size)
        out = {"status": "completed", "total": len(prompts), "success": len(results),
               "failed": len(errors), "results": results, "errors": errors}
        print(json.dumps(out, ensure_ascii=False))
        return 0 if not errors else 1

    if not args.prompt:
        p.error("需要 --prompt 或 --prompts-file")

    generate(args.prompt, size=args.size, output=args.output)
    print(json.dumps({"status": "success", "output": args.output, "size_used": args.size or "auto"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
