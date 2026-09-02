# MultiQC MVP run record

## Command

Run from `E:\all-agent-workspace\codex-projects\bio-skills\bio-spec-kit`:

```powershell
.venv\Scripts\python.exe extensions\bio-multiqc\scripts\run_multiqc.py `
  --input tests\fixtures\multiqc `
  --output spec-mvp\artifacts\multiqc-mvp `
  --config extensions\bio-multiqc\config\multiqc_config.yaml `
  --multiqc-bin .venv\Scripts\multiqc.exe `
  --preset fastqc-multiqc-mvp
```

## Input and runtime

- Input: `tests/fixtures/multiqc/sample_fastqc/fastqc_data.txt`
- Fixture values: sample `test_R1`, 10000 total sequences, length 100, GC 48
- Python: `.venv/Scripts/python.exe`, 3.12.10
- MultiQC: `.venv/Scripts/multiqc.exe`, 1.35
- Wrapper: `bio-multiqc`, version 0.1.0
- External network: not required

## Successful output

The run exited `0` and wrote `release_ready=true` only after content checks passed:

- `multiqc_report.html`
- `multiqc_report_data/multiqc_data.json`
- `multiqc_report_data/multiqc_sources.json`
- `multiqc_report_data/multiqc.log`
- `multiqc-verdict.json`
- `input-manifest.json`
- `artifact-manifest.json`
- `wrapper-stdout.log` and `wrapper-stderr.log`

The machine-readable data contains `FastQC → test_R1 →
total_sequences=10000, avg_sequence_length=100, percent_gc=48`; the log contains
`Found 1 reports` and the HTML contains the FastQC/sample/value markers.

## Failure information

The first verifier attempt failed because MultiQC 1.35 wrote a localized
`report_creation_date` in the Windows system encoding. The wrapper initially
assumed UTF-8 and raised `UnicodeDecodeError`; the failure was fixed by compatible
UTF-8/GB18030/CP1252 reading while preserving the raw generated files. The final
test suite also exercises a missing executable and confirms non-zero exit,
`ok=false`, and `release_ready=false`.
