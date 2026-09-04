---
name: wgcna-module-constraint
description: Build and audit bulk WGCNA modules, module-trait relationships, hub-gene constraints, and downstream module handoffs. Use when an expression matrix needs co-expression modules or when a downstream analysis must be constrained to stable modules. Do not use for directed regulation claims, raw single-cell dropout data, or tiny cohorts.
metadata:
  role: tool-usage-and-result-interpretation
  primary_tool: Rscript
  source: vendor/sources/bioSkills/gene-regulatory-networks/coexpression-networks
---

# WGCNA module constraint

Read [the upstream co-expression skill](references/upstream-coexpression-networks.md)
for the method rationale and [the usage guide](references/wgcna-usage.md) or
[example](references/wgcna_analysis.R) only when implementing a selected mode.

## Contract

- Input: normalized expression matrix with samples as rows/genes as columns,
  sample traits, subject/batch metadata, gene namespace, and the feature's
  module constraint policy.
- Output: sample/gene QC, signed-network and soft-power record, module labels,
  eigengenes, module-trait correlations with p-values, kME-based hub table,
  preservation evidence when claimed, and constrained downstream gene sets.
- Executable: pinned `Rscript` with `WGCNA` and its dependencies. The Agent
  chooses parameters only within the approved preset and records them.

## Workflow

1. Confirm the design and sample count before network construction. Keep batch
   and subject metadata visible; do not silently residualize biology.
2. Use a signed network consistently for power selection and construction,
   inspect `goodSamplesGenes`, and record block size and outlier handling.
3. Relate eigengenes to traits; define hubs by signed kME, not raw expression or
   an unqualified causal label.
4. A module becomes a constraint only after the approved stability rule is met
   (for example, independent preservation or a declared resampling check).
5. Hand module genes plus their provenance to pathway enrichment; do not rerun
   or rewrite the upstream matrix in the handoff.

## Fail closed

Stop or mark reference-only when fewer than the preset minimum samples are
available, the design is singular, the network type differs across steps, the
grey module is treated as biological evidence, batch dominates modules, or
preservation/stability is claimed without an executed diagnostic. WGCNA edges
are marginal co-expression, not direct regulation.
