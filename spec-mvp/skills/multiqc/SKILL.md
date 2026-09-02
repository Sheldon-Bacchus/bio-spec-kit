---
name: multiqc
description: Aggregate bounded bioinformatics QC outputs with the project MultiQC wrapper, producing a real HTML report and machine-readable data that are checked against the input fixture. Use when a Spec feature requires a user-openable QC report or a QC evidence artifact. Do not treat MultiQC itself as a pass/fail gate or fabricate a report/verdict.
metadata:
  role: tool-usage-and-workflow-control
  primary_tool: multiqc
  source: vendor/sources/bioSkills/reporting/automated-qc-reports and vendor/sources/MultiQC
---

# MultiQC project skill

Read [the upstream QC guidance](references/upstream-automated-qc-reports.md)
when deciding module scope, sample-name handling, or gate boundaries. The
project executable is the bounded wrapper at
`extensions/bio-multiqc/scripts/run_multiqc.py`; it calls the host's real
MultiQC CLI.

## Contract

- Input: an existing directory of upstream tool logs/metrics, an expected
  sample/tool manifest, a pinned config, and an output directory outside the
  input tree.
- Output: `multiqc_report.html`, `multiqc_data/` including JSON and source
  mapping, a wrapper verdict, a review note, command/version metadata, and
  output hashes. The HTML is the user-facing artifact; JSON is for checks.
- Default command from the repository root:

  `python extensions/bio-multiqc/scripts/run_multiqc.py --input <input> --output <output> --config extensions/bio-multiqc/config/multiqc_config.yaml --multiqc-bin .venv/Scripts/multiqc.exe`

## Research Core contract handoff

For the approved `005-skills-nextflow-research-core` representative slice, the
candidate machine contract is recorded at
`specs/005-skills-nextflow-research-core/contracts/multiqc/node.contract.json`.
It is a feature-level contract artifact, not a replacement for this Skill's
prose and not an instruction to run a Spec Kit lifecycle. The static node
contract declares capability and interface; the per-run
`research-core-status.json` run-status envelope records `execution`,
`scientific`, and `release` separately. A successful artifact check leaves
scientific verification and human release as independent decisions.

## Workflow

1. Read the feature's `spec.md` and identify the expected sample/tool evidence;
   do not infer a roster from whatever MultiQC happens to find.
2. Run the wrapper with the pinned config and capture stdout, stderr, command,
   executable path, and MultiQC version.
3. Verify exit status, HTML existence, machine-readable data, source mapping,
   expected sample/tool markers, and a content marker that is unique to the
   fixture. Review the HTML directly after those checks.
4. Keep report generation separate from any threshold gate or human approval.
   A polished report is not proof that upstream QC passed.

## Fail closed

Stop when the executable/input/config is missing, MultiQC finds no intended
module, the expected sample/tool is absent, machine-readable output is
missing, the report does not contain fixture-derived evidence, or AI/network
summary mode is enabled for sensitive data. `--mode skip` is lifecycle wiring
only and is never release-ready.
