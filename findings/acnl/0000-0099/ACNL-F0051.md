---
id: ACNL-F0051
aliases:
- F-13
title: F-13 掘削適用は 32 スロットのレコード配列経由 — `HIGH`
summary: '`sub_5A16B0(actionID, playerIdx, item0, item1, item2, X, Y, a8, a9, a10)` が'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 10150468
- 5891508
- 10150236
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:855-869
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-13 掘削適用は 32 スロットのレコード配列経由 — `HIGH`

`sub_5A16B0(actionID, playerIdx, item0, item1, item2, X, Y, a8, a9, a10)` が
`0x009AE244`（22B × 32）の空きスロットに登録し `sub_5A0C2C` で実行する。

対して `Player_StartFieldAction` (`0x0059E5B4`) のキューは
`0x009AE15C`（18B × **4**）しかない。

**根拠**: decompile 双方。

**含意**: 複数マスを同時処理するなら `sub_5A16B0` 側を使う必要がある。
ただしセッション1でこの直接呼び出しはクラッシュした（TODO-01）。

---

