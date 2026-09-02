# Bio-Spec Kit：科研 Spec MVP 精炼总索引

> 用途：作为后续 IDE 编写的单一入口。这里保留结论、项目地图和关键链接；完整审计见 [BIO-SPEC-KIT-REFERENCE.md](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/BIO-SPEC-KIT-REFERENCE.md)。本路线不包含 PA-LUAD 或 Plaud 课堂内容。

## 结论

当前是“官方兼容的科研 Spec 候选架构”，还不是已完成的自驾系统：Bio preset、extension、workflow 尚未在 CLI 中启用，主 bundle 尚未通过解析，active feature 仍缺 `tasks.md`。

## 官方兼容规则

官方主链：

```text
constitution → specify → clarify → plan → tasks → analyze
→ implement → verify/converge
```

官方 artifact 文件名不改：`spec.md`、`plan.md`、`tasks.md`。

科研增强只加后缀：

```text
speckit.specify-research
speckit.clarify-research
speckit.plan-research
speckit.tasks-research
speckit.analyze-research
speckit.implement-research
speckit.converge-research
```

`Quest` 只表示多个 Task 组成的科研目标，不替代官方 Task：

```text
Quest Q-001 → Task T001/T002 → Evidence E001 → Gate
```

暂定组件：`bio-research-mvp` preset、`spec-research-mvp` workflow、`bio-research-core` bundle，以及 `research-evidence`、`research-review`、`deterministic-verifier` extensions。MVP 稳定前不创造另一套独立命名。

## 三个科研过程 Benchmark Bundle

每个 Bundle 都必须包含：`case input + reference package + hidden oracle + negative cases + deterministic verifier + human rubric`。

| Bundle | 测试对象 | 最小内容 | 主要指标 |
|---|---|---|---|
| `spec-fixture-design` | 研究问题 → Spec | 研究请求、样本设计、冲突/缺失信息、gold `spec.md`、estimand、decision ledger | clarification、冲突识别、无依据假设、范围泄漏、Schema validity |
| `spec-fixture-execution` | Spec → Plan → Tasks → Skill → artifact | 已批准 Spec/Plan/Tasks、小型生信 fixture、I/O contract、manifest、verdict、run state | FR/SC 覆盖、false-pass、provenance、fail-stop、重跑一致性、with/without Skill gain |
| `spec-fixture-claims` | Evidence → Validation → Claim → Release | 支持/冲突/不足的 evidence、evidence graph、claim mapping、release decision | evidence-link、overclaim、冲突处理、合理拒答、release-gate accuracy |

第一套必须先做；如果 Spec 错了，后面只能“正确执行错误问题”。E1 计算重现不能冒充 E2 独立队列或 E3 正交/实验验证。

## IDE 编写顺序

1. 建立 `specs/004-spec-research-core/`，固定状态、ID、后缀命名和三套 Bundle 目录。
2. 完成 `spec-fixture-design`：未知、冲突、clarification、blocked 和 Claim boundary 必须可验证。
3. 在隔离项目验证 preset install、template resolve、command materialization、workflow registration、bundle validate/build/install。
4. 完成 `spec-fixture-execution`，只接一个小型真实执行切片。
5. 完成 `spec-fixture-claims`，验证证据图、边界、拒绝和 release。
6. 三套 Bundle 稳定后，才决定是否把 `*-research` 升级为正式产品术语。

## 不可绕过的 Gate

- unresolved/conflict 未处理，禁止 `approved`；
- 每个 FR/SC 必须映射到 Task、验证方式和 Evidence；
- `skipped`、`not-evaluable`、`passed` 必须分开；
- 失败必须 fail-closed，不能用 exit 0 或文件存在代替科研通过；
- reviewer、reason、时间、证据和 waiver 必须可审计；
- 正式证据使用 immutable `run_id`，不能依赖 `runs/current`；
- Analyze、人工批准和 provenance 未通过，禁止 release。

## 项目地图

### 本地核心文件

