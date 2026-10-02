#!/usr/bin/env python3
"""cross-system-hub 占断辅助工具：提供真随机抽牌/起卦与八字排盘，避免模型"心算随机"或"心算排盘"。

用法:
  python tools/divine.py tarot [--spread single|three|cross|relation] [--no-reversed]
  python tools/divine.py iching
  python tools/divine.py bazi YYYY-MM-DD HH:MM --gender m|f     (需 pip install lunar_python)

所有随机均来自 secrets 模块（操作系统级随机源）。
"""
import argparse
import secrets
import sys

# ---------------- 塔罗 ----------------
MAJOR = ["0 愚人", "I 魔术师", "II 女祭司", "III 皇后", "IV 皇帝", "V 教皇", "VI 恋人",
         "VII 战车", "VIII 力量", "IX 隐士", "X 命运之轮", "XI 正义", "XII 倒吊人",
         "XIII 死神", "XIV 节制", "XV 恶魔", "XVI 高塔", "XVII 星星", "XVIII 月亮",
         "XIX 太阳", "XX 审判", "XXI 世界"]
SUITS = ["权杖", "圣杯", "宝剑", "星币"]
RANKS = ["王牌", "二", "三", "四", "五", "六", "七", "八", "九", "十", "侍从", "骑士", "王后", "国王"]
DECK = MAJOR + [f"{s}{r}" for s in SUITS for r in RANKS]
assert len(DECK) == 78

SPREADS = {
    "single": ["核心讯息"],
    "three": ["过去/根源", "现在/处境", "趋势/可能走向"],
    "relation": ["我的状态", "对方/环境的状态", "关系的连接点", "阻碍", "建议方向"],
    # Waite《Pictorial Key》Part III §7 原位置名
    "cross": ["笼罩·整体氛围", "交叉·阻碍", "冠顶·目标与理想", "其下·已成的根基", "其后·正在过去的影响",
              "其前·即将到来的影响", "自我态度", "环境与亲友", "希望与恐惧", "将来·汇总走向"],
}


