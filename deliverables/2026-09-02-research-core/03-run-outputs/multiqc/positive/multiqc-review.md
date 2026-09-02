# MultiQC review report

- Decision: COMPLETED
- Input: specs/005-skills-nextflow-research-core/evaluation/cases/multiqc-mvp/inputs
- Output: specs/005-skills-nextflow-research-core/evaluation/runs/multiqc-mvp-20260902
- Command: ['.venv/Scripts/multiqc.exe', 'specs/005-skills-nextflow-research-core/evaluation/cases/multiqc-mvp/inputs', '--outdir', 'specs/005-skills-nextflow-research-core/evaluation/runs/multiqc-mvp-20260902', '--filename', 'multiqc_report.html', '--config', 'extensions/bio-multiqc/config/multiqc_config.yaml', '--force']

## Review notes

- Confirm that the expected tools and samples are present.
- Confirm that thresholds and outliers are scientifically acceptable.
- Confirm the JSON verdict and provenance are recorded before release.
