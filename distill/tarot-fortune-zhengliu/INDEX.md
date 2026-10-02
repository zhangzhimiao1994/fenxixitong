# INDEX — skill 关系图

```
cross-system-hub
 ├─ psyche ──────────── composes-with → freud-hub, jung-*
 ├─ huangdi-neijing
 ├─ tarot
 │   ├─ tarot-draw-protocol ── depends-on: (none) ── contrasts-with: zhouyi-divination
 │   ├─ tarot-card-meaning ─── depends-on: tarot-draw-protocol
 │   ├─ tarot-spread-synthesis ─ depends-on: tarot-card-meaning
 │   └─ tarot-projective-dialogue ─ composes-with: psyche, jung-complex-archetype, freud-anxiety-defense
 ├─ fortune
 │   ├─ bazi-liunian ──── composes-with: five-elements-network, chijiuzhan-san-jieduan
 │   ├─ astrology-transit ─ composes-with: jung-libido-individuation, jung-persona-self
 │   └─ ziwei-doushu ──── contrasts-with: bazi-liunian（同样基于出生时间，侧重领域地图）
 ├─ zhouyi
 │   └─ zhouyi-divination ─ depends-on → hexagram-situation-diagnosis, line-position-timing, auspicious-risk-language
 └─ mao-thought（引擎）── maodun-fenxi, diaocha-yanjiu, jianmiezhan-jizhong-bingli, tan-gangqin, chijiuzhan-san-jieduan, neiyin-juedinglun
```

| 关系 | 说明 |
|------|------|
| tarot-draw-protocol ↔ zhouyi-divination | contrasts-with：同为随机取象；塔罗看内在态度，起卦看事情态势；共用"再三渎"规则 |
| fortune → zhouyi-divination | 无出生信息时的替代入口 |
| bazi-liunian ↔ astrology-transit | 周期对照（大运交接 / 土星回归），仅作类比，不等价 |
