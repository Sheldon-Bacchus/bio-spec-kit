#!/usr/bin/env python3
"""Run a conventional Nextflow or Snakemake entrypoint safely."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", choices=("skip", "nextflow", "snakemake"), default="skip")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path(".bio/runs/current/pipeline"))
    args = parser.parse_args()
    root = args.root.resolve()
    args.output.mkdir(parents=True, exist_ok=True)

    if args.engine == "skip":
        verdict = {"schema_version": "1", "stage": "pipeline", "ok": True, "status": "skipped"}
        (args.output / "pipeline-verdict.json").write_text(json.dumps(verdict, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(verdict))
        return 0

    executable = shutil.which(args.engine)
    if not executable:
        verdict = {"schema_version": "1", "stage": "pipeline", "ok": False, "error": f"tool not found: {args.engine}"}
        (args.output / "pipeline-verdict.json").write_text(json.dumps(verdict, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(verdict))
        return 2

    if args.engine == "nextflow":
        entrypoint = root / ".bio" / "pipeline" / "main.nf"
        command = [executable, "run", str(entrypoint)]
    else:
        entrypoint = root / ".bio" / "pipeline" / "Snakefile"
        command = [executable, "--snakefile", str(entrypoint), "--cores", "1"]

    if not entrypoint.exists():
        verdict = {"schema_version": "1", "stage": "pipeline", "ok": False, "error": f"missing entrypoint: {entrypoint}"}
        (args.output / "pipeline-verdict.json").write_text(json.dumps(verdict, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(verdict))
        return 2

    completed = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
    (args.output / "stdout.log").write_text(completed.stdout, encoding="utf-8")
    (args.output / "stderr.log").write_text(completed.stderr, encoding="utf-8")
    verdict = {
        "schema_version": "1",
        "stage": "pipeline",
        "ok": completed.returncode == 0,
        "status": "completed" if completed.returncode == 0 else "failed",
        "engine": args.engine,
        "command": command,
        "returncode": completed.returncode,
        "entrypoint": str(entrypoint),
    }
    (args.output / "pipeline-verdict.json").write_text(json.dumps(verdict, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(verdict))
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())

