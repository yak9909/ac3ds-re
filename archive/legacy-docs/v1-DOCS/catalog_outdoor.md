# カタログ注文画面の屋外表示

対象は JPN 版（Title ID `0004000000086200`）の通常カタログ、すなわち
家具などを一覧から選んで注文する `BsMenuCatalog` の mode 0 である。

## 結論

**通常の一覧表示・品目選択・価格確認・注文は、屋外でも成立する可能性が高い。**
2Dレイアウトと品目プロバイダはメニュー自身が生成し、起動入口にも部屋判定はない。

ただし、家具カテゴリの選択中に表示される家具モデルは2Dメニューだけでは完結しない。
`BsFtrMgr` の子として家具アクターを1体生成するが、stockの村room 0はこのmanagerを生成しない。
room 0に38枠の容量値があることと、manager objectが存在することは別である。

Catalog camera、Catalog専用3灯、Catalog用render layer 2は屋外にも存在する。
従って3D成立の不足要素は描画基盤ではなく `BsFtrMgr` の生成と、その3段階初期化完了後に
preview actorを生成する順序である。詳細は [`furniture_rendering.md`](furniture_rendering.md) に分離した。

屋外で壊れる主要因は、6番目の「検索」カテゴリだけが使う **店内限定の検索辞書** である。
メニュー初期化は現在部屋が `0x39`～`0x3C` の場合に限り、7204バイトの `DICT`
オブジェクトを生成する。屋外ではこのポインタが null のままなのに検索状態へは遷移できるため、
ソフトウェアキーボードの後段が検索完了条件を満たせず、ループ、戻り、無反応などの壊れ方をする。

したがって最も安全な実現方法は、**mode 0 の画面を通常どおり開き、屋外では検索カテゴリだけを
無効化する**ことである。完全な検索を屋外でも使うには、店内CROの寿命管理を含めて辞書を移植するか、
検索処理を独自実装する必要がある。

## 解析方法

- 静的解析の主根拠: `code.bin.i64`（idalib）
- 補助照合: `code_runtime.elf.i64`
- 動的照合: Remote GDB で手動 suspend 済みの実機プロセス
- 外部実装との照合: ローカルに保存された Vapecord ソース

`code_runtime` や実機メモリは静的結論の代用にはせず、実行時ポインタ、CROスタブの再配置先、
現在開いているオブジェクトの型を照合するためにだけ使用した。

## 画面の入口と構成

### 起動入口

`vc_CFUNCTION` (`0x6D1BBC`) は引数をカタログモードとして受け取る。
mode 0 では次を行う。

（疑似C を省略。原本は _local/legacy-src/…）

この関数には現在部屋、店舗アクター、店員NPCの判定がない。Vapecord の `Game::Catalog()` も
プレイヤーを idle にし、通常メニューを開いた後、USA版の対応入口 `0x6D33D8` を mode 0 で呼ぶ。

### `BsMenuCatalog`

| 項目 | 値 |
|---|---|
| コンストラクタ | `0x21D0A0` |
| 確保サイズ | `0x3BB0` |
| 初期化 | `0x21C76C` |
| 更新 | `0x21CC10` |
| 描画 | `0x21C6A4` |
| 終了処理 | `0x21CF20` |
| primary vtable | `0x8E8028` |
| secondary vtable | `0x8E8094` |

初期化は `Layout/catalog/catalogue.arc` を読み、`ctlg_book`、`ctlg_list`、`ctlg_T`
の各レイアウトをメニュー内部に構築する。mode 0 のボタン設定とカテゴリ作成も同じ初期化内で行う。

品目一覧はカテゴリ別ファクトリから生成される。実機で家具カテゴリを開いていた時の
`object+8156` は vtable `0x8F23D4` の `FtrList` だった。これは店舗シーンから借りた
オブジェクトではなく、カタログメニューのファクトリが確保する一覧プロバイダである。

`BsStrcCatalog` のグローバル `dword_94A6AC` は現在表示中の標準注文画面では0だった。
ただし、これは `OrderList` が使う特殊な3D構造体が無いことを示すだけで、通常の家具プレビューが
無いことは意味しない。標準の `FtrList` は後述の共通家具アクター経路を使用していた。

