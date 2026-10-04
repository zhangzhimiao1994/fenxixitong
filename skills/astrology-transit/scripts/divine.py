#!/usr/bin/env python3
"""cross-system-hub 占断辅助工具：提供真随机抽牌/起卦与八字排盘，避免模型"心算随机"或"心算排盘"。

单文件、可随 skill 拷走：不读写其他文件，不依赖当前工作目录。
维护：源码只在仓库 tools/divine.py；改完运行 tools/sync_scripts.py 同步到各 skill 的 scripts/。

用法（<本脚本> = 本文件路径；python3 不可用时换 python）:
  python3 <本脚本> tarot [--spread single|three|relation|stakes|cross] [--no-reversed]
  python3 <本脚本> iching
  python3 <本脚本> bazi YYYY-MM-DD [HH:MM] --gender m|f [--no-hour] [--lon 经度]   (需 lunar_python)
  python3 <本脚本> pillars 年柱 月柱 日柱 [时柱]                                (需 lunar_python)
  python3 <本脚本> taisui 出生年 [--year 流年]
  python3 <本脚本> astro YYYY-MM-DD HH:MM --tz 8 --lat 纬度 --lon 经度           (需 ephem)

tarot / iching / taisui 只用标准库。所有随机均来自 secrets 模块（操作系统级随机源）。
"""
import argparse
import os
import secrets
import sys


def _utf8_stdio():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except AttributeError:  # Python < 3.7 或被替换的流
            pass


def _requirements_path():
    """依赖清单相对于本脚本所在目录查找：skills/<x>/scripts/ 下同目录；仓库 tools/ 下取上一级。"""
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(here, "requirements.txt"), os.path.join(os.path.dirname(here), "requirements.txt")):
        if os.path.isfile(cand):
            return cand
    return os.path.join(here, "requirements.txt")


def _dependency_missing(pkg, fallback):
    print(f"[DEPENDENCY_MISSING] {pkg}")
    print(f"安装命令: pip install -r {_requirements_path()}（或 pip install {pkg}），安装成功后重跑本命令。")
    print(f"若当前环境禁止安装或安装失败: {fallback}")
    sys.exit(2)

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
        print("变爻: 无")
    print("取辞: " + reading_target(values, base, changed))


def _line_name(i, yang):
    num = "九" if yang else "六"
    if i == 0:
        return "初" + num
    if i == 5:
        return "上" + num
    return num + LINE_NAMES[i]


def reading_target(values, base, changed):
    """朱熹《易学启蒙·考变占》变爻取辞规则（1 变、乾坤 6 变两条另见《周易本义》）。"""
    mv = [i for i, v in enumerate(values) if v in (6, 9)]
    still = [i for i in range(6) if i not in mv]
    b = hexagram(base).split(" ")[1].split("（")[0]
    c = hexagram(changed).split(" ")[1].split("（")[0]
    n = len(mv)
    if n == 0:
        return f"本卦 {b} 卦辞"
    if n == 1:
        return f"本卦 {b} {_line_name(mv[0], base[mv[0]])} 爻辞"
    if n == 2:
        lo, hi = mv
        return f"本卦 {b} {_line_name(lo, base[lo])}、{_line_name(hi, base[hi])} 爻辞，以上爻 {_line_name(hi, base[hi])} 为主（据《启蒙》转述）"
    if n == 3:
        return f"本卦 {b} 卦辞为主，之卦 {c} 卦辞为辅（据《启蒙》转述）"
    if n == 4:
        lo, hi = still
        return f"之卦 {c} 不变爻 {_line_name(lo, changed[lo])}、{_line_name(hi, changed[hi])} 爻辞，以下爻 {_line_name(lo, changed[lo])} 为主（据《启蒙》转述）"
    if n == 5:
        i = still[0]
        return f"之卦 {c} 不变爻 {_line_name(i, changed[i])} 爻辞（据《启蒙》转述）"
    if b in ("乾", "坤"):
        return f"{b}卦 {'用九' if b == '乾' else '用六'}"
    return f"之卦 {c} 卦辞（据《启蒙》转述）"


# ---------------- 八字 ----------------
def solar_time(date, time, lon):
    """北京时间 → 真太阳时：经度差每度 4 分钟 + 均时差（Spencer 近似）。"""
    import math
    from datetime import datetime, timedelta
    t = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    g = 2 * math.pi / 365 * (t.timetuple().tm_yday - 1)
    eot = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                    - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    delta = (lon - 120) * 4 + eot
    return t + timedelta(minutes=delta), delta


