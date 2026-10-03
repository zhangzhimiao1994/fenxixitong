# TARGET_BRIEF — 体系分析 + 托勒密 蒸馏

- **路线**：书 / 长内容（Method route，RIA+E+B）
- **日期**：2026-10-03
- **用途**：为 Cross-System Hub 新增「🧩 体系分析」维度（行为科学六书），并为「🌟 运势」维度补充古典占星本命框架（托勒密）。产出的 skill 要能被 `cross-system-hub` 路由调用，也能单独使用。
- **证据模式**：用户提供的原书 PDF（本地文件，已用 PyMuPDF 抽取文字层，按 PDF 页码 `PAGE n` 引用）；外部批评和证据强度用 reliable-secondary 标注。

## 来源清单

| key | 书 | 作者 | 页数 | 文本层 | 产出位置 |
|-----|----|------|:---:|-------|---------|
| attached | Attached: The New Science of Adult Attachment | Amir Levine, Rachel Heller | 268 | 原生 | `skills/tixi-fenxi/attach-*` |
| mindset | Mindset: The New Psychology of Success | Carol S. Dweck | 147 | 原生 | `skills/tixi-fenxi/mindset-*` |
| hold-me-tight | Hold Me Tight | Sue Johnson | 209 | 原生 | `skills/tixi-fenxi/eft-*` |
| atomic-habits | Atomic Habits | James Clear | 289 | 原生 | `skills/tixi-fenxi/habit-*` |
| deep-work | Deep Work | Cal Newport | 190 | 原生 | `skills/tixi-fenxi/deepwork-*` |
| superforecasting | Superforecasting | Philip E. Tetlock, Dan Gardner | 360 | 扫描 + OCR | `skills/tixi-fenxi/forecast-*` |
| tetrabiblos | Tetrabiblos（J. M. Ashmand 英译） | Claudius Ptolemy | 200 | archive.org 扫描 + OCR | `skills/fortune/ptolemy-*` |

## 已知局限

- 扫描本有 OCR 错字和页眉，PAGE n 是 PDF 页码，不是印刷页码。
- 原书受版权保护：skill 内以位置引用加转述为主，短引用每处 ≤15 词。
- Mindset 的干预效应在大规模重复研究中很小；Tetrabiblos 的预测效力没有科学证据。两者都在 skill 的 B 段写明。

## 未决问题

- 无
