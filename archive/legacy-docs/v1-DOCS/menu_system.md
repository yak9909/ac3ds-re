# 下画面メニュー、タブ、カタログの状態機械

対象は JPN 版無印（Title ID `0004000000086200`）。本書は
`code.bin.i64`（idalib セッション `acnl_code`）の静的解析を主根拠とする。
実機で起きた現象は制御フローの照合にだけ用い、本書作成中は Remote GDB の停止中プロセス、
breakpoint、実行時パッチには触れていない。

## 結論

`BsMenuCatalog` は、持ち物などの「通常下画面メニュー」と同じ画面生成managerには登録されるが、
`BsMenuTab` が要求する下メニュー用ハンドシェイクを実装していない、独立性の高い画面である。

- カタログ初期化が隠すのは `BsMenuMgr+500` の `BsHandCursor`。タブ本体
  `BsMenuMgr+480` の `BsMenuTab` ではない。
- 通常の持ち物画面は `MENU_FLAGS` の `0x08` を立て、入場完了時に `0x10` を立てる。
  `BsMenuTab` はこの2段階を待って「閉じる」タブを出し、次状態へ進む。
- `BsMenuCatalog` は `0x08` / `0x10` を一度も立てない。読むのは終了要求 `0x20` だけである。
- カタログの終了処理はカタログ自身、3Dプレビュー、`BsMenuBg` の背景を片付けるが、
  field側が開始した player state `0x16`、controller state 5、タブ、カーソル、地図を戻さない。
- したがって、通常Xの持ち物経路で画面IDだけをカタログへ差し替えると、開始側の所有者と
  終了側の所有者が一致しない。UI重複と終了後ロックはこの不一致から生じる。
- 最新実験でカタログが表示されなかった直接原因も確定した。タブ退場後に接続した
  「メニュー終了まで待機」は `0x08` が0なので即終了し、`0x20` を立てる。
  カタログはそのbitを見て生成直後に自壊する。

## `BsMenuMgr` の常設構成

`BsMenuMgr_Init` (`0x6D3144`) は次の4画面を常設する。

| manager field | screen ID | class | 役割 |
|---:|---:|---|---|
| `+472` | `0x217` | `BsMenuMain` | 下画面メニュー全体の制御、別画面への復帰 |
| `+476` | `0x260` | `BsMenuBg` | `mvmnt_undscrn` の背景・下地アニメーション |
| `+480` | `0x218` | `BsMenuTab` | 上部タブ群、閉じるボタン、入退場アニメーション |
| `+500` | `0x216` | `BsHandCursor` | タッチ用の手カーソル |

`+484` の `BsMenuMap`（screen `0x219`）などは必要時に生成される。
factory registry は `0x94FDB8 + screenId * 8` で、各entryの第2wordが確保・constructor wrapper。
対応するwrapperとRTTI/vtableを照合した結果であり、`+500` をタブとみなした旧解釈は誤りだった。

通常持ち物とカタログは常設子ではなく、共通の画面registryから別オブジェクトとして生成される。

| menu ID | screen ID | class | constructor |
|---:|---:|---|---:|
| `0x00` | `0x220` | `BsMenuItem` | `BsMenuItem_Ctor` |
| `0x7C` | `0x258` | `BsMenuCatalog` | `BsMenuCatalog_Ctor` (`0x21D0A0`) |

この構造は「同じmanagerから開ける」ことだけを保証する。画面間でタブ、player、field controllerの
開始・終了契約が同じであることは保証しない。

## 共通画面生成manager

画面要求と画面実体の生成は別フレームで行われる。

```text
Menu_RequestOpen(menuId, arg)                  0x6D1330
  g_MenuOpenState: 1 -> 2
  g_MenuOpenId/Arg を保存
        |
        v
Menu_PollOpen(manager)                         0x6D10A8
  MENU_FLAGS bit 0x04 を待つ
  menuId -> word_9863E4[menuId] -> screenId
  g_MenuOpenState: 2 -> 3
  UiScreen_OpenById(screenId, manager, menuId, 0)
        |
        +-- 失敗: state 3 -> 1
        `-- 成功: screenを登録

Menu_UnregisterScreen                          0x6D102C
  最後のscreenが消えた時だけ state 3 -> 1