- [总参考与审计](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/BIO-SPEC-KIT-REFERENCE.md)
- [当前 README](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/README.md)
- [评测矩阵与 MVP](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/docs/evaluation-matrix.md)
- [active feature：research skills](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/specs/001-research-skills/spec.md)
- [MultiQC vertical slice](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/specs/002-multiqc-vertical-slice/spec.md)
- [Shared integration vertical slice](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/specs/003-shared-integration-vertical-slice/spec.md)
- [研究型 preset](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/presets/bio-research-mvp/)
- [候选生信 preset](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/presets/bioinformatics/)
- [研究型 workflow](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/workflows/bio-research-mvp/)
- [生信生命周期 workflow](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/workflows/bulk-rnaseq/)
- [核心 bundle](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/bundles/bioinformatics-core/)
- [现有 fixture 测试输入](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/tests/fixtures/)

### 官方 Spec Kit

- [Spec Kit 总览](https://github.com/github/spec-kit)
- [Agentic SDD](https://github.com/github/spec-kit/blob/main/docs/reference/agentic-sdd.md)
- [Presets](https://github.com/github/spec-kit/blob/main/docs/reference/presets.md)
- [Workflows](https://github.com/github/spec-kit/blob/main/docs/reference/workflows.md)
- [Bundles](https://github.com/github/spec-kit/blob/main/docs/reference/bundles.md)
- [Matsen walkthrough](https://matsen.fhcrc.org/general/2026/02/10/spec-kit-walkthrough.html)

### 评测与社区参考

- [SkillsBench](https://arxiv.org/abs/2602.12670)：with/without Skill 成对实验、deterministic verifier。
- [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401)：软件工程 Skill 边际收益参考。
- [spec-kit-verify](https://github.com/ismaelJimenez/spec-kit-verify)：Spec 到实现的覆盖审计。
- [spec-kit-verify-tasks](https://github.com/datastone-inc/spec-kit-verify-tasks)：防止 Tasks 虚假完成。
- [tiny-spec rubric](https://github.com/GrayMa77er/tiny-spec/blob/main/docs/sdd-evaluation-rubric.md)：SDD 框架质量评分参考。
- [PaperBench](https://openai.com/index/paperbench/)：完整科研复现与层级 rubric。
- [BioFlowBench](https://github.com/YufeiHouAnne/BioFlowBench)：科研工作流指标参考。
- [BixBench](https://arxiv.org/abs/2503.00096)：真实计算生物学任务参考。
- [LAB-Bench](https://arxiv.org/abs/2407.10363)：生物学与实验知识任务参考。
- [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)：task/solver/scorer/sandbox 结构参考。
- [Langfuse](https://github.com/langfuse/langfuse)：trace、dataset、judge 和人工标注参考。
- [DeepEval](https://github.com/confident-ai/deepeval)、[Ragas](https://github.com/vibrantlabsai/ragas)：评测器实现参考，不等于科研验证标准。

## 术语分层

```text
模型层：token、baseline、A/B、ablation、pass@k、cost efficiency
Skill 层：trigger、invocation contract、harness、sandbox、trajectory
Spec 层：Spec、Plan、Task、Quest、contract、schema、clarification、blocked、refusal
验证层：grader、reference package、deterministic verifier、LLM-as-judge、hard gate
科研层：Question、Hypothesis、Estimand、Observable、Validation、Claim、provenance、reproducibility、E1/E2/E3
```

这些分数不能合并成一个“总能力分”：模型能力、Skill 边际收益、Spec 合规性和科研 Claim 有效性必须分轨报告。

## MVP 完成定义

```text
官方 artifact 可生成
∧ 后缀命令可 materialize
∧ bundle 可 validate/build/install
∧ FR/SC → Task → Evidence 可追踪
∧ clarification/conflict/blocked 可执行
∧ Analyze 与人工 Gate 可持久化
∧ 不产生 false pass
∧ immutable run 可重现
∧ 三个 Bundle 都有 verifier 与 negative cases
```

