# Evaluation protocol（local fixture first batch）

**Feature**：`005-skills-nextflow-research-core`  
**Status**：`FROZEN PROTOCOL / NO LONG-TERM RUN`  
**Decision**：C-005 resolved on `2026-09-02 Asia/Shanghai`

This file defines an evaluation interface, not a benchmark result. The first
batch is deliberately local and short so that inputs, permissions, oracle,
verifier and provenance remain reviewable in the current repository.

## 1. Case package

Each case must contain or reference:

```text
case/
├── case.yml                 # task, scope, input and expected state
├── inputs/                  # local fixture or declared repository paths
├── oracle.yml               # hidden from the Agent during a real evaluation
├── verifier/                # deterministic checker
├── reference/               # expected observables or bounded reference
└── trace/                   # command/version/hash/variant record
```

The repository copy of `oracle.yml` is a development artifact for this feature;
a production evaluation must make the oracle unavailable to the evaluated
Agent. An external dataset, API or hosted trace service is not part of this
authorization.

### Case eligibility record

Eligibility is decided before an Agent is run and is recorded per
`case_id/variant_id`. A case is eligible only when the case manifest is
schema-valid, its declared input paths and hashes are readable, the oracle and
deterministic verifier are frozen and reachable, the tool/permission/budget
constraints are satisfied, and the case does not reuse an output or oracle
derived while defining the candidate schema.

Pre-run exclusion is limited to the following explicit reasons:
`MISSING_INPUT`, `MISSING_ORACLE`, `MISSING_VERIFIER`,
`PERMISSION_DENIED`, `BUDGET_UNAVAILABLE`, `SCHEMA_INVALID` or
`CONSTRUCTION_LEAKAGE`. Every exclusion record must contain `case_id`,
`variant_id`, `reason_code`, `recorded_at` and the affected path or
decision. An excluded case is not a failure, but it remains visible and cannot
silently change the denominator.

Once a case is eligible, timeout, non-zero execution, missing or malformed
output, verifier exception, verifier failure, malformed trace, and an
unsupported claim are all counted as a failed repetition. They are never
converted into pre-run exclusions after observing the result.

## 2. First-batch case allocation

| Case | Role | Input | Component | Status |
|---|---|---|---|---|
| `multiqc-mvp` | construction + smoke | `tests/fixtures/multiqc/` | `multiqc` | runnable locally |
| `multiqc-mvp/negative/missing-input` | exception/fail-closed | nonexistent input path | `multiqc` | verifier case |
| `shared-integration-reference` | construction/reference plumbing only; not unseen validation | `tests/fixtures/shared-integration/` | `cross-branch-integration` | reserved, not eligible as unseen validation |
| `holdout-unseen-component` | final holdout slot | not populated in this run | unseen component | not run |

The MultiQC case is the only execution smoke in this implementation slice. The
shared-integration case is already one of the fixed 13 components, so it cannot
serve as the required unseen validation case; it is retained only as a
reference/plumbing slot. The `holdout-unseen-component` slot is therefore
explicitly `NOT_RUN` and remains a gate before any reusable-Core claim. No case
is allowed to use an output generated during schema design as its hidden answer
without recording that leakage.

## 3. A0–A3 comparison matrix

| Variant | Spec condition | Core/preset condition | Skill condition |
|---|---|---|---|
| A0 | no Spec Kit artifact | no Research Core | no Skill or fixed raw baseline |
| A1 | official Spec Kit artifacts | no Bio Research Core contract | no Skill or fixed raw baseline |
| A2 | official Spec Kit artifacts | frozen Research Core v0 contract | no selected Skill |
| A3 | official Spec Kit artifacts | frozen Research Core v0 contract | selected component Skill/contract |

For a valid paired comparison, task statement, input manifest, model, tool
permissions, time/compute budget, output format, oracle/verifier and review rubric
are identical. Only the declared Spec/Research Core/Skill condition changes.

### Paired eligibility, repetitions and non-determinism

