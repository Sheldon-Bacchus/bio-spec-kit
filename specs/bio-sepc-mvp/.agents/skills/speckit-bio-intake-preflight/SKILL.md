---
name: speckit-bio-intake-preflight
description: Validate the bioinformatics manifest and sample metadata
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: bio-intake:commands/preflight.md
---

# Intake preflight

Run the deterministic intake validator before proposing an analysis. Read the
resulting JSON verdict and report every error. Do not continue to QC or primary
analysis while the verdict is failing.

Expected inputs are `.bio/manifest.json` and `.bio/samples.tsv`. Preserve the
report and verdict under the current run's evidence directory.

User request:

$ARGUMENTS