"""cross-system-hub 回复自检：按总入口现行规则逐项检查一条回复，只用标准库，不联网。

用法：
  python3 scripts/check_reply.py <reply.txt> --level L1|L2|L3|L4|crisis
  python3 scripts/check_reply.py --level L2 < reply.txt      # 不给文件就从标准输入读
退出码：0 = 全部通过；1 = 有 ✗；2 = 参数错误。

检查项（都对应 SKILL.md 里的条款，本脚本不另立规则）：
  1. 问号数（4.1）：全文最多 1 个；续接提示、C5 的热线行豁免；crisis 档另豁免 C5 的安全问句
  2. 篇幅（4.2）：正文字数 ≤ 深度表上限；摘录行、安全格式、⚖️ 清单、门槛句与 12356、三周计划、
     续接提示、收尾行不计；汉字 1 个算 1 字，英文 1 个词算 1 字，连续数字算 1 字；crisis 档不查
  3. 内部术语（4.5 不外露清单 + STEP/C/L 编号 + 示范话术占位）；摘录行除外
  4. 运势段评价词（顺逆禁令）：回复里有八字或星盘内容时，运势段（摘录行除外）不出现
     顺 / 不顺 / 利 / 不利 / 吉 / 凶 / 喜用
  5. 收尾行（4.6）：有免责和核对请求；有工具摘录时还要有"缺乏科学证据"；crisis 档不带收尾行
"""
import argparse
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

LIMITS = {"L1": 300, "L2": 900, "L3": 1500, "L4": 1500}

# 4.5 不外露术语（与 SKILL.md 4.5 同一份清单；改清单时两处一起改）
TERMS = ["体系", "维度", "主要矛盾", "观察层", "象征层", "校准层", "半条链", "半截链", "循环链", "解释链",
         "环节链", "一句带过", "完整段", "停顿轮", "候选", "激活", "段落契约", "判决", "计分", "⚖️"]
CODE_RE = re.compile(r"STEP ?\d|(?<![A-Za-z0-9])[CL]\d{1,2}(?![0-9A-Za-z])")
PLACEHOLDER_RE = re.compile(r"……|__+|\[[^\]\n]{0,12}\]")

# 摘录行前缀（象征契约 + 4.5 跟随回复语言）
EXCERPT_RE = re.compile(r"(工具抽到|你抽到|工具排盘|工具星盘|工具起卦|你报的牌|你贴的盘|你摇到|"
                        r"Tool draw|Tool chart|Tool cast|Tool reading|You drew)[：:][^。\n]*[。]?")
FORTUNE_HINT = re.compile(r"工具排盘|工具星盘|Tool chart|八字|星盘|命盘|紫微|四柱|大运|流年|行运|日主")
FORTUNE_WORDS = ["不顺", "不利", "喜用", "顺", "利", "吉", "凶"]
# 带这些字但不是评价词的常用词
NOT_EVAL = ["顺序", "顺便", "顺手", "顺着", "顺带", "顺口", "利用", "利息", "权利", "便利", "流利", "锋利",
            "利索", "利落", "麻利", "吉他"]

CLOSING_ZH = ("以上是帮你理清思路的框架", "牌义只作自我反思的框架")
CLOSING_EN = ("This is a framework",)
SAFETY_KEYS = ("110", "12338", "12356", "12355", "保护令", "验伤", "暗号", "随手能拿", "有人的地方",
               "成瘾医学科", "婚姻家庭")
CHECKLIST_KEYS = ("持证财务顾问", "原则：", "自己填：", "先弄清", "3 个信号", "可逆的试法", "只提")
PLAN_RE = re.compile(r"^\s*(三周计划|第 ?\d ?周|Day ?\d|每日：|Week ?\d)")
CONTINUE_RE = re.compile(r"回[\"'“‘]继续[\"'”’]|reply [\"“]continue[\"”]", re.I)
THRESHOLD_RE = re.compile(r"(2 ?周|两周|2 ?weeks|two weeks)")
THRESHOLD_TAIL = re.compile(r"评估|门诊|医院|see a doctor|get (it )?checked|evaluat", re.I)
C5_SAFETY_Q = re.compile(r"安全吗|伤害自己|具体要怎么做|safe right now|hurt yourself", re.I)


def split_sentences(text):
    out, buf = [], ""
    for ch in text:
        buf += ch
        if ch in "。！？!?\n":
            out.append(buf)
            buf = ""
    if buf:
        out.append(buf)
    return out


