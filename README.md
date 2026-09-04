# Bio Spec Kit

Reusable GitHub Spec Kit components for evidence-first bioinformatics work.

The MVP boundary and package decisions are maintained in
[`prest-spec-mvp/`](prest-spec-mvp/) and [`skills/`](skills/). Read those
boundaries before adding a new Preset, Bio Skill, Extension, or research
Feature.

This repository is intentionally a composition layer around Spec Kit:

- `prest-spec-mvp` is the narrow Spec Kit control-plane Preset.
- `skills/*` is the Bio Skill capability plane and owns scientific methods.
- `presets/bioinformatics` is a broader Preset, separate from the MVP.
- `extensions/*` are deferred deterministic bridges and reusable commands.
- `workflows/*` are broader execution surfaces, separate from the MVP.
- `bundles/*` package a tested stack for one-command installation.

The actual scientific computation remains in Nextflow, Snakemake, or another
versioned pipeline engine. Spec Kit coordinates intent, evidence, review, and
reproducibility; it is not a replacement for a workflow engine.

## Control-plane MVP

The first publishable slice is the `prest-spec-mvp` Preset. It defines the
minimum Spec Kit artifacts needed to state a research question, plan, task
list, capability binding, acceptance boundary, and evidence requirement. It
does not run a pipeline or select a Bio Skill automatically.

## Local development

From a clean Spec Kit project:

```powershell
specify init --here --integration codex --force
specify preset add --dev .\prest-spec-mvp
specify preset info bio-spec-mvp
specify preset resolve spec-template
specify preset resolve plan-template
```

The package can be installed as a local bundle after validation:

```powershell
specify bundle validate --path .\bundles\bioinformatics-core
specify bundle build --path .\bundles\bioinformatics-core --output .\dist
specify bundle install .\dist\bioinformatics-core-0.1.0.zip
```

## BioSpec MVP control plane

The narrowest research package is [`prest-spec-mvp/`](prest-spec-mvp/). It is a
standalone Spec Kit Preset with the same publication shape as a community
Preset: `preset.yml`, `commands/`, `docs/`, `scripts/`, `templates/`, and
`tests/`. It contains no generated results, worker runtime, dataset, Workflow,
or scientific analysis implementation.

The boundary is intentionally explicit:

```text
Spec Kit / Preset  → WHAT, WHY, contract, acceptance, evidence, skill binding
Bio Skills         → HOW: method, tool choice, failure modes, interpretation
Script / Tool      → deterministic execution
```

Workflow orchestration, autonomous workers, model routing, and the complete
Extension system are deferred. The broader SkillsBench material and local
execution experiments remain in the ignored `run-working/` boundary and are
not part of the GitHub Preset package.

## Minimal artifact contract

The MVP's primary artifacts are the standard Spec Kit documents:

- `constitution.md` — durable project principles;
- `spec.md` — question, scope, requirements, and claim boundary;
- `plan.md` — research design and required capability bindings;
- `tasks.md` — concrete work units derived from the plan;
- `checklist.md` — reviewer-owned acceptance checks.

The `plan.md` capability binding records `capability`, `skill_id`, `inputs`,
`outputs`, `constraints`, `acceptance`, and `evidence`. It names the Bio Skill
needed for the work; it does not contain the Skill's method handbook. Runtime
reports, logs, run ledgers, and result directories belong to a later execution
surface, not to this Preset.

## Design rules

1. Spec Kit owns WHAT, WHY, contract, acceptance, evidence, and skill binding.
2. Bio Skills own HOW: scientific methods, tools, failure modes, and
   interpretation.
3. A Template is an artifact contract, not a method handbook.
4. `skill_id`, inputs, outputs, constraints, acceptance, and evidence are
   explicit before a capability is selected or executed.
5. Deterministic control belongs in an Extension only when Markdown guidance
   cannot reliably enforce the rule.
6. Workflow orchestration and worker execution are outside the MVP boundary.

## Status

This is the first local MVP. It provides a reusable control-plane package and
an explicit handoff to Bio Skills; assay-specific methods, thresholds, and
production execution should be added to the capability/execution planes only
after the corresponding Skill contract is reviewed.
