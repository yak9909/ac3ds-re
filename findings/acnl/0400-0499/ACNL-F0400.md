---
id: ACNL-F0400
aliases:
- F-373
title: 'F-373（2026-09-08）: ON直後クラッシュ。無罪のものとフック抜きビルド'
summary: 利用者の申告： チートONの瞬間にクラッシュ（項目は触っていない）。
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 5555256
- 5556296
tags:
- hook
supersedes: []
source: v1:RE/FINDINGS.md:24117-24139
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-373（2026-09-08）: ON直後クラッシュ。無罪のものとフック抜きビルド

利用者の申告： チートONの瞬間にクラッシュ（項目は触っていない）。
実機値： PC=`0x0054C438`（前回と同一）、R4=`0x0`、要求なし、
部屋 `0x63`。保存R4=`0x32939880`（正常）・保存LR=`0x0054C848`
（MainLoop）・入力系 2 語は素（入力遮断は入っていない）。

### 確定したこと

- 入口R4は正常で、+0x04 以降 +0x14 までに R4 が NULL 化した。
  書けるのは +0x10 の分岐だけだが実体は R1/R3 のみ。
  よって入口 R0（＝呼び出し元の this）が NULL。2 回とも変動（0x18/0x0）。
- 入力遮断の 2 語は素。入力遮断は無罪。
- 発火は起きていない（項目OFF・要求なし）。UseExit・通知は無罪。

### 残る軸とフック抜きビルド

チートON状態の残り： A1/A2 ノード・メニュースレッド・
しずえフック存在・フォント/木（受動）。`OwnGuiToggle` の
`ShizueSkip::Install()` を外した診断ビルドを用意（検証器 2 種 0 件）。
これで落ちればフック存在は無罪、落ちなければ有罪。
診断が済んだら呼び出しを戻すこと（コードに注記済み）。

