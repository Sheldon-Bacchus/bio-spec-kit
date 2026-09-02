# MVP 源码级调用链分析

本分析只记录已经由当前本地源码和真实运行结果确认的机制。Spec Core、
Agent Skills Core 和 Execution / Workflow Core 是三个不同所有者。

## 真实调用链

```text
文件系统
  → Spec Kit/Codex skill discovery
  → metadata 进入 host context
  → host 选择并激活 skill
  → SKILL.md 进入 context
  → LLM 读取 spec/plan/tasks 并产生 shell/file tool call
  → Agent host 执行 Python wrapper
  → wrapper subprocess.run([...]) 执行 MultiQC CLI
  → MultiQC 读取 FastQC fixture 并写 HTML/JSON/log
  → host 把 stdout/退出码返回 LLM，文件由 Agent 再读取
  → wrapper/verifier 与 Spec acceptance 判断是否通过
```

### 每个箭头的实际所有者

| 箭头 | 当前实现/所有者 | 不应混称的对象 |
|---|---|---|
| 文件系统 → skill discovery | Codex host 扫描 `.agents/skills/<name>/SKILL.md`；Spec Kit 只负责生成/安装目录 | 不是 LLM，也不是 `scripts/` |
| discovery → metadata context | Agent Skills 规范和 host 的加载器读取 frontmatter `name`/`description` | 不是 Spec Core |
| metadata → activation | host 的 skill matching / 用户显式调用决定是否激活 | 不是 Skill 自己执行 |
| activation → `SKILL.md` context | host 将被选中的 `SKILL.md` 正文提供给模型；references 由模型按需读取 | 不是上游仓库整包导入 |
| context → tool call | LLM 根据 skill、spec 和当前状态决定调用；模型只提出调用 | LLM 不直接运行 Python/R |
| tool call → process | Agent host 的 shell/process/file tool 执行命令并返回 stdout、stderr、退出码 | 不是 `SKILL.md` |
| wrapper → MultiQC | `extensions/bio-multiqc/scripts/run_multiqc.py` 的 `subprocess.run` 使用 argv 列表调用外部 executable | wrapper 是脚本，不是新 Tool |
| MultiQC → artifacts | MultiQC 1.35 的 CLI/parser 解析 FastQC，生成 `multiqc_report.html` 与 `multiqc_report_data/` | MultiQC 不做独立 QC 门判定 |
| artifacts → next decision | host 返回命令结果，LLM 读取 verdict/log/data；确定性 verifier 重新检查内容 | 不是“Agent 直觉” |

## Spec Kit 源码证据

- Codex integration 在 `spec-kit/src/specify_cli/integrations/codex/__init__.py`
  将 `folder` 设为 `.agents/`、`commands_subdir` 设为 `skills`，并将
  registrar 指向 `.agents/skills`。
- `spec-kit/src/specify_cli/integrations/base.py` 的 `SkillsIntegration.setup`
  将 command template 处理为每个独立的 `speckit-<name>/SKILL.md`，重建
  frontmatter，然后写入项目目录。它不负责读取科研结果。
- `spec-kit/templates/commands/specify.md` 定义模型在创建/更新规格时应
  读取用户输入、既有 spec 和相关约束；它是提示模板，不是运行时 parser。
- `spec-kit/templates/commands/plan.md`、`tasks.md`、`implement.md` 和
  `converge.md` 是 Agent 的工作指令。它们要求模型读取并修改 Markdown
  artifacts，但不自动证明外部统计程序曾经运行。

## 什么时候 Markdown 进入 context

有三种不同情况，不能合并为“Spec Kit 自动读了 Markdown”：

1. Skill metadata：host 做 discovery 时只需读取 frontmatter，通常先看到
   `name` 和 `description`。
2. Skill body：skill 被匹配/显式激活后，host 将对应 `SKILL.md` 提供给 LLM。
3. Spec artifacts：`spec.md`、`plan.md`、`tasks.md` 不是因为存在于磁盘就
   自动进入 context。当前 `.agents/skills/speckit-*` 的正文明确要求 Agent
   在相应工作流阶段用 file/shell 工具读取它们；模型再根据读取内容决定
   下一次工具调用。

