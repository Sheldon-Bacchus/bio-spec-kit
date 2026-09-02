# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

## Summary

[Extract the primary requirement and the smallest technical approach from the
feature specification and research notes.]

## Technical Context

**Language/Version**: [e.g., Python 3.11 or NEEDS CLARIFICATION]

**Primary Dependencies**: [e.g., MultiQC, Nextflow, pandas or NEEDS CLARIFICATION]

**Storage**: [files, object storage, database, or N/A]

**Testing**: [test command and fixture strategy]

**Target Platform**: [platform or NEEDS CLARIFICATION]

**Project Type**: [library/CLI/pipeline/documentation or NEEDS CLARIFICATION]

**Constraints**: [resource, reproducibility, privacy, or safety constraints]

**Scale/Scope**: [bounded MVP scope]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Evidence before automation:
- Domain contracts first:
- Deterministic execution and provenance:
- Human quality/release gates:
- Small, testable, composable skills:

## Research design and analysis contract

- **Question and estimand**:
- **Study/sample unit**:
- **Inputs and reference identity**:
- **Variables, controls, and covariates**:
- **QC thresholds and failure actions**:
- **Statistical or decision procedure**:
- **Validation and claim boundary**:

Do not silently select thresholds, contrasts, or causal interpretations. Record
unresolved choices in `research.md` and resolve them before execution.

## Pipeline and execution design

```text
specify → plan → tasks → bounded execution → deterministic validation → human review
```

Describe which Spec Kit workflow steps orchestrate the lifecycle and which
pipeline engine (if any) performs the scientific computation. Spec Kit is the
coordination layer; Nextflow, Snakemake, or another engine remains responsible
for the computational DAG.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
presets/                 # reusable Spec Kit templates
extensions/              # deterministic commands and scripts
workflows/               # official Spec Kit workflow definitions
tests/                   # fixture and integration tests
```

**Structure Decision**: [Select and explain the concrete directories for this feature.]

## Provenance and review gates

- **Inputs**: paths, identifiers, versions, and hashes:
- **Outputs**: artifact paths and content checks:
- **Runtime**: repository revision, parameters, environment, and logs:
- **Review gates**: design, QC/validation, and release:
- **Failure policy**: stop, preserve verdict, and record repair or waiver:

## Validation strategy

- Fixture dataset or dry run:
- Unit/contract checks:
- End-to-end workflow command:
- Expected machine-readable evidence:
- Human-observable report:

## Complexity Tracking

> Fill only if the constitution check has a justified violation.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| [None or documented violation] | | |
