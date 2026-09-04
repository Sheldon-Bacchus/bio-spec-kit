# BioSpec MVP architecture

BioSpec MVP fixes one boundary: **Spec Kit is the control plane; Bio Skills are
the capability plane.** The preset shapes what a research feature must state;
it does not teach or execute the scientific method.

```text
Spec Kit / Preset → control plane: artifact contracts, command guidance,
                    acceptance and evidence requirements
Bio Skills        → capability plane: scientific method and domain decisions
Script / Tool      → execution plane: deterministic machine operations
Extension         → optional bridge: deterministic control capability
Feature           → specs/<feature>/spec.md, plan.md, tasks.md, contracts/
Run               → caller-owned state and evidence outside this source package
```

## Preset boundary

`preset.yml` contains only Spec Kit-supported item types and paths that exist
within this package. A research contract is not a preset item type. It is
authored for a concrete feature under `specs/<feature>/contracts/` and is
checked by feature tests or a later deterministic bridge when one is actually
needed.

The five template overrides retain the official headings needed by Spec Kit
and add only the minimum research fields. A template is an artifact contract:
it defines what must be delivered, not how DESeq2, edgeR, WGCNA, GSEA, or
another method works. The `speckit.specify` command is additive, so the
upstream command remains the base behavior.

## Capability-binding boundary

`plan-template.md` is the handoff point from control to capability. Each
planned analysis step may declare:

```yaml
required_capabilities:
  - capability:
    skill_id:
    inputs: []
    outputs: []
    assumptions: []
    parameters: {}
    constraints: []
    acceptance: []
    evidence: []
```

`skill_id` identifies the Bio Skill that owns the method. The template may
leave it unresolved as a clarification item; it must not replace the Skill
with a method handbook. The actual method choice, failure modes, tool routing,
and result interpretation belong under `skills/`.

## Deferred surfaces

Workflow orchestration, timelines, autonomous workers, model routing, and a
complete Extension system are deliberately outside this MVP. Human review is
recorded as a requirement in the generated artifacts and checklist. A future
Workflow may consume those artifacts, but it is not part of this Preset's
manifest or package boundary.

## Runtime boundary

Generated state, logs, reports, and experiment outputs are not source files.
They must be written by a caller to its own run location. The repository's
local `run-working/` directory is an ignored working/archive area and is never
part of this preset package or its publication archive.
