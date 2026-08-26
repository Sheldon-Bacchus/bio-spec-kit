# Research: Scientific and Bioinformatics Agent Skills

**Snapshot date**: 2026-08-26
**Scope**: Two independent catalogs, with Agent invocation and evidence quality
as the primary selection factors.

## Research Method

The two sub-agents were assigned separate scopes:

- Agent A searched only cross-domain scientific capabilities: literature,
  writing, citation management, experiment design, notebooks, open science,
  and research automation.
- Agent B searched only bioinformatics-specific skills or bounded capabilities:
  FASTQ/BAM/VCF, RNA-seq, single-cell, variant analysis, QC, and related Agent
  wrappers.

The results were normalized using the project rubric:

- Agent invocation contract: 20%
- Scientific utility: 20%
- Maintenance and adoption: 15%
- Documentation and tests: 15%
- License: 10%
- Security and privacy boundary: 10%
- Spec Kit fit: 10%

Scores are 0-5. GitHub stars, forks, and release values are observations, not
proof of scientific quality. An unverified field remains unverified.

## Decision Summary

1. Keep the two catalogs disjoint at the skill or capability level.
2. Use PaperQA2, Quarto, Jupyter Book, Zotero MCP, and OSF API as the strongest
   broad-science candidates for controlled evaluation.
3. Use GPTomics/bioSkills as the most Agent-native bioinformatics baseline, but
   require a license and dependency audit before promotion.
4. Use nf-core/rnaseq, nf-core/sarek, and MultiQC as the strongest executable
   bioinformatics candidates because their inputs, outputs, releases, tests,
   and execution boundaries are more concrete.
5. Treat ClawBio, Hermes bioinformatics skill, YuliaNuzhnenko skills, and
   K-Dense bioinformatics skills as wrapper-needed until their per-skill tests,
   licenses, and permissions are verified.
6. Treat sc-best-practices as a knowledge and review source, not an executor.
   Treat CellAgent as a research prototype, not a default production skill.

## Broad Scientific Catalog

