# Tasks: Frozen DEG shared-integration vertical slice

## Phase 1: Spec and contract

- [X] T001 Define the frozen DEG table contract and descriptive-only claim boundary.
- [X] T002 Define explicit identifier normalization and duplicate policies.

## Phase 2: Deterministic execution

- [X] T003 Add the table-level integration extension and command entrypoint.
- [X] T004 Emit shared, membership, four direction, summary, manifest, verdict, and claim artifacts.
- [X] T005 Add the known-answer fixture.

## Phase 3: Verification

- [X] T006 Add positive, duplicate, direction-conflict, row-order, and input-change tests.
- [X] T007 Run the wrapper against the archived PA/LUAD DEG tables with the explicit duplicate policy.
- [X] T008 Compare the real run summary with the archived shared-149 reference artifact.
- [ ] T009 Add the offline pathway slice after this integration contract is stable.
