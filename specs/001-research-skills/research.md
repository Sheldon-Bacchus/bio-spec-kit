# 调研报告：科研与生信 Agent Skill

**快照日期**：2026-08-26
**调研范围**：两个相互独立的候选目录，重点评估 Agent 调用方式和证据质量。

## 调研方法

两个子 Agent 的任务范围严格分开：

- Agent A 只搜索跨领域科研能力：文献、写作、引用管理、实验设计、
  Notebook、开放科学和科研自动化。
- Agent B 只搜索生信专用 Skill 或可约束的生信能力：FASTQ/BAM/VCF、
  RNA-seq、单细胞、变异分析、QC 和相关 Agent wrapper。

所有结果使用项目评分规则统一整理：

- Agent 调用合同：20%
- 科研价值：20%
- 维护和采用度：15%
- 文档和测试：15%
- 许可证：10%
- 安全和隐私边界：10%
- Spec Kit 适配性：10%

评分范围为 0-5。GitHub stars、forks 和 release 数量只是观察到的采用度
信号，不等于科研质量。无法核实的字段保留“未核实”。

## 决策摘要

1. 在 Skill 或能力层面保持两个目录完全分开。
2. 通用科研第一批重点评估 PaperQA2、Quarto、Jupyter Book、Zotero MCP
   和 OSF API。
3. GPTomics/bioSkills 是最接近 Agent-native 的生信基线，但进入项目前
   必须完成许可证和依赖审查。
4. nf-core/rnaseq、nf-core/sarek 和 MultiQC 是第一批最适合受控执行试点
   的生信候选，因为输入、输出、版本、测试和执行边界较清楚。
5. ClawBio、Hermes bioinformatics skill、YuliaNuzhnenko skills 和
   K-Dense 生信 skills 在逐个 Skill 的测试、许可证和权限核实前，标记为
   wrapper-needed。
6. sc-best-practices 作为知识与审查规则来源，不作为执行器；CellAgent
   作为科研原型，不作为默认生产 Skill。

## 通用科研 Skill 目录

