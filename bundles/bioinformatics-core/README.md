# Bioinformatics Core Bundle

This bundle installs the first reusable Bio Spec Kit stack:

- `bioinformatics` preset
- `bio-intake` extension
- `bio-qc` extension
- `bio-pipeline` extension
- `bio-provenance` extension
- `bio-review` extension
- `bulk-rnaseq` workflow

The bundle is intended for local development and clean-project installation
tests first. It does not include Nextflow, Snakemake, R, aligners, or reference
data. Those remain project- or organization-managed dependencies.

## Install from a local artifact

```powershell
specify bundle install .\bioinformatics-core-0.1.0.zip
```

## Verification expectations

After installation, run the `bulk-rnaseq` workflow with `engine=skip` against a
small fixture before enabling a production pipeline engine.

