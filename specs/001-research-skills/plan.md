# Implementation Plan: Scientific and Bioinformatics Skill Research

**Branch**: 001-research-skills | **Date**: 2026-08-26 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from specs/001-research-skills/spec.md

## Summary

Create a read-only, evidence-backed research catalog with two disjoint
categories: broad scientific Agent skills and bioinformatics-specific Agent
skills. Each candidate receives an invocation contract, evidence record,
weighted score, integration tier, and bounded Spec Kit mapping. The first
implementation phase will document decisions and validation contracts; it will
not install or execute third-party skills.

## Technical Context

**Language/Version**: Markdown, YAML, and JSON; existing Python validation
scripts in the repository remain the only executable support.

**Primary Dependencies**: Spec Kit project templates and workflow; Git for
versioned evidence; optional upstream documentation and public repository pages.
No third-party skill is a runtime dependency in this phase.

**Storage**: Versioned files under specs/001-research-skills and, after review,
the repository catalogs/ directory.

**Testing**: Markdown review, YAML/JSON parsing, contract-field validation,
classification review, and git diff checks. No unreviewed external command is
executed.

**Target Platform**: Local Git repository used by Codex and other Agent hosts.

**Project Type**: Research catalog and Spec Kit design artifact for reusable
preset, extension, bundle, and adapter decisions.

**Performance Goals**: A maintainer can reproduce a candidate tier decision in
under 10 minutes; a research snapshot can be reviewed in under 30 minutes.

**Constraints**: Discovery is read-only; no credentials or project data leave
the repository; volatile stars/releases/commits are observation-date values;
unverified license or data flow blocks default-bundle admission.

**Scale/Scope**: Two catalogs with at least 6 broad scientific candidates and
8 bioinformatics candidates in the first snapshot, plus contracts and a
repeatable quickstart.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Evidence |
|---|---|---|
| Evidence before automation | PASS | Every candidate requires source, observation date, and evidence status. |
| Domain contracts first | PASS | The two catalogs and invocation contract are explicit. |
| Deterministic execution and provenance | PASS | Version, commit/release, query/command, and source fields are required. |
| Quality and human gates are non-bypassable | PASS | Preferred-pilot candidates require QC, provenance, and human-review boundaries. |
| Small, testable, composable skills | PASS | Candidates are evaluated individually and assigned bounded integration tiers. |
| Research safety and evidence | PASS | Discovery is read-only; external data and credential transfer are prohibited. |

## Phase 0: Research Decisions

The agent research results are consolidated in [research.md](research.md).
The key decisions are:

1. Keep broad scientific and bioinformatics catalogs strictly separate.
2. Evaluate individual skills or bounded capabilities, not entire mixed
   repositories.
3. Treat stars and forks as secondary adoption signals, never as quality proof.
4. Prefer a controlled pilot only after invocation, license, safety, and
   maintenance evidence is complete.
5. Keep Spec Kit as the coordination, evidence, gate, and provenance layer;
   let domain tools execute domain computation.

## Phase 1: Design and Contracts

The design artifacts are:

- [data-model.md](data-model.md): candidate, evidence, invocation, score, and
  recommendation entities.
- [contracts/](contracts/): machine-readable field contracts for candidate
  records, Agent invocation, and scoring.
- [quickstart.md](quickstart.md): local review and validation procedure.

## Project Structure

### Documentation

    specs/001-research-skills/
    ├── spec.md
    ├── plan.md
    ├── research.md
    ├── data-model.md
    ├── quickstart.md
    ├── contracts/
    │   ├── candidate-record.yml
    │   ├── invocation-contract.yml
    │   └── scoring-record.yml
    └── checklists/
        └── requirements.md

### Repository Integration Targets

    bio-spec-kit/
    ├── catalogs/                 # reviewed candidate indexes after approval
    ├── presets/                  # domain-facing Spec Kit templates
    ├── extensions/               # bounded invocation and gate adapters
    ├── bundles/                  # optional, audited collections
    ├── workflows/                # lifecycle orchestration
    └── tests/                    # smoke and contract fixtures

**Structure Decision**: Keep this feature's evidence and contracts under its
feature directory first. Promote only reviewed records into catalogs/, and
promote executable candidates into extensions/ or bundles/ only through a later
implementation task with explicit approval.

## Complexity Tracking

No constitution violations. No complexity exception is required.