def bazi(date, time, gender, no_hour=False, lon=None):
    try:
        from lunar_python import Solar
    except ImportError:
        _dependency_missing("lunar_python", "请用户从专业排盘软件粘贴四柱+大运；禁止心算排盘。")
    if lon is not None and not no_hour:
        corrected, delta = solar_time(date, time, lon)
        print(f"真太阳时校正: 经度 {lon} → {delta:+.0f} 分钟 → {corrected:%Y-%m-%d %H:%M}")
        date, time = f"{corrected:%Y-%m-%d}", f"{corrected:%H:%M}"
    y, m, d = map(int, date.split("-"))
    hh, mm = (12, 0) if no_hour else map(int, time.split(":"))
    lunar = Solar.fromYmdHms(y, m, d, hh, mm, 0).getLunar()
    ec = lunar.getEightChar()
    print(f"公历 {date} {'（无时辰）' if no_hour else time}  →  农历 {lunar.toString()}")
    if no_hour:
        print("无时辰: 只排年月日三柱；旺衰计分不含时柱；起运岁数为近似值")
        print(f"三柱: {ec.getYear()} {ec.getMonth()} {ec.getDay()}")
        print(f"五行: {ec.getYearWuXing()} {ec.getMonthWuXing()} {ec.getDayWuXing()}")
    else:
        if lon is None:
            print("注意: 未做真太阳时校正（加 --lon 出生地经度 即可自动校正，如成都 104.07）。")
        print(f"四柱: {ec.getYear()} {ec.getMonth()} {ec.getDay()} {ec.getTime()}")
        print(f"五行: {ec.getYearWuXing()} {ec.getMonthWuXing()} {ec.getDayWuXing()} {ec.getTimeWuXing()}")
    print(f"日主: {ec.getDayGan()}")
    print(f"十神(天干): 年{ec.getYearShiShenGan()} 月{ec.getMonthShiShenGan()}" + ("" if no_hour else f" 时{ec.getTimeShiShenGan()}"))
    # 旺衰简化计分（本工具约定，非唯一流派）：月支本气生扶日主 +2、否则 -1；
    # 其余天干、年日时支（取本气五行）生扶日主各 +1、否则 -1。≥+2 偏强，≤-2 偏弱，其间中和
    gen = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
    me = ec.getDayWuXing()[0]
    helps = lambda e: e == me or gen[e] == me
    wx = [ec.getYearWuXing(), ec.getMonthWuXing(), ec.getDayWuXing(), ec.getTimeWuXing()]
    score = 2 if helps(wx[1][1]) else -1
    for i in ((0, 1) if no_hour else (0, 1, 3)):
        score += 1 if helps(wx[i][0]) else -1
    for i in ((0, 2) if no_hour else (0, 2, 3)):
        score += 1 if helps(wx[i][1]) else -1
    level = "偏强（喜克、泄、耗）" if score >= 2 else "偏弱（喜生、扶）" if score <= -2 else "中和（流派分歧，只谈倾向）"
    print(f"旺衰计分: {score:+d} → {level}")
    mother = [k for k, v in gen.items() if v == me][0]          # 生我（印）
    child = gen[me]                                              # 我生（食伤）
    wealth = gen[child]                                          # 我克（财）
    officer = [k for k, v in gen.items() if v == mother][0]     # 克我（官杀）
    if score <= -2:
        print(f"喜用（扶抑法）: {mother}（印，生我）、{me}（比劫，同我）")
    elif score >= 2:
        print(f"喜用（扶抑法）: {child}（食伤，泄）、{wealth}（财，耗）、{officer}（官杀，克）")
    else:
        print("喜用（扶抑法）: 中和，不定喜用，只按十神分布谈倾向")
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


# ---------------- 太岁 ----------------
ZHI = "子丑寅卯辰巳午未申酉戌亥"
SHENGXIAO = "鼠牛虎兔龙蛇马羊猴鸡狗猪"
LIUHAI = {frozenset(p) for p in ["子未", "丑午", "寅巳", "卯辰", "申亥", "酉戌"]}
LIUPO = {frozenset(p) for p in ["子酉", "卯午", "巳申", "寅亥", "辰丑", "戌未"]}
SANXING = [set("寅巳申"), set("丑戌未"), {"子", "卯"}]
ZIXING = set("辰午酉亥")


