---
id: ACNL-F0544
aliases:
- IDA-opus-5-F006
title: 親ヒープの残りは実測できる。確保量は35倍過大だった（2026-09-21、HIGH、実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。2 体目の資源ヒープ `0x40000` が **0 を返して失敗**した。'
date: '2026-09-21'
category: system
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9751624
- 9436920
- 7657284
tags:
- heap
supersedes: []
source: IDA:work/FINDINGS.md:3973-3997
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F006: 親ヒープの残りは実測できる。確保量は35倍過大だった（2026-09-21、HIGH、実機）

解析ソフト: IDA / 解析モデル: opus-5。2 体目の資源ヒープ `0x40000` が **0 を返して失敗**した。
ガードが次段への伝播を止めたので実害は無い（この経路は過去にゲームを落としている）。
原因は推測せず測った: 親ヒープ `[0x0094CC48]` = `0x301668EC` は RTTI で **`sead::ExpHeap`**
（vtable `0x8FFEF8`、TypeInfo 経由で `N4sead7ExpHeapE`）。その vtable **スロット15 = `0x0074D744`**
が `getFreeSize()`（`+124`→`+120` の自由リストを歩き各ノードの `+12` を合計するだけ。ロック以外の副作用なし）。

呼んだ結果:

| ヒープ | 確保 | 実使用 | 事前計算 |
|---|---|---|---|
| 親 | — | **残り 109,976 B**（要求 262,144 B に不足） | — |
| A 資源 `0x40000` | 262,144 B | **7,544 B** | `book.bcres` 7,040 B ＋ 諸経費 504 B |
| A instance `0x20000` | 131,072 B | **1,400 B** | `model_preflight` の **1,396 B** |

**`model_preflight.py` の instance バイト数が実機と 4 B 差で一致した**（当てはめではなく
ゲーム自身の問い合わせ経路を Unicorn で回した値なので、道具の検算になっている）。
これを根拠に 2 体目を資源 `0x8000` / instance `0x2000` にして成功。
**以後、ヒープは「ファイル長＋1 KiB」と `model_preflight` の値から決め、`0x40000`/`0x20000` を惰性で使わない。**

根拠: 本文の呼び出し記録（`events.jsonl` の `measure_parent_free` / `measure_a_res_free` /
`measure_a_inst_free`）、`run3_result.json` の `heap_measurements`、`0x74D744` の逆アセンブル。
反証条件: `getFreeSize` が断片化を無視している、別スレッドが同時に確保している。