Eligibility is evaluated independently for every case/variant before execution.
The paired A0–A3 analysis set is the intersection of case IDs that are eligible
for all four variants; exclusions and their reasons remain in the run record.
If the intersection is empty or below the protocol minimum, the comparison state
is `NOT_RUN/INSUFFICIENT_ELIGIBLE_CASES` and no pass rate is emitted.

Each eligible case/variant cell has exactly 3 repetitions. The repetition index
is `1..3`. When the executor exposes a seed, record a seed derived from the
stable tuple `protocol_version:case_id:variant_id:replicate_index`. When it does
not, record `seed_status: unavailable`; never invent a seed or claim controlled
randomness.

The default case policy is `determinism: strict`. Each repetition must pass the
same deterministic verifier and produce the same normalized output hash. A cell
passes only when all three repetitions pass and their hashes agree. Any timeout,
execution/verifier error, failed assertion or hash difference makes the cell
fail and sets `nondeterminism_observed` when applicable. A future case may opt
into `determinism: semantic` only with a frozen semantic verifier; differing
hashes then remain a diagnostic and every repetition must still pass.

The local MultiQC positive/negative runs in this bounded slice are construction
smoke evidence, not A0–A3 repetitions. They must not be used to populate an
A0–A3 score.

## 4. Oracle and verifier contract

The oracle must specify:

- required task-level state (`READY`, `NEEDS_INPUT`, `BLOCKED` or `ESCALATE`);
- required observable artifacts and fields;
- allowed route/method choices and forbidden silent defaults;
- negative cases that must fail closed;
- required input, output, runtime and provenance identity;
- claims that are exploratory only and cannot enter release.

The deterministic verifier may inspect files, JSON/YAML fields, hashes, source
markers, exit codes and explicit status transitions. It must not change the
input, edit the result to pass, or infer a biological conclusion outside the
oracle. Human review remains mandatory for scientific claim and release scope.

## 5. Metrics

### Primary metric

`task_level_pass_rate = passed_case_variant_cells / eligible_case_variant_cells`

A case passes only when the task-level oracle and deterministic verifier pass and
the output stays within its claim boundary. An execution exit code of zero alone
is not a pass.

### Diagnostic metrics

- `contract_completeness`: required contract fields with a value or explicit
  state divided by required fields; diagnosis, not effectiveness.
- `traceability_coverage`: required links
  `requirement → method → component → output → evidence` present divided by
  required links.
- `composition_validity`: compatible port/shape/cardinality/identity/route
  connections divided by attempted connections.
- `execution_realizability`: declared cases with a deterministic execution and
  verifier entry point divided by cases in scope.
- `provenance_completeness`: required source/version/parameter/environment/
  command/hash fields present divided by required provenance fields.
- `ambiguity_rate`: unresolved or multiply-interpretable decision points divided
  by decision points inspected.
- `unsupported_claim_rate`: emitted claims outside observable/estimand/evidence
  boundary divided by emitted claims inspected.
- `fail_closed_rate`: negative cases stopped at the expected boundary with a
  locatable reason divided by negative cases run.

No diagnostic metric may be reported as a substitute for task-level correctness,
scientific replication or causal evidence.

## 6. Splits and authorization

- `construction`: may contain the 13 known components and is used to shape the
  candidate contract.
- `dev`: may be used to fix verifier wording and non-holdout plumbing.
- `validation`: must include a component or workflow not used to define the
  candidate schema. The current `shared-integration` fixture is known
  construction material and therefore cannot satisfy this gate.
- `holdout`: remains untouched until the oracle, verifier and comparison
  conditions are frozen in a separately reviewable run record.

The minimum validation gate is one truly unseen case with a frozen oracle,
verifier and eligibility record. Until it exists, the Core status is
`NOT_GENERALIZED` even if construction smoke passes.

This run authorizes only local fixture smoke and verifier checks. It does not
authorize BixBench/BioBench downloads, external API calls, sensitive-data
transfer, third-party installation, hosted tracing or a long-running benchmark.
