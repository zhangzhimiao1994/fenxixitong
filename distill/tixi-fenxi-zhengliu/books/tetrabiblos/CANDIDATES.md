# CANDIDATES —《四书》Tetrabiblos

审核四条：跨语境证据 / 生成力 / 独特性 / 有边界。PAGE 为 PDF 页。
状态：approved = 成为或并入原子 skill；rejected = 见 `REJECTED.md`。

## framework（框架）

| # | 候选 | 位置 | 四条审核 | 状态 → 去向 |
|---|---|---|---|---|
| F1 | 预测的有限可能：强因/弱因 + 对冲 + 同时原因（物种、出生地、养育、习俗）+ 医生条件句 | I.1-3, PAGE 29-41；呼应 II.1 PAGE 68、III.1 PAGE 99、IV.10 PAGE 165-168 | 多处出现 ✓；能把"算命说我X年有劫"转成可行动的条件句 ✓；托勒密自身的限度论，非通用"别迷信" ✓；自带边界 ✓ | approved → `ptolemy-fate-calibration` |
| F2 | 行星状态评估：四性 → 吉凶/中性 → 昼夜派别 → 五种尊贵（庙/三分/旺/界/相位）→ 宇宙强弱（东西方、速度、顺逆）→ 盘中强弱（角/续/果） | I.4-8 PAGE 41-44；I.20-27 PAGE 56-67；III.3-4 PAGE 102-105 反复调用 | 卷一定义、卷三卷四全程调用 ✓；能对任一行星给出"顺/拧"判断 ✓；古典尊贵为本书独有结构 ✓；需写明无经验支持 ✓ | approved → `ptolemy-planet-condition` |
| F3 | 本命主题五步法：位置 → 主宰星 → 性质 → 程度 → 早晚 | III.4 PAGE 104-105；实际应用于 III.5（父母）、IV.2（财富）、IV.4（职业）、IV.7（朋友） | 卷三、卷四每章套用 ✓；可直接产出某一主题的解读 ✓；与现代宫主星法不同（强调"五种权利"计票）✓；可写明哪些主题禁用 ✓ | approved → `ptolemy-topic-ruler` |
| F4 | 心性判断：水星（理性）+ 月亮（感性）→ 其主宰星 → 星座模式 → 东西方 → 得位/失位双面特质 | III.18 PAGE 135-141；I.14 PAGE 51；I.27 PAGE 67 | 卷一的模式定义 + 卷三的完整应用 ✓；能生成"特质的高低两面 + 下一步"✓；"同一行星两种表达"是本书独特写法 ✓；须过滤道德化标签 ✓ | approved → `ptolemy-mind-temperament` |
| F5 | 世运占星：日月食的地点/时间/类别/性质四步 | II.5-9 PAGE 80-87 | 有结构但针对国家、灾害 | rejected（只作 overview） |
| F6 | 寿命推算（hyleg/prorogator、杀星、方向推运） | III.11-15 PAGE 116-128 | 无证据 + 极高伤害 | rejected |
| F7 | 时间推运：人生七期 + 时主 + 年推（profection） | IV.10 PAGE 165-170 | 七期框架为通用发展阶段描述；年推属事件择时 | 部分 approved：仅"年龄合宜检查"原则并入 `ptolemy-topic-ruler`；年推 rejected |

## principle（原则）

| # | 候选 | 位置 | 状态 → 去向 |
|---|---|---|---|
| P1 | "规则不能是确定无误的"——物质多变，只能推论 | I.1 PAGE 29；I.2 PAGE 33 | approved → fate-calibration R |
| P2 | 失误多半来自不合格从业者；有人借占星之名行别的占卜、预言不可知之事以欺骗无知者 | I.2 PAGE 33 | approved → fate-calibration E（识别"不可知断言"） |
| P3 | 天象永不精确重复 → 历史案例不可原样套用 | I.2 PAGE 33-34 | approved → fate-calibration |
| P4 | 预知的价值是事先准备，使心平稳 | I.3 PAGE 37 | approved → fate-calibration A2/E |
| P5 | 弱因可被对冲阻止；"若无阻碍"才发生 | I.3 PAGE 37-39 | approved → fate-calibration 主干 |
| P6 | 同质增强、异质削弱（热星遇热体质更强） | I.13 PAGE 50；I.26 PAGE 65-66 | approved → planet-condition（"主场/客场"） |
| P7 | 土星归昼、火星归夜：凶性被相反性质调和 | I.7 PAGE 43 | approved → planet-condition（派别 sect） |
| P8 | 和谐相位（三分、六分：同性别星座）vs 不和谐（四分、对冲） | I.16 PAGE 52-54 | approved → planet-condition |
| P9 | 星座起点取二分二至点（回归黄道），其他细分为"科学的虚荣" | I.25 PAGE 64-65 | approved → planet-condition B（不扩充细分） |
| P10 | 星与主题位置"出生时就有联系"才起作用 | III.5 PAGE 109 | approved → topic-ruler E |
| P11 | 兄弟姐妹只能"一般、粗略"地看，追求细节是徒劳 | III.6 PAGE 109 | approved → topic-ruler B（作者自己的限度） |
| P12 | 人性很少处于极端，多为适度交替；同一时期可有得有失 | IV.10 PAGE 167-168 | approved → topic-ruler / fate-calibration |
| P13 | 判断须合乎年龄与地域等"更大的先在原因" | IV.10 PAGE 165-166 | approved → topic-ruler E（年龄合宜检查） |
| P14 | 判断要靠自己 + 科学；只能给"一般概念"不能给具体形态 | 百言集 I, PAGE 181 | approved（旁证，标注作者存疑）→ fate-calibration |
| P15 | 懂行者可避开许多影响、事先准备；智者改良天象如农夫 | 百言集 V、VIII, PAGE 181 | approved（旁证）→ fate-calibration |
| P16 | 择日：只在本命允许时有用 | 百言集 VI, PAGE 181 | rejected（择日） |

