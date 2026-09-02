# 05 — Requirements Quality Checklist

**Feature**：[`../spec.md`](../spec.md)  
**状态**：`REVIEWED / ALL_ACCEPTED_WITH_BOUNDED_SCOPE`

本清单检查的是“这次改造工程的需求是否写清楚”，不是实现测试，也不是 13 个
Skill 的运行验收。`review/requirements-review.md` 记录了本轮逐项判断；40 项
已接受，最终 Analyze 报告已关闭 `RQ-040`。勾选代表需求质量已被审阅，
不代表科学验证或 release approval。

## A. 目标与边界

- [x] `RQ-001` 能在不读取目标 Skill 细节的情况下理解本 Feature 要解决的问题。
- [x] `RQ-002` 明确说明 Spec Kit 是本工程的执行协议，不是目标内容。
- [x] `RQ-003` 明确列出本轮允许产生的文件和明确禁止修改的目标文件。
- [x] `RQ-004` 目标、非目标、依赖和失败恢复没有互相冲突。
- [x] `RQ-005` `08 Implement` 的用户审批门不是隐含在聊天上下文中。

## B. 输入与证据

- [x] `RQ-006` 每个输入材料都有来源角色，且“参考文档”没有被写成执行指令。
- [x] `RQ-007` 外部 worktree 文件的可复现性风险和 C-001 已显式记录。
- [x] `RQ-008` 根 constitution、Feature constitution、Spec Kit command rules 的
      权限关系清楚。
- [x] `RQ-009` FACT、INFERENCE、PROPOSAL、UNKNOWN 的判定规则可以复核。
- [x] `RQ-010` 动态事实（版本、commit、数据库状态、采用度）不会被凭感觉补齐。

## C. 13 个逻辑 Skill 覆盖

- [x] `RQ-011` 5 个项目适配器和 8 个参考组件的计数分母明确。
- [x] `RQ-012` 中文镜像、英文副本、`.agents` 投影不会重复计数。
- [x] `RQ-013` 每个组件都有 `component_id` 和可回溯 source path。
- [x] `RQ-014` 每个组件都要求显式记录 upstream input 和 downstream output。
- [x] `RQ-015` 每个组件都要求 method/estimand、precondition、route 和 hard boundary。
- [x] `RQ-016` 每个组件的 `examples/tests/provenance/runtime_status` 有状态值。
- [x] `RQ-017` “合并”与“编排/handoff/视图统一”在需求中不是同义词。
- [x] `RQ-018` 不同 estimand、身份或失败责任的组件有不可替代边界。

## D. Nextflow invariants 与接口

- [x] `RQ-019` 每条 invariant 都要求来源、范围、科研映射、失败模式和可观察验证。
- [x] `RQ-020` queue/value、cardinality、shape、tuple/meta 和 stable key 都被覆盖。
- [x] `RQ-021` named output、显式 route、原子节点和 subworkflow 组合关系明确。
- [x] `RQ-022` 参数/参考、profile/执行环境、work/publish 和 cache/resume 分离明确。
- [x] `RQ-023` execution success、scientific verdict、human release 不被合并。
- [x] `RQ-024` Nextflow 结构规则没有被偷换成生物学结论或 Spec Kit 生命周期。

## E. Research Core / Bio preset 分层

- [x] `RQ-025` Core、Bio profile/preset、Skill、execution、verifier、review 各有 owner。
- [x] `RQ-026` 每个层都写明负责什么和不负责什么。
- [x] `RQ-027` Markdown、JSON/YAML、Nextflow/脚本和证据记录的读者与职责不混淆。
- [x] `RQ-028` C-003 未确认时，需求不会假装 core 边界已经冻结。
- [x] `RQ-029` `node.contract.json` 的候选命名和待确认状态已显式记录。

## F. 量化与安全

- [x] `RQ-030` 主指标是任务级结果/验收，而不是字段数量或单一 LLM judge 分数。
- [x] `RQ-031` 所有比较变体使用相同数据、任务、模型、工具预算和 verifier。
- [x] `RQ-032` construction 与 validation/holdout 的关系明确，避免用答案设计考试。
- [x] `RQ-033` trace、矩阵和 assertions 工具与科学 oracle、verifier、人工 review
      的所有权没有混淆。
- [x] `RQ-034` 评估未获批准前不安装第三方服务、不上传敏感数据、不启动长期运行。
- [x] `RQ-035` 空结果、冲突、映射损失、来源不可读和不支持 claim 都有失败语义。

## G. Spec Kit 产物一致性

- [x] `RQ-036` 每个 FR/SC/US 至少能映射到一个计划动作、任务或审计检查。
- [x] `RQ-037` 每个任务都有明确动作、文件路径、依赖和验证证据。
- [x] `RQ-038` checklist 检查需求质量，不以“有任务”代替“需求可验收”。
- [x] `RQ-039` Analyze 是只读报告，不会偷偷修写 spec/plan/tasks 或目标文件。
- [x] `RQ-040` 未解决的 CRITICAL/HIGH finding 会阻止进入 Implement。
