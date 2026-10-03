# test-results —《掌控习惯》原子 skill 盲测

方法：只看各 SKILL.md 的 `description`（触发信号 + 不触发场景），逐条判断用例是否会激活本 skill、是否会说明边界；不参考正文。四个 skill 互相作为近邻，同时参照 deepwork-depth-philosophy、deepwork-embrace-boredom、mindset-reaction-diagnosis 的 description 判断分流。

## 第一轮（初版 description）

### habit-identity-votes
| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活 | 命中"减下来又胖回去了" → 激活 | ✅ | — |
| should-trigger-02 | 激活 | 命中"我就不是早起的人"；作息不是能力问题，不会被 mindset 抢走 | ✅ | — |
| should-trigger-03 | 激活 | 命中"想成为能写作的人但总觉得自己不是" + "全靠意志力" | ✅ | — |
| should-not-trigger-01 | 不激活 → mindset-reaction-diagnosis | 不触发场景写明"失败后觉得自己是废物 → mindset-reaction-diagnosis" | ✅ | — |
| should-not-trigger-02 | 不激活 → habit-four-laws-audit | 写明"具体卡在哪一环（没动力、没成就感）→ four-laws" | ✅ | — |
| edge-01 | 可激活（身份过紧）+ 边界 | description 没有角色转型信号，只有"我是谁 → psyche"，盲判会直接分给 psyche | ❌ | 增加触发"退役/转岗后不知道自己还算什么人"；psyche 分流改为"存在性困惑、角色丧失后持续低落" |
| edge-02 | 不给方案，转介 | 写明"成瘾、进食障碍 → 转介" | ✅ | — |

### habit-four-laws-audit
| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活 | 命中"戒不掉睡前刷手机" | ✅ | — |
| should-trigger-02 | 激活 | 命中"一回家就瘫沙发" | ✅ | — |
| should-trigger-03 | 激活 | 命中"明明知道不好还是忍不住" | ✅ | — |
| should-not-trigger-01 | 不激活 → deepwork-embrace-boredom | 写明"坐下来专注不住、一无聊就掏手机 → deepwork-embrace-boredom" | ✅ | — |
| should-not-trigger-02 | 不激活 → habit-starter-design | 写明"还没开始 → starter" | ✅ | — |
| edge-01 | 可激活 + 成瘾边界 | 初版写"物质成瘾 → 转介"，盲判会对吸烟完全不激活，与"可补环境视角 + 转介"的预期不符 | ❌ | 改为"以转介为主（如习惯性吸烟，可只补'情境即提示'视角并建议戒烟门诊）" |
| edge-02 | 不操控伴侣，转 eft- | 写明"伴侣的习惯引发冲突 → eft-" | ✅ | — |

### habit-starter-design
| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活 | 命中"想养成读书习惯但一直没开始" | ✅ | — |
| should-trigger-02 | 激活 | 命中"定了每天跑 5 公里三天就放弃"（未建立，不算 streak 的"断了"） | ✅ | — |
| should-trigger-03 | 激活 | 命中"每次计划都很完美就是不动" | ✅ | — |
| should-not-trigger-01 | 不激活 → deepwork-depth-philosophy | 写明"写论文/写书的整块时段 → deepwork-depth-philosophy" | ✅ | — |
| should-not-trigger-02 | 不激活 → habit-streak-plateau | 写明"断了、没效果、做腻了 → streak" | ✅ | — |
| edge-01 | 激活 + 承认结构约束 | 会激活，但 description 未提示无固定作息时如何处理，无法判断会说明边界 | ❌ | 增加触发"三班倒没有固定时间"及处理提示（随班次的锚点或每周固定时点） |

### habit-streak-plateau
| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活（中断型） | 命中"断了一周就不想再捡起来""打卡断了就全盘放弃" | ✅ | — |
| should-trigger-02 | 激活（无效型） | 命中"坚持一个月了体重一点没变" | ✅ | — |
| should-trigger-03 | 激活（厌倦型） | 命中"每天都一样，越来越没劲""要不要换个方法重新来" | ✅ | — |
| should-not-trigger-01 | 不激活 → starter | 写明"习惯还没开始 → starter" | ✅ | — |
| should-not-trigger-02 | 不激活 → mindset-reaction-diagnosis | 写明"一失败就觉得自己不行的信念 → mindset-reaction-diagnosis"；"天赋"一词指向能力信念 | ✅ | — |
| edge-01 | 叫停极端节食 + 转介 | 会以"平台期"激活，但 description 无极端节食边界 | ❌ | 增加"为冲平台期打算极端节食、过度运动 → 先叫停，建议医生/营养师，有催吐迹象则转介" |
| edge-02 | 不硬推，建议专业评估 | 写明"情绪低落持续两周以上 → psyche 并建议专业帮助" | ✅ | — |

**第一轮通过率**：23 / 27 = **85.2%**（identity 6/7，four-laws 6/7，starter 5/6，streak 6/7；4 个 edge_case 未通过，均为 description 缺少边界信号）。

## 第二轮（修订后 description）

| skill | 重测用例 | 判定 | 通过? |
|---|---|---|---|
| habit-identity-votes | edge-01 | 命中新增"退役/转岗后不知道自己还算什么人" → 激活；"角色丧失后持续低落 → psyche"提供边界 | ✅ |
| habit-four-laws-audit | edge-01 | "以转介为主，习惯性吸烟可只补环境视角并建议戒烟门诊" → 部分激活并说明边界 | ✅ |
| habit-starter-design | edge-01 | 命中"三班倒没有固定时间"，并带出随班次锚点的处理 | ✅ |
| habit-streak-plateau | edge-01 | 命中极端节食边界 → 先叫停并转介 | ✅ |

其余 23 条用例与修订无关，复核判定不变。

**第二轮通过率**：27 / 27 = **100%**（每个 skill 均 ≥ minimum_pass_rate 0.8）。

## 残余风险（盲测发现但未完全消除）

1. "刷手机"同时出现在 habit-four-laws-audit 与 deepwork-embrace-boredom：分界依赖"固定生活场景（床上、沙发）"与"工作/学习中分心"的区分；用户只说"刷手机停不下来"时可能需要一个澄清问题。
2. "第三天就放弃"（starter）与"断了一周"（streak）靠"习惯是否已建立"区分；用户没说持续时长时，应先问做了多少次。
3. 盲测由蒸馏者本人执行，存在知情偏差；建议后续用 darwin-skill 的独立评审复测。
