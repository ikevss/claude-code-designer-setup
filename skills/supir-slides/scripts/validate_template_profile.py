#!/usr/bin/env python3
"""Validate a paipai-slides template profile.

The validator is intentionally tolerant of incomplete templates: a source deck
may not have every canonical page role. Missing roles are warnings so generation
can fall back to the nearest available reference. Broken asset paths and
contradictory brand/font policies are surfaced as errors or warnings.
"""

import argparse
import json
import sys
from pathlib import Path

CANONICAL_PAGE_ROLES = ["cover", "toc", "section", "content", "closing"]
PAGE_ROLE_ALIASES = {
    "contents": "toc",
    "agenda": "toc",
    "chapter": "section",
    "section_divider": "section",
    "title_page": "content",
    "content_text": "content",
    "content_chart": "content",
    "content_table": "content",
    "content_diagram": "content",
    "diagram": "content",
    "evidence": "content",
    "chart_evidence": "content",
    "end": "closing",
    "thanks": "closing",
    "disclaimer": "closing",
}
CONTENT_VARIANT_ALIASES = {
    "title_page",
    "content_text",
    "content_chart",
    "content_table",
    "content_diagram",
    "diagram",
    "evidence",
    "chart_evidence",
}
LEGACY_BRAND_POLICY_MARKERS = [
    "softly inherited",
    "not forced",
    "do not explicitly require",
    "visual_reference_only",
    "自然风格痕迹",
    "不强制",
]
LEGACY_FONT_MARKERS = ["Microsoft YaHei", "微软雅黑", "YaHei"]


