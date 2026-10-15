---
id: ACNL-F0607
aliases:
- IDA-opus-5.5-F091
title: '0xAA7994 はホストの枠 — 自分のプレイヤーは [自分の通信番号]（2026-10-06、HIGH: 静的（vc_PLAYERINSTANCE の索引）＋実機の症状が一致）'
summary: 解析モデル opus-5.5。
date: '2026-10-06'
category: network
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 11172244
- 6039512
- 11003792
tags:
- player
supersedes: []
source: IDA:work/FINDINGS.md:4704-4711
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F091: 0xAA7994 はホストの枠 — 自分のプレイヤーは [自分の通信番号]（2026-10-06、HIGH: 静的（vc_PLAYERINSTANCE の索引）＋実機の症状が一致）

解析モデル opus-5.5。
- 実機（hhd_t020a、ゲストで操作）: キャラクリの複製がホストのモデル、ゲストの画面ではホストが変わる、ホスト側でゲストの位置がホストの位置へ一瞬同期、本人の目の差し替えが時間切れ（rf r20）。目の形は相手へ反映しない。
- `vc_PLAYERINSTANCE 0x5C27D8` は `*(0xA7E790 + 4×(番号 + 42113))` = **0xAA7994 + 4×番号**（`tools/project.py calc`）。番号 4 以上は `vc_A_GETONLINEPLAYERINDEX` で自分に読み替える。→ 0xAA7994 は 0 番 = ホストの枠で、ゲストでは自分ではない（オフラインは 0 なので一致）。`vc_PSOFFSET(自分の番号)` と `Save_GetCurrentPlayer` は同じ `dword_AA914C`。
- gohan（HHD 画面・PlayerClone）が 0xAA7994 を自分として使っていたため、ゲストではホストの記録・vc_UPDATE・状態パケット（ホストの位置入りのバッファ）・複製・顔の差し替えになっていた。種別 11 で送ったゲスト自身のプロフィールは目の形が書かれていなかった。→ [自分の番号] に修正（gohan 400d61f）。種別 11 は相手ごとに送る（手順 9・座標同期と同じ）。
- 未修正: gohan の他機能（BuildingEditor、GridCursorGameApi）も 0xAA7994 を自分として使っている（オンラインのゲストで同じ誤りの可能性。今回の範囲外）。

