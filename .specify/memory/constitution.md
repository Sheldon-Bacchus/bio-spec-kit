<!--
Sync Impact Report
- Version change: scaffold -> 1.0.0
- Modified principles: placeholder principles replaced with five project principles.
- Added sections: Research Safety & Evidence; Workflow & Release Gates.
- Removed sections: none; the scaffold sections were populated rather than removed.
- Follow-up TODOs: none.
-->

# bio-spec-kit Constitution

## Core Principles

### I. Evidence Before Automation

Every research capability MUST preserve the source, version, query or command,
retrieval time, and evidence needed to reproduce its conclusion. An Agent MAY
summarize or propose work, but it MUST NOT present an unverified claim, citation,
or generated result as established evidence.

### II. Domain Contracts First

Every preset, extension, and workflow MUST define its intended domain, accepted
inputs, required metadata, outputs, failure behavior, and ownership boundary.
Generic Agent behavior MUST NOT silently replace domain-specific scientific
methods, reference resources, or statistical assumptions.

### III. Deterministic Execution and Provenance

Execution MUST be reproducible from a recorded specification, parameters,
tool versions, reference data versions, environment identifiers, and input and
output manifests. Network calls, external databases, containers, and mutable
repositories MUST be pinned or recorded with enough detail to reconstruct the
run.

### IV. Quality and Human Gates Are Non-Bypassable

Input integrity, domain QC, statistical design, interpretation, and release
approval MUST be explicit gates. An Agent MUST stop, report the failing gate,
and request an authorized decision; it MUST NOT weaken thresholds, skip review,
or overwrite an approval record to complete a workflow.

### V. Small, Testable, Composable Skills

Each skill or extension MUST have a narrow responsibility, documented invocation
contract, safe defaults, and deterministic smoke or contract tests. External
skills MUST be imported by an auditable allowlist with license, dependency,
network, and permission review rather than copied wholesale into the project.

## Research Safety & Evidence

Human genomic, clinical, unpublished, or otherwise sensitive data MUST be
classified before an external Agent, MCP server, API, or hosted service is
used. Default integrations MUST be read-only and limited to public data.
Credentials, protected data, and private notes MUST NOT be sent to an external
service without explicit authorization and an appropriate data-processing
review. Research recommendations MUST distinguish evidence, inference, and
uncertainty.

## Workflow & Release Gates

Changes MUST follow the Spec Kit sequence of specification, planning, task
generation, implementation, and verification. A release candidate MUST include
the relevant QC report, statistical or methodological review, provenance
manifest, approval record, and license/dependency inventory. A failed check
MUST remain visible in the run record; waivers require an identified approver,
timestamp, reason, scope, and expiry or re-review condition.

## Governance

This constitution supersedes local conventions that conflict with it. Any
amendment MUST state the affected principles, rationale, migration impact, and
version change. Changes require a reviewed commit and MUST update dependent
templates, presets, extensions, or checklists when their contracts are affected.
Every feature review MUST verify evidence, domain contracts, reproducibility,
gate behavior, and external dependency permissions. Complexity beyond the
current user need requires explicit justification in the feature plan.

**Version**: 1.0.0 | **Ratified**: 2026-08-26 | **Last Amended**: 2026-08-26
