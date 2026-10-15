---
id: ACNL-F0120
aliases:
- F-82
title: 'F-82: Catalog終了はfield X ownerを戻さず、3D経路には屋外hard rejectがない'
summary: 'confidence: **HIGH**（Catalog end、field X開始、通常持ち物終了の静的比較）、'
date: '2026-08-24'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 2206204
- 6884904
tags:
- catalog
supersedes: []
source: v1:RE/FINDINGS.md:5050-5076
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-82: Catalog終了はfield X ownerを戻さず、3D経路には屋外hard rejectがない

confidence: **HIGH**（Catalog end、field X開始、通常持ち物終了の静的比較）、
**MEDIUM**（屋外でのpreview actor生成可否はruntime factory状態が未採取）

field Xは `sub_165B40 -> sub_5C1F08 -> sub_65945C` でplayerをstate `0x16`へ移し、
field controllerをstate 5へ進める。通常持ち物の終了側には
`sub_672CAC -> sub_650F3C` があり、playerをstate `0x06`へ戻す。

Catalogの終了は自身のlayout/provider/previewを解放し、`BsMenuBg` をkind 0へ戻し、
`byte_949D23=1`などを更新するだけである。tab command、`BsHandCursor_Show`、
player/controller復帰、地図復帰を行わない。従って過去の「やめる」後のstate `0x16`と
下画面lockはCatalog destructorの失敗ではなく、field X ownerとCatalog ownerの非対称である。

3Dは `BsMenuCatalog_UpdatePreview` (`0x21A9FC`) から `CatalogPreview_UpdateActor` (`0x690E28`)へ進む。
最初のgateはCatalog mode 0と有効な選択indexで、現行パッチは公式mode 0入口を使うため、
最新の3D非表示をmode未設定だけでは説明できない。その先にはitem適格性、ItemParam、
`g_BsFtrMgr` の生成完了、actor bank、model resourceが必要である。
村room 0／商店街room 1は拒否bit `0x10000`を持たず、静的には屋外を一律拒否しない。
actor typeはItem.binの家具familyから固定tableで選ばれ、room用factoryを要求しない。
stock room 0に無いのはtype `0xEE` のmanager objectである。

詳細なクラス構成、11タブ、27状態、command writer、終了契約、実験対照表は
`DOCS/menu_system.md` にまとめた。本finding作成中は停止中の実機へ一切アクセスしていない。

---

