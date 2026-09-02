# Spec MVP

This directory is the first project-level skill package and execution proof.
It intentionally keeps three layers separate:

```text
Spec Core              specs/002-multiqc-vertical-slice/
Agent Skills Core      spec-mvp/skills/ and .agents/skills/
Execution Core         extensions/bio-multiqc/ + .venv/MultiQC 1.35
```

The five staged skills are `bulk-pa-luad`, `cross-branch-integration`,
`pathway-enrichment`, `wgcna-module-constraint`, and `multiqc`. The first four
are audited adapters with pinned boundaries and references. `multiqc` is the
first executable vertical slice.

For the detailed separation of Skill tests, scientific-method tests, full-result
E1/E2/E3 validation, and the proposed research MVP, see
[`docs/evaluation-matrix.md`](docs/evaluation-matrix.md).

## Official-first boundary

The callable Spec Kit MVP now lives at the repository root:

- `presets/bio-research-mvp/` contains the official-template-compatible preset.
- `workflows/bio-research-mvp/workflow.yml` contains the official workflow
  definition using `command`, `shell`, and `gate` steps.

The YAML in `spec-mvp/workflows/multiqc-vertical-slice.yml` is retained as a
design note for the original layer model. It is not installed as a Spec Kit
workflow because its custom step types are not part of the official engine.

Run the real slice from the repository root:

```powershell
.venv\Scripts\python.exe -m unittest discover -s spec-mvp\tests -p "test_*.py" -v
```

Run a user-openable report into a fresh directory:

```powershell
.venv\Scripts\python.exe extensions\bio-multiqc\scripts\run_multiqc.py `
  --input tests\fixtures\multiqc `
  --output spec-mvp\artifacts\multiqc-mvp `
  --config extensions\bio-multiqc\config\multiqc_config.yaml `
  --multiqc-bin .venv\Scripts\multiqc.exe `
  --preset fastqc-multiqc-mvp
```

Open [the generated report](artifacts/multiqc-mvp/multiqc_report.html) after
the command completes. The output directory is intentionally a local run
artifact and should be regenerated from the fixture rather than hand-edited.
