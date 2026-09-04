---
name: pathway-enrichment
description: Run reproducible GO and KEGG enrichment from executed differential or module results, choosing ORA versus ranked GSEA, mapping IDs consistently, using the tested-gene universe, and separating up/down direction. Use for pathway analysis, GO/KEGG ORA, background selection, or enrichment interpretation. Do not use to invent a gene list or treat enrichment as validation of the same DE result.
metadata:
  role: tool-usage-and-result-interpretation
  primary_tool: Rscript
  source: vendor/sources/bioSkills/pathway-analysis and vendor/sources/scientific-agent-skills/skills/pathway-enrichment
---

# Pathway enrichment

Use the relevant reference instead of loading all pathway material:

- [upstream general enrichment](references/upstream-scientific-agent-pathway-enrichment.md)
  for ORA/GSEA method selection and result semantics.
- [GO source](references/upstream-go-enrichment.md) for universe, ontology,
  ID mapping, redundancy, and GOseq.
- [KEGG source](references/upstream-kegg-pathways.md) for organism/keyType,
  live-database pinning, and topology boundaries.
- [DE-to-pathway source](references/upstream-expression-to-pathways.md) for the
  handoff from a signed DE table.

## Contract

- Input: executed result table or module gene list, tested-gene universe for
  ORA, organism and ID namespace, direction (if applicable), database release
  or access date, method, and thresholds.
- Output: ID mapping audit, mapped foreground/universe counts, GO/KEGG result
  table with raw and adjusted p-values, fold enrichment, overlap genes,
  direction labels, database provenance, and optional figures.
- Executable: pinned `Rscript` with `clusterProfiler` and the relevant local
  OrgDb/GO.db; KEGG network access is an explicit exception and must be pinned
  or replaced by a local snapshot.

## Workflow

1. Choose ORA for a thresholded list and GSEA for a complete ranked list; do
   not threshold then call it GSEA.
2. Map foreground and universe through the same ID path, deduplicate, and
   report mapping loss. Pass the measured/tested universe explicitly to ORA.
3. Set GO ontology explicitly, split up/down when direction matters, and
   report fold enrichment with BH-adjusted p-values and overlap size.
4. For KEGG, use the correct organism/keyType and record the live release or
   frozen snapshot. Interpret terms as hypotheses, not proof.

## Fail closed

Stop when the universe is missing for ORA, the foreground and universe use
different ID namespaces, mapping loss is unexplained, no ranked score exists
for requested GSEA, or a KEGG result has no access date/release record. Do not
edit result files to make a term pass a cutoff.
