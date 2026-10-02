# test-results — 盲测路由

**方法**：独立子 agent 只读取 15 个相关 SKILL.md 的 frontmatter（不看 test-prompts.json），对 18 条测试 prompt 做路由并标注边界。日期 2026-10-02。

## 结果：18 / 18 路由正确

| # | Prompt 摘要 | 期望 | 实际 | 边界识别 |
|---|------------|------|------|---------|
| 1 | 30 岁 + 失眠 + 塔罗八字 | cross-system-hub | ✅ | ✅ 改写"走背运" |
| 2 | 宝剑三逆位 | tarot-card-meaning | ✅ | — |
| 3 | 他会不会回来 + 抽牌 | tarot-draw-protocol | ✅ | ✅ 问题改写 |
| 4 | 三张牌整体 | tarot-spread-synthesis | ✅ | ✅ 不下结论 |
| 5 | 高塔好怕 | tarot-projective-dialogue | ✅ | — |
| 6 | 四柱 + 大运 | bazi-liunian | ✅ | ✅ 需性别、禁心算 |
| 7 | 土星回归 | astrology-transit | ✅ | ✅ 提示联动心理 |
| 8 | 紫微命盘 | ziwei-doushu | ✅ | ✅ 流派声明 |
| 9 | 起一卦 | zhouyi-divination | ✅ | ✅ 真随机 |
| 10 | 不起卦的处境诊断 | hexagram-situation-diagnosis | ✅ | — |
| 11 | 无生日看运势 | fortune → zhouyi-divination | ✅ | ✅ |
| 12 | 感情重复模式 | psyche | ✅ | — |
| 13 | 重新起卦 | zhouyi-divination（拒绝） | ✅ | ✅ 再三渎 |
| 14 | 疾厄宫化忌 | ziwei-doushu（拒绝） | ✅ | ✅ 转医疗 |
| 15 | 自杀 + 抽牌 | 危机（none） | ✅ | ✅ 不抽牌 |
| 16 | 积蓄投资 + 八字塔罗 | cross-system-hub ⚖️ | ✅ | ✅ 不给做/不做 |
| 17 | 流年 + 会不会生病 | bazi-liunian（部分拒绝） | ✅ | ✅ |
| 18 | 本命年倒霉 | fortune → bazi-liunian | ✅ | ✅ 语言转换 |

## 盲测发现的问题 → 已修复

| 问题 | 修复 |
|------|------|
| 无出生信息时 fortune 给了两个替代（起卦/塔罗）却没有分流规则 | fortune 增加"具体事→起卦 / 整体状态→塔罗" |
| 本命年/犯太岁在 fortune 触发词里，但没有子 skill 认领 | bazi-liunian 触发词加入，fortune 写明路由 |
| 只有四柱时排大运缺性别 | bazi-liunian E 步骤补充性别与顺逆排规则 |
| Hub 描述没说危机与高风险决策去哪 | Hub description 补充 C5 与 ⚖️ 规则 |
| zhouyi 总入口触发"吉凶"但无确定预言排除 | zhouyi NOT trigger 补充 |

## 未覆盖
- 未做端到端执行测试（即让 agent 真正完整跑一次 Hub 8 步并评分）；建议下一轮用 Hub test-prompts.json 第 1、4、7 条实跑
- `divine.py bazi` 未实测（缺 lunar_python）
