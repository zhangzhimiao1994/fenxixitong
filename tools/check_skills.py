"""skills/ 目录一致性检查。提交前运行：python tools/check_skills.py

检查项（任一失败则退出码 1）：
  1. 每个 skill 只有一份：SKILL.md 只能在 skills/<slug>/SKILL.md，不允许在入口目录下嵌套子 skill 副本
  2. frontmatter 是合法 YAML，且有 name、description、version；不用块标量（| 或 >）
  3. 每个 skill 有可解析的 test-prompts.json，且至少有一条用例
  4. related_skills 里引用的 slug 都存在
警告（不影响退出码）：frontmatter 的 name 与目录名不一致
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
VENDORED = {"find-skills", "kimiim", "skillhub-preference", "time-awareness", "worker-safety"}

errors, warnings = [], []
slugs = {p.parent.name for p in SKILLS.glob("*/SKILL.md")}

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

for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"\n{len(slugs)} 个 skill（其中 {len(VENDORED & slugs)} 个平台自带未检查）；{len(errors)} 个错误，{len(warnings)} 个警告")
sys.exit(1 if errors else 0)
