# Feature Specification: Verified MultiQC vertical slice

**Feature Branch**: `002-multiqc-vertical-slice`
**Created**: 2026-08-26
**Status**: MVP implemented locally

## User Story 1: Open a real QC report (Priority: P1)

As a researcher, I want to run one clean command on a fixed QC fixture and open
the resulting report, so that I can verify the Spec → Skill → executable →
artifact chain without trusting a generated Markdown claim.

### Acceptance Scenarios

1. **Given** a clean output directory and `tests/fixtures/multiqc` containing a
   FastQC log, **when** the MultiQC project skill's wrapper is run with the
   `fastqc-multiqc-mvp` preset, **then** the real MultiQC CLI exits zero and the
   output contains a non-empty `multiqc_report.html`, a
   `multiqc_report_data/multiqc_data.json`, a source map, a MultiQC log, a JSON
   verdict, and an input manifest.
2. **Given** the same run, **when** a reviewer reads the machine-readable data,
   **then** it contains sample `test_R1` with `total_sequences=10000`,
   `avg_sequence_length=100`, and `percent_gc=48`, and the log confirms one
   FastQC report was parsed.
3. **Given** the generated HTML path, **when** a user opens it in a browser,
   **then** the report visibly contains the FastQC section and fixture-derived
   sample/metric content.

## User Story 2: Prevent a static-result shortcut (Priority: P1)

As a maintainer, I want the verification to fail or change when the input
fixture changes, so that a pre-written YAML/HTML/JSON file cannot masquerade as
an execution result.

### Acceptance Scenarios

1. **Given** two clean temporary input directories differing only in
   `Total Sequences`, **when** the wrapper is executed independently, **then**
   the parsed MultiQC value and input manifest hash differ accordingly.
2. **Given** a missing executable, config, input directory, machine-readable
   artifact, or expected FastQC content, **when** the wrapper runs, **then** it
   returns non-zero, writes a failed verdict, and sets `release_ready=false`.

## Functional Requirements

- **FR-001**: The feature MUST keep Spec artifacts, skill instructions, and
  deterministic execution code in separate directories and responsibilities.
- **FR-002**: The project MUST expose a loadable `multiqc` skill under
  `.agents/skills/multiqc/SKILL.md` and stage its auditable source under
  `spec-mvp/skills/multiqc/`.
- **FR-003**: The wrapper MUST call the host-provided MultiQC executable using a
  structured argument list and capture stdout, stderr, exit code, and version.
- **FR-004**: The wrapper MUST produce both user-facing HTML and machine-readable
  artifacts; HTML existence alone MUST NOT be sufficient for success.
- **FR-005**: The MVP MUST verify the expected FastQC sample and values from the
  fixture through MultiQC's parsed JSON and source/log evidence.
- **FR-006**: The run MUST preserve input and output hashes and a failed state;
  `--mode skip` MUST never be release-ready.
- **FR-007**: The project MUST not require MCP, Nextflow, dynamic skill routing,
  or a full RNA-seq runtime to execute this feature.

## Key Entities

- **Spec artifact**: this `spec.md`, its `plan.md`, and `tasks.md`.
- **Project skill**: the `multiqc` Agent Skill and its selected references.
- **Execution artifact**: HTML, parsed JSON, source map, log, manifests, and
  wrapper verdict emitted by the real run.

## Out of Scope

Nextflow/workflow-engine execution, multi-agent orchestration, MCP, automatic
skill routing, biological interpretation, and making MultiQC itself a QC gate.
