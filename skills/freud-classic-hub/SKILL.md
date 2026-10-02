---
name: freud-classic-hub
description: 弗洛伊德经典三模型 Hub。当用户的问题属于「内心冲突/纠结」「丧失后走不出来」「焦虑回避」三大经典领域时，由此 Hub 路由到对应的原始蒸馏 skill。当用户说「弗洛伊德经典模型」「用最基础的那个」等触发词时激活。
---

# Freud Classic Hub —— 弗洛伊德经典三模型路由中心

## 触发条件
- 用户提到「结构模型」「本我自我超我」「三我冲突」
- 用户说「我是不是在哀悼还是忧郁」「丧失后走不出来」
- 用户说「我很焦虑但不知道为什么」「我在回避什么」
- 用户的问题属于经典弗洛伊德核心三模型范畴

## 路由规则

### 判别标准

首先判断问题类型——按以下维度打分，最高分即目标 skill：

| 判定维度 | 指向 structural-model | 指向 mourning-melancholia | 指向 anxiety-defense |
|---------|----------------------|--------------------------|---------------------|
| 核心冲突 | 「我应该…但我不想」「我控制不住」 | 「我配不上」「我活该」「我不好」 | 「我怕」「我躲」「我不知道怕什么」 |
| 情绪基调 | 纠结、拉扯、矛盾 | 空虚、自责、无价值 | 紧张、回避、恐慌 |
| 时间特征 | 当下正在发生 | 追溯某个丧失后开始 | 持续或阵发，无明确起点 |
| 身体信号 | 无明显躯体化 | 疲劳、食欲↓、兴趣↓ | 心跳加速、出汗、胃紧 |

**路由决策** `=` 按上述四维度逐项打分（每条命中 +1），最高累计分即目标。

```
用户问题
  │
  ├─ 「应该…但不想」「控制不住」> 其他 → freud-structural-model
  │   （本我-自我-超我三角冲突）
  │
  ├─ 「配不上/活该/不好」> 其他，且有丧失线索 → freud-mourning-melancholia
  │   （哀悼 vs 忧郁鉴别）
  │
  └─ 「怕/躲/不知道怕什么」> 其他 → freud-anxiety-defense
      （焦虑信号 + 防御机制）
```

### 跨模型处理

```
if 两维度分数持平:
  按优先级：structure > mourning > anxiety
  （内心冲突是最紧迫的——先拆解三角，再往下走）

if 三个维度均分:
  → 🔴 CHECKPOINT 提示用户："这个问题涉及内心冲突、丧失和焦虑三个维度，建议从 freud-structural-model 开始，后续按需接入另两个。确认？"
```

## 🔴 CHECKPOINT：路由前确认

在进入具体子 skill 之前，输出一行确认：

```
🔴 路由决策：→ freud-{target}（原因：{最高分维度}，得分 {X}/4）
如果路由错误，回复「不对，应该是…」我将重新判别。
```

## 失败模式与 fallback

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| 用户说「不对，不是这个」 | 改用次高分 skill 重新判别 | → 转发到 `freud-hub`（让更广的主题路由接管） |
| 四条判定维度均不明确 | 追问一句：「你现在更接近哪种感觉——(A)内心在打架 (B)觉得自己不配 (C)在怕什么但说不清？」 | 用户拒绝选择 → 转发 `freud-hub` |
| 用户描述含自杀意念 | 停止路由，直接提供 400-161-9995，不分析 | 强制转发 `freud-mourning-melancholia`（含自杀评估） |
| 子 skill 文件不存在 | 从 Hub 速查表直接输出该模型的简要框架 | 转发 `freud-complete` 做全量分析 |

## 执行步骤

| 步骤 | 输入 | 操作 | 输出 |
|------|------|------|------|
| 1 | 用户原始消息 | 按「判别标准」四维度打分 | 三个分数（各0-4） |
| 2 | 三个分数 | **🔴 CHECKPOINT**：输出路由决策 `→ freud-{target}（{原因}，得分 {X}/4）` | 等待用户确认 |
| 3 | 确认后的 target | `read` 对应子 skill 的 SKILL.md | 子 skill 内容 |
|  |  | `freud-structural-model` → `freud-zhengliu/skills/freud-structural-model/SKILL.md` |  |
|  |  | `freud-mourning-melancholia` → `freud-zhengliu/skills/freud-mourning-melancholia/SKILL.md` |  |
|  |  | `freud-anxiety-defense` → `freud-zhengliu/skills/freud-anxiety-defense/SKILL.md` |  |
| 4 | 子 skill 执行结果 | 检查用户反馈 | 满意 → 结束；不满意 → fallback 表 |

## 不触发（路由到其他架构）

- 涉及梦/口误 → `freud-hub` → `freud-dreams-parapraxes`
- 涉及身体症状 → `freud-hub` → `freud-trauma-hysteria`
- 涉及性格/性心理 → `freud-hub` → `freud-sexuality-development`
- 涉及压抑/潜意识 → `freud-hub` → `freud-metapsychology`
- 涉及自恋/群体 → `freud-hub` → `freud-narcissism-identification`
- 涉及强迫重复 → `freud-hub` → `freud-death-drive-repetition`
- 涉及文明批判 → `freud-hub` → `freud-anxiety-civilization`
- 纯外部现实问题、非精神分析框架

## 三个经典模型速查

| Skill | 核心问题 | 关键概念 |
|-------|---------|---------|
| `freud-structural-model` | 谁在脑子里吵架？ | 本我（我要）、自我（调解）、超我（你不配） |
| `freud-mourning-melancholia` | 你在骂谁？ | 丧失对象内化进自我，自我谴责 = 骂内化对象 |
| `freud-anxiety-defense` | 你在怕什么？ | 焦虑先于压抑，防御是自我的自我保护 |

## 反例黑名单 —— 不要做的事

1. **不要跳过判别直接分析** —— 即使问题看起来很明显，也先打分后路由
2. **不要把三个模型都输出一遍** —— 一次只激活一个子 skill
3. **不要替用户决定「你应该用哪个」而不解释** —— 给出判别理由
4. **不要在用户表达自杀意念时继续分析** —— 停止路由，给热线
5. **不要在四维度均不明确时猜一个** —— 追问 A/B/C 三选一

## 与其他架构的关系

- `freud-classic-hub`：3个经典模型，最基础、最原始蒸馏
- `freud-hub`：9个按主题的扩展模型，覆盖更广
- `freud-complete`：全量16本著作一次性分析
