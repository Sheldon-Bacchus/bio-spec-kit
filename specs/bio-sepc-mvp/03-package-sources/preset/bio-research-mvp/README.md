# Bio Research Spec Kit MVP preset

This is a project-local Spec Kit preset. It keeps the official Spec Kit
artifact lifecycle and adds only the research fields needed for the first
vertical slice:

- scientific question, hypothesis, estimand, scope, and claim boundary;
- study/data design and explicit validation;
- reproducibility and human-review gates;
- task-level validation commands and evidence paths;
- a separate Research Core/Bio profile ownership contract for composable Skills.

It does not replace the Spec Kit command engine, add a new state-machine
runtime, or turn the five research design documents into mandatory runtime
contracts. Those concerns remain separate contract/control-plane artifacts; this
preset does not put Spec Kit stages into a Skill or claim that a runtime is
scientifically validated.

The preset manifest also exposes a direct machine-readable binding from the
MultiQC component and Skill path to
`specs/005-skills-nextflow-research-core/contracts/multiqc/node.contract.json`;
the profile contract remains the source for ownership and boundary semantics.
The binding is a bounded local evidence slice: unseen-component validation and
the A0-A3 effect score remain not run, so it is not a reusable-Core or
scientific-validity claim.

Install it during local development with:

```powershell
specify preset add --dev .\presets\bio-research-mvp
specify preset resolve spec-template
```
