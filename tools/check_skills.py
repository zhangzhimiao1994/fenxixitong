"""skills/ 目录一致性检查。提交前运行：python tools/check_skills.py

检查项（任一失败则退出码 1）：
  1. 每个 skill 只有一份：SKILL.md 只能在 skills/<slug>/SKILL.md，不允许在入口目录下嵌套子 skill 副本
  2. frontmatter 是合法 YAML，且有 name、description、version；不用块标量（| 或 >）
  3. 每个 skill 有可解析的 test-prompts.json，且至少有一条用例
  4. related_skills 里引用的 slug 都存在
  5. 总入口维度表里每个入口 skill 都存在，且含"## 被总入口调用时：段落契约"一节（自动识别新加的维度行）；
     "层"只取观察/象征/校准；"顺序"是数字且不重复；互译表的列名都在维度表里
  6. 提到 divine.py 的 skill：有 scripts/divine.py 且与 tools/divine.py 哈希一致、有 scripts/requirements.txt、
     SKILL.md 有 divine-tool 标记块、标记块外不再写死 tools/divine.py
  7. 分析层不能路由到维护层：hub 维度表的入口、任何 skills/*/SKILL.md 里不出现指向 meta/ 的路径
  8. meta/*/SKILL.md 的 frontmatter 是合法 YAML，且有 name、description（meta 维护 skill 不计入分析 skill 数）
警告（不影响退出码）：frontmatter 的 name 与目录名不一致；维度入口里出现字数配额（数字 + 字）
"""
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("缺少 PyYAML：pip install -r requirements.txt")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SKILLS = Path(__file__).resolve().parent.parent / "skills"
# 平台自带的 skill / 参考文档，不按本仓库约定维护
VENDORED: set = set()  # 本仓库为通用 agent 技能包，不内置任何平台 skill

META = SKILLS.parent / "meta"  # 维护层：蒸馏、进化用，永远不能被 hub 路由到
META_PATH = re.compile(r"(?<![\w.-])meta[/\\]")

errors, warnings = [], []
slugs = {p.parent.name for p in SKILLS.glob("*/SKILL.md")}
meta_slugs = {p.parent.name for p in META.glob("*/SKILL.md")}

# 7. 分析层里不出现指向 meta/ 的路径
for p in sorted(SKILLS.glob("*/SKILL.md")):
    for n, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
        if META_PATH.search(line):
            errors.append(f"{p.parent.name}:{n}: 出现指向 meta/ 的路径，分析 skill 不能引用维护层：{line.strip()[:40]}")

for p in sorted(SKILLS.rglob("SKILL.md")):
    rel = p.relative_to(SKILLS)
    if len(rel.parts) != 2:
        errors.append(f"{rel.as_posix()}: 嵌套的 SKILL.md，子 skill 只放在 skills/<slug>/，入口里按 slug 引用")

for p in sorted(SKILLS.glob("*/SKILL.md")):
    slug = p.parent.name
    if slug in VENDORED:
        continue
    text = p.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{slug}: 没有 frontmatter")
        continue
    for line in m.group(1).split("\n"):
        bm = re.match(r"^([\w_-]+):\s*[|>][-+]?\s*$", line)
        if bm:
            errors.append(f"{slug}: frontmatter 的 {bm.group(1)} 用了块标量（| 或 >），部分运行时（如 Hermes）会读成 \"|\"；改成单行")
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        errors.append(f"{slug}: frontmatter 不是合法 YAML（值里含冒号时要加引号）：{str(e).splitlines()[0]}")
        continue
    if not isinstance(fm, dict):
        errors.append(f"{slug}: frontmatter 不是映射")
        continue
    for key in ("name", "description", "version"):
        if not fm.get(key):
            errors.append(f"{slug}: frontmatter 缺 {key}")
    if fm.get("name") and fm["name"] != slug:
        warnings.append(f"{slug}: name 是 {fm['name']!r}，与目录名不一致")
    for item in fm.get("related_skills") or []:
        ref = item.get("slug") if isinstance(item, dict) else item
        if isinstance(ref, str) and ref not in slugs:
            errors.append(f"{slug}: related_skills 引用了不存在的 {ref}")

    tp = p.parent / "test-prompts.json"
    if not tp.exists():
        errors.append(f"{slug}: 缺 test-prompts.json")
        continue
    try:
        data = json.loads(tp.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"{slug}: test-prompts.json 无法解析：{e}")
        continue
    # 仓库里并存三种格式：darwin 的 test_cases、zhengliu 的分组列表、cross-system-hub 的分级列表
    if isinstance(data, list):
        n = len(data)
    else:
        n = len(data.get("test_cases") or []) + sum(
            len(data.get(k) or []) for k in ("should_trigger", "should_not_trigger", "edge_case", "edge_cases"))
    if n == 0:
        errors.append(f"{slug}: test-prompts.json 里没有用例")