## 家具3Dプレビューの実経路

### 選択品から家具アクターまで

mode 0 の家具一覧では `sub_21A9FC` (`0x21A9FC`) が選択番号の変化を監視する。
選択が有効になると、現在品を `vc_GET_CURRENT_CATALOG_ITEM` (`0x691AC8`) が返す
グローバル `g_CatalogPreview` へ渡し、`CatalogPreview_UpdateActor` (`0x690E28`) がプレビューを生成する。

```text
FtrList の選択変更
  -> BsMenuCatalog::sub_21A9FC
  -> CatalogPreview_UpdateActor(&g_CatalogPreview, selectedItem)
       -> Item.binの家具familyから固定actor typeを選択
       -> sub_57ADFC(type, g_BsFtrMgr, request, ...)
       -> UiScreen_OpenById(..., parent = BsFtrMgr)
```

`g_CatalogPreview` は `+0` が現在のプレビューアクターポインタ、`+4` が選択中の `Item` である。
選択解除とメニュー終了時は `sub_6910B8` (`0x6910B8`) が `vc_UPDATE_MENU`
(`0x51F4C0`) でアクターを破棄してポインタを0へ戻す。

室内実機では次を確認した。

| 対象 | 実機値 | 意味 |
|---|---:|---|
| `g_CatalogPreview+0` | `0x3041E900` | 表示中の家具プレビューアクター |
| `g_CatalogPreview+4` | `0x00002EA3` | 選択中の家具Item |
| `g_BsFtrMgr` | `0x330BC474` | 現在の `BsFtrMgr` |
| manager vptr / type | `0x008F2BE8` / `0xEE` | `BsFtrMgr` と一致 |

従って、標準カタログも実際に3D家具を生成している。以前の
「`dword_94A6AC == 0` なので標準画面に3D系は不要」という解釈は、
`BsStrcCatalog` と共通家具プレビューを混同したものであり、ここで訂正する。

### 屋外を拒否していない根拠

`CatalogPreview_UpdateActor` の生成条件を簡略化すると次になる。リクエストの表示モードは常に2なので、
逆コンパイル上の2つのOR条件は常に真になる。

（疑似C を省略。原本は _local/legacy-src/…）

`sub_5B3A98` (`0x5B3A98`) は room flag `0x10000` を持つ部屋を除外するが、
村 room 0 のflagsは `0x26`、商店街 room 1 は `0x206` で、いずれもこのbitを持たず通過する。
`BsFtrMgr` 初期化 `0x68FC44` が使う部屋別容量表は村に `0x26`（38）枠、商店街に2枠を
割り当てている。しかしstock scene builderはroom flags bit `0x8` が立つ場合だけ、type `0xEE`を含む
室内共通groupを生成する。room 0のroom固有type列にも `0xEE` は無く、stockではmanagerが存在しない。

家具アクター種別は現在room descriptorではなく、`Item/Param/Item.bin` の30-byte record `+17` と
固定表 `g_FurnitureActorTypeByFamily` から選ぶ。全86 familyに対応するtype `0xBB`～`0xEB` のfactoryは
実行ファイル内にあるため、屋外CROへfactoryを移植する必要はない。

なお、`g_BsFtrMgr == 0` の時は `sub_57ADFC` が直ちに0を返し、`CatalogPreview_UpdateActor` も成功扱いで
メニュー処理へ戻る。つまり家具管理自体が無い部屋では、stock経路は「3Dプレビューなし」へ
安全に縮退する。さらに同関数はactor生成前に選択cacheを更新するため、失敗後に同一品を再試行しない。

### カメラと照明

`CameraCatalog` (`vtable 0x8E84F0`) は独立した店内オブジェクトではなく、
`BsCamera` のコンストラクタ `0x68EDDC` がオブジェクト内 `+768` に常設するサブカメラである。
屋外にも必須の共通 `BsCamera` に内包されるため、カタログカメラのクラス自体は室内限定ではない。