```

`Menu_RequestOpen` の成功はキュー投入成功であり、constructor成功ではない。
`0x6D1154` の `UiScreen_OpenById` 戻りだけが画面生成成功の同期点になる。
一方、このmanagerは playerやfield controllerの所有状態を知らず、screenの登録・破棄だけを管理する。

## `MENU_FLAGS` の下画面契約

`vc_MENU_FLAGS` (`0x949D68`) は複数の画面が共有するbitfieldである。今回確定した範囲は次の通り。

| bit | 今回の意味 | 主な使用箇所 |
|---:|---|---|
| `0x01/0x02/0x04` | 地図・下画面managerの同期phase。初期readyは `0x04` | `0x6D32F0`, `0x6D701C`, `0x6D67F0` |
| `0x08` | 通常下メニューの入場開始／存在通知 | `BsMenuItem_OpenEnter` (`0x199F9C`) |
| `0x10` | 通常下メニューの入場完了 | `BsMenuItem_OpenUpdate` (`0x199F44`) |
| `0x20` | 下メニューへの終了broadcast | `0x6D4EE8`, `0x6D7194` |
| `0x800` | 一部modal画面の追加状態 | 通常持ち物の完了処理など |

通常の `BsMenuItem` は次の対称な手順を持つ。

```text
OpenEnter  0x199F9C:  (flags & ~0x18) | 0x08
OpenUpdate 0x199F44:  入場完了で 0x10 を立てる
Update     0x19FC58:  0x20 を見ると CloseUpdate へ
CloseEnter 0x19AB74:  0x20 を消して退場開始
CloseUpdate 0x19AAC0: 退場完了で 0x08/0x10 を消し、screenを破棄
```

これに対し `BsMenuCatalog` 範囲内の `MENU_FLAGS` xrefは
`BsMenuCatalog_Update` (`0x21CC10`) の2件だけで、`0x20` の読出しである。
`0x08` / `0x10` の書込みも、終了時のclearも存在しない。
従って「実画面が生成されれば必ず `0x08` が立つ」という旧前提は成立しない。

## `BsMenuTab`

### リソースとタブindex

`0x6D3B98` は `Layout/Menu/menu_tab.arc`、`menu_tab.bclyt`、
`menu_tab_in` / `menu_tab_out` 系アニメーションをロードする。
`0x6D51F4` が作る11個のcontrolは次の通り。

| index | layout button | 意味 |
|---:|---|---|
| 0 | `B_itm_00` | 持ち物 |
| 1 | `B_Dsin_00` | マイデザイン |
| 2 | `B_rfrnc_00` | reference系 |
| 3 | `B_frnd_00` | フレンド |
| 4 | `B_list_00` | リスト |
| 5 | `B_plus_00` | plus系 |
| 6 | `B_chat_00` | チャット |
| 7 | `B_manp_00` | `manp`系（用途名は未確定） |
| 8 | `B_post_00` | 画像投稿 |
| 9 | `B_call_00` | 呼出し |
| 10 | `B_back_00` | 戻る／閉じる |

index 10はカタログの「やめる」ではない。常設 `BsMenuTab` が所有する閉じるボタンである。

### 主要field

| offset | 内容 |
|---:|---|
| `+6427` | 選択中／現在tab index。`10`は閉じる、`-1`は未選択 |
| `+6576` | tab内部flags |
| `+6578` | 現在有効・表示中のtab mask |
| `+6580` | 入場または退場対象mask。`0x8000`はアニメーション進行中 |

### 入場と退場

- `BsMenuTab_BeginEnter` (`0x6D581C`) は `+6580` のbitに対して入場アニメを開始する。
- `BsMenuTab_UpdateEnter` (`0x6D5B4C`) は完了時に対象bitを `+6578` へORし、
  `+6580` を0へ戻す。
- `BsMenuTab_BeginExit` (`0x6D5DA8`) は同じ `+6580` を退場maskとして使う。
- `BsMenuTab_UpdateExit` (`0x6D6528`) は完了時にcontrolを無効化し、
  `+6578 &= ~mask`、`+6580 = 0` とする。
- `BsMenuTab_AllTabsOutEnter` (`0x6D6B88`) は現在の `+6578` 全bitを
  `+6580` へコピーしてstock退場を開始する。
- `BsMenuTab_AllTabsOutUpdate` (`0x6D6A98`) は退場完了後、論理状態を「タブ選択」へ戻す。
  この関数自身は再入場アニメーションを開始しない。
- `BsMenuTab_AllTopTabsInEnter` (`0x6D6388`) はindex 0～4、9、10を入場対象にする。
  index 10を含むため、別ownerがこの状態を命令すると「閉じる」だけが再出現し得る。

### command byte `0x949D24`

`BsMenuTab_ConsumeCommand` (`0x6D3F04`) は毎回byteを読み、直ちに番兵値11へ戻してから
状態を切り替える。今回重要なcommandは次の通り。

| command | 遷移 |
|---:|---|
| 6 | 上タブをすべてイン |
| 7 | 上タブをすべてアウト |
| 8 | 上タブをイン |
| 9 | 上タブをアウト |
| 10 | 下タブをイン |

command 6の書込み元は `0x19DE74`、`BsMenuMain_BackToItemUpdate` (`0x1A0C0C`)、
`0x25C81C`、`0x332900`、`0x332944`、`0x332988` の6関数。
command 7の書込み元は `0x19D1C8`、`0x19D3FC`、`0x19EBB0`、`0x19F45C`、
`0x25C9BC`、`0x30CF1C` の6関数である。`BsMenuCatalog` はcommand 6/7をどちらも書かない。

### 「閉じる」ボタンが単独で残る理由

`BsMenuTab_LowerMenuSwitchUpdate` (`0x6D6060`) は `MENU_FLAGS&0x08` を確認すると、
選択tabの入場アニメ完了後に `+6578 |= 0x0400` とし、index 10を有効化する。
またcommand 6もindex 10を入場対象に含める。

したがって、地図上に残った無反応な「閉じる」はカタログのボタンではなく、
`BsMenuTab` の表示mask/controlだけが論理状態より先に再有効化されたもの。
最新失敗でどのcommand 6 writerが実際に走ったかは動的採取を停止しているため断定しないが、
全書込み元は上記に限定できた。常設 `BsMenuMain` の持ち物復帰状態
`0x1A0C0C` は、screen終了を検知するとcommand 6と `Menu_RequestOpen(0,1)` を同時に発行するため、
静的には最も直接的な候補である。

### 27状態の一覧

状態記述子は `0x8508FC` から20バイト刻みで
`[UTF-8 name, enter, 0, update, 0]`。

| # | state名 | enter | update |
|---:|---|---:|---:|
| 0 | 待機 | `0x6D4448` | `0x6D4444` |
| 1 | タブＩＮ | `0x6D666C` | `0x6D4610` |
| 2 | タブＯＵＴ | `0x6D6BD4` | `0x6D4C88` |
| 3 | タブ選択 | `0x6D4D8C` | `0x6D474C` |
| 4 | メニューイン | `0x6D4CB4` | `0x6D4700` |
| 5 | メニュー切り替え | `0x6D62AC` | `0x6D6060` |
| 6 | メニューアウト | `0x6D4EE8` | `0x6D4E5C` |
| 7 | メニューアウト待ち | `0x6D6AC4` | `0x6D67F0` |
| 8 | 待機 | `0x6D77E0` | `0x6D7728` |
| 9 | チャット用タブ退場 | `0x6D6440` | `0x6D6214` |
| 10 | チャット用タブ入場 | `0x6D5B14` | `0x6D5AB8` |
| 11 | タブ出現待ち | `0x6D72C0` | `0x6D70F8` |
| 12 | メニューアウト待ち | `0x6D78F4` | `0x6D783C` |
| 13 | チャット終了待ち | `0x6D5648` | `0x6D5510` |
| 14 | 下メニュー切り替え | `0x6D7784` | `0x6D76E4` |
| 15 | もどる | `0x6D626C` | `0x6D5FB0` |
| 16 | Mydesign用タブ退場 | `0x6D77E4` | `0x6D7758` |
| 17 | Mydesign用タブ入場 | `0x6D7228` | `0x6D70C0` |
| 18 | 地図同期タブ入場 | `0x6D701C` | `0x6D6F60` |
| 19 | 上タブをすべてイン | `0x6D6388` | `0x6D61E8` |
| 20 | 上タブをすべてアウト | `0x6D6B88` | `0x6D6A98` |
| 21 | 上タブをイン | `0x6D4FF8` | `0x6D4EBC` |
| 22 | 上タブをアウト | `0x6D5658` | `0x6D55EC` |
| 23 | 下タブをイン | `0x6D5804` | `0x6D5AE8` |
| 24 | メニュー終了まで待機 | `0x6D73A8` | `0x6D7194` |
| 25 | 画像投稿 | `0x6D6B18` | `0x6D68A0` |
| 26 | ランダムマッチ帰還 | `0x6D6F90` | `0x6D6C4C` |

## `BsMenuCatalog` の実際の開始・終了契約

### 初期化

| 項目 | 値 |
|---|---:|
| constructor | `0x21D0A0` |
| size | `0x3BB0` |
| init | `0x21C76C` |
| update | `0x21CC10` |
| end | `0x21CF20` |
| vtable | `0x8E8028` |

constructorは `object+15265` のmodeを一旦6にする。初期化phase 2で
`byte_9497F0` を同fieldへコピーするため、公式入口 `vc_CFUNCTION(0)` を使えばmode 0になる。
現行のX置換実験も公式入口を呼んでいるので、最新実験についてmodeの未設定は原因ではない。

初期化はcatalog layoutと一覧providerを作り、最後に
`BsHandCursor_Hide(*(off_949D4C+500))` を呼ぶ。`+480` の `BsMenuTab` には触れない。
また、カテゴリ／一覧の初期化は `BsMenuBg_RequestKind(manager+476, 1, 0)` で背景kind 1を要求する。

### 内部状態

カタログ自身は15状態を持つ。主なまとまりは、待機、カテゴリ選択の入場／退場／待機、
一覧初期化・入場・退場、ボタン入場・退場、検索入力・検索中・該当なし、購入確認・購入処理。
これはカタログ内部の2D画面状態であり、`BsMenuTab` の27状態とは別の状態機械である。

### 閉じる処理

- mode 0のカテゴリ側終了 `0x21C1B0` は `BsMenuBg_RequestKind(bg,0,6)` の後、
  カタログscreenを破棄する。
- 非0 modeの一覧終了 `0x21BA4C` も背景kind 0／animation 6を要求してscreenを破棄する。
- `BsMenuCatalog_Update` は `MENU_FLAGS&0x20` があれば自身を破棄する。
- `BsMenuCatalog_End` はlayout、provider、検索辞書、3Dプレビューを解放し、
  `byte_949D23=1`、`byte_9497F1=0` などのcatalog globalを更新する。

終了処理には次が存在しない。

- `BsMenuTab` のcommand 6/7発行
- `BsHandCursor_Show`
- playerをstate `0x06`へ戻す `sub_650F3C`
- field controller state 5の解除
- 地図画面への復帰
- `MENU_FLAGS` の `0x08/0x10` clear

`byte_949D23` の直接consumerは `0x314BD8` の別owner側状態であり、`BsMenuTab` や
field X controllerはこの完了byteを見ない。店内端末から開くstock文脈では呼出し元が後片付けし、
通常Xから差し替えた文脈ではそのownerが存在しない。

## field X経路との所有者不一致

通常Xは `sub_165B40 -> sub_5C1F08 -> sub_65945C` でplayer stateを `0x16`へ変更し、
成功後にfield controllerをstate 5へ進める。その後 `BsMenuTab` の
「メニュー切り替え」から通常持ち物screenを要求する。

通常持ち物を閉じる経路には `sub_672CAC -> sub_650F3C` があり、playerをstate `0x06`へ戻す。
カタログにはこの逆操作がない。そのため画面IDだけを置換すると次の非対称になる。

```text
開始: field X owner
  player 0x06 -> 0x16
  controller 0 -> 5
  BsMenuTab: 通常下メニュー待ち

