# PIPELINE_STATE

| 阶段 | 状态 | 说明 |
|------|:---:|------|
| 选路线 | ✅ | 书 / 长内容（Method route） |
| 来源取得 | ✅ | 用户提供 7 本 PDF；PyMuPDF 抽文本，扫描本使用自带的 OCR 层 |
| BOOK_OVERVIEW | ✅ ×7 | `books/<key>/BOOK_OVERVIEW.md` |
| 候选提取 | ✅ ×7 | `books/<key>/CANDIDATES.md` |
| 审核与拒绝 | ✅ | 拒绝共 70 条（attached 11、hold-me-tight 9、mindset 9、atomic-habits 6、deep-work 10、superforecasting 6、tetrabiblos 19），见各书 `REJECTED.md` |
| 写 skill | ✅ | 27 个原子 skill + 维度路由 `tixi-fenxi` |
| 链接 | ✅ | `INDEX.md`；`ptolemy-fate-calibration` ⇄ `forecast-calibrate-claim` 双向链接 |
| 盲测 | ✅（自评） | `test-results.md` |
| 接入 | ✅ | `cross-system-hub` v4.2.0（第 6 个维度 + 校准层）、`fortune`（托勒密路由、转换表、证据）、`psyche`（分流）、互译表加"体系分析"列 |
| 平铺镜像 | ✅ | 新 skill 已复制到 `skills/<slug>/`，与仓库现有约定一致 |

## 被拒的重要内容（防止回流）

- 托勒密：寿命、死亡、父母安危、子女、婚姻判决、心智疾病、性取向、地位、旅行凶险、世运占星。不得落地为对用户的预测
- Mindset："假成长型"只借用这个名称（来自作者 2015/2016 年的补充），检查项都以 2006 年初版原文为依据
- Hold Me Tight：用催产素、镜像神经元解释对话效果的部分属于作者推测，不作依据

## 剩余风险

1. 盲测是自评，建议用 `darwin-skill` 独立评分
2. 各书的外部批评和元分析引用没有联网逐条核对，已标为 reliable-secondary
3. Attached 的问卷是图片，文字层为空，没有读到；skill 里不计分
4. 托勒密：界（terms）表的 OCR 无法辨认，没有内置；排盘工具没有中天精确度数和逆行状态，只能用整宫近似
5. PAGE n 是 PDF 页码，《超预测》的印刷页码 = PDF 页码 − 14
