---
id: ACNL-F0125
aliases:
- F-87
title: 'F-87: room 0の38-bank late allocationがphase 1即時失敗の最有力。容量1版を準備'
summary: 'confidence: **MEDIUM**（create/destroy経路と確保量は静的確定、容量1版の実機結果は未確認）'
date: '2026-08-24'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5987864
- 6880324
- 8515068
- 6880556
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5165-5191
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-87: room 0の38-bank late allocationがphase 1即時失敗の最有力。容量1版を準備

confidence: **MEDIUM**（create/destroy経路と確保量は静的確定、容量1版の実機結果は未確認）

`Room_GetFurnitureCapacity` (`0x5B5E18`) はroom 0に `0x26`（38）を返す。
`BsFtrMgr_CreateResources` (`0x68FC44`) は35,840-byte共通heapの後、38 bankそれぞれに
CPU 96,000 bytes、VRAM 20,500 bytes、VRAM 5,500 bytesを確保する。合計はCPU
3,648,000 bytes、VRAM 988,000 bytes（共通heapは別）。各bankのCPU pointerが1件でもnullなら
phase 1は0を返す。

`UiScreen_CreatePhases` (`0x81EDFC`) はphase 1 falseをresult 1へ変換する。
`sub_51EF38` はresult 1でnew childを直ちに破棄するため、呼出し後の
`owned=0/status=3/g_BsFtrMgr=0` と整合する。phase 2の非同期waitならchild pointerが残るため、
現在の即時消失とは一致しにくい。

第3版 `PATCHES/cave_catalog_inventory_adapter.py` は `0x68FD2C` をhookし、adapter state 2かつ
preview status 0の間だけ容量を1へ変える。Catalog previewは1 actorだけなので1 bankで足りる。
通常のroom load、既存manager利用時、Catalog終了後はstock容量を維持する。sourceの構文、
cave範囲、hook/anchorを検証し、停止中Remote GDBへ適用した。`0x68FD2C=EA5FC647`、
private preview state `0/0`、全hook/cave読戻し一致、breakpoint 0件を確認して再開済み。

実機では容量1により `owned=g_BsFtrMgr=0x33133D90`、manager `+24=1`、`+19=1` まで進んだ。
従って38-bank late allocationが以前のphase 1即時失敗を起こしていたという判定は、動的にも
支持された。以後のクラッシュは容量確保失敗ではなく、F-88のphase 1公開競合である。

---

