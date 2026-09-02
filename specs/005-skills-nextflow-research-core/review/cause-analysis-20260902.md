VERDICT: REVISE —— validator 的 ERROR/warning 主要揭示 Skill 打包与工具兼容性问题；fresh architecture-critic 的 REVISE 则揭示 Research Core 的真实契约与证据边界缺口。两者可以同时成立。当前 bounded MultiQC v0 切片可继续作为有界实现，但不应据此宣称 Research Core 已具备可复用架构。

| 现象 | 层级 | 根因 | 证据锚点 | 后果 | 建议方向 |
|---|---|---|---|---|---|
| `../../docs/templates/...` 相对链接越出独立 Skill 目录 | 真实问题；skill-forge 安装/打包层 | Skill 被作为独立可安装单元分发，但正文仍依赖仓库外部路径 | `C:\\Users\\ldc\\.codex\\skills\\skill-forge\\SKILL.md:88,145-146,169-173` 要求标准模板、`references/` 等随 Skill 组织；`skill-forge\\references\\synthesis-rules.md:41` 要求溢出内容移入 Skill 内部 references | 独立安装后链接不可解析，违背可移植性 | 把模板内容复制为随 Skill 分发的 reference，或改为安装环境可解析的稳定链接；不要依赖上游仓库相对路径 |
| `extensions`、`version` 被 validator 警告为未知 frontmatter | 工具/安装兼容性；不是设计本身的结构错误 | skill-forge 的生成约定比当前 validator 的 frontmatter schema 更宽 | `skill-forge\\SKILL.md:16-30,136-146` 明确规定 `extensions`、`version`；`skill-forge\\references\\synthesis-rules.md:9-15` 也将其列为生成字段；`review-skill\\SKILL.md:53-64` 只规定 validator 版本门槛，没有证明其支持这些扩展字段 | 当前 validator 可能降级、警告或忽略字段；不等于 Skill 内容无效，但说明两套 schema 未对齐 | 明确兼容性策略：升级/配置 validator、将扩展字段放入兼容命名空间，或在发布前做 validator 版本矩阵验证 |
| 正文约 5,143 tokens，超过 5,000 | 仅提示；真实但非阻塞质量问题 | 5,000 是 soft target，不是硬上限 | `skill-forge\\SKILL.md:142-145,206-208` 明确使用 “soft-target”，并允许内容进入 `references/`；`skill-forge\\references\\synthesis-rules.md:41` 明确“不要将 soft target 当作 hard cap” | 上下文占用略增；不会自动证明内容错误或不可安装 | 若正文仍可读、完整，可保留；若持续膨胀，将低频内容迁移到 references |
| `review-skill` 中的 Claude quickstart URL 检查失败，解析到私有地址/请求被阻断 | 工具/环境层；不是链接内容本身的真实性结论 | validator 的网络请求、代理、DNS 或 SSRF 防护拒绝了该 URL | `C:\\Users\\ldc\\.codex\\skills\\review-skill\\SKILL.md:74-80` 与 `review-skill\\references\\install-skill-validator.md:39-44` 都把该 URL 作为安装说明；`review-skill\\SKILL.md:5-9` 将 validator 与 Claude CLI 定义为外部依赖 | 只能说明本次 URL 检查未完成；不能推出文档 URL 错误，也不能推出 Claude CLI 不可用 | 将其记录为网络/安全策略导致的 degraded check；如需验证，在允许访问的环境中单独检查 |
| B-001：public façade/module 组合无法由 canonical contract 表达 | 真实架构/契约缺口 | 设计批准 façade 引用多个 atomic module，但 schema 没有对应关系字段 | `specs/005-skills-nextflow-research-core/clarifications.md:58-71`；`contracts/node-contract.schema.json:7-24,25-194` | façade 的边界只能存在于 prose 或内部拓扑中，路由器/验证器无法验证 | 增加最小、带版本且可解析的 module reference；或在完成具体 façade fit-test 前，把该能力明确延期 |
| B-002：静态能力契约与运行状态混合 | 真实架构/契约缺口 | node contract 必填 execution/scientific/release 状态，而 run-status 又重复定义这些状态 | `contracts/node-contract.schema.json:19-23,156-173`；`contracts/run-status.schema.json:7-47`；`contracts/multiqc/node.contract.json:193-196` | public contract 可能过期，或被误解为当前运行状态；`release: approved` 也缺少审批主体和状态转移约束 | 将 node contract 限定为静态能力；把 run_id、运行状态和审批证据放入 run envelope，并由 verifier 检查合法状态组合 |
| B-003：已记录 MultiQC 证据无法从当前 checkout 直接重现 | 真实的证据打包/可复现性问题；根因偏范围/协议与运行环境，不是 Core 抽象本身 | manifest/source map 使用另一工作区的绝对路径，当前 checkout 路径不同 | `evaluation/runs/multiqc-mvp-20260902/input-manifest.json:2`；`artifact-manifest.json:5-14`；`multiqc_sources.json:4`；当前 verifier 路径逻辑在 `evaluation/cases/multiqc-mvp/verifier/verify_case.py:122-124,208-215` | hash 可证明字节一致，却不能证明 artifact identity 在当前 checkout 中可解析；历史 PASS 不能直接等价为当前环境可重现 | 使用仓库相对路径并记录 run-root/host 元数据；在当前 checkout 重跑，或把现有记录降级为历史证据 |
| S-001：schema 未验证跨字段契约完整性 | 真实契约缺口，但当前 bounded slice 可作为 verifier 增强项 | `takes/emits`、`named_outputs.port_id` 是自由字符串，未验证端口存在性、唯一性和方向 | `contracts/node-contract.schema.json:68-113,100-110,197-255`；机械兼容性目标在 `evaluation-protocol.md:91-94` | schema PASS 的 contract 仍可能引用不存在端口、把 input 当 output 或漏掉一侧 | 增加最小 verifier 规则：端口唯一、输入/输出存在、takes/emits 属于端口集合、named output 指向 output port |
| S-002：identity 语义只是描述性字符串 | 真实契约缺口，主要阻塞泛化而非当前单案例运行 | `identity_keys` 和 `constraints` 未定义 namespace、唯一性范围、join cardinality、duplicate/unmatched policy | `data-model.md:81-97`；`contracts/node-contract.schema.json:114-129,242-249`；预期检查见 `research.md:64` | 不同组件可能对“同一记录”有不同解释，组合表面兼容但语义错误 | 定义最小 identity vocabulary，或把这些要求显式纳入独立 verifier contract |
| S-003：provenance 允许占位文本 | 真实契约缺口；对 bounded v0 是证据完整性风险，对通用 Core 是泛化阻碍 | provenance schema 只要求泛化对象/数组，MultiQC contract 使用运行时占位描述 | `contracts/node-contract.schema.json:131-154`；`contracts/multiqc/node.contract.json:173-190` | 无法机械确认输入/输出 hash、工具版本、命令、reference 和环境 identity | 分离静态 source provenance 与 per-run provenance，并定义最小类型化字段及链接 |
| S-004：A0–A3 缺少 eligible-case 与重复运行规则 | 范围/验证协议问题，同时是评估设计缺口 | 定义了分子和分母，却未定义排除条件、随机种子、重复运行聚合和非确定性处理 | `evaluation-protocol.md:45-56,74-105` | pass rate 分母可能不稳定；一次随机运行可能影响结论；不同变体不可严格比较 | 在扩大评估前固定 eligibility、timeout/error 计入方式、seed/repetition 和 paired-case 聚合规则 |

