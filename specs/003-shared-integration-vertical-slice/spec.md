# Feature Specification: Frozen DEG shared-integration vertical slice

**Feature Branch**: `003-shared-integration-vertical-slice`  
**Status**: MVP implementation complete for the deterministic shared slice  
**Scope**: table-level integration only

## User Story 1: Recompute the shared result

As a researcher, I want to run one bounded command on two frozen DEG result
tables, so that the shared genes and four direction strata are produced from
the declared inputs rather than copied from a previous report.

### Acceptance scenarios

1. **Given** two UTF-8 TSV files containing `gene_symbol`, `logFC`, `DEG`, and
   `direction`, **when** the wrapper runs, **then** it writes `shared_all.tsv`,
   `shared_UpUp.tsv`, `shared_DownDown.tsv`, `shared_UpDown.tsv`,
   `shared_DownUp.tsv`, `shared_membership.tsv`, and `intersection_summary.tsv`.
2. **Given** the checked-in fixture, **when** the wrapper runs, **then** the
   shared result is `GENE_A`, `GENE_B`, `GENE_C`, `GENE_D`, with one gene in
   each direction stratum.
3. **Given** the result, **when** a reviewer reads the manifest and claim,
   **then** the input hashes, column contract, duplicate policy, output hashes,
   and descriptive-only claim boundary are present.

## User Story 2: Prevent silent scientific guessing

As a maintainer, I want invalid or ambiguous frozen tables to fail closed, so
that the MVP never invents an ID mapping, direction, or duplicate resolution.

### Acceptance scenarios

1. **Given** a duplicate selected gene and the default `error` policy, **when**
   the wrapper runs, **then** it returns non-zero and writes a terminal failed
   verdict.
2. **Given** a direction that disagrees with the sign of `logFC`, **when** the
   wrapper runs, **then** it returns non-zero with `direction_effect_conflict`.
3. **Given** the same rows in a different order, **when** the wrapper runs,
   **then** canonical result tables have the same content and hashes.
4. **Given** one input file is changed, **when** the wrapper runs, **then** the
   run ID and relevant output hashes change.

## Functional requirements

- **FR-001**: The wrapper MUST consume already selected DEG tables; it MUST
  not rerun edgeR, limma, WGCNA, GO, or KEGG.
- **FR-002**: The wrapper MUST require declared gene, effect, status, and
  direction columns unless the corresponding optional column is explicitly
  disabled.
- **FR-003**: Selected rows MUST have finite, non-zero effects and directions
  consistent with the effect sign.
- **FR-004**: Gene normalization and duplicate handling MUST be explicit and
  recorded in provenance.
- **FR-005**: The four direction tables MUST be mutually exclusive and their
  union MUST equal the direct intersection.
- **FR-006**: The wrapper MUST emit input/output hashes, run manifest,
  machine-readable verdict, and a descriptive-only claim.
- **FR-007**: The MVP MUST NOT describe overlap as common mechanism, causality,
  independent validation, or clinical efficacy.
- **FR-008**: A failed validation MUST NOT be release-ready.

## Out of scope

Raw-count DEG execution, QC-to-DEG gating, live KEGG, WGCNA, joint multi-omics
models, independent cohort validation, experimental validation, and automatic
release approval.
