VERDICT: REVISE — The bounded MultiQC slice is coherent, but the reusable design is not ready for further implementation because static/run state semantics, façade composition, and genuinely unseen validation remain unresolved.

| # | Dimension | Score and justification |
|---|---|---|
| 1 | Requirement and quality-attribute fidelity | 🟡 Requirements and boundaries are unusually explicit, but the design’s generalization claim is ahead of its validation protocol. |
| 2 | Boundary quality (cohesion/coupling) | 🟡 Ownership is clear in prose, but façade-to-module references and port referential integrity are not represented mechanically. |
| 3 | Pattern restraint (forces-based) | 🟡 Most patterns have stated forces, but the generalized Core/adapter machinery is not yet fit-tested outside the construction set. |
| 4 | Data and state modeling | 🔴 The canonical node contract mixes static component declaration with run-specific status and lacks semantic state invariants. |
| 5 | Change tolerance / YAGNI | 🟡 Stable names and explicit gaps help, but façade composition, evaluation adapters, and status machinery are broader than the demonstrated seam. |
| 6 | Failure and scale realism | 🟡 Fail-closed behavior is well stated for local cases, while retry, idempotency, concurrency, partial publication, and resume semantics are unspecified. |
| 7 | Decision capture and legibility | 🟢 Decisions, rejected scope, evidence classes, approval boundaries, and deferred work are extensively recorded. |

## Blockers

### B-001 — Static component contracts carry run-specific state

- **Dimension:** 4 — Data and state modeling.
- **Anchor:** `specs/005-skills-nextflow-research-core/contracts/node-contract.schema.json:4-5,8-23,156-173` defines a public component contract that requires `execution`, `scientific`, and `release` status; `specs/005-skills-nextflow-research-core/contracts/multiqc/node.contract.json:193-197` hard-codes `execution: passed`; the separate run envelope already has `run_id` and the same statuses at `specs/005-skills-nextflow-research-core/contracts/run-status.schema.json:8-17,26-47`.
- **Why it matters:** A public node contract should describe a reusable capability and interface, while `execution: passed` is a property of one run. Requiring both in the same canonical object makes the contract stale or misleading after another run, and it does not define whether status is component capability, current-run state, or historical evidence.
- **Suggested direction:** Separate static contract metadata from run-status records. Keep the node contract linked to a run-status or capability-evidence reference, and make `run_id`, artifact identity, and status transitions properties of the run envelope.

### B-002 — The approved façade-to-atomic-module relationship is not representable

- **Dimension:** 2 — Boundary quality.
- **Anchor:** The approved decision says a public façade may reference multiple atomic module contracts in `specs/005-skills-nextflow-research-core/spec.md:49-53` and `specs/005-skills-nextflow-research-core/clarifications.md:66-71`; the data model anticipates `parent_component_id` at `specs/005-skills-nextflow-research-core/data-model.md:41-46`; however, the complete candidate schema property set at `specs/005-skills-nextflow-research-core/contracts/node-contract.schema.json:25-195` contains no module-reference, parent-component, or façade-composition field.
- **Why it matters:** `kind: facade` exists, but the canonical machine contract cannot declare which atomic modules it owns, exposes, versions, or composes. The decision is therefore prose-only and cannot be validated or used safely by a router.
- **Suggested direction:** Add an explicit, versioned module-reference relation with defined public exposure semantics, or narrow C-004 so façade composition remains a named future seam until a concrete façade is fit-tested.

### B-003 — The planned validation case is not genuinely unseen

- **Dimension:** 1 — Requirement and quality-attribute fidelity.
- **Anchor:** `cross-branch-integration` is already one of the fixed 13 construction components in `specs/005-skills-nextflow-research-core/data-model.md:186-206` and has a full audit record at `specs/005-skills-nextflow-research-core/contracts/skill-audit-record.yml:67-93`; the evaluation protocol nevertheless assigns `shared-integration-reference` to that component at `specs/005-skills-nextflow-research-core/evaluation-protocol.md:30-43`, while requiring validation to use a component not used to define the schema at `specs/005-skills-nextflow-research-core/evaluation-protocol.md:107-115`; the research ledger records that no such independent validation case exists at `specs/005-skills-nextflow-research-core/research.md:82-85,100-111`.
- **Why it matters:** The Core is explicitly described as a hypothesis that must fit an un参与构造的 Skill or workflow. Reusing a known roster component cannot test whether the abstraction generalizes, and the current record confirms that the independent verifier has not run.
- **Suggested direction:** Reserve a truly unmodeled component or workflow, freeze its oracle and verifier before inspecting its contract, and make that validation a gate before adding further components or treating the Core as reusable.

## Should-fix

### S-001 — Schema validation does not enforce cross-field contract integrity

