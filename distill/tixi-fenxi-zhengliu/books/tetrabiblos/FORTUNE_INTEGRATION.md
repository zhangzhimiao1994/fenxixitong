# FORTUNE_INTEGRATION — 托勒密 4 个原子 skill 接入 fortune 维度的建议

> 本文件只是建议，**未修改** `skills/fortune/SKILL.md`。由维护者决定是否合入。

## 一、新增 skill 一览（均在 `skills/fortune/` 下）

| slug | 一句话用途 | 依赖 |
|---|---|---|
| `ptolemy-planet-condition` | 古典尊贵 + 昼夜派别 + 强弱，判断某颗行星"在主场还是客场" | 工具 `divine.py astro` |
| `ptolemy-topic-ruler` | 卷三第 4 章五步法，只用于职业方向与财富来源风格（福点） | condition |
| `ptolemy-mind-temperament` | 卷三第 18 章：水星 + 月亮 + 主宰星 → 特质的高/低两面 | condition |
| `ptolemy-fate-calibration` | 卷一第 1-3 章：把"注定/有劫"断言降级为条件句 + 现代证据 + 现实准备 | 无需出生数据 |

## 二、建议加入第一节"方法路由"表的行

在现有"出生年月日 + 时间 + 地点 | 西方星盘 | astrology-transit"一行**之后**插入：

| 用户已有/愿提供 | 首选方法 | 子 skill | 擅长回答 |
|---|---|---|---|
| 出生年月日 + 时间 + 地点，且说"古典/托勒密/入庙/吉星凶星" | 古典本命（托勒密） | `ptolemy-planet-condition` | 哪颗行星有力、某颗星状态顺不顺 |
| 同上 + 问职业方向或"靠什么赚钱" | 古典本命主题法 | `ptolemy-topic-ruler` | 职业发言人、财富来源风格、早显/晚成 |
| 同上 + 问性格、思维与情绪风格（古典） | 古典心性 | `ptolemy-mind-temperament` | 特质的高低两面 |
| 不需要出生信息：手里有一句别人给的预言，或问"是不是注定/准不准" | 预测校准 | `ptolemy-fate-calibration` | 断言拆解、条件句改写、欺诈标记 |

## 三、建议的"信号 → 路由"补充表（可放在第一节表格下方）

| 用户信号（原话式） | 路由 | 备注 |
|---|---|---|
| "托勒密怎么看""古典占星""入庙/入旺/落陷""吉星凶星" | `ptolemy-planet-condition` | 无时间 → 只读星座层 |
| "我的土星/火星是不是很凶" | `ptolemy-planet-condition` | 同时执行第三节转换表 |
| "用古典方法看我适合什么工作""中天说明什么""福点" | `ptolemy-topic-ruler` | 只做白名单主题 |
| "大器晚成还是少年得志" | `ptolemy-topic-ruler` | 只谈象征节奏 |
| "古典占星看我性格""水星月亮说明什么""优点和阴影" | `ptolemy-mind-temperament` | 诊断请求先走 psyche 第五节第 2 条 |
| "算命的说我 X 年有劫""注定离婚""要花钱化解" | `ptolemy-fate-calibration` | 付费化解 → 第五节第 4 条固定回答 |
| "星盘/八字是不是注定的""占星准不准" | `ptolemy-fate-calibration` | 适用于八字、紫微断语的校准，不限于星盘 |
| "土星回归""今年行运""水逆" | `astrology-transit`（不变） | 现代行运与古典结构可串联：先 condition/topic-ruler 读结构，再交 transit |
| 托勒密体系下问寿命、死亡、父母安危、子女、婚姻判决、地位、旅行凶险、心智疾病 | 第〇节第 0 步 🛑 拒绝该部分 | 详见 `distill/.../tetrabiblos/REJECTED.md` R1-R14 |

## 四、与第五节"边界"的接口

- 第五节第 3 条"宿命焦虑 → psyche"之前，可先插入一步：**断言型焦虑**（用户带着具体预言）→ `ptolemy-fate-calibration` 给 1 段校准；情绪持续 → 再转 `psyche`。
- 第五节第 1 条"科学证据"可补一条时间孪生研究：Dean & Kelly (2003, *Journal of Consciousness Studies*)，与 Carlson (1985) 并列。

## 五、建议补入第三节"语言转换表"的行

| 托勒密原话 | 输出时改为 |
|---|---|
| 凶星 (malefic) | 张力型行星（土星偏收缩迟滞，火星偏冲动切割） |
| 吉星 (benefic) | 滋养型行星 |
| 落 (fall) / 失位 (inglorious) | 逆风 / 条件差时的表达 |
| 得位 (in glory) | 条件好时的表达 |
| 失效、无力 | 不太显现 |
| 短命、夭折、杀星 (anaretic) | **禁止使用** |

## 六、frontmatter 建议

`fortune` 的 `related_skills` 可追加：`ptolemy-planet-condition, ptolemy-topic-ruler, ptolemy-mind-temperament, ptolemy-fate-calibration`。

## 七、与现有 astrology-transit 的分工说明

- `astrology-transit` 的 `source_book` 已写托勒密传统框架，但内容是现代三要素 + 行运周期；托勒密 4 件套补的是**古典本命结构**（尊贵、主宰星、心性两面）和**预测限度论**。
- 两者都用 `tools/divine.py astro`（回归黄道 + 整宫制），数据口径一致；托勒密件套额外说明工具不提供中天精确度数、逆行与界。
- 互不重复的约定：凡涉及"当前/今年/周期"一律归 transit；凡涉及"结构/古典规则/限度"归 ptolemy-*。
