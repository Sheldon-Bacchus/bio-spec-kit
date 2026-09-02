# Fresh-context audit remediation record

**Feature**：`005-skills-nextflow-research-core`  
**Date**：`2026-09-02 Asia/Shanghai`  
**Scope**：Only the paths approved by `review/approval.md` were eligible for
modification. Existing unrelated dirty worktree entries were preserved.  
**Current status**：`COMPLETED_WITH_EXPLICIT_DEFERRED_ITEMS`

This record supersedes neither the historical bounded-slice audit nor its
evidence. It records the second, fresh-context review of reusable-Core
representation and evaluation boundaries. The old `PASS` in
`review/subagent-audit-final-20260902.md` is retained as bounded-slice history;
it is not evidence of unseen-component generalization.

## Finding disposition

| Finding | Disposition | Evidence and remaining boundary |
|---|---|---|
| B-001: façade/module relationship absent from the canonical contract | `REMEDIATED_FOR_CONTRACT_SHAPE` | `node-contract.schema.json` has `module_refs`; the cross-field validator resolves a versioned atomic module, checks component/schema identity, public binding existence, direction/shape/cardinality/channel compatibility and one-to-one façade exposure. A temporary atomic-module/façade fit test is part of `--self-test`. No real unseen façade runtime has been run. |
| B-002: static capability mixed with run status | `REMEDIATED` | `node-contract.schema.json` is static and rejects `status`; `run-status.schema.json` owns the nested `status.execution/scientific/release`, checkout identity and typed run provenance; the MultiQC contract and Skill handoff use this separation. |
| B-003: run evidence pointed outside the current checkout | `REMEDIATED_FOR_FROZEN_RUN` | The frozen positive run's manifests, source map, verdict, review pointers and status envelope use repository-relative POSIX paths; the contract validator resolves them against the current repository and the verifier checks actual file hashes/sizes. The existing wrapper still emits executor-native paths in some generated fields, including stderr metadata; the extension is outside this authorization and remains a portability risk. |
| S-001: missing cross-field port/reference/unique/direction checks | `REMEDIATED_FOR_V0_GATE` | `contracts/validate_contracts.py` checks unique ports/routes/gates/named outputs, exact public input/output exposure, direction, named-output references, identity references and façade bindings; regression self-tests mutate unknown ports, direction, duplicate ports and output references. |
| S-002: descriptive identity strings without join semantics | `REMEDIATED_FOR_V0_VOCABULARY` | Static identity definitions now require namespace, scope, uniqueness scope, requiredness, join cardinality, duplicate/unmatched policy, transport and missing-key behavior; port keys must resolve to required definitions. This is a minimum vocabulary, not proof that every biological join is scientifically valid. |
| S-003: weak/placeholder provenance | `REMEDIATED_FOR_TYPED_ENVELOPE` | Static provenance declares source refs and required run fields without run values; run-status has typed repository, manifest/hash, command, executable/version, parameters, environment, reference-snapshot and verifier links. Placeholder static provenance and missing/incorrect manifest hashes fail validation. |
| S-004: A0-A3 eligibility/repetition/non-determinism underspecified | `REMEDIATED_FOR_PROTOCOL_DESIGN_ONLY` | `evaluation/a0-a3-matrix.yml`, `evaluation/cases/multiqc-mvp/case.yml` and `evaluation/validate_protocol.py` freeze pre-run exclusions, post-run failure accounting, paired intersection, three repetitions, seed-unavailable recording, strict hash agreement and score suppression. No A0-A3 run or effect score is claimed. |

## Deferred items and risks

| Item | Status | Reason |
|---|---|---|
| Architecture review B-003: truly unseen validation | `NOT_RUN / NOT_GENERALIZED` | The current MultiQC case and shared-integration material were known construction/reference material. A holdout-unseen-component slot remains empty. |
| T026/T028 | `DEFERRED / NOT_RUN` | Long-running, external and quantitative benchmark execution was not authorized. |
| T029 / A-007 | `DEFERRED` | The local Windows run exposed GB18030 output and executor-native absolute paths. The wrapper is not an approved write target; cross-platform consumer compatibility needs a separate approval and runtime matrix. |
| Current checkout cleanliness | `RECORDED_RISK` | The status envelope records the full HEAD commit and `working_tree_dirty: true`; relative evidence and hashes are authoritative for this dirty checkout, not a clean-commit reproducibility claim. |
| Scientific/release conclusion | `NOT_VERIFIED / PENDING` | Artifact readiness and deterministic verifier success do not establish QC thresholds, biological validity or human release. |

## Five-axis review

| Axis | Judgment |
|---|---|
| Correctness | Static and run contracts have separate schemas; cross-field and hash checks close the identified v0 representation failures; positive and negative case verifiers remain separate. The judgment is bounded to the frozen local case. |
| Readability | Core ownership, data model, quickstart, protocol and remediation record name the boundary explicitly; the validator emits field-specific failures. Historical audits remain immutable context. |
| Architecture | Capability, run evidence, execution, verifier, protocol and human review are separate interfaces linked by component/version/path/hash. Façade fit is represented but unseen generalization is not inferred. |
| Security | Repository-relative POSIX paths reject absolute paths, traversal and cross-root manifest references; command/executable evidence is checked; no external service, upload or package installation was used. |
| Performance | Hashing streams files in bounded blocks and the HTML parser reads one local report; no long benchmark was introduced. The implementation is adequate for the bounded fixture, not a performance claim for large cohorts. |

## Fresh verification record

Fresh verification was rerun after the remediation in the current checkout.
All required gates returned exit code 0:

| Gate | Fresh result |
|---|---|
| JSON Schema, format checks and Python compilation | `PASS JSON schema/format validation and Python compilation` |
| YAML parse for protocol, case and preset contracts | `PASS YAML parse for protocol, case and preset contracts` |
| Contract validator plus regression self-tests | `PASS node cross-field contract`; `PASS run status and evidence manifests`; `PASS cross-field regression self-tests` |
| A0-A3 protocol validator | `PASS frozen A0-A3 eligibility/repetition protocol` |
| Positive verifier | `{"ok": true, "case": "positive"}` |
| Negative verifier | `{"ok": true, "case": "negative"}` |
| Portable manifest/status/source path scan | `PASS portable manifest/status/source JSON has no absolute paths` |
| Skill projection parity and approved-scope scan | `Skill-byte-parity=True`; `approved-feature-files=64`; no unapproved Feature path was introduced |

The commands used for that fresh run were:

```text
python specs/005-skills-nextflow-research-core/contracts/validate_contracts.py --repo-root . --node specs/005-skills-nextflow-research-core/contracts/multiqc/node.contract.json --run-status specs/005-skills-nextflow-research-core/evaluation/runs/multiqc-mvp-20260902/research-core-status.json --self-test
python specs/005-skills-nextflow-research-core/evaluation/validate_protocol.py
python specs/005-skills-nextflow-research-core/evaluation/cases/multiqc-mvp/verifier/verify_case.py --output specs/005-skills-nextflow-research-core/evaluation/runs/multiqc-mvp-20260902 --case positive
python specs/005-skills-nextflow-research-core/evaluation/cases/multiqc-mvp/verifier/verify_case.py --output specs/005-skills-nextflow-research-core/evaluation/runs/multiqc-mvp-negative-20260902 --case negative
```
