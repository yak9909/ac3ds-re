---
id: ACNL-F0591
aliases:
- IDA-opus-5.5-F075
title: 'ウィンドウの中身にテクスチャがあるなら UV の組が要る（無いと nwlyt_CalcTexCoordsForGpu が落ちる）（2026-10-05、HIGH: 実機のクラッシュ + 静的）'
summary: 解析ソフト IDA（ida-pro-mcp / idalib-mcp）、解析モデル opus-5.5。T013 段 2 の実機試験。
date: '2026-10-05'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7583924
- 7583312
- 7583556
- 7584956
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4475-4488
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F075: ウィンドウの中身にテクスチャがあるなら UV の組が要る（無いと nwlyt_CalcTexCoordsForGpu が落ちる）（2026-10-05、HIGH: 実機のクラッシュ + 静的）

解析ソフト IDA（ida-pro-mcp / idalib-mcp）、解析モデル opus-5.5。T013 段 2 の実機試験。

- 症状: HHD 画面で「かみがた」（髪のモードへ切り替え = hhd_hair を初めて描く）で SIGSEGV。PC=0x73B8B4（`nwlyt_CalcTexCoordsForGpu 0x73B650` の `FLDS S2,[R1]`、
  R1 = R10 + R9<<5）、LR=0x73B744、R10=0（UV 配列の先頭）、R9=0。
- 原因: tools/hhd/make_acnl_layouts.py の wnd1 の中身を「UV 0 組」で書いていた。髪の枠（W_Frame_00C）は中身の材質に my_cmn_Base8_00 があり、
  nwlyt_Window_DrawSelf 0x73BCBC は中身を `nwlyt_CalcTexCoordsForGpu(ctx, 材質, *(win+348), ...)` で描く → 無い UV 配列を読む。
  目の枠は中身の材質にテクスチャが無く読まれないので落ちなかった（目のモードの段 1・段 2 の 1〜3 は PASS）。
- ACNL の実物: カタログの ctlg_list の W_scrn_00 / 01 は中身に texMap 1・UV 1 組（0,0,1,0,0,1,1,1）。→ 生成器は材質の座標生成の数だけ UV の組を置くよう修正
  （髪の枠 24 個 = テクスチャ 1・UV 1、目の枠 12 個 = 0・0）。designer の比較値は修正前と同じ。
- 同じ試験で、`GuiMenu::BlockGameAll` はボタンとスライドパッドだけでタッチは止めない（下の地図・タブが反応した）→ `BlockGameTouch` も呼ぶ（gohan の SyncInputLock の作り）。
- 修正版: gohan 作業ブランチの「also block the game's touch」の commit、arc 333,864 B。実機未確認。

