---
name: speckit-bio-qc-run
description: Evaluate QC metrics against explicit thresholds
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: bio-qc:commands/run.md
---

# QC evaluation

Run the deterministic QC evaluator. The input metrics and thresholds must be
machine-readable and versioned. Report the verdict, failed metrics, and the
evidence path. Never replace a failed metric with an unrecorded assumption.

User request:

$ARGUMENTS