# 5. 总入口维度表：每行的入口 skill 存在、含段落契约；入口里出现字数配额 → 警告
#    维度表 = cross-system-hub/SKILL.md 里第一张表头同时含"层"和"入口"的表；新加的行自动被检查
HUB = SKILLS / "cross-system-hub" / "SKILL.md"
CONTRACT = "## 被总入口调用时：段落契约"
if HUB.exists():
    hub_lines = HUB.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    cols, entries, orders = None, [], {}
    LAYERS = ("观察", "象征", "校准")
    for i, line in enumerate(hub_lines):
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.strip().startswith("|") else None
        if cols is None:
            if cells and "层" in cells and "入口" in cells:
                cols = cells
            continue
        if not cells:
            break
        if set("".join(cells)) <= set("-: "):
            continue
        if len(cells) != len(cols):
            errors.append(f"cross-system-hub: 维度表第 {i + 1} 行列数 {len(cells)} 与表头 {len(cols)} 不一致")
            continue
        if META_PATH.search(cells[cols.index("入口")]):
            errors.append(f"cross-system-hub: 维度表第 {i + 1} 行（{cells[0]}）的入口指向 meta/，维护层不能被 hub 路由到")
            continue
        m = re.search(r"`([\w-]+)`", cells[cols.index("入口")])
        if not m:
            errors.append(f"cross-system-hub: 维度表第 {i + 1} 行（{cells[0]}）的入口列没有 `slug`")
            continue
        if m.group(1) in meta_slugs:
            errors.append(f"cross-system-hub: 维度表 {cells[0]} 的入口 {m.group(1)} 是 meta/ 下的维护 skill，不能被 hub 路由到")
        entries.append((cells[0], m.group(1)))
        layer = cells[cols.index("层")]
        if layer not in LAYERS:
            errors.append(f"cross-system-hub: 维度表 {cells[0]} 的'层'是 {layer!r}，只能取 {'/'.join(LAYERS)}")
        if "顺序" in cols:
            order = cells[cols.index("顺序")]
            try:
                order = float(order)
            except ValueError:
                errors.append(f"cross-system-hub: 维度表 {cells[0]} 的'顺序'不是数字：{order!r}")
            else:
                if order in orders:
                    errors.append(f"cross-system-hub: 维度表 {cells[0]} 的'顺序' {order:g} 与 {orders[order]} 重复")
                orders[order] = cells[0]
    if cols is None:
        errors.append("cross-system-hub: 找不到维度表（表头需含'层'和'入口'两列）")
    elif "顺序" not in cols:
        errors.append("cross-system-hub: 维度表缺'顺序'列")
    # 互译表的列名（除"主题"和最后的翻译列）都必须是维度表里的维度名；缺列 → 警告（该维度不参与共振）
    ref = SKILLS / "cross-system-hub" / "references" / "translation-and-plan.md"
    if ref.exists():
        head = next((l for l in ref.read_text(encoding="utf-8").split("\n") if l.startswith("| 主题 |")), None)
        if head is None:
            errors.append("translation-and-plan.md: 找不到互译表（表头以'| 主题 |'开头）")
        else:
            tcols = [c.strip() for c in head.strip().strip("|").split("|")][1:]
            tcols = [c for c in tcols if not c.endswith("翻译")]
            dims = {d for d, _ in entries}
            for c in tcols:
                if c not in dims:
                    errors.append(f"translation-and-plan.md: 互译表列 {c!r} 不在维度表里")
            for d in sorted(dims - set(tcols)):
                warnings.append(f"translation-and-plan.md: 互译表没有维度 {d!r} 的列（该维度不参与共振）")
    dim_names = [d for d, _ in entries]
    PROPER = ("心理援助热线", "心理危机", "心理门诊", "心理咨询", "心理科", "心理学")  # 热线、机构名不算点名维度
    for dim, slug in entries:
        ep = SKILLS / slug / "SKILL.md"
        if not ep.exists():
            errors.append(f"维度表 {dim}: 入口 {slug} 不存在")
            continue
        et = ep.read_text(encoding="utf-8").replace("\r\n", "\n")
        if CONTRACT not in et:
            errors.append(f"维度表 {dim}: 入口 {slug} 缺少一节'{CONTRACT[3:]}'")
        else:
            # 段落契约里点名其他维度的中文名 → 警告（新增维度时这些条款要跟着改，应改成按层或按维度表的列写）
            body = re.split(r"\n(?:## |> )", et.split(CONTRACT, 1)[1], maxsplit=1)[0]
            for e in PROPER:
                body = body.replace(e, "")
            for other in dim_names:
                if other != dim and other in body:
                    warnings.append(f"{slug}: 段落契约里点名了其他维度'{other}'（改成按层或按维度表的列写）")
        for n, line in enumerate(et.split("\n"), 1):
            if re.search(r"\d+ ?字", line):
                warnings.append(f"{slug}:{n}: 入口里出现字数配额（字数只在总入口深度表）：{line.strip()[:40]}")
    print(f"维度表：{len(entries)} 个维度入口已检查")

