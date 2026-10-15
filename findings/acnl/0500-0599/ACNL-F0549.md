---
id: ACNL-F0549
aliases:
- IDA-opus-5-F003
title: 不可視だった UnitCursor は生のゲーム座標に置かれていた（2026-09-20、HIGH、静的＋実機、自己訂正）
summary: '解析ソフト: IDA / 解析モデル: opus-5。`tools/hw/unitcursor_hw.py:356` は node行列を'
date: '2026-09-20'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5165064
- 5166996
- 5165036
- 5178508
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4090-4111
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F003: 不可視だった UnitCursor は生のゲーム座標に置かれていた（2026-09-20、HIGH、静的＋実機、自己訂正）

解析ソフト: IDA / 解析モデル: opus-5。`tools/hw/unitcursor_hw.py:356` は node行列を
`[s,0,0,pos.x, 0,s,0,pos.y, 0,0,s,pos.z]` と組み、`pos` はプレイヤーの**生のゲーム座標**だった。
IDA-opus-5-F002 によりこの村は曲面側なので、これは別エージェントが実機で不可視を実証した配置そのもの。
さらに正しい行列は平行移動だけでなく**同じ角度のX回転**を含むため、位置と姿勢の両方が誤っていた。
**IDA-unknown-F029 が最有力候補として挙げた `node+0x228` / `+0x22C` の差は、順位を下げる。**
それは `ModelInstance_Create` の第7引数 `a7 = 3` 側でのみ観測しており、木が成功した `a7 = 1` で
測り直していない。

併せて判明した別件: 同スクリプトは instance holder を16Bゼロ埋めするだけで `0x004ED008` を呼んでおらず、
`holder+0` の vtable が0のままだった（`ModelInstance_Create` は `holder+4` と `holder+8` しか書かない）。
**ただしこれは不可視の原因ではない。** `TransformNodeHolder_SetMatrix3x4 0x004ED794` も
`UpdateWorldAndSkeleton 0x004ECFEC` も `holder+4` しか参照しないことを逆アセンブルで確認した。
破棄時に危険な欠陥であり、座標の問題とは分けて直す。

根拠: `tools/hw/unitcursor_probe.py` の S12 と `CREATE_ARGS`、`tools/hw/unitcursor_hw.py:349-361`、
`0x004ED008` / `0x004ED794` / `0x004ECFEC` / `0x004F048C` の逆アセンブル。
**2026-09-21 実機で確定（IDA-opus-5-F005）**: 曲面変換した姿勢で `UnitCursor` を置いたら出た。
`a7=1` で測り直しても `node+0x228 = 0` / `+0x22C = -1` は `a7=3` のときと同じで、しかも描けた。
**`a7` も `node+0x228`/`+0x22C` も原因ではなかった。** 残っていた反証条件は消え、確度を HIGH へ上げる。

