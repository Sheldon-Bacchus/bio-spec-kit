---
description: "Task list template for an evidence-aware research feature"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`

**Prerequisites**: `plan.md` and `spec.md`; use `research.md`, `data-model.md`,
`contracts/`, and `quickstart.md` when generated.

**Format**: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel without touching the same files.
- **[Story]**: User story label such as `[US1]`; use `[FOUNDATION]` for shared work.
- Include exact file paths and a validation command or evidence path in every
  task that produces an artifact.

## Phase 1: Setup

- [ ] T001 [FOUNDATION] Confirm the feature directory, fixture boundary, and run output path.
- [ ] T002 [P] [FOUNDATION] Record tool, reference, and environment versions in the plan.

## Phase 2: Foundational contracts

- [ ] T003 [FOUNDATION] Define the input/output contract in `specs/[###-feature]/contracts/`.
- [ ] T004 [FOUNDATION] Define deterministic validation rules and failure actions.
- [ ] T005 [FOUNDATION] Add or update the bounded fixture in `tests/fixtures/`.

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Smallest independently testable value]

**Independent Test**: [Exact command and expected evidence]

- [ ] T006 [US1] Implement the smallest execution path in `[exact path]`.
- [ ] T007 [US1] Add deterministic verification in `[exact test path]`; evidence: `[path]`.
- [ ] T008 [US1] Add the human-observable report or review artifact in `[exact path]`.

## Phase 4: Review and reproducibility

- [ ] T009 [FOUNDATION] Record input/output hashes, parameters, tool versions, and run identity in `[exact path]`.
- [ ] T010 [FOUNDATION] Add the review gate and persist the decision in `[exact path]`.
- [ ] T011 [FOUNDATION] Run the full validation command from `quickstart.md` and preserve the verdict.

## Dependencies and execution order

- Setup precedes foundational contracts.
- Foundational contracts and fixtures block user-story execution.
- User Story 1 is the MVP checkpoint.
- Review and reproducibility tasks run only after the artifact and validation exist.

## Implementation strategy

1. Complete setup and contracts.
2. Implement and validate User Story 1 only.
3. Pause for human review at the MVP gate.
4. Add later user stories or domain extensions only after the vertical slice passes.
