# test-results — 《深度工作》4 个原子 skill 盲测

方法：只读各 SKILL.md frontmatter 的 description（不看正文），逐条判断用例会不会激活、该路由到哪里、会不会说明边界。判定"通过"= 激活/不激活的判断与预期一致，且 edge_case 能从 description 读出应说明的边界。
第一轮发现 3 条不通过，修改对应 description 后第二轮重测。

## 第一轮

### deepwork-depth-philosophy

| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活（节奏式） | "论文整块时间总被切碎"命中触发信号 → 激活 | ✅ | — |
| should-trigger-02 | 激活（双峰式） | 命中"要不要干脆闭关几天" → 激活 | ✅ | — |
| should-trigger-03 | 激活（4DX） | 命中"想记录深度工作时长但坚持不下去" → 激活 | ✅ | — |
| should-not-trigger-01 | 不激活 → habit- | 不触发场景写明一般日常习惯 → habit-starter-design | ✅ | — |
| should-not-trigger-02 | 不激活 → embrace-boredom | 不触发场景写明"坐下来也专注不住" → 兄弟 skill | ✅ | — |
| edge-01 | 激活 + 特异性检查 | description 写明高管角色先说明可能不适用 | ✅ | — |
| edge-02 | 不加码排程，劝降量就医 | description 只写"情绪耗竭 → psyche"，读不出"长期少睡、身心不适时不再加排深度时段"，判定可能照常给排程 | ❌ | 在不触发场景加入"为赶进度长期少睡、出现心慌失眠等身心不适 → 先劝降量与就医，不再加排深度时段" |

### deepwork-embrace-boredom

| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活 | 命中"写着写着就去搜别的东西""一无聊就忍不住刷手机" | ✅ | — |
| should-trigger-02 | 激活 | 命中"排队等人都要掏手机""想练练专注力" | ✅ | — |
| should-trigger-03 | 激活 | "能不能练专注"+ description 中的在线/离线分块 → 激活 | ✅ | — |
| should-not-trigger-01 | 不激活 → craftsman-tools | 不触发场景写明 App 去留 → craftsman-tools | ✅ | — |
| should-not-trigger-02 | 不激活 → habit-four-laws-audit | 不触发场景写明具体坏习惯机制设计 → habit-four-laws-audit | ✅ | — |
| edge-01 | 不诊断，建议评估 | description 写明问 ADHD 不做诊断、建议专业评估 | ✅ | — |

### deepwork-craftsman-tools

| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活 | 命中"要不要退出朋友圈/微博" | ✅ | — |
| should-trigger-02 | 激活 | 命中"做自媒体是不是一定要开账号" | ✅ | — |
| should-trigger-03 | 激活（规划闲暇） | 命中"下班后时间都被刷没了" | ✅ | — |
| should-not-trigger-01 | 不激活（强制工具） | 不触发场景写明工作必需工具 → embrace-boredom | ✅ | — |
| should-not-trigger-02 | 不激活 → psyche | 不触发场景写明比较焦虑、自我否定 → psyche | ✅ | — |
| edge-01 | 激活 + 指出新生/新城市例外 | description 未提翻转处境，判定可能直接给"删除"倾向 | ❌ | 在 description 主句后加入"正在大量结识新人（新生、刚到新城市）、与家人长期异地或靠线上曝光谋生时，结论可能是保留并限时段" |

### deepwork-shallow-shutdown

| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活 | 命中"一天开了五个会，正事一点没动" | ✅ | — |
| should-trigger-02 | 激活（停工仪式） | 命中"晚上躺床上还在想工作" | ✅ | — |
| should-trigger-03 | 激活（时间块） | 命中"想做时间块但总被打乱" | ✅ | — |
| should-not-trigger-01 | 不激活 → depth-philosophy | 不触发场景写明闭关/固定时段选择 → depth-philosophy | ✅ | — |
| should-not-trigger-02 | 仅个人层面 | 不触发场景写明组织制度改造只给个人做法 | ✅ | — |
| edge-01 | 说明入门级应推迟预算谈话 | description 未提入门级例外，判定可能直接建议找老板谈 | ❌ | 在不触发场景加入"入门级或完全由他人派活的岗位 → 可激活，但先只用停工仪式和轻量时间块，暂不建议找老板谈浅层预算" |

**第一轮通过率：22 / 25 = 88%**（已高于 0.8 门槛，但按规范仍修订不通过项）

## 第二轮（修订 description 后重测）

| skill | case id | 判定 | 通过? |
|---|---|---|---|
| deepwork-depth-philosophy | edge-02 | 新 description 明确：长期少睡、心慌失眠 → 劝降量与就医，不再加排 | ✅ |
| deepwork-craftsman-tools | edge-01 | 新 description 明确：新生、刚到新城市 → 可能保留并限时段 | ✅ |
| deepwork-shallow-shutdown | edge-01 | 新 description 明确：入门级先用停工仪式与轻量时间块，暂不谈预算 | ✅ |
| 其余 22 条 | — | 修订只增加边界说明，未改动触发信号，复核仍通过 | ✅ |

**第二轮通过率：25 / 25 = 100%**

## 交叉路由检查（与兄弟 skill description 对照）

| 近邻请求 | deepwork 侧路由 | 兄弟 skill 侧路由 | 一致? |
|---|---|---|---|
| "戒不掉睡前刷手机" | embrace-boredom 不触发 → habit-four-laws-audit | habit-four-laws-audit 触发信号含此句 | ✅ |
| "坐下来专注不住、一无聊就掏手机" | embrace-boredom 触发 | habit-four-laws-audit 不触发 → deepwork-embrace-boredom | ✅ |
| "深度工作时长记录坚持不下去" | depth-philosophy 触发 | habit-streak-plateau 不触发 → deepwork-depth-philosophy | ✅ |
| "写论文的整块时段怎么排、开工前磨蹭" | depth-philosophy 触发 | habit-starter-design 不触发 → deepwork-depth-philosophy | ✅ |
| "纠结要不要卸载某个 App" | craftsman-tools 触发 | habit-four-laws-audit 不触发 → deepwork-craftsman-tools | ✅ |

## 局限

- 盲测由同一蒸馏者执行，只能检验 description 的自洽与路由清晰度，不能替代独立评审或真实用户对话测试。
- 未测试中英混杂、极短提问（如"怎么专注"）等模糊输入；这类请求可能同时命中 embrace-boredom 与 depth-philosophy，需要 hub 层再加一句澄清问题。