- **Dimension:** 2 — Boundary quality.
- **Anchor:** The requirement claims mechanical composition checks over ports, shape, cardinality, identity, and route at `specs/005-skills-nextflow-research-core/spec.md:149-151,327-329`; in the schema, `public_interface.takes/emits` are unconstrained strings at `specs/005-skills-nextflow-research-core/contracts/node-contract.schema.json:68-84`, while `ports` and `named_outputs.port_id` are independently defined at `specs/005-skills-nextflow-research-core/contracts/node-contract.schema.json:85-112,197-255`.
- **Why it matters:** The schema accepts a `takes` name that is not an input port, a named output that points to a nonexistent or input port, duplicate port IDs, and an interface whose direction disagrees with the referenced port. Shape validation alone cannot establish composition validity.
- **Suggested direction:** Add a dedicated contract linter with cross-reference, uniqueness, direction, and route compatibility checks, and state clearly whether that linter—not JSON Schema alone—is the canonical composition gate.

### S-002 — Provenance fields are structurally present but semantically weak

- **Dimension:** 4 — Data and state modeling.
- **Anchor:** The constitution requires identity, versions, reference data, and hashes at `specs/005-skills-nextflow-research-core/constitution.md:50-58,89-94`; the candidate schema only requires loosely typed source references, input hashes, parameters, and environment at `specs/005-skills-nextflow-research-core/contracts/node-contract.schema.json:131-154`; the representative contract uses a placeholder string for hashes and defers the executable version to another artifact at `specs/005-skills-nextflow-research-core/contracts/multiqc/node.contract.json:173-190`.
- **Why it matters:** `input_hashes` accepts arbitrary strings and may be empty; output hashes, command, exact executable version, reference/database release, and explicit linkage to the run manifest are not required. A contract can therefore validate while failing the provenance invariant it is meant to express.
- **Suggested direction:** Distinguish contract-time source declarations from run-time provenance. Require a structured run-manifest reference and define required fields for input/output hashes, command, executable versions, parameters, environment, and reference snapshots; preserve unknown values explicitly.

### S-003 — Retry, idempotency, and partial-publication semantics are unspecified

- **Dimension:** 6 — Failure and scale realism.
- **Anchor:** The design requires cache/resume identity and fail-closed behavior at `specs/005-skills-nextflow-research-core/constitution.md:60-80`, but the failure/recovery section only lists coarse stop-and-return loops at `specs/005-skills-nextflow-research-core/plan.md:275-283`; the MultiQC contract’s operational policy is limited to “fresh directory unless explicit overwrite” at `specs/005-skills-nextflow-research-core/contracts/multiqc/node.contract.json:181-190`.
- **Why it matters:** The design does not say what happens when a process is retried after partial output, two runs target the same output, a verifier sees stale artifacts, or resume reuses a semantically incompatible result. “Fresh directory” reduces one risk but does not define idempotency, atomic publication, locking, or recovery.
- **Suggested direction:** Declare the supported v0 execution envelope explicitly—e.g. single local run, fresh immutable output directory, no concurrent writers—or add run identity, atomic publish, retry classification, stale-output detection, and resume invalidation rules.

### S-004 — The data model and machine schema disagree on port direction

- **Dimension:** 4 — Data and state modeling.
- **Anchor:** `specs/005-skills-nextflow-research-core/data-model.md:81-97` defines port direction as `upstream/input/output/downstream`, while `specs/005-skills-nextflow-research-core/contracts/node-contract.schema.json:197-215` permits only `input` and `output`.
- **Why it matters:** The conceptual model contains topology-facing directions that disappear in the machine contract without a documented normalization rule. Different consumers may interpret “upstream/downstream” as port direction, graph relation, or omit it entirely.
- **Suggested direction:** State that upstream/downstream are graph relations rather than port directions, or align the machine model and add one explicit conversion rule tested against a public and atomic contract.

## Nit

### N-001 — External technical evidence is date-stamped but not immutably captured

- **Dimension:** 7 — Decision capture and legibility.
- **Anchor:** `specs/005-skills-nextflow-research-core/research.md:17-19,74-76,89-103` records Nextflow/nf-core URLs and access date but explicitly leaves the nf-core website version and external revisions unknown.
- **Why it matters:** A future re-review may observe changed documentation at the same URL, making it difficult to distinguish source evolution from a changed interpretation of the invariant.
- **Suggested direction:** Capture immutable section snapshots or commit/version identifiers where available; otherwise retain the affected invariant as proposal/guideline evidence rather than normative frozen evidence.

### N-002 — Audit-state vocabulary and runtime-state vocabulary lack an explicit mapping

- **Dimension:** 4 — Data and state modeling.
- **Anchor:** Human audit fields use `有/条件/无/待核/不适用/未验证` at `specs/005-skills-nextflow-research-core/data-model.md:14-22` and `specs/005-skills-nextflow-research-core/contracts/skill-audit-record.yml:3-17`, while runtime contract states use separate English enums at `specs/005-skills-nextflow-research-core/contracts/node-contract.schema.json:156-173`.
- **Why it matters:** The separation is defensible, but without a declared mapping or explicit namespace distinction, automated summaries may treat `未验证`, `not-verified`, and `reference-only` as interchangeable despite their different meanings.
- **Suggested direction:** Add a small vocabulary mapping or explicitly mark the domains as non-convertible, with conversion allowed only through a verifier or review decision.

Final summary: REVISE before further implementation; the bounded local implementation remains useful evidence, but the reusable Core needs a clean static/run contract split, executable façade and port relations, and a real unseen validation gate. No files were modified.
