# Analysis Plan

## Technical context

- Pipeline engine:
- Execution profile:
- Runtime / container:
- Reference data:
- Expected scale:

## Pipeline design

```text
intake → QC → primary analysis → statistical analysis → provenance → report
```

## Data model and contracts

Describe `.bio/manifest.json`, `.bio/samples.tsv`, reference locks, run
directories, and machine-readable verdicts.

## QC plan

| Metric | Threshold | Source | Failure action |
|---|---|---|---|
| | | | |

## Statistical plan

- Primary model:
- Contrasts:
- Multiple-testing method:
- Batch / covariate handling:
- Sensitivity analyses:
- Assumption diagnostics:

## Reproducibility plan

- Input checksums:
- Pipeline revision:
- Tool versions:
- Container / environment lock:
- Parameters:
- Logs and reports:

## Human review gates

1. Intake and design
2. QC
3. Statistical interpretation
4. Final release

## Validation strategy

- Fixture dataset:
- Dry run:
- Unit checks:
- End-to-end check:
- Expected evidence:

