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
    # 高风险决策专用：只看态度，不设"趋势/结果"位，避免牌面暗示做或不做
    "stakes": ["我在怕什么", "我在期待什么", "我忽略了什么"],
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
        sys.exit("[DEPENDENCY_MISSING] lunar_python 未安装。\n"
                 "AGENT 操作: 运行 `pip install -r requirements.txt`（或 `pip install lunar_python`），安装成功后重跑本命令。\n"
                 "若当前环境禁止安装: 请用户从专业排盘软件粘贴四柱+大运；禁止心算排盘。")
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
    from datetime import date
    this_year = date.today().year
    years = []
    for yr in range(this_year, this_year + 3):
        # 取当年 6 月 1 日（已过立春）的年柱作为流年
        gz = Solar.fromYmd(yr, 6, 1).getLunar().getYearInGanZhiByLiChun()
        years.append(f"{yr} {gz}")
    print("流年（立春换年）: " + " / ".join(years))


# ---------------- 星盘 ----------------
SIGNS = ["白羊", "金牛", "双子", "巨蟹", "狮子", "处女", "天秤", "天蝎", "射手", "摩羯", "水瓶", "双鱼"]
PLANETS = [("太阳", "Sun"), ("月亮", "Moon"), ("水星", "Mercury"), ("金星", "Venus"), ("火星", "Mars"),
           ("木星", "Jupiter"), ("土星", "Saturn"), ("天王", "Uranus"), ("海王", "Neptune"), ("冥王", "Pluto")]
ASPECTS = [(0, "合"), (60, "六分"), (90, "四分"), (120, "三分"), (180, "对分")]


def _fmt(lon):
    lon %= 360
    return f"{SIGNS[int(lon // 30)]} {lon % 30:4.1f}°"


def _longitudes(ephem, when):
    out = {}
    for cn, en in PLANETS:
        body = getattr(ephem, en)(when)
        out[cn] = float(ephem.Ecliptic(body, epoch=when).lon) * 180 / 3.141592653589793
    return out


def astro(date, time, tz, lat, lon):
    try:
        import ephem
    except ImportError:
        sys.exit("[DEPENDENCY_MISSING] ephem 未安装。\n"
                 "AGENT 操作: 运行 `pip install -r requirements.txt`（或 `pip install ephem`），安装成功后重跑本命令。\n"
                 "若当前环境禁止安装: 请用户从 astro.com 粘贴星盘；禁止心算行星位置。")
    import math
    from datetime import datetime, timedelta
    local = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    utc = local - timedelta(hours=tz)
    when = ephem.Date(utc)
    natal = _longitudes(ephem, when)
    print(f"出生: {date} {time} (UTC{tz:+g})  纬度 {lat} 经度 {lon}  | 回归黄道")
    for cn, _ in PLANETS:
        print(f"  {cn}: {_fmt(natal[cn])}")
    # 上升点：由地方恒星时与黄赤交角计算
    obs = ephem.Observer()
    obs.date, obs.lat, obs.lon = when, str(lat), str(lon)
    ramc = float(obs.sidereal_time())
    eps = math.radians(23.4393 - 0.0130 * ((utc.year - 2000) / 100))
    phi = math.radians(lat)
    asc = math.degrees(math.atan2(math.cos(ramc), -(math.sin(ramc) * math.cos(eps) + math.tan(phi) * math.sin(eps)))) % 360
    print(f"  上升: {_fmt(asc)}  （整宫制：第 1 宫 = {SIGNS[int(asc // 30)]}）")
    print("主要相位（个人行星间，容许度 ≤6°）:")
    names = ["太阳", "月亮", "水星", "金星", "火星", "木星", "土星"]
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            d = abs(natal[a] - natal[b]) % 360
            d = min(d, 360 - d)
            for ang, label in ASPECTS:
                if abs(d - ang) <= 6:
                    print(f"  {a} {label} {b}（{d:.1f}°）")
    now = ephem.now()
    transit = _longitudes(ephem, now)
    print(f"当前行运（{ephem.Date(now).datetime():%Y-%m-%d} UTC）:")
    for cn in ["木星", "土星"]:
        hits = []
        for target in ["太阳", "月亮"]:
            d = abs(transit[cn] - natal[target]) % 360
            d = min(d, 360 - d)
            for ang, label in [(0, "合"), (90, "刑"), (180, "冲")]:
                if abs(d - ang) <= 5:
                    hits.append(f"{label}本命{target}")
        d = abs(transit[cn] - asc) % 360
        if min(d, 360 - d) <= 5:
            hits.append("合上升")
        if cn == "土星":
            d = abs(transit[cn] - natal["土星"]) % 360
            if min(d, 360 - d) <= 8:
                hits.append("土星回归")
        print(f"  行运{cn}: {_fmt(transit[cn])}  {'、'.join(hits) if hits else '与本命 ☉☽↑ 无紧密相位'}")


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
    s = sub.add_parser("astro")
    s.add_argument("date")
    s.add_argument("time")
    s.add_argument("--tz", type=float, default=8, help="出生地时区，北京时间=8")
    s.add_argument("--lat", type=float, required=True, help="纬度，北纬为正")
    s.add_argument("--lon", type=float, required=True, help="经度，东经为正")
    a = p.parse_args()
    if a.cmd == "tarot":
        draw_tarot(a.spread, not a.no_reversed)
    elif a.cmd == "iching":
        cast_iching()
    elif a.cmd == "astro":
        astro(a.date, a.time, a.tz, a.lat, a.lon)
    else:
        bazi(a.date, a.time, a.gender)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