### skill-forge 安装/打包层

skill-forge 本身把 Skill 视为可独立安装、可移植的目录单元。它要求标准模板和 references 通过 Skill 自己的目录结构承载，并要求安装后执行链接存在性检查：`SKILL.md` 的验证门包括“每个正文链接的 reference 必须存在”以及完整的 10 个 mandatory sections（`skill-forge\\SKILL.md:88,98,169-173`）。

因此，越出独立目录的相对链接是真问题。它不是 validator 的误报，而是打包边界与链接目标不一致：源仓库中可能存在该文件，独立安装后却不存在。

`extensions` 与 `version` 则不同。它们是 skill-forge 的明确生成约定，不是随机添加的未知字段（`skill-forge\\SKILL.md:16-30`；`references\\synthesis-rules.md:9-15`）。当前 validator 报未知，说明 validator 的 frontmatter 识别能力与 skill-forge 约定不兼容；它不能单独证明这些字段非法。是否需要调整，取决于目标宿主是否会拒绝未知字段，而不能只根据 warning 判断。

5,000 tokens 是维护性目标。skill-forge 明确规定这是 soft target，并推荐把低频内容移到 references，而不是把它当成发布硬门槛（`skill-forge\\SKILL.md:142-145,206-208`；`references\\synthesis-rules.md:41`）。5,143 tokens 应被视为轻微结构优化提示，不应升级为安装失败或架构缺陷。