def draw_tarot(spread, reversed_ok):
    deck = DECK[:]
    # Fisher–Yates with secrets
    for i in range(len(deck) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        deck[i], deck[j] = deck[j], deck[i]
    positions = SPREADS[spread]
    print(f"牌阵: {spread}（{len(positions)} 张）  随机源: secrets（OS 级）")
    for pos, card in zip(positions, deck):
        orient = "逆位" if reversed_ok and secrets.randbelow(2) else "正位"
        print(f"  [{pos}] {card} · {orient}")


# ---------------- 周易三钱法 ----------------
# 三爻卦按 初→三爻 的阴阳（1=阳, 0=阴）
TRIGRAMS = {(1, 1, 1): "乾", (1, 1, 0): "兑", (1, 0, 1): "离", (1, 0, 0): "震",
            (0, 1, 1): "巽", (0, 1, 0): "坎", (0, 0, 1): "艮", (0, 0, 0): "坤"}
ORDER = ["乾", "震", "坎", "艮", "坤", "巽", "离", "兑"]
# KING_WEN[上卦][下卦] = (序号, 卦名)，列顺序同 ORDER
_KW = {
    "乾": [(1, "乾"), (25, "无妄"), (6, "讼"), (33, "遁"), (12, "否"), (44, "姤"), (13, "同人"), (10, "履")],
    "震": [(34, "大壮"), (51, "震"), (40, "解"), (62, "小过"), (16, "豫"), (32, "恒"), (55, "丰"), (54, "归妹")],
    "坎": [(5, "需"), (3, "屯"), (29, "坎"), (39, "蹇"), (8, "比"), (48, "井"), (63, "既济"), (60, "节")],
    "艮": [(26, "大畜"), (27, "颐"), (4, "蒙"), (52, "艮"), (23, "剥"), (18, "蛊"), (22, "贲"), (41, "损")],
    "坤": [(11, "泰"), (24, "复"), (7, "师"), (15, "谦"), (2, "坤"), (46, "升"), (36, "明夷"), (19, "临")],
    "巽": [(9, "小畜"), (42, "益"), (59, "涣"), (53, "渐"), (20, "观"), (57, "巽"), (37, "家人"), (61, "中孚")],
    "离": [(14, "大有"), (21, "噬嗑"), (64, "未济"), (56, "旅"), (35, "晋"), (50, "鼎"), (30, "离"), (38, "睽")],
    "兑": [(43, "夬"), (17, "随"), (47, "困"), (31, "咸"), (45, "萃"), (28, "大过"), (49, "革"), (58, "兑")],
}
LINE_NAMES = ["初", "二", "三", "四", "五", "上"]
VALUE_NAMES = {6: "老阴 ⚋→⚊（变）", 7: "少阳 ⚊", 8: "少阴 ⚋", 9: "老阳 ⚊→⚋（变）"}


def hexagram(lines):
    lower = TRIGRAMS[tuple(lines[:3])]
    upper = TRIGRAMS[tuple(lines[3:])]
    num, name = _KW[upper][ORDER.index(lower)]
    return f"第{num}卦 {name}（{upper}上{lower}下）"


def cast_iching():
    # 背=3（阳）、字=2（阴）；三枚之和：6老阴 7少阳 8少阴 9老阳
    values = [sum(3 if secrets.randbelow(2) else 2 for _ in range(3)) for _ in range(6)]
    print("三钱法起卦（自下而上）  随机源: secrets（OS 级）")
    for i in range(5, -1, -1):
        print(f"  {LINE_NAMES[i]}爻: {values[i]} {VALUE_NAMES[values[i]]}")
    base = [1 if v in (7, 9) else 0 for v in values]
    changed = [1 - b if v in (6, 9) else b for b, v in zip(base, values)]
    moving = [LINE_NAMES[i] for i, v in enumerate(values) if v in (6, 9)]
    print(f"本卦: {hexagram(base)}")
    if moving:
        print(f"变爻: {'、'.join(moving)}（共 {len(moving)} 个）")
        print(f"之卦: {hexagram(changed)}")
    else:
        print("变爻: 无（静卦，看本卦卦辞）")


# ---------------- 八字 ----------------
def bazi(date, time, gender):
    try:
        from lunar_python import Solar
    except ImportError:
        sys.exit("未安装 lunar_python。请先运行: pip install lunar_python\n"
                 "或改用专业排盘软件，把四柱与大运结果粘贴给 skill。")
    y, m, d = map(int, date.split("-"))
    hh, mm = map(int, time.split(":"))
    lunar = Solar.fromYmdHms(y, m, d, hh, mm, 0).getLunar()
    ec = lunar.getEightChar()
    print(f"公历 {date} {time}  →  农历 {lunar.toString()}")
    print("注意: 未做真太阳时校正；出生地经度偏离东经120°较多时，请先换算真太阳时再输入。")
    print(f"四柱: {ec.getYear()} {ec.getMonth()} {ec.getDay()} {ec.getTime()}")
    print(f"五行: {ec.getYearWuXing()} {ec.getMonthWuXing()} {ec.getDayWuXing()} {ec.getTimeWuXing()}")
    print(f"日主: {ec.getDayGan()}")
    print(f"十神(天干): 年{ec.getYearShiShenGan()} 月{ec.getMonthShiShenGan()} 时{ec.getTimeShiShenGan()}")
    yun = ec.getYun(1 if gender == "m" else 0)
    print(f"起运: 出生后约 {yun.getStartYear()} 年 {yun.getStartMonth()} 个月")
    for dy in yun.getDaYun()[1:9]:
        print(f"  大运 {dy.getGanZhi()}  {dy.getStartYear()}-{dy.getEndYear()}（{dy.getStartAge()}-{dy.getEndAge()}岁）")


def main():
    p = argparse.ArgumentParser(description="cross-system-hub 占断辅助工具")
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tarot")
    t.add_argument("--spread", choices=SPREADS, default="three")
    t.add_argument("--no-reversed", action="store_true")
    sub.add_parser("iching")
    b = sub.add_parser("bazi")
    b.add_argument("date")
    b.add_argument("time")
    b.add_argument("--gender", choices=["m", "f"], required=True)
    a = p.parse_args()
    if a.cmd == "tarot":
        draw_tarot(a.spread, not a.no_reversed)
    elif a.cmd == "iching":
        cast_iching()
    else:
        bazi(a.date, a.time, a.gender)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