def taisui(birth_year, year=None):
    from datetime import date
    year = year or date.today().year
    by = ZHI[(birth_year - 4) % 12]
    ly = ZHI[(year - 4) % 12]
    rel = []
    if by == ly:
        rel.append("值太岁（本命年）")
        if by in ZIXING:
            rel.append("自刑")
    if (ZHI.index(by) - ZHI.index(ly)) % 12 == 6:
        rel.append("冲太岁")
    if any(by in g and ly in g and by != ly for g in SANXING):
        rel.append("刑太岁")
    if frozenset(by + ly) in LIUHAI:
        rel.append("害太岁")
    if frozenset(by + ly) in LIUPO:
        rel.append("破太岁")
    print(f"{year} 年流年地支: {ly}（{SHENGXIAO[ZHI.index(ly)]}年）| 生年 {birth_year} 地支: {by}（属{SHENGXIAO[ZHI.index(by)]}）")
    print("注意: 生日在立春（约 2 月 4 日）前的，生年地支要算上一年")
    print("与太岁关系: " + ("、".join(rel) if rel else "无"))


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
        _dependency_missing("ephem", "请用户从 astro.com 粘贴星盘；禁止心算行星位置。")
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
    print("主要相位（个人行星之间、及其与木星/土星，容许度 ≤6°）:")
    names = ["太阳", "月亮", "水星", "金星", "火星", "木星", "土星"]
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if a in ("木星", "土星") and b in ("木星", "土星"):
                continue  # 木土相位是同龄人共有的世代相位，不作个人解读
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
                    hits.append(f"{label}本命{target}（差 {abs(d - ang):.1f}°）")
        d = abs(transit[cn] - asc) % 360
        if min(d, 360 - d) <= 5:
            hits.append(f"合上升（差 {min(d, 360 - d):.1f}°）")
        if cn == "土星":
            d = abs(transit[cn] - natal["土星"]) % 360
            if min(d, 360 - d) <= 8:
                hits.append(f"土星回归（差 {min(d, 360 - d):.1f}°）")
        print(f"  行运{cn}: {_fmt(transit[cn])}  {'、'.join(hits) if hits else '与本命 ☉☽↑ 无紧密相位'}")


def find_pillars(year_p, month_p, day_p, hour_p=None, start=1900, end=2050):
    """反查：给定四柱（或三柱），列出公历里能对上的日期；对不上就明说"不存在"。"""
    try:
        from lunar_python import Solar
    except ImportError:
        _dependency_missing("lunar_python", "请用户提供公历生日，或从排盘软件粘贴；禁止心算反查。")
    import datetime as dt
    gz = [a + b for a, b in zip("甲乙丙丁戊己庚辛壬癸" * 6, "子丑寅卯辰巳午未申酉戌亥" * 5)]
    if year_p not in gz or month_p not in gz or day_p not in gz or (hour_p and hour_p not in gz):
        print("输入不是合法干支（应为 甲子…癸亥）。")
        return
    branches = "子丑寅卯辰巳午未申酉戌亥"
    stems = "甲乙丙丁戊己庚辛壬癸"
    hits, ymd_hits, near = [], [], []
    for y in range(start, end + 1):
        if gz[(y - 4) % 60] != year_p:
            continue
        d = dt.date(y, 1, 25)
        while d <= dt.date(y + 1, 2, 10):
            ec = Solar.fromYmdHms(d.year, d.month, d.day, 12, 0, 0).getLunar().getEightChar()
            if ec.getYear() == year_p and ec.getMonth() == month_p and ec.getDay() != day_p:
                dp = ec.getDay()
                if dp[0] == day_p[0] or dp[1] == day_p[1]:  # 只差一个字的日柱，可能是抄错
                    near.append(f"{d.isoformat()}（{dp}）")
            if ec.getYear() == year_p and ec.getMonth() == month_p and ec.getDay() == day_p:
                ymd_hits.append(d)
                if hour_p:
                    for i, br in enumerate(branches):
                        h = (i * 2) % 24
                        ec2 = Solar.fromYmdHms(d.year, d.month, d.day, h if i else 0, 30, 0).getLunar().getEightChar()
                        if ec2.getTime() == hour_p:
                            rng = "23:00-00:59" if i == 0 else f"{h - 1:02d}:00-{h:02d}:59"
                            hits.append(f"{d.isoformat()} {br}时（{rng}）")
                            break
                else:
                    hits.append(d.isoformat())
            d += dt.timedelta(days=1)
    label = " ".join(x for x in [year_p, month_p, day_p, hour_p] if x)
    if not hits:
        print(f"反查 {label}（{start}-{end}）：不存在这样的组合。")
        # 诊断最可能记错的是哪一柱（五虎遁：年干定月干；五鼠遁：日干定时干）
        m_stem = stems[(2 * (stems.index(year_p[0]) % 5) + 2 + (branches.index(month_p[1]) - 2) % 12) % 10]
        if month_p[1] in branches and m_stem != month_p[0]:
            print(f"  诊断: 月柱和年柱对不上——{year_p[0]}年的{month_p[1]}月应是 {m_stem}{month_p[1]}，月柱或年柱很可能记错。")
        elif ymd_hits and hour_p:
            h_stem = stems[(2 * (stems.index(day_p[0]) % 5) + branches.index(hour_p[1])) % 10]
            print(f"  诊断: 年月日能对上（{', '.join(x.isoformat() for x in ymd_hits[:3])}），时柱不对——{day_p[0]}日的{hour_p[1]}时应是 {h_stem}{hour_p[1]}。")
        elif near:
            print(f"  诊断: 年柱、月柱能对上，日柱最可能记错。同月里只差一个字的日柱（候选）：")
            per_year = {}
            for n in near:
                per_year.setdefault(n[:4], []).append(n)
            for items in per_year.values():
                print("    " + "；".join(items[:3]))
        else:
            print("  诊断: 年柱与月柱在此范围内没有同时出现，年柱可能记错。")
        print("  请提供公历生日，用 bazi 重排。")
        return
    print(f"反查 {label}（{start}-{end}）：可能的公历日期 {len(hits)} 个")
    for h in hits:
        print("  " + h)
    print("注意: 节气交接当天按正午判断，交节日出生请再用 bazi 核对。")


