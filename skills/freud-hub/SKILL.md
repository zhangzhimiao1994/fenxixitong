---
name: freud-hub
version: "1.1.0"
description: 弗洛伊德全集技能中心。当用户的问题涉及弗洛伊德相关领域但不确定用哪个具体技能时，由此 Hub 进行路由。当用户说「弗洛伊德怎么说」「精神分析怎么看」等笼统触发词时激活。
---

> 被维度入口或总入口调用时，只提供素材；格式、篇幅、提问、收尾、危机话术按总入口全局契约。

# Freud Hub —— 弗洛伊德全集技能路由中心

## 触发条件
- 用户提到「弗洛伊德」「精神分析」「心理动力学」等关键词
- 用户表现出与精神分析理论匹配的症状/困惑
- 用户说「帮我用弗洛伊德视角分析」
- 用户问题跨越多个子skill边界

## 路由规则

### 一级判别：是否是经典三模型？

先判断是否属于经典三模型范畴（内心冲突/丧失/焦虑防御）。若是 → 转发 `freud-classic-hub`，不在此 Hub 内处理。

```
if 用户问题含以下任一模式:
  「我应该…但我不想」「控制不住自己」→ classic → structural-model
  「我不配」「我活该」「失去后走不出来」→ classic → mourning-melancholia
  「我怕」「我躲」「不知道怕什么」→ classic → anxiety-defense
  → 转发 freud-classic-hub
```

### 二级路由：主题匹配

```
用户问题
  │
  ├─ 属于经典三模型范畴 → freud-classic-hub（二级路由）
  │
  ├─ 「查不出原因的身体症状」「哭不出来」「嗓子堵」→ freud-trauma-hysteria
  ├─ 「做了个梦」「反复做同一个梦」「怎么老是忘记/口误」→ freud-dreams-parapraxes
  ├─ 「我为什么总是这样」「性格从哪来」「洁癖/抠门/控制欲」→ freud-sexuality-development
  ├─ 「越压抑越反弹」「说不出来」「想不通为什么」→ freud-metapsychology
  ├─ 「我不够好」「别人怎么看我」「被孤立」「大家都这样」→ freud-narcissism-identification
  ├─ 「我纠结」「走不出来」「我不配好起来」→ freud-mourning-structure
  ├─ 「我又在重复」「每次都这样」「为什么又重蹈覆辙」→ freud-death-drive-repetition
  ├─ 「控制不住地担心」「为什么这么痛苦」「这社会是不是有问题」→ freud-anxiety-civilization
  ├─ 「整体怎么看弗洛伊德」「越不能越想」「禁忌」→ freud-development-overview
  └─ 跨3个以上领域 → freud-complete（全量一次性分析）
```

### 跨领域处理

```
if 命中 2 个主题:
  选主导主题（用户花最多篇幅描述的那个）
  先说明：「这个问题主要涉及 {主题A}，同时关联 {主题B}，先从 A 切入」

if 命中 3+ 个主题:
  → 🔴 CHECKPOINT：「这个问题跨 {N} 个领域，用 freud-complete 做全量分析还是逐个子 skill 查？」
```

## 🔴 CHECKPOINT：路由前确认

```
🔴 路由决策：→ freud-{target}（命中关键词：{具体词}）
如果路由错误，回复「不对」我将重新匹配。
```

## 失败模式与 fallback

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| 用户说「不对，不是这个主题」 | 取次高分主题重新路由 | → 输出完整路由树让用户手动选 |
| 用户话太短无法判定主题 | 追问：「你最困扰的是哪个方面——(A)身体/症状 (B)梦/行为 (C)关系/性格 (D)焦虑/情绪 (E)反复的模式？」 | → 转发 `freud-complete` 做全量分析 |
| 用户描述含自杀意念 | 不路由，执行 `cross-system-hub` C5 | → 提醒后可接 `freud-mourning-structure`（含自杀评估） |
| 子 skill 文件不存在 | 从速查表直接输出该模型的简要框架 | → 转发 `freud-complete` |

## 执行步骤

