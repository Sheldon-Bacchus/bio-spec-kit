# Implementation Plan: Frozen DEG shared-integration vertical slice

**Branch**: `003-shared-integration-vertical-slice`  
**Spec**: [spec.md](spec.md)

## Architecture

```text
spec.md / plan.md / tasks.md
          ↓
cross-branch-integration Skill
          ↓
extensions/bio-integration/scripts/run_shared_integration.py
          ↓
frozen PA/LUAD DEG tables
          ↓
shared + four direction strata + provenance + claim
```

The wrapper owns deterministic table validation and integration. The Skill owns
the activation boundary. The Spec owns user-observable behavior. The upstream
DEG method remains an input provider, not something silently rerun by this
slice.

## Technical decisions

- Use Python standard library only.
- Treat input tables as already filtered DEG artifacts; the wrapper does not
  recreate upstream FDR thresholds.
- Default to exact identifier matching and duplicate hard failure.
- Permit `max-abs-effect` only as an explicit policy for the known PA duplicate
  symbols; record it in every run.
- Sort all canonical output rows by normalized gene ID.
- Keep the claim descriptive-only and `release_ready=false` until later gates.
- Use the small checked-in fixture for deterministic tests and allow the same
  command to consume the real archived PA/LUAD tables.

## Verification strategy

1. Compile the wrapper.
2. Run the positive fixture and check all four strata.
3. Run the duplicate, direction-conflict, row-order, and changed-input cases.
4. Run the wrapper on the archived PA/LUAD DEG tables using the explicitly
   recorded duplicate policy and compare the summary to the source shared-149
   artifact.
