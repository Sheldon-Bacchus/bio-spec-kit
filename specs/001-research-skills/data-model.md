# 数据模型：Skill 调研目录

## CandidateSkill（候选 Skill）

表示一个外部 Skill、Agent package、服务或边界清晰的生信能力。

| 字段 | 必需 | 规则 |
|---|---|---|
| id | 是 | 稳定的小写标识符；不要使用会变化的显示名称 |
| name | 是 | 上游项目的人类可读名称 |
| domain | 是 | 只能是 scientific-general 或 bioinformatics |
| source_url | 是 | 官方仓库、文档、论文或 API 地址 |
| scope | 是 | 明确包含和排除的能力 |
| invocation_class | 是 | skill-file、cli、mcp、api、notebook、pipeline-wrapper 或 knowledge-reference |
| status | 是 | candidate、reviewed、superseded 或 excluded |
| observation_date | 是 | 变化性证据的 ISO 日期 |

## EvidenceRecord（证据记录）

记录为什么认为候选可信，或者为什么证据仍然不完整。

| 字段 | 必需 | 规则 |
|---|---|---|
| version_or_commit | 否 | release、tag、commit、论文版本或 unverified |
| stars | 否 | 只有从可靠来源观察到数字时才填写，否则为 unverified |
| forks | 否 | 只有从可靠来源观察到数字时才填写，否则为 unverified |
| maintenance_signal | 是 | recent、intermittent、stale 或 unknown，并说明原因 |
| license | 是 | SPDX 风格标识、mixed、missing 或 needs-review |
| documentation_signal | 是 | mature、usable、partial 或 weak |
| test_signal | 是 | contract-tests、CI、examples-only、absent 或 unknown |
| sources | 是 | 支撑该记录的一个或多个 URL |
| confidence | 是 | high、medium 或 low |
| evidence_notes | 是 | 简短、可审计的说明；不得写无证据的结论 |

## InvocationContract（调用合同）

说明 Agent 如何调用能力而不需要自行猜测。

| 字段 | 必需 | 规则 |
|---|---|---|
| entrypoint | 是 | Skill 路径、命令、MCP tool、API 操作或参考动作 |
| input_schema | 是 | 文件、标识符、元数据和必需的参考资源 |
| output_schema | 是 | 预期文件、记录、报告或断言 |
| side_effects | 是 | none、local-files、network-read、network-write、external-write 或 execution |
| permissions | 是 | 最小文件系统、网络、凭据和写入权限 |
| failure_policy | 是 | stop、report-and-review、retry-bounded 或 reference-only |
| provenance_outputs | 是 | 版本、命令、参数、日志、hash 和来源元数据 |
| human_gate | 是 | 发布或外部写入前所需的质量门和审批要求 |

## ScoreRecord（评分记录）

保存可重复计算的加权评估结果。

| 字段 | 必需 | 规则 |
|---|---|---|
| invocation_score | 是 | 0-5 |
| utility_score | 是 | 0-5 |
| maintenance_adoption_score | 是 | 0-5 |
| docs_tests_score | 是 | 0-5 |
| license_score | 是 | 0-5；许可证未解决时不能高于 2 |
| safety_score | 是 | 0-5；未披露的敏感数据传输属于关键失败 |
| speckit_fit_score | 是 | 0-5 |
| total_score | 是 | 加权后的 0-5 总分 |
| confidence | 是 | high、medium 或 low |
| critical_failures | 是 | 没有关键失败时为空列表 |
| reviewer | 是 | Agent 或人工审阅者标识 |
| scored_date | 是 | ISO 日期 |

## IntegrationRecommendation（集成建议）

把候选映射到边界清晰的下一步动作。

| 层级 | 含义 |
|---|---|
| preferred-pilot | 证据足以进行受控公共数据试点；尚不是默认核心依赖 |
| wrapper-needed | 能力有价值，但项目必须补充 schema、权限、质量门或 provenance |
| reference-only | 只使用文档、方法或 prompt 结构；不作为依赖执行 |
| exclude | 范围、安全、许可证、证据或维护失败，禁止复用 |

必需字段：

- target_type：preset、extension、bundle、adapter、checklist 或 none
- target_name
- required_gates
- evidence_gaps
- approval_state：proposed、approved-for-pilot 或 rejected

## 关系与生命周期

CandidateSkill 一对多 EvidenceRecord
CandidateSkill 一对一 InvocationContract
CandidateSkill 一对一 ScoreRecord
CandidateSkill 一对一 IntegrationRecommendation

生命周期：

candidate → evidence-collected → scored → reviewed →
approved-for-pilot 或 reference-only/excluded → superseded

候选只有在调用合同完整、没有关键安全或许可证失败，并且已经确定人工
审阅门之后，才能进入 approved-for-pilot。