def load_profile(path):
    path = Path(path)
    if path.is_dir():
        profile_path = path / "template.json"
        base_dir = path
    else:
        profile_path = path
        base_dir = path.parent
    try:
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Template profile not found: {profile_path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {profile_path}: {exc}") from exc
    if not isinstance(profile, dict):
        raise SystemExit(f"Template profile must be a JSON object: {profile_path}")
    return profile_path, base_dir, profile


def as_dict(value):
    return value if isinstance(value, dict) else {}


def resolve_asset(base_dir, rel_path):
    if not isinstance(rel_path, str) or not rel_path:
        return None
    path = Path(rel_path)
    return path if path.is_absolute() else base_dir / path


def add_asset_check(errors, base_dir, label, rel_path):
    path = resolve_asset(base_dir, rel_path)
    if path is None:
        errors.append(f"{label} has an empty or non-string path")
    elif not path.exists() or not path.is_file():
        errors.append(f"{label} points to a missing file: {rel_path}")


def scan_legacy_markers(profile, markers):
    text = json.dumps(profile, ensure_ascii=False)
    return [marker for marker in markers if marker in text]


def validate_roles(profile, base_dir, errors, warnings, infos):
    assets = as_dict(profile.get("assets"))
    selected_refs = as_dict(assets.get("selected_refs"))
    style_layer = as_dict(profile.get("style_layer"))
    page_role_map = as_dict(style_layer.get("page_role_map"))
    aliases = as_dict(style_layer.get("page_role_aliases")) or PAGE_ROLE_ALIASES

    known_roles = set(CANONICAL_PAGE_ROLES) | set(PAGE_ROLE_ALIASES) | set(aliases)
    configured_roles = set(selected_refs) | set(page_role_map)
    missing = [role for role in CANONICAL_PAGE_ROLES if role not in configured_roles]
    if missing:
        warnings.append(
            "missing canonical role reference(s): "
            + ", ".join(missing)
            + "; generation should fall back to a nearby role or style preset"
        )

    for role in sorted(configured_roles):
        if role not in known_roles:
            warnings.append(f"unknown page role key {role!r}; keep custom variants in layout_features unless intentional")
        elif role in CONTENT_VARIANT_ALIASES:
            infos.append(f"content variant {role!r} is configured and maps to canonical role 'content'")

    for role, rel_path in sorted(selected_refs.items()):
        add_asset_check(errors, base_dir, f"assets.selected_refs.{role}", rel_path)
    for role, rel_path in sorted(page_role_map.items()):
        add_asset_check(errors, base_dir, f"style_layer.page_role_map.{role}", rel_path)

    for alias, canonical in sorted(aliases.items()):
        if canonical not in CANONICAL_PAGE_ROLES:
            warnings.append(f"alias {alias!r} maps to unknown canonical role {canonical!r}")
        if alias in configured_roles and canonical not in configured_roles:
            warnings.append(f"alias role {alias!r} exists but canonical role {canonical!r} is missing")

    if "content" not in configured_roles:
        warnings.append("no generic 'content' reference is configured; ordinary pages will need an alias or fallback")


def validate_brand(profile, base_dir, errors, warnings, infos):
    assets = as_dict(profile.get("assets"))
    brand_assets = as_dict(assets.get("brand_assets"))
    style_layer = as_dict(profile.get("style_layer"))
    brand_elements = style_layer.get("brand_elements", [])

    for name, rel_path in sorted(brand_assets.items()):
        add_asset_check(errors, base_dir, f"assets.brand_assets.{name}", rel_path)

    if brand_elements and not isinstance(brand_elements, list):
        errors.append("style_layer.brand_elements must be a list when present")
        return

    asset_values = set(brand_assets.values())
    required = {
        "kind",
        "asset",
        "source_page_role",
        "position",
        "identity",
        "source",
        "retain_policy",
        "confidence",
    }
    for index, element in enumerate(brand_elements or []):
        if not isinstance(element, dict):
            errors.append(f"style_layer.brand_elements[{index}] must be an object")
            continue
        missing = sorted(required - set(element))
        if missing:
            warnings.append(
                f"style_layer.brand_elements[{index}] missing field(s): {', '.join(missing)}"
            )
        asset = element.get("asset")
        if asset:
            add_asset_check(errors, base_dir, f"style_layer.brand_elements[{index}].asset", asset)
            if asset not in asset_values:
                warnings.append(
                    f"style_layer.brand_elements[{index}].asset is not listed in assets.brand_assets: {asset}"
                )
        identity = element.get("identity")
        retain_policy = element.get("retain_policy")
        if identity == "template_brand" and retain_policy == "retain_by_default":
            infos.append(f"template brand element retained by default: {asset or element.get('visible_text', index)}")
        if retain_policy in {"remove", "replace"} and identity == "template_brand":
            infos.append(f"template brand override recorded for element {index}: {retain_policy}")

    legacy_markers = scan_legacy_markers(profile, LEGACY_BRAND_POLICY_MARKERS)
    if legacy_markers:
        warnings.append("legacy soft brand policy marker(s) found: " + ", ".join(legacy_markers))


def validate_typography(profile, warnings, infos):
    legacy_fonts = scan_legacy_markers(profile, LEGACY_FONT_MARKERS)
    if legacy_fonts:
        warnings.append("legacy Microsoft YaHei font marker(s) found: " + ", ".join(legacy_fonts))

    style_layer = as_dict(profile.get("style_layer"))
    typography_signature = as_dict(style_layer.get("typography_signature"))
    if typography_signature:
        infos.append("style_layer.typography_signature is present")
    else:
        warnings.append("style_layer.typography_signature is missing; generation may rely on generic font wording")


def validate_content_layer(profile, warnings):
    content_layer = profile.get("content_layer")
    if not isinstance(content_layer, dict):
        warnings.append("content_layer is missing or not an object; style/content separation is incomplete")
        return
    page_slot_map = content_layer.get("page_slot_map")
    if isinstance(page_slot_map, dict):
        missing = [role for role in CANONICAL_PAGE_ROLES if role not in page_slot_map]
        if missing:
            warnings.append("content_layer.page_slot_map missing canonical role(s): " + ", ".join(missing))
    else:
        warnings.append("content_layer.page_slot_map is missing or not an object")


def validate(path):
    profile_path, base_dir, profile = load_profile(path)
    errors = []
    warnings = []
    infos = []

    for key in ("id", "display_name", "assets", "style_layer", "reuse_policy"):
        if key not in profile:
            warnings.append(f"top-level field {key!r} is missing")

    validate_roles(profile, base_dir, errors, warnings, infos)
    validate_brand(profile, base_dir, errors, warnings, infos)
    validate_typography(profile, warnings, infos)
    validate_content_layer(profile, warnings)

    return {
        "profile_path": str(profile_path),
        "base_dir": str(base_dir),
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "infos": infos,
    }


def print_human(report):
    status = "OK" if report["ok"] else "FAILED"
    print(f"{status}: {report['profile_path']}")
    for key, label in (("errors", "ERROR"), ("warnings", "WARN"), ("infos", "INFO")):
        for item in report[key]:
            print(f"{label}: {item}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate a paipai-slides template.json profile.")
    parser.add_argument("profile_or_template_dir", help="Path to template.json or a template directory.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON report.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when warnings are present, not only errors.",
    )
    args = parser.parse_args(argv)

    report = validate(args.profile_or_template_dir)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report)

    if report["errors"] or (args.strict and report["warnings"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
