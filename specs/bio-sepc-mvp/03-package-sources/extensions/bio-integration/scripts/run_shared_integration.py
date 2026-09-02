#!/usr/bin/env python3
"""Run a deterministic, bounded integration of two frozen DEG tables.

This is deliberately a table-level MVP. It does not rerun DEG, pathway
enrichment, WGCNA, or a joint statistical model. The input tables must already
represent the selected DEG sets; the wrapper only validates, normalizes, and
integrates them.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import sys
from pathlib import Path
from typing import Any


WRAPPER_VERSION = "0.1.0"
SCHEMA_VERSION = "0.1"
TRUTHY = {"1", "true", "t", "yes", "y"}
ALLOWED_DIRECTIONS = {"up", "down"}
CATEGORY_ORDER = ("UpUp", "DownDown", "UpDown", "DownUp")


class IntegrationError(Exception):
    """A deterministic input or execution failure."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalize_gene(raw: str, mode: str) -> str:
    value = raw.strip()
    if not value:
        raise IntegrationError("empty_gene_id", "A selected row has an empty gene identifier")
    return value.upper() if mode == "upper" else value


def parse_direction(raw: str, effect: float, *, source: str, line_number: int) -> str:
    direction = raw.strip().lower()
    if direction not in ALLOWED_DIRECTIONS:
        raise IntegrationError(
            "invalid_direction",
            f"Invalid direction {raw!r} in {source}:{line_number}; expected up or down",
        )
    expected = "up" if effect > 0 else "down"
    if direction != expected:
        raise IntegrationError(
            "direction_effect_conflict",
            f"Direction/effect conflict for {source}:{line_number}: {direction} vs {effect}",
        )
    return direction


def read_deg_table(
    path: Path,
    *,
    role: str,
    gene_column: str,
    effect_column: str,
    status_column: str,
    direction_column: str,
    normalization: str,
    duplicate_policy: str,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    if not path.is_file():
        raise IntegrationError("missing_input", f"Missing {role} input: {path}")

    selected_rows = 0
    total_rows = 0
    records: dict[str, dict[str, Any]] = {}
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            headers = set(reader.fieldnames or [])
            required = {gene_column, effect_column}
            if status_column:
                required.add(status_column)
            if direction_column:
                required.add(direction_column)
            missing = sorted(required - headers)
            if missing:
                raise IntegrationError(
                    "invalid_schema",
                    f"{role} table is missing columns: {', '.join(missing)}",
                )
            for line_number, row in enumerate(reader, start=2):
                total_rows += 1
                if status_column and (row.get(status_column) or "").strip().lower() not in TRUTHY:
                    continue
                selected_rows += 1
                gene = normalize_gene(row.get(gene_column) or "", normalization)
                try:
                    effect = float(row.get(effect_column, ""))
                except ValueError as exc:
                    raise IntegrationError(
                        "invalid_effect",
                        f"Non-numeric {effect_column} for {gene} in {path.name}:{line_number}",
                    ) from exc
                if not math.isfinite(effect) or effect == 0:
                    raise IntegrationError(
                        "invalid_effect",
                        f"Selected {role} row has non-finite or zero effect for {gene} in {path.name}:{line_number}",
                    )
                direction = (
                    parse_direction(
                        row.get(direction_column) or "",
                        effect,
                        source=path.name,
                        line_number=line_number,
                    )
                    if direction_column
                    else ("up" if effect > 0 else "down")
                )
                record = {
                    "gene_id": gene,
                    "effect": effect,
                    "direction": direction,
                    "source_line": line_number,
                }
                previous = records.get(gene)
                if previous is None:
                    records[gene] = record
                    continue
                if duplicate_policy == "error":
                    raise IntegrationError(
                        "duplicate_gene_id",
                        f"Duplicate selected gene identifier {gene} in {path.name}:{line_number}",
                    )
                if duplicate_policy == "first":
                    continue
                if duplicate_policy == "max-abs-effect" and abs(effect) > abs(float(previous["effect"])):
                    records[gene] = record
    except UnicodeDecodeError as exc:
        raise IntegrationError("invalid_encoding", f"Input is not UTF-8: {path.name}") from exc

    if not records:
        raise IntegrationError("empty_selected_input", f"No selected DEG rows found in {path.name}")
    return records, {
        "role": role,
        "path": str(path.resolve()),
        "sha256": sha256_file(path),
        "total_rows": total_rows,
        "selected_rows": selected_rows,
        "unique_selected_genes": len(records),
    }


def category(pa_direction: str, luad_direction: str) -> str:
    return {
        ("up", "up"): "UpUp",
        ("down", "down"): "DownDown",
        ("up", "down"): "UpDown",
        ("down", "up"): "DownUp",
    }[(pa_direction, luad_direction)]


def failed_output(output: Path, *, code: str, message: str, input_paths: list[Path]) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=True)
    input_hashes = {str(path.resolve()): sha256_file(path) for path in input_paths if path.is_file()}
    run_id = f"RUN-{hashlib.sha256(canonical_json(input_hashes).encode('utf-8')).hexdigest()[:12]}"
    verdict = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "status": "failed",
        "ok": False,
        "release_ready": False,
        "claim_status": "not_evaluable",
        "error_code": code,
        "error": message,
    }
    write_json(output / "integration-verdict.json", verdict)
    write_json(
        output / "provenance.json",
        {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "input_hashes": input_hashes,
            "output_hashes": {"integration-verdict.json": sha256_file(output / "integration-verdict.json")},
            "status": "invalid",
        },
    )
    write_json(
        output / "run-manifest.json",
        {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "status": "failed",
            "execution_status": "not_completed",
            "input_refs": sorted(input_hashes),
            "output_refs": ["integration-verdict.json"],
        },
    )
    return verdict


