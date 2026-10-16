# ゲームのリスト UI を借りる汎用部品（GameList）

記録: IDA-opus-5.5-F036（2026-09-25）。静的解析は `ida/db/acnl_jpn_v15_annotated.i64`。
番地・欄は実機（公共事業カタログを表示して停止した状態）でも読んで照合した（§7）。

## 1. 目的と要件（利用者、2026-09-25）

- 公共事業エディターで、公共事業を**リストから選べる**ようにする（今は十字キーで順送りだけ）。
- ゲームの公共事業リストの UI を**下画面だけ**借りる。上画面は変えない（村のカメラ・配置を続けられる）。
- 「やめる」「けってい」ボタンは出さない。
- **公共事業専用に作らない**。「文字列の一覧から 1 つ選ぶ」汎用部品にする。
- エディターの ON/OFF で下画面 UI の**登場／退場アニメーション**。連続の ON/OFF にも耐える。

## 2. ゲームの作り

公共事業のリストは `BsMenuCatalog`（メニュー id 124、mode 1）が持つ。部品は 2 つに分かれる。

| 部品 | 持ち主 | 中身 |
|---|---|---|
| 枠 `ctlg_list`（`catalogue.arc`） | `BsMenuCatalog +996`（Layout 332 B） | 板・スクロールバーの位置 `N_scrl_pos_00`。アニメ `ctlg_list_in/_out/_kind`（+1740/+1780/+1820） |
| 中身 `ctlg_cntnt_00`（同じ arc） | 一覧オブジェクト（`BsMenuCatalog +8156`） | 8 行・選択枠・スクロール。アニメ in/out（+376/+416）・fade_in/out（+496/+456） |
| ボタン `common/btn_pos.arc` | `BsMenuCatalog`（`ComButton2Lyt`） | やめる／けってい。**借りない＝作らなければ出ない** |
| 上画面 `ctlg_T` | `BsMenuCatalog +1328` | 値段など。**借りない** |

### 2.1 一覧のクラス（RTTI）

`CatalogBase`（vtbl `0x8E5C90`, ctor `sub_1C5AC8`）→ `SelectBase`（`0x8E5704`, ctor `sub_1B07D8`）→
**`InstSelect<8>`（`0x8E54B4`, ctor `sub_7C6EB0`, 大きさ 4,812 B）** → 派生 10 種
（Letter `0x8E5524` / Search `0x8E5694` / Ticket / Clothes / Excavate / Ftr / Music `0x8F39B8` / Order / **PWork `0x8F3AA8`** / lyt::TourList）。
**`InstSelect<8>` がゲーム共通の 8 行リスト**。純粋仮想は vt[13]（一覧を作る）と vt[25]（i 行目の文字）の 2 つだけ。

| vt | 基底の実装 | 役割 |
|---|---|---|
| [0]/[1] | `0x1ACFA4` / `0x1ACF94` | デストラクタ / delete 付き |
| [3] | `0x1B0288` | 後始末（Layout・スクロール・文字箱） |
| [4] | `0x1B0314` | 毎フレームの更新（入力・スクロール・状態機械） |
| [5] | `0x1C58D0` | 描画登録: `vc_ACSYSTEM_DATA2(+44)` → `LayoutMgr_AddLayout(mgr, +44, 1)` |
| [12] | `0x1AF9A0` | 組み立て段 2 の中身（行ボタン `B_list_%02d` を ButtonActionControl へ、選択枠 `P_slct_00`） |
| [13] | 純粋仮想 | 一覧を作る。件数を +2500 に置き 1 を返す |
| [15] | `0x1AFEC8` | 行の文字を入れ直す（スクロール時）。文字は vt[25] |
| [16] | `0x1AF858` | 選択の見た目を (新, 旧) で付け替える。**自分から選択を動かすのに使える** |
| [20]/[22] | `0x1C59C8` / `0x1C5A58` | 入場／退場アニメの毎フレーム（状態の calc） |
| [24] | `0x1B0698` | 待機（決定を拾い +2792 に選択を置く） |
| [25] | 純粋仮想 | i 行目の「語」オブジェクト。`vt[3]` が UTF-16 文字列を返すもの |

