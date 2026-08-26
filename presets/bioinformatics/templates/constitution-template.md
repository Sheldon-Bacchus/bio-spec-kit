# Bioinformatics Project Constitution

## Governing principles

### 1. Scientific question before implementation

Every analysis begins with a biological question, an estimand, and a stated
scope. Tool choice must serve the question rather than define it.

### 2. Evidence before interpretation

Every important claim must point to a reproducible artifact, metric, figure,
test, or external source. The agent must distinguish observed results from
hypotheses and future work.

### 3. Fail fast and never hide data problems

Missing metadata, invalid references, broken checksums, failed QC, and
ambiguous statistical designs must stop the relevant stage with an actionable
error. Skips require an explicit, recorded waiver.

### 4. Reproducibility is part of the output

Inputs, sample metadata, references, parameters, software versions, container
digests, pipeline revision, logs, and generated reports are first-class
artifacts.

### 5. Human review at scientific decision points

Humans review intake, QC, statistical design, and final release. Approval is
not a substitute for deterministic checks; it is the decision record after
those checks.

### 6. Prototype small, then scale

Every new workflow must have a small fixture dataset and a dry-run path before
production-scale execution.

## Required artifact conventions

- `.bio/manifest.json` — project and assay identity
- `.bio/samples.tsv` — sample-level metadata
- `.bio/runs/<run-id>/` — immutable run evidence
- `provenance.json` — versions, hashes, parameters, and environment
- `approvals/<stage>.json` — human decisions and reasons

## Quality gates

- Intake gate: metadata, references, and design are valid.
- QC gate: configured thresholds pass or a waiver is recorded.
- Statistics gate: contrasts, assumptions, and diagnostics are reviewed.
- Release gate: report, provenance, and outputs are complete.