因此，本项目的 MultiQC skill 只规定“读取当前 feature spec、选择 preset、
调用 wrapper、检查 verdict”，不把 Spec 内容复制进 skill，避免重复指令。

## scripts/ 为什么不是 Tool

`SKILL.md` 中的 `extensions/bio-multiqc/scripts/run_multiqc.py` 是一个文件，
由 host 提供的 shell/process tool 启动。它不会因放在 `scripts/` 目录就自动
获得新的权限、schema 或 context channel。真正的 Tool 是 host 暴露的命令执行
和文件读写能力；脚本只实现确定性逻辑。

同理，Rscript、edgeR、limma、clusterProfiler、WGCNA 和 MultiQC 是
Execution / Workflow Core 的 executable/library，不是 LLM，也不是 Skill。

## 状态边界

| 状态 | 短期存在于 LLM context | 必须落盘/可重建 |
|---|---|---|
| 当前选择的 skill、下一步计划 | 是 | 不是唯一真相 |
| spec/plan/tasks 内容 | 可能暂时在 context | 必须保留为版本化 artifacts |
| shell 命令、stdout、stderr、退出码 | tool 返回时可见 | 必须写入 run log/verdict |
| MultiQC 版本、fixture/input hashes | 不能只靠模型记忆 | `runtime`、`input-manifest.json`、`artifact-manifest.json` |
| HTML/JSON/log | 不应塞进 prompt | 作为用户可审计产物 |
| workflow gate/approval | 模型可提出选择 | 必须由 workflow/approval record 持久化 |

## Skill 增多后的 routing 与 conflict

当前 MVP 采用固定 allowlist，不开发动态 router。每个 skill 的 description
只描述触发边界：MultiQC 负责汇总 QC；bulk-pa-luad 负责 paired DE；
pathway-enrichment 负责 GO/KEGG；WGCNA 负责模块；cross-branch 负责交集
和方向分层。它们通过 artifact contract 连接，而不是重复把所有 instructions
互相复制。

后续 skill 数量增加时应保持三层 disclosure：frontmatter 做廉价 routing，
`SKILL.md` 只放当前决策约束，较长方法说明放 `references/`。冲突的主要
来源是多个 skill 对同一结果文件给出不同写入规则，因此结果文件只能由
Execution Core 写，skill 只选择 preset、调用 executable 和解释边界。

## implement/converge 的能力边界

`implement` 可以依据 `tasks.md` 让 Agent 执行任务、编辑代码并运行命令，
`converge` 可以把 spec/plan/tasks 与代码状态作一致性审计并追加缺失任务。
它们都不能仅凭 Markdown 证明：

- R/CLI 真的运行过；
- 结果值来自输入而不是人工改写；
- 外部数据库版本仍与上次相同；
- HTML 内容真实对应上游 log。

所以 MVP 将内容级检查放入 wrapper/test：JSON 中必须有 FastQC sample/value、
log 必须确认 `Found 1 reports`、source map 必须存在，并用“修改 fixture 后
结果跟着改变”的测试阻止静态模板捷径。`release_ready` 只在这些检查和
MultiQC exit code 同时通过时为 true。

## 当前 bio-spec-kit 实际架构图

```text
Spec Core
├── specs/001-research-skills/         # research feature artifacts
└── specs/002-multiqc-vertical-slice/  # MVP black-box feature

Agent Skills Core
├── .agents/skills/speckit-*            # Spec Kit native Codex skills
├── .agents/skills/{5 project skills}   # runtime discovery copies
└── spec-mvp/skills/{5 adapters}       # auditable staging source + references

Execution / Workflow Core
├── extensions/bio-multiqc/             # wrapper, config, extension command
├── workflows/bulk-rnaseq/              # lifecycle controller, not runtime engine
├── spec-mvp/presets/                   # MVP preset contract
├── spec-mvp/workflows/                 # vertical-slice workflow contract
└── tests/fixtures/multiqc/              # upstream FastQC input

External runtime
└── .venv/Scripts/multiqc.exe (1.35)
```
