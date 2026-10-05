---
name: hub-evolve
version: "1.0.0"
description: "维护本仓库 cross-system-hub 的流程 skill：把一本新书蒸馏后接入 hub（归入已有维度的子 skill，或新增维度），以及按 evals/ 的评测协议进化 hub（实测、对照、3 位独立评审打分、棘轮保留或回滚）。触发词：接入这本书、蒸馏这本书到 hub、把这本书加进 hub、进化 hub、给 hub 打分、跑一轮 hub 评测。不处理用户的心理、关系、运势等分析提问，那些交给 cross-system-hub。"
---

# hub-evolve：接入新书与进化 hub

本 skill 只在维护仓库时使用，属于 `meta/` 维护层。`meta/` 下的任何 skill 都不能被 hub 路由到。
下文路径都相对于仓库根目录。

| 用户说 | 走哪一节 |
|---|---|
| 接入这本书 / 蒸馏这本书到 hub | A |
| 进化 hub / 给 hub 打分 / 跑一轮评测 | B |
| 任何分析提问（我最近怎么了、帮我看看运势） | 不处理，交给 `skills/cross-system-hub` |

---

## A. 接入新书

### A1 蒸馏

1. 调用 `meta/zhengliu`，选"书 / 长内容"路线（方法路线，RIA+E+B）。
2. 产出目录放在 `distill/<书名>/`，包含 BOOK_OVERVIEW、候选、rejected、GLOSSARY、子 skill 草稿和 test-prompts。
3. 如果用户没给原文、笔记或经用户批准的来源位置 → 🛑 STOP，先向用户要，不凭记忆蒸馏（zhengliu 的规则）。

### A2 判断归属（如果……就……）

先读 `skills/cross-system-hub/SKILL.md` 的维度表，再逐条判断：

- **如果**已有某个维度能用这本书的机制解释用户的问题 → **就**把它做成那个维度下的子 skill，并在该维度入口段落契约的"选用哪些子 skill"里加一行。不新增维度。
- **如果**这本书同时满足下面两条 → **才**新增维度：
  1. 有自己的激活信号（用户说出某类话时只有它该被叫起来）；
  2. 能给出现有维度给不了的解释。
  只满足一条 → 按上一条归入已有维度。
- **如果**拿不准 → 🔴 CHECKPOINT：先向用户说明理由（倾向归入哪个维度、为什么、另一种做法的代价），等用户确认再动手。

### A3 新增维度（只在 A2 判定新增时）

完全按 `skills/cross-system-hub/references/dimension-template.md` 的步骤做，这里只列必做项，细节以模板为准：

1. 建入口 skill `skills/<入口名>/SKILL.md`，正文最前面放"## 被总入口调用时：段落契约"。
2. 在 hub 维度表加一行。
3. 在 `skills/cross-system-hub/references/translation-and-plan.md` 的互译表加一列。
4. 新入口或子 skill 用到抽牌、排盘、起卦工具 → 运行 `python tools/sync_scripts.py`，再运行 `python tools/sync_scripts.py --check`，必须 0 差异。
5. 在 `skills/cross-system-hub/test-prompts.json` 加至少 2 条测试，其中 1 条和旧维度混合出现；新增题目要补跑对照组（见 B2）。

### A4 收尾检查

运行 `python tools/check_skills.py`，必须 0 错误。
- 如果有错误 → 按报错逐条修，修完重跑；不允许带错误交付。
- 如果报"指向 meta/"的错误 → 删掉那条路径；分析层不能引用维护层。

---

## B. 进化 hub（评测协议）

协议、目录和历史分数见 `evals/README.md`；执行细节只在 `evals/specs/` 里定义，本节只写流程和规则。

### B1 一轮的步骤

1. 读 `evals/history.tsv`，记下当前协议下的最好均分 `BEST`。
2. 读 `evals/specs/lessons.md`。
3. 定本轮改法（遵守 B3 的修改原则），只改和本轮问题有关的文件。
4. **实测**：由独立实测者按 `evals/specs/runner.md` 带 skill 跑全部测试题，产出写到 `evals/runs/<round>/run_<ID>.md`。题目只用 `python evals/tools/get_prompts.py <ids>` 获取。
5. **对照组**：复用 `evals/baselines/base_<ID>.md`；只有新增的题目才按 `evals/specs/baseline.md` 补跑，并把新文件加入 `evals/baselines/`。
6. **评审**：3 位独立评审分别按 `evals/specs/judge.md` 打分，各写 `judge_<A|B|C>.json`。
7. 本轮均分 = 3 位评审总分的平均。
8. **棘轮**：
   - 如果均分 **严格高于** `BEST` → 保留本轮改动，kept=yes；
   - 否则 → 整体回滚本轮所有改动（不挑着留），kept=no。
