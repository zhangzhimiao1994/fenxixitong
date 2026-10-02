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
1. **原文核对进度**（2026-10-02，用户提供原文）：
   - ✅ Waite《Pictorial Key》：已核对。修正 4 处——凯尔特法为 Part III §7、"明确提问"出自 §8；力量/正义对调原文未给理由、未提马赛；四花色-元素对应非 Waite 原书；死神原释义含 "mortality"（本体系作伦理取舍并注明）；凯尔特十位置改用 Waite 原名
   - ✅ 《周易本义》：经文、系辞、筮仪引文全部无误；变爻取辞规则仅 1 变、乾坤 6 变两条可由《本义》印证，其余待《易学启蒙》原文
   - ✅ 《紫微斗数全书》（四卷本）：已核对。修正宫名（妻妾、奴仆）、破军原为"耗星"、四化原义、十干四化表、大限起法差异；注明原书为吉凶断语体系，本 skill 只取结构
   - ⏳ 八字（《子平真诠》《滴天髓阐微》）、星盘（《Tetrabiblos》《The Astrology of Personality》）、《易学启蒙》、荣格全集第 8 卷：尚未取得原文
2. **流派依赖**：八字旺衰、紫微安星、占星宫制均存在流派差异，skill 中已声明默认规则，但未穷举
3. **八字排盘未实测**：`divine.py bazi` 依赖 `lunar_python`，本机未安装，代码按该库公开 API 编写，需安装后跑一次验证
4. **真太阳时**：工具未做经度校正，已在输出中提示
5. **科学效力**：塔罗与命理的预测效力缺乏证据（C1、C2），skill 全部以"象征/倾向"语言输出，并在 Hub 中设为象征层、不得推翻事实