# 6. 工具打包：提到 divine.py 的 skill（SKILL.md 或 references/*.md）必须自带工具，单独拷走也能运行
import hashlib  # noqa: E402

TOOL_SRC = SKILLS.parent / "tools" / "divine.py"
TOOL_BLOCK = re.compile(r"<!-- divine-tool:begin -->.*?<!-- divine-tool:end -->", re.S)
src_hash = hashlib.sha256(TOOL_SRC.read_bytes()).hexdigest() if TOOL_SRC.exists() else None
if src_hash is None:
    errors.append("tools/divine.py 不存在")
for p in sorted(SKILLS.glob("*/SKILL.md")):
    d, slug = p.parent, p.parent.name
    text = p.read_text(encoding="utf-8")
    refs = [f.read_text(encoding="utf-8") for f in sorted((d / "references").glob("*.md"))]
    if "divine.py" not in text and not any("divine.py" in r for r in refs):
        continue
    packed = d / "scripts" / "divine.py"
    if not packed.exists():
        errors.append(f"{slug}: 提到 divine.py 但缺 scripts/divine.py（运行 python tools/sync_scripts.py）")
    elif src_hash and hashlib.sha256(packed.read_bytes()).hexdigest() != src_hash:
        errors.append(f"{slug}: scripts/divine.py 与 tools/divine.py 哈希不一致（运行 python tools/sync_scripts.py）")
    if not (d / "scripts" / "requirements.txt").exists():
        errors.append(f"{slug}: 缺 scripts/requirements.txt（运行 python tools/sync_scripts.py）")
    if not TOOL_BLOCK.search(text):
        errors.append(f"{slug}: SKILL.md 缺 <!-- divine-tool:begin/end --> 标记块（运行 python tools/sync_scripts.py）")
    outside = TOOL_BLOCK.sub("", text)  # 标记块内第 1 步的回退顺序不算
    for line in outside.split("\n"):
        if "tools/divine.py" in line:
            errors.append(f"{slug}: SKILL.md 仍写死 tools/divine.py 路径（改成 scripts/divine.py）：{line.strip()[:40]}")

# 8. meta 维护 skill：frontmatter 合法（单行 YAML，有 name、description）
for p in sorted(META.glob("*/SKILL.md")):
    slug = p.parent.name
    text = p.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"meta/{slug}: 没有 frontmatter")
        continue
    if any(re.match(r"^([\w_-]+):\s*[|>][-+]?\s*$", line) for line in m.group(1).split("\n")):
        errors.append(f"meta/{slug}: frontmatter 用了块标量（| 或 >），改成单行")
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        errors.append(f"meta/{slug}: frontmatter 不是合法 YAML（值里含冒号时要加引号）：{str(e).splitlines()[0]}")
        continue
    if not isinstance(fm, dict):
        errors.append(f"meta/{slug}: frontmatter 不是映射")
        continue
    for key in ("name", "description"):
        if not fm.get(key):
            errors.append(f"meta/{slug}: frontmatter 缺 {key}")
    if fm.get("name") and fm["name"] != slug:
        warnings.append(f"meta/{slug}: name 是 {fm['name']!r}，与目录名不一致")

for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"meta 维护 skill {len(meta_slugs)} 个（不计入分析 skill）")
print(f"\n{len(slugs)} 个分析 skill（其中 {len(VENDORED & slugs)} 个平台自带未检查）；{len(errors)} 个错误，{len(warnings)} 个警告")
sys.exit(1 if errors else 0)
