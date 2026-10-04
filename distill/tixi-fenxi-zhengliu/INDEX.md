# INDEX — 体系分析 + 托勒密 原子 skill 链接图

关系类型：`depends-on`（先用它）· `composes-with`（可串联）· `contrasts-with`（易混，需分流）

## 🧩 体系分析 `skills/tixi-fenxi/`（入口：`tixi-fenxi`）

### 💞 关系体系
| skill | 用途 | 链接 |
|-------|------|------|
| `attach-style-reading` | 粗判自己/伴侣的依恋倾向（非诊断） | composes-with `attach-dating-signals` |
| `attach-dating-signals` | 约会初期分清心动和警报 | composes-with `attach-style-reading`、`attach-secure-communication` |
| `attach-anxious-avoidant-trap` | 一追一逃的结构性解法、去留判断 | depends-on `attach-style-reading`；contrasts-with `eft-demon-dialogues` |
| `attach-secure-communication` | 把具体需要说出口（五原则） | contrasts-with `eft-hold-me-tight-talk` |
| `eft-demon-dialogues` | 识别找坏人/抗议波尔卡/冻结逃跑循环 | composes-with `eft-raw-spot-deescalation` |
| `eft-raw-spot-deescalation` | 拆雷区，用七步复盘一次低谷 | depends-on `eft-demon-dialogues` |
| `eft-hold-me-tight-talk` | 说出"我最怕/我最需要"，用 A.R.E. 接住 | depends-on `eft-raw-spot-deescalation` |
| `eft-forgiving-injuries` | 依恋伤害的六步修复 | composes-with `eft-hold-me-tight-talk` |

### 🌱 成长体系
| skill | 用途 | 链接 |
|-------|------|------|
| `mindset-reaction-diagnosis` | 四个时刻的反应诊断 | 入口 |
| `mindset-trigger-reframe` | 触发点 → 改写内心独白 → 何时何地怎么做 | depends-on `mindset-reaction-diagnosis` |
| `mindset-process-praise` | 改写表扬、安慰、批评的措辞 | contrasts-with `mindset-false-growth-check` |
| `mindset-false-growth-check` | 假成长型审计 | contrasts-with `mindset-reaction-diagnosis` |

### ⚙️ 行动体系
| skill | 用途 | 链接 |
|-------|------|------|
| `habit-identity-votes` | 结果目标 → 身份 + 每日一票 | composes-with `habit-four-laws-audit` |
| `habit-four-laws-audit` | 四定律找卡住的那一环 | composes-with `habit-starter-design` |
| `habit-starter-design` | 执行意图、习惯堆叠、两分钟规则 | composes-with `habit-four-laws-audit` |
| `habit-streak-plateau` | 中断、平台期、厌倦 | depends-on `habit-starter-design` |
| `deepwork-depth-philosophy` | 四种深度哲学 + 仪式 + 4DX | composes-with `deepwork-embrace-boredom` |
| `deepwork-embrace-boredom` | 专注力训练 | depends-on `deepwork-depth-philosophy` |
| `deepwork-craftsman-tools` | 手艺人法决定工具去留 | composes-with `deepwork-embrace-boredom` |
| `deepwork-shallow-shutdown` | 浅层预算、时间块、停工仪式 | composes-with `deepwork-depth-philosophy` |

### 🎯 判断体系（预测校准层）
| skill | 用途 | 链接 |
|-------|------|------|
| `forecast-calibrate-claim` | 任何判断（含象征倾向）→ 可检验的概率命题 + 复盘日 | depends-on `forecast-fermi-baserate`；composes-with `ptolemy-fate-calibration`、`fortune` |
| `forecast-fermi-baserate` | 费米拆解 → 基率 → 内部调整 | composes-with `forecast-calibrate-claim` |
| `forecast-update-postmortem` | 小步更新 + Brier 复盘 | depends-on `forecast-calibrate-claim` |

## 🌟 运势 `skills/fortune/`（入口：`fortune`）

| skill | 用途 | 链接 |
|-------|------|------|
| `ptolemy-planet-condition` | 古典尊贵、派别、强弱 | 被另外三个 depends-on |
| `ptolemy-topic-ruler` | 卷三第 4 章五步法：职业方向与财富来源（福点） | depends-on `ptolemy-planet-condition`；contrasts-with `astrology-transit` |
| `ptolemy-mind-temperament` | 卷三第 18 章：水星 + 月亮 → 特质的高低两面 | depends-on `ptolemy-planet-condition`；contrasts-with `psyche` |
| `ptolemy-fate-calibration` | 卷一第 1-3 章：把"注定"降级为条件句 | composes-with `forecast-calibrate-claim`、`neiyin-juedinglun` |

## 跨维度接口

- `cross-system-hub` v4.3.0 起，关系、成长、行动、判断是四个一级维度（关系/成长/行动属观察层，判断属校准层）；`tixi-fenxi` 退为它们共用的内部路由，按维度选子 skill 并做关系安全筛查。C9 → `forecast-calibrate-claim`；STEP 8 → `habit-starter-design`、`forecast-calibrate-claim`
- `psyche` ⇄ 关系/成长/行动：心理维度讲成因，这三个维度讲"从哪一环下手"
- `mao-thought/maodun-fenxi` 定主要矛盾 → 主要矛盾所在的行为科学维度提供下手的具体工具
- （历史）v4.2.0 时这四类合为一个"体系分析"维度，入口是 `tixi-fenxi`
