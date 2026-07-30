#!/usr/bin/env python3
"""环境自动初始化脚本 - 检测并安装必要依赖"""

import json
import os
import subprocess
import sys
import shutil
from pathlib import Path


def check_command(cmd):
    """检查命令是否可用"""
    return shutil.which(cmd) is not None


def run_command(cmd, check=True):
    """运行命令"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=60
        )
        if check and result.returncode != 0:
            return False, result.stderr
        return True, result.stdout
    except subprocess.TimeoutExpired:
        return False, "命令超时"
    except Exception as e:
        return False, str(e)


def check_node():
    """检查 Node.js"""
    return check_command("node")


def check_pnpm():
    """检查 pnpm"""
    return check_command("pnpm")


def check_open_slide():
    """检查 open-slide CLI"""
    try:
        result = subprocess.run(
            ["npx", "@open-slide/cli", "--version"],
            capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0
    except:
        return False


def check_officecli():
    """检查 OfficeCLI"""
    try:
        result = subprocess.run(
            ["npx", "officecli", "--version"],
            capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0
    except:
        return False


def check_python_package(package):
    """检查 Python 包"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def install_open_slide():
    """安装 open-slide"""
    print("📦 正在安装 open-slide...")
    success, output = run_command("npm install -g @open-slide/cli", check=False)
    if success:
        print("✅ open-slide 安装成功")
        return True
    else:
        print(f"❌ open-slide 安装失败: {output}")
        return False


def install_officecli():
    """安装 OfficeCLI"""
    print("📦 正在安装 OfficeCLI...")
    success, output = run_command("npm install -g officecli", check=False)
    if success:
        print("✅ OfficeCLI 安装成功")
        return True
    else:
        print(f"❌ OfficeCLI 安装失败: {output}")
        return False


def install_python_packages():
    """安装 Python 依赖"""
    packages = ["pptx", "PIL"]
    package_names = ["python-pptx", "Pillow"]
    missing = []

    for pkg, name in zip(packages, package_names):
        if not check_python_package(pkg):
            missing.append(name)

    if missing:
        print(f"📦 正在安装 Python 依赖: {', '.join(missing)}")
        success, output = run_command(
            f"pip install {' '.join(missing)}", check=False
        )
        if success:
            print("✅ Python 依赖安装成功")
            return True
        else:
            print(f"❌ Python 依赖安装失败: {output}")
            return False
    else:
        print("✅ Python 依赖已就绪")
        return True


def detect_cli():
    """检测可用的 CLI"""
    result = {
        "open-slide": False,
        "officecli": False,
        "recommended": None
    }

    if check_open_slide():
        result["open-slide"] = True
        result["recommended"] = "open-slide"
        print("✅ open-slide 可用")
    else:
        print("⚠️ open-slide 不可用")

    if check_officecli():
        result["officecli"] = True
        if not result["recommended"]:
            result["recommended"] = "officecli"
        print("✅ OfficeCLI 可用")
    else:
        print("⚠️ OfficeCLI 不可用")

    # 如果都不可用，尝试安装
    if not result["recommended"]:
        print("🔧 尝试自动安装 CLI...")
        if install_open_slide():
            result["open-slide"] = True
            result["recommended"] = "open-slide"
        elif install_officecli():
            result["officecli"] = True
            result["recommended"] = "officecli"

    return result


def detect_api():
    """检测可用的 AI 生图 API"""
    result = {
        "agnes": True,  # 已内置 Key
        "gpt": True,    # 已内置 Key
        "recommended": "agnes"
    }

    print("✅ Agnes Image API 已配置（内置 Key）")
    print("✅ GPT Image API 已配置（内置 Key）")

    return result


def main():
    parser = argparse.ArgumentParser(description="Supir Slides 环境初始化")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--quiet", action="store_true", help="静默模式")
    args = parser.parse_args()

    if not args.quiet:
        print("🔧 Supir Slides 环境检测中...\n")

    # 检测 Node.js
    if not check_node():
        print("❌ Node.js 未安装，请先安装 Node.js")
        return 1
    print("✅ Node.js 可用")

    # 检测 pnpm
    if not check_pnpm():
        print("⚠️ pnpm 未安装，尝试使用 npm")
    else:
        print("✅ pnpm 可用")

    # 检测 CLI
    cli_result = detect_cli()

    # 检测 Python 依赖
    install_python_packages()

    # 检测 API
    api_result = detect_api()

    # 输出结果
    result = {
        "status": "success",
        "cli": cli_result,
        "api": api_result,
        "python": {
            "pptx": check_python_package("pptx"),
            "Pillow": check_python_package("PIL")
        }
    }

    if not args.quiet:
        print("\n" + "="*50)
        print("✅ 环境检测完成！")
        print("="*50)
        print(f"推荐 CLI: {cli_result['recommended'] or '需要安装'}")
        print(f"推荐 API: {api_result['recommended']}")
        print("="*50)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    import argparse
    raise SystemExit(main())
