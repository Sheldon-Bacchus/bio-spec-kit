# Run MultiQC

Use this command only after the upstream analysis step has completed.

The wrapper:

1. Accepts one bounded input result directory.
2. Uses the project-owned MultiQC configuration.
3. Runs MultiQC without shell interpolation.
4. Writes an HTML report, parsed data, input/artifact manifests, a JSON verdict,
   stdout/stderr logs, and a Markdown review report.
5. In the `fastqc-multiqc-mvp` preset, verifies fixture-derived sample values,
   the source map, and the MultiQC log rather than checking HTML existence only.
6. Stops on an execution or content-verification failure so the workflow cannot
   silently release.

Default invocation:

    python .specify/extensions/bio-multiqc/scripts/run_multiqc.py
      --input .bio/runs/current/pipeline
      --output .bio/runs/current/multiqc
      --config .specify/extensions/bio-multiqc/config/multiqc_config.yaml
      --mode required

For the clean vertical slice, use a fresh output directory and the explicit
fixture preset:

    python extensions/bio-multiqc/scripts/run_multiqc.py
      --input tests/fixtures/multiqc
      --output .bio/runs/current/multiqc-mvp
      --config extensions/bio-multiqc/config/multiqc_config.yaml
      --multiqc-bin .venv/Scripts/multiqc.exe
      --preset fastqc-multiqc-mvp

MultiQC 1.35 emits `multiqc_report_data/` for the default report filename. The
wrapper records that actual path in the verdict and does not assume the older
`multiqc_data/` directory name.

The mode skip is allowed only for local smoke tests and produces a visible
skipped verdict. It is not a release-ready QC result.
