---
name: three-kingdoms
version: 1.0.0
description: |
  三大经典智慧系统整合（毛泽东选集 + 黄帝内经 + 周易）。
  55 个子 skill，覆盖战略决策、身心调节、局势判断三大维度。
  自动路由，无需手动指定子 skill。

  毛泽东（25 skill）：复杂决策、竞争战略、组织管理、多任务平衡
  黄帝内经（22 skill）：身心健康、情绪管理、系统调节、季节适应
  周易（8+4 skill）：处境判断、进退时机、冲突处理、关系诊断

  触发词：
  - 毛泽东系：矛盾、优先级、冲突、实事求是、调查、群众路线、团队、弹钢琴、阶段、转折、根据地、集中兵力、持久战、不对称、统一战线
  - 黄帝内经系：身体、情绪、累、虚、上火、换季、饮食、失衡
  - 周易系：进退两难、该不该、时机、关系、冲突处理、转折点、危机

  NOT trigger: 纯技术问题（代码 bug、服务器故障）、简单问答（天气查询、价格查询）、紧急危机需立即行动

not_trigger: |
  纯技术故障排查、单一事实查询、紧急生命安全危机、闲聊无关话题、纯娱乐性对话
---

# 三大经典 → 55 个思维 Skill

> 毛泽东选集 1-5 卷 + 黄帝内经（素问+灵枢）+ 周易 → 一个统一入口

当用户的问题落入以下三个维度时自动激活：

## 🔴 STEP 0：问题分类

```
用户问题 → 哪个维度？
├─ 战略/决策/竞争/组织/团队 → 毛泽东（mao-thought/）
├─ 身体/情绪/系统调节/季节/饮食 → 黄帝内经（huangdi-neijing/）
├─ 处境判断/进退时机/关系/冲突/危机 → 周易（zhouyi/）
└─ 跨维度 → 组合使用
```

---

## 毛泽东选集 25 skill（mao-thought/）

### 认知与认识论
| # | 子 skill | 目录 | 一句话 | 何时触发 |
|---|---------|------|--------|---------|
| 1 | 实践认识论 | `mao-thought/shijian-renshilun/` | 实践→认识→再实践的螺旋认知循环 | "怎么验证我的想法对不对" |
| 2 | 实事求是四高 | `mao-thought/shishiqiushi-sigao/` | 去粗取精、去伪存真的信息加工法 | "信息太多怎么提炼" |
| 3 | 矛盾分析法 | `mao-thought/maodun-fenxi/` | 从多矛盾中找到主要矛盾的瓶颈识别 | "多个问题交织不知道根在哪" |
| 4 | 矛盾特殊性 | `mao-thought/maodun-techuxing/` | 不同性质问题用不同方法 | "别人的方法在我这不灵" |
| 5 | 内因决定论 | `mao-thought/neiyin-juedinglun/` | 外因通过内因起作用 | "是我问题还是环境问题" |
| 6 | 两类矛盾 | `mao-thought/lianglei-maodun/` | 对抗性 vs 非对抗性冲突分级 | "跟这人是敌是友" |

### 调查与信息
| # | 子 skill | 目录 | 一句话 | 何时触发 |
|---|---------|------|--------|---------|
| 7 | 调查研究 | `mao-thought/diaocha-yanjiu/` | 没有调查就没有发言权 | "信息不足不敢下判断" |
| 8 | 群众路线 | `mao-thought/qunzhong-luxian/` | 从群众中来到群众中去 | "方案推不下去""不知道真实情况" |

### 竞争战略
| # | 子 skill | 目录 | 一句话 | 何时触发 |
|---|---------|------|--------|---------|
| 9 | 持久战三阶段 | `mao-thought/chijiuzhan-san-jieduan/` | 防御→相持→反攻 | "我该守还是该攻" |
| 10 | 不对称战略 | `mao-thought/buduicheng-zhanlue/` | 弱者重新定义竞争范式 | "对方比我强太多怎么打" |
| 11 | 星星之火根据地 | `mao-thought/xingxingzhihuo-genjudi/` | 边缘突破→根据地的路径规划 | "从零开始怎么破局" |
| 12 | 集中优势兵力 | `mao-thought/jianmiezhan-jizhong-bingli/` | 在关键局部集中绝对优势 | "资源有限怎么分配" |
| 13 | 十六字诀 | `mao-thought/shiliuzijue/` | 敌进我退、敌驻我扰的竞争节奏 | "对手步步紧逼怎么办" |
| 14 | 战略战术辩证法 | `mao-thought/zhanlue-zhanshu-bianzheng/` | 宏观被动中制造微观主动 | "整体下风但局部有机会" |
| 15 | 统一战线独立自主 | `mao-thought/tongyi-zhanxian-duli/` | 合作中保持独立 | "怎么合作又不被吃掉" |

