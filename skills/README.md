# Bio Skills capability plane

`skills/` is the auditable source tree for project Bio Skills. Bio Skills are
the capability plane: they own the scientific method, domain decisions,
failure modes, tool routing, and result interpretation. They are not Spec Kit
templates and are not bundled into the `bio-spec-mvp` Preset.

Long upstream material is kept under each Skill's `references/` and is read
only for the selected decision. The runnable Codex discovery copies live under
`.agents/skills/` because the Codex integration discovers
`.agents/skills/<name>/SKILL.md`, not arbitrary package directories.

The five initial adapters are:

| Skill | Main role | Runtime binding | Current status |
|---|---|---|---|
| `bulk-pa-luad` | tool use + result interpretation | `Rscript`, edgeR, limma | adapter staged; runtime needs pinned R environment |
| `cross-branch-integration` | capability routing + interpretation | `Rscript` and table/matrix libraries | adapter staged; no joint model in MVP |
| `pathway-enrichment` | tool use + interpretation | `Rscript`, clusterProfiler, OrgDb/GO.db | adapter staged; GO/KEGG runtime pending |
| `wgcna-module-constraint` | tool use + interpretation | `Rscript`, WGCNA | adapter staged; stability gate pending |
| `multiqc` | tool use + result interpretation | project wrapper + MultiQC 1.35 | executable path available in `.venv` |

These are project adapters, not a wholesale import of `vendor/sources/`. Their
source paths and boundaries are recorded in `skill-catalog.yml`.

The control-to-capability handoff is intentionally small. A plan names a
`skill_id` and records the capability's inputs, outputs, constraints,
acceptance, and evidence. It does not copy the Skill's method instructions
into the Preset.

## Upstream reference stack for the first transcriptomics pass

The review-only copies for the planned analysis chain are under
`skills/reference-stack/`. Read them in this order:

```text
01-mds → 02-deg → 02-deg-results → 03-de-visualization/03-volcano
       → 04-pathway-workflow → 05-kegg
```

This directory is deliberately outside `.agents/skills/`: it is not runtime
discovery and does not silently add external skills to the project's allowlist.
The mapping, source paths, and boundaries are documented in its `README.md`.

For Chinese review, a parallel non-runtime mirror is available at
`skills/reference-stack-zh-CN/`. It contains Chinese summaries and
decision points while preserving links to the complete English originals. It
is a translation/review backup, not an additional discovered Skill.
