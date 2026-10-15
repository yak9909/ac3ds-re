---
id: ACNL-F0648
aliases:
- Ghidra-gpt-sol-5.6-F010
- G-F010
title: inventory drop完了はFieldAction handleのstatus 2待ちで成立する
summary: '**確度: HIGH（添付bytesの命令列＋実機症状が一致）。**'
date: '2026-09-19'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 5891508
- 10150236
- 5857412
- 5860484
- 1683508
- 2883212
- 9789428
- 3286352
- 1683704
- 2546460
- 1683728
- 8478348
tags:
- inventory
supersedes: []
source: Ghidra:work/FINDINGS.md:214-260
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F010: inventory drop完了はFieldAction handleのstatus 2待ちで成立する

**確度: HIGH（添付bytesの命令列＋実機症状が一致）。**

ユーザー実機観測:
- 足元へドラッグ&ドロップするとfield側dropは実行される
- 元Itemは持ち物slotに残る
- ドラッグ中iconがdrop直前位置で停止
- BsMenuItemが操作不能になる

この症状は、現行balloon ARが `Player_DropItem` のreturn contractを破っていることで直接説明できる。

`Item_PlaceItem @ 0x59E5B4` は `g_FieldActionSlots @ 0x9AE15C` の4 slotからfree entryをallocateし、そのslot index `0..3` をreturnする。entry strideは `0x12`、type byteは `+0x0E`、status byteは `+0x0F`。free slotなしは `-1`。

したがって `Player_DropItem @ 0x596084` の非負returnはboolではなく **FieldAction completion handle**。

`FUN_0019AD30` はそのreturnを `BsMenuItem+0xD8` に保存し、後続 `FUN_0019AF8C` が毎frame `FUN_00596c84(handle)` をcallする。

`0x596C84` は `0x9AE15C + handle*0x12` のstatusを返す。BsMenuItem側は:
- status 0/1: 待機継続
- status 3: error処理
- status 2: 成功完了処理

status 2時、`0x19B034` で `0x2BFE8C` を `selectedSlot, g_EmptyItem(0x955FF4)` 付きでcallする。下位 `0x322550` が実際に4-byte Itemをinventory slotへcopyするため、ここで元slotがempty化される。

その後:
- `0x19B0F8 -> 0x26DB1C`: slot icon再読込
- `0x19B110 -> 0x815E8C`: BsMenuItem内部state遷移

を実行する。

現行balloon ARはcustom成功時に固定 `r0=1` をreturnするが、その経路では `Item_PlaceItem` を呼ばずslot 1をallocateしていない。よってBsMenuItemは無関係なslot 1を監視し、通常freeならstatus 0のまま永久待機する。

これにより:
- Itemが消えない
- drag iconが更新されない
- UI stateが進まない

を全て説明できる。

Player state `0x16 -> 0x06` はこの待機不整合の二次効果か独立副作用か未確定。まずcompletion handle contractを修復してから再評価する。

**修正候補（MEDIUM）:** `Item_PlaceItem` のtype `0x10` はslot allocate後にstatus=2を即設定し、dispatchせずhandleを返す。field配置なしのcompletion tokenとして利用できる可能性があるが、実機副作用未確認のためまだARへ反映しない。

根拠: `docs/inventory_menu.md`、`work/evidence/inventory_menu_20260915.md`。