### 心态与行动
| # | 子 skill | 目录 | 一句话 | 何时触发 |
|---|---------|------|--------|---------|
| 16 | 战略藐视战术重视 | `mao-thought/zhanlue-miaoshi-zhanshu-zhongshi/` | 心态不怕 + 行动认真 | "压力太大不敢行动" |
| 17 | 在战争中学习战争 | `mao-thought/cong-zhanzheng-xuexi-zhanzheng/` | 干起来再学 | "没准备好不敢开始" |
| 18 | 放下包袱开动机器 | `mao-thought/fangxia-baofu-kaidong-jiqi/` | 卸掉认知包袱 + 深度思考 | "脑子里太多事转不动" |
| 19 | 主动性灵活性计划性 | `mao-thought/zhudongxing-linghuoxing-jihuaxing/` | 执行力三要素平衡 | "计划总被打乱" |

### 组织与管理
| # | 子 skill | 目录 | 一句话 | 何时触发 |
|---|---------|------|--------|---------|
| 20 | 惩前毖后治病救人 | `mao-thought/chengqianbihou-zhibing-jiuren/` | 揭发错误 + 帮助改正 | "有人犯错怎么处理" |
| 21 | 组织纠偏诊断 | `mao-thought/zuzhi-jiupian-zhenduan/` | 表现→根源→处方的组织诊断 | "团队文化出问题了" |
| 22 | 一般号召个别指导 | `mao-thought/yiban-gebie-zhidao/` | 先试点再推广 | "新方案怎么推" |
| 23 | 弹钢琴 | `mao-thought/tan-gangqin/` | 中心工作与全面的节奏管理 | "多任务忙不过来" |
| 24 | 辩证平衡 | `mao-thought/bianzheng-pingheng/` | 多目标动态平衡 | "短期长期怎么兼顾" |
| 25 | 有效沟通问题解决 | `mao-thought/youxiao-goutong-wenti-jiuej/` | 反八股 + 四步法 | "沟通效率低" |

---

## 黄帝内经 22 skill（huangdi-neijing/）

### 素问：宏观系统篇（12 个）
| # | 子 skill | 目录 | 一句话 | 何时触发 |
|---|---------|------|--------|---------|
| 26 | 阴阳平衡 | `huangdi-neijing/yin-yang-balance/` | 系统失衡的对立面诊断 | "感觉整个人被掏空了" |
| 27 | 五行网络 | `huangdi-neijing/five-elements-network/` | 多要素连锁效应分析 | "问题会引发什么连锁反应" |
| 28 | 负反馈制衡 | `huangdi-neijing/negative-feedback/` | 亢盛时引入制衡 | "越用力越糟糕" |
| 29 | 标本先后 | `huangdi-neijing/biao-ben-priority/` | 表症与根源的优先级 | "小事做了一堆，大事没推动" |
| 30 | 正邪评估 | `huangdi-neijing/zheng-xie-assessment/` | 自身能力 vs 外部压力 | "我是能力不够还是负担太重" |
| 31 | 因地制宜 | `huangdi-neijing/context-adaptation/` | 方案在新环境中的适配 | "为什么换个地方就不灵了" |
| 32 | 治未病 | `huangdi-neijing/prevention-strategy/` | 问题爆发前的预防 | "怎么提前防范风险" |
| 33 | 传变预测 | `huangdi-neijing/cascade-prediction/` | 局部问题如何扩散到全局 | "这个问题会引发其他问题吗" |
| 34 | 四季调神 | `huangdi-neijing/seasonal-regimen/` | 根据季节调整作息饮食 | "换季了身体不对劲" |
| 35 | 五味调和 | `huangdi-neijing/five-flavors-balance/` | 饮食偏好的平衡调节 | "特别想吃某种味道停不下来" |
| 36 | 情绪-脏腑代理 | `huangdi-neijing/emotion-organ-proxy/` | 情绪对身体的影响 | "最近一直焦虑身体也不舒服" |
| 37 | 司外揣内 | `huangdi-neijing/observation-inference/` | 从信号推断内部状态 | "几个信号互相矛盾怎么判断" |

### 灵枢：微观操作篇（10 个）
| # | 子 skill | 目录 | 一句话 | 何时触发 |
|---|---------|------|--------|---------|
| 38 | 形神一体 | `huangdi-neijing/body-mind-integration/` | 心理与生理的因果联系 | "情绪不好身体也跟着出问题" |
| 39 | 通调水道 | `huangdi-neijing/bottleneck-unblock/` | 找到堵塞点并疏通 | "卡住了但不知道卡在哪" |
| 40 | 沟通说服 | `huangdi-neijing/communicate-persuade/` | 对不配合者的方案转化 | "对方很强势不愿意配合" |
| 41 | 虚实补泻 | `huangdi-neijing/excess-deficiency-decision/` | 该加强还是该削减 | "该投入还是该撤出" |
| 42 | 四海调控 | `huangdi-neijing/four-seas-regulation/` | 复杂系统的核心枢纽管理 | "面面俱到但都管不过来" |
| 43 | 司外揣内（灵枢版） | `huangdi-neijing/observe-infer/` | 从表象推断内部隐藏状态 | "怎么看穿表象" |
| 44 | 因质施治 | `huangdi-neijing/personalize-by-constitution/` | 按个体差异定制方案 | "一刀切方案不适用" |
| 45 | 调气复常 | `huangdi-neijing/qi-regulation/` | 恢复系统正常功能 | "表面症状处理了但没好" |
| 46 | 先治其本 | `huangdi-neijing/root-cause-priority/` | 从根源解决连锁问题 | "好几个问题不知道该先解哪个" |
| 47 | 时机-机会窗口 | `huangdi-neijing/timing-opportunity/` | 何时做比做什么更重要 | "是现在做还是再等等" |

