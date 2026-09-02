---
name: speckit-bio-pipeline-run
description: Run a versioned Nextflow or Snakemake pipeline
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: bio-pipeline:commands/run.md
---

# Pipeline execution

Confirm the approved manifest, QC verdict, engine, reference, and execution
profile before running. Use the deterministic runner, which passes arguments
as a subprocess list and never evaluates agent-generated shell text.

User request:

$ARGUMENTS