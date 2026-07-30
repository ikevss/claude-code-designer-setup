#!/usr/bin/env python3
"""
GordenImage2PPTX — Core Image Generator Module

Reads configuration from the skill's own .env file, provides a unified
generate_image() function for all image extraction tasks (B2 background,
B3 frame, B4 icons).

This module uses GPT Image 2 API (OpenAI-compatible /v1/images/generations
endpoint) to replace Codex built-in imagegen when running in non-Codex
environments.

Usage from other scripts:
    from image_generator import ImageGenerator

    gen = ImageGenerator()  # loads .env automatically
    path = gen.generate("extract clean background...", "background.png")
"""

from __future__ import annotations

import base64
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional


# ── Auto-install missing dependencies ────────────────────────────
_REQUIRED_PACKAGES = {
    "requests": "requests",
    "dotenv": "python-dotenv",
    "pptx": "python-pptx",
    "PIL": "pillow",
    "numpy": "numpy",
}


def _ensure_deps() -> None:
    """Check required packages and auto-install any that are missing."""
    missing = []
    for import_name, pip_name in _REQUIRED_PACKAGES.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pip_name)

    if not missing:
        return

    print(f"[GordenImage2PPTX] 首次运行，自动安装缺少的依赖: {', '.join(missing)}")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", *missing],
            stdout=subprocess.DEVNULL,
        )
        print(f"[GordenImage2PPTX] 依赖安装完成")
    except subprocess.CalledProcessError as exc:
        raise SystemExit(
            f"[GordenImage2PPTX] 自动安装失败，请手动执行:\n"
            f"  pip install {' '.join(missing)}"
        ) from exc


_ensure_deps()

try:
    import requests
except ImportError:
    raise SystemExit(
        "requests is required. Install with: python -m pip install requests"
    )

# ── Locate the skill root (parent of scripts/) ──────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPT_DIR.parent

# ── Load .env from skill root ────────────────────────────────────
def _load_env() -> None:
    """Load .env from the skill root if python-dotenv is available."""
    env_path = _SKILL_ROOT / ".env"
    if not env_path.exists():
        return
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path, override=False)
    except ImportError:
        # Fallback: parse .env manually (simple KEY=VALUE)
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value


_load_env()


class ImageGenerator:
    """Generate images via OpenAI-compatible /v1/images/generations endpoint.

    Used for:
    - B2: Extracting/regenerating clean backgrounds
    - B3: Extracting frame/skeleton layers on chroma-key background
    - B4: Generating icon/element sheets on chroma-key background
    """

    def __init__(self, env_prefix: str = "GPT_IMAGE"):
        self.api_key = os.environ.get(f"{env_prefix}_API_KEY", "")
        self.api_url = os.environ.get(f"{env_prefix}_API_URL", "https://api.openai.com/v1")
        self.model = os.environ.get(f"{env_prefix}_MODEL", "gpt-image-2")
        self.size = os.environ.get(f"{env_prefix}_SIZE", "1920x1080")
        self.timeout = int(os.environ.get(f"{env_prefix}_TIMEOUT", "300"))
        self.max_retries = int(os.environ.get(f"{env_prefix}_MAX_RETRIES", "3"))

        # Normalize: ensure API_URL ends with the endpoint path
        if not self.api_url.endswith("/images/generations"):
            self._gen_url = self.api_url.rstrip("/") + "/images/generations"
        else:
            self._gen_url = self.api_url

        self._available = bool(self.api_key)

    @property
    def available(self) -> bool:
        """Whether the API is configured and ready to use."""
        return self._available

    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate(
        self,
        prompt: str,
        filename: str,
        out_dir: Path | str,
        *,
        size: Optional[str] = None,
        n: int = 1,
    ) -> Optional[Path]:
        """
        Generate one image and save it to out_dir/filename.

        Returns the Path on success, None on failure.
        """
        if not self._available:
            print(
                f"  [{filename}] ImageGenerator not configured: "
                f"set GPT_IMAGE_API_KEY in .env",
                file=sys.stderr,
            )
            return None

        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / filename

        payload = {
            "model": self.model,
            "prompt": prompt,
            "n": n,
            "size": size or self.size,
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                resp = requests.post(
                    self._gen_url,
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get("data", [])
                    if items:
                        item = items[0]
                        if "b64_json" in item:
                            img_bytes = base64.b64decode(item["b64_json"])
                            out_path.write_bytes(img_bytes)
                            return out_path
                        elif "url" in item:
                            img_resp = requests.get(item["url"], timeout=60)
                            out_path.write_bytes(img_resp.content)
                            return out_path
                # Non-200 or empty data
                print(
                    f"  [{filename}] attempt {attempt}/{self.max_retries}: "
                    f"HTTP {resp.status_code}",
                    file=sys.stderr,
                )
            except requests.exceptions.Timeout:
                print(
                    f"  [{filename}] attempt {attempt}/{self.max_retries}: timeout",
                    file=sys.stderr,
                )
            except Exception as exc:
                print(
                    f"  [{filename}] attempt {attempt}/{self.max_retries}: {exc}",
                    file=sys.stderr,
                )
            if attempt < self.max_retries:
                time.sleep(3)

        return None

    def generate_batch(
        self,
        tasks: list[dict],
        out_dir: Path | str,
        *,
        delay: float = 1.0,
    ) -> dict[str, Optional[Path]]:
        """
        Generate a batch of images.

        tasks: list of {"id": str, "filename": str, "prompt": str}
        Returns: {task_id: Path_or_None}
        """
        results = {}
        total = len(tasks)
        for i, task in enumerate(tasks):
            tid = task["id"]
            fname = task["filename"]
            prompt = task["prompt"]
            print(
                f"[{i+1}/{total}] {tid} ...",
                end=" ",
                flush=True,
            )
            path = self.generate(prompt, fname, out_dir)
            results[tid] = path
            print("OK" if path else "FAIL")
            if delay > 0 and i < total - 1:
                time.sleep(delay)
        return results


# ── CLI entry point ──────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="GordenImage2PPTX — Test image generation"
    )
    parser.add_argument(
        "--prompt",
        default="A clean office background with no text or icons, 16:9 ratio",
    )
    parser.add_argument("--out", default="test_output.png")
    args = parser.parse_args()

    gen = ImageGenerator()
    if not gen.available:
        print("ERROR: ImageGenerator not configured. Set GPT_IMAGE_API_KEY in .env")
        sys.exit(1)

    print(f"Model: {gen.model}")
    print(f"URL:   {gen._gen_url}")
    print(f"Size:  {gen.size}")
    path = gen.generate(args.prompt, args.out, Path("."))
    if path:
        print(f"OK: {path} ({path.stat().st_size} bytes)")
    else:
        print("FAILED")
        sys.exit(1)
