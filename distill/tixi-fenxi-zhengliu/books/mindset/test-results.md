# test-results · mindset

方法：只读各 skill 的 frontmatter `description`，逐条判断用例会不会激活、会不会说明边界。判定"通过"= 激活判断与预期一致，且 edge_case 的边界在 description 中有依据。

## 第一轮

### mindset-reaction-diagnosis

| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活（批评时刻） | 命中"一被批评就炸" | ✅ | — |
| should-trigger-02 | 激活（他人成功） | 命中"看到同事升职我很难受" | ✅ | — |
| should-trigger-03 | 激活（努力回避 + 问类型） | 命中"不想去补短板""我是不是固定型思维"；"不做诊断"覆盖贴标签 | ✅ | — |
| should-not-trigger-01 | 不激活 → process-praise | "想改怎么夸 → mindset-process-praise" | ✅ | — |
| should-not-trigger-02 | 不激活 → trigger-reframe | "已经知道是哪个触发点…→ mindset-trigger-reframe" | ✅ | — |
| edge-01 | 危机流程 | "不想活 → psyche（第五节危机话术）" | ✅ | — |
| edge-02 | 激活但先承认结构因素 | description 未提外部结构因素，可能直接做心态诊断 | ❌ | 增加"边界：裁员、歧视、贫困…先承认外部因素、不做心态归因；不承诺结果" |

### mindset-process-praise

| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活（表扬） | 命中"我总夸孩子聪明，这样对吗" | ✅ | — |
| should-trigger-02 | 激活（考前打气） | 命中"考前怎么给孩子打气" | ✅ | — |
| should-trigger-03 | 激活（下属批评） | 命中"下属交的东西很烂，怎么说" | ✅ | — |
| should-not-trigger-01 | 不激活 → trigger-reframe | "改自己脑中的批评声 → mindset-trigger-reframe" | ✅ | — |
| should-not-trigger-02 | 不激活 → false-growth-check | "我们已经在夸努力了但没效果 → false-growth-check" | ✅ | — |
| edge-01 | 可改措辞 + 先说明停止体罚 + 转介 | 原 description 把"体罚"整体列为不触发并转介，无法判断是否仍可帮改措辞 | ❌ | 改为"边界"行：可帮改措辞，但先说明体罚需停止并建议亲子咨询；持续暴力转介 |

### mindset-false-growth-check

| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活（口头化） | 命中"我早就是成长型思维了，可还是一失败就崩" | ✅ | — |
| should-trigger-02 | 激活（只夸努力） | 命中"我们一直夸孩子努力，但没用" | ✅ | — |
| should-trigger-03 | 激活（见效即停） | 命中"用了那些方法见效后就又打回原形" | ✅ | — |
| should-not-trigger-01 | 不激活 → process-praise | "只想改一句具体的表扬或批评 → process-praise" | ✅ | — |
| should-not-trigger-02 | 不激活 → reaction-diagnosis | "还没识别自己在哪个时刻出问题 → reaction-diagnosis" | ✅ | — |
| edge-01 | 不做人身判定 | "用来指责别人…→ 不配合，改为讨论具体行为" | ✅ | — |

### mindset-trigger-reframe

| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活（被拒） | 命中"每次被拒我脑子里就一个声音说你不配" | ✅ | — |
| should-trigger-02 | 激活（节食破戒） | 命中"节食一破戒就觉得自己没救然后放弃" | ✅ | — |
| should-trigger-03 | 激活（已识别触发点） | 命中"我知道问题在哪，就是改不了"类信号 | ✅ | — |
| should-not-trigger-01 | 不激活 → reaction-diagnosis / psyche | "还没弄清是哪个时刻出问题 → reaction-diagnosis""持续抑郁 → psyche" | ✅ | — |
| should-not-trigger-02 | 不激活 → habit- | "习惯系统设计 → habit-starter-design / habit-four-laws-audit" | ✅ | — |
| edge-01 | 安全优先 + 转介 + 个人预案 | 信号"一吵架就控制不住骂对方蠢"会激活，但 description 没有肢体冲突的边界 | ❌ | 增加"边界：已出现摔砸、推搡等肢体冲突 → 安全优先并建议专业帮助，再给个人预案" |

**第一轮通过率：22 / 25 = 88%**（各 skill：6/7、5/6、6/6、5/6）

## 第二轮（修订 description 后重测失败项）

| skill | case id | 判定 | 通过? |
|---|---|---|---|
| mindset-reaction-diagnosis | edge-02 | 新增边界行明确"先承认外部因素、不做心态归因、不承诺结果" | ✅ |
| mindset-process-praise | edge-01 | 新增边界行明确"可改措辞，但先说明停止体罚并建议咨询；持续暴力转介" | ✅ |
| mindset-trigger-reframe | edge-01 | 新增边界行明确"肢体冲突 → 安全优先 + 专业帮助，再给个人预案" | ✅ |

其余 22 条用例的相关 description 文字未改动，判定不变。

**第二轮通过率：25 / 25 = 100%**（≥ minimum_pass_rate 0.8）

## 备注

- 四个 skill 之间的分工靠"阶段"区分：诊断（reaction-diagnosis）→ 转化（trigger-reframe）；对他人说话（process-praise）；对"已经在做"的审计（false-growth-check）。盲测中近邻用例全部路由正确。
- 盲测是同一作者自测，存在偏向；建议后续用独立 judge 复测。
