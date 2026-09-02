---
name: bulk-pa-luad
description: Run or design bulk expression differential analysis for the PA-LUAD feature using edgeR for count-model inference and limma for paired continuous-data checks. Use when a feature specifies paired subjects, edgeR contrasts, limma paired/blocking terms, or DE result handoff. Do not use for single-cell per-cell testing, unpaired defaults, or workflow-engine execution.
metadata:
  display_name: "Bulk paired RNA-seq: edgeR QL + limma"
  scope: "paired bulk RNA-seq differential expression"
  role: tool-usage-and-result-interpretation
  primary_tool: Rscript
  source: vendor/sources/bioSkills/differential-expression/edger-basics
---

# Bulk PA-LUAD

This is a project adapter, not a replacement for the upstream edgeR and metadata
skills. Read the relevant reference only when its decision is needed:

- [edgeR source](references/upstream-edger-basics.md) for count-model mechanics.
- [metadata and paired-design source](references/upstream-metadata-joins.md) for
  sample joins and `~ subject + condition` design logic.
- [usage guide](references/edger-usage.md) and examples for concrete R patterns.

## Contract

- Input: raw integer count matrix, sample metadata, an explicit subject/pairing
  column, condition levels, contrast, organism/reference namespace, and a
  feature spec that defines the estimand.
- Output: filtered-count manifest, design/contrast record, edgeR result table,
  paired limma result when requested, diagnostics, software versions, and input
  and output hashes.
- Executable: `Rscript` calling pinned `edgeR` and `limma`. The Agent may write
  an R script, but the host executes it and the result files are evidence.

## Required decisions

1. Validate that each subject has the required condition levels exactly once, or
   explicitly document a repeated-measures design.
2. For counts use `filterByExpr` before normalization/dispersion, explicit
   `normLibSizes(method=...)`, robust dispersion estimation, and the modern
   edgeR QL test. Do not feed TPM/CPM/VST into the count model.
3. Encode pairing in the design (`~ subject + condition` or an equivalent
   no-intercept contrast). Never replace pairing with an unpaired test because
   it is shorter.
4. Treat `limma2` in the request as an unresolved label. Until the feature
   contract names a real package/function, interpret it as `limma` paired/block
   modeling and record that assumption in the run manifest.
5. Export signed statistics and the tested-gene universe for downstream
   enrichment. A post-hoc edit of a result table is not an acceptable result.

## Fail closed

Stop with a machine-readable error when the count matrix is non-integer,
metadata joins are incomplete, pairing is ambiguous, the design is singular,
required R packages are missing, or a result lacks the expected tested-gene
universe and tool version. A no-hit result is valid only when the executed
model and diagnostics are present; it must not be converted into a fabricated
positive list.
