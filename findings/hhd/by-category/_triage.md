<!-- 生成物。編集しない（kb.py index が作り直す） -->

# hhd / _triage

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| HHD-F0002 | 髪のページ送り — ドラッグ・弾き・滑りの規則（2026-10-05、MEDIUM: 静的のみ。定数はすべて逆アセンブルの即値・リテラル） | 解析モデル opus-5.5。IDB に関数 30・状態のグローバル 9 を命名、注記 6、保存。 | MEDIUM | S |
| HHD-F0004 | キー番号とページ送り（2026-10-05、MEDIUM: 静的のみ。ビットの意味は ACNL の実測表との照合） | `PadKeyId_ToSeadMask 0x43E23C`（20 通りの分岐表、行き先の MOV 即値を Python で読んだ）と ACNL の sead ビット表（reference/old_project/DOCS/input_block.md）が並びで一致。 | MEDIUM | S |
| HHD-F0005 | 画面全体の流れとプレイヤーの見た目の並び（2026-10-05、MEDIUM: 静的のみ） | `CharaCreate_MainCalc 0x1EE0F8` の処理順（切替 → 目の色 → 髪の色 → 肌の色 → 目 → 髪・ページ・けってい）。docs/hhd/chara_create_screen.md 6 章。 | MEDIUM | S |
| HHD-F0006 | 髪のページの作り（2026-10-05、MEDIUM: 静的のみ） | `CharaHairBaseLayout_RefreshPages 0x35D954`: 髪 32 個（B 0-15 / G 16-31）を 1 ページ 8 個で 3 枚のページ枠に回して貼る。+304 で性別の 16 個に絞る。 | MEDIUM | S |
| HHD-F0007 | ボタンの状態機械は実名 ButtonBaseActor（2026-10-05、MEDIUM: 静的のみ。状態名・アニメ名の文字列と処理の照合） | 静的初期化 0x5BC318 が "ButtonBaseActor::StateID_Init" ほか 17 状態を登録（RTTI の代わりに実名が残る数少ない場所）。 | MEDIUM | S |
| HHD-F0010 | 配置・版・RTTI の有無（2026-10-05、HIGH: ヘッダ・全バイト照合・全数検索） | cci 2 本: 無印 = TitleVersion v0、Rev 1 = v2080（exheader remaster 2）。利用者の RomFS フォルダ 2 本は ctrtool の抽出と全ファイル一致（v1.0 16,632 / v1.1 16,693）。 | HIGH | S |
| HHD-F0012 | 品番 → モデル名・アイコン、家具リストの資源（2026-10-06、MEDIUM: 静的 + ROM の実データ） | `Item_GetParamIndex` 0x588350: (id & 0x7FFF) − 0x2000（≤ 0x1740）。`Item_GetModelName` 0x440978 = `g_ItemModelNameTable` 0x653EF4[番号]（5,953 件、無ければ "none"）。 | MEDIUM | S |
| HHD-F0013 | 家具・壁紙/床のカタログの窓と地（2026-10-06、MEDIUM: 静的 + レイアウトの実データ） | カタログのモード名の列挙（0x761FE4、`sub_50801C` が使う）: None, DataStore, CustomerList, OrderList, RemakeMenu, CatalogTrash, CatalogAudio, CatalogOrgel, CatalogCloth, CatalogSearch, **CatalogFtrNormal（家具）, CatalogFtrWall（壁紙）, CatalogFtrRag（床）**, CatalogFtr | MEDIUM | S |
| HHD-F0017 | ゴミ箱の当たりの判定（2026-10-07、MEDIUM: 静的のみ） | 解析ソフト: IDA / 解析モデル: opus-5.5。T022 のゴミ箱の当たりを HHD と同じにするため。 | MEDIUM | S |
| HHD-F0018 | 模様替え画面の上段のタブと家具リストの部品（2026-10-07、HIGH 相当: レイアウトの実データ + スクショ 4 枚と一致） | 解析ソフト: IDA（資源は 3DSkit の展開 + BFLYT の prt1 の生バイト）/ 解析モデル: opus-5.5。T022。 | HIGH | S |
