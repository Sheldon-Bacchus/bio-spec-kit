# Merge and composition decisions

**Feature**：`005-skills-nextflow-research-core`  
**Status**：`FROZEN_FOR_IMPLEMENTATION_SCOPE`  
**Decision date**：`2026-09-02 Asia/Shanghai`

“合并”在本文件中只表示阅读入口或数据编排关系。它不删除源文件、不改变
estimand、不转移算法所有权，也不把一个报告生成器变成科学验证器。

## Decision table

| Objects | Decision | Evidence basis | Preserved boundary | Next task |
|---|---|---|---|---|
| `bulk-pa-luad` ↔ `02-deg` | `merge-view` | Both describe differential-expression analysis, but one is a project adapter and one is a reference stack | edgeR/limma adapter behavior and reference prose remain separate; pairing and count-model constraints remain owned by the adapter | T023 |
| `bulk-pa-luad` ↔ `02-deg-results` | `compose-only` | Result curation consumes executed DE output rather than re-estimating it | tested universe, NA semantics and result identity remain downstream responsibilities | T013, T023 |
| `multiqc` ↔ `bulk-pa-luad` | `compose-only` | QC artifacts can be upstream evidence for analysis, but their observables and estimands differ | report generation never becomes DE approval; QC threshold/release remain separate gates | T024 |
| `multiqc` ↔ `01-mds` | `compose-only` | QC evidence may precede exploratory visualization; no shared scientific observable | sample/tool identity and projection interpretation remain separate | T013 |
| `cross-branch-integration` ↔ `bulk-pa-luad` | `compose-only` | Integration consumes branch results and compares them by stable IDs | no automatic joint model or causal interpretation | T013, T023 |
| `cross-branch-integration` ↔ `02-deg-results` | `compose-only` | Both operate on result-level artifacts, but integration owns correspondence and direction strata | unmatched records and branch-specific evidence are preserved | T013 |
| `pathway-enrichment` ↔ `04-pathway-workflow` | `compose-only` | Adapter and reference workflow share ORA/GSEA routing concepts but have different ownership | route selection, tested universe and database semantics are not collapsed into one implementation | T013, T025 |
| `pathway-enrichment` ↔ `04-pathway-enricher` | `compose-only` | Generic project adapter and Enrichr-specific adapter can hand off a declared gene-set request | external API, library release and privacy boundary remain Enrichr-specific | T013 |
| `04-pathway-workflow` ↔ `05-kegg` | `compose-only` | Workflow orchestrates database methods; KEGG owns KEGG IDs, topology and release semantics | KEGG live/frozen database behavior remains a separate method boundary | T013 |
| `pathway-enrichment` ↔ `05-kegg` | `keep-separate` | Generic GO/KEGG routing and KEGG topology have different database/estimand constraints | KEGG organism/keyType, snapshot and SPIA rules remain independent | T013 |
| `wgcna-module-constraint` ↔ `pathway-enrichment` | `compose-only` | A stable module gene set may be handed to enrichment | co-expression is not causal regulation; stability gate remains WGCNA-owned | T013 |
| `03-de-visualization` ↔ `03-volcano` | `compose-only` | Volcano/MA is a specialized visualization route | effect/shrinkage and threshold semantics remain explicit; no plot is an inference engine | T013 |
| `02-deg-results` ↔ `03-de-visualization` | `compose-only` | Visualization consumes result artifacts | result filtering and statistical identity remain upstream | T013 |

## Missing or pending capabilities

| Capability | Decision | Why it is not silently added | Follow-up |
|---|---|---|---|
| Shared machine-readable component contract | `missing` → candidate added under `contracts/` | Existing `SKILL.md` prose does not define stable ports, cardinality and status fields | T007, T008, T024 |
| Unseen-case scientific verifier | `missing` | A local wrapper smoke test cannot establish general scientific validity | T017-T019, T026 |
| Canonical S00–S13 assignment for every component | `pending` | Current mapping is an auditable proposal, not a user-approved biological lifecycle | T013, T014 |
| External Enrichr/KEGG reproducibility snapshot | `missing` | Network/API data and release permissions are not authorized in this run | future separately approved task |

## Non-actions

- No source Skill is deleted, moved, renamed, or merged.
- The external consolidated documents are frozen as audit inputs only; they are not
  rewritten and not treated as runtime instructions.
- No Spec Kit stage is written into a Skill, workflow, or preset runtime path.