主な欄: +36 Layout 名 `"ctlg_cntnt_00"` / +44 Layout / +280 arc の保持体 / +376 in / +416 out / +548 スクロール /
+2368 先頭の行番号 / +2496 行数 8 / +2500 件数 / +2504 文字箱の容量 / +2512 アニメ中 / +2513 入力止め /
+2524 組み立ての段 / +2556 行ボタン配列（224 B × 8）/ +2560 ButtonActionControl / +2788 選択枠 Pane / +2792 選択（-1 なし）。

### 2.2 行の文字

`vc_ACMESSAGEBOX_FUNC2(textbox, word)` は `word->vt[3]()` の返す UTF-16（メッセージ符号）を流すだけ。
**`script::WordPtr` = `{vtbl 0x0090491C, UTF-16 の番地, 容量}`（12 B、`vc_SETUPSTACK 0x308204` が作る形）**で足りる。
`WordPtr` の vt[3] = `0x75C418` は `+4` を返す。公共事業は `WordFix<38>`（100 B）に `STR_Fobj_name` を引いて入れている。

### 2.3 状態機械

`sub_8163C0(obj, calc, 0)` が obj+28/+32 の表（`{名前, enter, 0, calc, 0}` 20 B）から探し、obj+12/+16 に入れて **enter をその場で呼ぶ**。
毎フレーム vt[4] が calc を呼ぶ。`SelectBase` の表 `0x874308`（6 状態）:
何もしない / **入場処理**（enter `sub_1C55B4` = in を結合・+2512=1、calc → vt[20]）/ **退場処理**（enter `sub_1C5660`、calc → vt[22]。終われば「何もしない」）/
**待機処理**（enter vt[23]、calc vt[24]）/ リストフェードアウト / 何もしない。
入場は `sub_1C58F4(list)`、退場は `sub_1C5A34(list)`（どちらも状態を切り替えるだけ）。

### 2.4 アニメ（UiAnim 40 B, ctor `sub_1261EC`, dtor `sub_568CAC`）

欄: +0 vtbl `0x90062C` / +4 総フレーム / +8 現在 / +12 前回 / +16 速度 / +20 flags（1=一回、2=逆）/ +24 nw::lyt のアニメ / +28 結合中。

| 操作 | 関数 |
|---|---|
| 読み込み | `UiAnim_Load 0x568A04(anim, "name.bclan", holder)` |
| 結合 | `sub_4B8ECC(layout, anim)` |
| フレームを置く | `sub_568C00(anim)`、**値は VFP `s0`**（任意のフレームに置ける＝逆向きの途中から始められる） |
| 1 フレーム進める | `UiAnim_Step 0x568964` ＋ `vc_ACSYSTEM_DATA2 0x568030(layout)`（Layout の計算） |
| 終わったか | `UiAnim_IsFinished 0x74F58C`（flags 1: 現在 ≥ 総-1 / flags 3: 現在 ≤ 0） |
| 解除 | `sub_568840(layout, anim)` |

枠の kind は `sub_21B874` と同じく「結合 → フレーム → 計算 → 解除」で見た目だけ焼く。フレーム = 表 `0x848B18[+15264 の値]`。
**公共事業は +15264 = 6 → 2.0**（実機）。

### 2.5 入力

`SelectBase +2560` = **`ButtonActionControl`**（vtbl `0x8EE23C`, ctor `sub_2F7B04`）。
タッチは `byte_ACF6E0`（押下）/ `word_ACF6EA,EC`（座標）、十字は**メニュー管理 `BsMenuMgr`（`off_949D4C`）の +508（フォーカス）と手カーソル（+500 `BsHandCursor`）**を使う。
**+212 bit0 = 決定済み、+180 = 決定した行ボタン（その +200 に行番号）**。待機の calc がそれを拾う。
**+212 bit3 = 入力処理を丸ごと飛ばす**（vt[4] が毎フレーム +2513 から作る）。

