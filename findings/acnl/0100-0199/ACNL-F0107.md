---
id: ACNL-F0107
aliases:
- F-69
title: 'F-69: 通常カタログは屋外表示可能。壊れる根因は店内限定の検索 `DICT`'
summary: 'confidence: **HIGH**（画面・注文・部屋分岐は `code.bin.i64` で静的確認。屋外起動の実機試験だけ未実施）'
date: '2026-08-24'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7150524
- 2213740
- 3110348
- 2214828
- 1985864
tags:
- catalog
supersedes: []
source: v1:RE/FINDINGS.md:4639-4666
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-69: 通常カタログは屋外表示可能。壊れる根因は店内限定の検索 `DICT`

confidence: **HIGH**（画面・注文・部屋分岐は `code.bin.i64` で静的確認。屋外起動の実機試験だけ未実施）

通常カタログ入口 `vc_CFUNCTION` (`0x6D1BBC`) は mode 0 で
`Menu_RequestOpen(124, 0)` を呼び、部屋、店舗アクター、店員NPCを検査しない。
`BsMenuCatalog` 初期化 (`0x21C76C`) は `Layout/catalog/catalogue.arc` と
`ctlg_book` / `ctlg_list` / `ctlg_T` を自前で読み、カテゴリ別一覧プロバイダもメニュー側で生成する。

`BsMenuCatalog` 範囲で `Room_GetCurrentId` (`0x2F75CC`) を呼ぶのは `0x21CBAC` の1件だけ。
`sub_5B37D0` は room 57～60 (`0x39`～`0x3C`) だけを許し、その時だけ
7204バイトの検索辞書を確保して `object+15276` に置く。通常カテゴリはこの辞書を使わない。

検索カテゴリは辞書がnullでも状態遷移を続ける。`sub_21C24C` は画面 `0x23E` の
`BsSkb` を開けるが、`sub_21C05C` は辞書がなければCRO側の非同期検索開始・結果判定を行えず、
正常に完了できない。室内実機の再配置先近傍 `0xBDF86C` には
`STR_Item_search_keyword` があり、検索が実行時CRO依存であることも一致した。

通常 mode 0 の注文処理 `sub_1E4D48` (`0x1E4D48`) は価格・品目ID、ベル、80件の注文メール枠、
`Mail_SP_Kodanuki` レコード、セーブデータを扱い、部屋判定をしない。同関数の room 161 判定は
別の mode 5 専用分岐である。

よって推奨構成は、屋外から `0x6D1BBC(0)` を呼び、店舗外では検索カテゴリだけを無効化するもの。
一覧、選択、価格、注文、終了はstock経路を維持できる。完全検索にはCRO寿命管理を含む辞書移植か、
独自検索の実装が必要。現在部屋IDの偽装は全システムへ波及するため非推奨。

詳細: `DOCS/catalog_outdoor.md`