`BsLightMgr_CreateRoomLights` (`0x190578`) はroom固有lightの後、対応する全room経路で次の
専用ライトを生成してactiveにする。room 0もこの経路へ到達する。

| type | class | 実機オブジェクト |
|---:|---|---:|
| `0x105` | `BsLightDiffuseCatalog` | `0x3309BA0C` |
| `0x106` | `BsLightAmbientCatalog` | `0x3309BBDC` |
| `0x107` | `BsLightHemiSphereCatalog` | `0x3309BC50` |

これらは `BsMenuCatalog` 自身ではなく、共通 `BsLightMgr` が事前に用意する。
以前の「Catalog専用3灯は店内scene限定で、屋外では屋外lightだけを使う」という解釈は訂正する。
global rendererも3 layerを常時生成し、preview mode 2は第3 layerを選ぶ。従って現在の3D非表示を
カメラ、light、render passの欠落で説明することはできない。

## 2Dメニュー本体の唯一の直接的な部屋依存

`BsMenuCatalog` の関数範囲 `0x21A000`～`0x21D300` から
`Room_GetCurrentId` (`0x2F75CC`) への直接参照は `0x21CBAC` の1件だけである。
家具3Dは `sub_690E28` を経由して間接的に現在部屋を参照するため、この節の件数には含めない。

（疑似C を省略。原本は _local/legacy-src/…）

部屋判定関数は `sub_5B37D0` (`0x5B37D0`) で、厳密に 57～60 だけを許す。
実機は部屋 `0x3C` で、`object+15276` に7204バイトのオブジェクトが存在し、先頭近くに
`DICT` が確認できた。

## なぜ検索だけが屋外で壊れるか

処理の関係は次のとおり。

```text
mode 0 カタログ
  ├─ 通常カテゴリ → FtrList等 → 一覧・価格・注文      部屋非依存
  └─ 検索カテゴリ
       ├─ BsSkb (画面ID 0x23E) → 文字入力             ほぼ部屋非依存
       └─ searchDict (7204 bytes, DICT) → 検索実行     0x39..0x3C限定生成
```

1. `sub_21B738` (`0x21B738`) はカテゴリ番号5を検索として扱う。
   `searchDict` があれば `sub_14FE4C` を呼ぶが、null でも状態遷移自体は続ける。
2. `sub_21C24C` (`0x21C24C`) は一般的なソフトウェアキーボード
   `BsSkb`（画面ID `0x23E`）を開く。辞書がなければキーボードへ渡す検索ポインタは0になる。
3. `sub_21C05C` (`0x21C05C`) は辞書がある場合だけ `sub_14FE54` で非同期検索を開始し、
   `sub_14FD94` で結果を判定する。辞書がないと検索完了フラグを立てられず、正常な一覧復帰または
   「該当なし」への遷移が成立しない。
4. 終了処理 `0x21CF20` は辞書が存在する時だけCRO側デストラクタを呼び、メモリを解放する。

`0x14FE4C` などは `code.bin` 内では `LDR PC, [PC,#-4]` 形式の再配置スタブである。
室内実機で確認した呼出先は次のとおり。

| スタブ | 実機の再配置先 |
|---|---|
| `0x14FE4C` | `0xBDF694` |
| `0x14FE54` | `0xBDFA3C` |
| `0x14FE5C` | `0xBDF6AC` |
| `0x14FE64` | `0xBDF5C8` |
| `0x14FE6C` | `0xBE0000` |

この実行領域の近傍 `0xBDF86C` には `STR_Item_search_keyword` が存在する。
つまり検索辞書はメイン `.code` だけで完結せず、実行時ロードされたCRO側実装に依存する。
屋外遷移でそのCROがアンロードされる可能性があるため、室内で得た再配置先や辞書ポインタを
そのまま保持して屋外で呼ぶことはできない。

## 注文処理は店内に依存しない

通常 mode 0 の購入処理は `sub_1E4D48` (`0x1E4D48`) にある。

1. 一覧プロバイダの virtual `+44` から価格、virtual `+32` から品目IDを得る。
2. プレイヤーの所持金を確認し、ベルを減らす。
3. `sub_70F8D8` で80件の注文メール領域から空きを探す。
4. `Mail_SP_Kodanuki` の640バイトレコードを構築し、選択品を添付する。
5. `sub_1E4860` でセーブ側の注文メール領域へコピーする。

