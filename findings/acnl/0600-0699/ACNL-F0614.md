---
id: ACNL-F0614
aliases:
- IDA-opus-5.5-F098
title: '公共事業エディターのプレビュー切り替えの実測（2026-10-06、HIGH: 実機の計測。gohan work/preview-probe 1836acd）'
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。'
date: '2026-10-06'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags:
- building
supersedes: []
source: IDA:work/FINDINGS.md:4766-4775
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F098: 公共事業エディターのプレビュー切り替えの実測（2026-10-06、HIGH: 実機の計測。gohan work/preview-probe 1836acd）

解析ソフト: IDA / 解析モデル: opus-5.5。
- 17 回の切り替え（1 つずつ・連打・長押しを含む）で、ゲームのフレームは非待機の区間で最長 36.7 ms（30fps のまま）、プレビューの FrameStep は最長 0.96 ms。**ゲームのフレームは止まっていない。**
- 切り替え 1 回（ゲーム側）はすべて 17 フレーム = 約 535 ms: 片付けの待ち 5 + 待機（揺れ止めの残り）4 + 読み込み 6（1 ファイル 2 フレーム x 3 本。依頼の次のフレームで完了）+ 準備 1 + 生成 1。うち 9 フレーム（約 300 ms）は意図的な待ち。
- その前にメニュー側で: 選択が 250 ms 止まるのを待つ（BuildingEditor kKindSettleMs）+ Resolve（RomfsIndex で 3 ファイルの大きさを引く）平均 125 ms（72〜150 ms）。合計で約 0.9 秒。
- 連打・長押しの間はプレビューへ何も頼まれない（落ち着いた最後の種類だけ）ので、両者に違いは無い（利用者の指摘どおり）。
- したがってスレッドを分けても速くならない。縮められるのは待ち（250 ms + 9 フレーム）、Resolve（125 ms）、読み込みの順次（6 フレーム）。
- 記録: work/logs/preview_probe_run1.bin / _summary.txt。道具: tools/dynamic/dump_preview_probe.py・summarize_preview_probe.py。

