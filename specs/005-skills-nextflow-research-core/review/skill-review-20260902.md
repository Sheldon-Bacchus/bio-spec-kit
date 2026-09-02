# Four-Skill structural review

**Review date**: `2026-09-02 Asia/Shanghai`  
**Mode**: `structural-only` (`llm_scoring: false`)  
**Validator**: `skill-validator v1.6.1`  
**Saved state**: `C:/Users/ldc/.config/skill-validator/review-state.yaml`

本报告只审计本轮安装的四个 Agent Skill；不把第三方 Skill 改写为本项目版本，
不把结构通过解释成科学有效或运行时有效。由于用户要求只保留四个核心 Skill，
没有启动 Claude LLM 评分；因此本报告不提供 LLM novelty 均值，也不声称达到
novelty 阈值 3。

## 1. Structural validation

| Skill | 安装路径 | validator 结果 | 需要处理的 finding |
|---|---|---|---|
| `summarization` | `C:/Users/ldc/.codex/skills/summarization` | `PASS`, exit 0 | 无 |
| `architecture-critic` | `C:/Users/ldc/.codex/skills/architecture-critic` | `PASS`, exit 0 | 无 |
| `review-skill` | `C:/Users/ldc/.codex/skills/review-skill` | `ERROR`, exit 1 | 外部 Claude quickstart 链接校验被本机网络安全层阻断；不能据此判定远端页面不存在 |
| `skill-forge` | `C:/Users/ldc/.codex/skills/skill-forge` | `ERROR + 3 warnings`, exit 1 | 相对链接越出 Skill 目录；`extensions`/`version` 被当前 validator 标为未识别；正文 5,143 tokens 超过建议的 5,000 |

`review-skill` 的硬规则要求先通过 `skill-validator`，所以本轮已补齐必要的
validator 工具，但没有绕过上述错误继续声称四个包全部结构 clean。第三方源包
没有被修改。

## 2. Content checks

| Skill | Examples | Edge cases/failure | Scope/prerequisite gates | MongoDB contextual data |
|---|---|---|---|---|
| `summarization` | `CONDITIONAL`：有文档类型和用途规则，但无完整 before/after 示例 | `PASS`：不可读、内部冲突、问题不匹配和长度失控均有处理 | `PASS`：先定目的/预算、读完整源、保留证据与 caveat | `N/A` |
| `architecture-critic` | `PASS`：有完整 critic prompt、7 维 rubric 和报告结构 | `PASS`：明确何时不使用、fresh context、具体锚点、过度设计和失败 verdict | `PASS`：必须有书面设计；fresh subagent、只读、advisory、不改设计 | `N/A` |
| `review-skill` | `PASS`：有 CLI 命令、退出码表和报告结构 | `PASS`：validator exit 0/1/2/3、LLM 可跳过、内容检查分支均明确 | `PASS`：先检查配置和依赖，再定位 Skill、结构校验、内容审阅 | `N/A`：该 Skill 审计 Skill，不要求 MongoDB 数据 |
| `skill-forge` | `PASS`：triage worked examples 和多种输出文件形状 | `PASS`：cache/improve/create、路径穿越、命名冲突、自我生成、空研究、脚本验证等均显式 | `PASS`：synthesize-only、source sanitization、fact-check、fresh self-review、verification gate | `N/A` |

## 3. Observable quality signals（非 LLM 分数）

| Skill | Token signal | Scope/precision signal | Novelty status |
|---|---:|---|---|
| `summarization` | 1,054 body tokens | 目的预算、证据强度和长度纪律明确 | 未评分；主要价值是 purpose-budget lossy compression |
| `architecture-critic` | 2,211 body tokens | fresh-context、file anchor、7 维评审和不改设计明确 | 未评分；主要价值是把独立 adversarial review 变成硬流程 |
| `review-skill` | 4,219 包含 references/assets | prerequisite、validator 和 structural/content 分层明确 | 未评分；主要价值是可重复结构检查和审计维度 |
| `skill-forge` | 8,043 含 references | synthesize-only、provenance、脚本验证和自审循环明确，但包体偏重 | 未评分；主要价值是未来蒸馏规则，不在本轮调用 |

这里的 token 数来自 validator 的可观察输出，不是效果指标。没有 LLM judge，不能
把“Novelty”写成数值，也不能得出任何 Skill 对模型任务成功率的因果结论。

## 4. Findings

### Blocker / publish blocker

- `SKILL-001` — `review-skill/SKILL.md:80`（同一链接也见
  `references/install-skill-validator.md:44`）：`skill-validator` 报告
  `https://code.claude.com/docs/en/quickstart` 的 HEAD 请求被本机代理解析到
  私有地址并阻断。它是 validator 的环境性 link-check error；在修复或豁免前，
  `review-skill` 不应标成 structural-clean，但不应擅自改掉第三方链接。
- `SKILL-002` — `skill-forge/SKILL.md:183`：`../../docs/templates/skill/standard/template.md`
  在独立安装目录中越出 Skill 根目录，违反当前 validator 的自包含链接要求。
  这说明“从源码子目录下载后作为独立 Skill”与该相对链接假设不一致；第三方
  包不可直接发布为 clean。

### Should-fix

- `SKILL-003` — `skill-forge/SKILL.md:17,30`：`extensions` 与 `version` 被
  `skill-validator v1.6.1` 标为 unrecognized frontmatter。若这是作者有意使用的
  扩展元数据，需要在发布目标的 schema/validator policy 中明确；本轮不替作者
  删除字段。
- `SKILL-004` — `skill-forge/SKILL.md`：body 5,143 tokens，超过 validator
  建议的 5,000。未来实际调用时应按 progressive disclosure 重新评估，不能为了
  变绿而丢掉 forge 的安全门禁。
- `SKILL-005` — `summarization/SKILL.md:16-26`：目的和预算规则明确，但没有
  一个短的输入→压缩输出示例；对“损失什么、保留什么”的行为验证仍需由本项目
  的压缩产物和后续评估补足。
- `SKILL-006` — 四个包均未做 LLM 评分：本轮只能给结构/内容审计，不能满足
  “novelty 均值 ≥ 3”的 full-review 结论。若以后需要数值评分，必须单独批准并
  配置 Claude/等价 judge。

### Nit

- `SKILL-007` — `architecture-critic/SKILL.md:128-134` 要求将报告写到 repo
  root 或设计文件旁；本项目链路将其落在 Feature 的 `review/` 目录，以避免污染
  根目录。该落点是本项目配置决定，不是第三方 Skill 的结构错误。

## 5. 本轮结论

- 可直接用于本项目链路的能力：`summarization`、`architecture-critic`。
- `review-skill` 已用于本轮检查，但其自身存在 link-check blocker；它仍可作为
  审计方法来源，不能称为 clean package。
- `skill-forge` 已安装但明确 deferred；不参与当前压缩或架构审计，不生成新的
  Skill，不修改自己或其他第三方 Skill。
- 本轮配置和审计文件之外，没有把这些 Skill 注入目标 workflow、preset 或现有
  生信 Skill。
