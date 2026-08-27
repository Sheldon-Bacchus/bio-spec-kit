# 04 Open Science、Provenance 与可复现

> 用途：定义从输入、代码、参数到结果、报告和发布的可追溯链。当前仅作为设计输入，不接入任何运行链路。

## 结论

provenance 不能只是文件列表，而应是带关系的图：

```text
DATA + REFERENCE + CODE + PARAM + ENV + TOOL + SEED
                         ↓
                        RUN
                         ↓
               RESULT / FIGURE / EVIDENCE / DOC
                         ↓
                    CLAIM / RELEASE
```

hash 证明内容身份，ID 证明语义身份，关系证明来源和依赖。

## 一、核心 artifact 类型

```text
PROJECT   项目与研究问题
DATA      原始、派生、模拟数据
CODE      仓库、commit、脚本、notebook
PARAM     参数、contrast、阈值、随机种子
ENV       lockfile、容器 digest、runtime
TOOL      外部软件、数据库、API
REF       genome、annotation、gene set 等参考资源
RUN       一次具体执行
RESULT    表格、模型、统计输出
FIGURE    图表及其 source data
EVIDENCE  QC、验证、审批、claim reconciliation
DOC       report、paper、supplement
PRES      presentation
EXTERNAL  OSF、DOI、accession、网页/API 快照
```

每个对象要有稳定 `artifact_id`；每次生成要有不可变 `artifact_version_id`。

## 二、关系模型

```yaml
relation:
  from: DAT-counts-v1
  relation_type: used_by
  to: RUN-20260827-001
  role: primary_input
  verified: true
```

建议关系：`derived_from`、`used_by`、`generated_by`、`validated_by`、`visualizes`、`summarizes`、`cites`、`registered_at`、`supersedes`、`failed_at`、`rerun_of`。

最小 `provenance.json`：

```json
{
  "schema_version": "1",
  "project_id": "PROJECT-001",
  "run_id": "RUN-20260827-001",
  "status": "verified",
  "started_at": "",
  "finished_at": "",
  "parent_run_id": null,
  "artifacts": [],
  "relations": [],
  "execution": {},
  "validation": {},
  "external_resources": [],
  "exceptions": []
}
```

## 三、必须记录的元数据

### 数据

来源、文件/对象 ID、大小、时间、SHA-256、格式/schema、样本数量和 ID、原始/派生/模拟类型、访问限制、下载时间、URL、accession/DOI。核验要求：文件存在、size 一致、hash 一致、schema 通过、样本 ID 与 manifest 完全匹配。

### 代码

仓库 URL、commit SHA、branch/tag、clean/dirty 状态、dirty patch hash、实际执行入口、notebook kernel/执行顺序、包版本或代码 hash。dirty workspace 若无 patch 记录，不得标记为 exact reproducible。

### 参数

完整 JSON/YAML 快照、默认值与显式值、contrast、阈值、过滤、reference、annotation、gene set、模型公式、profile、随机种子和参数 hash。运行命令参数必须能与快照和报告中的参数对齐。

### 环境

优先记录容器 image digest，其次是 Conda lock、`uv.lock`、`poetry.lock`、`package-lock.json`，至少要有软件版本清单。还要记录 runtime、workflow engine、executor/profile、CPU/GPU、系统、locale、时区和 lockfile hash。

### 外部资源

记录工具/数据库/API 名称和版本、endpoint、查询参数、请求时间、HTTP 状态、返回内容 hash、DOI/URL/accession。动态或不可下载资源要保存快照、响应或归档、checksum 和失败重试记录。

### 结果与沟通文件

结果记录输入 run、结果 hash、schema、行列数、缺失值/过滤规则、统计方法、软件和参数、结果类别。图表记录 source data、生成脚本/notebook cell、结果 ID、图表参数、单位、图片和可编辑源文件 hash。报告、论文和幻灯片必须引用结果、图表和 evidence ID，并记录生成版本、审阅人、时间和 hash。

## 四、四个冻结点

### F0 设计冻结

冻结 scientific question、estimand、样本/设计元数据、primary contrast、纳排标准、primary endpoint、主要模型和 OSF registration（如有）。修改必须新版本并写变更原因。

### F1 执行输入冻结

冻结数据、reference、code commit、environment lock/container digest、参数、随机种子和 workflow profile，生成 run/input/environment manifest。

### F2 结果冻结

冻结 result tables、诊断、QC verdict、图表 source data、negative-result classification 和 validation report。禁止覆盖，只能新 run。

### F3 发布冻结

冻结 claim 与 result/figure ID 的关系、provenance、validation verdict、review approval、OSF/DOI archive 和 release manifest。

## 五、阶段输入输出与 gate

### Execution

输入：设计冻结、数据 manifest、代码、参数、环境、工具、seed、approved profile。

输出：`run-manifest`、command、stdout/stderr、exit status、input/parameter/environment/tool/output manifest。

Execution Gate 要求所有输入和输出可验证、命令可重构、seed 已记录、失败不能伪装为成功。

### Evidence Validation

输入：run、输出、QC、统计诊断、provenance、外部快照。

输出：schema/statistics/figure/provenance validation、claim reconciliation、exception register。

必须验证：artifact 存在、hash 一致、关系闭合、图表和报告版本一致、报告数字可从结果重算、失败/跳过/waiver 有记录。文件存在不等于内容已验证。

### Reproducibility / Communication

输入：已验证 provenance、frozen results、figures、模板和 approvals。

输出：report、paper、presentation、communication matrix、OSF/DOI record、release manifest。

Release Gate 要求主要 claim 有 evidence、图表有来源、负结果未省略、数字一致、限制已披露、provenance 已归档、人工审批完整。

## 六、Negative、Rerun、Drift 与失效资源

### Negative

明确区分 `negative`、`null`、`inconclusive`、`failed`、`not_run`、`suppressed` 和 `not_applicable`。低功效、执行失败、未运行不能写成“未发现效应”。

### Rerun

重跑必须新建 `run_id`，并记录：原 run、原因、输入是否相同、变化的 artifact、diff、结论是否改变、是否需重新审批。代码、参数、环境或外部资源改变时应标记为 `reanalysis`，不是同一运行重试。

### Drift

监测 Git、lockfile、container、reference、annotation、数据库、API、workflow engine 和硬件/backend。未知或不兼容漂移不得标记为 fully reproducible；漂移后需 fixture/regression test 和差异报告。

### 不可复现

```text
exact
computationally_equivalent
conditional
partial
failed
unknown
```

`failed` 或 `unknown` 可以报告，但不能宣称 reproducible；必须记录失败命令、阶段、日志、环境差异、可能原因、对 claim 的影响和 reviewer/waiver。

### 外部资源失效

优先使用已保存快照；用 checksum 判断是否被替换；不能只依赖活 URL。若必须换资源，要新建 external artifact，并记录 `supersedes`，不能静默改用最新版。

## 七、MVP 取舍

MVP 不需要先做完整 OSF 集成或复杂 provenance graph 数据库。先实现一个 `run-manifest + artifact manifest + sha256 + provenance.json` 的最小链：

```text
输入文件 hash
代码 commit
参数快照
环境摘要
一次 run
输出文件 hash
一个 validation verdict
```

这条链能让后续五个方向共享同一底层证据接口。