mode 0 の経路には部屋ID、店員NPC、店舗オブジェクトへの参照がない。
同関数内に `Room_GetCurrentId() == 161` はあるが、別用途の mode 5 専用分岐であり、
通常カタログには入らない。

## Vapecord実装との一致

Vapecord はカタログを任意の場所から mode 0 で開く一方、店舗外では次の2フックを入れている。

- ソフトウェアキーボードを開く呼出しを止め、「検索非対応」を通知する。
- 検索状態ではB入力を強制した扱いにして、その経路を抜ける。

USA版フック `0x21C408` / `0x21C0AC` は、JPN版静的解析ではそれぞれ
`UiScreen_OpenById(0x23E, ...)` の `0x21C348` とB入力判定の `0x21BFEC` に対応する。
これは「カタログ全体は屋外で使えるが、標準検索だけは店舗外で成立しない」という解析結果と一致する。

## 実現方法の比較

### A. stockの3Dプレビューを保ち、屋外では検索だけ無効化する（推奨）

信頼度: **MEDIUM**（生成・描画経路は静的確定、manager ready待ち版は実機未適用）

- プレイヤーを idle にする。
- ほかのメニューが開いていない状態を作る。
- `0x6D1BBC(0)` で Menu ID `0x7C` を開く。
- 部屋 `0x39`～`0x3C` 以外では検索カテゴリの決定を拒否するか、検索状態を即座に戻す。
- `g_BsFtrMgr` が無いroomではtype `0xEE`をsaved `BsMenuTab`下へ一時生成する。
- owned managerの `(byte[19]&3)==3` を待ってからCatalog selection cacheを1回だけ無効化する。
- 家具選択時に `g_CatalogPreview+0`、actor bank/modelを確認する。
- Catalog終了時はpreview actor、その後owned managerの順でstock破棄経路へ渡す。

通常カテゴリの閲覧、価格表示、注文、終了処理をstockのまま使える。変更範囲も最小である。

### A2. 屋外では3Dプレビューだけ止める（安全なフォールバック）

信頼度: **HIGH**

屋外で家具が暗い、画面外に出る、描画順が崩れる場合は、`sub_21A9FC` から
`sub_690E28` への呼出しだけを屋外で抑止する。既に生成済みなら `sub_6910B8` でstockの
破棄経路を通す。一覧・価格・注文は3Dアクターを参照しないため、家具画像なしでも機能を維持できる。
室内の `BsFtrMgr`、家具アクター、専用ライトのポインタを屋外へ持ち越す方法は使わない。

### B. stockの辞書を屋外でも生成する

信頼度: **MEDIUM-LOW**

技術的には、7204バイト確保とCROコンストラクタを部屋判定なしで実行すればよい。ただし、
CRO自体が屋外でロードされている保証がない。必要なのは単なる分岐NOPではなく、CROのロード寿命、
辞書初期化、非同期検索、デストラクタまで含めた管理である。屋外で未ロードの再配置先を呼べば即座に落ちうる。

### C. 検索だけ独自実装する

信頼度: **MEDIUM**

`BsSkb` または別キーボードで文字列を得て、取得済みカタログ品目名を独自にフィルタする。
実装量は多いが、店内CROから完全に切り離せるので、最終的には最も堅牢な完全版になりうる。

### D. 現在部屋IDを店舗に偽装する

**非推奨。** `g_CurrentRoomId` を `0x3C` などに変えると、カタログ以外のアクター、マップ、
イベント、退出、セーブ処理まで偽の部屋を見る。検索CROが未ロードなら問題も解決しない。

## 「屋外表示は難しい」とされた理由

- 画面自体は開くため、検索カテゴリを選んだ後の不具合がカタログ全体の部屋依存に見えやすい。
- 問題の辞書はメニューオブジェクト末尾のオプションポインタで、通常一覧とは離れた状態機械から使われる。
- `code.bin` の検索呼出しは再配置スタブだけで、実体がCRO側にある。
- `BsStrcCatalog` と、通常 `FtrList` が使う共通家具プレビューが別系統なので、
  前者のグローバルだけを見ると「3D表示は無い」または「店舗シーン全体が必要」と両方向に誤認しやすい。
