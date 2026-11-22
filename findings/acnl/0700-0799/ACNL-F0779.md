---
id: ACNL-F0779
aliases: []
title: "下画面managerの所有欄とメニュー登録リストは別の寿命を表す"
summary: "manager+472〜504は常設/動的画面の参照欄で、画面factory・actor親子・メニューリスト・描画リストは別契約。全タブ退場でmanagerの全画面が破棄されるわけではない。"
date: "2026-11-22"
category: "ui"
build: "acnl_jpn_v15"
confidence: "MEDIUM"          # LOW / MEDIUM / HIGH
tool: "exports+codebytes"
addresses: [0x6d3144, 0x1d3a84, 0x6d102c, 0x6d1b34, 0x6d1074, 0x6d1428, 0x225778]
tags: ["menu", "map", "layout"]
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

下画面managerの欄、登録メニューのリスト、actorの親子、画面factoryは別構造。MEDIUM（生成・登録・解除の独立したARM根拠と元code.binの表）。

## 根拠

- 0x1D3A84がdescriptor0x94DFC8/factory0x94FDBC/count669を登録。0x528C60→0x51EC58で子actorを作る。
- 0x6D3144はmanager+500/472/476/480へscreen0x216/217/260/218を生成し、+484/488/492/496/504を0初期化。
- 表の実名は順にBsHandCursor/BsMenuMain/BsMenuBg/BsMenuTab。BsMenuMap0x219とBsMenuRoomMgr0x261は動的。
- 0x6D102Cは0x9864FCへnodeを追加、0x6D1B34は除去。0x6D1074が見るのはopen state1とhead0のみ。
- 地図Release0x6D0E30、部屋Release0x225778、チャットRelease0x193C3Cが別々のmanager欄を0にする。
- BsMenuTabは11ボタンを内部配列（+1948/stride388）に持つ。0x6D3B98のpane/group名配列で確認。11 screenのリストではない。
- vtable0x8F3710のslot3/6/9は0x6D7E58/0x6D808C/0x6D7F58、地図0x8F3658は0x6D0928/0x6D0E30/0x6D0BF0、部屋0x8E82CCは0x22556C/0x225778/0x2256D8。元bytesで照合。
- _local/evidence/164/selected_functions.txt、xrefs.tsv、tables.json。全欄・子画面はtopics/acnl/bottom-screen-widgets.md §1。

## 反証条件・未確認点

全669profile・全子ウィジェットの内部解放の網羅ではない。+496全型と特殊部屋の全寿命は未確認。実機追試なし。
