# Feature Specification: Scientific and Bioinformatics Skill Research

**Feature Branch**: `001-research-skills`

**Created**: 2026-08-26

**Status**: Draft

**Input**: User description: "Research reusable general scientific Agent skills and bioinformatics Agent skills for bio-spec-kit, keeping the two categories separate, and evaluate their quality, ratings, and Agent invocation methods before installation."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Separate the research domains (Priority: P1)

As the owner of `bio-spec-kit`, I want one catalog for broad scientific skills
and one catalog for bioinformatics-specific skills so that a general research
capability is not confused with a domain execution capability.

**Why this priority**: The two catalogs have different users, risks, evidence
standards, and integration paths. Mixing them makes later preset selection
unreliable.

**Independent Test**: Review the catalog headings and candidate scope; every
candidate is assigned to exactly one catalog, and no general-science catalog
entry is a bioinformatics-only skill.

**Acceptance Scenarios**:

1. **Given** the research results are generated, **When** a reviewer opens the
   catalog, **Then** it contains exactly two named sections: broad scientific
   skills and bioinformatics skills.
2. **Given** a candidate focuses on FASTQ, BAM, VCF, RNA-seq, single-cell,
   variant calling, or an equivalent bioinformatics-only capability, **When**
   it is classified, **Then** it appears only in the bioinformatics section.
3. **Given** a candidate focuses on literature, writing, citation management,
   experiment design, notebooks, or open science across domains, **When** it
   is classified, **Then** it appears only in the broad scientific section.

### User Story 2 - Compare Agent-callable skills with evidence (Priority: P1)

As a researcher, I want each candidate to show how an Agent can invoke it and
what evidence supports its quality so that I can distinguish a usable skill
from a promising description or research prototype.

**Why this priority**: Agent invocation is the user's stated selection factor;
stars alone do not establish scientific or operational quality.

**Independent Test**: Select any five candidates from either catalog and verify
that each has a source URL, invocation mechanism, maintenance signal, license
status, documentation/test signal, security note, and score or an explicit
reason for exclusion.

**Acceptance Scenarios**:

1. **Given** a candidate exposes a `SKILL.md`, CLI, MCP server, API, notebook,
   or workflow wrapper, **When** it is recorded, **Then** the exact invocation
   class and required inputs/outputs are stated.
2. **Given** GitHub stars, forks, releases, or commit activity cannot be
   verified, **When** the candidate is scored, **Then** the field is marked
   unverified rather than estimated.
3. **Given** a candidate has a permissive license but executes code or sends
   data to external services, **When** it is evaluated, **Then** those risks
   are visible beside the recommendation.

### User Story 3 - Select candidates without bypassing scientific gates (Priority: P1)

As a project maintainer, I want a repeatable score and admission rule so that
only candidates with sufficient quality, maintenance, safety, and Spec Kit fit
enter a preset, extension, bundle, or adapter.

**Why this priority**: The project will be reused by multiple projects, teams,
and Agents; an undocumented import decision would become a supply-chain and
scientific-quality risk.

**Independent Test**: Re-score a candidate from its evidence record and obtain
the same tier and integration recommendation without relying on hidden context.

**Acceptance Scenarios**:

1. **Given** a candidate scores at least 4.0/5 and has no critical license or
   data-handling failure, **When** it is reviewed, **Then** it may be marked
   preferred for a controlled pilot.
2. **Given** a candidate is a research prototype, has missing license evidence,
   or lacks a reproducible invocation contract, **When** it is reviewed, **Then**
   it is marked reference-only or pilot-only rather than core.
3. **Given** a candidate would execute a pipeline or write to an external
   service, **When** it is proposed for integration, **Then** the proposal
   includes a QC, provenance, and human-approval boundary.

### User Story 4 - Map findings to Spec Kit integration points (Priority: P2)

As a maintainer, I want each recommended candidate mapped to a preset,
extension, bundle, or external adapter so that the next implementation phase
can be planned without copying an entire upstream repository.

**Why this priority**: Research is useful only when it produces a safe,
bounded path to reuse.

**Independent Test**: For every preferred candidate, a reviewer can identify
whether it is directly usable, needs a wrapper, is reference-only, or is
excluded, and can see the next Spec Kit artifact to create.

**Acceptance Scenarios**:

1. **Given** a candidate is recommended, **When** the integration map is read,
   **Then** it names one bounded integration target and its required gates.
2. **Given** a candidate is not suitable for the core bundle, **When** the map
   is read, **Then** it explains whether the reason is scope, license, safety,
   maintenance, or missing evidence.

### Edge Cases

- A repository has high stars but no recent maintenance, tests, license clarity,
  or safe execution boundary; stars MUST NOT be treated as the decision alone.
- A project contains both general scientific and bioinformatics skills; each
  individual skill MUST be classified, not the repository copied as one unit.
- A candidate's documentation describes Agent invocation but does not provide a
  deterministic input/output contract; it MUST be marked wrapper-needed.
- A source reports different star or release values across pages; the catalog
  MUST retain the observation date and mark conflicting values for recheck.
- A skill may contact an external API or receive human genomic/clinical data;
  it MUST be excluded from default execution until data-flow and permission
  review are complete.
- A candidate has no reliably verified license; it MUST NOT enter the default
  bundle, even if its scientific utility is high.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The research artifact MUST contain exactly two disjoint candidate
  catalogs: `scientific-general` and `bioinformatics`.
- **FR-002**: `scientific-general` MUST be limited to cross-domain research
  capabilities such as literature, writing, citation management, experiment
  design, statistical reasoning, notebooks, knowledge management, or open
  science; it MUST exclude bioinformatics-only execution skills.
- **FR-003**: `bioinformatics` MUST contain only bioinformatics-specific skills,
  Agent libraries, or executable capabilities that can be bounded as a
  bioinformatics skill.
