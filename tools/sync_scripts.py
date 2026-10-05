"""把 tools/divine.py 打包进每个用到它的 skill，让单独拷走的 skill 文件夹也能运行工具。

用法：
  python tools/sync_scripts.py          # 写入
  python tools/sync_scripts.py --check  # 只检查；有差异 → 列出并以退出码 1 结束

对每个在 SKILL.md 或 references/*.md 里提到 divine.py 的 skill：
  1. scripts/divine.py      与 tools/divine.py 逐字节一致
  2. scripts/requirements.txt  依赖清单（lunar_python、ephem）
  3. SKILL.md 里的 <!-- divine-tool:begin --> … <!-- divine-tool:end --> 标记块：
     已存在就替换，不存在就插到第一个 "## " 标题之前
  4. SKILL.md、references/*.md、test-prompts.json 里写死的 tools/divine.py 路径 → scripts/divine.py，
     pip install -r requirements.txt → pip install -r scripts/requirements.txt
     （参数原样保留；标记块内第 1 步的回退顺序不改）
幂等：连续运行两次，第二次没有任何改动。
"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
SOURCE = ROOT / "tools" / "divine.py"

BEGIN = "<!-- divine-tool:begin -->"
END = "<!-- divine-tool:end -->"
BLOCK = f"""{BEGIN}
**运行抽牌/排盘工具**（路径相对于本 SKILL.md 所在目录）：
1. 找脚本，按顺序取第一个存在的：`scripts/divine.py` → `../<任一同仓 skill>/scripts/divine.py` → 仓库根 `tools/divine.py`。
2. 运行：`python3 <脚本路径> <子命令> <参数>`；`python3` 不可用时换 `python`。
3. 输出 `[DEPENDENCY_MISSING]` → 执行 `pip install -r <脚本所在目录>/requirements.txt` 后重跑一次；仍失败 → 按下面第 4 步。
4. 找不到脚本 / 环境不能执行代码 / 安装失败 → 不编造任何牌面、卦象、命盘：塔罗请用户自己抽牌并报出牌名和正逆位；周易请用户掷三枚硬币六次，按"背=3、字=2"报出每次三枚之和（6/7/8/9，共 6 个数）；八字、星盘请用户贴出排盘结果。
{END}"""

REQUIREMENTS = """# divine.py 的依赖：tarot、iching、taisui 子命令只用标准库，不需要安装
lunar_python>=1.3   # bazi（八字排盘）、pillars（四柱反查）子命令需要
ephem>=4.1          # astro（星盘与行运）子命令需要
"""

BLOCK_RE = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
PATH_RE = re.compile(r"(?:python3?\s+)?tools/divine\.py")


def mentions(skill_dir):
    files = [skill_dir / "SKILL.md"] + sorted((skill_dir / "references").glob("*.md"))
    return any("divine.py" in f.read_text(encoding="utf-8") for f in files if f.is_file())


def fix_paths(text):
    text = PATH_RE.sub("scripts/divine.py", text)
    return text.replace("pip install -r requirements.txt", "pip install -r scripts/requirements.txt")


def render_skill_md(text):
    m = BLOCK_RE.search(text)
    if m:
        return fix_paths(text[:m.start()]) + BLOCK + fix_paths(text[m.end():])
    text = fix_paths(text)
    lines = text.split("\n")
    in_fence = False
    in_front = lines[0].strip() == "---"
    for i, line in enumerate(lines):
        if in_front:
            if i > 0 and line.strip() == "---":
                in_front = False
            continue
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("## "):
            return "\n".join(lines[:i] + BLOCK.split("\n") + [""] + lines[i:])
    return text.rstrip("\n") + "\n\n" + BLOCK + "\n"


def plan():
    """返回 [(路径, 期望字节)]；只含与磁盘不一致的项。"""
    src = SOURCE.read_bytes()
    req = REQUIREMENTS.encode("utf-8")
    targets, packed = [], []
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        d = skill_md.parent
        if not mentions(d):
            continue
        packed.append(d.name)
        targets.append((d / "scripts" / "divine.py", src))
        targets.append((d / "scripts" / "requirements.txt", req))
        text = skill_md.read_bytes().decode("utf-8")
        crlf = "\r\n" in text  # 保留文件原有的换行风格（Windows 检出可能是 CRLF）
        out = render_skill_md(text.replace("\r\n", "\n"))
        targets.append((skill_md, (out.replace("\n", "\r\n") if crlf else out).encode("utf-8")))
        extra = sorted((d / "references").glob("*.md")) + [d / "test-prompts.json"]
        for f in extra:
            if f.is_file():
                t = f.read_bytes().decode("utf-8")
                targets.append((f, fix_paths(t).encode("utf-8")))
    diffs = [(p, b) for p, b in targets if not p.is_file() or p.read_bytes() != b]
    return packed, diffs


def main():
    check = "--check" in sys.argv[1:]
    packed, diffs = plan()
    for p, b in diffs:
        rel = p.relative_to(ROOT).as_posix()
        state = "缺失" if not p.is_file() else "内容不一致"
        if check:
            print(f"DIFF  {rel}: {state}")
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b)
            print(f"WRITE {rel}（原{state}）")
    print(f"\n{len(packed)} 个 skill 打包了 divine.py：{', '.join(packed)}")
    if check:
        print(f"检查完成：{len(diffs)} 处差异" + ("（运行 python tools/sync_scripts.py 修复）" if diffs else ""))
        sys.exit(1 if diffs else 0)
    print(f"同步完成：写入 {len(diffs)} 个文件")


if __name__ == "__main__":
    main()
