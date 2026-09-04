"""Validate the publishable BioSpec MVP preset package.

The validator is deliberately small and deterministic. It checks the package
boundary and official preset manifest shape; it does not run an agent,
pipeline, or scientific analysis.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


SUPPORTED_TYPES = {"template", "command", "script"}
SUPPORTED_STRATEGIES = {"replace", "prepend", "append", "wrap"}
SCRIPT_STRATEGIES = {"replace", "wrap"}
REQUIRED_PRESET_FIELDS = {
    "id",
    "name",
    "version",
    "description",
    "author",
    "repository",
    "license",
}
CORE_TEMPLATE_NAMES = {
    "constitution-template",
    "spec-template",
    "plan-template",
    "tasks-template",
    "checklist-template",
}
CAPABILITY_BINDING_ANCHORS = (
    "## Capability Bindings",
    "required_capabilities:",
    "skill_id:",
    "inputs:",
    "outputs:",
    "constraints:",
    "acceptance:",
    "evidence:",
)
FORBIDDEN_DIRECTORY_NAMES = {"artifacts", "run-working"}


def _inside_package(package_root: Path, relative_name: str) -> tuple[Path | None, str | None]:
    """Resolve a manifest path while rejecting absolute and parent traversal."""

    normalized = relative_name.replace("\\", "/")
    candidate_name = PurePosixPath(normalized)
    if candidate_name.is_absolute() or ":" in normalized:
        return None, "path must be relative to the package"
    if ".." in candidate_name.parts:
        return None, "path traversal is not allowed"
    candidate = (package_root / Path(*candidate_name.parts)).resolve()
    try:
        candidate.relative_to(package_root.resolve())
    except ValueError:
        return None, "path escapes the package"
    return candidate, None


def validate_package(package_root: Path) -> list[str]:
    package_root = package_root.resolve()
    errors: list[str] = []

    for required in ("README.md", "LICENSE", "preset.yml"):
        if not (package_root / required).is_file():
            errors.append(f"missing required package file: {required}")
    for required_dir in ("commands", "docs", "scripts", "templates", "tests"):
        if not (package_root / required_dir).is_dir():
            errors.append(f"missing required package directory: {required_dir}/")

    for path in package_root.rglob("*"):
        if path.is_dir() and path.name.lower() in FORBIDDEN_DIRECTORY_NAMES:
            errors.append(f"runtime directory is not allowed in preset: {path.relative_to(package_root)}")
    nested_manifests = sorted(
        path.relative_to(package_root).as_posix()
        for path in package_root.rglob("preset.yml")
        if path != package_root / "preset.yml"
    )
    if nested_manifests:
        errors.append(f"nested preset manifests are not allowed: {', '.join(nested_manifests)}")
    workflow_manifests = sorted(
        path.relative_to(package_root).as_posix() for path in package_root.rglob("workflow.yml")
    )
    if workflow_manifests:
        errors.append(f"workflow manifests belong outside the preset: {', '.join(workflow_manifests)}")

    manifest_path = package_root / "preset.yml"
    if not manifest_path.is_file():
        return errors
    try:
        document = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        errors.append(f"cannot parse preset.yml: {exc}")
        return errors
    if not isinstance(document, dict):
        return errors + ["preset.yml must contain a mapping"]
    if document.get("schema_version") != "1.0":
        errors.append("schema_version must be \"1.0\"")

    preset = document.get("preset")
    if not isinstance(preset, dict):
        errors.append("preset must be a mapping")
        preset = {}
    missing_preset_fields = sorted(REQUIRED_PRESET_FIELDS - set(preset))
    errors.extend(f"preset is missing field: {field}" for field in missing_preset_fields)
    if preset.get("id") != "bio-spec-mvp":
        errors.append('preset.id must be "bio-spec-mvp"')

    requires = document.get("requires")
    if not isinstance(requires, dict) or not isinstance(requires.get("speckit_version"), str):
        errors.append("requires.speckit_version must be a string")

    provides = document.get("provides")
    if not isinstance(provides, dict):
        errors.append("provides must be a mapping")
        return errors
    extra_provides_keys = sorted(set(provides) - {"templates"})
    errors.extend(f"unsupported provides key: {key}" for key in extra_provides_keys)
    entries = provides.get("templates")
    if not isinstance(entries, list) or not entries:
        errors.append("provides.templates must be a non-empty list")
        return errors

    names: set[str] = set()
    seen_core_templates: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"provides.templates[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be a mapping")
            continue
        item_type = entry.get("type")
        if item_type not in SUPPORTED_TYPES:
            errors.append(f"{prefix}.type {item_type!r} is not supported")
        name = entry.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{prefix}.name must be a non-empty string")
        elif name in names:
            errors.append(f"duplicate provided item name: {name}")
        else:
            names.add(name)
        file_name = entry.get("file")
        if not isinstance(file_name, str) or not file_name.strip():
            errors.append(f"{prefix}.file must be a non-empty string")
        else:
            resolved, path_error = _inside_package(package_root, file_name)
            if path_error:
                errors.append(f"{prefix}.file: {path_error}")
            elif resolved is not None and not resolved.is_file():
                errors.append(f"{prefix}.file does not exist: {file_name}")
        strategy = entry.get("strategy", "replace")
        if strategy not in SUPPORTED_STRATEGIES:
            errors.append(f"{prefix}.strategy {strategy!r} is not supported")
        if item_type == "script" and strategy not in SCRIPT_STRATEGIES:
            errors.append(f"{prefix}.script strategy must be replace or wrap")
        replaces = entry.get("replaces")
        if replaces is not None and not isinstance(replaces, str):
            errors.append(f"{prefix}.replaces must be a string when present")
        if item_type == "template" and name in CORE_TEMPLATE_NAMES:
            seen_core_templates.add(name)

    missing_core_templates = sorted(CORE_TEMPLATE_NAMES - seen_core_templates)
    errors.extend(f"missing core template entry: {name}" for name in missing_core_templates)

    plan_template = package_root / "templates" / "plan-template.md"
    if plan_template.is_file():
        plan_content = plan_template.read_text(encoding="utf-8")
        for anchor in CAPABILITY_BINDING_ANCHORS:
            if anchor not in plan_content:
                errors.append(f"plan-template.md is missing capability anchor: {anchor}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate_package(args.package)
    result: dict[str, Any] = {
        "package": str(args.package.resolve()),
        "ok": not errors,
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
