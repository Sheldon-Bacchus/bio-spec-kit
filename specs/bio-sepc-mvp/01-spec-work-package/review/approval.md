# 08 Implement approval record

**Feature**：`005-skills-nextflow-research-core`  
**Decision date**：`2026-09-02 Asia/Shanghai`  
**Approver**：`user instruction in current task; personal identity not supplied`  
**Decision**：`APPROVED_WITH_BOUNDED_SCOPE`

The user instructed: “你全部自行决定吧，开始执行，最后还要开子agent审计”。
This is recorded as authorization to resolve C-001–C-005 and implement the
bounded local slice below. It is not authorization to infer permissions outside
the listed paths.

## Resolved clarifications

| ID | Decision |
|---|---|
| C-001 | Freeze the two external Chinese overview files under `inputs/`, preserving original paths, observation date and SHA-256. |
| C-002 | Keep the 13-component denominator fixed at 5 project adapters + 8 reference components; record checkout differences as source gaps. |
| C-003 | Core owns generic lifecycle/contract/identity/provenance/gate/verifier/evaluation skeleton; Bio profile owns biological semantics, S00–S13 and method routes. |
| C-004 | Use `node.contract.json` for public machine contracts; a façade may reference atomic module contracts. |
| C-005 | Use local fixture cases and A0–A3 naming; run only short local smoke/negative checks in this task. |

## Allowed write paths

The following paths are approved for this run:

- `specs/005-skills-nextflow-research-core/**`;
- `spec-mvp/skills/multiqc/SKILL.md`;
- `.agents/skills/multiqc/SKILL.md`;
- `presets/bio-research-mvp/preset.yml`;
- `presets/bio-research-mvp/README.md`;
- `presets/bio-research-mvp/contracts/research-core-profile.yml`.

The two MultiQC Skill files must remain content-identical because the latter is
the runtime discovery projection of the former. The approved Skill edit is a
contract handoff only; it must not add Spec Kit lifecycle steps.

## Evaluation authorization

| Capability | Decision | Constraint |
|---|---|---|
| Local fixture smoke | `approved` | Fresh local output directory; record command, versions and hashes |
| Local negative case | `approved` | Must fail closed and preserve a visible failure verdict |
| Existing local `shared-integration` fixture | `reference-only` | No execution in this slice; reserve for validation protocol |
| BixBench/BioBench/external datasets | `not approved` | No download or upload |
| External APIs, hosted tracing or third-party installation | `not approved` | No network/service permission inferred |
| Long-running benchmark or prompt optimization | `not approved` | Protocol only; no effect score |
| Human scientific/release approval | `not delegated` | Agent may record evidence, not approve a scientific claim |

## Required evidence before closing the slice

- C-001–C-005 appear in `spec.md` and `clarifications.md`;
- the 13-component audit and invariant mapping are present;
- the candidate schema validates the MultiQC contract instance;
- positive and negative local verifiers pass against their intended outcomes;
- source and runtime Skill projections are identical;
- no unapproved target path changed;
- `review/implementation-record.md` records the exact local runs, bounded review,
  and the preserved pre-existing dirty worktree boundary;
- the independent sub-agent audit is recorded after implementation. This is now
  satisfied by the final read-only audit in
  `review/subagent-audit-final-20260902.md`; the earlier initial and conditional
  audit records remain preserved for the remediation trail.

## Bounded-slice closure evidence

The final independent audit returned `PASS` and recommended closing the bounded
local implementation. Positive and negative verifiers were rerun after the
verifier remediation and both returned `0`. This closure does not approve
scientific QC or human release, does not run the deferred evaluation, and does
not alter the separate `scientific_status=not-verified` and
`release_status=pending` states.
