---
id: ACNL-F0055
aliases:
- F-17
title: F-17 コードケーブとして使える範囲 — `HIGH`
summary: '`Shovel_DecideState` (`0x662E68`-`0x663450`) 内で、パッチ `0x663294 = EA000028`'
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 6696552
- 6698064
- 6697620
- 6697624
- 6697652
- 6697656
- 6697700
- 6697784
- 6697628
- 6697836
- 6697932
- 6697636
- 6619136
- 6815744
- 6698068
- 6698084
- 11401316
- 8916732
- 8916728
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:988-1011
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-17 コードケーブとして使える範囲 — `HIGH`

`Shovel_DecideState` (`0x662E68`-`0x663450`) 内で、パッチ `0x663294 = EA000028`
（無条件 B）により到達不能になった領域:

| 範囲 | サイズ | 入口 | 備考 |
|---|---|---|---|
| `0x663298`-`0x6632B4` | 28B | `0x663294` のフォールスルーのみ | `0x6632B8` は生存 |
| `0x6632E4`-`0x663338` | 84B | `0x66329C` の BEQ のみ | |
| **`0x66336C`-`0x6633CC`** | **96B** | **`0x6632A4` の BEQ のみ** | 現在ケーブとして使用 |

`0x650000`-`0x680000` (192KB) の B/BL 全走査で、`0x66336C`-`0x663454` への
分岐は 4 件のみ（`0x6632A4` からの 1 件が唯一の外部入口、残り 3 件は域内）。

**`0x663454`-`0x663464` は literal pool（`0xADF864` / `0.2f` / `0x880EFC` /
`0x880EF8` / `1.0f`）。絶対に上書きしないこと。**
`0x663464` は `DOCS/shovel_speed.md` の `scoop_swing_wait1` 速度リテラル。

**重大な依存関係**: この領域が死んでいるのは `0x663294` のパッチが前提。
`PATCHES/apply_patches.py` で revert するとケーブが**生きた経路**になり暴走する。
ケーブを外してからパッチを revert すること。

---

