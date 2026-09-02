# Independent sub-agent audit — initial pass

**Feature**：`005-skills-nextflow-research-core`  
**Audit date**：`2026-09-02 Asia/Shanghai`  
**Agent**：`Confucius` (`01a06091-890a-7742-9025-1b657a4d259a`)  
**Mode**：read-only; no file creation, modification, deletion, reset, network,
dependency installation or long-running evaluation.

This record preserves the first independent audit before remediation. The
sub-agent report was returned through the agent channel; the findings below are
transcribed with their severity and disposition so the approval gate has a
durable audit trail.

## Initial findings and disposition

| ID | Initial severity | Finding | Disposition |
|---|---|---|---|
| A-001 | HIGH | Positive verifier checked review boundary as text markers and did not parse a structured status envelope. | Remediated: verifier now parses `research-core-status.json` and requires exact execution/scientific/release values. |
| A-002 | HIGH | Wrapper `multiqc-verdict.json` did not itself contain scientific/release fields. | Remediated within approved Feature scope: added `research-core-status.json` plus `contracts/run-status.schema.json`; wrapper verdict remains preserved as execution evidence. |
| A-003 | MEDIUM | HTML and review checks used permissive substring matching. | Remediated: parsed MultiQC JSON fields are compared numerically; status values are checked structurally; only human-boundary prose remains a separate explicit note. |
| A-004 | MEDIUM | Initial report said the top task summary omitted T029. | Current-tree recheck after the report shows the top summary is `T001-T025,T027 COMPLETE; T026,T028,T029 DEFERRED`; treated as a stale observation, not an outstanding defect. |
| A-005 | HIGH | Approval required a materialized independent audit record, which did not yet exist. | Remediated by this file and the final audit record to be written after the second audit. |
| A-006 | MEDIUM | Preset exposed the component contract only indirectly through the profile contract. | Remediated: `preset.yml` now has a direct machine-readable `component_contract_bindings` entry; profile remains the ownership source. |

## Independent confirmations

The initial sub-agent also confirmed, without treating them as scientific proof:

- 13 audit records and 13 mapping rows agree with the 5+8 denominator;
- `hard_boundary` is required and present in all 13 records;
- the MultiQC contract fits the Draft 2020-12 node schema;
- positive and negative run directories exist with the intended wrapper states;
- the two approved MultiQC Skill projections are byte-identical and do not
  contain a Spec Kit nine-step runtime workflow;
- validation, holdout, scientific QC, human release and benchmark scores were
  not run or claimed.

The final state must be established by a fresh read-only sub-agent pass after
the remediation above; this initial pass is not itself the final approval.
