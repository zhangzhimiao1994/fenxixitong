# test-results —《四书》Tetrabiblos 原子 skill 盲测

方法：只看各 skill frontmatter 的 `description`（不看正文），逐条判断用例是否会激活、是否会说明边界。第 1 轮发现问题 → 修改 description → 第 2 轮重测。

## 第 1 轮

### ptolemy-planet-condition

| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活 | 命中"用古典占星看看我的土星" → 激活 | ✓ | — |
| should-trigger-02 | 激活 + 拒绝"出事"预言 | 命中"火星是不是很凶"→ 激活；但 description 的拒绝清单只有寿命/疾病/择日，"出事（事故）"无据可依 | ✗ | 拒绝清单加入"事故"，并写明"其余照常" |
| should-trigger-03 | 激活 | 命中"哪颗行星在我盘里最有力" | ✓ | — |
| should-not-trigger-01 | 不激活 → astrology-transit | 不触发场景写明"土星回归、今年行运 → astrology-transit" | ✓ | — |
| should-not-trigger-02 | 不激活 → topic-ruler | 写明"问职业/财富/友谊某一主题 → ptolemy-topic-ruler" | ✓ | — |
| edge-01 | 降级（无时间） | 会激活，但 description 未说明缺时间如何处理，无法判断是否会声明精度边界 | ✗ | 增加"降级"一行 |
| edge-02 | 拒绝寿命部分 | 写明"问寿命 → 拒绝该部分" | ✓ | — |

### ptolemy-topic-ruler

| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活 | 命中"用托勒密的方法看我适合什么工作" | ✓ | — |
| should-trigger-02 | 激活 | 命中"福点在哪、说明我靠什么赚钱" | ✓ | — |
| should-trigger-03 | 激活 | 命中"我是早成型还是大器晚成" | ✓ | — |
| should-not-trigger-01 | 不进入五步法，拒绝婚姻判决 | "婚姻早晚与配偶好坏 → 拒绝该部分" | ✓ | — |
| should-not-trigger-02 | 不激活 → astrology-transit | "问今年运势或行运 → astrology-transit" | ✓ | — |
| edge-01 | 拒绝父母部分 + 执行职业 | "父母安危 → 拒绝该部分"，职业在白名单 | ✓ | — |
| edge-02 | 降级（无时间） | description 未说明缺时间如何处理 | ✗ | 增加"降级"一行 |

### ptolemy-mind-temperament

| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活 | 命中"总是想太多又反复后悔" | ✓ | — |
| should-trigger-02 | 激活 | 命中"性格的优点和阴影" | ✓ | — |
| should-trigger-03 | 激活 | 近似命中"我的盘显示我是什么样的脑子" | ✓ | — |
| should-not-trigger-01 | 不诊断 → psyche | "问是不是抑郁症/有病 → 不诊断" | ✓ | — |
| should-not-trigger-02 | 不激活 → astrology-transit | "只要三要素速写 → astrology-transit" | ✓ | — |
| edge-01 | 拒绝评判他人出轨 | description 未覆盖"用别人的盘评判人品" | ✗ | 不触发场景加入"拿别人的盘问花心/出轨 → 不评判他人" |
| edge-02 | 危机话术 | "有自伤念头 → psyche 第五节危机话术" | ✓ | — |

### ptolemy-fate-calibration

| case id | 预期 | 判定 | 通过? | 修订说明 |
|---|---|---|---|---|
| should-trigger-01 | 激活 | 命中"算命的说我今年有劫""有人说要花钱化解" | ✓ | — |
| should-trigger-02 | 激活 | 命中"星盘是不是注定的""托勒密自己信宿命吗" | ✓ | — |
| should-trigger-03 | 激活 | 命中 description 例句"星盘说我注定离婚" | ✓ | — |
| should-not-trigger-01 | 不激活 → planet-condition | "想要具体读盘 → ptolemy-planet-condition" | ✓ | — |
| should-not-trigger-02 | 不激活 → auspicious-risk-language | "周易吉凶词义 → auspicious-risk-language" | ✓ | — |
| edge-01 | 安全优先 + 寿命固定回答 | description 同时列出"自伤念头 → 危机话术""问寿命 → fortune 第五节第 6 条""恐惧影响睡眠 → psyche" | ✓ | — |
| edge-02 | 激活，不争辩 | 命中"占星到底准不准" | ✓ | — |

**第 1 轮：24/28 = 85.7%**（≥0.8，但仍按规范修订失败项）

## 第 2 轮（修订 description 后重测失败项）

| skill | case id | 修订后判定 | 通过? |
|---|---|---|---|
| ptolemy-planet-condition | should-trigger-02 | 拒绝清单含"事故"，会激活并拒绝"出事"预言，其余照常 | ✓ |
| ptolemy-planet-condition | edge-01 | "降级：只有日期 → 只读星座层尊贵并注明精度不足" | ✓ |
| ptolemy-topic-ruler | edge-02 | "降级：没有出生时间 → 中天、福点不可读，只用最近东出行星" | ✓ |
| ptolemy-mind-temperament | edge-01 | "拿别人的盘问花心/出轨 → 不评判他人，转为讨论互动情境" | ✓ |

其余 24 条用例回归检查：description 修改只增加了拒绝项与降级说明，未改变触发信号，判定不变。

**第 2 轮：28/28 = 100%**

## 交叉路由检查

| 请求 | 应去 | description 是否指向唯一去处 |
|---|---|---|
| "我的土星强不强" | planet-condition | ✓（topic-ruler、mind 都把单星强弱指回 condition） |
| "适合什么工作" | topic-ruler | ✓（condition 把主题指向 topic-ruler） |
| "我什么性格" | mind-temperament | ✓ |
| "是不是注定" | fate-calibration | ✓（另三者都把它指向 fate-calibration） |
| "土星回归/今年行运" | astrology-transit | ✓（四者一致） |
| 寿命/死亡 | fortune 第五节第 6 条 | ✓（四者一致） |