| 候选 | Agent 调用方式 | 质量与证据信号 | 评分 | 层级 | 下一步 |
|---|---|---|---:|---|---|
| [PaperQA2](https://github.com/Future-House/paper-qa) | Python API 或 CLI，用于论文和证据检索 | 报告为 8.6k stars、872 forks；Apache-2.0；有论文和 LitQA2 评测；文档成熟 | 4.8 | preferred-pilot | 定义只读 literature-evidence adapter，保留 DOI、页码、证据片段、查询和检索时间 |
| [Quarto](https://github.com/quarto-dev/quarto) | CLI 渲染包含 Python/R/Julia 单元的科研文档 | 文档和发布流程成熟；不同组件的许可证需要分别清点 | 4.7 | preferred-pilot | 定义可复现报告 preset，锁定执行环境并增加发布审批 |
| [Jupyter Book](https://github.com/jupyter-book/jupyter-book) | CLI、MyST、Notebook 和 CI 构建 | 报告为 4.2k stars、726 forks；BSD-3-Clause；有文档、CHANGELOG、nox 和 CI | 4.6 | preferred-pilot | 定义 research-notebook/knowledge-base extension，记录执行和依赖清单 |
| [Zotero MCP](https://github.com/drxaibi/zotero-mcp) | MCP server，连接本地 Zotero 或 Web API | 报告为 MIT；本地数据库和 API 模式有文档；写权限和测试规模仍需审查 | 4.1 | wrapper-needed | 先做只读 citation-management adapter；写入和全文传输必须人工批准 |
| [OSF API](https://developer.osf.io/) | REST API 和 OAuth，用于项目、注册、文件和元数据 | 有官方 API/OpenAPI 文档和 OAuth；GitHub stars 不是主要质量指标 | 4.2 | wrapper-needed | 定义 open-science/provenance adapter，使用最小权限并审批写操作 |
| [AutoRA](https://github.com/AutoResearch/autora) | Python API，用于模型发现和实验设计 | 有论文和教程证据；release 和真实设备安全覆盖需要重新核实 | 4.0 | wrapper-needed | 第一阶段只允许模拟实验；真实实验必须人工批准 |
| [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | SKILL.md，兼容 Codex、Claude Code、Cursor，并可调用 Python/API | 报告为 34.5k stars、3.3k forks；有测试和安全脚本；各 Skill 的许可证与权限可能不同 | 4.3 | wrapper-needed | 建立逐 Skill allowlist，不能整体复制仓库 |
| [AI4S Skills](https://github.com/ai4s-research/ai4s-skills) | 面向探索、综述、写作和可复现研究的 Agent Skill package | 报告为 157 stars、15 forks；MIT；有 v0.1.0 和 Zenodo 引用；生产验证有限 | 3.7 | reference-only | 借鉴其 workflow 和审查提示，不直接纳入核心 |
| [OpenAlex MCP Server](https://github.com/cyanheads/openalex-mcp-server) | MCP 查询 OpenAlex 元数据和引用关系 | 调用方式清楚；stars 和 release 稳定性未可靠核实；API 质量需检查 | 3.8 | wrapper-needed | 作为只读文献发现 adapter，记录查询参数、时间和来源 |

### 通用科研结论

PaperQA2 是最适合证据型文献检索的候选。Quarto 和 Jupyter Book 最适合
科研报告、Notebook 和可复现发布。Zotero MCP 与 OSF API 可以补充有状态的
科研资料管理，但写操作必须显式批准。Scientific Agent Skills 的认可度
信号最强，但应作为候选 Skill 来源，而不是未经审计的整体依赖，因为其中
不同 Skill 的权限和许可证可能不一致。

## 生信 Skill 目录

| 候选 | Agent 调用方式 | 质量与证据信号 | 评分 | 层级 | 下一步 |
|---|---|---|---:|---|---|
| [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) | Agent 按任务选择单个 SKILL.md，再调用 Python/CLI 工具 | 明确面向 Codex、Claude Code、Gemini 和 OpenCode；覆盖 FASTQ/BAM/VCF/RNA-seq/单细胞；许可证和采用度需逐 Skill 审查 | 4.5 | wrapper-needed | 作为领域 Skill 参考；只导入经过审计的 allowlist，并补齐 schema、版本锁定和质量门 |
| [nf-core/sarek](https://github.com/nf-core/sarek) | Agent 生成 samplesheet/参数，锁定 pipeline release 后调用 Nextflow | 报告为 573 stars、531 forks；报告为 MIT；有 CI、release、benchmark/truth-set 和 Zenodo 信号 | 4.9 | preferred-pilot | 建立 WGS/WES 变异 preset，加入参考资源、肿瘤-正常配对、QC、注释、provenance 和发布门 |
| [nf-core/rnaseq](https://github.com/nf-core/rnaseq) | Agent 生成 samplesheet/参数并调用固定版本的 pipeline | 有社区模板、CI、release、FASTQ QC、比对/定量和 MultiQC；许可证与当前版本需复核 | 4.8 | preferred-pilot | 建立 bulk RNA-seq preset；差异表达和富集分析必须拆成独立统计阶段 |
| [MultiQC](https://github.com/MultiQC/MultiQC) | CLI 读取结果目录、配置文件和报告模块 | 跨工具 QC 生态成熟，并支持 strict validation；阈值和许可证细节需当前审查 | 4.7 | preferred-pilot | 增加 QC report adapter，同时输出机器可读的质量门指标和人类可读报告 |
| [nf-core/scrnaseq](https://github.com/nf-core/scrnaseq) | Agent 生成 samplesheet 和 aligner/参考/profile 参数 | 官方 usage contract、容器/profile 路径和社区维护信号较好；许可证和采用度需复核 | 4.5 | wrapper-needed | 许可证和参考资源合同核实后，再建立单细胞上游 preset |
| [ClawBio](https://github.com/ClawBio/ClawBio) | 本地 Agent Skill library，提供 Python CLI、Galaxy bridge 和 Nextflow wrapper | 定位为生信原生 Agent；强调 strict preflight 和结果 bundle；项目较新，测试覆盖需审查 | 4.2 | wrapper-needed | 重点评估它的 preflight 和 reproducibility bundle 设计 |
| [nf-core/seqinspector](https://github.com/nf-core/seqinspector) | Agent 提供 FASTQ 或 Illumina run folder，再调用固定版本 pipeline | 范围专注于 QC，并有 nf-core CI 信号；stars 和许可证未可靠核实 | 4.3 | wrapper-needed | 完成许可证和报告 schema 审核后，用于 intake/QC 试点 |
| [sc-best-practices](https://www.sc-best-practices.org/) | 知识型 Skill/checklist，不直接执行分析 | 在方法、QC、统计和报告规范方面较强；本身不是执行器 | 4.0 | reference-only | 把相关章节转换为审查 checklist 和统计决策门 |
| [Hermes bioinformatics skill](https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/research/bioinformatics/SKILL.md) | SKILL.md 指导 Agent 使用序列工具、samtools、BWA、VEP 等命令 | 方法覆盖较广，但没有统一项目合同、审批协议和已核实许可证信号 | 3.8 | wrapper-needed | 审查每个命令，并补齐安全输入/输出、资源和 provenance 合同 |
| [bioinformatics-agent-skills](https://github.com/YuliaNuzhnenko/bioinformatics-agent-skills) | 支持在多个 coding Agent 中安装 Skill 并用自然语言调用 | 覆盖 RNA-seq、单细胞、VEP 和多组学；测试、许可证和维护需核实 | 3.5 | reference-only | 先作为 prompt 与领域范围参考，直到具备可执行测试 |
| [K-Dense 生信 skills](https://github.com/K-Dense-AI/scientific-agent-skills) | SKILL.md，调用 Python、CLI 和 API | 科学 Skill 来源规模大，覆盖基因组和单细胞；必须逐 Skill 审查版本与许可证 | 3.6 | wrapper-needed | 只选择单个 Skill，并加上本项目的质量门和 provenance 合同 |
| [CellAgent](https://arxiv.org/abs/2407.09811) | 面向单细胞分析的科研型 multi-agent framework | 有论文和原型证据；“无需人工干预”的定位不适合默认生产流程 | 3.2 | reference-only | 只借鉴任务分解思想；试点前必须增加容器、固定工具、审计和人工审查 |

### 生信结论

最安全的第一批执行路径是：固定版本的 nf-core pipeline 加 MultiQC，
外层由 Spec Kit preset 负责校验 samplesheet、参考资源、版本、容器、QC
指标、统计分析和审批。GPTomics/bioSkills 是最好的 Agent-native 组织方式
参考，但不是自动可信的依赖；项目本身仍需补齐合同和质量门。

## 备选方案及取舍

### 整体复制大型 Agent Skill 仓库

不采用。混合许可证、隐藏网络调用、可变依赖和不受约束的权限会违反项目
constitution。按单个 Skill 建立 allowlist 更容易审计。

### 只按 stars 选择

不采用。stars 代表认可度，不代表科研有效性、测试、许可证清晰度、可重复
性或数据安全。

### 允许 Agent 任意生成并执行生信 pipeline

不采用。参考版本、统计假设、QC 阈值和结果发布决定必须由确定性合同和
人工质量门约束。

### 所有候选都放入核心 bundle

不采用。文献工具、执行器、知识参考和有状态 MCP server 的权限和运行风险
不同。四个集成层级可以保留这些边界。

## 安装前必须补齐的证据

- 试点前重新核实当前 stars、forks、release 和 commit；本快照中的变化字段
  不能直接作为发布元数据。
- 确认 GPTomics/bioSkills、Scientific Agent Skills、nf-core/rnaseq、
  nf-core/scrnaseq、MultiQC 和 seqinspector 的仓库及单个 Skill 许可证。
- 检查首选候选的依赖锁、容器 digest、网络端点和默认文件系统权限。
- 增加公共数据 smoke fixture，并验证 QC 或审批失败时会停止流程并保留
  失败记录。
