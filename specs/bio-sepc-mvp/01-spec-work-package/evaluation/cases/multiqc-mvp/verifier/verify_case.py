#!/usr/bin/env python3
"""Deterministic verifier for the local MultiQC representative case."""

from __future__ import annotations

import argparse
from datetime import datetime
from hashlib import sha256
from html.parser import HTMLParser
import json
import re
import sys
from pathlib import Path, PurePosixPath


WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")
GIT_COMMIT = re.compile(r"^(?:[0-9a-f]{40}|unknown)$")


def load_json(path: Path) -> dict:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise AssertionError(f"cannot read JSON {path}: {exc}") from exc
    value = None
    last_error: Exception | None = None
    for encoding in ("utf-8", "gb18030", "cp1252"):
        try:
            value = json.loads(raw.decode(encoding))
            break
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            last_error = exc
    if value is None:
        raise AssertionError(f"cannot parse JSON {path}: {last_error}")
    if not isinstance(value, dict):
        raise AssertionError(f"JSON root is not an object: {path}")
    return value


def read_text_compat(path: Path) -> str:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise AssertionError(f"cannot read text {path}: {exc}") from exc
    for encoding in ("utf-8", "gb18030", "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def sha256_file(path: Path) -> str:
    digest = sha256()
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as exc:
        raise AssertionError(f"cannot hash {path}: {exc}") from exc
    return digest.hexdigest()


def repo_root_for_output(output: Path) -> Path:
    """Derive the repository root from the feature's run layout."""

    resolved = output.resolve()
    try:
        return resolved.parents[4]
    except IndexError as exc:
        raise AssertionError(
            f"output path does not use the expected repository run layout: {output}"
        ) from exc


def portable_relative(value: object, label: str) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise AssertionError(f"{label} must be a non-empty relative path")
    if WINDOWS_ABSOLUTE.match(value) or value.startswith(("/", "\\")):
        raise AssertionError(f"{label} must not be absolute: {value!r}")
    if "\\" in value:
        raise AssertionError(f"{label} must use POSIX separators: {value!r}")
    relative = PurePosixPath(value)
    if any(part in {"", ".", ".."} for part in relative.parts):
        raise AssertionError(f"{label} contains an unsafe path component: {value!r}")
    return relative


def repo_relative(path: Path, repo_root: Path, label: str) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(repo_root.resolve()).as_posix()
    except ValueError as exc:
        raise AssertionError(f"{label} is outside the repository: {path}") from exc


class ReportStructureParser(HTMLParser):
    """Collect semantic HTML attributes without accepting arbitrary text markers."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.titles: list[str] = []
        self.section_anchors: list[str] = []
        self.module_anchors: list[str] = []
        self._in_title = False
        self._title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag.lower() == "title":
            self._in_title = True
            self._title_parts = []
        section_anchor = attributes.get("data-section-anchor")
        if section_anchor is not None:
            self.section_anchors.append(section_anchor)
        module_anchor = attributes.get("data-module-anchor")
        if module_anchor is not None:
            self.module_anchors.append(module_anchor)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title" and self._in_title:
            self.titles.append("".join(self._title_parts))
            self._in_title = False
            self._title_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)


def parse_report_structure(path: Path) -> ReportStructureParser:
    parser = ReportStructureParser()
    try:
        parser.feed(read_text_compat(path))
        parser.close()
    except (OSError, ValueError) as exc:
        raise AssertionError(f"cannot parse report HTML {path}: {exc}") from exc
    return parser


def review_status_block(review: str) -> tuple[dict[str, str] | None, list[str]]:
    """Parse the fenced status block as exact key/value lines."""

    errors: list[str] = []
    lines = review.splitlines()
    try:
        start = lines.index("```yaml")
        end = lines.index("```", start + 1)
    except ValueError:
        return None, ["research-core review has no fenced YAML status block"]
    block = lines[start + 1 : end]
    expected_lines = [
        "execution_status: passed",
        "scientific_status: not-verified",
        "release_status: pending",
    ]
    if block != expected_lines:
        errors.append(
            "research-core review status block must equal "
            f"{expected_lines!r}, got {block!r}"
        )
        return None, errors
    return {
        "execution_status": "passed",
        "scientific_status": "not-verified",
        "release_status": "pending",
    }, errors


def compare(errors: list[str], label: str, observed: object, expected: object) -> None:
    if observed != expected:
        errors.append(
            f"{label} mismatch: expected {expected!r}, got {observed!r}"
        )


def has_exact_line_sequence(lines: list[str], expected: list[str]) -> bool:
    width = len(expected)
    return any(
        lines[index : index + width] == expected
        for index in range(len(lines) - width + 1)
    )


def check_relative(errors: list[str], label: str, value: object) -> None:
    try:
        portable_relative(value, label)
    except AssertionError as exc:
        errors.append(str(exc))


def expected_case_path(output: Path, *parts: str) -> Path:
    feature_root = output.resolve().parents[2]
    return feature_root.joinpath("evaluation", "cases", "multiqc-mvp", *parts)


def expected_paths(output: Path) -> dict[str, str]:
    repo_root = repo_root_for_output(output)
    run_root = output.resolve()
    return {
        "input": repo_relative(
            expected_case_path(output, "inputs"),
            repo_root,
            "case input",
        ),
        "input_file": repo_relative(
            expected_case_path(
                output,
                "inputs",
                "sample_fastqc",
                "fastqc_data.txt",
            ),
            repo_root,
            "case input file",
        ),
        "output": repo_relative(run_root, repo_root, "run output"),
        "report": repo_relative(run_root / "multiqc_report.html", repo_root, "report"),
        "data_dir": repo_relative(
            run_root / "multiqc_report_data",
            repo_root,
            "data directory",
        ),
        "data": repo_relative(
            run_root / "multiqc_report_data" / "multiqc_data.json",
            repo_root,
            "parsed data",
        ),
        "sources": repo_relative(
            run_root / "multiqc_report_data" / "multiqc_sources.json",
            repo_root,
            "source map",
        ),
        "log": repo_relative(
            run_root / "multiqc_report_data" / "multiqc.log",
            repo_root,
            "MultiQC log",
        ),
        "input_manifest": repo_relative(
            run_root / "input-manifest.json",
            repo_root,
            "input manifest",
        ),
        "artifact_manifest": repo_relative(
            run_root / "artifact-manifest.json",
            repo_root,
            "artifact manifest",
        ),
        "contract": repo_relative(
            repo_root
            / "specs"
            / "005-skills-nextflow-research-core"
            / "contracts"
            / "multiqc"
            / "node.contract.json",
            repo_root,
            "node contract",
        ),
        "verifier": repo_relative(Path(__file__).resolve(), repo_root, "verifier"),
    }


def verify_positive(output: Path) -> list[str]:
    errors: list[str] = []
    paths = expected_paths(output)
    run_root = output.resolve()
    input_file = expected_case_path(
        output,
        "inputs",
        "sample_fastqc",
        "fastqc_data.txt",
    )

    verdict = load_json(run_root / "multiqc-verdict.json")
    compare(errors, "verdict.status", verdict.get("status"), "completed")
    compare(errors, "verdict.ok", verdict.get("ok"), True)
    compare(errors, "verdict.release_ready", verdict.get("release_ready"), True)
    compare(errors, "verdict.input", verdict.get("input"), paths["input"])
    compare(errors, "verdict.output", verdict.get("output"), paths["output"])
    for field in ("input", "output", "report", "data_dir", "input_manifest", "artifact_manifest"):
        check_relative(errors, f"verdict.{field}", verdict.get(field))
    compare(
        errors,
        "verdict.command",
        verdict.get("command"),
        [
            ".venv/Scripts/multiqc.exe",
            paths["input"],
            "--outdir",
            paths["output"],
            "--filename",
            "multiqc_report.html",
            "--config",
            "extensions/bio-multiqc/config/multiqc_config.yaml",
            "--force",
        ],
    )
    compare(errors, "verdict.report", verdict.get("report"), paths["report"])
    compare(errors, "verdict.data_dir", verdict.get("data_dir"), paths["data_dir"])
    compare(errors, "verdict.input_manifest", verdict.get("input_manifest"), paths["input_manifest"])
    compare(
        errors,
        "verdict.artifact_manifest",
        verdict.get("artifact_manifest"),
        paths["artifact_manifest"],
    )
    runtime = verdict.get("runtime")
    if not isinstance(runtime, dict):
        errors.append("verdict.runtime must be an object")
    else:
        compare(errors, "runtime.wrapper", runtime.get("wrapper"), "0.1.0")
        compare(errors, "runtime.python", runtime.get("python"), "3.12.10")
        compare(errors, "runtime.multiqc", runtime.get("multiqc"), "multiqc, version 1.35")
        compare(errors, "runtime.executable", runtime.get("executable"), ".venv/Scripts/multiqc.exe")
        compare(errors, "runtime.version_returncode", runtime.get("version_returncode"), 0)

    status_record = load_json(run_root / "research-core-status.json")
    compare(errors, "status.schema_version", status_record.get("schema_version"), "0.1")
    compare(errors, "status.run_id", status_record.get("run_id"), run_root.name)
    compare(errors, "status.component_id", status_record.get("component_id"), "multiqc")
    compare(errors, "status.contract_ref", status_record.get("contract_ref"), paths["contract"])
    compare(errors, "status.contract_schema_version", status_record.get("contract_schema_version"), "0.1")
    compare(errors, "status.verifier_ref", status_record.get("verifier_ref"), paths["verifier"])
    check_relative(errors, "status.contract_ref", status_record.get("contract_ref"))
    check_relative(errors, "status.verifier_ref", status_record.get("verifier_ref"))
    repository = status_record.get("repository")
    if not isinstance(repository, dict):
        errors.append("status.repository must be an object")
    else:
        compare(errors, "status.repository.path_base", repository.get("path_base"), "repository-root")
        commit = repository.get("git_commit")
        if not isinstance(commit, str) or GIT_COMMIT.fullmatch(commit) is None:
            errors.append("status.repository.git_commit must be a full lowercase commit or unknown")
        if not isinstance(repository.get("working_tree_dirty"), bool):
            errors.append("status.repository.working_tree_dirty must be boolean")
    compare(errors, "status.artifact_ready", status_record.get("artifact_ready"), True)
    compare(errors, "status.source_verdict", status_record.get("source_verdict"), "multiqc-verdict.json")
    compare(errors, "status.review_record", status_record.get("review_record"), "research-core-review.md")
    expected_status = {
        "execution": "passed",
        "scientific": "not-verified",
        "release": "pending",
    }
    compare(errors, "status.status", status_record.get("status"), expected_status)

    provenance = status_record.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("status.provenance must be an object")
    else:
        input_manifest_path = run_root / "input-manifest.json"
        artifact_manifest_path = run_root / "artifact-manifest.json"
        compare(
            errors,
            "provenance.input_manifest",
            provenance.get("input_manifest"),
            {
                "path": "input-manifest.json",
                "sha256": sha256_file(input_manifest_path),
            },
        )
        check_relative(
            errors,
            "provenance.input_manifest.path",
            provenance.get("input_manifest", {}).get("path")
            if isinstance(provenance.get("input_manifest"), dict)
            else None,
        )
        compare(
            errors,
            "provenance.artifact_manifest",
            provenance.get("artifact_manifest"),
            {
                "path": "artifact-manifest.json",
                "sha256": sha256_file(artifact_manifest_path),
            },
        )
        check_relative(
            errors,
            "provenance.artifact_manifest.path",
            provenance.get("artifact_manifest", {}).get("path")
            if isinstance(provenance.get("artifact_manifest"), dict)
            else None,
        )
        compare(errors, "provenance.command", provenance.get("command"), verdict.get("command"))
        compare(
            errors,
            "provenance.executable",
            provenance.get("executable"),
            {
                "id": "multiqc",
                "version": "1.35",
                "path": ".venv/Scripts/multiqc.exe",
            },
        )
        compare(
            errors,
            "provenance.parameters",
            provenance.get("parameters"),
            {
                "preset": "fastqc-multiqc-mvp",
                "mode": "required",
                "output_policy": "fresh directory unless explicit overwrite is approved",
            },
        )
        environment = provenance.get("environment")
        if not isinstance(environment, dict):
            errors.append("provenance.environment must be an object")
        else:
            for field in ("platform", "python"):
                if not isinstance(environment.get(field), str) or not environment[field]:
                    errors.append(f"provenance.environment.{field} must be non-empty")
            tool_versions = environment.get("tool_versions")
            if not isinstance(tool_versions, dict):
                errors.append("provenance.environment.tool_versions must be an object")
            else:
                compare(errors, "tool_versions.multiqc", tool_versions.get("multiqc"), "1.35")
                compare(errors, "tool_versions.wrapper", tool_versions.get("wrapper"), "0.1.0")
        compare(
            errors,
            "provenance.reference_snapshots",
            provenance.get("reference_snapshots"),
            [
                {
                    "id": "external-reference-data",
                    "status": "not_applicable",
                    "version_or_date": "not-applicable",
                }
            ],
        )
    recorded_at = status_record.get("recorded_at")
    if not isinstance(recorded_at, str):
        errors.append("status.recorded_at must be an ISO date-time string")
    else:
        try:
            datetime.fromisoformat(recorded_at.replace("Z", "+00:00"))
        except ValueError:
            errors.append("status.recorded_at must be an ISO date-time string")

    report = run_root / "multiqc_report.html"
    if not report.is_file() or report.stat().st_size == 0:
        errors.append(f"missing or empty report: {report}")
    else:
        report_structure = parse_report_structure(report)
        if "bio-spec-kit MultiQC QC Report: MultiQC Report" not in report_structure.titles:
            errors.append("report has no exact MultiQC title element")
        if "general_stats_table" not in report_structure.section_anchors:
            errors.append("report has no general_stats_table section anchor")
        if "fastqc_sequence_counts" not in report_structure.section_anchors:
            errors.append("report has no fastqc_sequence_counts section anchor")
        if "fastqc" not in report_structure.module_anchors:
            errors.append("report has no fastqc module anchor")

    data_dir = run_root / "multiqc_report_data"
    required_artifacts = (
        data_dir / "multiqc_data.json",
        data_dir / "multiqc_sources.json",
        data_dir / "multiqc.log",
        run_root / "multiqc-review.md",
        run_root / "research-core-status.json",
        run_root / "research-core-review.md",
        run_root / "input-manifest.json",
        run_root / "artifact-manifest.json",
    )
    for path in required_artifacts:
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty required artifact: {path}")

    data = load_json(data_dir / "multiqc_data.json")
    fastqc_stats = data.get("report_general_stats_data", {}).get("fastqc", {})
    sample_data = fastqc_stats.get("test_R1")
    if not isinstance(sample_data, dict):
        errors.append("parsed MultiQC data has no FastQC sample test_R1")
    else:
        expected_fields = {
            "total_sequences": 10000,
            "avg_sequence_length": 100,
            "percent_gc": 48,
        }
        for field, expected in expected_fields.items():
            try:
                observed = float(sample_data.get(field))
                matches = observed == float(expected)
            except (TypeError, ValueError):
                matches = False
            if not matches:
                errors.append(
                    f"FastQC field mismatch for {field}: expected {expected!r}, "
                    f"observed {sample_data.get(field)!r}"
                )

    sources = load_json(data_dir / "multiqc_sources.json")
    expected_sources = {"FastQC": {"all_sections": {"test_R1": paths["input_file"]}}}
    compare(errors, "MultiQC source map", sources, expected_sources)

    log_line_pattern = re.compile(
        r"^\[(?P<timestamp>[^\]]+)\]\s+"
        r"(?P<logger>\S+)\s+\[(?P<level>[A-Z]+)\s+\]\s+"
        r"Found (?P<count>[0-9]+) reports\s*$"
    )
    parsed_report_counts = []
    for line in read_text_compat(data_dir / "multiqc.log").splitlines():
        match = log_line_pattern.fullmatch(line)
        if match and match.group("logger") == "multiqc.modules.fastqc.fastqc":
            parsed_report_counts.append(int(match.group("count")))
    if parsed_report_counts != [1]:
        errors.append(
            "MultiQC log must contain exactly one structured FastQC report-count record; "
            f"got {parsed_report_counts!r}"
        )

    input_manifest = load_json(run_root / "input-manifest.json")
    input_file_hash = sha256_file(input_file)
    input_records = [
        {
            "path": paths["input_file"],
            "size": input_file.stat().st_size,
            "sha256": input_file_hash,
        }
    ]
    compare(errors, "input manifest.schema_version", input_manifest.get("schema_version"), "0.1")
    compare(errors, "input manifest.run_id", input_manifest.get("run_id"), run_root.name)
    compare(errors, "input manifest.path_base", input_manifest.get("path_base"), "repository-root")
    compare(errors, "input manifest.input_root", input_manifest.get("input_root"), paths["input"])
    compare(errors, "input manifest.files", input_manifest.get("files"), input_records)
    aggregate_records = [
        {
            "path": input_file.relative_to(expected_case_path(output, "inputs")).as_posix(),
            "size": input_file.stat().st_size,
            "sha256": input_file_hash,
        }
    ]
    aggregate = sha256(json.dumps(aggregate_records, sort_keys=True).encode("utf-8")).hexdigest()
    compare(errors, "input manifest.sha256", input_manifest.get("sha256"), aggregate)

    artifact_manifest = load_json(run_root / "artifact-manifest.json")
    artifact_records = []
    expected_artifacts = [
        ("report", report),
        ("data", data_dir / "multiqc_data.json"),
        ("log", data_dir / "multiqc.log"),
        ("sources", data_dir / "multiqc_sources.json"),
    ]
    for key, path in expected_artifacts:
        artifact_records.append(
            {
                "path": paths[key],
                "exists": True,
                "size": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    compare(errors, "artifact manifest.schema_version", artifact_manifest.get("schema_version"), "0.1")
    compare(errors, "artifact manifest.run_id", artifact_manifest.get("run_id"), run_root.name)
    compare(errors, "artifact manifest.path_base", artifact_manifest.get("path_base"), "repository-root")
    compare(errors, "artifact manifest.run_root", artifact_manifest.get("run_root"), paths["output"])
    compare(errors, "artifact manifest.artifacts", artifact_manifest.get("artifacts"), artifact_records)

    multiqc_review = read_text_compat(run_root / "multiqc-review.md")
    if f"- Input: {paths['input']}" not in multiqc_review:
        errors.append("MultiQC review does not use the repository-relative input path")
    if f"- Output: {paths['output']}" not in multiqc_review:
        errors.append("MultiQC review does not use the repository-relative output path")

    review = read_text_compat(run_root / "research-core-review.md")
    _, status_errors = review_status_block(review)
    errors.extend(status_errors)
    if not has_exact_line_sequence(
        review.splitlines(),
        [
            "This record does not approve scientific release, and a generated report is not a",
            "QC threshold verdict or downstream biological validation.",
        ],
    ):
        errors.append("research-core review is missing the exact non-release boundary statement")
    if "Path base: `repository-root`" not in review:
        errors.append("research-core review must declare its repository-root path base")
    return errors


def verify_negative(output: Path) -> list[str]:
    errors: list[str] = []
    paths = expected_paths(output)
    run_root = output.resolve()
    verdict = load_json(run_root / "multiqc-verdict.json")
    compare(errors, "verdict.status", verdict.get("status"), "failed")
    compare(errors, "verdict.ok", verdict.get("ok"), False)
    compare(errors, "verdict.release_ready", verdict.get("release_ready"), False)
    expected_input = paths["input"] + "/does-not-exist"
    expected_error = f"MultiQC input directory does not exist: {expected_input}"
    compare(errors, "verdict.input", verdict.get("input"), expected_input)
    compare(errors, "verdict.output", verdict.get("output"), paths["output"])
    check_relative(errors, "verdict.input", verdict.get("input"))
    check_relative(errors, "verdict.output", verdict.get("output"))
    compare(errors, "verdict.command", verdict.get("command"), None)
    compare(errors, "verdict.runtime", verdict.get("runtime"), None)
    compare(errors, "verdict.error", verdict.get("error"), expected_error)
    review_path = run_root / "multiqc-review.md"
    if review_path.is_file():
        review = read_text_compat(review_path)
        if f"- Input: {expected_input}" not in review:
            errors.append("negative MultiQC review does not use the repository-relative input path")
        if f"- Output: {paths['output']}" not in review:
            errors.append("negative MultiQC review does not use the repository-relative output path")
    else:
        errors.append(f"missing negative review: {review_path}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--case", choices=("positive", "negative"), default="positive")
    args = parser.parse_args()
    try:
        errors = (
            verify_negative(args.output)
            if args.case == "negative"
            else verify_positive(args.output)
        )
    except AssertionError as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(json.dumps({"ok": True, "case": args.case, "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
