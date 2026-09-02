# Bounded implementation record

**Feature**：`005-skills-nextflow-research-core`  
**Execution date**：`2026-09-02 Asia/Shanghai`  
**Authorization**：`review/approval.md` → `APPROVED_WITH_BOUNDED_SCOPE`

## Implemented paths

The Agent wrote only within the approved Feature tree, the two MultiQC Skill
projections, and the three approved Bio preset files:

- Feature documentation, contracts, mappings, cases, verifiers, runs and review
  records under `specs/005-skills-nextflow-research-core/`;
- `spec-mvp/skills/multiqc/SKILL.md`;
- `.agents/skills/multiqc/SKILL.md`;
- `presets/bio-research-mvp/preset.yml`;
- `presets/bio-research-mvp/README.md`;
- `presets/bio-research-mvp/contracts/research-core-profile.yml`.

No other Skill, workflow, bundle, extension or external data source was modified
or invoked; no hosted service or third-party package was installed. Existing
local Python validation dependencies were used only for schema/protocol checks.
Existing unrelated dirty worktree changes were preserved.

## Local execution evidence

### Positive case

- Run directory: `evaluation/runs/multiqc-mvp-20260902/`
- Input: `evaluation/cases/multiqc-mvp/inputs/`
- Wrapper: `extensions/bio-multiqc/scripts/run_multiqc.py` (read-only use)
- Runtime: Python `3.12.10`, MultiQC `1.35`
- Wrapper return code: `0`
- Wrapper verdict: `status=completed`, `ok=true`, `release_ready=true` (artifact-ready only)
- Research Core machine status: `research-core-status.json` with exact
  `execution/scientific/release` values
- Deterministic verifier: passed
- Input and artifact manifests: present with SHA-256 records
- Research Core review record: `research-core-review.md`

### Negative case

- Run directory: `evaluation/runs/multiqc-mvp-negative-20260902/`
- Input: intentionally nonexistent directory
- Wrapper return code: `2`
- Verdict: `status=failed`, `ok=false`, `release_ready=false`
- Failure message explicitly states that the MultiQC input directory does not exist
- Deterministic negative verifier: passed

## Postconditions

- `spec-mvp/skills/multiqc/SKILL.md` and `.agents/skills/multiqc/SKILL.md` are
  byte-identical; SHA-256 is
  `C4616CC9DC9118508BD93619A516FA1FC4A18EBDFEEAA773A856BA60E734DC91`.
- The MultiQC contract validates against `contracts/node-contract.schema.json`.
- The contract keeps `execution=passed`, `scientific=not-verified` and
  `release=pending` independent.
- T026/T028 remain `DEFERRED/NOT_RUN`; no benchmark score is claimed.
- A local portability observation is retained: this Windows MultiQC run emitted
  `multiqc_data.json` as GB18030; the wrapper compatibility reader and verifier
  parsed it successfully, but a cross-platform UTF-8 consumer still needs a
  separately approved compatibility decision.

## Independent audit and verifier remediation

- The initial independent audit is preserved in
  `review/subagent-audit-initial-20260902.md`.
- A second read-only audit (Ampere,
  `01a0609a-f91d-7180-842d-d60a051e1354`) identified a MEDIUM risk that several
  verifier checks relied on text substring markers. That audit is preserved in
  `review/subagent-audit-second-20260902.md`.
- Within the approved verifier path, those checks were replaced with semantic
  HTML parsing, fixture-derived JSON equality, anchored log-record matching,
  exact review status/boundary checks and exact negative error equality. The
  positive and negative verifiers were rerun successfully.
- The final independent read-only audit (Curie,
  `01a060a2-7f94-79a1-bbbb-128d4a23c651`) returned `PASS` and recommended
  closing the bounded local implementation. Its materialized record is
  `review/subagent-audit-final-20260902.md`.

## Fresh-context reusable-Core remediation

The subsequent fresh-context audit found that the historical PASS covered only
the bounded local slice. Within the same approved Feature boundary, the
remediation added:

- static node capability versus per-run status separation;
- versioned facade/module references and a cross-field contract validator;
- typed repository-relative input/artifact manifests and checkout identity;
- explicit identity join vocabulary and typed run provenance;
- pre-run eligibility, failure accounting, three-repetition and determinism
  rules with a machine-checked A0-A3 protocol gate;
- current positive/negative verifier checks for path, manifest, hash and status
  exactness.

The complete disposition and five-axis review are in
review/remediation-20260902.md. The current evidence remains bounded:
architecture-review B-003 unseen validation is NOT_RUN/NOT_GENERALIZED,
T026/T028/T029 remain deferred, and scientific/release status remains
not-verified/pending. No A0-A3 score or human scientific approval is claimed.
