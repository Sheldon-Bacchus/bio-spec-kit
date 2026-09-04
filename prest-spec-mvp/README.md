# BioSpec MVP

BioSpec MVP is the smallest publishable Spec Kit preset for an evidence-aware
research specification control plane. It is a preset source package, not a
research run, a pipeline engine, a Bio Skill collection, or a worker runtime.

The package has one job: make the official Spec Kit lifecycle ask for the
scientific question, estimand, scope, evidence boundary, validation criteria,
and explicit assumptions before implementation is planned.

## Package boundary

```text
.
├── preset.yml                 # Spec Kit preset manifest
├── commands/                  # Additive command guidance
├── docs/                      # Package documentation
├── scripts/                   # Package self-validation only
├── templates/                 # Official template overrides
└── tests/                     # Deterministic package tests
```

This package deliberately does not contain:

- generated reports, run outputs, logs, caches, or fixture results;
- `run-working/`, worker processes, autonomous orchestration, or model routing;
- a `workflow.yml`, a Workflow package, or a second nested preset;
- a scientific dataset, a fixed assay, or a claim about biological validity;
- the former Evidence Closure Kernel and MultiQC execution experiments.

Those materials remain outside this source package in the local ignored
`run-working/_archive/spec-mvp-pre-refactor-20260904/` area for traceability.
They are not part of the GitHub publication boundary.

## What the preset provides

The manifest uses only the official preset item types (`template` and
`command`). BioSpec MVP provides the five standard core templates and one
additive `speckit.specify` command. It does not register a custom `contract`
item: feature contracts belong to `specs/<feature>/contracts/` and are
consumed by the selected Bio Skill or, later, a deterministic extension.

The templates are artifact contracts, not method handbooks. The plan template
provides a small capability-binding slot for `capability`, `skill_id`,
`inputs`, `outputs`, `assumptions`, `parameters`, `constraints`, `acceptance`,
and `evidence`. The scientific method and tool choice remain in the referenced
Bio Skill.

## Install locally

From an initialized Spec Kit project:

```powershell
specify preset add --dev .\prest-spec-mvp
specify preset info bio-spec-mvp
specify preset resolve spec-template
```

Workflow is deliberately deferred from this MVP. No Workflow is installed or
required to use this package; human review obligations are represented in the
generated artifacts, acceptance fields, and checklist. Broader execution
workflows remain separate repository surfaces and are not part of this control
plane package.

## Validate the package

The package test suite performs structural checks without network access or
model execution:

```powershell
python .\scripts\validate_package.py --package .
python -m unittest discover -s .\tests -p "test_*.py" -v
```

The acceptance boundary is intentionally small: a clean package, a valid
official manifest, existing referenced files, official template anchors, and
no runtime directories. A passing package test is not evidence that a
scientific method or a downstream analysis is valid.

## Upstream references

- [Spec Kit preset reference](https://github.com/github/spec-kit/blob/main/docs/reference/presets.md)
- [Spec Kit preset scaffold](https://github.com/github/spec-kit/blob/main/presets/scaffold/preset.yml)
