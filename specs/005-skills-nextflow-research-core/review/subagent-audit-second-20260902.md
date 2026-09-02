# 第二次独立子 Agent 审计记录（修复前）

**审计 agent**：Ampere (`01a0609a-f91d-7180-842d-d60a051e1354`)  
**审计模式**：只读；未写文件、未联网、未安装依赖、未运行长期 benchmark   
**审计范围**：当前工作树中的 Feature、MultiQC Skill/preset、contract、verifier 和正/负运行产物  
**结论**：`CONDITIONAL`；不建议在修复 verifier 前关闭

## 结论摘要

该审计确认以下主体证据成立：

- `node-contract.schema.json` 和 `run-status.schema.json` 将 execution、scientific、release 分成独立的封闭枚举；正例 status envelope 为 `passed` / `not-verified` / `pending`，负例 wrapper 为 failed / false / false。
- `skill-audit-record.yml` 有固定 13 条记录（5 个 project adapters + 8 个 reference components），mapping 有 13 个唯一数据行，记录均有 `hard_boundary` 和必要审计字段。
- preset 已在 `preset.yml` 直接声明 MultiQC 的 component→Skill→node contract→profile 绑定。
- `tasks.md` 顶部状态已包含 `T001-T025,T027 COMPLETE; T026,T028,T029 DEFERRED`；T027 已完成，T026/T028/T029 仍按边界延期。
- 两份 MultiQC Skill 字节一致，未发现把 Spec Kit 九步写入运行 Skill 的证据。
- 未发现把 local smoke 写成科学有效性、QC/release approval、13 个组件 runtime verified、holdout 或 benchmark 的越界声明；A-007 的 GB18030 portability 观察被保留；既有 dirty files 未被归因或修改。

## Finding

| ID | 严重度 | 位置 | 判断 |
|---|---|---|---|
| A-009 | MEDIUM | `evaluation/cases/multiqc-mvp/verifier/verify_case.py:77-79,122-123,137-145,158-159` | verifier 对 HTML、日志、review 和负例错误仍使用 substring/marker 检查，不能满足“结构化、字段级、fixture-derived 的严格精确校验”，存在理论上的伪通过风险。 |

审计未发现 CRITICAL 或 HIGH finding，也未发现额外 LOW finding。关闭条件是：将上述文本 substring 检查改为结构化/精确等值断言，重新执行现有正例和负例 verifier，并由新的只读审计确认结果。

## 处理状态

该 finding 已在本记录之后、且仍在 `review/approval.md` 明确的 verifier 路径内修复：

- HTML 改为 `HTMLParser` 收集 exact title/section/module anchors；
- log 改为完整 logging record 的 `fullmatch`，精确要求 FastQC report count 为 `[1]`；
- source map 改为与 fixture-derived expected map 完整等值；
- review 改为完整 fenced YAML status block 和 exact boundary sentence sequence；
- negative error 改为 fixture-derived input path 与完整 error message 等值比较。

本记录是修复前审计的可追溯证据，不是最终关闭结论；修复后的最终审计另行记录。
