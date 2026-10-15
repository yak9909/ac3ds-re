---
id: ACNL-F0035
aliases:
- F-149
title: 'F-149: 会話本文フレームを構成する6 PictureとTextBoxを、相対配置のまま複製できた — `HIGH`（静的＋実機）'
summary: F-148のcommit点を使い、list 32の末尾へ `P_bg_L_00` / `P_bg_R_00` / `P_soft_L` /
date: '2026-09-08'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5075384
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:533-555
by: unknown
original_by: ''
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ''
---
## F-149: 会話本文フレームを構成する6 PictureとTextBoxを、相対配置のまま複製できた — `HIGH`（静的＋実機）

F-148のcommit点を使い、list 32の末尾へ `P_bg_L_00` / `P_bg_R_00` / `P_soft_L` /
`P_soft_R` / `P_soft_T` / `P_soft_B` の6 Picture、続けて `T_msg_00` を追加した。
各Paneは元を0x158 bytes（TextBoxは0x108 bytes）private caveへ非所有コピーし、元の
DrawContextと更新cursorを次のdrawへ渡す。実機では本文フレームの四辺と本文が、元UIに影響せず
別位置で完全に揃って描画された。話者名の背景/文字 (`P_nam_00/01`, `T_nam_00`) は意図的に
対象外であり、複製側に表示されない。

初版は全Paneの `+0x8C/+0x9C` を背景と同じ絶対座標へ上書きし、全ての縁が中心で重なった。
停止中live値では背景基準が `(0,-73)`、左右縁が `(-143,-73)/(143,-73)`、上/下縁が
`(0,-5)/(0,-141)` と分かった。従って現行scriptは各sourceの座標へ
`target_background - source_background` を加算する。target背景 `(-50,-20)` に対する出力は
背景 `(-50,-20)`、左右縁 `(-193,-20)/(93,-20)`、上/下縁 `(-50,48)/(-50,-88)`、本文
`(-51,-21)` であり、これは独立な実行時座標読出しと実機の整列表示の双方に一致した。

`PATCHES/cave_ui_picture_clone.py` はsourceのvtable/name、TextBox batchの再利用条件、hook/cave/
全clone領域のstock状態を検証してから適用し、read-backも行うboot限定実験である。検証後に
hook `0x4D71B8`、cave、全clone bufferは復元済み。

**根拠**: F-147/F-148のstatic command-list/cursor根拠、停止中の7 source Paneの名前・vtable・
translation値、scriptのread-back、初版の中心重畳と差分版の整列表示という対照実験。