9. 无论保留还是回滚，都把 3 个分数、均分、kept 和一句 note 如实追加到 `evals/history.tsv`，并同步 `evals/README.md` 的分数表。不改旧记录。
10. 🔴 CHECKPOINT：向用户报告本轮分数、保留或回滚、评审一致指出的问题，等用户决定是否继续下一轮。

### B2 隔离与平台中性

- 环境能并行启动子 agent → 实测者、补跑对照组、3 位评审都用彼此独立的子 agent 并行跑。
- 环境不能并行 → 按顺序逐个在全新上下文里执行（新会话或清空上下文），保证实测者和评审互相看不到对方的产出，评审之间也互相看不到。
- 不论哪种环境，改 skill 的人不给自己打分。
- 本 skill 不依赖任何特定平台的工具名；"启动子 agent""新上下文"用所在环境自己的方式实现。

### B3 修改原则（来自前 15 轮的教训，详见 `evals/specs/lessons.md`）

1. **一件事只在一处定义**，其他地方写指针（"见总入口 4.2"），不复述。
2. **不新增字数数字**：篇幅只在 hub 的深度表里定义；入口、子 skill、参考文件只写"约几成 / 1 句"。
3. **hub 有大小上限**：以当前保留版本的 `skills/cross-system-hub/SKILL.md` 体积为上限；要加内容，先删同等或更多的重复，或把细节移到入口或参考文件，hub 只留指针。
4. **只修多位评审一致指出的问题**。只有一位评审提到、而且要新增规则的 → 先判断它会不会和现有规则冲突；会冲突或拿不准 → 本轮不修，记进 note。
5. 写法要具体：给格式、示例、判据；不为省字把规则压成缩写或代号。
6. **停止条件**：如果连续两轮均分涨幅都小于 1 分（含回滚的轮次记为 0），🛑 STOP，向用户报告现状和剩余问题，不要继续自动循环。

### B4 失败分支

- 如果某条实测没产出 run 文件，或某位评审没产出 json → 只重跑缺的那一份，不重跑整轮；仍失败 → 本轮作废，不记分，告知用户。
- 如果 3 位评审总分最大差 ≥ 5 分 → 先检查评审是否读到了同一批 run 文件，再决定是否重评那位离群的评审。
- 如果工具（`divine.py`）在实测中报错 → 按 skill 自己的兜底处理，并在执行记录里如实写出；不允许编造工具结果。
- 如果 `check_skills.py` 在改完后报错 → 先修到 0 错误再进入实测。

---

## C. 边界

- 不修改 `skills/` 里和本轮无关的 skill。
- 不把 `meta/` 下的任何 skill 加进 hub 维度表，`skills/` 里不出现指向 `meta/` 的路径（`check_skills.py` 会报错）。
- 评测时不让实测者看到 `test-prompts.json` 里的 `expected`：实测者只能通过 `evals/tools/get_prompts.py` 拿到 `id : prompt`。
- `evals/runs/` 不入库；`evals/baselines/` 和 `evals/history.tsv` 入库。

## 反例黑名单

| 不要做 | 为什么 | 改成 |
|---|---|---|
| 让实测者直接读 test-prompts.json | 看到 expected 会照着答，分数虚高 | 只用 get_prompts.py |
| 1–2 位评审就决定保留 | 噪声比改动带来的涨幅还大 | 固定 3 位，取平均 |
| 均分持平就保留 | 棘轮要求严格高于 | 持平即回滚 |
| 回滚后不记分 | 历史失真，下一轮误判 BEST | 回滚也写进 history.tsv |
| 为修一条意见在 hub 加新规则 | 前几轮多次因此产生新冲突、掉分 | 先查冲突，优先删重复、写指针 |
| 新书一来就新增维度 | 维度膨胀，路由变难 | 按 A2 两条判据，拿不准先问 |
