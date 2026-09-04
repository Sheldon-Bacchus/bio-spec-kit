# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the official Spec Kit plan command.

## Summary

[Extract the primary requirement and the smallest technical approach from the
feature specification and research notes.]

## Technical Context

**Language/Version**: [e.g., Python 3.12 or NEEDS CLARIFICATION]

**Primary Dependencies**: [e.g., a named pipeline engine or NEEDS CLARIFICATION]

**Storage**: [files, object storage, database, or N/A]

**Testing**: [test command and bounded fixture strategy]

**Target Platform**: [platform or NEEDS CLARIFICATION]

**Project Type**: [library/CLI/pipeline/documentation or NEEDS CLARIFICATION]

**Performance Goals**: [domain-specific or NEEDS CLARIFICATION]

**Constraints**: [reproducibility, privacy, safety, or resource constraints]

**Scale/Scope**: [bounded MVP scope]

## Research Design

- **Question and estimand**:
- **Population and sample unit**:
- **Inputs and reference identity**:
- **Variables, controls, covariates, and contrasts**:
- **QC and exclusion rules**:
- **Statistical or decision procedure**:
- **Validation design and independence**:
- **Claim boundary and non-goals**:

Do not silently select thresholds, contrasts, references, or causal
interpretations. Record unresolved choices in `research.md` and resolve them
before execution.

## Capability Bindings

This section is the handoff from the Spec Kit control plane to the Bio Skill
capability plane. Define what capability is needed and what the selected Skill
must receive and return. Do not copy a method handbook into this plan.

### Required Capabilities

```yaml
required_capabilities:
  - capability: [domain function required by the feature]
    skill_id: [Bio Skill identifier or NEEDS CLARIFICATION]
    inputs:
      - [named input and identity]
    outputs:
      - [named output or decision record]
    assumptions:
      - [assumption that affects the capability]
    parameters:
      [parameter name]: [value, range, or NEEDS CLARIFICATION]
    constraints:
      - [scientific, data, or reproducibility constraint]
    acceptance:
      - [observable condition for accepting the capability result]
    evidence:
      - [evidence path, validation command, or NEEDS CLARIFICATION]
```

Each executable or analytical step must be traceable to one capability entry.
The `skill_id` names the Bio Skill that owns method selection, failure modes,
tool routing, and result interpretation. If the binding is not known, leave it
as a clarification item instead of inventing a Skill or a method.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Evidence is defined before interpretation:
- Domain contracts and acceptance criteria are explicit:
- Deterministic checks and provenance are planned:
- Human review is required at consequential gates:
- The scope remains the smallest independently testable slice:

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
src/                         # implementation, when applicable
tests/                       # unit, contract, and integration tests
docs/                        # project documentation, when applicable
```

**Structure Decision**: [Document the selected structure and reference the
real directories. Remove unused entries from the delivered plan.]

## Provenance and Review Gates

- **Inputs**: paths, identifiers, versions, and hashes:
- **Outputs**: evidence paths and content checks:
- **Runtime**: repository revision, parameters, environment, and logs:
- **Review gates**: specification, design, validation, and release:
- **Failure policy**: stop, preserve the verdict, and record repair or waiver:

## Validation Strategy

- Bounded fixture or dry run:
- Unit and contract checks:
- End-to-end command, if explicitly in scope:
- Expected machine-readable evidence:
- Human-observable review material:

## Complexity Tracking

> Fill only if Constitution Check has a justified violation.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| [None or documented violation] | | |
