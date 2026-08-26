# 实施计划：科研与生信 Skill 调研

**分支**：001-research-skills | **日期**：2026-08-26 | **规格**：[spec.md](spec.md)

**输入**：specs/001-research-skills/spec.md 中的功能规格

## 摘要

建立一个只读、基于证据的调研目录，包含两个互不重叠的类别：
通用科研 Agent Skill 和生信专用 Agent Skill。每个候选都要有调用合同、
证据记录、加权评分、集成层级以及边界清晰的 Spec Kit 映射。
第一阶段只记录决策和验证合同，不安装或执行第三方 Skill。

## 技术上下文

**语言/版本**：Markdown、YAML 和 JSON；仓库现有的 Python 验证脚本继续
作为唯一可执行辅助工具。

**主要依赖**：Spec Kit 项目模板和 workflow；Git 负责版本化证据；可选的
上游文档和公共仓库页面。本阶段不把任何第三方 Skill 作为运行时依赖。

**存储**：specs/001-research-skills 下的版本化文件，以及审阅通过后放入
仓库 catalogs/ 目录的记录。

**测试**：Markdown 审阅、YAML/JSON 解析、合同字段校验、领域分类复核和
git diff 检查。不执行未经审查的外部命令。

**目标平台**：供 Codex 和其他 Agent host 使用的本地 Git 仓库。

**项目类型**：用于可复用 preset、extension、bundle 和 adapter 决策的
科研调研目录与 Spec Kit 设计产物。

**性能目标**：维护者可以在 10 分钟内复现一个候选的层级决定；一版调研
快照可以在 30 分钟内完成审阅。

**约束**：调研只读；不能把凭据或项目数据传出仓库；stars/releases/
commits 等变化字段必须记录观察日期；未核实的许可证或数据流会阻止
进入默认 bundle。

**规模/范围**：第一版包含至少 6 个通用科研候选、8 个生信候选，以及合同
文件和可重复运行的 quickstart。

## Constitution 检查

*质量门：Phase 0 调研前必须通过；Phase 1 设计后再次检查。*

| 质量门 | 状态 | 证据 |
|---|---|---|
| 证据优先于自动化 | PASS | 每个候选都要求来源、观察日期和证据状态。 |
| 先定义领域合同 | PASS | 两个目录和调用合同已经明确。 |
| 确定性执行与 provenance | PASS | 要求记录版本、commit/release、查询/命令和来源。 |
| QC 与人工质量门不可绕过 | PASS | preferred-pilot 候选必须有 QC、provenance 和人工审阅边界。 |
| Skill 小而可测试、可组合 | PASS | 候选按单个能力评估，并分到边界清晰的集成层级。 |
| 科研安全与证据 | PASS | 调研只读；禁止外部数据和凭据传输。 |

## Phase 0：调研决策

Agent 调研结果汇总于 [research.md](research.md)。核心决策如下：

1. 严格分开通用科研目录和生信目录。
2. 按单个 Skill 或边界清晰的能力评估，不整体复制混合仓库。
3. 把 stars 和 forks 当作次级采用度信号，不能当作质量证明。
4. 只有在调用、许可证、安全和维护证据齐全后，才进入受控试点。
5. Spec Kit 负责协调、证据、质量门和 provenance；领域工具负责实际计算。

## Phase 1：设计与合同

设计产物如下：

- [data-model.md](data-model.md)：候选、证据、调用、评分和推荐实体。
- [contracts/](contracts/)：候选记录、Agent 调用和评分的机器可读字段合同。
- [quickstart.md](quickstart.md)：本地审阅和验证流程。

## 项目结构

### 文档

    specs/001-research-skills/
    ├── spec.md
    ├── plan.md
    ├── research.md
    ├── data-model.md
    ├── quickstart.md
    ├── contracts/
    │   ├── candidate-record.yml
    │   ├── invocation-contract.yml
    │   └── scoring-record.yml
    └── checklists/
        └── requirements.md

### 仓库集成目标

    bio-spec-kit/
    ├── catalogs/                 # 审阅通过后的候选索引
    ├── presets/                  # 面向领域的 Spec Kit 模板
    ├── extensions/               # 有边界的调用和质量门 adapter
    ├── bundles/                  # 可选、经过审计的能力集合
    ├── workflows/                # 生命周期编排
    └── tests/                    # smoke 和合同 fixture

**结构决定**：先把证据和合同放在当前 feature 目录。只有审阅通过后，
才把记录提升到 catalogs/；只有完成单独实现任务并获得明确批准后，才把
可执行候选提升到 extensions/ 或 bundles/。

## 复杂度记录

没有违反 constitution 的地方，不需要复杂度例外。
