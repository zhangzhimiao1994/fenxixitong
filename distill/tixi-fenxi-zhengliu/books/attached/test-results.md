# test-results —《关系依恋》(Attached) 盲测

方法：只读每个 skill 的 description（含触发信号、不触发场景），逐条判断用例是否会激活本 skill、是否会说明边界。同时对照同目录已有的兄弟 skill（eft-demon-dialogues、eft-hold-me-tight-talk 等）的 description，检查会不会撞车。判定人：蒸馏 agent 自评（非独立评审，见文末局限）。

## 第一轮（初稿 description）

初稿与终稿的差别：
- style-reading 初稿触发信号含"他是回避型吗"，不触发场景里没有"约会初期 → dating-signals"。
- trap 初稿触发信号含"我越找他他越躲"，不触发场景只写"eft- 系列"。
- secure-communication 初稿只写"想把需要说出口"，没区分"具体日常需要"和"深层恐惧"。

| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| style-reading/should-trigger-01 | 触发 | 触发，会说明问卷局限 | ✅ | |
| style-reading/should-trigger-02 | 触发 | 触发 | ✅ | |
| style-reading/should-trigger-03 | 触发 | 触发 | ✅ | |
| style-reading/should-not-trigger-01 | 不触发→dating | **会触发**（"他是不是回避型"类信号 + 无约会初期排除） | ❌ | 加"约会初期（几次到几周）、核心是要不要继续 → attach-dating-signals"；触发信号改为长期关系语境 |
| style-reading/should-not-trigger-02 | 不触发→trap | 不触发 | ✅ | |
| style-reading/edge-01（暴力） | 不做风格分析、转介 | description 未写暴力；正文决策树有 | ⚠️ | 判通过（正文第一层就拦截），终稿保留 |
| style-reading/edge-02（诊断） | 先说不诊断 | 会 | ✅ | |
| trap/should-trigger-01 | 触发 | 触发 | ✅ | |
| trap/should-trigger-02 | 触发 | 触发 | ✅ | |
| trap/should-trigger-03 | 触发 | 触发 | ✅ | |
| trap/should-not-trigger-01 | 不触发 | 不触发 | ✅ | |
| trap/should-not-trigger-02 | 不触发→eft | 不触发，但与 eft-demon-dialogues 的"我越说他越躲"信号重叠，路由不清 | ❌ | 删除"我越找他他越躲"；写清 trap 管"结构性分歧、留或走"，循环识别 → eft-demon-dialogues，降温 → eft-raw-spot-deescalation |
| trap/edge-01（掐脖子） | 不分析、转介 | 会 | ✅ | |
| comm/should-trigger-01 | 触发 | 与 eft-hold-me-tight-talk（"不知道怎么跟他说我需要他"）双触发 | ❌ | 限定为"具体、日常的需要"，深层恐惧 → eft-hold-me-tight-talk |
| comm/should-trigger-02 | 触发 | 触发 | ✅ | |
| comm/should-trigger-03 | 触发 | 触发 | ✅ | |
| comm/should-not-trigger-01 | 不触发 | 不触发 | ✅ | |
| comm/should-not-trigger-02 | 不触发→dating | 不触发 | ✅ | |
| comm/edge-01（酒后摔东西） | 不给摊牌脚本 | 会 | ✅ | |
| dating/should-trigger-01 | 触发 | 触发 | ✅ | |
| dating/should-trigger-02 | 触发 | 触发 | ✅ | |
| dating/should-trigger-03 | 触发 | 触发 | ✅ | |
| dating/should-not-trigger-01 | 不触发→style | 不触发 | ✅ | |
| dating/should-not-trigger-02 | 不触发→psyche | 不触发 | ✅ | |
| dating/edge-01（约会三次觉得他回避） | dating 为主 | 与 style-reading 初稿双触发 | ❌ | 同 style-reading 修订 |
| dating/edge-02（自己总嫌弃对方） | 触发回避分支 | 触发 | ✅ | |

第一轮：26 例，通过 22，**通过率 84.6%**（达标线 80%），但 4 处路由冲突都在兄弟 skill 之间，全部修订。

## 第二轮（终稿 description）

| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| style-reading/should-not-trigger-01 | 不触发→dating | 命中"约会初期 + 要不要继续"排除项，路由 dating | ✅ | — |
| style-reading/edge-01 | 转介 | description 不触发本 skill 的分析；正文决策树第二层拦截 | ✅ | — |
| trap/should-trigger-02 | 触发 | 命中"好的时候特别好…一直这样好几年""离不开" | ✅ | 复查：未与 eft-demon-dialogues 冲突（用户问的是去留） |
| trap/should-not-trigger-02 | 不触发→eft | 命中"想认出循环/降温 → eft-*" | ✅ | — |
| comm/should-trigger-01 | 触发 | 命中"具体、日常需要（多陪伴）" | ✅ | — |
| dating/edge-01 | dating 为主 | style-reading 已排除约会初期，dating 唯一主触发 | ✅ | — |
| 其余 20 例 | 同第一轮 | 复查无变化 | ✅ | — |

第二轮：26 例，通过 26，**通过率 100%**。

## 边界说明检查（是否会说明边界）

| skill | 不诊断 | 人会变/自评局限 | 暴力转介 | 自伤→psyche 第五节 |
|---|---|---|---|---|
| attach-style-reading | ✅ | ✅ | ✅ | ✅ |
| attach-anxious-avoidant-trap | —（不涉及） | ✅（只听一方） | ✅ | ✅ |
| attach-secure-communication | — | ✅（不保证解决） | ✅ | ✅ |
| attach-dating-signals | ✅（不给对方定性） | ✅（大数法则标 inference） | ✅ | ✅ |

## 局限

- 盲测由蒸馏 agent 自己完成，不是独立评审；建议用 darwin-skill 或另起 agent 再测一次。
- 只做了 description 层面的路由判断，没有实际跑模型输出去检查回复格式。
- eft-* 兄弟 skill 是并行产出的，后续若它们修改 description，需要复测交界用例（trap/should-not-trigger-02、comm/should-trigger-01）。