| 步骤 | 输入 | 操作 | 输出 |
|------|------|------|------|
| 1 | 用户原始消息 | 扫描是否命中经典三模型关键词 | 是 → 转发 `freud-classic-hub`；否 → 继续步骤2 |
| 2 | 过滤后的消息 | 按路由树匹配主题（关键词计数，最高命中即目标） | 目标 skill |
| 3 | 目标 skill | **🔴 CHECKPOINT**：输出路由决策 `→ freud-{target}（命中关键词：{具体词}）` | 等待用户确认 |
| 4 | 确认 | `read` 对应 skill 的 SKILL.md | 子 skill 内容 |
| 5 | 子 skill 结果 | 检查用户反馈 | 满意 → 结束；不满意 → fallback 表 |

### 子 Skill 路径速查

| Skill | 路径 |
|-------|------|
| `freud-trauma-hysteria` | `skills/freud-trauma-hysteria/SKILL.md` |
| `freud-dreams-parapraxes` | `skills/freud-dreams-parapraxes/SKILL.md` |
| `freud-sexuality-development` | `skills/freud-sexuality-development/SKILL.md` |
| `freud-metapsychology` | `skills/freud-metapsychology/SKILL.md` |
| `freud-narcissism-identification` | `skills/freud-narcissism-identification/SKILL.md` |
| `freud-mourning-structure` | `skills/freud-mourning-structure/SKILL.md` |
| `freud-death-drive-repetition` | `skills/freud-death-drive-repetition/SKILL.md` |
| `freud-anxiety-civilization` | `skills/freud-anxiety-civilization/SKILL.md` |
| `freud-development-overview` | `skills/freud-development-overview/SKILL.md` |
| `freud-classic-hub` | `skills/freud-classic-hub/SKILL.md` |
| `freud-complete` | `skills/freud-complete/SKILL.md` |

## 快速参考

### 理论精华速查

**结构模型**：本我（我要）← 自我（调解）→ 超我（你不配）+ 外部现实（不行）
**动力学**：力比多 = 可量化的性能量 → 可转移（升华）或堵住（症状）
**发展**：口欲→肛欲→阴茎（俄狄浦斯）→潜伏→生殖
**二元本能**：Eros（联结/爱）↔ Thanatos（解体/死）
**治疗目标**：本我在哪里，自我就应该在那里

### 关键修正历程
- 1895：创伤→躯体化（癔症研究）
- 1900：梦 = 愿望满足（梦的解析）
- 1915：压抑消耗持续能量、潜意识用物表象思考
- 1920：**转向**——强迫重复 + 死本能，创伤梦不是愿望满足
- 1923：结构模型（本我-自我-超我）
- 1926：**第二次修正**——焦虑先于压抑（不是压抑产生焦虑）
- 1930：文明的代价 = 本能压抑，幸福不在宇宙的设计中

### 紧急情况
如果用户表达自杀意念：
- **不分析、不解释**——这不是精神分析能处理的
- 执行 `cross-system-hub` C5（热线以那里为准）
- 建议前往最近的精神卫生中心或急诊

## 反例黑名单 —— 不要做的事

1. **不要跳过一级判别** —— 即使问题看起来不属于经典三模型，也先扫一遍
2. **不要把所有子 skill 都输出一遍** —— 一次只激活一个
3. **不要在用户话太短时猜一个主题** —— 追问 A/B/C/D/E
4. **不要在跨领域时假装单一主题能覆盖** —— 3+ 领域直接建议 freud-complete
5. **不要跳过 CHECKPOINT** —— 路由决策必须展示给用户确认
6. **不要在自杀意念出现时继续分析** —— 先给热线

## 子 Skill 清单

| Skill | 覆盖著作 | 核心功能 |
|-------|---------|---------|
| `freud-trauma-hysteria` | 癔症研究 | 创伤→躯体化、宣泄疗法 |
| `freud-dreams-parapraxes` | 梦的解析 + 日常心理病理学 | 梦解析、失误行为 |
| `freud-sexuality-development` | 性学三论 | 力比多发展、性心理阶段 |
| `freud-metapsychology` | 压抑 + 潜意识 | 压抑机制、物/词表象 |
| `freud-narcissism-identification` | 自恋导论 + 群体心理学 | 自恋类型、认同、群体力比多 |
| `freud-mourning-structure` | 哀悼与忧郁 + 自我与本我 + 纲要 | 结构模型、哀悼vs忧郁 |
| `freud-death-drive-repetition` | 超越快乐原则 | 强迫重复、死本能 |
| `freud-anxiety-civilization` | 抑制症状与焦虑 + 文明及其不满 | 焦虑信号、文明代价 |
| `freud-development-overview` | 图腾与禁忌 + 引论 | 俄狄浦斯全景、导航索引 |
