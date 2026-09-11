# 维护 humanizer-cn 的约定

本文件说明如何修改 humanizer-cn 而不破坏它的打包或提示词。

## 这个仓库有什么

humanizer-cn 是一个纯 Markdown 的 agent skill，没有构建步骤。`SKILL.md` 是 agent 读取的提示词，是唯一的事实来源。

保持可移植：不要写只适用于某一两个 agent 工具的指令。

## 关键文件

- `SKILL.md` —— 提示词本体。含 YAML 元数据、两条铁律、成因说明、按强弱分级并连续编号的 32 个模式。
- `eval.md` —— 改写后的逐项自检清单。反编造检查放在第一位。
- `README.md` —— 安装、用法、模式概览、版本历史。
- `.claude-plugin/plugin.json`、`marketplace.json` —— Claude 插件与市场清单。
- `agents/openai.yaml` —— OpenAI 兼容 agent 的显示名与默认提示。
- `scripts/validate-package.py` —— 打包自洽性校验。

## 修改规则

- **模式**：从 1 连续编号、无缺口，最强最高频的在前。一个新的 tell 只有在没有现成模式能涵盖它时才单列；优先折进已有模式。增删或重编号任何模式，都要同步更新 `SKILL.md` 里的交叉引用（如"中文专属优化"里的 §编号）、`eval.md` 第四节的分组、以及 `README.md` 的模式概览。校验脚本从 `#### N.` 标题推导模式数。
- **版本**：`SKILL.md` 的 `metadata.version`、`README.md` 版本历史首条、`.claude-plugin/plugin.json` 的 `version` 三处必须一致。不要把 `version` 写成顶层字段。
- **铁律**：`不编造` 与 `最小有效改动` 是本 skill 的立身之本，**禁止删除或弱化**。校验脚本会检查"不编造"是否在场。
- **反编造红线**：任何新增或修改的"改写后"示例，都**只能使用"改写前"已有的信息**。绝不为了"看起来更具体"而虚构事实、名字、数字、日期、来源。这是 humanizer-cn 相对 humanizer-zh 的核心修正，任何示例都不得违反。
- **只检测模式与评分表的隔离**：评分表只服务改写模式；只检测模式不改写、不打分、不猜作者归属。改动任一处都要维持这个隔离。
- **allowed-tools**：与英文 humanizer 不同，cn 保留 `allowed-tools` 声明；改 YAML 时不要误删。
- **历史**：任何行为变化或不明显的修复，都在 `README.md` 版本历史里加一条简短说明。
- **发布前**：运行 `python3 scripts/validate-package.py`。

## 写作风格

在注释、提示词、文档、描述、校验信息里都用平实语言：结论先行、常用词、主动语态、短句短段、同一个东西用同一个词、要求用"必须"、删掉重复和多余的词。行为相关的示例、被盯上的短语、命令、路径、schema 字段、引用要原样保留。
