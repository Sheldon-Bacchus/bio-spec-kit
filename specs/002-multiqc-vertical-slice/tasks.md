# Tasks: Verified MultiQC vertical slice

## Phase 1: Skill staging and contract

- [X] T001 Stage five project skill adapters and selected upstream references under `spec-mvp/skills/`.
- [X] T002 Install the five adapter entrypoints into `.agents/skills/` for Codex discovery.
- [X] T003 Record each skill's role, source, executable, preset, and fail-closed exceptions in `spec-mvp/skills/skill-catalog.yml`.

## Phase 2: MultiQC execution

- [X] T004 Add the MultiQC project skill contract and bounded wrapper invocation.
- [X] T005 Add fixture-derived content verification for HTML, parsed JSON, source map, and log.
- [X] T006 Add runtime/version, input manifest, artifact manifest, stdout, and stderr records.
- [X] T007 Make non-empty output directories fail closed unless `--overwrite` is explicit.

## Phase 3: End-to-end verification

- [X] T008 Add a minimal FastQC fixture with a sequence-length distribution section.
- [X] T009 Add a clean-entry unittest that runs the real MultiQC 1.35 executable.
- [X] T010 Add a changed-input test proving parsed output and input hash change.
- [X] T011 Record the actual command, versions, paths, and failure behavior in the MVP handoff.
