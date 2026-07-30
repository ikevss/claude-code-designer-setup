#!/usr/bin/env python3
"""版本管理脚本 - 管理幻灯片项目的版本快照"""

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


VERSIONS_DIR = ".supir-slides/versions"
MANIFEST_FILE = "manifest.json"


def get_project_root():
    """获取项目根目录"""
    return Path.cwd()


def get_versions_dir():
    """获取版本目录"""
    return get_project_root() / VERSIONS_DIR


def load_manifest():
    """加载版本清单"""
    manifest_path = get_versions_dir() / MANIFEST_FILE
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return {"versions": [], "current": None}


def save_manifest(manifest):
    """保存版本清单"""
    manifest_path = get_versions_dir() / MANIFEST_FILE
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def cmd_snapshot(args):
    """创建版本快照"""
    versions_dir = get_versions_dir()
    versions_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest()

    # 生成版本号
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    version_id = f"v{timestamp}"

    # 创建版本目录
    version_dir = versions_dir / version_id
    version_dir.mkdir(parents=True, exist_ok=True)

    # 复制当前项目文件
    project_root = get_project_root()
    files_copied = 0

    for item in project_root.iterdir():
        if item.name.startswith("."):
            continue
        if item.name == "node_modules":
            continue

        dest = version_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, ignore=shutil.ignore_patterns(".git", "node_modules"))
        else:
            shutil.copy2(item, dest)
        files_copied += 1

    # 更新清单
    version_info = {
        "id": version_id,
        "timestamp": dt.datetime.now().isoformat(),
        "message": args.message or f"快照 {version_id}",
        "files_count": files_copied
    }
    manifest["versions"].append(version_info)
    manifest["current"] = version_id
    save_manifest(manifest)

    print(json.dumps({
        "status": "success",
        "version": version_id,
        "message": version_info["message"],
        "files_count": files_copied
    }))
    return 0


def cmd_list(args):
    """列出所有版本"""
    manifest = load_manifest()

    if not manifest["versions"]:
        print("暂无版本快照")
        return 0

    for v in manifest["versions"]:
        current = " [当前]" if v["id"] == manifest.get("current") else ""
        print(f"{v['id']}{current} | {v['timestamp']} | {v['message']}")

    return 0


def cmd_restore(args):
    """恢复到指定版本"""
    manifest = load_manifest()

    version_info = next((v for v in manifest["versions"] if v["id"] == args.version), None)
    if not version_info:
        print(f"版本不存在: {args.version}", file=sys.stderr)
        return 1

    versions_dir = get_versions_dir()
    version_dir = versions_dir / args.version

    if not version_dir.exists():
        print(f"版本目录不存在: {version_dir}", file=sys.stderr)
        return 1

    # 备份当前版本
    if manifest.get("current"):
        print(f"备份当前版本 {manifest['current']}...")
        cmd_snapshot argparse.Namespace(message=f"恢复前自动备份")

    # 恢复文件
    project_root = get_project_root()
    for item in version_dir.iterdir():
        dest = project_root / item.name
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    manifest["current"] = args.version
    save_manifest(manifest)

    print(json.dumps({
        "status": "success",
        "restored": args.version,
        "message": version_info["message"]
    }))
    return 0


def cmd_diff(args):
    """对比两个版本差异"""
    versions_dir = get_versions_dir()
    v1_dir = versions_dir / args.version1
    v2_dir = versions_dir / args.version2

    if not v1_dir.exists():
        print(f"版本不存在: {args.version1}", file=sys.stderr)
        return 1
    if not v2_dir.exists():
        print(f"版本不存在: {args.version2}", file=sys.stderr)
        return 1

    # 使用 diff 命令对比
    try:
        result = subprocess.run(
            ["diff", "-r", str(v1_dir), str(v2_dir)],
            capture_output=True, text=True
        )
        if result.stdout:
            print(result.stdout)
        else:
            print("两个版本相同")
    except Exception as e:
        print(f"对比失败: {e}", file=sys.stderr)
        return 1

    return 0


def main():
    parser = argparse.ArgumentParser(description="幻灯片版本管理")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("snapshot", help="创建版本快照")
    p.add_argument("--message", "-m", default="", help="版本说明")

    sub.add_parser("list", help="列出所有版本")

    p = sub.add_parser("restore", help="恢复到指定版本")
    p.add_argument("version", help="版本 ID")

    p = sub.add_parser("diff", help="对比两个版本")
    p.add_argument("version1", help="版本 1")
    p.add_argument("version2", help="版本 2")

    args = parser.parse_args()

    commands = {
        "snapshot": cmd_snapshot,
        "list": cmd_list,
        "restore": cmd_restore,
        "diff": cmd_diff
    }

    return commands[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
