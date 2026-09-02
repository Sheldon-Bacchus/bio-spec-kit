#!/usr/bin/env python3
"""Validate the frozen A0-A3 protocol and construction-case boundary."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


EXCLUSION_CODES = {
    "MISSING_INPUT",
    "MISSING_ORACLE",
    "MISSING_VERIFIER",
    "PERMISSION_DENIED",
    "BUDGET_UNAVAILABLE",
    "SCHEMA_INVALID",
    "CONSTRUCTION_LEAKAGE",
}
FAILURE_KEYS = {
    "eligible_timeout",
    "eligible_execution_error",
    "eligible_missing_or_malformed_output",
    "eligible_verifier_error_or_fail",
    "eligible_malformed_trace",
    "eligible_unsupported_claim",
}


class ProtocolError(ValueError):
    """A frozen protocol invariant was violated."""


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ProtocolError(f"cannot read YAML {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ProtocolError(f"YAML root must be an object: {path}")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProtocolError(message)


def validate_matrix(matrix: dict[str, Any]) -> None:
    require(matrix.get("protocol_version") == "0.2", "protocol version must be 0.2")
    require(
        matrix.get("status") == "FROZEN_PROTOCOL / A0-A3_NOT_RUN",
        "matrix must remain frozen with A0-A3 marked not run",
    )
    variants = matrix.get("variants")
    require(isinstance(variants, list), "variants must be a list")
    require(
        all(isinstance(item, dict) for item in variants),
        "each variant must be an object",
    )
    require(
        [item.get("id") for item in variants] == ["A0", "A1", "A2", "A3"],
        "variants must be ordered A0, A1, A2, A3",
    )
    fixed = matrix.get("fixed_comparison_conditions")
    require(isinstance(fixed, list) and len(fixed) >= 5, "fixed comparison conditions are incomplete")

    eligibility = matrix.get("eligibility")
    require(isinstance(eligibility, dict), "eligibility must be an object")
    require(
        eligibility.get("decision_stage") == "before_agent_run",
        "eligibility must be decided before an Agent run",
    )
    required = eligibility.get("required")
    require(isinstance(required, list) and len(required) >= 5, "eligibility checks are incomplete")
    exclusion_codes = eligibility.get("pre_run_exclusion_codes")
    require(isinstance(exclusion_codes, list), "pre-run exclusion codes must be a list")
    require(
        set(exclusion_codes) == EXCLUSION_CODES,
        "pre-run exclusion codes are incomplete or changed",
    )

    failure_accounting = matrix.get("failure_accounting")
    require(isinstance(failure_accounting, dict), "failure_accounting must be an object")
    require(
        set(failure_accounting) == FAILURE_KEYS,
        "failure accounting must cover timeout, execution, output, verifier, trace and claims",
    )
    require(
        all(value == "count_as_failed_repetition" for value in failure_accounting.values()),
        "eligible post-run failures must count as failed repetitions",
    )

    repetition = matrix.get("repetition_policy")
    require(isinstance(repetition, dict), "repetition_policy must be an object")
    require(repetition.get("count_per_case_variant") == 3, "each eligible cell needs three repetitions")
    require(repetition.get("replicate_indices") == [1, 2, 3], "replicate indices must be 1, 2, 3")
    require(
        isinstance(repetition.get("seed_derivation"), str)
        and "case_id" in repetition["seed_derivation"]
        and "replicate_index" in repetition["seed_derivation"],
        "seed derivation must include case and replicate identity",
    )
    require(
        repetition.get("unsupported_seed_record") == "seed_status: unavailable",
        "unsupported seed behavior must be recorded explicitly",
    )
    require(repetition.get("default_determinism") == "strict", "strict determinism must be the default")
    require(
        isinstance(repetition.get("strict_cell_pass"), str)
        and "all repetitions pass" in repetition["strict_cell_pass"]
        and "hashes agree" in repetition["strict_cell_pass"],
        "strict cell pass rule must include all repetitions and hash agreement",
    )

    paired = matrix.get("paired_aggregation")
    require(isinstance(paired, dict), "paired_aggregation must be an object")
    require(
        paired.get("eligible_case_set") == "intersection across A0,A1,A2,A3",
        "paired set must be the intersection across all four variants",
    )
    minimum_eligible = paired.get("minimum_eligible_case_count")
    require(
        isinstance(minimum_eligible, int) and minimum_eligible >= 1,
        "paired minimum must be a positive integer",
    )
    require(
        paired.get("empty_or_insufficient_status") == "NOT_RUN/INSUFFICIENT_ELIGIBLE_CASES",
        "insufficient paired eligibility must suppress scoring",
    )
    require(
        paired.get("denominator") == "eligible case-variant cells, not successful attempts",
        "denominator must use eligible cells",
    )

    authorization = matrix.get("current_authorization")
    require(isinstance(authorization, dict), "current_authorization must be an object")
    require(
        authorization.get("construction_smoke_is_not_a0_a3_cell") is True,
        "construction smoke must not be counted as an A0-A3 cell",
    )
    require(authorization.get("unseen_validation_status") == "NOT_RUN", "unseen validation must remain not run")
    require(authorization.get("effect_score_status") == "NOT_RUN", "effect score must remain not run")


def validate_case(case: dict[str, Any]) -> None:
    require(case.get("case_id") == "multiqc-mvp", "unexpected construction case id")
    require(case.get("variant_id") == "construction-smoke", "construction case must use smoke variant")
    require(case.get("evaluation_role") == "construction_smoke", "construction case role must be explicit")
    eligibility = case.get("eligibility")
    require(isinstance(eligibility, dict), "case eligibility must be an object")
    require(eligibility.get("evaluated_before_run") is True, "case eligibility must be pre-run")
    require(eligibility.get("eligible_for_a0_a3") is False, "construction smoke cannot be A0-A3 eligible")
    exclusion_codes = eligibility.get("pre_run_exclusion_codes")
    require(isinstance(exclusion_codes, list), "case exclusion codes must be a list")
    require(
        set(exclusion_codes) == EXCLUSION_CODES,
        "case exclusion codes must match the frozen protocol",
    )
    failure_accounting = case.get("failure_accounting")
    require(isinstance(failure_accounting, dict), "case failure accounting must be an object")
    require(
        set(failure_accounting) == {
            "eligible_timeout",
            "eligible_nonzero_execution",
            "eligible_missing_or_malformed_output",
            "eligible_verifier_error_or_fail",
            "eligible_malformed_trace",
            "eligible_unsupported_claim",
        },
        "case failure accounting is incomplete",
    )
    require(
        all(value == "failure" for value in failure_accounting.values()),
        "case eligible failures must remain failures",
    )
    repetition = case.get("repetition_policy")
    require(isinstance(repetition, dict), "case repetition policy must be an object")
    require(repetition.get("count") == 3, "case repetition count must be three")
    require(repetition.get("determinism") == "strict", "case determinism must be strict")
    require(
        isinstance(repetition.get("cell_pass_rule"), str)
        and "all three repetitions pass" in repetition["cell_pass_rule"]
        and "hashes agree" in repetition["cell_pass_rule"],
        "case cell pass rule must require three passing repetitions and equal hashes",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--matrix",
        type=Path,
        default=Path("specs/005-skills-nextflow-research-core/evaluation/a0-a3-matrix.yml"),
    )
    parser.add_argument(
        "--case",
        type=Path,
        default=Path("specs/005-skills-nextflow-research-core/evaluation/cases/multiqc-mvp/case.yml"),
    )
    args = parser.parse_args()
    try:
        validate_matrix(load_yaml(args.matrix))
        validate_case(load_yaml(args.case))
    except ProtocolError as exc:
        print(f"ERROR: {exc}")
        return 1
    print("PASS frozen A0-A3 eligibility/repetition protocol")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