### 2.6 組み立てと後始末

- arc の保持体 `ArcResAccReader`（584 B, ctor `sub_120D54`, dtor `sub_567310`）。読み込み `sub_567244(holder, "Layout/catalog/catalogue.arc")` は**終わるまで 0**（毎フレーム呼ぶ）。テクスチャは VRAM（`ArcResourceAccessorVRAM`）。
- Layout（332 B, ctor `sub_12653C`, dtor `sub_5BEB4C`）。作成 `sub_5685A4(layout, "x.bclyt", 0, cmdBytes)`（+236 に保持体を先に置く）。後始末 `sub_133A5C(layout)`。
- 一覧は `Heap_Alloc 0x2FD0CC(size, heap = *(dword_96FC3C + 4), 4)` → `sub_7C6EB0`（InstSelect<8>）→ vtbl を差す → +2504 = 容量。
  組み立て `sub_1C513C(list, holder, heap)` を 1 が返るまで毎フレーム。段 2 のあと `sub_298018(list+548, 枠の "N_scrl_pos_00")`。
- **レイアウトを作る前に書体とテクスチャを保持体へ登録する**（`BsMenuCatalog_Init` case 0、逆アセンブル 0x21C7DC〜0x21C828）:
  名前 = `sub_747528(*0x94C9C8, 0)`（SafeString、vt+8 を呼んでから +4）、書体 = `sub_52D6A8(*0x94C9C8, 0)` → `sub_4B3FD4(holder+0xC, 名前, 書体)`、続けて `sub_568CFC(holder)`（arc の .bclim を全部）。
  実機: 名前 `Garden_msg_size16.bcfnt`、書体 `0x3302ABE0`。**抜かすと行の TextBox の +0xE0 が 0 のままで `vc_ACMESSAGEBOX_FUNC1` 0x5E20A8 が SIGSEGV**（2026-09-25、gohan d18342a＋判定の書き換えで実機発生）。
- 後始末（`sub_21CF20` と同じ順）: 枠 `sub_133A5C` → 一覧 vt[3] → vt[1] → 保持体 dtor。

## 2.7 元の下画面 UI（地図・タブ）の退場と復帰（実機で確認）

村の下画面は `BsMenuMapVillage`（地図とアイコン、優先度 0x81 × 25 枚）と `BsMenuTab`（0x87）などで、自前のリスト（優先度 2）はその下に隠れる（実機）。
ゲーム自身の窓口で退場させる:

| 操作 | 書く所 | 読む側 | 結果 |
|---|---|---|---|
| 全タブ退場 | `0x949D24 = 7` | `BsMenuTab_ConsumeCommand 0x6D3F04`（毎フレーム・**状態に関係なく**） | `AllTabsOutEnter/Update` → タブ選択 |
| 地図退場 | `0x949D25 = 0` | `sub_6D1428` → `sub_6D0B54` → `sub_2B3A98` | 地図が Out → 画面を破棄（`vc_UPDATE_MENU`）。BsMenuMgr+484 = 0 |
| 地図とタブを戻す | `0x949D24 = 2` | 同上 | 状態 18「地図同期タブ入場」（`0x949D25 = 1` で地図 0x219 を開く）→ 状態 7（全タブ入場）→ タブ選択 |

- `BsMenuTab` = `*(BsMenuMgr 0x949D4C + 480)`。「タブ選択」= calc `0x6D474C`。命令は**タブ選択で落ち着いているとき（+6580 = 0、0x949D24 = 11、0x949D25 = 2）だけ**書く。
- 実機（2026-09-25）: 書く前 +6578 = 0x81DF・+484 = 0x32E142F0・フラグ 0x2 → 7 と 0 を書いて 2 秒: +6578 = 0・+484 = 0・MAPBOOL 0・フラグ 0x4、下画面にリストが見えた（`work/evidence/screens/gamelist_20260925/after_cmd7_map0.png`）→ 2 を書いて 3 秒: +6578 = 0x81DF・地図が同じ番地に戻る・フラグ 0x2、見た目も元どおり（`after_cmd2.png`）。

