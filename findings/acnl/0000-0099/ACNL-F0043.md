---
id: ACNL-F0043
aliases:
- F-05
title: F-05 アニメ名テーブル基準は `0x0085FFB0` — `HIGH`
summary: 16B × 約1028（終端未検証）。`+0` 未使用 / `+4` 本体名 / `+8` `_e1` / `+12` `_m1`。
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8781744
- 8781760
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:723-737
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-05 アニメ名テーブル基準は `0x0085FFB0` — `HIGH`

16B × 約1028（終端未検証）。`+0` 未使用 / `+4` 本体名 / `+8` `_e1` / `+12` `_m1`。

**根拠**: memory 実読で idx 0 が全ゼロエントリ、idx 1 が `scoop_wait1` と確認。
実機で速度リテラルを書き換え、どの動作が変化するかを観測して ID 対応を確定。

**注意**: 「名前ポインタが非NULLの最初のエントリ」を先頭とすると `0x85FFC0` になり、
全 ID が 1 ずれる。セッション1で実際に誤り、実機検証で発覚した。

スコップ帯: 71 `swing1` / 72 `swing_wait1` / 73 `dig1` / 74 `hane1` /
75 `suka1` / 76 `stump1` / 77 `get1` / 78 `putaway1` / 79 `bury1`。

---