### validator 工具/环境层

`review-skill` 将 `skill-validator` 和 Claude CLI 定义为外部依赖，并把 Claude quickstart URL 作为缺失 CLI 时的安装指引（`review-skill\\SKILL.md:5-9,74-80`）。该 URL 检查失败且被解析到私有地址，首先说明检查器的网络访问或安全策略失败。

这类结果不能说明：

- URL 页面不存在；
- 文档内容错误；
- Claude CLI 安装说明无效；
- Skill 的内部链接全部不可用。

它只能说明 validator 在当前网络/代理/SSRF 防护条件下没有完成该项外部检查。应保留为环境层 degraded result，不能当成 Skill 逻辑错误。

### Research Core 真实架构问题

fresh architecture-critic 的 REVISE 有三项核心含义：

1. bounded MultiQC slice 的范围纪律基本成立。设计明确区分了目标、非目标、证据边界和人工审批边界，相关约束见 `spec.md:13-43,126-166`、`evaluation-protocol.md:58-72,107-119`。因此 REVISE 不是在宣称当前 MultiQC smoke run 没有价值。

2. B-001、B-002 是真正的公共契约问题。它们影响“未来组件是否能通过同一个可验证边界组合”的能力。若 bounded v0 只使用单一 MultiQC 节点，B-001 可以显式延期；B-002 则至少应把当前状态定义为局部实现约定，而不能把混合状态模型当成通用 canonical contract。

3. B-003 和 S-004 主要涉及证据可重现性与评估协议。它们不一定阻止一次本地 MultiQC 运行，但阻止把该运行作为可迁移、可复核、可比较的 Research Core 证据。尤其是 B-003：当前记录的路径指向另一 checkout，属于证据资产身份问题，而不是 MultiQC 科学算法问题。

S-001 至 S-003 都是契约机器可验证性不足；它们可能不阻塞当前单案例 bounded slice，但会阻塞“任意组件均可复用”的架构主张。S-004 在启动更大规模 A0–A3 比较前应修复协议，否则 pass rate 的统计含义不稳定。

### 不应误判的问题

不应把 validator 的所有输出都归因于 Skill 内容错误，也不应把 architecture-critic 的 REVISE 理解为当前 bounded MultiQC 实现已经失败。

两者检查的对象不同：

- validator 主要检查 Skill 包的结构、frontmatter、链接、正文大小和外部资源可达性；
- architecture-critic 检查设计的边界、状态模型、契约表达能力、失败语义、可复用性和证据是否支持架构主张。

因此，下面的组合完全一致：

```text
Skill validator:
  包结构/字段/链接检查通过或部分通过
  + 一个相对链接 ERROR
  + 若干兼容性和软目标 warning

Research Core architecture review:
  bounded MultiQC slice 范围清楚
  + 通用 façade、状态、provenance、复用验证仍有缺口
  => REVISE
```

最终方向应是：保留 bounded MultiQC v0 的明确局部范围；将 B-001、B-002、B-003 作为扩大 Research Core 前的修复或显式门槛；将 S-001 至 S-004 纳入契约/评估协议收敛；将 validator 的 frontmatter 和网络问题作为独立的安装兼容性与环境记录处理。

## 2026-09-02 fresh-context remediation disposition

本次修复不删除以上历史判断，而是把它们拆成“当前 bounded evidence 已修复”
与“可复用 Research Core 尚未证明”两层：

- cause-analysis B-001 已由 node contract 的 module_refs、版本化 module
  binding 和 cross-field linter 表达；没有把 self-test 的临时 façade fit 当成
  unseen runtime 验证。
- cause-analysis B-002 已由静态 node capability 与 run-status envelope 分离；
  execution/scientific/release 只存在于单次运行 status 对象。
- cause-analysis B-003 已对冻结 MultiQC run 修复为 repository-relative manifest、
  source map、verdict/review/status pointers，并由当前 checkout 实际 hash/size
  复核；wrapper 的 executor-native absolute paths 与 GB18030 输出仍记录为
  T029/A-007 风险。
- S-001–S-003 已落入 schema、cross-field validator 和 positive/negative verifier；
  S-004 已落入带有机器检查门的 eligibility/repetition protocol，但没有运行
  A0–A3 或生成 score。

逐项证据、五轴 review、命令和延期状态以
review/remediation-20260902.md 为准。architecture-critique 中另一个同号
B-003（unseen validation）仍为 NOT_RUN/NOT_GENERALIZED，不能因本地 case
通过而关闭。
