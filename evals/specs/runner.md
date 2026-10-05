# 实测执行规范（with_skill）

你扮演一个**装好了本仓库 skill 的 agent**，用户发来一条消息，你按 skill 真实执行，产出要发给用户的回复。

## 参数

- `<REPO>`：仓库根目录。下文路径都相对于它。
- `<OUT_DIR>`：产出目录，默认 `evals/runs/<round>/`。
- `<IDS>`：本次要跑的题目 id，逗号分隔。

## 取题

只用下面的命令获取题目，它只打印 `id : prompt`：

```bash
python evals/tools/get_prompts.py <IDS>
```

不读 `skills/*/test-prompts.json`，不读 `evals/` 下的其他文件（baselines、history、其他 run、评审结果）。

## 规则

1. **先读 skill**：完整阅读 `skills/cross-system-hub/SKILL.md`。它让你去读哪个文件，就读哪个文件，例如：
   - 维度入口 `skills/guanxi/`、`skills/chengzhang/`、`skills/xingdong/`、`skills/panduan/` 等的 SKILL.md 和它们选中的子 skill
   - `skills/psyche/SKILL.md`、`skills/fortune/SKILL.md`、`skills/tarot/SKILL.md`
   - `skills/cross-system-hub/references/translation-and-plan.md`

   不读和这条消息无关的 skill；不读 `meta/`。

2. **工具要真跑**：skill 要求抽牌、排盘、起卦时，按 skill 里"运行抽牌/排盘工具"标记块的写法真实运行脚本。
   - 本机没有 `python3` 时用可用的 python，并在执行记录里如实写出实际运行的命令
   - 输出 `[DEPENDENCY_MISSING]` 时，按 skill 的指示安装依赖后重跑
   - 安装失败时，按 skill 的兜底处理
   - **禁止自己编牌面、卦象或命盘**

3. **单轮**：只回复这一轮。如果 skill 规定这一轮要停下来问用户，就照规定只输出这一轮该说的话，不要替用户回答。

4. **分段回复**：如果按 skill 的规则，这一轮回复要分成两部分（第一部分末尾有"回'继续'我接着说"一类续接提示）——
   1. 先写第一部分，作为第 1 轮回复；
   2. 模拟用户下一句只回"继续"；
   3. 按 skill 写第二部分，作为第 2 轮回复。

5. **不改仓库文件**，不做版本控制操作。

## 产出

每条消息写一个文件：`<OUT_DIR>/run_<ID>.md`，格式：

```
## 执行记录
- 读过的文件：…
- 按 skill 规则得出的结果（只写结论，不写推导过程）：安全筛查 = …；激活维度 = …；主要矛盾 = …；选中的子 skill = …；深度等级 = …
- 工具命令（实际运行的命令）与原始输出（原样粘贴）：…
- 是否分段、分段理由、两部分各自的正文字数 / 上限（不分段写"否"）
- skill 里不清楚、互相矛盾或做不到的地方（引用 skill 原文 + 一句说明；没有就写"无"）：…

## REPLY
（不分段时：原样发给用户的回复）

## REPLY-1
（分段时：第一部分）

## USER-2
继续

## REPLY-2
（分段时：第二部分）
```

不分段时只写 REPLY 一节；分段时只写 REPLY-1 / USER-2 / REPLY-2 三节。

## 回报（≤120 字）

每条消息一行：`ID | 激活维度 | 是否用了工具 | 发现的 skill 问题数`。
