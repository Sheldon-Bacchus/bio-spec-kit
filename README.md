# Bio Spec Kit

Reusable GitHub Spec Kit components for evidence-first bioinformatics work.

The unified project map, decision log, MVP boundaries, validation layers, and
current implementation status are maintained in
[BIO-SPEC-KIT-REFERENCE.md](BIO-SPEC-KIT-REFERENCE.md). Read that file first
before adding a new preset, extension, workflow, Skill, or research Feature.

This repository is intentionally a composition layer around Spec Kit:

- `presets/bioinformatics` changes the language, templates, and agent prompts.
- `extensions/*` provide deterministic checks and reusable commands.
- `workflows/*` define lifecycle order and human review gates.
- `bundles/*` package a tested stack for one-command installation.

The actual scientific computation remains in Nextflow, Snakemake, or another
versioned pipeline engine. Spec Kit coordinates intent, evidence, review, and
reproducibility; it is not a replacement for a workflow engine.

## First workflow

The initial workflow is `bulk-rnaseq`. It expects a project with:

```text
.bio/
├── manifest.json
├── samples.tsv
├── qc/metrics.json
└── pipeline/
    ├── main.nf       # when engine=nextflow
    └── Snakefile     # when engine=snakemake
```

The pipeline engine can be set to `skip` for a dry lifecycle test.

## Local development

From a clean Spec Kit project:

```powershell
specify init --here --integration codex --force
specify preset add --dev .\presets\bioinformatics
specify extension add --dev .\extensions\bio-intake
specify extension add --dev .\extensions\bio-qc
specify extension add --dev .\extensions\bio-pipeline
specify extension add --dev .\extensions\bio-provenance
specify extension add --dev .\extensions\bio-review
specify workflow add --dev .\workflows\bulk-rnaseq
specify workflow run bulk-rnaseq -i engine=skip
```

The package can be installed as a local bundle after validation:

```powershell
specify bundle validate --path .\bundles\bioinformatics-core
specify bundle build --path .\bundles\bioinformatics-core --output .\dist
specify bundle install .\dist\bioinformatics-core-0.1.0.zip
```

## Official-first research MVP

The narrower research MVP keeps the official Spec Kit lifecycle and adds only
research fields to the templates plus one callable workflow. It is deliberately
separate from the broader `bioinformatics` preset and from the five research
design documents.

```powershell
specify preset add --dev .\presets\bio-research-mvp
specify extension add --dev .\extensions\bio-multiqc
specify extension add --dev .\extensions\bio-review
specify workflow add --dev .\workflows\bio-research-mvp
specify workflow run bio-research-mvp `
  -i spec="Create a bounded MultiQC evidence report for the supplied fixture" `
  -i multiqc_input=tests/fixtures/multiqc `
  -i multiqc_output=.bio/runs/current/multiqc `
  -i multiqc_config=.specify/extensions/bio-multiqc/config/multiqc_config.yaml `
  -i multiqc_preset=fastqc-multiqc-mvp
```

The workflow uses only the official command, shell, and gate step types. The
existing `spec-mvp/workflows/multiqc-vertical-slice.yml` remains a design
reference until the official workflow has been validated locally; it is not
registered as a Spec Kit workflow.

## Evidence contract

Each run should preserve these artifacts under `.bio/runs/<run-id>/`:

- `intake/intake-verdict.json`
- `qc/qc-verdict.json`
- `pipeline/pipeline-verdict.json`
- `provenance/provenance.json`
- `approvals/<stage>.json`
- `report/`

Approval gates are interactive workflow controls. The approval extension also
writes explicit, versionable approval records so a decision is not trapped in
runtime state only.

## Design rules

1. Scientific claims must have an evidence artifact.
2. QC thresholds are configuration, not hidden prompt assumptions.
3. Statistical design is explicit before result interpretation.
4. Tool versions, references, parameters, and input hashes are recorded.
5. Human approval is required before expensive execution and final release.
6. Failed checks stop the workflow unless a documented waiver is recorded.

## Status

This is the first local MVP. It provides a reusable package structure and a
small deterministic core; assay-specific thresholds and production pipeline
implementations should be added only after validating the lifecycle on a small
public dataset.
