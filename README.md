# Cross-System Hub — 跨体系个人分析器 v3

> 心理 / 关系 / 成长 / 行动 / 身心 / 判断 / 塔罗 / 运势 / 周易 九个维度看个人处境，毛选"矛盾-行动引擎"抓主要矛盾、落成行动，判断维度把倾向改写成可检验的命题。

## 🧭 体系结构

| 维度 | 层 | 入口 | 子 skill |
|------|----|------|:---:|
| 🧠 **心理**（荣格 + 弗洛伊德） | 观察 | `skills/psyche/` | 20 |
| 💞 **关系**（依恋 + 情绪聚焦） | 观察 | `attach-*`、`eft-*` | 8 |
| 🌱 **成长**（心态） | 观察 | `mindset-*` | 4 |
| ⚙️ **行动**（习惯 + 深度工作） | 观察 | `habit-*`、`deepwork-*` | 8 |
| 🌿 **身心**（黄帝内经） | 观察 | `skills/huangdi-neijing/` | 23 |
| 🎯 **判断**（超预测） | 校准 | `forecast-*` | 3 |
| 🃏 **塔罗**（Rider-Waite-Smith） | 象征 | `skills/tarot/` | 4 |
| 🌟 **运势**（八字 / 星盘 / 紫微 / 托勒密古典） | 象征 | `skills/fortune/` | 7 |
| 🏛️ **周易**（义理诊断 + 起卦） | 象征 | `skills/zhouyi/` | 13 |
| 🚩 **毛选·矛盾-行动引擎** | 贯穿 | `skills/mao-thought/` | 26 |
| 🔗 **跨体系 Hub** | — | `skills/cross-system-hub/` | — |

关系、成长、行动、判断四个维度激活时，hub 查 `skills/cross-system-hub/references/behavior-dimensions.md` 选子 skill；关系安全场景格式和这四个维度的边界也在那里。用户只问其中一类单一问题时，由对应子 skill 直接触发。

**这四个维度的六本来源书**：《关系依恋》(Attached)、《依恋与亲密关系》(Hold Me Tight)、《终身成长》(Mindset)、《掌控习惯》(Atomic Habits)、《深度工作》(Deep Work)、《超预测》(Superforecasting)。运势维度的古典部分来自托勒密《四书》(Tetrabiblos)。

**两条元规则**：
1. **实事求是**：观察维度（心理、关系、成长、行动、身心）基于用户陈述的事实；判断维度只把判断改写成可检验的命题，不定主要矛盾；象征维度（塔罗、运势、周易）只提供视角与节奏，不得推翻事实，也不得单独决定"主要矛盾"
2. **内因决定**：象征为镜，行动在人——不输出确定预言，不恐吓，不推荐付费化解

## 📥 安装（给 agent 的指令）

把本仓库放进你的 agent 的 skills 目录后，**立即执行一次依赖安装**：

```bash
pip install -r requirements.txt
```

运行时若 `tools/divine.py` 输出 `[DEPENDENCY_MISSING]`，agent 应先执行上述安装命令再重试；只有在环境禁止安装时，才改为请用户粘贴排盘结果。

## 🎲 工具

`tools/divine.py`：用操作系统级随机源抽塔罗、三钱法起卦，以及八字排盘，避免模型"心算随机"或"心算排盘"。

```bash
python tools/divine.py tarot --spread three        # single | three | relation | cross
python tools/divine.py iching                      # 本卦 / 变爻 / 之卦
python tools/divine.py bazi 1996-08-12 15:20 --gender f
```

## 🧪 蒸馏记录

新增的塔罗、运势、周易起卦 skill 按 [zhengliu](https://github.com/zhangzhimiao1994/zhengliu-) 方法路线（RIA+E+B）编写，蒸馏过程见 `distill/tarot-fortune-zhengliu/`。

关系、成长、行动、判断四个维度（23 个）和托勒密古典本命（4 个）由 7 本原书蒸馏而来，同样走 RIA+E+B 路线。每本书的概览、候选、拒绝理由、术语和盲测都在 `distill/tixi-fenxi-zhengliu/books/<书>/`，总览见该目录下的 `INDEX.md` 和 `DIGEST.md`。

## 🚀 使用方式

每个 skill 目录内含 `SKILL.md` 与 `test-prompts.json`。将本仓库克隆到 OpenClaw workspace 的 `skills/` 目录下即可使用。

**目录约定**：
- 每个 skill 只在 `skills/<slug>/` 放一份，入口 skill（`psyche`、`fortune`、`mao-thought` 等）只按 slug 路由，不在自己目录下放子 skill 副本。
- frontmatter 必须是合法 YAML，并带 `name`、`description`、`version`；值里有冒号时要加引号。

改动 skill 后、提交前运行：

```bash
python tools/check_skills.py
```

脚本检查四项：有没有嵌套副本、frontmatter 是否合法、`test-prompts.json` 是否存在且有用例、`related_skills` 引用的 slug 是否存在。任何一项不过，退出码为 1。

## ⚠️ 声明

塔罗、命理与起卦的预测效力缺乏科学证据支持，本系统将其用作自我反思与叙事的框架。任何分析都不替代医疗、心理咨询、法律或财务专业意见。

## 🏷️ 版本

| Tag | 说明 |
|-----|------|
| `v3.2.1` | 删除 `tixi-fenxi`：选子 skill 的路由表、关系安全场景格式、边界并入 `cross-system-hub/references/behavior-dimensions.md` |
| `v3.2.0` | 关系、成长、行动、判断升为 hub 一级维度（6 维 → 9 维）；`tixi-fenxi` 退为内部路由；hub 安全筛查补亲密暴力 |
| `v3.1.2` | 删除 `three-kingdoms-skill`（与 `cross-system-hub` 重复），其组合链路并入 hub 参考文件第三节；写明 `freud-mourning-melancholia` / `freud-mourning-structure` 分界 |
| `v3.1.1` | 删除入口目录下 153 份子 skill 重复副本；补齐 version 与 test-prompts；修 20 个非法 YAML frontmatter；新增 `tools/check_skills.py` |
| `v3.1.0` | 新增体系分析维度（行为科学六书）与预测校准层；运势补托勒密古典本命 |
| `v3.0.0` | 体系重构：心理合并、新增塔罗/运势、毛选改为引擎 |
| `v2.0.0` | 跨体系五维分析器 v2.0 |
