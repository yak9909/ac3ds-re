---
id: ACNL-F0616
aliases:
- IDA-opus-5.5-F100
title: '待ちを外したプレビューの実測と、HHD が開かなくなった原因（2026-10-06、HIGH: 実機の計測と実機の変数）'
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。'
date: '2026-10-06'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4784-4794
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F100: 待ちを外したプレビューの実測と、HHD が開かなくなった原因（2026-10-06、HIGH: 実機の計測と実機の変数）

解析ソフト: IDA / 解析モデル: opus-5.5。
- gohan work/preview-fast 9829f64 の実測（work/logs/preview_probe_fast1.bin / _summary.txt、40 回の切り替え）:
  単独の切り替え 11 フレーム = 約 367 ms（片付け 2・待機 1・読み込み 6・準備 1・生成 1）。前（F098）は 17 フレーム約 535 ms + メニュー側の 250 ms 待ちと大きさ引き 125 ms。
  大きさ引きは 108 回中 102 回が覚え表から（0 ms）、専用スレッドで引いたのは 6 回（最長 136 ms）。ゲームのフレームは止まっていない（FrameStep 最長 1.04 ms）。
  長押しでまだ引いていない種類を通る間は「引いている途中」で何も出さない（記録しない待機になるので、押していた時間が 1 つの間隔に見える）。
- HHD式スタイル変更が開かず入力だけ止まった（利用者報告）: 実機で HhdScreen の段 = 1（Copy = 下画面 UI の退場待ち）、arc は読めている、GameList の s_holdField = 0。
  公共事業エディターを一度開くと PublicWorks::FrameStep → MapEditor::FrameStep が毎フレーム走り、マップエディターが止まっている間は毎フレーム HoldField(false) で依頼を返す（ReleaseHoldIfUnwanted、15317bd から）。旗が 1 本の共用だったので HHD の依頼も消えていた。
  修正 gohan 07dfb9f: HoldField を持ち主のビット（kHoldMapEditor / kHoldHhd）にし、誰か 1 人でも持っていれば退場させておく。未実機。