| Candidate | Agent invocation | Evidence and quality signal | Score | Tier | Next action |
|---|---|---|---:|---|---|
| [PaperQA2](https://github.com/Future-House/paper-qa) | Python API or CLI for paper and evidence retrieval | 8.6k stars and 872 forks reported; Apache-2.0; paper and LitQA2 evaluation; mature documentation | 4.8 | preferred-pilot | Define a read-only literature-evidence adapter preserving DOI, page, quote span, query, and retrieval time |
| [Quarto](https://github.com/quarto-dev/quarto) | CLI rendering of research documents with Python/R/Julia cells | Mature documentation and release process; license differs by component and needs inventory | 4.7 | preferred-pilot | Define a reproducible-report preset with locked execution and publication approval |
| [Jupyter Book](https://github.com/jupyter-book/jupyter-book) | CLI, MyST, notebooks, and CI build | 4.2k stars and 726 forks reported; BSD-3-Clause; docs, CHANGELOG, nox, and CI | 4.6 | preferred-pilot | Define a research-notebook/knowledge-base extension with execution and dependency manifests |
| [Zotero MCP](https://github.com/drxaibi/zotero-mcp) | MCP server against local Zotero or Web API | MIT reported; local database and API modes documented; write permissions and testing need review | 4.1 | wrapper-needed | Start read-only citation-management adapter; require explicit approval for writes or full-text transfer |
| [OSF API](https://developer.osf.io/) | REST API and OAuth for projects, registrations, files, and metadata | Official API/OpenAPI documentation and OAuth model; GitHub stars are not the main signal | 4.2 | wrapper-needed | Define open-science/provenance adapter with least-privilege scopes and approval for writes |
| [AutoRA](https://github.com/AutoResearch/autora) | Python API for model discovery and experiment design | Research and tutorial evidence; release and real-device safety coverage need recheck | 4.0 | wrapper-needed | Allow simulation-only design in the first pilot; require human approval for real experiments |
| [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | SKILL.md skills for Codex, Claude Code, Cursor, and Python/API tools | 34.5k stars and 3.3k forks reported; tests and security scripts; per-skill licenses and permissions differ | 4.3 | wrapper-needed | Build a per-skill allowlist; do not copy the repository wholesale |
| [AI4S Skills](https://github.com/ai4s-research/ai4s-skills) | Agent skill package for exploration, review, writing, and reproducibility | 157 stars and 15 forks reported; MIT; v0.1.0 and Zenodo citation; limited production validation | 3.7 | reference-only | Borrow workflow structure and review prompts; do not make it core without stronger tests |
| [OpenAlex MCP Server](https://github.com/cyanheads/openalex-mcp-server) | MCP calls to OpenAlex metadata and citation graph | Invocation is clear; stars and release stability were not reliably verified; API quality needs checks | 3.8 | wrapper-needed | Use as a read-only discovery adapter with query/time/source recording |

### Broad-science conclusions

PaperQA2 is the best evidence-oriented literature candidate. Quarto and
Jupyter Book are the best reproducible publication and notebook candidates.
Zotero MCP and OSF API add stateful research management, but their write
operations require explicit approval. Scientific Agent Skills has the strongest
recognition signal but must be treated as a catalog source rather than a
trusted monolith because its skills may have different permissions and
licenses.

## Bioinformatics Catalog

| Candidate | Agent invocation | Evidence and quality signal | Score | Tier | Next action |
|---|---|---|---:|---|---|
| [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) | Per-skill SKILL.md selected by an Agent and backed by Python/CLI tools | Explicitly targets Codex, Claude Code, Gemini, and OpenCode; broad FASTQ/BAM/VCF/RNA-seq/single-cell coverage; license and adoption numbers need per-skill audit | 4.5 | wrapper-needed | Use as the initial domain skill reference; import only an audited allowlist and add project schemas, version locks, and gates |
| [nf-core/sarek](https://github.com/nf-core/sarek) | Agent creates samplesheet/parameters, pins a pipeline release, then invokes Nextflow | 573 stars and 531 forks reported; MIT reported; CI, releases, benchmark/truth-set, and Zenodo signals | 4.9 | preferred-pilot | Build WGS/WES variant preset with reference, tumor-normal, QC, annotation, provenance, and release gates |
| [nf-core/rnaseq](https://github.com/nf-core/rnaseq) | Agent creates samplesheet/parameters and invokes a pinned pipeline release | Community template, CI, releases, FASTQ QC, alignment/quantification, and MultiQC; license and current release must be rechecked | 4.8 | preferred-pilot | Build bulk RNA-seq preset; keep differential expression and enrichment as separate statistical stages |
| [MultiQC](https://github.com/MultiQC/MultiQC) | CLI against result directories, configuration files, and report modules | Mature cross-tool QC ecosystem and strict validation mode; thresholds and license details need current audit | 4.7 | preferred-pilot | Add a QC report adapter that emits machine-readable gate metrics and human-readable reports |
| [nf-core/scrnaseq](https://github.com/nf-core/scrnaseq) | Agent generates samplesheet and aligner/reference/profile parameters | Official usage contract, container/profile paths, and community maintenance; license and current adoption need recheck | 4.5 | wrapper-needed | Add single-cell upstream preset only after license and reference-resource contract review |
| [ClawBio](https://github.com/ClawBio/ClawBio) | Local Agent skill library with Python CLI, Galaxy bridge, and Nextflow wrappers | Bioinformatics-native positioning, strict preflight, result bundles; project is newer and test coverage needs audit | 4.2 | wrapper-needed | Evaluate its preflight and reproducibility bundle as a reference implementation |
| [nf-core/seqinspector](https://github.com/nf-core/seqinspector) | Agent supplies FASTQ or Illumina run folder and invokes a pinned pipeline | QC-only scope and nf-core CI signal; stars and license were not reliably verified | 4.3 | wrapper-needed | Use for intake/QC pilot after license and report schema verification |
| [sc-best-practices](https://www.sc-best-practices.org/) | Knowledge skill/checklist rather than direct execution | Strong method, QC, statistics, and reporting guidance; it is not an executor | 4.0 | reference-only | Convert relevant chapters into review checklists and statistical decision gates |
| [Hermes bioinformatics skill](https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/research/bioinformatics/SKILL.md) | SKILL.md instructs an Agent to use sequence tools, samtools, BWA, VEP, and related commands | Broad method coverage but no unified project contract, approval protocol, or verified license signal | 3.8 | wrapper-needed | Audit each command and add safe input/output, resource, and provenance contracts |
| [bioinformatics-agent-skills](https://github.com/YuliaNuzhnenko/bioinformatics-agent-skills) | Skill installation and natural-language invocation across coding Agents | Covers RNA-seq, single-cell, VEP, and multi-omics; tests, license, and maintenance need verification | 3.5 | reference-only | Use as prompt and domain-scope reference until executable tests are present |
| [K-Dense bioinformatics skills](https://github.com/K-Dense-AI/scientific-agent-skills) | SKILL.md with Python, CLI, and API calls | Large scientific skill source with genomics and single-cell coverage; per-skill version and license review required | 3.6 | wrapper-needed | Select individual skills only; add the project gate and provenance contract |
| [CellAgent](https://arxiv.org/abs/2407.09811) | Research multi-agent framework for single-cell analysis | Research paper and prototype evidence; its no-human-intervention framing is unsuitable for default production | 3.2 | reference-only | Extract decomposition ideas only; require containers, fixed tools, audits, and human review before any pilot |

### Bioinformatics conclusions

The safest initial executable path is a pinned nf-core pipeline plus MultiQC,
wrapped by a Spec Kit preset that validates samplesheets, references, versions,
containers, QC metrics, statistics, and approval. GPTomics/bioSkills is the
best Agent-native organization reference, but it is not automatically a
trusted dependency. The project must supply the missing contracts and gates.

## Alternatives Considered

### Copying a large Agent skill repository wholesale

Rejected because mixed licenses, hidden network calls, mutable dependencies, and
unbounded permissions would violate the constitution. Per-skill allowlisting is
more auditable.

### Selecting by stars alone

Rejected because stars measure recognition, not scientific validity, tests,
license clarity, reproducibility, or safe data handling.

### Letting an Agent generate and execute arbitrary bioinformatics pipelines

Rejected because reference versions, statistical assumptions, QC thresholds,
and release decisions require deterministic contracts and human gates.

### Making every candidate part of the core bundle

Rejected because literature tools, executors, knowledge references, and
stateful MCP servers have different permissions and operational risks. The
four integration tiers preserve these boundaries.

## Evidence Gaps Before Installation

- Recheck current star, fork, release, and commit values immediately before a
  pilot; volatile values in this snapshot are not release metadata.
- Confirm per-repository and per-skill licenses for GPTomics/bioSkills,
  Scientific Agent Skills, nf-core/rnaseq, nf-core/scrnaseq, MultiQC, and
  seqinspector.
- Inspect dependency locks, container digests, network endpoints, and default
  filesystem permissions for every preferred or wrapper-needed candidate.
- Add public-data smoke fixtures and verify that failed QC or approval gates
  stop execution and preserve the failure record.