- stockの呼出し元は店内端末経由だが、実際の共通入口 `0x6D1BBC` 自体には部屋制限がない。

## 下画面メニュー統合の静的再解析

メニュー全体の状態機械、タブ登退場、閉じるボタン、カタログ終了契約の詳細は
[`menu_system.md`](menu_system.md) に分離した。ここでは屋外カタログに直結する結論をまとめる。

### 表示内容とhost統合は別問題

カタログ本体の一覧・注文・3D preview経路には、村roomを一律拒否するhardな「屋内専用」分岐は
見つからない。一方、通常Xで始まる下画面hostは `BsMenuItem` 専用の契約を持ち、カタログは
それを実装していない。このため「カタログ内容を屋外で動かせる可能性」と
「持ち物画面を差し替えれば安全に開閉できること」は同義ではない。

通常持ち物は共有 `MENU_FLAGS` の `0x08` を入場開始時に、`0x10` を入場完了時に立て、
終了時に両方を消す。`BsMenuTab` はこのhandshakeを待ってタブと閉じるボタンを制御する。
`BsMenuCatalog` は `0x08/0x10` を一度も書かず、終了broadcast `0x20` を読むだけである。
また、catalog初期化が隠す `BsMenuMgr+500` は `BsHandCursor` であって、
`BsMenuMgr+480` の `BsMenuTab` ではない。従って屋外でタブが重なるのは偶発的な描画不具合ではなく、
stock catalogがfield用タブを退場させる責任を持たないためである。

catalog終了も、自身のlayout/provider/previewと `BsMenuBg` を片付けるだけで、field X側が開始した
player state `0x16`、controller state 5、タブ、地図、cursorを戻さない。以前の
「やめる」後ロックはcatalogのdestructor失敗ではなく、開始ownerと終了ownerの不一致である。

### 最新版が表示前に終了した正確な流れ

`PATCHES/cave_catalog_inventory_tabs_out.py` のconstructor成功同期版は次の構成だった。

1. `0x6D6338` で公式 `vc_CFUNCTION(0)` を呼び、catalog mode 0を要求。
2. `0x6D1154` の `UiScreen_OpenById` 成功return後にstockの全タブ退場へ遷移。
3. 退場完了後、stock「メニュー終了まで待機」`0x6D7194` へ接続。

手順3はgenericなscreen終了待ちではない。`MENU_FLAGS&0x08` が消えた瞬間に
`MENU_FLAGS|=0x20` として次へ進む、通常下メニュー専用の終了処理である。Catalogは最初から
`0x08` を立てないため、タブ退場直後に `0x20` が立ち、生成済みCatalogのupdateがそれを読んで
自身を破棄する。実機の「state `0x16`、タブ退場、catalog非表示、直後にstate `0x06`とタブ再入場」
はconstructor失敗ではなく、生成直後の即時終了で説明できる。

残った無反応の閉じるボタンはCatalogの「やめる」ではない。常設 `BsMenuTab` のindex 10であり、
表示mask/controlだけが論理ownerとずれて再有効化されたもの。再入場command 6の全writerは静的に
列挙済みだが、今回どのwriterが実際に走ったかは、動的解析停止中のため断定していない。

### 3Dプレビューの現在の判定

`BsMenuCatalog_UpdatePreview` (`0x21A9FC`) の最初のgateはcatalog mode 0と有効な選択indexである。
現行実験は公式入口を使うため、最新結果をmode未設定では説明できない。その先ではitem適格性、
ItemParam、`g_BsFtrMgr` の家具manager、managerの生成完了、actor bank、model resourceが必要になる。
村room 0／商店街room 1は拒否bit `0x10000` を持たず、静的には屋外を明示拒否しないが、
stock room 0は `BsFtrMgr` を生成しないため、外部から正規の生成3phaseを完了させる必要がある。

従って静的結論は次の範囲に限定する。

