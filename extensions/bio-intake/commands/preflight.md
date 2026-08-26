---
description: "Validate the bioinformatics manifest and sample metadata"
---

# Intake preflight

Run the deterministic intake validator before proposing an analysis. Read the
resulting JSON verdict and report every error. Do not continue to QC or primary
analysis while the verdict is failing.

Expected inputs are `.bio/manifest.json` and `.bio/samples.tsv`. Preserve the
report and verdict under the current run's evidence directory.

User request:

$ARGUMENTS

