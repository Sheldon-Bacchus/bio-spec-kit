# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`

**Created**: [DATE]

**Status**: Draft

**Input**: User description: "$ARGUMENTS"

## Research Framing

<!-- Keep this section about the scientific question, not the implementation. -->

- **Scientific question**:
- **Primary estimand**:
- **Hypothesis or decision target**:
- **Population / system**:
- **Sample unit and replication**:
- **Primary comparison**:
- **Scope**:
- **Evidence boundary**: What this feature may support and must not support.
- **Known unknowns**: Record unresolved choices instead of silently filling them in.

## Capability Demand

<!-- State the capability the feature needs; do not teach the method here. -->

- **Required capability**: What domain function must be provided?
- **Candidate `skill_id`**: [Optional; resolve or mark for clarification during planning]
- **Required inputs**: [Named inputs and identity requirements]
- **Required outputs**: [Named outputs, decisions, or evidence]
- **Capability non-goals**: [Methods or claims explicitly out of scope]

## User Scenarios & Testing *(mandatory)*

### User Story 1 - [Brief Title] (Priority: P1)

[Describe the smallest independently valuable research decision or user journey]

**Why this priority**: [Explain the value and priority]

**Independent Test**: [Describe the smallest test that demonstrates value]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [observable outcome]
2. **Given** [initial state], **When** [action], **Then** [observable outcome]

### User Story 2 - [Brief Title] (Priority: P2)

[Optional independently testable follow-up journey]

**Independent Test**: [How to verify it independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [observable outcome]

### Edge Cases

- Missing or invalid sample metadata:
- Missing input, reference, or evidence source:
- QC, validation, or provenance failure:
- Evidence insufficient to support the requested claim:
- Conflicting results or changed input identity:

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The feature MUST make the scientific question and primary estimand explicit.
- **FR-002**: The feature MUST define population, sample unit, comparison, and scope.
- **FR-003**: The feature MUST define input identity and validation criteria.
- **FR-004**: The feature MUST distinguish observations from interpretation and claims.
- **FR-005**: The feature MUST record provenance sufficient for audit or reproduction.
- **FR-006**: The feature MUST stop or record an explicit non-release state when a required check fails.
- **FR-007**: Unresolved load-bearing choices MUST be marked for clarification rather than silently assumed.

### Key Entities *(include if feature involves data)*

- **Question**: The scientific question and estimand being investigated.
- **Observable**: A measured or computed value with source and run identity.
- **Validation**: A deterministic or human check applied to one or more observables.
- **Claim**: A bounded interpretation linked to observables and validations.
- **Run**: One execution with inputs, outputs, parameters, and provenance.

## Evidence and Acceptance Criteria

| ID | Criterion | Evidence path or validation command | Failure action |
|---|---|---|---|
| QC-001 | [Explicit quality criterion] | [Path or command] | [Stop/review/repair] |
| VAL-001 | [Explicit validation criterion] | [Path or command] | [Stop/review/repair] |
| REL-001 | [Release boundary criterion] | [Path or command] | [Do not release] |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The P1 user story can be demonstrated from a clean, bounded fixture or dataset.
- **SC-002**: Every supported or release-candidate claim has an observable, validation result, and evidence path.
- **SC-003**: A reviewer can distinguish supported, inconclusive, not-supported, and not-evaluable outcomes.

## Assumptions

- [Assumption about users, data, environment, or reference identity]
- [Assumption about the scope boundary]
- [Dependency that must be available before execution]
