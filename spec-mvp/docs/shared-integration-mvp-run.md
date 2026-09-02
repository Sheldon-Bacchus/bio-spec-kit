# Shared integration MVP run record

## Purpose

This run is the first real execution of the `003-shared-integration-vertical-
slice` Feature. It does not rerun PA or LUAD differential expression. It
consumes the already produced DEG artifacts, makes the duplicate policy
explicit, recomputes the deterministic intersection, and compares it with the
archived shared-149 reference output.

## Command

Run from `E:\all-agent-workspace\codex-projects\bio-skills\bio-spec-kit`:

```powershell
$research = "E:\all-agent-workspace\codex-projects\research-top\PROJECT-PA-LUAD-EVIDENCE-TO-EXPERIMENT-V1"

.venv\Scripts\python.exe extensions\bio-integration\scripts\run_shared_integration.py `
  --pa "$research\03_completed_modules\M03_PA_DE\output\PA_DE__V2__DEG.tsv" `
  --luad "$research\03_completed_modules\M03_LUAD_DE_GSE75037\output\LUAD_GSE75037_DE__V2__DEG.tsv" `
  --output spec-mvp\artifacts\shared-integration-real `
  --duplicate-policy max-abs-effect
```

The PA table has two known duplicated gene symbols (`ICOSLG` and `SERPINA3`).
`max-abs-effect` is therefore supplied explicitly and is recorded in the
output provenance. The default policy is `error` for unknown duplicates.

## Observed result

```text
shared = 149
UpUp = 50
DownDown = 17
UpDown = 73
DownUp = 9
partition_sum = true
membership_union = true
claim_status = descriptive_only
release_ready = false
```

The generated five gene-ID sets were compared with the archived
`M07_shared_149_direction` outputs. All five sets matched exactly:

| Output | MVP | Archived reference | Gene-ID set |
|---|---:|---:|---|
| all_shared | 149 | 149 | equal |
| UpUp | 50 | 50 | equal |
| DownDown | 17 | 17 | equal |
| UpDown | 73 | 73 | equal |
| DownUp | 9 | 9 | equal |

## What this run proves

- The new wrapper can consume the existing PA/LUAD DEG artifacts directly.
- The explicit duplicate policy is sufficient to reproduce the shared-149
  gene sets.
- The four direction strata are deterministic and partition the intersection.
- The result is emitted with manifests, hashes, a machine-readable verdict,
  and a bounded descriptive claim.

## What this run does not do

- It does not validate the upstream PA/LUAD DEG statistical models.
- It does not run WGCNA, GO, KEGG, or an independent cohort.
- It does not claim a shared mechanism or causality.
- It does not set `release_ready=true`.