## case（书中案例/应用）

| # | 候选 | 位置 | 状态 → 去向 |
|---|---|---|---|
| C1 | 农夫、牧人、水手凭经验预测天气，但常因缺知识而出错 | I.2 PAGE 31-32 | approved → fate-calibration A1 |
| C2 | 磁石遇蒜不吸铁、伤口敷药不溃烂（"对冲"类比） | I.3 PAGE 38-39 | approved → fate-calibration A1（注：蒜/磁石之说本身是错误古代信念，Ashmand 注亦引反证） |
| C3 | 埃及人把占星与医术结合，设"防护与补救" | I.3 PAGE 40-41 | approved → fate-calibration A1（改写为"现实对冲手段"） |
| C4 | 职业：水星→书写、会计、教学、商贸；金星→香料、染色、衣饰；火星→火与金属；水金合→音乐诗歌；有木星作证→更体面 | IV.4 PAGE 149-151 | approved → topic-ruler A1 |
| C5 | 财富：福点主宰星——土星靠建筑农业航海，木星靠职位信托，火星靠军职，金星靠友人与女性馈赠，水星靠学问与贸易 | IV.2 PAGE 145-146 | approved → topic-ruler A1（只取"财富来源风格"） |
| C6 | 友谊三种：自发（日月）、利益（福点）、苦乐（上升） | IV.7 PAGE 158-159 | approved → topic-ruler A1 |
| C7 | 木星得位：慷慨、虔敬；失位：挥霍、偏执（同一特质的两面） | III.18 PAGE 139 | approved → mind-temperament A1 |
| C8 | 水星得位：审慎、善学、长于论证；失位：浮躁、健忘、多变 | III.18 PAGE 141 | approved → mind-temperament A1 |
| C9 | 双体星座使心多变、多才、易后悔；固定星座使心坚定、记仇、执拗 | III.18 PAGE 136 | approved → mind-temperament |
| C10 | 父母：日、土主父，月、金主母；以"护卫星"(doryphory)看家境 | III.5 PAGE 105-106 | rejected（父母健康/寿命部分）；"家境象征"仅在用户主动问家庭背景时作叙事，不单列 |
| C11 | 地位：日月在阳性星座且在角宫、五星护卫 → 王侯 | IV.3 PAGE 146-147 | rejected（地位预言） |

## counterexample（反例 / 作者自己的反向论证）

| # | 候选 | 位置 | 状态 → 去向 |
|---|---|---|---|
| X1 | "只看天象而不顾同时原因，预判必定很不完整" | I.2 PAGE 35 | approved → fate-calibration 黑名单 |
| X2 | "因为没考虑对冲，人们才以为未来不可改变"——宿命论来自方法缺陷 | I.3 PAGE 40 | approved → fate-calibration |
| X3 | 若忽略地域等先在原因，会说出"埃塞俄比亚人白肤直发"之类荒谬判断 | IV.10 PAGE 165-166 | approved → topic-ruler（年龄/处境合宜检查） |
| X4 | Ashmand 脚注：Hemmings 与英王"同时出生、一生相似"轶事 | I.2 脚注 PAGE 34-35 | approved 作为**反例**：单一轶事 vs Dean & Kelly 时间孪生研究阴性 → fate-calibration |
| X5 | 卷二民族性格（"南方人凶猛""西方人柔弱"） | II.2 PAGE 69-70 | approved 作为黑名单反例（刻板印象）；内容 rejected |
| X6 | 心性章失位描述中的"盗贼、通奸者、渎神者"等道德标签 | III.18 PAGE 137-140 | approved 作为黑名单反例 → mind-temperament |

## glossary

见 `GLOSSARY.md`（约 30 条）。

## 统计

- framework 7（approved 4，部分 approved 1，rejected 2）
- principle 16（approved 15，rejected 1）
- case 11（approved 9，rejected 2）
- counterexample 6（全部作为反例使用，其中 X5 内容 rejected）
- 进入 `REJECTED.md` 的独立条目：19 条（含未在上表单列的卷三卷四高风险主题）