def main():
    p = argparse.ArgumentParser(
        description="cross-system-hub 占断辅助工具（tarot / iching / taisui 只用标准库；bazi、pillars 需 lunar_python；astro 需 ephem）",
        epilog="子命令详细参数：<子命令> --help。缺依赖时输出 [DEPENDENCY_MISSING] 和安装命令。")
    sub = p.add_subparsers(dest="cmd", metavar="{tarot,iching,bazi,pillars,taisui,astro}")
    t = sub.add_parser("tarot", help="抽塔罗牌：tarot [--spread single|three|relation|stakes|cross] [--no-reversed]")
    t.add_argument("--spread", choices=SPREADS, default="three")
    t.add_argument("--no-reversed", action="store_true", help="不出逆位")
    sub.add_parser("iching", help="三钱法起卦：iching（本卦 / 变爻 / 之卦 / 取辞）")
    b = sub.add_parser("bazi", help="八字排盘：bazi YYYY-MM-DD [HH:MM] --gender m|f [--no-hour] [--lon 经度]")
    b.add_argument("date")
    b.add_argument("time", nargs="?", default="12:00")
    b.add_argument("--gender", choices=["m", "f"], required=True)
    b.add_argument("--no-hour", action="store_true", help="不知道出生时辰：只排三柱，计分不含时柱")
    b.add_argument("--lon", type=float, help="出生地经度（东经为正），给出则自动换算真太阳时")
    ts = sub.add_parser("taisui", help="太岁关系：taisui 出生年 [--year 流年]")
    ts.add_argument("birth_year", type=int)
    ts.add_argument("--year", type=int, help="流年，默认今年")
    s = sub.add_parser("astro", help="星盘与行运：astro YYYY-MM-DD HH:MM --tz 8 --lat 纬度 --lon 经度")
    s.add_argument("date")
    s.add_argument("time")
    s.add_argument("--tz", type=float, default=8, help="出生地时区，北京时间=8")
    s.add_argument("--lat", type=float, required=True, help="纬度，北纬为正")
    s.add_argument("--lon", type=float, required=True, help="经度，东经为正")
    fp = sub.add_parser("pillars", help="四柱反查：pillars 年柱 月柱 日柱 [时柱] → 可能的公历日期")
    fp.add_argument("year_p")
    fp.add_argument("month_p")
    fp.add_argument("day_p")
    fp.add_argument("hour_p", nargs="?")
    fp.add_argument("--from", dest="start", type=int, default=1900)
    fp.add_argument("--to", dest="end", type=int, default=2050)
    a = p.parse_args()
    if not a.cmd:
        p.print_help()
        sys.exit(2)
    if a.cmd == "pillars":
        find_pillars(a.year_p, a.month_p, a.day_p, a.hour_p, a.start, a.end)
    elif a.cmd == "tarot":
        draw_tarot(a.spread, not a.no_reversed)
    elif a.cmd == "iching":
        cast_iching()
    elif a.cmd == "taisui":
        taisui(a.birth_year, a.year)
    elif a.cmd == "astro":
        astro(a.date, a.time, a.tz, a.lat, a.lon)
    else:
        bazi(a.date, a.time, a.gender, a.no_hour, a.lon)


if __name__ == "__main__":
    _utf8_stdio()
    main()
