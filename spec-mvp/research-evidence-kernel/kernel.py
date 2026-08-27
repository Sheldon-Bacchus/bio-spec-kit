"""Deterministic, local Evidence Closure Kernel MVP.

This module intentionally uses only the Python standard library.  It evaluates
a small Question -> Observable -> Validation -> Claim chain and writes
machine-readable artifacts.  It is not a biological analysis engine.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "0.1"
REQUIRED_QUESTION_FIELDS = ("id", "text", "estimand", "scope", "decision_rule")


class KernelError(Exception):
    """A deterministic input or execution error with a stable code."""

    def __init__(self, code: str, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise KernelError("missing_input", f"Missing required input: {path.name}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise KernelError("invalid_json", f"Invalid JSON in {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise KernelError("invalid_schema", f"Expected an object in {path.name}")
    return value


def parse_effects(path: Path) -> dict[str, float]:
    if not path.exists():
        raise KernelError("missing_input", f"Missing required input: {path.name}")
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            if reader.fieldnames is None or not {"gene_id", "log2fc"}.issubset(reader.fieldnames):
                raise KernelError(
                    "invalid_schema",
                    f"{path.name} must contain gene_id and log2fc columns",
                )
            effects: dict[str, float] = {}
            for line_number, row in enumerate(reader, start=2):
                gene_id = (row.get("gene_id") or "").strip()
                if not gene_id:
                    raise KernelError("invalid_schema", f"Empty gene_id in {path.name}:{line_number}")
                if gene_id in effects:
                    raise KernelError("duplicate_id", f"Duplicate gene_id {gene_id} in {path.name}")
                try:
                    value = float(row.get("log2fc", ""))
                except ValueError as exc:
                    raise KernelError(
                        "invalid_value",
                        f"Non-numeric log2fc for {gene_id} in {path.name}:{line_number}",
                    ) from exc
                if not math.isfinite(value):
                    raise KernelError("invalid_value", f"Non-finite log2fc for {gene_id} in {path.name}:{line_number}")
                effects[gene_id] = value
    except UnicodeDecodeError as exc:
        raise KernelError("invalid_encoding", f"Input is not UTF-8: {path.name}") from exc
    if not effects:
        raise KernelError("empty_input", f"No effect rows found in {path.name}")
    return effects


def validate_question(question: dict[str, Any]) -> list[str]:
    return [field for field in REQUIRED_QUESTION_FIELDS if not question.get(field)]


def make_run_id(question: dict[str, Any], input_hashes: dict[str, str]) -> str:
    seed = canonical_json({"question": question, "input_hashes": input_hashes})
    return f"RUN-{hashlib.sha256(seed.encode('utf-8')).hexdigest()[:12]}"


def compare_expected_hashes(
    expected: dict[str, Any] | None,
    actual: dict[str, str],
) -> list[str]:
    if not expected:
        return []
    mismatches: list[str] = []
    for name, expected_hash in expected.items():
        actual_hash = actual.get(name)
        if actual_hash != expected_hash:
            mismatches.append(f"{name}: expected {expected_hash}, observed {actual_hash}")
    return mismatches


def _base_artifacts(output_dir: Path, run_id: str, input_hashes: dict[str, str]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "input_hashes": input_hashes,
        "output_hashes": {},
        "software": {"kernel": SCHEMA_VERSION, "python": f"{sys.version_info.major}.{sys.version_info.minor}"},
        "parameters": {},
        "output_dir": str(output_dir),
    }


def evaluate(input_dir: Path, output_dir: Path) -> dict[str, Any]:
    """Evaluate one local fixture and persist the MVP artifacts.

    The return value is the same normalized summary written to
    ``validation-verdict.json``.  Scientific failure states are normal results;
    malformed inputs are persisted as failed/not-evaluable verdicts rather than
    being silently swallowed.
    """

    input_dir = input_dir.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    question_path = input_dir / "question.json"
    pa_path = input_dir / "pa_effects.tsv"
    luad_path = input_dir / "luad_effects.tsv"
    input_paths = [question_path, pa_path, luad_path]
    input_hashes = {
        path.name: sha256_file(path) for path in input_paths if path.exists()
    }
    provisional_run_id = f"RUN-{hashlib.sha256(canonical_json(input_hashes).encode('utf-8')).hexdigest()[:12]}"

    try:
        question = load_json(question_path)
        missing_fields = validate_question(question)
        run_id = make_run_id(question, input_hashes)
        validation_path = input_dir / "validation.json"
        validation_input = load_json(validation_path) if validation_path.exists() else {}

        if missing_fields:
            verdict = {
                "schema_version": SCHEMA_VERSION,
                "run_id": run_id,
                "status": "needs_clarification",
                "claim_status": "not_evaluable",
                "release_ready": False,
                "error_code": "missing_question_fields",
                "missing_fields": missing_fields,
                "blockers": [f"question.{field}" for field in missing_fields],
            }
            _persist_failure(output_dir, verdict, run_id, input_hashes, question)
            return verdict

        rule = question["decision_rule"]
        if not isinstance(rule, dict):
            raise KernelError("invalid_schema", "question.decision_rule must be an object")
        required_rule_fields = ("effect_threshold", "minimum_overlap", "minimum_concordance")
        missing_rule_fields = [field for field in required_rule_fields if field not in rule]
        if missing_rule_fields:
            verdict = {
                "schema_version": SCHEMA_VERSION,
                "run_id": run_id,
                "status": "needs_clarification",
                "claim_status": "not_evaluable",
                "release_ready": False,
                "error_code": "missing_decision_rule_fields",
                "missing_fields": [f"decision_rule.{field}" for field in missing_rule_fields],
                "blockers": [f"decision_rule.{field}" for field in missing_rule_fields],
            }
            _persist_failure(output_dir, verdict, run_id, input_hashes, question)
            return verdict

        pa = parse_effects(pa_path)
        luad = parse_effects(luad_path)
        effect_threshold = float(rule["effect_threshold"])
        minimum_overlap = int(rule["minimum_overlap"])
        minimum_concordance = float(rule["minimum_concordance"])
        if effect_threshold < 0 or minimum_overlap < 1 or not 0 <= minimum_concordance <= 1:
            raise KernelError("invalid_rule", "Decision rule thresholds are out of range")

        actual_expected = question.get("expected_input_hashes")
        if actual_expected is not None and not isinstance(actual_expected, dict):
            raise KernelError("invalid_schema", "expected_input_hashes must be an object")
        provenance_mismatches = compare_expected_hashes(actual_expected, input_hashes)

        pa_responsive = {gene for gene, value in pa.items() if abs(value) >= effect_threshold}
        luad_responsive = {gene for gene, value in luad.items() if abs(value) >= effect_threshold}
        overlap = sorted(pa_responsive & luad_responsive)
        concordant = sorted(gene for gene in overlap if math.copysign(1, pa[gene]) == math.copysign(1, luad[gene]))
        overlap_count = len(overlap)
        concordant_count = len(concordant)
        concordance = concordant_count / overlap_count if overlap_count else 0.0
        main_passed = overlap_count >= minimum_overlap and concordance >= minimum_concordance

        independent_available = bool(validation_input.get("independent_available", False))
        independent_concordance = validation_input.get("independent_concordance")
        independent_minimum = float(validation_input.get("minimum_concordance", minimum_concordance))
        independent_passed = (
            independent_available
            and independent_concordance is not None
            and float(independent_concordance) >= independent_minimum
        )

        if provenance_mismatches:
            claim_status = "not_evaluable"
            validation_status = "not_evaluable"
        elif not main_passed:
            claim_status = "not_supported"
            validation_status = "failed"
        elif not independent_available:
            claim_status = "inconclusive"
            validation_status = "inconclusive"
        elif not independent_passed:
            claim_status = "not_supported"
            validation_status = "failed"
        else:
            claim_status = "supported"
            validation_status = "passed"

        observable = {
            "schema_version": SCHEMA_VERSION,
            "observables": [
                {
                    "id": "O-PA",
                    "name": "PA gene-level effect",
                    "definition": "gene-level log2 fold change",
                    "unit": "log2FC",
                    "value": pa,
                    "source": pa_path.name,
                    "status": "produced",
                },
                {
                    "id": "O-LUAD",
                    "name": "LUAD gene-level effect",
                    "definition": "gene-level log2 fold change",
                    "unit": "log2FC",
                    "value": luad,
                    "source": luad_path.name,
                    "status": "produced",
                },
                {
                    "id": "O-CONCORDANCE",
                    "name": "cross-disease concordance",
                    "definition": "direction-consistent responsive genes divided by responsive overlap",
                    "unit": "fraction",
                    "value": {
                        "overlap_genes": overlap,
                        "concordant_genes": concordant,
                        "overlap_count": overlap_count,
                        "concordant_count": concordant_count,
                        "concordance": concordance,
                    },
                    "source_ids": ["O-PA", "O-LUAD"],
                    "status": "produced",
                },
            ],
            "run_id": run_id,
        }
        write_json(output_dir / "observables.json", observable)

        validation = {
            "schema_version": SCHEMA_VERSION,
            "validation_id": "V-Q1-001",
            "run_id": run_id,
            "target_ids": ["O-PA", "O-LUAD", "O-CONCORDANCE"],
            "status": validation_status,
            "checks": {
                "question_complete": not missing_fields,
                "provenance_valid": not provenance_mismatches,
                "minimum_overlap": {
                    "observed": overlap_count,
                    "required": minimum_overlap,
                    "passed": overlap_count >= minimum_overlap,
                },
                "minimum_concordance": {
                    "observed": concordance,
                    "required": minimum_concordance,
                    "passed": concordance >= minimum_concordance,
                },
                "independent_validation": {
                    "available": independent_available,
                    "observed": independent_concordance,
                    "required": independent_minimum,
                    "passed": independent_passed,
                },
            },
            "provenance_mismatches": provenance_mismatches,
        }
        write_json(output_dir / "validation-verdict.json", validation)

        claim = {
            "schema_version": SCHEMA_VERSION,
            "claim_id": "C-Q1-001",
            "question_id": question["id"],
            "statement": question.get(
                "claim_statement",
                "在指定样本和分析范围内，PA 与 LUAD 存在方向一致的共同转录响应。",
            ),
            "status": claim_status,
            "observable_ids": ["O-PA", "O-LUAD", "O-CONCORDANCE"],
            "validation_ids": ["V-Q1-001"],
            "evidence_ids": question.get("evidence_ids", ["E-INTERNAL-RUN"]),
            "does_not_support": ["共同病因", "因果机制", "临床疗效"],
            "limitations": ["本 MVP 使用固定本地 fixture，不代表真实队列结果。"],
            "provenance_valid": not provenance_mismatches,
            "release_ready": False,
            "review_state": "ready_for_review" if claim_status == "supported" else "blocked_or_downgraded",
        }
        write_json(output_dir / "claim.json", claim)

        output_hashes = {
            path.name: sha256_file(path)
            for path in (output_dir / "observables.json", output_dir / "validation-verdict.json", output_dir / "claim.json")
        }
        provenance = {
            "schema_version": SCHEMA_VERSION,
            "provenance_id": f"P-{run_id[4:]}",
            "run_id": run_id,
            "input_hashes": input_hashes,
            "output_hashes": output_hashes,
            "parameters": {
                "effect_threshold": effect_threshold,
                "minimum_overlap": minimum_overlap,
                "minimum_concordance": minimum_concordance,
                "independent_validation_required": True,
            },
            "software": {"kernel": SCHEMA_VERSION, "python": f"{sys.version_info.major}.{sys.version_info.minor}"},
            "status": "valid" if not provenance_mismatches else "mismatch",
        }
        write_json(output_dir / "provenance.json", provenance)

        run_manifest = {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "status": "succeeded",
            "execution_status": "succeeded",
            "input_refs": sorted(input_hashes),
            "output_refs": ["observables.json", "validation-verdict.json", "claim.json"],
            "provenance_id": provenance["provenance_id"],
        }
        write_json(output_dir / "run-manifest.json", run_manifest)

        summary = {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "status": "completed",
            "validation_status": validation_status,
            "claim_status": claim_status,
            "release_ready": False,
            "review_state": claim["review_state"],
            "observable_ids": [item["id"] for item in observable["observables"]],
            "provenance_valid": not provenance_mismatches,
            "provenance_mismatches": provenance_mismatches,
        }
        write_json(output_dir / "summary.json", summary)
        return summary

    except KernelError as exc:
        run_id = provisional_run_id
        status = "failed_retryable" if exc.retryable else "failed_terminal"
        verdict = {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "status": status,
            "claim_status": "not_evaluable",
            "release_ready": False,
            "error_code": exc.code,
            "error": exc.message,
        }
        _persist_failure(output_dir, verdict, run_id, input_hashes, {})
        return verdict


def _persist_failure(
    output_dir: Path,
    verdict: dict[str, Any],
    run_id: str,
    input_hashes: dict[str, str],
    question: dict[str, Any],
) -> None:
    write_json(output_dir / "validation-verdict.json", verdict)
    write_json(
        output_dir / "provenance.json",
        {
            "schema_version": SCHEMA_VERSION,
            "provenance_id": f"P-{run_id[4:]}",
            "run_id": run_id,
            "input_hashes": input_hashes,
            "output_hashes": {"validation-verdict.json": sha256_file(output_dir / "validation-verdict.json")},
            "status": "invalid" if verdict.get("status", "").startswith("failed") else "incomplete",
        },
    )
    write_json(
        output_dir / "run-manifest.json",
        {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "status": verdict.get("status", "failed_terminal"),
            "execution_status": "not_started",
            "input_refs": sorted(input_hashes),
            "output_refs": ["validation-verdict.json"],
            "provenance_id": f"P-{run_id[4:]}",
        },
    )
    if question:
        write_json(output_dir / "question.json", question)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the local Evidence Closure Kernel MVP")
    parser.add_argument("--input", type=Path, required=True, help="Fixture directory")
    parser.add_argument("--output", type=Path, required=True, help="Output directory")
    args = parser.parse_args(argv)
    result = evaluate(args.input, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("status") == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