終了: BsMenuCatalog owner
  catalog layout/provider/previewを破棄
  BsMenuBgをkind 0へ
  byte_949D23 = 1
  （field X ownerには通知しない）
```

「やめる」後にplayer `0x16`、地図なし、下画面操作不能となるのは、catalogの終了失敗ではなく、
catalogが自分の担当範囲だけを正常終了し、field X側の所有状態が取り残されるためである。

## 最新のconstructor戻り版が即時終了した理由

最新の `PATCHES/cave_catalog_inventory_tabs_out.py` は次の順だった。

1. `0x6D6338` で公式 `vc_CFUNCTION(0)` を呼び、catalog mode 0を要求する。
2. `0x6D1154` の `UiScreen_OpenById` 成功returnで
   `BsMenuTab_AllTabsOutEnter/Update` へ遷移する。
3. 退場完了時の `0x6D6AB8` を「メニュー終了まで待機」update `0x6D7194` へ接続する。

静的に追うと、手順3が即時終了条件だった。

```text
Catalog生成成功
  -> 全タブ退場
  -> BsMenuTab_WaitMenuEndUpdate
       MENU_FLAGS & 0x08 == 0   // Catalogは一度も立てない
       -> MENU_FLAGS |= 0x20
       -> 背景をindex 10へ
       -> 地図同期状態へ
  -> BsMenuCatalog_Update
       MENU_FLAGS & 0x20 != 0
       -> catalogを破棄
