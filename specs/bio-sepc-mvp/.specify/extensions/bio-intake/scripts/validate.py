#!/usr/bin/env python3
"""Validate the small, versioned intake contract used by Bio Spec Kit."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_MANIFEST_FIELDS = ("project_id", "assay", "reference", "pipeline")
REQUIRED_SAMPLE_COLUMNS = ("sample_id", "group")


def load_document(path: Path) -> dict[str, Any]:
    if path.suffix.lower() == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
    else:
        try:
            import yaml  # type: ignore[import-not-found]
        except ImportError as exc:
            raise RuntimeError(
                f"{path} is YAML; install PyYAML or use a JSON manifest"
            ) from exc
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object at the top level")
    return value


def validate(manifest_path: Path, samples_path: Path) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    manifest: dict[str, Any] = {}

    if not manifest_path.exists():
        errors.append(f"missing manifest: {manifest_path}")
    else:
        try:
            manifest = load_document(manifest_path)
        except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid manifest: {exc}")

    for field in REQUIRED_MANIFEST_FIELDS:
        if field not in manifest or manifest[field] in (None, ""):
            errors.append(f"manifest missing required field: {field}")

    if not samples_path.exists():
        errors.append(f"missing sample metadata: {samples_path}")
    else:
        try:
            with samples_path.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle, delimiter="\t")
                columns = reader.fieldnames or []
                for column in REQUIRED_SAMPLE_COLUMNS:
                    if column not in columns:
                        errors.append(f"sample metadata missing column: {column}")
                rows = list(reader)
            sample_ids = [row.get("sample_id", "").strip() for row in rows]
            if not rows:
                errors.append("sample metadata has no rows")
            if "sample_id" in columns and any(not value for value in sample_ids):
                errors.append("sample metadata contains an empty sample_id")
            if len(sample_ids) != len(set(sample_ids)):
                errors.append("sample metadata contains duplicate sample_id values")
            if "group" in columns and any(not row.get("group", "").strip() for row in rows):
                errors.append("sample metadata contains an empty group")
            if len(rows) < 2:
                warnings.append("fewer than two samples are present; statistical analysis may be impossible")
        except (OSError, csv.Error) as exc:
            errors.append(f"cannot read sample metadata: {exc}")

    return errors, warnings, manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path(".bio/manifest.json"))
    parser.add_argument("--samples", type=Path, default=Path(".bio/samples.tsv"))
    parser.add_argument("--output", type=Path, default=Path(".bio/runs/current/intake"))
    args = parser.parse_args()

    errors, warnings, manifest = validate(args.manifest, args.samples)
    args.output.mkdir(parents=True, exist_ok=True)
    verdict = {
        "schema_version": "1",
        "stage": "intake",
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "manifest": manifest,
        "inputs": {"manifest": str(args.manifest), "samples": str(args.samples)},
    }
    (args.output / "intake-verdict.json").write_text(
        json.dumps(verdict, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    error_lines = [f"- {item}" for item in errors] or ["- None"]
    warning_lines = [f"- {item}" for item in warnings] or ["- None"]
    report = [
        "# Intake report",
        "",
        f"- Decision: **{'PASS' if verdict['ok'] else 'FAIL'}**",
        f"- Project: `{manifest.get('project_id', 'unknown')}`",
        f"- Assay: `{manifest.get('assay', 'unknown')}`",
        "",
        "## Errors",
        *error_lines,
        "",
        "## Warnings",
        *warning_lines,
        "",
    ]
    (args.output / "intake-report.md").write_text("\n".join(report), encoding="utf-8")
    print(json.dumps(verdict, ensure_ascii=False))
    return 0 if verdict["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
