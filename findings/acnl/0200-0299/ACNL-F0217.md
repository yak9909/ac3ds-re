---
id: ACNL-F0217
aliases:
- F-192
title: 'F-192: ★★★★フラッシュは配列の `[0].w0` を破壊する。退避先はポインタ −4 — `HIGH`（静的＋実機）'
summary: '`TextDraw_EmitStatePrefix`（`0x4D5CB0`）も `DrawCtx_FlushBatch`（`0x4B8360`）も、'
date: '2026-08-30'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5070000
- 4948832
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:11746-11789
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-192: ★★★★フラッシュは配列の `[0].w0` を破壊する。退避先はポインタ −4 — `HIGH`（静的＋実機）

### 1. ヘッダシャッフル

`TextDraw_EmitStatePrefix`（`0x4D5CB0`）も `DrawCtx_FlushBatch`（`0x4B8360`）も、
流す直前に同じ入れ替えを行う。

```c
v6    = v5[3];      // 配列[0].w0 = 実データ
v5[3] = ヘッダ;      // ★ここが潰れる
v5[2] = v6;         // 元の値は「配列ポインタ − 4」へ退避
```

PICA のバースト形式が `[param0][header][params...]` なので、
**配列の実体はポインタの 12 バイト手前から始まり、`[0].w0` はヘッダ用スロットを兼ねる。**

| 配列 | ポインタ | 実体 | 退避先 |
|---|---|---|---|
| 索引 | `*(drawctx+1640)` = `drawctx+148` | `drawctx+136` | `drawctx+144` |
| 行列＋色 | `*(drawctx+1644)` = `drawctx+580` | `drawctx+568` | `drawctx+576` |
| 幾何 | `*(drawctx+1648)` = `drawctx+1108` | `drawctx+1096` | `drawctx+1104` |

**いずれも「配列ポインタ − 4」が退避先。**

### 2. ★同じ配列を 1 フレームに 2 回流すときは復元が要る

ゲーム自身は 1 回しか流さないのでこの破壊性は表に出ない。
**フラッシュを 2 回呼ぶ設計では、2 回目の前に必ず復元すること。**

```
LDR R2,[R0,#1640] / LDR R1,[R2,#-4] / STR R1,[R2]
LDR R2,[R0,#1644] / LDR R1,[R2,#-4] / STR R1,[R2]
LDR R2,[R0,#1648] / LDR R1,[R2,#-4] / STR R1,[R2]
```

復元しないと、行列 0 と追加幾何 0 の先頭ワードがヘッダのまま流れ、
**変換と UV が壊れてスプライトが描画されない**（実機で確認）。

### 3. フラッシュ後に配列を読むと「書いた値」ではない

同じ理由で、**検証は書いた直後に行うこと。**

---

