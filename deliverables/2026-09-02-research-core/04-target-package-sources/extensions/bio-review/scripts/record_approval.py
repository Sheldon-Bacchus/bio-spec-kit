#!/usr/bin/env python3
"""Persist an explicit human review decision."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", required=True)
    parser.add_argument("--decision", choices=("approve", "reject", "waiver"), required=True)
    parser.add_argument("--reviewer", default=os.environ.get("BIO_REVIEWER", "unknown"))
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--reason", default="")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    output = args.output or Path(".bio/runs/current/approvals") / f"{args.stage}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "schema_version": "1",
        "stage": args.stage,
        "decision": args.decision,
        "reviewer": args.reviewer,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "evidence": args.evidence,
        "reason": args.reason,
    }
    output.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(record, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

