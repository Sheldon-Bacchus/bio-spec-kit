# Bulk RNA-seq workflow

This workflow is a lifecycle controller, not a replacement for a production
RNA-seq pipeline. It validates the intake contract, checks QC metrics, pauses
for human review, optionally runs Nextflow or Snakemake, collects provenance,
and records a final release decision.

## Required project files

```text
.bio/
├── manifest.json
├── samples.tsv
└── qc/
    ├── metrics.json
    └── thresholds.json
```

Use `engine=skip` to test lifecycle wiring. Use `engine=nextflow` only when
`.bio/pipeline/main.nf` exists, or `engine=snakemake` when
`.bio/pipeline/Snakefile` exists.

## Gate policy

The initial workflow uses hard-stop gates. A future assay-specific overlay may
add a documented waiver branch, but the waiver must create an explicit review
record rather than silently continuing.

