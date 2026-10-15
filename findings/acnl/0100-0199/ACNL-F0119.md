---
id: ACNL-F0119
aliases:
- F-81
title: 'F-81: constructor成功同期版はCatalogを生成後、`0x20`で表示前に自己終了させる'
summary: 'confidence: **HIGH**（3 hookの静的制御フロー、`MENU_FLAGS`契約、直近実機症状を照合）'
date: '2026-08-24'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7168824
- 7147860
- 7170952
- 7170712
- 7170744
- 7172500
- 7168096
tags:
- catalog
supersedes: []
source: v1:RE/FINDINGS.md:5023-5049
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-81: constructor成功同期版はCatalogを生成後、`0x20`で表示前に自己終了させる

confidence: **HIGH**（3 hookの静的制御フロー、`MENU_FLAGS`契約、直近実機症状を照合）

constructor成功同期版 `PATCHES/cave_catalog_inventory_tabs_out.py` は、
`0x6D6338` で公式 `vc_CFUNCTION(0)` を要求し、`0x6D1154` の
`UiScreen_OpenById` 成功return後に `BsMenuTab_AllTabsOutEnter/Update`
(`0x6D6B88` / `0x6D6A98`)へ移る。退場完了hook `0x6D6AB8` は
`BsMenuTab_WaitMenuEndUpdate` (`0x6D7194`)へ接続する。

`0x6D7194` はgenericなscreen待機ではない。`MENU_FLAGS&0x08` が0なら直ちに
cursorを隠し、`MENU_FLAGS|=0x20`、背景・地図復帰側の状態遷移を行う。
F-80のとおりCatalogは最初から`0x08`を立てないため、タブ退場直後に`0x20`が立つ。
次の `BsMenuCatalog_Update` はそれを読んでscreenを破棄する。

従って直近の「state `0x16`、タブ退場、catalog非表示、すぐstate `0x06`へ戻って
タブ再入場、無反応な閉じるボタン」という結果は、要求失敗やconstructor失敗ではない。
Catalogは生成されたが、通常下メニュー専用の終了待機へ渡したため表示前に終了した。

残る閉じるボタンはCatalogの「やめる」ではなく、`BsMenuTab` index 10
(`B_back_00`) である。`BsMenuTab_LowerMenuSwitchUpdate` (`0x6D6060`) とcommand 6は
このindexを有効化する。表示mask/controlと論理ownerの再同期に失敗すれば、地図上へ
無反応なボタンだけが残り得る。今回どのcommand 6 writerが実際に走ったかは、動的解析を
止めているため未確定とする。

---

