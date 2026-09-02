# SkillsBench 对照协议参考

更新时间：2026-08-31

本文档解释 SkillsBench/BenchFlow 的测试逻辑，并把它压缩成当前项目可以先执行的本地协议。这里记录的是结构和实验设计，不在本文件中创建 task YAML，也不把外部 SkillsBench 任务直接伪装成本项目的生物科研 benchmark。

## 1. 任务目录结构

SkillsBench 当前的 native task 入口是 `task.md`；任务运行环境、oracle 和 verifier 分开保存：

```text
task-id/
├── task.md                 # 给 Agent 的任务说明和任务元数据
├── environment/
│   ├── Dockerfile          # 固定运行环境
│   └── skills/             # with-skill 时挂载的任务 skill
├── oracle/
│   └── solve.sh            # 人工编写的参考解；Agent 不可见
└── verifier/
    ├── test.sh             # deterministic verifier 入口
    └── test_outputs.py     # 可选的结构/语义检查
```

当前 BenchFlow native 标准还支持 `verifier/verifier.md`、`verifier/rubrics/` 和 `evidence/`。本项目先保留上面的最小概念结构；真正落盘时，`task.md` 仍按本项目既有 Spec/Workflow 规则生成，不先复制外部 YAML。

## 2. 四个角色分别是什么

### no-skill

同一个 Agent、同一个模型、同一个 task、同一个 container 和同一个 verifier，但不挂载目标 skill：

```text
skill-mode = no-skill
skills-dir = empty / omitted
```

它测的是“没有额外 skill 时的基线能力”。不能把通用系统内置能力、工具能力或任务输入误判成目标 skill。

### curated-skill

仍然使用完全相同的 Agent 和模型，只把人工选定的 skill 目录挂载进去：

```text
skill-mode = with-skill
skills-dir = <selected local skill directory>
```

它测的是“同一模型得到这个 skill 后是否提升”。一次只放本实验声明的 skill，不能把整个 `.agents/skills`、外部仓库或 reference-package 一起挂进去。

### oracle

`oracle/solve.sh` 是人工维护的参考实现。先单独运行 oracle，确认任务和 verifier 能得到满分，再让模型运行。oracle 不等于 LLM，也不能复制到 Agent workspace；它只负责证明题目和验收链条本身成立。

### deterministic verifier

verifier 在 Agent 退出后运行，只读取 Agent 留下的约定输出和可公开检查的状态，不读取 oracle 的答案文件。它应该使用 schema、解析、精确值、集合关系、统计边界和 provenance 检查，并写出：

```text
/logs/verifier/reward.txt   # 0.0 到 1.0 的兼容标量
/logs/verifier/reward.json  # 分项证据和失败原因
```

verifier 自己出错属于 infrastructure failure；Agent 输出不正确则是 scored failure。对科研案例，不能用“图片看起来像”替代数值和语义检查。

## 3. 最小测量矩阵

先不做 self-generated-skill，也不换本地模型；每个模型先跑以下两个条件：

| 条件 | 模型 | 任务/输入 | 工具预算 | verifier | 目的 |
|---|---|---|---|---|---|
| A | 固定模型 M | 同一任务、同一 capsule | 固定 | 同一个 | no-skill baseline |
| B | 固定模型 M | 同一任务、同一 capsule | 固定 | 同一个 | curated-skill lift |

每个 cell 做多次重复，而不是只看一次：

```text
model × task × condition × repeat
```

最少记录 `run_id`、模型版本、skill 内容 digest、task digest、工具调用轨迹、输入/输出文件 digest、耗时、token/cost、verifier reward 和失败原因。A/B 之间唯一有意变化的是 skill 可见性。

## 4. 当前项目怎样测 `bix-26-q3`

`bix-26-q3` 是 BixBench 的 KEGG/DE 开放回答题，不是天然的 artifact benchmark。它的适配顺序应是：

1. 把 capsule 数据放进 task environment；reference-package 和原始 JSONL 不挂给 Agent。
2. 把题目改成要求 Agent 生成结构化结果，例如 `answer.json`，至少包含条件、阈值、物种代码、通路名称、贡献基因数和 provenance。
3. 用独立 oracle 从 `res_GluFevsGluFePlus.rds` 重算目标值；不要只抄 JSONL 的 `ideal`。
4. verifier 精确检查 `answer.json` 的 schema、数值、通路、方向、阈值和证据链；纯文本 `11` 只能作为兼容字段，不能是唯一证据。
5. 分别运行 no-skill 和 curated-skill。curated skill 先只放一个明确的 DE→KEGG skill；不要同时注入整个 bio skill 库。

`bix-26-q3` 的 notebook 还暴露了一个重要 negative case：题目文字提到 `padj < 0.05`，而 notebook 的上调筛选段只写了 `log2FoldChange > 1.5`，随后由 `enrichKEGG` 使用 p/q-value cutoff。这个差异必须进入任务的 ambiguity/claim boundary，而不是让 Agent 猜一个“看起来合理”的实现。

## 5. 是否需要本地部署 nanoGPT / “nono-gpt”

不需要。SkillsBench README 中的 nanoGPT 是某个单独的 GPU 任务对象；普通的 no-skill/curated-skill 评测不要求部署或训练 nanoGPT。

对当前生物科研 MVP，正确顺序是：

```text
固定一个可调用的模型 M
        ↓
同一个 Agent harness
        ├── no-skill
        └── curated-skill
        ↓
同一个本地 sandbox + 同一个 deterministic verifier
```

本地模型是可选项，不是前置条件。若以后用本地模型，必须让 no-skill 和 curated-skill 使用同一模型、同一量化版本、同一上下文上限、同一工具权限和同一预算；否则测到的可能是模型差异，不是 skill lift。第一轮建议先用一个可稳定记录调用轨迹的模型完成协议验证，再增加本地模型作为第二个 `model` cell。

## 6. 不污染 Agent 的硬边界

- Agent 只能看到 task prompt、声明的输入数据、允许的工具和选定 skill。
- `oracle/`、原始 BixBench JSONL 的答案列、hidden-oracle 和 verifier 私有 fixture 不进入 Agent mount。
- verifier 在 Agent 退出后启动；Agent 不能调用 verifier 读取答案。
- no-skill 运行不能读取 task-local `environment/skills/`；with-skill 运行只能读取本次声明的 skill。
- 当前先测 `no-skill` 与 `curated-skill`；`self-gen` 等以后单独开实验，不能混入第一轮结论。

## 来源

- [SkillsBench README](https://github.com/benchflow-ai/skillsbench/blob/main/README.md)
- [SkillsBench skill instructions](https://github.com/benchflow-ai/skillsbench/blob/main/.agents/skills/skillsbench/SKILL.md)
- [BenchFlow CLI reference](https://github.com/benchflow-ai/benchflow/blob/main/docs/reference/cli.md)
- [BenchFlow task standard](https://github.com/benchflow-ai/benchflow/blob/main/docs/task-standard.md)
- [BenchFlow task authoring](https://github.com/benchflow-ai/benchflow/blob/main/docs/task-authoring-task-md.md)

