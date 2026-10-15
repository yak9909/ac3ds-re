---
id: ACNL-F0319
aliases:
- F-295
title: F-295 (HIGH・実機) — ★方式 (a) 完成。ヒープから借りて**メニュー全体を正規経路で描いた**
summary: 道具は `PATCHES/alloc_lyt_heap.py`（確保）と `PATCHES/build_pane_tree.py`（組み立て）。
date: '2026-09-04'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5675860
tags:
- menu
- heap
supersedes: []
source: v1:RE/FINDINGS.md:18791-18844
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-295 (HIGH・実機) — ★方式 (a) 完成。ヒープから借りて**メニュー全体を正規経路で描いた**

道具は `PATCHES/alloc_lyt_heap.py`（確保）と `PATCHES/build_pane_tree.py`（組み立て）。
全文は `scratchpad/MEMO_f295_heap_menu.md`。

### ★F-221 の訂正 — 0x4000 の上限は Alloc 関数の制限ではない

`g_GfxAllocator` も `off_96F150`（nw::lyt のアロケータ）も
**同じ `ssys::ma::Allocator::Alloc`(`0x569B54`)** を使う。
**0x4000 の上限は g_GfxAllocator 側のヒープ（sead::ExpHeap）の性質**であって関数の制限ではない。
`off_96F150` は別ヒープ（`0x32C45F78`、3.7MB 級）を持ち、**64KB を一度に借りられた**。

```
sub_4B8CF0(size, align) → 借りた番地 0x32EB0F60 / 0x10000 バイト
```

### 置きかた

```
借りた領域 +0x000  共有 Material（80B）  ★全枚で 1 個
           +0x080  共有 texMap（0x40）
           +0x100  Picture[N]（1 枚 0x160）
.bss       root Pane 2 個だけ
```

**Material と texMap を全枚で共有できる**のは、F-293 で
**色が頂点カラー（`Picture+0x140`）で決まる**と分かったため。

### 実機の結果

F-282 のメニュー（パネル・見出し帯・下帯・縁・選択帯 ＋ 題名 ＋ 6 項目 = **74 枚**）が
**そのまま正しく描画された**。

```
必要 0x66C0 バイト（借りた 0x10000 で最大 185 枚）
歩いて数えた子 = 74 / 置いた 74 枚 -> 一致
node TOP 記録長 = 0x38E0 / node BOT = 0x0
```

**描画のためのコードケーブは 0 語。** 残るケーブは A1・A2（ノード登録）と F・T（drawctx 記録）だけ。

### ★手順上の落とし穴（実際に踏んだ）

**1 語ずつ `write_dbg_memory` してはいけない。**
74 枚 × 約 130 語 ≈ 12,000 回の GDB 書き込みになり **MCP が時間切れ**になった
（IDA も対象も無事。「タイムアウト＝フリーズではない」がまた当たった）。
→ **Python 側で `bytearray` に組んでから 0x1000 バイトずつ一括転送する。**
   26,816 バイトが 9 回の転送で一瞬。

### 残り

借りた領域を返す手段（アロケータ vtable +0x0C）／下画面の木／
枚数の上限（185 枚。日本語なら足りない → 借りる量を増やすか方式 b）／プラグインへの移植。

