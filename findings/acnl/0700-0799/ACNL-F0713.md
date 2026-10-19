---
id: ACNL-F0713
aliases: []
title: "Layout アロケータと ExpHeap の空きリスト構造"
summary: "Layoutアロケータはvptrとheapポインタを持ち、Alloc/Freeはheapの仮想関数へ引数を引き継ぐ。ExpHeapのfree/usedリストとブロックのリンク・payload長の既知部分へ型を付けた。"
date: 2026-10-19
category: system
build: acnl_jpn_v15
confidence: "MEDIUM"          # LOW / MEDIUM / HIGH
tool: IDA
addresses: [0x0096F150, 0x004B8CF0, 0x00569B44, 0x00569B54, 0x008FFEF8, 0x00133564, 0x0074D744, 0x0074DB48, 0x0055D050, 0x0055D424]
tags: ["layout", "heap"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6.1-sol
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

`g_LayoutAllocator` (0x0096F150)を `SsysMaAllocator *` とし、`nw_lyt_AllocMemory`、`ssys_ma_Allocator_Alloc/Free`、ExpHeap vtableと部分構造を型にした。確度 MEDIUM：アロケータctor/ラッパと、独立したExpHeap ctor・空き走査・確保・解放の命令が一致する。実機なし。

| 型/関数 | 確認した内容 |
|---|---|
| SsysMaAllocator (8B) | +0 vptr、+4 heapポインタ。vslot+8 alloc(this,bytes,alignment)、+0xC free(this,ptr) |
| nw_lyt_AllocMemory | `void *(unsigned int bytes, int alignment)`。大域allocatorへthisを追加して尾呼出し |
| ssys_ma_Allocator_Free | `void (SsysMaAllocator *allocator, void *pointer)`。R1のpointerを引き継ぐ |
| ExpHeap先頭0x98 | +0 vptr、+0x78 freeリスト、+0x88 usedリスト |
| 各list (0x10) | +0末尾link、+4先頭link、+8件数、+0xCブロック先頭からlinkへのoffset |
| block (0x10) | +0前/+4次link、+0xA整列ずれ、+0xC payloadバイト数。+8は未命名 |

ExpHeap型は全体サイズを断定する型ではなく、free/used両リストを含む先頭部分である。任意のheap派生がExpHeapという一般保証にはせず、この対象経路と既存 [ACNL-F0708] のvtable整合範囲を表す。

## 根拠

一次証拠：`_local/evidence/98/primary.txt`、原本bytes/vtableの `primary-index.json`、`type-verification.json`。

- `0x120DBC` はallocator vptrを保存し+4を0へ初期化。`0x4B8CF0` はbytes/alignをR1/R2へ移し、大域0x96F150をR0に読みvslot+8へ分岐する。固定0x4000上限が無いことは [ACNL-F0708] の再解析とも一致。
- `0x569B44` は `LDR R0,[R0,#4]` → heap vtable+0x1C → `BX R2`。R1を変更しないためFreeは2引数である。疑似Cに現れるthisだけの引数ではptrが欠ける。
- `0x569B54` はalign0を1にし、bytesにalignを加え、heap vtable+0x18へ尾呼出しする。R2も残るためheapへも整列指定が伝わる。typed wrapperは要求bytesを受け、内部の加算は関数本体の契約として記録する。
- 原本ExpHeap vtableの+0x18/+0x1Cは `0x55D818/0x55D424`、+0x3C/+0x40は `0x74D744/0x74D8B0`。新規に不明slotへABIを推定していない。
- `0x133564` はfree番兵をthis+0x78にし+0x78/7Cへ自己参照、+0x80件数0、+0x84 link offsetを0へ初期化。used側は+0x88/8C/90/94。一般リストでoffsetを減算して実ブロックへ戻す形が、空き走査と一致する。
- `0x74D744` は+0x7Cから辿り、番兵+0x78まで各block+0xCを合計。`0x74DB48` は同じリストを辿り、payload長と整列後に要求が入るかを判定する。総空きと最大連続空きは異なる。
- `0x55D050` はblock+0xAの整列ずれ、+0xCのpayloadを更新し、freeからunlinkして余りを戻す。`0x55D424` は整列時の戻り参照からblockを回復しused側をunlink、payloadへ整列ずれを戻してfreeへ併合する。+8の用途は今回名前にしていない。

## 反証条件・未確認点

- allocatorが実行時に別heap派生へ結び直された場合はheapフィールドの具体型を再検討する。全allocatorでExpHeapの欄を読めるとは主張しない。
- 実残量、断片化、失敗経路、解放後のGPU参照、実機の確保/解放成功は今回未確認。旧F0333等の残量標本を現在値として再利用しない。
