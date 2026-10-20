---
id: ACNL-F0725
aliases: []
title: "実機で描画の資源のヒープの空きは、背景の確保の前に合計 3,196,648 バイト・最大の塊 3,196,535 バイトだった（2026-10-20、HIGH（実機の表示））"
summary: "2026-10-20 の実機で、描画の資源（字形・自作 UI）の確保の後、背景の確保の前にゲームのヒープを gohan が測った空きは、合計 3,196,648 バイト・最大の塊 3,196,535 バイト（整列 128）。"
date: 2026-10-20
category: system
build: acnl_jpn_v15
confidence: HIGH
tool: gohan の実機の状態表示（プラグイン）
addresses: [0x0096F150, 0x008FFEF8]
tags: [heap]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: haiku-5.5
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

- 実機（gohan の開発版、2026-10-20）の表示で、描画の資源を確保した後・背景を確保する前の空きは、合計 3,196,648 バイト（0x30C6E8）、最大の塊 3,196,535 バイト（0x30C677、整列 128）。
- 測ったアロケータは g_LayoutAllocator（0x0096F150）で、そのヒープは ExpHeap（ACNL-F0713 の構造）。空きは vtable 0x008FFEF8 の `get_free_size` と `get_max_allocatable_size` で取る。
- 背景の確保の結果は、依頼文の表示に無いため、この空きで足りたかは分からない。

## 根拠

- 実機の表示（写しの証拠: `_local/evidence/105/status-and-source.txt` の 1）: 「確保前の空き: 合計 3196648 / 最大の塊 3196535 バイト」。依頼文では、字形・自作 UI の 98,816 バイト（0x18200）を確保した後の値とされる。この 98,816 は表示には現れず、gohan の計算とは照合していない。
- 表示の出どころ: `src/ui/renderer/install.cpp` の `BackgroundAllocationStatusText` が「確保前の空き」を出す。測定は `src/game/lyt/recording_resources.cpp` で、必須の資源（字形・必須の画像）を流し込んだ後、背景を確保する前（`heapSpace` を呼ぶ行）。
- 測り方: `src/game/lyt/resource_api.cpp` の `Space`: `freeBytes = get_free_size(heap)`、`largestBlock = get_max_allocatable_size(heap, alignment)`（alignment は 128）。vtable は `vtbl_sead_ExpHeap_addr`（0x008FFEF8）。アロケータは `g_LayoutAllocator_addr`（0x0096F150）。SHA256 は証拠ファイルの 2。
- 数値の換算は道具で行った（証拠ファイル 3）。

## 反証条件・未確認点

- 反証条件: 表示の値が g_LayoutAllocator 以外のヒープの空きだった場合。`get_free_size` と `get_max_allocatable_size` の戻り値が、ここで書いた意味と違った場合。
- 98,816 バイトの確保後という時点は、依頼文の記述の値で、実機の表示には無い。
- 背景の確保の結果（成功か失敗か）は依頼文に無い。
- 測った後の、描画の他の確保や解放による変化は見ていない。
- 「描画の資源のヒープ」が、ACNL-F0713 の ExpHeap の 1 つに当たるという対応は、gohan の `allocator_` の取り方（`g_LayoutAllocator` を読む）からの読みで、ゲームの側で直接確かめてはいない。
- gohan の作業ツリーの版（依頼文の 028adbc との一致）は未確認（Git を使っていない）。
