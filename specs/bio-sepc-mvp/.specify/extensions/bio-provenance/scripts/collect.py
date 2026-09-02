#!/usr/bin/env python3
"""Collect a small, portable provenance manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_revision(root: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path(".bio/runs/current/provenance"))
    parser.add_argument(
        "--path",
        action="append",
        default=[".bio/manifest.json", ".bio/samples.tsv", ".bio/qc/metrics.json", ".bio/qc/thresholds.json"],
        help="relative input path to hash; may be repeated",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    files: list[dict[str, object]] = []
    missing: list[str] = []
    for relative in args.path:
        path = root / relative
        if path.exists() and path.is_file():
            files.append({"path": relative, "size": path.stat().st_size, "sha256": sha256(path)})
        else:
            missing.append(relative)
    manifest = {
        "schema_version": "1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repository_revision": git_revision(root),
        "python": sys.version,
        "platform": platform.platform(),
        "files": files,
        "missing_files": missing,
    }
    (args.output / "provenance.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest))
    return 0 if not missing else 2


if __name__ == "__main__":
    sys.exit(main())

