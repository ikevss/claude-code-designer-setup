#!/usr/bin/env python3
"""风格管理脚本 - 保存/列出/加载风格配置"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime


# 默认风格目录
DEFAULT_STYLES_DIR = Path(__file__).parent.parent / "styles"


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


def get_styles_dir():
    """获取风格目录"""
    return Path(os.environ.get("SUPIR_STYLES_DIR", DEFAULT_STYLES_DIR))


def list_styles():
    """列出所有可用风格"""
    styles_dir = get_styles_dir()

    if not styles_dir.exists():
        print("暂无可用风格")
        return []

    styles = []
    for style_file in styles_dir.glob("*.md"):
        style_name = style_file.stem
        # 读取风格文件获取描述
        try:
            with open(style_file, "r", encoding="utf-8") as f:
                content = f.read()
                # 提取第一行作为描述
                lines = content.strip().split("\n")
                description = lines[0].lstrip("# ").strip() if lines else ""
                styles.append({
                    "name": style_name,
                    "description": description,
                    "path": str(style_file)
                })
        except Exception:
            styles.append({
                "name": style_name,
                "description": "",
                "path": str(style_file)
            })

    return styles


def get_style(style_name):
    """获取指定风格的配置"""
    styles_dir = get_styles_dir()
    style_file = styles_dir / f"{style_name}.md"

    if not style_file.exists():
        raise FileNotFoundError(f"风格不存在: {style_name}")

    with open(style_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 解析风格配置
    style_config = {
        "name": style_name,
        "path": str(style_file),
        "content": content,
        "colors": {},
        "fonts": {},
        "layout": {}
    }

    # 简单解析颜色系统
    for line in content.split("\n"):
        if "背景色" in line and "#" in line:
            style_config["colors"]["background"] = line.split("#")[1].split("（")[0].strip()
        elif "主色" in line and "#" in line:
            style_config["colors"]["primary"] = line.split("#")[1].split("（")[0].strip()
        elif "强调色" in line and "#" in line:
            style_config["colors"]["accent"] = line.split("#")[1].split("（")[0].strip()

    return style_config


def save_style(name, content, description=""):
    """保存风格配置"""
    styles_dir = get_styles_dir()
    styles_dir.mkdir(parents=True, exist_ok=True)

    style_file = styles_dir / f"{name}.md"

    # 构建风格文件内容
    if not content.startswith("#"):
        content = f"# {name}\n\n{content}"

    with open(style_file, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "name": name,
        "path": str(style_file),
        "created_at": datetime.now().isoformat()
    }


def delete_style(style_name):
    """删除风格"""
    styles_dir = get_styles_dir()
    style_file = styles_dir / f"{style_name}.md"

    if not style_file.exists():
        raise FileNotFoundError(f"风格不存在: {style_name}")

    style_file.unlink()
    return {"name": style_name, "deleted": True}


def main():
    parser = argparse.ArgumentParser(description="风格管理")
    sub = parser.add_subparsers(dest="command", required=True)

    # list 命令
    p = sub.add_parser("list", help="列出所有可用风格")
    p.add_argument("--json", action="store_true", help="输出 JSON 格式")

    # get 命令
    p = sub.add_parser("get", help="获取指定风格配置")
    p.add_argument("name", help="风格名称")

    # save 命令
    p = sub.add_parser("save", help="保存风格配置")
    p.add_argument("name", help="风格名称")
    p.add_argument("--content", default="", help="风格内容")
    p.add_argument("--file", default="", help="从文件读取内容")

    # delete 命令
    p = sub.add_parser("delete", help="删除风格")
    p.add_argument("name", help="风格名称")

    args = parser.parse_args()

    load_env()

    try:
        if args.command == "list":
            styles = list_styles()
            if args.json:
                print(json.dumps(styles, ensure_ascii=False, indent=2))
            else:
                if not styles:
                    print("暂无可用风格")
                else:
                    for style in styles:
                        print(f"{style['name']} | {style['description']}")

        elif args.command == "get":
            style = get_style(args.name)
            print(json.dumps(style, ensure_ascii=False, indent=2))

        elif args.command == "save":
            content = args.content
            if args.file:
                with open(args.file, "r", encoding="utf-8") as f:
                    content = f.read()
            result = save_style(args.name, content)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif args.command == "delete":
            result = delete_style(args.name)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        return 0

    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
