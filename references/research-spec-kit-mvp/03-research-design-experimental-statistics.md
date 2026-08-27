# 03 Research Design、实验设计与统计

> 用途：定义领域 Skill 进入前的通用研究设计合同。当前仅作为设计输入，不接入任何运行链路。

## 结论

`Research Design` 是所有 bioinformatics、wet-lab、imaging 和 ML Skill 的上游合同。它先决定“研究什么、比较什么、谁是独立单位、什么结果支持什么 claim”，领域 Skill 再负责执行方法。

```text
Research Design
  → Experimental Design / AutoRA
  → Statistical Power
  → Domain Execution
  → Statistical Analysis
  → Independent Validation
  → Claim Decision
```

## 一、Research Design 标准字段

### 1. Scientific question

```yaml
question:
  question_id: Q-001
  question: ""
  background_rationale: ""
  hypothesis: ""
  claim_scope: ""
  analysis_mode: exploratory | confirmatory | descriptive | post_hoc
  decision_context: ""
```

问题必须指定比较对象、结果变量、目标总体和解释边界，不能只写“分析数据”“找 marker”。

### 2. Study design

```yaml
study_design:
  study_type: randomized | observational | case_control | cohort | diagnostic | simulation
  design_structure: parallel | paired | repeated | crossover | cluster | nested | factorial | longitudinal
  unit_of_assignment: ""
  unit_of_observation: ""
  unit_of_inference: ""
  allocation_method: ""
  randomization_seed: null
  blocking_factors: []
  strata: []
  order_effects: []
  blinding: ""
  stopping_rules: []
  protocol_deviations: []
```

处理施加在哪一级，独立重复原则上就在哪一级计数。细胞、孔、技术重复不能自动等同于患者、动物或独立生物样本。

### 3. Data and samples

```yaml
data_samples:
  population: ""
  sampling_frame: ""
  eligibility_criteria: []
  exclusion_criteria: []
  sample_unit_id: ""
  hierarchy: "patient > sample > aliquot > well > cell"
  sample_size_planned: null
  sample_size_analyzed: null
  replication_structure: biological | technical | temporal | batch
  attrition_assumption: ""
  missingness_plan: MCAR | MAR | MNAR | model_based | other
  data_source: new | historical | public | simulated
  data_version: ""
```

必须显式区分 biological replicate、technical replicate、重复测量和 cluster；缺失配对不能静默改成独立样本。

### 4. Variables

每个变量应记录：

```yaml
variable:
  variable_id: VAR-001
  role: exposure | treatment | outcome | covariate | confounder | mediator | modifier | quality_metric
  definition: ""
  type: continuous | ordinal | binary | categorical | count | time_to_event | image_derived | embedding
  unit: ""
  measurement_method: ""
  time_anchor: ""
  allowed_values: []
  transformation: null
  missing_code: null
  directionality: ""
  pre_specified: true | false
  derived_from: []
```

主要 outcome、阈值、协变量角色和时间锚点必须在执行前定义。treatment 后产生的 mediator 不能无条件当作混杂变量调整。

### 5. Controls

```yaml
control:
  control_id: CTRL-001
  control_type: untreated | vehicle | sham | positive | negative | technical | batch | reference
  control_role: calibration | background | treatment_effect | quality | positive_validation
  matched_factors: []
  allocation_rule: ""
  expected_behavior: ""
  failure_threshold: ""
  concurrent: true | false
```

vehicle、sham、positive 和 negative control 不能相互替代；没有同期 control 时，通常无法分离时间、批次与处理效应。

### 6. Estimand

```yaml
estimand:
  estimand_id: EST-001
  treatment_contrast: "A - B"
  population: ""
  outcome: ""
  timepoint: ""
  summary_measure: mean_difference | ratio | odds_ratio | hazard_ratio | proportion
  intercurrent_events: []
  handling_strategy: treatment_policy | per_protocol | composite | other
  effect_direction: ""
  practical_threshold: null
  claim_limit: ""
```

统计检验不是 estimand。必须先定义要估计什么，再选择模型和检验。

### 7. Statistical plan

```yaml
statistics:
  primary_analysis: ""
  model_formula: ""
  contrast_set: []
  covariates: []
  assumption_checks: []
  effect_size: ""
  confidence_interval: 0.95
  alpha: 0.05
  sidedness: two_sided
  multiplicity_family: ""
  adjustment: Holm | BH_FDR | Tukey | Bonferroni | simulation | none
  missing_data_method: ""
  outlier_policy: ""
  sensitivity_analyses: []
```

必须同时报告效应量、区间、p 值/校正结果和诊断信息。非显著不等于无效应；替代分析若是结果后才选择，必须标记为探索性或 post hoc。

