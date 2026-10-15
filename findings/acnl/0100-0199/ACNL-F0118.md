---
id: ACNL-F0118
aliases:
- F-80
title: 'F-80: `BsMenuCatalog` は通常下画面メニューの `0x08/0x10` handshakeを実装しない'
summary: 'confidence: **HIGH**（`code.bin.i64` の全直接xref、`BsMenuItem` と'
date: '2026-08-24'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9739624
- 1679260
- 1679172
- 1682292
- 1682112
- 2214928
- 7156036
- 2213740
tags:
- menu
supersedes: []
source: v1:RE/FINDINGS.md:4998-5022
by: unknown
original_by: ''
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ''
---
## F-80: `BsMenuCatalog` は通常下画面メニューの `0x08/0x10` handshakeを実装しない

confidence: **HIGH**（`code.bin.i64` の全直接xref、`BsMenuItem` と
`BsMenuCatalog` のopen/update/close/endを比較）

通常持ち物 `BsMenuItem` は `MENU_FLAGS` (`0x949D68`) を次のように所有する。

- `BsMenuItem_OpenEnter` (`0x199F9C`): `0x08`を立てる。
- `BsMenuItem_OpenUpdate` (`0x199F44`): 入場完了時に`0x10`を立てる。
- `BsMenuItem_CloseEnter` (`0x19AB74`): 終了broadcast `0x20`を消す。
- `BsMenuItem_CloseUpdate` (`0x19AAC0`): `0x08/0x10`を消してscreenを破棄する。

対して `BsMenuCatalog` 範囲の同globalへの直接xrefは `BsMenuCatalog_Update`
(`0x21CC10`) にある読出し2件だけで、`0x20`を受けて自身を終了する経路である。
`0x08/0x10` のset/clearは存在しない。従ってF-78で置いた「実画面生成後にCatalogが
`0x08`を立てる」という前提は誤りであり、F-78/F-79の待機設計は本findingで置き換える。

`BsMenuMgr_Init` (`0x6D3144`) のfactory registryをscreen IDから逆引きすると、
`manager+480` がscreen `0x218` の `BsMenuTab`、`manager+500` がscreen `0x216` の
`BsHandCursor`である。`BsMenuCatalog_Init` (`0x21C76C`) が最後に隠すのは
`BsHandCursor`であり、タブではない。Catalogはtab command 6/7も発行しないため、
fieldの持ち物経路へ差し込んだ時にタブが重なるのはstock契約上の必然である。

---

