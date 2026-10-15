<!-- 生成物。編集しない（kb.py index が作り直す） -->

# hhd / ui

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| HHD-F0002 | 髪のページ送り — ドラッグ・弾き・滑りの規則（2026-10-05、MEDIUM: 静的のみ。定数はすべて逆アセンブルの即値・リテラル） | 解析モデル opus-5.5。IDB に関数 30・状態のグローバル 9 を命名、注記 6、保存。 | MEDIUM | S |
| HHD-F0005 | 画面全体の流れとプレイヤーの見た目の並び（2026-10-05、MEDIUM: 静的のみ） | `CharaCreate_MainCalc 0x1EE0F8` の処理順（切替 → 目の色 → 髪の色 → 肌の色 → 目 → 髪・ページ・けってい）。docs/hhd/chara_create_screen.md 6 章。 | MEDIUM | S |
| HHD-F0006 | 髪のページの作り（2026-10-05、MEDIUM: 静的のみ） | `CharaHairBaseLayout_RefreshPages 0x35D954`: 髪 32 個（B 0-15 / G 16-31）を 1 ページ 8 個で 3 枚のページ枠に回して貼る。+304 で性別の 16 個に絞る。 | MEDIUM | S |
| HHD-F0007 | ボタンの状態機械は実名 ButtonBaseActor（2026-10-05、MEDIUM: 静的のみ。状態名・アニメ名の文字列と処理の照合） | 静的初期化 0x5BC318 が "ButtonBaseActor::StateID_Init" ほか 17 状態を登録（RTTI の代わりに実名が残る数少ない場所）。 | MEDIUM | S |
| HHD-F0008 | キャラクリ画面のコード — 組み立て・絵の差し替え・色の反映・選択グループ（2026-10-05、MEDIUM: 静的のみ。実機未観測） | 解析ソフト: IDA 9.3（idalib、`ida/db/hhd_jpn_v11.i64`）＋ objdump / 解析モデル: opus-5.5。根拠は逆アセンブル・文字列・静的初期化と資源の照合。 | MEDIUM | S |
| HHD-F0009 | キャラクリ画面の資源 — レイアウト・部品・色の表・状態アニメ（2026-10-05、HIGH 相当: ファイルそのものを 3DSkit で読み、2 本のスクショと配置・色が一致） | 解析ソフト: 3DSkit（Tyulis、commit 2fb6077）＋要約スクリプト / 解析モデル: opus-5.5。 | HIGH | S |
| HHD-F0011 | HHD は G_Loop と loop を持つレイアウトで繰り返しのアニメを常に再生する（2026-10-05、MEDIUM: 静的のみ） | 解析モデル opus-5.5。`LayoutObj_StartLoopAnim 0x354170`（命名）は `FindGroup(G_Loop)` と anim `"loop"` があれば結んで再生し、+600/+604 に引数を残す。 | MEDIUM | S |
| HHD-F0013 | 家具・壁紙/床のカタログの窓と地（2026-10-06、MEDIUM: 静的 + レイアウトの実データ） | カタログのモード名の列挙（0x761FE4、`sub_50801C` が使う）: None, DataStore, CustomerList, OrderList, RemakeMenu, CatalogTrash, CatalogAudio, CatalogOrgel, CatalogCloth, CatalogSearch, **CatalogFtrNormal（家具）, CatalogFtrWall（壁紙）, CatalogFtrRag（床）**, CatalogFtr | MEDIUM | S |
| HHD-F0014 | 模様替え画面の状態とゴミ箱への落とし（2026-10-06、MEDIUM: 静的のみ。途中） | 模様替え画面（家具を置く画面）の本体は 0x3EA990〜0x3F2xxx のクラス。vtable は 0x6EF998〜0x6EFAB4（手前 2 語 0,0。直後に offset-to-top −8 の第 2 vtable）。 | MEDIUM | S |
| HHD-F0017 | ゴミ箱の当たりの判定（2026-10-07、MEDIUM: 静的のみ） | 解析ソフト: IDA / 解析モデル: opus-5.5。T022 のゴミ箱の当たりを HHD と同じにするため。 | MEDIUM | S |
| HHD-F0018 | 模様替え画面の上段のタブと家具リストの部品（2026-10-07、HIGH 相当: レイアウトの実データ + スクショ 4 枚と一致） | 解析ソフト: IDA（資源は 3DSkit の展開 + BFLYT の prt1 の生バイト）/ 解析モデル: opus-5.5。T022。 | HIGH | S |
