# 快速开始：验证 Skill 调研设计

本指南只验证本地调研产物，不安装或执行任何第三方 Skill。

## 前置条件

- 在仓库根目录运行命令。
- Spec Kit CLI 1.0.0 或更高版本。
- Git。
- Python 可选，仅用于本地解析 YAML/JSON。
- 不要向任何候选项目提供凭据或项目数据。

## 1. 确认 feature 位置

    Get-Content .specify/feature.json
    Test-Path specs/001-research-skills/spec.md
    Test-Path specs/001-research-skills/plan.md

预期结果：feature.json 指向 specs/001-research-skills，并且两个 feature
文件都存在。

## 2. 解析当前 Spec Kit 模板

    specify preset resolve spec-template
    specify preset resolve plan-template

预期结果：两个命令都能返回本地或 bundled 模板路径，不报错，并且解析
出来的模板仍然与当前项目 preset 兼容。

## 3. 检查规格质量

    rg -n "\[NEEDS CLARIFICATION|ACTION REQUIRED|\[FEATURE|\[DATE|\[PROJECT_NAME" specs/001-research-skills
    git diff --check

预期结果：第一条命令不应找到未解决的占位符；git diff --check 不应报告
空格或换行问题。

## 4. 检查两个领域的边界

阅读 research.md，并确认：

1. 通用科研候选只涉及文献、写作、引用、Notebook、实验设计、开放科学
   或跨领域科研能力。
2. 生信候选只涉及生信专用 Skill 或边界清晰的生信执行能力。
3. 没有候选同时出现在两个目录。
4. 每个候选都有来源 URL、调用类型、评分、集成层级和下一步动作；如果
   证据不全，必须明确标记。

预期结果：目录至少包含 6 个通用科研候选和 8 个生信候选。

## 5. 验证合同文件

    Get-ChildItem specs/001-research-skills/contracts/*.yml
    rg -n "name:|version:|required:|properties:|admission_rules:" specs/001-research-skills/contracts

预期结果：candidate-record.yml、invocation-contract.yml 和
scoring-record.yml 都存在，并包含各自的必需段落。

如果环境中安装了 YAML parser，可以运行：

    python -c "from pathlib import Path; import yaml; [yaml.safe_load(p.read_text(encoding='utf-8')) for p in Path('specs/001-research-skills/contracts').glob('*.yml')]; print('YAML contracts: OK')"

预期结果：输出 YAML contracts: OK。

## 6. 验证准入质量门

对每一个标记为 preferred-pilot 的候选：

- 确认评分至少为 4.0。
- 确认没有关键许可证、敏感数据、不安全默认执行或不可重复入口失败。
- 确认已经写明 QC、provenance 和人工审阅边界。

预期结果：存在未解决许可证或权限问题的候选，只能标记为 wrapper-needed
或 reference-only，不能标记为 preferred-pilot。

## 7. 记录审阅结果

开始试点前，应该在一个审阅过的 Git commit 中记录：

- 观察日期和重新核实后的采用度数据；
- 上游版本或 commit；
- 许可证和依赖清单；
- Agent 调用合同；
- 数据流和权限审查；
- 人工审批者和审批状态。

本验证流程不包含安装命令。安装必须在质量门通过后，作为单独的实现任务
执行。
