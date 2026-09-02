# Run shared branch integration

This command consumes two already executed, frozen DEG result tables. It does
not rerun differential expression and it does not infer a joint model.

```powershell
python extensions\bio-integration\scripts\run_shared_integration.py `
  --pa tests\fixtures\shared-integration\pa_deg.tsv `
  --luad tests\fixtures\shared-integration\luad_deg.tsv `
  --output spec-mvp\artifacts\shared-integration-mvp `
  --duplicate-policy error
```

For the real PA/LUAD archived tables, pass `--duplicate-policy max-abs-effect`
because the PA table contains two duplicated gene symbols that were already
known during the source analysis. The policy is recorded in provenance; it is
never inferred silently.
