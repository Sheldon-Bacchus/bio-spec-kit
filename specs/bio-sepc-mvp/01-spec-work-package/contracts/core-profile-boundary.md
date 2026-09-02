# Research Core / Bio profile boundary

**Feature**：`005-skills-nextflow-research-core`  
**Decision**：C-003 resolved on `2026-09-02 Asia/Shanghai`  
**Status**：`APPROVED DESIGN / NOT A RUNTIME IMPLEMENTATION`

The Core is a reusable contract and control-plane proposal. The Bio profile is
the domain layer that supplies biological vocabulary, stage semantics and method
routes. A concrete Skill or execution adapter owns algorithm bodies and tool
details. A verifier checks declared observables; a human reviewer owns claim and
release decisions.

## Ownership table

| Layer | Owns | Does not own | Evidence boundary |
|---|---|---|---|
| Research Core | Static component capability contract, public ports, shape/cardinality, queue/value semantics, stable identity vocabulary, façade/module references, run-provenance envelope, gate/verifier interfaces and evaluation protocol skeleton | Biology-specific estimands, organism rules, statistical defaults, tool implementation, execution/scientific/release decisions | Core fields are structural proposals until a component contract and verifier are run; run status belongs to the run envelope |
| Bio profile/preset | Organism and namespace vocabulary, Bio S00–S13 mapping, estimand terms, method families, tested-universe rules, route vocabulary such as ORA/GSEA or edgeR/limma | Spec Kit lifecycle definition, generic port mechanics, executor implementation, human approval | Profile expresses domain constraints; it does not prove that a method ran correctly |
| Skill/component | Narrow trigger, scientific purpose, method interpretation, preconditions, hard boundary, allowed route and domain-specific handoff | Cross-component lifecycle ownership, silent upstream rewriting, human release approval | `SKILL.md` is a human/Agent entry point, not the complete machine contract |
| Execution | R/Python/CLI/Nextflow process body, environment binding, deterministic computation and emitted artifacts | Research question, estimand choice, scientific verdict or human release | Exit code and files are execution evidence only |
| Verifier | Schema, field, hash, identity, content and negative-case checks; deterministic verdict | Scientific interpretation beyond its oracle, human claim approval, changing inputs to pass | A passing verifier is limited to its frozen oracle and observable set |
| Human review | Interpretation of estimand, unsupported claims, QC/statistical/methodological release and approval record | Rewriting raw results or replacing deterministic checks | Approval must remain a separate control-plane record |
| Evaluation adapter | Trace, matrix, version and assertion transport; local case orchestration | Scientific oracle, deterministic verifier, human review or result interpretation | Langfuse/Promptfoo are optional adapters, never the oracle |

## Contract separation

1. `SKILL.md` explains when to read a component, what it means and when to stop.
2. `node.contract.json` declares static machine-checkable ports, identity, routes,
   gates, named outputs, façade/module bindings and the run provenance fields that
   callers must provide. It never stores a current execution, scientific or
   release status.
3. `run-status.schema.json` records one run's repository identity, typed manifests,
   command/environment, verifier link and independent execution/scientific/release
   statuses. It binds to the static node contract by component and version.
4. Execution code produces artifacts and manifests without mutating the Skill
   prose or approval records.
5. Verifier output is a bounded machine verdict; a human review record decides
   whether a result may be released.

These representations link through `component_id`, contract version, source refs,
input/output identity and provenance. The `node.contract.json` and
`run-status.schema.json` are deliberately not one combined file: a reusable
capability cannot become stale merely because one run passed.

## C-003 consequence

The evaluation protocol skeleton is a Core concern because it defines how cases,
variants, oracle/verifier interfaces and trace records are compared. Individual
biological cases, domain oracles and scientific rubrics remain Bio profile or
human-review concerns. This boundary is still a design hypothesis and must be
fit-tested on an unseen component before it is generalized.
