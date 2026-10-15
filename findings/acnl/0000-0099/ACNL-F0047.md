---
id: ACNL-F0047
aliases:
- F-09
title: F-09 掘れる/掘れないの判定は 4 段構成 — `HIGH`
summary: スコップ振り下ろしから穴が空くまでに、少なくとも 4 段のガードがある。
date: '2026-09-08'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 6696584
- 6697604
- 6819600
- 5866052
- 5866732
- 5866616
- 5866832
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:798-814
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-09 掘れる/掘れないの判定は 4 段構成 — `HIGH`

スコップ振り下ろしから穴が空くまでに、少なくとも 4 段のガードがある。

1. `0x662E88` — `[player+0x171]` bit5 が 0 なら状態を設定せず素振りのみ（段差）
2. `0x663284`〜 — `[player+0xBDE]` の状態ID で 空振り / 跳ね返り / 掘る を選択
3. `0x680F10` — 同じ bit5 チェック。0 なら `Player_BeginFieldObjAction` を呼ばない
4. `FieldObj_ResolveDigAction` (`0x598244`) 内の複数分岐
   - `0x5984EC` 汎用チェーン
   - `0x598478` cat10 経路の末端
   - `0x598550` 掘る(19) を アクション26 に上書き（岩）

**根拠**: breakpoint による経路観測 + assembly。
各段を潰すごとに失敗地点が次の段へ移動することを実機で確認した。

---