```

したがって実機で見えた「state `0x16`へ移る、タブは退場する、カタログは出ず、すぐstate `0x06`と
タブが戻る」は、要求未消費やconstructor失敗ではない。catalogは生成されたが、退場完了直後に
下メニュー用待機状態が終了broadcastを出し、表示前に閉じた。

## 3Dプレビューとの関係

`BsMenuCatalog_UpdatePreview` (`0x21A9FC`) が `sub_690E28` を呼ぶhard gateは、
catalog mode `object+15265 == 0` と有効な選択indexである。現行実験は公式mode 0入口なので、
この最初のgateは満たす。

`CatalogPreview_UpdateActor` (`0x690E28`) はさらにitem種別、`ItemParam_GetRecord`、
`!sub_5B3A98(currentRoom)`、`g_BsFtrMgr` とそのactor bankを必要とする。
村room 0と商店街room 1は `sub_5B3A98` の拒否bit `0x10000`を持たず、静的には屋外を拒否しない。
一方、stock room 0は `BsFtrMgr` を生成しない。actor typeはroom factoryではなく、
Item.binの家具familyと固定tableから選ばれる。親managerが無い、または生成途中なら `UiScreen_OpenById` は0を返し、
カタログは3Dなしで安全に続行する。

精密再読では初版parentのactive `ScStage` と第2版のsaved `BsMenuTab` は共に
`+14=1/+15=0` で、`UiScreen_OpenChild` のlate-child gateを通る。第2版でも
`owned=0/status=3/g_BsFtrMgr=0` となったため、失敗はcreate phase内である。
room 0容量38はphase 1だけでCPU約3.65 MB＋VRAM約0.99 MBを要求する。第3版sourceは
adapter-owned create中だけ容量を1へ制限する。manager生成に成功した後は
`(manager[19]&3)==3` 後にcacheを1回だけ無効化する。
CameraCatalog、Catalog専用3灯、global render layer 2は屋外にも存在する。
詳細な読込・描画経路は [`furniture_rendering.md`](furniture_rendering.md)。

## 実験履歴と静的な判定

| 実験 | 実機結果 | 現在の静的判定 |
|---|---|---|
| `0x6D6338` のmenu要求だけcatalogへ置換 | catalog表示、タブ重複、3Dなし、終了後lock | field X開始後なのでowner不一致 |
| player state `0x16` callだけcatalogへ置換 | 要求 `2/0x7C` のまま何も開かない | controller/下画面stateが要求消費を駆動 |
| 「メニュー切り替え」enterを置換 | catalog表示、重複・終了lockは同じ | タブとfield ownerはさらに前で開始済み |
| 「メニューイン」から終了待機へ直結 | `0x08`の永久待機、何も表示しない | requestを消費するstateまで飛ばした |
| catalog要求直後に全タブ退場 | 退場後すぐ再入場、ghost閉じる | 画面生成前に通常updateを奪った |
| `0x08`を `0x6D6060` で待つ | catalog表示、タブ退場しない | catalog生成後は同update自体が止まり、catalogはbitを立てない |
| constructor成功後に退場し終了待機 | 退場、catalog非表示、すぐ復帰、ghost閉じる | `0x08==0`で即 `0x20`、catalogを生成直後に破棄 |

この表により、同じ失敗構成を再試行する必要はない。

## 次の設計に必要な条件

ここではパッチ案を実行しない。静的解析から確定した設計制約だけを残す。

1. カタログを通常下メニューとみなし、`0x08`だけを待つ構成は使えない。
2. stock「メニュー終了まで待機」を流用するなら、`0x08/0x10` の生成・clearを含む
   完全なadapterを用意しなければならない。bitを単独で強制すると永久待機または即時終了になる。
3. タブ非表示はカタログ初期化に期待せず、`BsMenuTab` のmaskと状態機械を別に所有する。
4. 開始側をfield Xにするなら、終了時に同じownerへ完了を返し、player state、controller、
   タブ、地図を対称に閉じる必要がある。
5. 逆に独立画面として開くなら、field Xのstate `0x16`／controller 5を開始させず、
   `Menu_PollOpen` を駆動する別の正規ownerが要る。
6. 3D可否はメニュー統合と分離して検証する。まず画面のowner契約を成立させ、その後に
   preview actor生成の各gateを一つずつ確認する。

更新版patchをactive stateのまま適用・読戻し確認し、Remote GDB processは再開済み。
3Dの目視後にユーザーが手動Suspendしてからmanager/actor/resource状態を採取する。