### 8. Validation strategy

```yaml
validation_strategy:
  validation_type: internal | external | technical | biological | orthogonal | holdout | replication
  validation_target: measurement | model | effect | claim
  independent_unit: ""
  split_rule: ""
  success_criteria: []
  positive_controls: []
  negative_controls: []
  robustness_checks: []
  replication_plan: ""
  claim_upgrade_rule: ""
  failure_interpretation: ""
```

验证必须能改变 claim 状态，不能只是同一批数据上重复同一模型。

## 二、三个通用能力的边界

### Experimental Design / AutoRA

负责实验采集前的设计：随机化单位、区组、分层、plate layout、factorial/DOE、运行顺序、carry-over 和下一轮实验候选。它可以提出方案或模拟，但不能默认控制真实仪器、修改样本或执行外部写操作；每轮需要人工批准、停止条件和审计记录。

### Statistical Power

在设计、estimand、primary analysis 和效应量定义之后计算样本量、MDE、power curve、dropout、ICC、cluster size、交互作用和多重比较影响。不得使用 post-hoc observed power 代替事前设计论证。

### Statistical Analysis

分析已经采集的数据，检查分布、异常值、缺失、方差、残差和模型诊断，按预先定义的 estimand 计算效应量、区间和多重校正。不得在结果出来后重新选择科学问题、主要终点或样本单位。

## 三、统一设计规则

### Paired / unpaired

- 同一受试者、动物、样本或实验单位接受两种条件时，优先建模配对差异；
- 配对必须有 `pair_id`，不完整配对要有预设处理规则；
- 时间序列或重复测量不等于普通 paired t-test；
- 独立单位接受不同处理才是 unpaired。

### 重复与伪重复

```text
n 应对应 treatment 被随机化的层级
technical replicate ≠ biological replicate
cells/wells/measurements nested in sample 必须聚合或使用层级模型
cluster design 需要 ICC 和设计效应
```

### 批次与混杂

至少登记：

```text
batch_id / run_date / operator_id / instrument_id / plate_id
position / processing_order / treatment_arm
```

若 treatment 与 batch 完全重合，治疗效应原则上无法与批次效应区分。回归不能自动修复不可识别的完全混杂，最多降低 claim。

### 阈值与多重性

每个阈值记录：值、单位、方向、来源、是否预先定义、适用场景、失败动作和敏感性范围。QC 阈值、统计显著性阈值和实质重要性阈值必须分开。

先定义 hypothesis family，再选择 Holm、BH-FDR、Tukey 等方法。未校正结果只能作为探索性结果。

### 失败分类

| 类型 | 示例 | 动作 |
|---|---|---|
| 输入失败 | schema、样本表、参考缺失 | stop |
| 质量失败 | control、污染、测量质量不合格 | stop 或 review |
| 设计失败 | 完全混杂、无独立重复 | 禁止强 claim |
| 模型失败 | 不收敛、假设严重违反 | 预设替代模型或 review |
| 验证失败 | 外部验证未过阈值 | 降低 claim |
| 资源失败 | 磁盘、网络、运行环境失败 | bounded retry |
| 科学假设失败 | 设计有效但未见效应 | 报告阴性结果 |

## 四、质量门

```text
RD-01 问题可检验：问题、outcome、比较、总体、模式齐全
RD-02 单位与重复正确：assignment/observation/inference 与复制结构明确
RD-03 设计可识别：随机化、区组、混杂和配对规则明确
RD-04 Estimand 与模型一致：目标估计量、公式、contrast、区间齐全
RD-05 样本量可辩护：SESOI、alpha、power、dropout、ICC/多重性齐全
RD-06 质量和失败可执行：指标、阈值、stop/retry/review 齐全
RD-07 多重性受控：primary/secondary/exploratory 与 correction 齐全
RD-08 验证能改变 claim：独立/正交对象和升级规则明确
RD-09 领域输入合同完整：进入领域 Skill 的必需字段齐全
```

领域 Skill 最少接收：`research_design_id`、`question_id`、`estimand_id`、`sample_manifest`、`variable_dictionary`、`control_plan`、`primary_outcome`、`primary_analysis`、`qc_gates`、`validation_plan`、`claim_scope` 和 `provenance_requirements`。

## 五、MVP 取舍

MVP 暂不实现完整 AutoRA 或复杂 power 模拟。先实现一个可核验的设计合同：

```text
Question + Estimand + Unit/Replication + Primary Analysis
  + QC Gate + Validation Target + Claim Limit
```

只要领域 Skill 能拒绝缺少这些字段的请求，并能把设计记录传给执行和验证阶段，共性底层就已经成立。

