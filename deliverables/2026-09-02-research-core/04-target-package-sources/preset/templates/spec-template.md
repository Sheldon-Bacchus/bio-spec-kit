# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`

**Created**: [DATE]

**Status**: Draft

**Input**: User description: "$ARGUMENTS"

## Research framing

<!-- Keep this section about what is being investigated, not which tool will be used. -->

- **Scientific question**:
- **Hypothesis**:
- **Primary estimand**:
- **Scope and population**:
- **Claim boundary**: What this work may support, and what it must not claim.
- **Known unknowns**: List unresolved choices instead of silently filling them in.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - [Brief Title] (Priority: P1)

[Describe the user journey or research decision in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe the smallest test that demonstrates value]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

### User Story 2 - [Brief Title] (Priority: P2)

[Optional second independently testable journey]

**Independent Test**: [How to verify it independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

### Edge Cases

- Missing or invalid metadata:
- Missing reference, tool, or input artifact:
- QC or validation failure:
- Evidence insufficient to support the requested claim:

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The workflow MUST make the scientific question and primary estimand explicit.
- **FR-002**: The workflow MUST define input identity, scope, and validation criteria.
- **FR-003**: The workflow MUST produce a machine-readable verdict for each required check.
- **FR-004**: The workflow MUST preserve enough provenance to reproduce the reported artifact.
- **FR-005**: The workflow MUST stop or record an explicit rejection when a required check fails.
- **FR-006**: The workflow MUST distinguish observed results from interpretation and unsupported claims.

### Key Entities *(include if this feature involves data)*

- **Question**: The biological question and estimand being investigated.
- **Observable**: A measured or computed value with source and run identity.
- **Validation**: A deterministic or human check applied to one or more observables.
- **Claim**: A bounded interpretation linked to observables and validations.
- **Run**: One execution with inputs, outputs, parameters, and provenance.

## Research acceptance criteria

| ID | Criterion | Evidence artifact or validation command | Failure action |
|---|---|---|---|
| QC-001 | [Explicit QC criterion] | [Path or command] | [Stop/review/repair] |
| VAL-001 | [Validation criterion] | [Path or command] | [Stop/review/repair] |
| REL-001 | [Release completeness criterion] | [Path or command] | [Do not release] |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The primary user story can be demonstrated from a clean, bounded fixture or dataset.
- **SC-002**: Every release-bound result has a machine-readable verdict and evidence path.
- **SC-003**: A reviewer can distinguish supported, inconclusive, and not-evaluable outcomes.

## Assumptions and non-goals

- [Assumption about the data, environment, or intended users]
- [Assumption about the reference, sample unit, or study design]
- [Non-goal for this MVP]
