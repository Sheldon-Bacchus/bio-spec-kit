# 04 Plan Quickstart（审阅入口）

**状态**：`BOUNDED_SLICE_REMEDIATED / REUSABLE_CORE_NOT_GENERALIZED`

## 先看哪几个文件

1. `constitution.md`：本改造工程的不可违反原则和 08 gate。
2. `spec.md`：本工程到底要解决什么、处理哪些输入、明确不做什么。
3. `clarifications.md`：五个已冻结的高影响决策及其 provenance。
4. `plan.md`：从来源研究到反向抽象和评估设计的顺序。
5. `checklists/requirements.md`：逐项检查需求是否写清楚。
6. `tasks.md`：未来具体动作、路径、依赖和验证证据。
7. `analysis.md`：跨文档一致性与门禁结论。
8. `review/approval.md`：本次允许修改的精确路径与评估权限。
9. `contracts/validate_contracts.py`：静态 node、run-status、manifest 和跨字段门禁。
10. `evaluation/validate_protocol.py`：A0–A3 eligibility、failure、repetition 和
    determinism 规则门。

## 人类快速判断

```text
这是不是在描述“改造工程”本身？
  ↓ 是
13 个 Skill 是否都有固定分母和 source role？
  ↓ 是/缺口显式
Nextflow 规则是否有来源、适用边界和失败模式？
  ↓ 是
Core / Bio / Skill / Execution / Verifier 是否分层？
  ↓ 是
主指标是否是任务级结果，而非字段数量？
  ↓ 是
五项澄清、目标路径和本地评估边界是否已获得用户批准？
  ↓ 是，才可进入批准范围内的 08
```

## Agent 读取顺序

```text
constitution → spec → clarifications → plan
             → checklist → tasks → analysis
```

读取外部 Skill 或 Nextflow 材料前，先确认它在 `spec.md` 输入表中的角色。文件
存在不等于它已经进入 context，也不等于它获得执行权限。

## 本次本地 smoke

在仓库根目录运行：

```powershell
& .venv/Scripts/python.exe extensions/bio-multiqc/scripts/run_multiqc.py `
  --input specs/005-skills-nextflow-research-core/evaluation/cases/multiqc-mvp/inputs `
  --output specs/005-skills-nextflow-research-core/evaluation/runs/multiqc-mvp `
  --config extensions/bio-multiqc/config/multiqc_config.yaml `
  --multiqc-bin .venv/Scripts/multiqc.exe `
  --preset fastqc-multiqc-mvp
& .venv/Scripts/python.exe specs/005-skills-nextflow-research-core/evaluation/cases/multiqc-mvp/verifier/verify_case.py `
  --output specs/005-skills-nextflow-research-core/evaluation/runs/multiqc-mvp
& .venv/Scripts/python.exe specs/005-skills-nextflow-research-core/contracts/validate_contracts.py `
  --repo-root . `
  --node specs/005-skills-nextflow-research-core/contracts/multiqc/node.contract.json `
  --run-status specs/005-skills-nextflow-research-core/evaluation/runs/multiqc-mvp/research-core-status.json `
  --self-test
& .venv/Scripts/python.exe specs/005-skills-nextflow-research-core/evaluation/validate_protocol.py
```

运行记录需在同一个 run directory 保存 repository-relative 的
`input-manifest.json`、`artifact-manifest.json` 和 typed
`research-core-status.json`；wrapper 的 executor-native 绝对路径不能直接作为
可移植 Core 证据。完整 Feature verifier 还要求在同一个 run directory 保存
`research-core-review.md`，用于记录 `execution/scientific/release` 三态；它是
独立的边界审查记录，不由 wrapper 的 `multiqc-review.md` 偷代。可直接复核的本轮
运行目录是 `evaluation/runs/multiqc-mvp-20260902/`，其中已包含该记录。

负例应使用一个不存在的 input 目录，预期 wrapper 返回码为 `2`，verdict
为 `failed` 且 `release_ready=false`。运行输出是 evidence，不是自动批准。 

## 明确禁止的快捷判断

- “有 `SKILL.md`” ≠ “有 runtime contract”；
- “有输入/输出两列” ≠ “能组合”；
- “进程 exit 0” ≠ “科学通过”；
- “字段更多” ≠ “Agent 更正确”；
- “文字相似” ≠ “可以合并”；
- “同一个数据集自测通过” ≠ “对 unseen case 泛化”；
- “Langfuse/Promptfoo 有分数” ≠ “科学 oracle 已通过”。

## 当前 Implement/Review 边界

- 本 Feature 的 C-001–C-005 已回答并写回 `spec.md`；
- `review/approval.md` 明确列出允许修改的目标路径；
- 本次仅允许本地 fixture smoke；外部数据、第三方服务、安装和长期评估未获
  授权；
- 目标 Skill 的增补不能包含 Spec Kit 九步；
- execution、scientific 和 release 状态必须分别保留。

本文件只帮助审阅本 Feature，不是未来 Bio preset 的用户使用手册。
