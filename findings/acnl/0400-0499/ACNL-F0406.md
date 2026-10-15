---
id: ACNL-F0406
aliases:
- F-379
title: 'F-379（2026-09-08）: 訂正 — 謎の構成は自前の診断フラグだった'
summary: F-378 を撤回する。A1/A2 素＋shizueフック入り＋入力入り＋メニュー起動中は、
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 1273956
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:24266-24279
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-379（2026-09-08）: 訂正 — 謎の構成は自前の診断フラグだった

F-378 を撤回する。A1/A2 素＋shizueフック入り＋入力入り＋メニュー起動中は、
どのビルドとも一致しないのではなく、**現行ツリーそのもの**
（`kDiagNoHooks=true` で A1/A2 を入れず、しずえフックは戻し済み）だった。
他エージェントの干渉の疑いは取り下げる。利用者の否定を受け入れ、
以後はセッション共有を前提にしない（混線の実績はプロキシの artifact 扱い）。

### 素の基準点（再起動・チートOFF・タイトル Suspend）

停止中・PC=`0x00137064`（通常の待ち位置）・R4 正常・部屋 `0x5E`。
sh/A1/ib1 すべて素。ここからチートON→無操作で PC 3 点読みを行い、
ウェッジ（同一 PC に停滞）と正常待機を分ける。

