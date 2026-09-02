#!/usr/bin/env python3
"""Evaluate scalar QC metrics without requiring third-party Python packages."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def evaluate(metrics: dict[str, Any], thresholds: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    errors: list[str] = []
    for name, rule in thresholds.items():
        if not isinstance(rule, dict):
            errors.append(f"threshold for {name} must be an object")
            continue
        if name not in metrics or not isinstance(metrics[name], (int, float)):
            checks.append({"metric": name, "ok": False, "reason": "missing or non-numeric metric"})
            continue
        value = float(metrics[name])
        failures: list[str] = []
        if "min" in rule and value < float(rule["min"]):
            failures.append(f"{value} < minimum {rule['min']}")
        if "max" in rule and value > float(rule["max"]):
            failures.append(f"{value} > maximum {rule['max']}")
        checks.append({"metric": name, "value": value, "rule": rule, "ok": not failures, "failures": failures})
    return checks, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", type=Path, default=Path(".bio/qc/metrics.json"))
    parser.add_argument("--thresholds", type=Path, default=Path(".bio/qc/thresholds.json"))
    parser.add_argument("--output", type=Path, default=Path(".bio/runs/current/qc"))
    args = parser.parse_args()

    errors: list[str] = []
    try:
        metrics = load_json(args.metrics)
        thresholds = load_json(args.thresholds)
        checks, evaluation_errors = evaluate(metrics, thresholds)
        errors.extend(evaluation_errors)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        metrics, thresholds, checks = {}, {}, []
        errors.append(str(exc))

    args.output.mkdir(parents=True, exist_ok=True)
    ok = not errors and bool(checks) and all(item.get("ok", False) for item in checks)
    verdict = {
        "schema_version": "1",
        "stage": "qc",
        "ok": ok,
        "metrics": metrics,
        "thresholds": thresholds,
        "checks": checks,
        "errors": errors,
    }
    (args.output / "qc-verdict.json").write_text(
        json.dumps(verdict, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    check_lines = [
        f"- `{item['metric']}`: {'PASS' if item.get('ok') else 'FAIL'}"
        for item in checks
    ] or ["- None"]
    error_lines = [f"- {item}" for item in errors] or ["- None"]
    report = [
        "# QC report",
        "",
        f"- Decision: **{'PASS' if ok else 'FAIL'}**",
        "",
        "## Checks",
        *check_lines,
        "",
        "## Errors",
        *error_lines,
        "",
    ]
    (args.output / "qc-report.md").write_text("\n".join(report), encoding="utf-8")
    print(json.dumps(verdict, ensure_ascii=False))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