---

## 周易 12 skill（zhouyi/）

| # | 子 skill | 目录 | 一句话 | 何时触发 |
|---|---------|------|--------|---------|
| 48 | 卦象处境诊断 | `zhouyi/hexagram-situation-diagnosis/` | 用卦象归类复杂处境 | "这个局面太复杂了帮我捋捋" |
| 49 | 进退边界 | `zhouyi/advance-retreat-boundary/` | 该进该退该守该等的判断 | "怕搞砸不敢推进" |
| 50 | 吉凶悔吝 | `zhouyi/auspicious-risk-language/` | 古典词语转现代风险语言 | "无咎是不是好事" |
| 51 | 冲突联盟诊断 | `zhouyi/conflict-coalition-diagnosis/` | 争端、联盟、分裂的处理 | "团队里两边人闹翻了" |
| 52 | 亢龙有悔检查 | `zhouyi/humility-overreach-check/` | 强势时检查是否过头 | "做得不错还要继续加码吗" |
| 53 | 时位定位表 | `zhouyi/line-position-timing/` | 事件处在初二三五四上的阶段判断 | "是不是还没到时候" |
| 54 | 观卦观察判断 | `zhouyi/observation-judgment/` | 表面与本质差距的判断 | "怎么看穿表象" |
| 55 | 关系聚合诊断 | `zhouyi/relationship-assembly/` | 亲密关系与团队凝聚力 | "这段感情能长久吗" |
| 56 | 蛊卦修复周期 | `zhouyi/repair-renewal-cycle/` | 系统腐坏是修还是推倒重来 | "旧系统不行了修还是换" |
| 57 | 震卦危机应对 | `zhouyi/response-action/` | 突发冲击的响应级别判断 | "突然出事了我该怎么回应" |
| 58 | 复卦反转周期 | `zhouyi/reversal-cycle/` | 拐点判断：该进受阻、该退不甘 | "进退两难死局怎么破" |
| 59 | 小过大过节制 | `zhouyi/scale-and-restraint-control/` | 资源是否足以承载目标 | "这事我能做多大" |

---

## 🔴 组合使用：跨系统经典链路

| 场景 | 链路 | 说明 |
|------|------|------|
| 职业困境+身心崩溃 | maodun-fenxi → body-mind-integration → hexagram-situation-diagnosis | 先理清矛盾→身心联动→处境判断 |
| 创业方向+节奏+压力 | chijiuzhan-san-jieduan → excess-deficiency-decision → advance-retreat-boundary | 阶段判断→投入产出→进退时机 |
| 团队冲突+管理+个人情绪 | lianglei-maodun → conflict-coalition-diagnosis → emotion-organ-proxy | 敌我判断→联盟处理→情绪影响 |
| 重大决策+信息不足 | diaocha-yanjiu → observation-judgment → timing-opportunity | 调查→透过现象→把握时机 |
| 多任务崩溃 | tan-gangqin → biao-ben-priority → scale-and-restraint-control | 弹钢琴→标本先后→节制规模 |

---

## 反例清单

以下场景**不要**使用本系统：

| 反例 | 为什么 | 替代方案 |
|------|--------|---------|
| 代码报错/shell 命令 | 不涉及策略分析 | 直接调试 |
| 天气/股票价格/时间查询 | 单一事实查询 | 直接回答 |
| 紧急物理危险 | 分析框架耽误时间 | 立即行动 |
| 午餐吃什么 | 过度使用贬值 | 简单决策 |
| 纯娱乐闲聊 | 不在系统覆盖范围 | 自然对话 |

---

## 使用原则

1. **自动路由**：你不需要指定用哪个 skill，说你的问题，Hub 自动匹配
2. **跨系统组合**：问题跨越多个维度时自动组合，无需手动指定
3. **先诊断后行动**：先匹配子 skill 诊断，再给行动方案
4. **3 秒检查**：先自问"够复杂吗？"——不够就不用

## 来源

- 毛泽东《毛泽东选集》第 1-5 卷 → 25 个 skill（book2skill 蒸馏）
- 《黄帝内经》素问 + 灵枢 → 22 个 skill（book2skill 蒸馏）
- 《周易》 → 12 个 skill（book2skill 蒸馏）

evidence level: firsthand（原文蒸馏）
