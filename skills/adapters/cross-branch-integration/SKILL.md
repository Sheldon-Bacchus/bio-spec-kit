---
name: cross-branch-integration
description: Integrate results across omics or analysis branches by validating sample correspondence, harmonizing identifiers and scales, computing gene intersections, and stratifying concordant versus discordant directions. Use when branches share subjects or biological questions and their outputs must be compared or combined. Do not use as a substitute for per-omic normalization or a causal claim.
metadata:
  role: workflow-control-and-result-interpretation
  primary_tool: Rscript
  source: vendor/sources/bioSkills/multi-omics-integration
---

# Cross-branch integration

Read the upstream references only for the selected mode:

- [integration design](references/upstream-integration-design.md) for paired,
  mosaic, horizontal, and diagonal correspondence.
- [data harmonization](references/upstream-data-harmonization.md) for per-view
  transforms, scaling, missingness, and batch handling.
- [usage guides and diagnostic](references/integration-usage.md) for concrete
  design checks.

## Contract

- Input: branch result tables or matrices, a sample map with stable subject IDs,
  feature-ID namespace and reference release, branch labels, effect direction
  convention, and the feature spec's integration question.
- Output: sample-map audit, matched/unmatched records, gene intersection table,
  direction strata (`up/up`, `down/down`, `up/down`, `down/up`), per-branch
  provenance, and a limitation report. An integrated score is optional and
  requires an explicit validation plan.
- Executable: a deterministic `Rscript` or small adapter using the chosen
  matrix/table libraries. MOFA2, mixOmics, and SNF remain separate runtime
  components and are not silently invoked by this skill.

## Workflow

1. Classify the question as shared genes, direction concordance, subtype,
   shared latent axis, or predictive signature before selecting a method.
2. Validate the subject/sample map and preserve missing or unmatched cases;
   never use row order as correspondence.
3. Normalize feature IDs using the same reference namespace, deduplicate with a
   recorded rule, and keep branch-specific evidence columns.
4. Compute intersections and direction strata from executed result tables.
   Define direction from the signed effect or statistic and record the cutoff.
5. If a joint model is requested, verify scale balance, batch identifiability,
   missing-view handling, and an out-of-sample validation target before fitting.

## Fail closed

Stop when subject correspondence is inferred rather than provided, IDs mix
assemblies/namespaces, a branch has no comparable effect field, direction
conventions disagree, batch is perfectly confounded with biology, or a claimed
integrated signature has no held-out validation. A gene intersection is a
descriptive result, not evidence that the branches share a causal mechanism.
