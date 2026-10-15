---
id: ACNL-F0272
aliases:
- F-249
title: 'F-249: 音量・ベロシティは振幅の 2 乗側 — `HIGH`（実機録音との数値照合 0.3dB 以内）'
summary: '`SE_ACT_FOOT_ERASE` の実機録音と自前の合成を 20ms 窓で突き合わせたところ、'
date: '2026-09-01'
category: sound
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:14549-14587
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-249: 音量・ベロシティは振幅の 2 乗側 — `HIGH`（実機録音との数値照合 0.3dB 以内）

`SE_ACT_FOOT_ERASE` の実機録音と自前の合成を 20ms 窓で突き合わせたところ、
track0（打撃音、`volume`/`velocity` とも 127）は ±3dB で一致するのに、
**track1（`volume 80`、ベロシティ 70/60/56）だけが 9〜18dB 大きすぎた。**

| ベロシティ | 線形（旧） | **2 乗** | 実機 |
|---|---|---|---|
| 70 | -9.2 dB | **-18.4 dB** | **-18.3 dB** |
| 60 | -10.5 dB | **-21.1 dB** | **-20.8 dB** |
| 56 | -11.1 dB | **-22.3 dB** | **-22.0 dB** |

→ `volume` / `expression` / `velocity` は **振幅の 2 乗側**（dB で `40*log10(v/127)`）。
`synth.VOL_POW = 2.0`。`volume`/`velocity` がどちらも 127 の音は変化しないので、
それまで一致していた打撃系の音は影響を受けない。

**先にバンク側を疑って外した記録:** 利用者の「高い音ほど音量が小さいのでは」という
仮説を確かめるため CBNK の葉 1,323 個の `+0x00`-`+0x3F` を全走査したが、
変化する欄は既知のものだけだった（`+0x04`=0x021F / `+0x1C`=32 / `+0x24`=8 は全葉で定数）。
`SE_ACT_FOOT_ERASE` が使う prog47 / prog24 はキー分割もベロシティ分割も持たず
`volume` は 127 固定。**キー依存の音量という仕組みはデータ側に存在しない。**

### 未解決の食い違い

実機は**音符の境目でくっきり段差**を持つ（各群内は ±0.2dB で平坦、境目で -2.5 / -1.2 dB）。
これはベロシティ 70/60/56 の 2 乗比と一致し、**tie 中もベロシティが効き直されている**
ように見える。しかし聴感では効き直さない側が選ばれた（`WIN_TEXT_OPEN` は tie 中に
ベロシティが 100→127 と**上がる**ので、効き直すと途中で音が膨らむ）。
`render.VEL_PER_NOTE` / `render.VEL_DOWN_ONLY` で切替可能な形で残してある。

### ★自動採点だけを信じてはいけない

`WIN_TEXT_OPEN/CLOSE` は包絡の当てはめ採点では悪化と出たが、原因は**録音のノイズ床**。
`open.wav` は末尾 200ms が **-13.9dB** で全く静かにならず、**基準として使えない**。
採点の下限を -15dB（聴こえる範囲）にすると `WIN_TEXT_CLOSE` は
2 乗の有無にかかわらず **1.05dB で完全に同じ**になる。

---

