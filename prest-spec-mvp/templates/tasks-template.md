---
description: "Task list template for an evidence-aware research feature"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature]/`

**Prerequisites**: `plan.md` and `spec.md`; use `research.md`, `data-model.md`,
`contracts/`, and `quickstart.md` when generated.

**Tests**: Include test tasks only when requested by the feature specification.

**Organization**: Group tasks by user story so each story remains
independently implementable and testable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel without touching the same files.
- **[Story]**: User story label such as `[US1]`; use `[FOUNDATION]` for shared work.
- Include exact file paths and an evidence path or validation command for every
  task that produces an output or decision record.
- For a capability task, preserve the plan's `skill_id`, declared inputs,
  outputs, acceptance condition, and evidence path. Do not restate the Skill's
  method instructions in the task list.

## Phase 1: Setup

**Purpose**: Confirm the bounded feature boundary before implementation.

- [ ] T001 [FOUNDATION] Confirm the feature directory, sample unit, input boundary, and output/evidence location.
- [ ] T002 [P] [FOUNDATION] Record reference, tool, environment, and repository versions.

---

## Phase 2: Foundational Contracts

**Purpose**: Complete prerequisites that block every user story.

- [ ] T003 [FOUNDATION] Define the input, output, provenance, and claim boundary in `specs/[###-feature]/contracts/`.
- [ ] T004 [FOUNDATION] Define deterministic validation rules and failure actions.
- [ ] T005 [P] [FOUNDATION] Add or identify the bounded fixture or dataset and record its identity.

**Checkpoint**: Foundation reviewed and approved before user-story work.

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Smallest independently testable value]

**Independent Test**: [Exact command and expected evidence]

### Tests for User Story 1 *(optional)*

- [ ] T006 [P] [US1] Add the contract or acceptance test in `[exact test path]`; evidence: `[path]`.

### Implementation for User Story 1

- [ ] T007 [US1] Implement the smallest execution path in `[exact path]`.
- [ ] T008 [US1] Add deterministic verification in `[exact test path]`; evidence: `[path]`.
- [ ] T009 [US1] Record the bounded result, provenance, and claim status in `[exact path]`.

**Checkpoint**: User Story 1 is independently testable and reviewed.

---

## Phase 4: Review and Reproducibility

- [ ] T010 [FOUNDATION] Verify input identity, parameters, tool versions, and run identity.
- [ ] T011 [FOUNDATION] Record the human review decision in `[exact path]`.
- [ ] T012 [FOUNDATION] Run the validation command from `quickstart.md` and preserve the verdict.

## Dependencies and Execution Order

- Setup precedes foundational contracts.
- Foundational contracts and fixtures block user-story execution.
- User Story 1 is the MVP checkpoint.
- Review and reproducibility tasks run only after the evidence and validation exist.

## Implementation Strategy

1. Complete setup and contracts.
2. Implement and validate User Story 1 only.
3. Pause for human review at the MVP gate.
4. Add later user stories or domain extensions only after the vertical slice passes.
