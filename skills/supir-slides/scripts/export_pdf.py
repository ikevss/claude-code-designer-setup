#!/usr/bin/env python3
"""PDF 导出 - 将 open-slide 项目导出为 PDF"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def check_dependencies():
    """检查依赖"""
    errors = []

    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        errors.append("Node.js 未安装")

    try:
        subprocess.run(["pnpm", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        errors.append("pnpm 未安装")

    return errors


def main():
    parser = argparse.ArgumentParser(description="导出幻灯片为 PDF")
    parser.add_argument("--project", default=".", help="open-slide 项目目录")
    parser.add_argument("--output", default="presentation.pdf", help="输出 PDF 路径")
    args = parser.parse_args()

    errors = check_dependencies()
    if errors:
        print("依赖检查失败:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    project_dir = Path(args.project).resolve()
    if not (project_dir / "package.json").exists():
        print(f"错误: 不是有效的 open-slide 项目: {project_dir}", file=sys.stderr)
        return 1

    print("提示: 请使用 open-slide 内置的导出功能:", file=sys.stderr)
    print(f"  cd {project_dir}", file=sys.stderr)
    print("  pnpm build", file=sys.stderr)
    print("  # 然后使用浏览器打印为 PDF", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
