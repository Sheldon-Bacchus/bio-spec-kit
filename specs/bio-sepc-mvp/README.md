# bio-spec-mvp

这是 `bio-spec-kit` 大仓库下面的一个目录级独立项目快照，按参考项目
[`Sheldon-Bacchus/bio-sepc-mvp`](https://github.com/Sheldon-Bacchus/bio-sepc-mvp)
整理为三个边界清楚的层级。它可以作为一个单独的 Codex 项目目录打开；源文件
是复制而来，原大仓库中的源路径仍然保留。

## 项目结构

```text
bio-sepc-mvp/
├── 01-spec-work-package/       # 005 项目的完整规格、计划、任务和审查证据
├── 02-skills/                  # Spec Kit 命令、Bio Skill 和运行时投影
│   ├── spec-kit-core/          # 9 个 Spec Kit 核心阶段 Skill
│   ├── spec-kit-auxiliary/     # 非核心阶段的辅助命令
│   ├── adapters/               # 5 个项目适配器
│   ├── reference-stack/        # 8 个参考组件
│   ├── reference-stack-zh-CN/  # 中文镜像，不重复计数
│   └── runtime-projection/     # 5 个 Codex 运行时投影，不重复计数
└── 03-package-sources/         # 可安装/注册的源包
    ├── preset/
    ├── workflow/
    │   ├── bio-research-mvp/    # 当前项目的主 workflow
    │   └── reference-drafts/    # 其他参考稿，不属于当前执行链
    └── extensions/
```

## “9 个”和“13 个”分别是什么

这两个数字属于不同层级，不能相加或互相替代：

1. **9 个 Spec Kit 核心阶段 Skill**：
   `constitution`、`specify`、`clarify`、`plan`、`tasks`、`analyze`、
   `checklist`、`implement`、`converge`。它们负责生成和推进 Spec/Plan/Tasks
   生命周期；`speckit-taskstoissues` 放在 auxiliary，不算核心九阶段。
2. **13 个生信逻辑组件**：5 个项目适配器加 8 个参考组件。
   中文镜像、英文副本、Codex 运行时投影、workflow、preset、bundle 和文档
   都不作为新的逻辑 Skill 计数。
3. **5 个 runtime projection** 是 5 个项目适配器在 Codex `.agents/skills`
   下的运行时副本，不是额外的 5 个逻辑组件。

## 文件分别在哪里

- 规格工作包：`01-spec-work-package/`
- 5 个项目适配器：`02-skills/adapters/`
- 8 个参考组件：`02-skills/reference-stack/`
- 9 个核心 Spec Kit 阶段：`02-skills/spec-kit-core/`
- Codex 运行时副本：`02-skills/runtime-projection/`
- Preset：`03-package-sources/preset/`
- 当前项目 Workflow：`03-package-sources/workflow/bio-research-mvp/`
- 参考 Workflow：`03-package-sources/workflow/reference-drafts/`
- Extension：`03-package-sources/extensions/`

因此，preset 和 workflow 现在不再只存在于大仓库根目录；它们已经复制到
这个独立项目的 `03-package-sources` 中。只有 `bio-research-mvp` 是当前项目
主 workflow；其他 workflow 已明确放入 `reference-drafts`，不会被解释为当前
项目的连续执行步骤。

## Workflow 边界

`bio-research-mvp` 是你的项目级 MVP 编排器。它当前的范围是：

```text
specify → 审查门 → plan → 审查门 → tasks
        → 受限 MultiQC 执行 → 审查门 → 记录批准
```

它不是完整的 S00–S13 生信科研主流程。S00–S13 的科研阶段定义仍属于
`01-spec-work-package` 中的研究设计和审计材料；将它们真正接成可执行主流程
需要单独冻结输入、输出、门禁、执行器和验证器，不能把参考稿直接拼进当前 MVP。

## 与大仓库的关系

这个目录没有嵌套 `.git`，避免在 `bio-spec-kit` 中建立嵌套 Git 仓库。它是
**目录级独立项目**，但 Git 根目录仍然由外层 `bio-spec-kit` 管理。若以后
需要完全独立的 Git 历史，可以从这个目录另行初始化或复制到仓库外部；本次
整理不改变父仓库的源文件。

详细来源和计数见：

- [`02-skills/MANIFEST.md`](02-skills/MANIFEST.md)
- [`03-package-sources/README.md`](03-package-sources/README.md)
