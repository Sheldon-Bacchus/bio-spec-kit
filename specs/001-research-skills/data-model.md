# Data Model: Skill Research Catalog

## CandidateSkill

Represents one externally sourced skill, Agent package, service, or bounded
bioinformatics capability.

| Field | Required | Rules |
|---|---|---|
| id | yes | Stable lowercase identifier; do not use a mutable display name |
| name | yes | Human-readable upstream name |
| domain | yes | Exactly scientific-general or bioinformatics |
| source_url | yes | Canonical repository, documentation, paper, or API URL |
| scope | yes | Capabilities included and explicitly excluded |
| invocation_class | yes | skill-file, cli, mcp, api, notebook, pipeline-wrapper, or knowledge-reference |
| status | yes | candidate, reviewed, superseded, or excluded |
| observation_date | yes | ISO date for volatile evidence |

## EvidenceRecord

Records why a candidate is considered credible or why evidence is incomplete.

| Field | Required | Rules |
|---|---|---|
| version_or_commit | no | Release, tag, commit, paper version, or unverified |
| stars | no | Numeric only when observed from a reliable source; otherwise unverified |
| forks | no | Numeric only when observed from a reliable source; otherwise unverified |
| maintenance_signal | yes | recent, intermittent, stale, or unknown with explanation |
| license | yes | SPDX-like identifier, mixed, missing, or needs-review |
| documentation_signal | yes | mature, usable, partial, or weak |
| test_signal | yes | contract-tests, CI, examples-only, absent, or unknown |
| sources | yes | One or more URLs supporting the record |
| confidence | yes | high, medium, or low |
| evidence_notes | yes | Short, auditable explanation; no unsupported claims |

## InvocationContract

Describes how an Agent may call the capability without guessing.

| Field | Required | Rules |
|---|---|---|
| entrypoint | yes | Skill path, command, MCP tool, API operation, or reference action |
| input_schema | yes | Files, identifiers, metadata, and required reference resources |
| output_schema | yes | Expected files, records, reports, or assertions |
| side_effects | yes | none, local-files, network-read, network-write, external-write, or execution |
| permissions | yes | Minimum filesystem, network, credential, and write permissions |
| failure_policy | yes | stop, report-and-review, retry-bounded, or reference-only |
| provenance_outputs | yes | Versions, commands, parameters, logs, hashes, and source metadata |
| human_gate | yes | Gate name and approval requirement before release or external write |

## ScoreRecord

Stores the reproducible weighted assessment.

| Field | Required | Rules |
|---|---|---|
| invocation_score | yes | 0-5 |
| utility_score | yes | 0-5 |
| maintenance_adoption_score | yes | 0-5 |
| docs_tests_score | yes | 0-5 |
| license_score | yes | 0-5; unresolved license cannot score above 2 |
| safety_score | yes | 0-5; undisclosed sensitive-data transfer is a critical failure |
| speckit_fit_score | yes | 0-5 |
| total_score | yes | Weighted result on 0-5 scale |
| confidence | yes | high, medium, or low |
| critical_failures | yes | Empty list when none |
| reviewer | yes | Agent or human reviewer identifier |
| scored_date | yes | ISO date |

## IntegrationRecommendation

Maps a candidate to a bounded next action.

| Tier | Meaning |
|---|---|
| preferred-pilot | Evidence is sufficient for a controlled public-data pilot; not yet a default core dependency |
| wrapper-needed | Useful capability, but the project must add schemas, permissions, gates, or provenance |
| reference-only | Use documentation, methods, or prompt structure; do not execute as a dependency |
| exclude | Scope, safety, license, evidence, or maintenance failure blocks reuse |

Required fields:

- target_type: preset, extension, bundle, adapter, checklist, or none
- target_name
- required_gates
- evidence_gaps
- approval_state: proposed, approved-for-pilot, or rejected

## Relationships and Lifecycle

CandidateSkill 1-to-many EvidenceRecord
CandidateSkill 1-to-1 InvocationContract
CandidateSkill 1-to-1 ScoreRecord
CandidateSkill 1-to-1 IntegrationRecommendation

Lifecycle:

candidate → evidence-collected → scored → reviewed → approved-for-pilot or
reference-only/excluded → superseded

No candidate may move to approved-for-pilot without a complete invocation
contract, no critical safety or license failure, and an identified human review
gate.
