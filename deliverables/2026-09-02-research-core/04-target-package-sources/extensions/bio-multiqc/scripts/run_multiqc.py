#!/usr/bin/env python3
"""Run MultiQC as a bounded, reviewable bio-spec-kit extension."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


WRAPPER_VERSION = "0.1.0"


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_review(path: Path, verdict: dict[str, Any]) -> None:
    status = str(verdict.get("status", "failed")).upper()
    lines = [
        "# MultiQC review report",
        "",
        f"- Decision: {status}",
        f"- Input: {verdict.get('input')}",
        f"- Output: {verdict.get('output')}",
        f"- Command: {verdict.get('command')}",
        "",
        "## Review notes",
        "",
        "- Confirm that the expected tools and samples are present.",
        "- Confirm that thresholds and outliers are scientifically acceptable.",
        "- Confirm the JSON verdict and provenance are recorded before release.",
        "",
    ]
    if verdict.get("error"):
        lines.extend(["## Error", "", f"- {verdict['error']}", ""])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def input_manifest(root: Path) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        files.append(
            {
                "path": path.relative_to(root).as_posix(),
                "size": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return files


def write_text_log(path: Path, value: str) -> None:
    path.write_text(value, encoding="utf-8")


def read_text_compat(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8", "gb18030", "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def read_json_compat(path: Path) -> Any:
    return json.loads(read_text_compat(path))


def runtime_info(executable: str) -> dict[str, Any]:
    version_run = subprocess.run(
        [executable, "--version"], check=False, capture_output=True, text=True
    )
    version_text = (version_run.stdout or version_run.stderr).strip()
    return {
        "wrapper": WRAPPER_VERSION,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "multiqc": version_text,
        "executable": executable,
        "version_returncode": version_run.returncode,
    }


def verify_fastqc_artifacts(
    output: Path,
    report_path: Path,
    *,
    expected_sample: str,
    expected_total_sequences: float,
    expected_sequence_length: str,
    expected_percent_gc: float,
) -> list[str]:
    errors: list[str] = []
    data_dir = output / f"{report_path.stem}_data"
    data_json = data_dir / "multiqc_data.json"
    log_path = data_dir / "multiqc.log"
    sources_json = data_dir / "multiqc_sources.json"

    for required in (data_dir, data_json, log_path, sources_json):
        if not required.exists():
            errors.append(f"missing expected artifact: {required}")
    if errors:
        return errors

    try:
        data = read_json_compat(data_json)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot parse MultiQC data JSON: {exc}"]

    general_stats = data.get("report_general_stats_data", {}).get("fastqc", {})
    sample_data = general_stats.get(expected_sample)
    if not isinstance(sample_data, dict):
        errors.append(
            "FastQC sample missing from report_general_stats_data: "
            f"{expected_sample}"
        )
        return errors

    checks = {
        "total_sequences": (expected_total_sequences, sample_data.get("total_sequences")),
        "avg_sequence_length": (float(expected_sequence_length), sample_data.get("avg_sequence_length")),
        "percent_gc": (expected_percent_gc, sample_data.get("percent_gc")),
    }
    for field, (expected, observed) in checks.items():
        try:
            matches = float(observed) == float(expected)
        except (TypeError, ValueError):
            matches = False
        if not matches:
            errors.append(
                f"FastQC fixture value mismatch for {field}: "
                f"expected {expected!r}, observed {observed!r}"
            )

    try:
        sources = read_json_compat(sources_json)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot parse MultiQC source map: {exc}")
    else:
        fastqc_sources = sources.get("FastQC", {}).get("all_sections", {})
        if expected_sample not in fastqc_sources:
            errors.append(f"FastQC source map has no entry for {expected_sample}")

    log_text = read_text_compat(log_path)
    if "Found 1 reports" not in log_text:
        errors.append("MultiQC log does not confirm one FastQC report was parsed")

    html = read_text_compat(report_path)
    for marker in (
        "FastQC",
        expected_sample,
        str(int(expected_total_sequences)),
        expected_sequence_length,
        str(int(expected_percent_gc)),
    ):
        if marker not in html:
            errors.append(f"HTML report is missing expected content marker: {marker}")
    return errors


def failed_verdict(
    *,
    stage: str,
    input_path: Path,
    output_path: Path,
    command: list[str] | None,
    error: str,
    runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "1",
        "stage": stage,
        "status": "failed",
        "ok": False,
        "release_ready": False,
        "input": str(input_path),
        "output": str(output_path),
        "command": command,
        "runtime": runtime,
        "error": error,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--mode", choices=("required", "skip"), default="required")
    parser.add_argument("--multiqc-bin", default="multiqc")
    parser.add_argument("--filename", default="multiqc_report.html")
    parser.add_argument(
        "--preset", choices=("generic", "fastqc-multiqc-mvp"), default="generic"
    )
    parser.add_argument("--expected-sample", default="test_R1")
    parser.add_argument("--expected-total-sequences", type=float, default=10000)
    parser.add_argument("--expected-sequence-length", default="100")
    parser.add_argument("--expected-percent-gc", type=float, default=48)
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow a non-empty output directory to be overwritten",
    )
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    verdict_path = args.output / "multiqc-verdict.json"
    review_path = args.output / "multiqc-review.md"

    if args.mode == "skip":
        verdict = {
            "schema_version": "1",
            "stage": "multiqc",
            "status": "skipped",
            "ok": True,
            "release_ready": False,
            "input": str(args.input),
            "output": str(args.output),
            "command": None,
            "error": None,
        }
        write_json(verdict_path, verdict)
        write_review(review_path, verdict)
        print(json.dumps(verdict, ensure_ascii=False))
        return 0

    if not args.input.is_dir():
        verdict = failed_verdict(
            stage="multiqc",
            input_path=args.input,
            output_path=args.output,
            command=None,
            error=f"MultiQC input directory does not exist: {args.input}",
        )
        write_json(verdict_path, verdict)
        write_review(review_path, verdict)
        print(json.dumps(verdict, ensure_ascii=False))
        return 2

    if not args.config.is_file():
        verdict = failed_verdict(
            stage="multiqc",
            input_path=args.input,
            output_path=args.output,
            command=None,
            error=f"MultiQC config file does not exist: {args.config}",
        )
        write_json(verdict_path, verdict)
        write_review(review_path, verdict)
        print(json.dumps(verdict, ensure_ascii=False))
        return 2

    preexisting = sorted(path.name for path in args.output.iterdir())
    if preexisting and not args.overwrite:
        verdict = failed_verdict(
            stage="multiqc",
            input_path=args.input,
            output_path=args.output,
            command=None,
            error=(
                "Output directory is not empty; use a fresh run directory or "
                "pass --overwrite explicitly. Existing entries: "
                + ", ".join(preexisting)
            ),
        )
        write_json(verdict_path, verdict)
        write_review(review_path, verdict)
        print(json.dumps(verdict, ensure_ascii=False))
        return 2

    executable = shutil.which(args.multiqc_bin)
    if executable is None:
        verdict = failed_verdict(
            stage="multiqc",
            input_path=args.input,
            output_path=args.output,
            command=[args.multiqc_bin],
            error=f"MultiQC executable not found: {args.multiqc_bin}",
        )
        write_json(verdict_path, verdict)
        write_review(review_path, verdict)
        print(json.dumps(verdict, ensure_ascii=False))
        return 2

    try:
        runtime = runtime_info(executable)
    except OSError as exc:
        verdict = failed_verdict(
            stage="multiqc",
            input_path=args.input,
            output_path=args.output,
            command=[executable, "--version"],
            error=f"cannot query MultiQC version: {exc}",
        )
        write_json(verdict_path, verdict)
        write_review(review_path, verdict)
        print(json.dumps(verdict, ensure_ascii=False))
        return 2

    if runtime["version_returncode"] != 0:
        verdict = failed_verdict(
            stage="multiqc",
            input_path=args.input,
            output_path=args.output,
            command=[executable, "--version"],
            error=f"MultiQC --version failed: {runtime['multiqc']}",
            runtime=runtime,
        )
        write_json(verdict_path, verdict)
        write_review(review_path, verdict)
        print(json.dumps(verdict, ensure_ascii=False))
        return 2

    command = [
        executable,
        str(args.input),
        "--outdir",
        str(args.output),
        "--filename",
        args.filename,
        "--config",
        str(args.config),
        "--force",
    ]
    input_files = input_manifest(args.input)
    if not input_files:
        verdict = failed_verdict(
            stage="multiqc",
            input_path=args.input,
            output_path=args.output,
            command=command,
            error="MultiQC input directory contains no files",
            runtime=runtime,
        )
        write_json(verdict_path, verdict)
        write_review(review_path, verdict)
        print(json.dumps(verdict, ensure_ascii=False))
        return 2

    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    write_text_log(args.output / "wrapper-stdout.log", completed.stdout)
    write_text_log(args.output / "wrapper-stderr.log", completed.stderr)
    report_path = args.output / args.filename
    verification_errors: list[str] = []
    if completed.returncode != 0:
        verification_errors.append(
            f"MultiQC returned non-zero exit code: {completed.returncode}"
        )
    if not report_path.is_file() or report_path.stat().st_size == 0:
        verification_errors.append(f"missing or empty report: {report_path}")
    if args.preset == "fastqc-multiqc-mvp" and not verification_errors:
        verification_errors.extend(
            verify_fastqc_artifacts(
                args.output,
                report_path,
                expected_sample=args.expected_sample,
                expected_total_sequences=args.expected_total_sequences,
                expected_sequence_length=args.expected_sequence_length,
                expected_percent_gc=args.expected_percent_gc,
            )
        )
    ok = not verification_errors
    finished_at = datetime.now(timezone.utc).isoformat()
    artifact_paths = [
        report_path,
        args.output / f"{report_path.stem}_data" / "multiqc_data.json",
        args.output / f"{report_path.stem}_data" / "multiqc.log",
        args.output / f"{report_path.stem}_data" / "multiqc_sources.json",
    ]
    artifact_manifest = [
        {
            "path": str(path),
            "exists": path.is_file(),
            "size": path.stat().st_size if path.is_file() else None,
            "sha256": sha256_file(path) if path.is_file() else None,
        }
        for path in artifact_paths
    ]
    input_manifest_path = args.output / "input-manifest.json"
    write_json(
        input_manifest_path,
        {
            "input_root": str(args.input),
            "files": input_files,
            "sha256": hashlib.sha256(
                json.dumps(input_files, sort_keys=True).encode("utf-8")
            ).hexdigest(),
        },
    )
    write_json(
        args.output / "artifact-manifest.json",
        {"generated_at": finished_at, "artifacts": artifact_manifest},
    )
    verdict = {
        "schema_version": "1",
        "stage": "multiqc",
        "status": "completed" if ok else "failed",
        "ok": ok,
        "release_ready": ok,
        "input": str(args.input),
        "output": str(args.output),
        "command": command,
        "returncode": completed.returncode,
        "report": str(report_path) if report_path.exists() else None,
        "data_dir": str(args.output / f"{report_path.stem}_data"),
        "preset": args.preset,
        "runtime": runtime,
        "input_manifest": str(input_manifest_path),
        "input_file_count": len(input_files),
        "artifact_manifest": str(args.output / "artifact-manifest.json"),
        "verification_errors": verification_errors,
        "stdout_tail": completed.stdout[-4000:],
        "stderr_tail": completed.stderr[-4000:],
        "error": None if ok else "MultiQC artifact verification failed.",
    }
    write_json(verdict_path, verdict)
    write_review(review_path, verdict)
    print(json.dumps(verdict, ensure_ascii=False))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
