#!/usr/bin/env python3
"""模板库管理 - 管理可复用的幻灯片模板"""

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path


DEFAULT_ROOT = Path(os.environ.get("SUPIR_SLIDES_ROOT", ".")) / ".supir-slides" / "templates"
INDEX_FILE = "index.json"
PROFILE_FILE = "template.json"


def utc_now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def read_json(path, default=None):
    if default is None:
        default = {}
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"JSON 解析错误 {path}: {e}") from e


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_index(root):
    data = read_json(root / INDEX_FILE, {"version": 1, "templates": []})
    data.setdefault("version", 1)
    data.setdefault("templates", [])
    return data


def save_index(root, index):
    index["templates"] = sorted(
        index.get("templates", []),
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )
    write_json(root / INDEX_FILE, index)


def cmd_list(args):
    root = args.root
    index = load_index(root)

    if not index["templates"]:
        print(f"模板库为空: {root}")
        return 0

    for entry in index["templates"]:
        marks = []
        if entry.get("id") == index.get("default_id"):
            marks.append("default")
        mark_str = f" ({', '.join(marks)})" if marks else ""
        print(f"{entry['id']}{mark_str} | {entry.get('display_name', '')} | {entry.get('created_at', '')}")

    return 0


def cmd_insert(args):
    root = args.root
    root.mkdir(parents=True, exist_ok=True)
    index = load_index(root)

    source_hash = ""
    if args.source_file:
        source = Path(args.source_file)
        if not source.exists():
            raise SystemExit(f"文件不存在: {source}")
        source_hash = sha256_file(source)

    template_id = args.id or f"tpl_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    template_dir = root / template_id
    template_dir.mkdir(parents=True, exist_ok=True)

    if args.source_file:
        dest = template_dir / Path(args.source_file).name
        shutil.copy2(args.source_file, dest)

    refs = {}
    if args.ref:
        for ref_spec in args.ref:
            if "=" not in ref_spec:
                continue
            role, src = ref_spec.split("=", 1)
            src_path = Path(src)
            if src_path.exists():
                dest = template_dir / f"{role}{src_path.suffix}"
                shutil.copy2(src, dest)
                refs[role] = dest.name

    profile = {
        "id": template_id,
        "display_name": args.display_name or template_id,
        "created_at": utc_now(),
        "source_sha256": source_hash,
        "refs": refs,
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
    }
    write_json(template_dir / PROFILE_FILE, profile)

    entry = {
        "id": template_id,
        "display_name": profile["display_name"],
        "created_at": profile["created_at"],
        "path": str(template_dir)
    }
    index["templates"] = [t for t in index["templates"] if t["id"] != template_id]
    index["templates"].append(entry)
    save_index(root, index)

    print(json.dumps({"status": "success", "template_id": template_id, "path": str(template_dir)}))
    return 0


def cmd_get(args):
    root = args.root
    index = load_index(root)

    entry = None
    for t in index["templates"]:
        if t["id"] == args.template or t.get("display_name") == args.template:
            entry = t
            break

    if not entry:
        if args.template in ("latest", "@latest") and index["templates"]:
            entry = index["templates"][0]
        elif args.template in ("default", "@default"):
            default_id = index.get("default_id")
            if default_id:
                entry = next((t for t in index["templates"] if t["id"] == default_id), None)

    if not entry:
        print(f"模板不存在: {args.template}", file=sys.stderr)
        return 1

    template_dir = Path(entry["path"])
    profile = read_json(template_dir / PROFILE_FILE, {})

    if args.assets_only:
        result = {
            "id": entry["id"],
            "display_name": entry.get("display_name"),
            "path": str(template_dir)
        }
    else:
        result = {"entry": entry, "profile": profile}

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_set_default(args):
    root = args.root
    index = load_index(root)

    for t in index["templates"]:
        if t["id"] == args.template:
            index["default_id"] = args.template
            save_index(root, index)
            print(f"已设为默认模板: {args.template}")
            return 0

    print(f"模板不存在: {args.template}", file=sys.stderr)
    return 1


def cmd_remove(args):
    root = args.root
    index = load_index(root)

    entry = next((t for t in index["templates"] if t["id"] == args.template), None)
    if not entry:
        print(f"模板不存在: {args.template}", file=sys.stderr)
        return 1

    template_dir = Path(entry["path"])
    if template_dir.exists():
        shutil.rmtree(template_dir)

    index["templates"] = [t for t in index["templates"] if t["id"] != args.template]
    if index.get("default_id") == args.template:
        index.pop("default_id", None)
    save_index(root, index)

    print(f"已删除模板: {args.template}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="幻灯片模板库管理")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="模板库根目录")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="列出所有模板")

    p = sub.add_parser("get", help="获取模板详情")
    p.add_argument("template")
    p.add_argument("--assets-only", action="store_true")

    p = sub.add_parser("insert", help="插入新模板")
    p.add_argument("--id", default="")
    p.add_argument("--display-name", default="")
    p.add_argument("--source-file", default="")
    p.add_argument("--ref", action="append", default=[])
    p.add_argument("--tags", default="")

    p = sub.add_parser("set-default", help="设为默认模板")
    p.add_argument("template")

    p = sub.add_parser("remove", help="删除模板")
    p.add_argument("template")

    args = parser.parse_args()

    commands = {
        "list": cmd_list,
        "get": cmd_get,
        "insert": cmd_insert,
        "set-default": cmd_set_default,
        "remove": cmd_remove
    }

    return commands[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