- 屋外を一律に拒否するhard gateは確認できない。
- preview actor factoryはItem.binのfamilyから固定tableで選ばれ、実行ファイル内に存在する。
- 精密再読ではactive `ScStage` とsaved `BsMenuTab` は共に `+14=1/+15=0` でparent gateを通る。
  以前の `ScStage +15=1` 拒否説は撤回する。
- saved `BsMenuTab` parent版でも `owned=0/status=3/g_BsFtrMgr=0` の即時失敗が再現した。
- room 0容量38ではphase 1がCPU約3.65 MB＋VRAM約0.99 MBをlate allocationする。
  第3版sourceはadapter-owned create中だけ容量を1へ制限する。
- manager生成に成功した場合は `g_BsFtrMgr`公開後も
  `(manager[19]&3)==3` まで待ってcacheを無効化する。
- 容量1版はmanager `+24=1`、`+19=1`、global公開まで成功し、38-bank失敗説を支持した。
- ただし未ready時にstock preview bodyへ戻るだけでtype `0xBC`の早期生成が起きる。
  第4版はstatus 1の間、preview update自体からreturnしてactor生成を完全に抑止する。
- manager phase 3もfield mapを走査するため、屋外配置Item `0x2090`をdefault type `0xBC`として
  生成して2回目のSIGSEGVになった。これは選択中Item `0x2EA3`とは別である。
- 第5版はadapter-owned phase 3に限りmap managerをnull扱いにし、配置actor生成だけを省く。
- manager完成後の3回目は選択Item `0x2EA3`自身で、ItemParam family 1が正規にtype `0xBC`
  (`AcFtrLoop`)を選んだ。この屋外objectはgeneric create用virtual slotを持たず、同じSIGSEGVになる。
- 同objectを完全な基底type `0xBB` (`AcFtr`)として再実行するとgeneric create result 2でattachできた。
  第6版はadapter active中のpreview openだけ `0xBC -> 0xBB`とし、Item requestは変更しない。
- 第6版で `0x2EA3`「0のランプ」と `0x2E78`「12つぶのぶどう」は実際に3D表示された。
  一方 `0x2C89`「1UPキノコ」はfamily 3/type `0xBD`で同じvptr+8 crashになった。
- 第7版はadapter active中のpreview openだけ、家具特殊type全域 `0xBC..0xEB`を基底`0xBB`へ
  置換する。Item requestは不変で、通常の室内Catalogとfield actor生成には作用しない。
- Catalogは生成失敗時もcache済みになるため、完全ready後に明示的な1回の再試行が必要である。

## 現在の作業境界

2026-08-25、saved `BsMenuTab` parent＋完全ready待ちの第2版でも3Dなしを実機確認し、
再Suspend後も `owned=0/status=3/g_BsFtrMgr=0/actor=0` だった。
容量1へ制限する第3版でphase 1成功後の早期actor生成がSIGSEGVになり、第4版でpreview待機を
修正した。続く2回目はphase 3のfield map走査だったため、第5版でadapter-owned map走査を省いた。
3回目の選択品actorは基底`AcFtr`としてcreate/attachを完了し、第6版で「0のランプ」と
「12つぶのぶどう」の3D表示を確認した。4回目は「1UPキノコ」のtype `0xBD`で同型crashだったため、
第7版へ拡張した。停止中actorは基底create result 2でItem `0x2C89`としてattach済み。

その後の実機試験で、1UPキノコを含む家具は一通り3D表示された。従って第7版は家具previewに
ついては有効である。ただし壁紙・絨毯などは表示されず、服カテゴリへ移動すると
`ModelInstance_SetRenderLayer` (`0x317BD0`) でSIGSEGVになった。これは無効vtable callではなく、
model finalize中のrender layer設定である。register/stack未採取のため原因は未確定。

現状の対応範囲は「屋外で家具カテゴリの3D previewを表示する実験版」に限定する。
壁紙・絨毯・服を含む全カテゴリ対応とは扱わない。特に服カテゴリはクラッシュするため、
第7版を再利用する場合も静的解析とguard修正が完了するまでは選択しない。