def run(args: argparse.Namespace) -> dict[str, Any]:
    pa_path = args.pa.resolve()
    luad_path = args.luad.resolve()
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()) and not args.overwrite:
        raise IntegrationError(
            "output_not_empty",
            f"Output directory is not empty: {output}; use a fresh directory or --overwrite",
        )
    output.mkdir(parents=True, exist_ok=True)

    params = {
        "pa_gene_column": args.pa_gene_column,
        "luad_gene_column": args.luad_gene_column,
        "pa_effect_column": args.pa_effect_column,
        "luad_effect_column": args.luad_effect_column,
        "pa_status_column": args.pa_status_column,
        "luad_status_column": args.luad_status_column,
        "pa_direction_column": args.pa_direction_column,
        "luad_direction_column": args.luad_direction_column,
        "id_normalization": args.id_normalization,
        "duplicate_policy": args.duplicate_policy,
    }
    input_hashes = {
        "pa": sha256_file(pa_path) if pa_path.is_file() else None,
        "luad": sha256_file(luad_path) if luad_path.is_file() else None,
    }
    run_seed = canonical_json({"input_hashes": input_hashes, "parameters": params})
    run_id = f"RUN-{hashlib.sha256(run_seed.encode('utf-8')).hexdigest()[:12]}"

    pa, pa_meta = read_deg_table(
        pa_path,
        role="PA",
        gene_column=args.pa_gene_column,
        effect_column=args.pa_effect_column,
        status_column=args.pa_status_column,
        direction_column=args.pa_direction_column,
        normalization=args.id_normalization,
        duplicate_policy=args.duplicate_policy,
    )
    luad, luad_meta = read_deg_table(
        luad_path,
        role="LUAD",
        gene_column=args.luad_gene_column,
        effect_column=args.luad_effect_column,
        status_column=args.luad_status_column,
        direction_column=args.luad_direction_column,
        normalization=args.id_normalization,
        duplicate_policy=args.duplicate_policy,
    )

    all_genes = sorted(set(pa) | set(luad))
    shared_genes = sorted(set(pa) & set(luad))
    membership_rows: list[dict[str, Any]] = []
    shared_rows: list[dict[str, Any]] = []
    categories: dict[str, list[dict[str, Any]]] = {name: [] for name in CATEGORY_ORDER}
    for gene in all_genes:
        pa_record = pa.get(gene)
        luad_record = luad.get(gene)
        is_shared = pa_record is not None and luad_record is not None
        membership_rows.append(
            {
                "gene_id": gene,
                "pa_present": str(pa_record is not None).lower(),
                "luad_present": str(luad_record is not None).lower(),
                "shared": str(is_shared).lower(),
                "pa_direction": pa_record["direction"] if pa_record else "",
                "luad_direction": luad_record["direction"] if luad_record else "",
            }
        )
        if not is_shared:
            continue
        group = category(pa_record["direction"], luad_record["direction"])
        row = {
            "gene_id": gene,
            "pa_effect": pa_record["effect"],
            "pa_direction": pa_record["direction"],
            "luad_effect": luad_record["effect"],
            "luad_direction": luad_record["direction"],
            "category": group,
        }
        shared_rows.append(row)
        categories[group].append(row)

    result_files = {
        "shared_all.tsv": (list(shared_rows), ["gene_id", "pa_effect", "pa_direction", "luad_effect", "luad_direction", "category"]),
        "shared_membership.tsv": (membership_rows, ["gene_id", "pa_present", "luad_present", "shared", "pa_direction", "luad_direction"]),
    }
    for group in CATEGORY_ORDER:
        result_files[f"shared_{group}.tsv"] = (
            categories[group],
            ["gene_id", "pa_effect", "pa_direction", "luad_effect", "luad_direction", "category"],
        )
    for name, (rows, fields) in result_files.items():
        write_tsv(output / name, fields, rows)

    summary_rows = [
        {"set_name": "PA_DEG", "n": len(pa), "definition": "selected rows from frozen PA DEG table"},
        {"set_name": "LUAD_DEG", "n": len(luad), "definition": "selected rows from frozen LUAD DEG table"},
        {"set_name": "all_shared", "n": len(shared_genes), "definition": "PA_DEG intersect LUAD_DEG after declared ID normalization"},
    ]
    summary_rows.extend(
        {"set_name": group, "n": len(categories[group]), "definition": f"{group} direction stratum"}
        for group in CATEGORY_ORDER
    )
    write_tsv(output / "intersection_summary.tsv", ["set_name", "n", "definition"], summary_rows)

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "inputs": [pa_meta, luad_meta],
        "parameters": params,
        "software": {
            "wrapper": WRAPPER_VERSION,
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
    }
    write_json(output / "input-manifest.json", manifest)

    claim = {
        "schema_version": SCHEMA_VERSION,
        "claim_id": f"C-{run_id[4:]}",
        "run_id": run_id,
        "statement": "在声明的 ID、方向和重复处理规则下，PA 与 LUAD 冻结 DEG 集合存在一个可重算的直接交集，并已按两侧方向分层。",
        "status": "descriptive_only",
        "release_ready": False,
        "does_not_support": ["共同机制", "共同病因", "因果关系", "独立验证", "临床疗效"],
        "limitations": [
            "本步骤不重新执行 DEG，也不评估上游统计模型。",
            "交集和方向一致性是描述性整合，不是独立生物学验证。",
        ],
        "source_artifacts": [str(pa_path), str(luad_path)],
    }
    write_json(output / "claim.json", claim)

    result_hashes = {name: sha256_file(output / name) for name in [*result_files, "intersection_summary.tsv"]}
    provenance = {
        "schema_version": SCHEMA_VERSION,
        "provenance_id": f"P-{run_id[4:]}",
        "run_id": run_id,
        "input_hashes": input_hashes,
        "output_hashes": result_hashes,
        "parameters": params,
        "status": "valid",
    }
    write_json(output / "provenance.json", provenance)

    verdict = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "status": "completed",
        "ok": True,
        "release_ready": False,
        "claim_status": "descriptive_only",
        "category_counts": {group: len(categories[group]) for group in CATEGORY_ORDER},
        "shared_count": len(shared_genes),
        "input_manifest": "input-manifest.json",
        "provenance": "provenance.json",
        "claim": "claim.json",
        "verification": {
            "partition_sum": sum(len(categories[group]) for group in CATEGORY_ORDER) == len(shared_genes),
            "membership_union": len(all_genes) == len(set(pa) | set(luad)),
        },
    }
    write_json(output / "integration-verdict.json", verdict)

    artifact_names = [*result_files, "intersection_summary.tsv", "input-manifest.json", "claim.json", "provenance.json", "integration-verdict.json"]
    write_json(
        output / "artifact-manifest.json",
        {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "artifacts": {name: sha256_file(output / name) for name in artifact_names},
        },
    )
    write_json(
        output / "run-manifest.json",
        {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "status": "completed",
            "execution_status": "completed",
            "input_refs": [str(pa_path), str(luad_path)],
            "output_refs": [*artifact_names, "artifact-manifest.json", "run-manifest.json"],
            "claim_status": "descriptive_only",
        },
    )
    return verdict


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run deterministic frozen DEG branch integration")
    parser.add_argument("--pa", type=Path, required=True)
    parser.add_argument("--luad", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pa-gene-column", default="gene_symbol")
    parser.add_argument("--luad-gene-column", default="gene_symbol")
    parser.add_argument("--pa-effect-column", default="logFC")
    parser.add_argument("--luad-effect-column", default="logFC")
    parser.add_argument("--pa-status-column", default="DEG")
    parser.add_argument("--luad-status-column", default="DEG")
    parser.add_argument("--pa-direction-column", default="direction")
    parser.add_argument("--luad-direction-column", default="direction")
    parser.add_argument("--id-normalization", choices=("exact", "upper"), default="exact")
    parser.add_argument("--duplicate-policy", choices=("error", "first", "max-abs-effect"), default="error")
    parser.add_argument("--overwrite", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = run(args)
    except IntegrationError as exc:
        result = failed_output(args.output.resolve(), code=exc.code, message=exc.message, input_paths=[args.pa.resolve(), args.luad.resolve()])
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("status") == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
