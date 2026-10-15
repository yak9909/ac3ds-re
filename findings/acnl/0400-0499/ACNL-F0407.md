---
id: ACNL-F0407
aliases:
- F-380
title: 'F-380（2026-09-08）: タイトルON後は正常動作。スレッド特定も確定'
summary: 利用者の申告： 現行 3gx では ON だけでは落ちない。
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:24280-24293
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-380（2026-09-08）: タイトルON後は正常動作。スレッド特定も確定

利用者の申告： 現行 3gx では ON だけでは落ちない。
実機値（チートON・無操作・Suspend）： 部屋 `0x5E`、全スレッド正常。

- 21 スレッド。カレント 364 の PC=`0x07057BB0` を `addr2line` すると
  `svcSleepThread`（メニュースレッドの 16ms 待ち）。固まりではない。
- 355 は `svcArbitrateAddressNoTimeout`（正常待ち）、327 はゲーム側。
  3 点とも正常系。ウェッジなし。
- よって F-375（空リスト修正）後のビルドでは ON 直後のクラッシュは
  起きていない。F-375 が効いた可能性が高い（未確定・遷移試験が残る）。
- Game Patching ON 時代の証拠（R4=`0x18`、0x420 の AND 語）は
  汚染の疑いが濃い。以後は Patching OFF を前提にし、番号を振り直さない。