def count_chars(text):
    cjk = len(re.findall(r"[一-鿿]", text))
    words = len(re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?", text))
    nums = len(re.findall(r"\d+(?:[.,:]\d+)?", text))
    return cjk + words + nums


def paragraphs(text):
    return [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def is_closing(par):
    s = par.strip()
    return s.startswith(CLOSING_ZH) or s.startswith(CLOSING_EN)


def strip_excerpts(text):
    return EXCERPT_RE.sub("", text)


def body_text(text):
    """去掉 4.2 规定不计正文的部分，返回正文。"""
    kept = []
    for par in paragraphs(text):
        if is_closing(par):
            continue
        lines = par.split("\n")
        # ⚖️ 清单、安全格式：多是成块的列表行，整块含清单或安全关键词就不计
        listy = sum(1 for l in lines if re.match(r"^\s*([-·•□]|\d+[.、)])", l)) >= max(1, len(lines) // 2)
        if listy and any(k in par for k in CHECKLIST_KEYS + SAFETY_KEYS):
            continue
        par_kept = []
        for line in lines:
            if PLAN_RE.match(line):
                continue
            if re.match(r"^\s*([-·•□]|\d+[.、)])", line) and any(k in line for k in SAFETY_KEYS + CHECKLIST_KEYS):
                continue
            par_kept.append(line)
        par = strip_excerpts("\n".join(par_kept))
        sents = []
        for s in split_sentences(par):
            if CONTINUE_RE.search(s):
                continue
            if "12356" in s or "持证财务顾问" in s:
                continue
            if THRESHOLD_RE.search(s) and THRESHOLD_TAIL.search(s):
                continue
            sents.append(s)
        kept.append("".join(sents))
    return "\n".join(kept)


def check_questions(text, level):
    rest = []
    for s in split_sentences(text):
        if CONTINUE_RE.search(s):
            continue
        if level == "crisis" and (C5_SAFETY_Q.search(s) or "12356" in s or "热线" in s):
            continue
        if "12356" in s and "热线" in s:
            continue
        rest.append(s)
    n = sum(s.count("？") + s.count("?") for s in rest)
    return n <= 1, f"问号 {n} 个（上限 1）"


def check_length(text, level):
    if level == "crisis":
        return True, "crisis 档不查篇幅"
    n = count_chars(body_text(text))
    lim = LIMITS[level]
    return n <= lim, f"正文约 {n} 字（{level} 上限 {lim}）"


def check_terms(text):
    t = strip_excerpts(text)
    hits = [w for w in TERMS if w in t]
    hits += sorted(set(CODE_RE.findall(t)))
    # ⚖️ 清单的"自己填"行按参考文件第四节本来就留空（"__"），不算示范话术里的占位
    t = "\n".join(l for l in t.split("\n") if not any(k in l for k in ("自己填", "□")))
    ph = PLACEHOLDER_RE.findall(t)
    hits += [f"占位{p}" for p in ph]
    return not hits, ("未见内部术语" if not hits else "出现：" + "、".join(hits))


def check_fortune(text):
    if not FORTUNE_HINT.search(text):
        return True, "回复里没有八字或星盘内容，不查"
    hits = []
    for par in paragraphs(text):
        if is_closing(par) or not FORTUNE_HINT.search(par):
            continue
        t = strip_excerpts(par)
        for w in NOT_EVAL:
            t = t.replace(w, "　" * len(w))
        for w in FORTUNE_WORDS:
            while w in t:
                hits.append(w)
                t = t.replace(w, "　" * len(w), 1)
    return not hits, ("运势段没有评价词" if not hits else "运势段出现：" + "、".join(hits))


def check_closing(text, level):
    pars = paragraphs(text)
    closing = [p for p in pars if is_closing(p)]
    if level == "crisis":
        return not closing, ("crisis 档没有收尾行" if not closing else "crisis 档不带收尾行，删掉")
    if not closing:
        return False, "缺收尾行（4.6 固定答案）"
    c = closing[-1]
    if "牌义只作自我反思的框架" in c:
        return True, "只问牌义版收尾行"
    has_disclaimer = "不替代专业意见" in c or "replace professional advice" in c
    has_check = "有出入告诉我" in c or "tell me if anything" in c.lower()
    problems = []
    if not has_disclaimer:
        problems.append("缺免责")
    if not has_check:
        problems.append("缺核对请求")
    if EXCERPT_RE.search(text) and not ("缺乏科学证据" in c or "scientific evidence" in c):
        problems.append("有象征数据却缺'预测效力缺乏科学证据'")
    return not problems, ("收尾行齐全" if not problems else "；".join(problems))


def main():
    ap = argparse.ArgumentParser(description="cross-system-hub 回复自检")
    ap.add_argument("reply", nargs="?", help="回复文件（UTF-8）；不给或写 - 就从标准输入读")
    ap.add_argument("--level", required=True, choices=["L1", "L2", "L3", "L4", "crisis"])
    a = ap.parse_args()
    if a.reply and a.reply != "-":
        with open(a.reply, encoding="utf-8") as f:
            text = f.read()
    else:
        if hasattr(sys.stdin, "reconfigure"):
            sys.stdin.reconfigure(encoding="utf-8")
        text = sys.stdin.read()
    text = text.replace("\r\n", "\n")
    checks = [
        ("1 问号", check_questions(text, a.level)),
        ("2 篇幅", check_length(text, a.level)),
        ("3 内部术语", check_terms(text)),
        ("4 运势评价词", check_fortune(text)),
        ("5 收尾行", check_closing(text, a.level)),
    ]
    ok_all = True
    for name, (ok, msg) in checks:
        ok_all &= ok
        print(f"{'✓' if ok else '✗'} {name}：{msg}")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
