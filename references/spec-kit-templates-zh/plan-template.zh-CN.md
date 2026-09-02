# 实施计划：[FEATURE]

**分支**：`[###-feature-name]` | **日期**：[DATE] | **规格**：[link]

**输入**：来自 `/specs/[###-feature-name]/spec.md` 的功能规格说明

**注意**：本模板由 `__SPECKIT_COMMAND_PLAN__` 命令填写；该命令的定义描述了执行工作流。

## 摘要

[从功能规格说明提取：主要需求 + 基于研究得出的技术方案]

## 技术上下文

<!--
  需要处理：用项目的技术细节替换本节内容。
  这里的结构只是用于指导迭代的建议。
-->

**语言/版本**：[例如 Python 3.11、Swift 5.9、Rust 1.75，或 NEEDS CLARIFICATION]

**主要依赖**：[例如 FastAPI、UIKit、LLVM，或 NEEDS CLARIFICATION]

**存储**：[如适用，例如 PostgreSQL、CoreData、文件，或 N/A]

**测试**：[例如 pytest、XCTest、cargo test，或 NEEDS CLARIFICATION]

**目标平台**：[例如 Linux server、iOS 15+、WASM，或 NEEDS CLARIFICATION]

**项目类型**：[例如 library/cli/web-service/mobile-app/compiler/desktop-app，或 NEEDS CLARIFICATION]

**性能目标**：[领域相关目标，例如 1000 req/s、10k lines/sec、60 fps，或 NEEDS CLARIFICATION]

**约束**：[领域相关约束，例如 <200ms p95、<100MB memory、offline-capable，或 NEEDS CLARIFICATION]

**规模/范围**：[领域相关规模，例如 10k users、1M LOC、50 screens，或 NEEDS CLARIFICATION]

## Constitution 检查

*门禁：Phase 0 研究前必须通过。Phase 1 设计后重新检查。*

[根据 constitution 文件确定的门禁]

## 项目结构

### 本功能的文档

```text
specs/[###-feature]/
├── plan.md              # 本文件（__SPECKIT_COMMAND_PLAN__ 命令输出）
├── research.md          # Phase 0 输出（__SPECKIT_COMMAND_PLAN__ 命令）
├── data-model.md        # Phase 1 输出（__SPECKIT_COMMAND_PLAN__ 命令）
├── quickstart.md        # Phase 1 输出（__SPECKIT_COMMAND_PLAN__ 命令）
├── contracts/           # Phase 1 输出（__SPECKIT_COMMAND_PLAN__ 命令）
└── tasks.md             # Phase 2 输出（__SPECKIT_COMMAND_TASKS__ 命令；不是由 __SPECKIT_COMMAND_PLAN__ 创建）
```

### 源代码（仓库根目录）
<!--
  需要处理：用本功能的具体布局替换下面的占位树。
  删除未使用的选项，并用真实路径展开选中的结构（例如 apps/admin、packages/something）。
  交付的计划中不能保留 Option 标签。
-->

```text
# [不使用时删除] 选项 1：单项目（默认）
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [不使用时删除] 选项 2：Web 应用（检测到“frontend”+“backend”时）
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [不使用时删除] 选项 3：移动端 + API（检测到“iOS/Android”时）
api/
└── [同上面的 backend 结构]

ios/ 或 android/
└── [平台专属结构：功能模块、UI 流程、平台测试]
```

**结构决策**：[记录选中的结构，并引用上面记录的真实目录]

## 复杂度追踪

> **只有在 Constitution Check 存在需要解释的违规时填写**

| 违规项 | 为什么需要 | 为什么拒绝更简单的替代方案 |
|---|---|---|
| [例如第 4 个项目] | [当前需求] | [为什么 3 个项目不够] |
| [例如 Repository pattern] | [具体问题] | [为什么直接访问数据库不够] |
