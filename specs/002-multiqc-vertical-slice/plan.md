# Implementation Plan: Verified MultiQC vertical slice

**Branch**: `002-multiqc-vertical-slice` | **Date**: 2026-08-26
**Spec**: [spec.md](spec.md)

## Architecture

```text
spec.md / plan.md / tasks.md
          ↓ read by Agent during the Spec Kit workflow
.agents/skills/multiqc/SKILL.md
          ↓ selected preset and bounded command
extensions/bio-multiqc/scripts/run_multiqc.py
          ↓ subprocess argv
.venv/Scripts/multiqc.exe 1.35
          ↓ parser
multiqc_report.html + multiqc_report_data/ + verdict/manifests
```

The Spec Core owns black-box behavior and acceptance. The Agent Skills Core owns
activation instructions and the fixed preset. The Execution / Workflow Core owns
the wrapper, external process, logs, artifact verification, and run state.

## Technical decisions

- Use the existing Python wrapper and installed MultiQC 1.35.
- Use a minimal FastQC `fastqc_data.txt` fixture, not a downloaded dataset.
- Use Python standard library for wrapper verification; no new dependency is
  required for the vertical slice.
- Derive the data directory from the report filename because MultiQC 1.35 emits
  `multiqc_report_data/` for `multiqc_report.html`.
- Treat the HTML as a user-facing view and JSON/log/source-map as evidence.
- Keep `--mode skip` for lifecycle wiring only and never mark it release-ready.
- Use a fresh output directory by default; overwriting requires explicit
  `--overwrite`.

## Files and responsibilities

| Area | Files | Responsibility |
|---|---|---|
| Skill Core | `.agents/skills/multiqc/`, `spec-mvp/skills/multiqc/` | discovery, contract, references, preset use |
| Execution Core | `extensions/bio-multiqc/scripts/run_multiqc.py` | process invocation, manifests, content checks |
| Config | `extensions/bio-multiqc/config/multiqc_config.yaml` | report presentation and JSON output |
| Spec Core | `specs/002-multiqc-vertical-slice/*` | user-observable contract and tasks |
| Fixture/test | `tests/fixtures/multiqc/`, `spec-mvp/tests/` | deterministic source input and end-to-end test |

## Verification strategy

1. Compile the wrapper.
2. Run the standard-library unittest against a fresh temporary directory.
3. Assert the wrapper's exit code and verdict.
4. Read MultiQC 1.35 JSON, log, source map, and HTML markers.
5. Repeat with one fixture value changed and assert both the parsed result and
   input hash change.
