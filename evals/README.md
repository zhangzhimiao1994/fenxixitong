# evals：cross-system-hub 评测工具

用来给 `skills/cross-system-hub` 打分、决定一轮改动保留还是回滚。流程由 `meta/hub-evolve` 调用；所有路径都相对于仓库根目录。

## 协议

- **题目**：`skills/cross-system-hub/test-prompts.json` 里的全部测试题（当前 30 条）。
- **实测**：独立实测者带 skill 跑全部题目，按 `specs/runner.md`；只用 `tools/get_prompts.py` 取题，看不到 expected。
- **对照组**：不带 skill 的回复，复用 `baselines/`；新增题目才按 `specs/baseline.md` 补跑。
- **评审**：3 位独立评审按 `specs/judge.md` 的 9 维 rubric 打分，本轮均分 = 3 人总分的平均（30 条 × 3 位评审，即协议 `30x3`）。
- **棘轮**：均分**严格高于** `history.tsv` 里同协议的最好成绩才保留，否则整体回滚；无论结果都如实记进 `history.tsv`。
- **停止**：连续两轮涨幅都小于 1 分，停下来向用户报告。

## 目录

| 路径 | 内容 | 入库 |
|---|---|---|
| `specs/runner.md` | 实测者规范（带 skill） | 是 |
| `specs/baseline.md` | 对照组规范（不带 skill） | 是 |
| `specs/judge.md` | 评审规范：9 维 rubric、打分标尺、产出格式 | 是 |
| `specs/lessons.md` | 前 15 轮的教训，改 skill 前先读 | 是 |
| `tools/get_prompts.py` | 取题：`python evals/tools/get_prompts.py 1,2,3`，只打印 `id : prompt` | 是 |
| `baselines/base_<ID>.md` | 对照组回复（第 12 轮跑出，复用） | 是 |
| `history.tsv` | 分数历史 | 是 |
| `runs/<round>/` | 每轮的 run、补跑的 base、评审 json | 否（`.gitignore`） |
| `legacy/` | 更早的进化记录（原 `evolution/` 目录：`FINAL_REPORT.md`、`results.tsv`），只作存档 | 是 |

## 一轮的操作步骤

1. 读 `history.tsv`，取 `30x3` 协议下的最好均分作为 `BEST`；读 `specs/lessons.md`。
2. 改 skill（只改和本轮问题有关的文件），运行 `python tools/check_skills.py`，须 0 错误；改了工具就运行 `python tools/sync_scripts.py --check`，须 0 差异。
3. 实测：独立实测者按 `specs/runner.md`，参数 `<REPO>` = 仓库根目录、`<OUT_DIR>` = `evals/runs/<round>/`，跑全部题目。
4. 对照组：新增题目按 `specs/baseline.md` 补跑，确认后复制进 `baselines/`。
5. 评审：3 位独立评审（A、B、C）按 `specs/judge.md` 各写 `evals/runs/<round>/judge_<X>.json`。
6. 算均分，按棘轮保留或整体回滚；在 `history.tsv` 和下表各追加一行。
7. 向用户报告分数和结论。

能并行起子 agent 的环境就并行跑第 3–5 步；不能的环境按顺序在全新上下文里执行，保证实测者和评审互不可见。

## 分数历史

内容同 `history.tsv`。`15x2` 是旧协议（15 题 × 2 评审），与 `30x3` 不可比。

| protocol | round | judge_A | judge_B | judge_C | mean | kept | note |
|---|---|---|---|---|---|---|---|
| 15x2 | R3 | 74.62 | 72.92 | - | 73.8 | yes | |
| 15x2 | rewrite | 69.76 | 70.65 | - | 70.2 | no | |
| 15x2 | R5 | 74.58 | 71.95 | - | 73.3 | yes | |
| 15x2 | R6 | 77.43 | 75.27 | - | 76.4 | yes | |
| 15x2 | R7 | 73.37 | 76.6 | - | 75.0 | no | |
| 15x2 | R8 | 74.08 | 71.22 | - | 72.65 | no | |
| 15x2 | R9 | 73.51 | 69.68 | - | 71.6 | yes | restructure; kept on restructure branch |
| 15x2 | R10 | 77.0 | 70.19 | - | 73.6 | yes | kept on restructure branch |
| 15x2 | R11 | 75.17 | 74.79 | - | 75.0 | yes | kept on restructure branch |
| 15x2 | R12 | 77.54 | 77.54 | - | 77.54 | yes | |
| 15x2 | R13 | 75.39 | 76.11 | - | 75.75 | no | |
| 30x3 | R12 | 75.07 | 75.14 | 74.34 | 74.85 | baseline | |
| 30x3 | R14 | 78.1 | 75.37 | 76.51 | 76.66 | yes | current main |
| 30x3 | R15 | 75.24 | 76.27 | 76.73 | 76.08 | no | |
