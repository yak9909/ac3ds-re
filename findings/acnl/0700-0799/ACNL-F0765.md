---
id: ACNL-F0765
aliases: []
title: "0x94CC48 は子ヒープの親になる sead::ExpHeap へのポインタ（0x94CC68 は別の建物用ヒープ）"
summary: "0x94CC48 は sead::ExpHeap（15,433,728 B）へのポインタ変数 void**。BsLightMgr_Create など約 350 箇所が子ヒープの親として読む、起動後に設定される共有の親ヒープ。0x94CC68 は別の建物用ヒープ変数。"
date: 2026-11-11
category: _product
build: acnl_jpn_v15
confidence: HIGH          # LOW / MEDIUM / HIGH
tool: IDA
addresses:
  - 0x94CC48
tags:
  - heap
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: sonnet-5.5
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

0x94CC48 は大域変数 `g_ParentHeap`（型 `void **`）。中身は sead::ExpHeap（総量 15,433,728 B）で、各マネージャが自分の子ヒープを作るときの親として渡す。0x94CC68 は別の変数で、建物用の ExpHeap（607,948 B）。確度 HIGH（実機の読み取りと静的な読み手の両方）。

## 根拠

- 実機の読み取り（ACNL-F0513、F0454、F0544）: `*(0x94CC48)` は ExpHeap（RTTI で確認）、`*(0x94CC68)` は 607,948 B の別ヒープ。
- 静的: xrefs が 356 件。例として 0x190D28 BsLightMgr_Create は `Heap_CreateNamed_0(a1+20, 204800, dword_94CC48, "BsLightMgr", 1, 0)` と、親ヒープの引数に 0x94CC48 の値を渡す。ほかに BsShadowViewMgr_Create（0x28FE24）、BsShadowMapMgr_CreateResources（0x264C08）、BsMenuCatalog_Init（0x21C76C）、dFieldFactory_Create（0x201208）、PwpPreview_LoadSlot（0x227CFC）などが読む。
- ファイルのイメージ上の値は 0（0x94CC48・0x94CC68 とも）。実行時に設定される。
- 旧版 gohan の `kParentHeap` と同じ番地。

## 反証条件・未確認点

- 書き込み元（起動時の初期化）は特定していない。356 件のうち書き込みを見分けていない。
- 0x94CC68 との親子関係は確かめていない。別の変数で別の ExpHeap であることまでが根拠。
- 名前の `g_ParentHeap` は役割の名前で、ゲーム内の実名ではない。
