"""Run one of the local deterministic Q1 fixtures."""

from __future__ import annotations

import argparse
from pathlib import Path

from kernel import evaluate


SCENARIOS = {
    "supported": "q1-minimal",
    "not-supported": "q1-not-supported",
    "inconclusive": "q1-inconclusive",
    "invalid-provenance": "q1-invalid-provenance",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Evidence Closure Kernel Q1 demo")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="supported")
    parser.add_argument("--output", type=Path, required=True, help="Directory for generated artifacts")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    input_dir = root / "examples" / SCENARIOS[args.scenario]
    result = evaluate(input_dir, args.output)
    print(f"scenario={args.scenario}")
    print(f"claim_status={result.get('claim_status')}")
    print(f"validation_status={result.get('validation_status', result.get('status'))}")
    print(f"release_ready={result.get('release_ready')}")
    return 0 if result.get("status") == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())

