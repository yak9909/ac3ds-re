---
id: ACNL-F0061
aliases:
- F-23
title: F-23 進行中アクションテーブル `0x9AE1A4` — `HIGH`
summary: 5 バイト × 32 エントリ。`g_FieldActionQueue`(`0x9AE15C`, 18B×4) の直後に隣接する
date: '2026-09-08'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 10150308
- 10150236
- 5896948
- 5897468
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1243-1268
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-23 進行中アクションテーブル `0x9AE1A4` — `HIGH`

5 バイト × 32 エントリ。`g_FieldActionQueue`(`0x9AE15C`, 18B×4) の直後に隣接する
（`0x9AE15C + 72 = 0x9AE1A4`）。

| offset | 内容 |
|---|---|
| `[0]` | X |
| `[1]` | Y |
| `[2]` | playerNo（**165 = 空き**の番兵） |
| `[3]` | フラグ（bit0..3 = プレイヤー別、bit4 = 特定アクション種別） |
| `[4]` | actionID |

- `FieldAction_FindActive(X, Y, playerNo)` (`0x59FAF4`) — 3 つすべて一致する
  エントリの index を返す。無ければ `-1`。`playerNo == 165` は自プレイヤーに読み替え
- `FieldAction_RegisterActive(actionID, X, Y, playerNo, a5)` (`0x59FCFC`) —
  `[2] == 165` の空きを探して登録。空きが無ければ `-1`

**根拠**: 両関数の decompile と、実機ダンプ（使用中 1 件 `X=64 Y=19 playerNo=0 actionID=19`、
空き 31 件）。

**含意**: 8 マス同時掘りのボトルネックは**このテーブルではなく 18B キューの 4 スロット**。
こちらは 32 エントリあり余裕がある。

---

