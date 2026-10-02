# PIPELINE_STATE

## 已完成阶段
- [x] 路线选择：书 / 长内容（Method）
- [x] 候选提取：框架 / 原则 / 案例 / 反例 / 术语
- [x] 验证四检（跨语境证据、生成力、区分度、边界）
- [x] 撰写 9 个 skill（RIA+E+B）+ test-prompts.json
- [x] 工具：`tools/divine.py`（塔罗、起卦已实测；八字依赖 lunar_python，见风险 3）
- [x] Hub 集成：cross-system-hub v3.0.0
- [x] 盲测：见 `test-results.md`

## 产出
| Skill | 路径 | 类型 |
|-------|------|------|
| psyche | skills/psyche | 路由（合并荣格+弗洛伊德，无新理论主张） |
| tarot | skills/tarot | 路由 |
| tarot-draw-protocol | skills/tarot/tarot-draw-protocol | 方法 |
| tarot-card-meaning | skills/tarot/tarot-card-meaning | 方法 |
| tarot-spread-synthesis | skills/tarot/tarot-spread-synthesis | 方法 |
| tarot-projective-dialogue | skills/tarot/tarot-projective-dialogue | 方法（整合设计） |
| fortune | skills/fortune | 路由 + 语言转换表 |
| bazi-liunian | skills/fortune/bazi-liunian | 方法 |
| astrology-transit | skills/fortune/astrology-transit | 方法 |
| ziwei-doushu | skills/fortune/ziwei-doushu | 方法 |
| zhouyi-divination | skills/zhouyi/zhouyi-divination | 方法 |

## 剩余风险（必须对使用者透明）
1. **原文未逐条核对**：zhengliu 要求"不凭记忆蒸馏"。本次由用户授权直接撰写，R 段均为位置引用 + 转述，标注为 reliable-secondary。提供原文后应逐条复核，尤其是 Waite 节号与子平/紫微篇目位置
2. **流派依赖**：八字旺衰、紫微安星、占星宫制均存在流派差异，skill 中已声明默认规则，但未穷举
3. **八字排盘未实测**：`divine.py bazi` 依赖 `lunar_python`，本机未安装，代码按该库公开 API 编写，需安装后跑一次验证
4. **真太阳时**：工具未做经度校正，已在输出中提示
5. **科学效力**：塔罗与命理的预测效力缺乏证据（C1、C2），skill 全部以"象征/倾向"语言输出，并在 Hub 中设为象征层、不得推翻事实
