# Evidence Closure Kernel MVP

这是 Research Spec Kit 的第一个隔离、可运行 MVP。它不是完整生信流程，也不修改上游 Spec Kit 或当前正式 Bio preset。

## MVP 证明什么

它只证明一条最小科研证据闭环可以被机器执行并审计：

```text
Question → Observable → Validation → Claim
                         ↓
                    Run/Provenance
```

Demo 使用本地固定的 PA/LUAD effect vector，不下载真实数据，不调用 OSF、PubMed、MCP 或实验设备。

## 运行

在本目录执行：

```powershell
python run_demo.py --scenario supported --output .demo-out/supported
python run_demo.py --scenario not-supported --output .demo-out/not-supported
python run_demo.py --scenario inconclusive --output .demo-out/inconclusive
python run_demo.py --scenario invalid-provenance --output .demo-out/invalid-provenance
```

每个输出目录应包含：

```text
observables.json
validation-verdict.json
claim.json
provenance.json
run-manifest.json
summary.json
```

`supported` 只表示预先定义的验证规则通过；由于 Demo 没有人工审批，`release_ready` 仍为 `false`。

## 场景含义

| 场景 | 预期 claim 状态 | 含义 |
|---|---|---|
| `supported` | `supported` | 主分析与独立验证均满足规则，但仍待人工复核 |
| `not-supported` | `not_supported` | 主分析或验证未达到预设规则 |
| `inconclusive` | `inconclusive` | 有主分析信号，但缺少独立验证 |
| `invalid-provenance` | `not_evaluable` | 输入 hash 与声明不一致，不能评价 |

## 设计限制

- 只使用 Python 标准库；
- 输入采用 JSON + TSV，避免第一版引入 YAML 依赖；
- 只计算方向一致性和响应基因重叠，不执行真实 DEG；
- Claim 状态由代码中的显式规则计算，不由模型自由生成；
- 时间戳、临时路径和完整 HTML 不参与规范化验收；
- 历史输出不覆盖，新的参数/输入应产生新的 output 目录和 run ID。

## 后续接入边界

后续可将 MultiQC、bulk RNA-seq、pathway、WGCNA 或其他能力作为 Observable provider / Skill adapter 接入，但它们必须遵守本目录定义的 Question、Validation、Claim、Run 和 Provenance 关系。

