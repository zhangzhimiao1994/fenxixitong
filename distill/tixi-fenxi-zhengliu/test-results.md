# test-results — 盲测汇总

方法：每本书的蒸馏 agent 只看各 skill 的 description，对 `test-prompts.json` 里每个用例判断"是否激活 / 是否路由到兄弟 skill / 是否说明边界"。第一轮不通过的，修改 description 后重测。逐条明细见 `books/<key>/test-results.md`。

⚠️ 局限：盲判由写 skill 的 agent 自己完成，没有独立评审，只测了 description 层面的路由，没有实际跑模型输出，结果可能偏乐观。后续建议用 `darwin-skill` 做独立评分。

| 书 | skill 数 | 用例数 | 第 1 轮 | 修订后 | 主要修订 |
|----|:---:|:---:|:---:|:---:|---------|
| attached | 4 | 26 | 22/26（84.6%） | 26/26 | 与 eft- 撞车的用例改为分流；约会初期 vs 风格判断分清 |
| hold-me-tight | 4 | 26 | 24/26 | 26/26 | 补"自伤当抗议"的边界、外遇仍在继续时不适用 |
| mindset | 4 | 25 | 22/25（88%） | 25/25 | 3 个 description 补边界（结构因素、体罚、肢体冲突） |
| atomic-habits | 4 | 27 | 23/27（85.2%） | 27/27 | 与 deepwork- 分界；成瘾/进食障碍转介 |
| deep-work | 4 | 25 | 22/25（88%） | 25/25 | 补身心不适、新到城市、入门级岗位三条边界 |
| superforecasting | 3 | 19 | 16/19（84%） | 19/19 | 补远期问题拆分、高噪音问题、暴力风险不做估计 |
| tetrabiblos | 4 | 28 | 24/28（85.7%） | 28/28 | 补"事故"拒绝项、缺出生时间的降级、不评判他人 |
| **合计** | **27** | **176** | **153/176（86.9%）** | **176/176** | |

维度路由 `tixi-fenxi/test-prompts.json`：7 个用例（3 个应触发、2 个不应触发、2 个边界），由主 agent 编写，尚未独立盲测。

## 结构校验（scratchpad/validate.py）

- 27 个 skill 的 frontmatter 中 `name` 都与目录名一致，`description` 都存在
- 所有 `related_skills` 和正文里反引号括起来的 slug 都能在仓库中找到
- 所有 `test-prompts.json` 都能解析，每个都有 3 个应触发、2 个不应触发、1-2 个边界用例