## 3. メモリ（実機、カタログ表示中）

- nw::lyt のヒープ = `dword_96FC3C`（`ssys::ma::Allocator`）の +4 = `sead::ExpHeap`、大きさ `0x3B0000`、**空き 1,456,124 B**。
- Layout のコマンドリスト = `graphic::MemoryMgr`（`off_96F304`）の FCRAM ヒープ（ExpHeap 大きさ `0x6AF000`）、**空き 865,080 B**。
  カタログは枠 `0x8000`＋中身 `0xB000`。
- 村（メニュー無し）の空きは未測定。**本物のメニューと同時に出すと VRAM・ヒープを二重に使う**ので、ゲームのメニューが開いたら自分は隠す。

## 4. 設計（汎用部品 GameList）

### 4.1 公開窓（案）

（疑似C を省略。原本は _local/legacy-src/…）

### 4.2 毎フレーム（ゲームのスレッド、`GridCursor::AddExtraFrameStep`＝描画フェーズの後）

段: Off → Loading（arc）→ Building（枠・一覧の組み立て）→ Entering → Shown → Leaving → Teardown → Off。

- 登場／退場は**枠と中身の両方の in/out を自分で結合して回す**（一覧の状態機械の入場／退場は使わない）。
  反転は「今のアニメを解除 → もう一方を結合 → フレーム = 総 - 1 - 今」で、見た目が飛ばない。
- 描画登録は毎フレーム `LayoutMgr_AddLayout(mgr, 枠, 1)` ＋ 一覧の vt[5]。
- 入力: 一覧の入力は**タッチだけ**使う（十字は建物エディターが使う）。十字がメニュー管理を読む経路はメニューの外では未検証なので、
  まず +2513 = 1（入力止め）で出し、決定は自前（タッチの当たり判定 or エディターからの `Select(i)` で vt[16]）にするか、実機で ButtonActionControl のタッチ経路を確かめてから任せる。
- ゲームのメニューが開いたら（`g_MenuOpenState 0x949D1E` ≠ 1、または `vc_MENU_FLAGS 0x949D68` の bit 0x08）即座に後始末し、閉じたら出し直す。**1 がアイドル**（村の屋外で 1・フラグ 0x2、実機）。

### 4.3 一覧のオブジェクト

- `Heap_Alloc(4812 + 0, heap, 4)` → `sub_7C6EB0` → vtbl = 自前の写し（`InstSelect<8>` の 26 語）。差し替えは vt[13]・vt[25]（と必要なら vt[0]/[1]）。
- 語は gohan の `.bss` に `WordPtr` を件数ぶん、UTF-16 も `.bss`。vt[25] はその番地を返す。

## 5. 未確認（実機で確かめること）

1. 村（メニュー無し）で `BsMenuMgr`（`off_949D4C`）と手カーソルが生きているか。十字の経路が安全か。
2. 描画フェーズ後（`0x1B721C`）に AddLayout して下画面に出るか（リストの UnlinkAll の時機）。
3. `sub_567244` の読み込みが村で何フレームかかるか・同期で止まらないか。
4. 村でのヒープ・FCRAM・VRAM の空き。

## 7. 実機の照合（2026-09-25、公共事業カタログ表示中）

- 下画面の Layout の並び（RenderBottom 入口）: mvmnt_undscrn(0) / **ctlg_list(2) = BsMenuCatalog 0x32E142F0 +996** / **ctlg_cntnt_00(2) = PWorkList 0x32E5F078 +44** / btn_pos(3) / menu_tab(0x87) / N_slct_win(0x90) / wipe 等(0xFF)。
- PWorkList: 件数 95、先頭 0、選択 0、+212=4、+2512..2515 = 0,0,0,1。in アニメ 総 11・現在 10・速度 1・flags 1。
- BsMenuCatalog +15264 = 6、+15265 = 1（mode）。`BsMenuMgr` 0x32FF803C、手カーソル 0x32C794F4（`BsHandCursor`）。