- **FR-004**: Every candidate record MUST include its canonical source URL,
  scope, Agent invocation class, required inputs, expected outputs, license
  status, maintenance signal, documentation/test signal, security and privacy
  concerns, and observation date.
- **FR-005**: Adoption signals MUST distinguish verified stars/forks/releases/
  commits from values that could not be verified; missing evidence MUST NOT be
  filled by inference.
- **FR-006**: The score MUST be reproducible on a 0-5 scale using these weights:
  Agent invocation contract 20%, scientific utility 20%, maintenance and
  adoption 15%, documentation and tests 15%, license 10%, security/privacy
  boundary 10%, and Spec Kit fit 10%.
- **FR-007**: A candidate MUST receive one of four integration tiers:
  `preferred-pilot`, `wrapper-needed`, `reference-only`, or `exclude`.
- **FR-008**: A candidate MUST NOT receive `preferred-pilot` when it has an
  unresolved critical license issue, undisclosed sensitive-data transfer,
  unsafe default execution, or no reproducible invocation path.
- **FR-009**: Each `preferred-pilot` recommendation MUST name a bounded Spec Kit
  target and specify the required QC, statistical, provenance, and human-review
  gates.
- **FR-010**: Discovery MUST NOT install, execute, or upload project data to a
  third-party candidate by default; installation or execution MUST be a later,
  explicitly approved implementation task.
- **FR-011**: The research artifact MUST preserve source links for the following
  initial candidates and record their status rather than silently dropping them:
  PaperQA2, AI4S Skills, Scientific Agent Skills, Zotero MCP, OpenAlex MCP,
  Quarto, Jupyter Book, AutoRA, OSF API, GPTomics/bioSkills, ClawBio, Hermes
  Agent bioinformatics skill, bioinformatics-agent-skills, nf-core/rnaseq,
  nf-core/sarek, nf-core/scrnaseq, nf-core/seqinspector, MultiQC,
  sc-best-practices, and CellAgent.
- **FR-012**: The artifact MUST include a concise decision summary identifying
  the first candidates to evaluate in a controlled pilot and the evidence gaps
  that must be closed before a core bundle release.

### Key Entities

- **Candidate Skill**: A repository, package, skill file, service, or workflow
  capability evaluated for reuse in one of the two domains.
- **Evidence Record**: Source links, observation date, version or commit,
  adoption signal, license status, maintenance signal, and quality evidence.
- **Invocation Contract**: Agent-facing description of how the capability is
  called, its inputs, outputs, side effects, permissions, and failure behavior.
- **Scoring Record**: Weighted category scores, total score, confidence, and
  integration tier.
- **Integration Recommendation**: A bounded mapping to a Spec Kit preset,
  extension, bundle, adapter, or a documented exclusion.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The first research snapshot contains at least 6 broad scientific
  candidates and at least 8 bioinformatics candidates, with no cross-domain
  classification errors found in a two-person review.
- **SC-002**: 100% of candidates retained in either catalog have a source URL,
  invocation class, license status, maintenance status, security note, score,
  and observation date, or are explicitly marked evidence-incomplete.
- **SC-003**: 100% of candidates recommended for a controlled pilot have a
  documented input/output contract and a stated QC, provenance, and review
  boundary before installation begins.
- **SC-004**: At least 80% of the top-tier recommendations score 4.0/5 or higher
  and have no unresolved critical admission failure.
- **SC-005**: A maintainer can reproduce the catalog classification and tier
  decision for any selected candidate in under 10 minutes using only the
  recorded evidence and scoring rubric.
- **SC-006**: No discovery run installs a third-party skill, executes an
  unreviewed external command, or transfers project data without an explicit
  implementation approval record.

## Assumptions

- “高薪、高评分” means high quality and high recognition/maintenance signals;
  the project will not treat GitHub stars as a substitute for scientific merit.
- The first snapshot is an evidence review as of 2026-08-26; volatile stars,
  releases, and commit activity must be rechecked before installation.
- A repository that contains both general and bioinformatics capabilities will
  be evaluated at the individual skill or capability level where possible.
- Public data and read-only operation are the default for external integrations.
- Spec Kit remains the coordination, evidence, gate, and provenance layer;
  domain tools remain responsible for domain execution.

## Initial Evidence Sources

### Broad scientific skills

- [PaperQA2](https://github.com/Future-House/paper-qa)
- [AI4S Skills](https://github.com/ai4s-research/ai4s-skills)
- [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- [Zotero MCP](https://github.com/drxaibi/zotero-mcp)
- [OpenAlex MCP Server](https://github.com/cyanheads/openalex-mcp-server)
- [Quarto](https://github.com/quarto-dev/quarto)
- [Jupyter Book](https://github.com/jupyter-book/jupyter-book)
- [AutoRA](https://github.com/AutoResearch/autora)
- [OSF API](https://developer.osf.io/)

### Bioinformatics skills and bounded capabilities

- [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills)
- [ClawBio](https://github.com/ClawBio/ClawBio)
- [Hermes Agent bioinformatics skill](https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/research/bioinformatics/SKILL.md)
- [bioinformatics-agent-skills](https://github.com/YuliaNuzhnenko/bioinformatics-agent-skills)
- [nf-core/rnaseq](https://github.com/nf-core/rnaseq)
- [nf-core/sarek](https://github.com/nf-core/sarek)
- [nf-core/scrnaseq](https://github.com/nf-core/scrnaseq)
- [nf-core/seqinspector](https://github.com/nf-core/seqinspector)
- [MultiQC](https://github.com/MultiQC/MultiQC)
- [sc-best-practices](https://www.sc-best-practices.org/)
- [CellAgent](https://arxiv.org/abs/2407.09811)
