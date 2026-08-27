# Minimal Contract

## Question

必需：`id`、`text`、`estimand`、`scope`、`decision_rule`。

## Observable

必需：`id`、`name`、`definition`、`value`、`source`、`run_id`、`status`。

## Validation

必需：`validation_id`、`target_ids`、`status`、`checks`、`run_id`。

## Claim

必需：`claim_id`、`question_id`、`statement`、`status`、`observable_ids`、`validation_ids`、`evidence_ids`、`does_not_support`。

## Run / Provenance

必需：`run_id`、`status`、`input_refs`、`output_refs`、输入 hash、输出 hash、规则参数和 kernel 版本。

## 状态规则

```text
缺少关键问题或规则 → needs_clarification
输入/解析/provenance 失败 → not_evaluable
主规则失败 → not_supported
主规则通过但独立验证缺失 → inconclusive
主规则和独立验证都通过 → supported
```

`supported` 不等于因果结论，也不自动等于 `RELEASED`；人工审批和更高证据等级由后续层补充。

