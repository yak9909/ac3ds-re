---
id: ACNL-F0760
aliases: []
title: "UI のレイアウトと資源は別のアロケータ変数を使い、描画命令は graphic MemoryMgr を経由する"
summary: "0x96FC3C/0x96FC40は別々のSsysMaAllocatorポインタで初期化時に同じ2D_UI_Heapを使う。0x96FC2Cはロード整列値、0x96F304は描画メモリの管理体へのポインタである。"
date: 2026-11-11
category: system
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0x96fc3c, 0x96fc40, 0x96fc2c, 0x96f304]
tags: ["heap", "layout"]
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

0x96FC3C/0x96FC40は別々のSsysMaAllocatorポインタで初期化時に同じ2D_UI_Heapを使う。0x96FC2Cはロード整列値、0x96F304は描画メモリの管理体へのポインタである。

確度MEDIUM。実測なし。各項目について命令列と、独立した呼び元・生成元・消費側またはvtable実データを照合した。

| 番地 | 付けた名前 | 型・プロトタイプ |
|---|---|---|
| `0x0096FC3C` | `g_UiLayoutAllocator` | `SsysMaAllocator *` |
| `0x0096FC40` | `g_UiResourceAllocator` | `SsysMaAllocator *` |
| `0x0096FC2C` | `g_UiResourceLoadAlignment` | `int` |
| `0x0096F304` | `g_GraphicMemoryMgr` | `T022_GraphicMemoryMgrPrefix *` |

## 根拠

- ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名はsymbolsを併読。原本code.binのSHA256はbuild台帳と一致。命令列は `tools/codebytes.py` の読取関数とCapstoneで独立照合した（`_local/evidence/146/original_asm.txt`）。型・vtable・表の原本値は同所 `bytes.json` と追加検算。作業用IDBで実測はしていない。
| 対象 | 生産・消費側の根拠 |
|---|---|
| 0x96FC3C | UiSystem_CreateSharedUiHeapAllocators0x5691F4がssys_ma_Allocator_Ctorを呼んで保存、0x12D3A4で+4に2D_UI_Heap。getter0x569170、0x4B37DC→0x4B8EBCがレイアウト割当系へ渡す。型SsysMaAllocator*。 |
| 0x96FC40 | 同じ0x5691F4が別のAllocatorを生成して同じheapを+4へ設定。getter0x5691E4→0x5671CCが+4を読みロード関数0x569EB8へ渡す。型SsysMaAllocator*。 |
| 0x96FC2C | 原本の語は0x80。0x5671BCがロード引数R2に、0x5670E8がR3に読み込む。0x5671CCでは0x569EB8の整列引数へ渡される。型int（符号付き整列値）、ポインタではない。 |
| 0x96F304 | 0x120A18はこの大域値のvt+8で割当へdispatch。vtbl_graphic_MemoryMgr0x904FA4と対応する0x6165A8はmemoryType0x10000にmanager+0x14のheap、0x20000/0x30000には+0x18/+0x1Cを使う。0x11DA78は同vtableとheap欄を構築。型は既存T022_GraphicMemoryMgrPrefix*。 |

- `ACNL-F0637`（A）・F0629（S）を既存知見として利用し、初期化と独立した消費命令を再読した。F0340（?）単独には依存しない。
- 旧版 `GameList.cpp:23`、`DecorLayout.cpp:75,76,78` と大筋一致。「読み込みのヒープの持ち主」はより正確にはAllocator自身。0x96FC3Cは既存g_LayoutAllocator0x96F150と同じ変数ではない。整列値の表記にPtrが付いていても、格納値はアドレスではない。

- 参考資料は依頼指定の旧版gohan（`_local/legacy-src/gohan-legacy/Sources`、出所は依頼文、台帳の既存キー無し）。未検証の手がかりとして用途を対比し、上記一次証拠を根拠とする。旧版本文を証拠の代わりにしない。

## 反証条件・未確認点

- heap共有はこの初期化経路での事実。全期間の同一性、空き容量、GPU寿命、割当成功は未保証。
- 上記生産/消費の値やvtableが別オブジェクト・別型を指すと判明した場合は再検討する。新しい実機確認やゲーム挙動の保証は含めない。
