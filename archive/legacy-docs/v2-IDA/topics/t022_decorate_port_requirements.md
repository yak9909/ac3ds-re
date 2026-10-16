# T022 HHD の家具リスト・壁紙/床紙リスト・ゴミ箱を ACNL の模様替え UI へ移植する — 必要なもの・不要なもの

2026-10-07 作成（IDA-opus-5.5）。設計・実装の前に、何を作り何を作らないかを確定するための文書。
根拠の番号は work/FINDINGS.md（IDA-opus-5.5-F0xx）と work/hhd/FINDINGS.md（IDA-opus-5.5-HHD-F0xx）。

## 最新の追加・訂正（2026-10-09 / IDA-gpt-6.1-sol-F013）

- 利用者の追加依頼で壁かけ家具（上段02）も移植済み。以下の「上段02は範囲外」は初期要件の履歴であり、現行版はdecor_catalog13以降の3タブ。天井/敷物の追加はしていない。壁リストの品・探索・UI根拠はIDA-gpt-6.1-sol-F012 / work/evidence/t022_wall_catalog/report.md。
- テントに見える家でも室内は通常部屋になり得るため、外観番号のテント判定を使わない。壁かけは実マップの配置条件、壁紙床は所有権と張替え対象の実モデル/材質で判定する。モデル型取得/材質検索のnative関数を読取りで使う。
- 張替えは通常setterを先に呼ぶ。外観由来の拒否時は、対象面の機能とオフライン制約を確認して下位setterへ。通信中の例外適用は未対応。外観記録・本体命令・UI資源は変更しない。decor_catalog14はPC/ビルド/リンク検査PASS、実機未確認。詳細work/evidence/t022_room_capabilities/report.md。

## 1. 依頼の範囲（利用者の言葉から）

「模様替え UI を開いている時」に、次の 3 つを HHD から移植する。挙動・押している間のテクスチャ変更なども忠実に。

1. HHD の家具リストを開くタブと、家具リストのメニュー
2. HHD の壁紙／床紙リストを開くタブと、壁紙／床紙リストのメニュー
3. ゴミ箱（模様替え UI で掴んだ家具を左下のゴミ箱へ運んで離すと消える）

補足（利用者）:
- 家具は HHD と ACNL の両方にあるものだけ。一致したものだけ HHD のプレビュー画像を持ってくる。
- リストから出した家具は「プレイヤーから近い部屋の空いている所」へ置く。置く処理は ACNL の「かざる」を流用し、空き場所の計算は HHD のものを自前で再現する。
- **模様替え機能そのもの（選択・掴む・動かす・回す・上に載った物を優先して選ぶ）はいじらない**（2026-10-07）。

## 2. 作らないもの（ゲームにすでにある／依頼の外）

| 物 | 理由 |
|---|---|
| 家具の選択・掴む・ドラッグ・回転・置き直し | ACNL の模様替え UI（ModuleIndoor の Chip。F050）がすでに持つ。利用者の指示で触らない |
| 「どの家具を消すか」の判断（一番近い家具を探す、上に載った物を先に消す等） | 選ぶのは利用者が模様替え UI で行う。上に載った物の優先も ACNL の UI が既に持つ（エディター Neutral 0xB3D1E4 が上の物 → それ以外の順で入力を配る、F050）。ゴミ箱は渡された 1 個を消すだけ |
| 試験用の FurnitureTest（gohan work/furniture-test）の「一番近い家具を消す」「上の物も消す」「左上から輪で探す」 | 経路を実機で確かめるための試験。本実装には持ち込まない |
| `Item_PlaceItem` 0x59E5B4 での配置・削除 | 落とし物の処理で、その場で家具が出ない／消えない。0x2001 はリンゴ（F103 / F104 で不採用） |
| 部屋のマップのデータだけを書き換える方法 | 画面の家具オブジェクトが追従しない（F103 試験 1） |
| 村（屋外）での動作 | 模様替え UI は ModuleIndoor にあり家の中だけ（F050） |

## 3. 作るもの

### 3.1 ゴミ箱

| 項目 | 中身 | 状態 |
|---|---|---|
| 見た目 | HHD `Layout/Main/Main.arc` の `min_Trash_00`（閉 / 開 / ふた、アニメ in/out/on/off/select/touch/touch_ok/ok/loop）を ACNL のレイアウト形式へ | 資源は特定済み（HHD-F013/F015）。変換は未 |
| 振る舞い | ゴミ箱の部品の状態 Idle / In / Wait / OnTarget（"on" + 音 onTarget）/ OffTarget（"off"）/ DroppedTarget（"ok" + 音 dropped）/ Out | 静的に確定（HHD-F015）。音を ACNL のどの音で鳴らすかは未定 |
| 重なりの判定 | ACNL の模様替え UI で**チップをドラッグ中**に、指（またはチップ）がゴミ箱に重なっているか | 場所は判明（F105）: `Chip_Drag_Calc` 0xB422C4（ModuleIndoor）が毎フレーム動き、指が離れたフレームに Drop を呼ぶ。読む値（指の位置）は未 |
| 離したとき | 重なっていれば、そのチップの家具を消す（まとめて掴んでいれば全部）。重なっていなければ ACNL の通常の Drop に任せる | 割り込む位置は判明（F105: 0xB42348〜0xB4239C の分岐の手前）。**未**: ModuleFtr の掴み状態（+4246・+20 等）の片付け方 |
| 家具を消す呼び出し | 家具のオブジェクトを `AcFtr_ChangeState` 0x56FD10(家具, 6)（前に vtable+144 が真か確かめる）。片付けがその家具のマスを部屋のデータから空にする | **実機で確認済み**（F104 試験 4: 即反映、8 フレームでマップ 0x7FFE）。ゲーム自身も部屋の家具を消すときこの手順（sub_4E4FD0）。模様替え UI には「捨てる」が無いので、この 1 本は必要 |
| チップの後始末 | 消した家具のチップを消す | 判明（F105）: 家具の記録は片付けが自動で外す（AcFtr_DestroyBegin → FtrRec_UnregisterAcFtr）。**チップは残る**（開いた時しか作り直さない）ので、自前でチップを状態 Out（Chip_Out_Calc 0xB4304C）にする |

### 3.2 家具リスト（タブとメニュー）

| 項目 | 中身 | 状態 |
|---|---|---|
| 開くタブ | 模様替え画面の上段のタブ = HHD **MainTop.arc の mit_RoomTop_00**。家具 = **L_Top_01（x −81、緑の葉っぱ AFurniture）**。部品 min_BtnTop_01（アニメ loop / ng / ok_out / select / select_ok / touch / touch_ok） | 資源と配置は確定（HHD-F018、スクショ一致）。変換は未 |
| 地 | `ctl_Base_01`（緑）。タブの段 y 92: 家 / ショップ / コレクション / 服 + 戻る（部品 ctl_BtnTop_01 / ctl_BtnBack_01）、種類の段 y 75（ctl_BtnKind_01 x 最大 10） | 部品の参照先まで確定（HHD-F018） |
| タブ・種類 | 表 0x67B464（HHD-F019）: 家（ベッド・テーブル・いす・たんす・オーディオ・しきり・あかり）/ ショップ（植物・食べ物・店・スポーツ・楽器・屋外・おもちゃ）/ コレクション（和風・ハート・絵・音楽・虫・化石・はにわ・ブロマイド）/ 服（8 種） | 確定（tools/hhd/catalog_kinds.py） |
| 品の並び | 種類ごとに Item.bin の種類のビット・ItemSort の順（HHD-F019）。HHD は持っている品だけ出すが、移植は HHD の進行が無いので全部出す（利用者 OK §5.6） | 確定（work/evidence/hhd_decorate/catalog_kinds.json） |
| 一覧 | 格子 ctl_Tum15_00（1 ページ 15 個 x 3 ページを回す、状態 Idle / In / Wait / Out / FastIn / FastOut / Drag / Slide / Swap）、名前の吹き出し wit_Slct（WinItem.arc）、NEW 印 | 静的で判明（IDA-gpt-6.1-sol-HHD-F001、MEDIUM）: 状態・ページ送りの定数・押下のアニメ・音・吹き出しの位置。work/evidence/hhd_decorate/tum15/report.md |
| 品物 | HHD と ACNL の両方にある物だけ（F101）。同じモデル名の ACNL 品番が複数ある物は名前でも突き合わせる | 曖昧な物の解消は未 |
| アイコン | `Layout/IconItem/%04d.arc`（%04d = HHD 品番 − 0x2000）。一致した物だけ持ってくる | 規則は確定（HHD-F012）。変換は未 |
| 出す | 空き場所の計算（HHD `Room_SearchFreeSpot` の順）を自前で書き、`Room_TryPutFurnitureAt` 0x6920CC で試し `BsFtrMgr_SpawnFromRecord` 0x68FA84 | 部品 2 本は実機確認済み（F103）。HHD の順の移植は未 |
| 模様替え UI との整合 | 出した家具のチップを自前で `Chip_Setup` 0xB43160 | 判明（F105） |
| ポケット | 無制限（ポケットから消さない） | 利用者の回答 §5 |

### 3.3 壁紙／床紙リスト（タブとメニュー）

| 項目 | 中身 | 状態 |
|---|---|---|
| 開くタブ | mit_RoomTop_00 の **L_Top_04（x −135、ピンクの家 ADoor）**（上段 04） | 確定（HHD-F018 / F019） |
| 地 | `ctl_Base_04`（ピンク、ページ「n/m」）。タブ 壁紙 BWall・床紙 BFloor（ドア・窓・カーテン・あかりは ACNL に品が 0 件なので出さない） | 確定。スクショ wallpaper_selected / flooring_selected と一致 |
| 品物 | 壁紙 144 / 144、床紙 114 / 114 が ACNL にもある（床はモデル名 floor_X ↔ carpet_X で照合） | 確定（catalog_kinds.py） |
| 替える処理 | 部屋の壁紙・床を替え、その場で見た目を反映する | 静的で判明（IDA-opus-5.5-F106、MEDIUM）: ゲーム自身の `HouseRoom_SetWallpaper` 0x2C5FA8 / `HouseRoom_SetFlooring` 0x2C6CCC(品*, 音) を呼ぶ。データを書くだけで、表示は本体の BsCharRoomViewMgr が毎フレーム読み直して差分を入れ替える。前の壁紙・床は残らない（無制限の方針どおり）。実機未確認 |

※ 上段 02（黄、壁に掛ける物）と 03（青、敷物）は依頼の範囲外として出さない（§5.6 の 3）。

## 4. 試験で確かめたことの扱い

| 試験 | 結果 | 本実装での使い道 |
|---|---|---|
| F103 試験 1（データだけ書く） | 画面が追従しない | 使わない |
| F103 試験 2（Item_PlaceItem 0xA） | 落とし物になる | 使わない |
| F103 試験 3（TryPut + Spawn） | 即反映・「かざる」と同じ | 家具リストの「出す」に使う |
| F104 試験 3（Item_PlaceItem 6） | 消えずリンゴになる | 使わない |
| F104 試験 4（AcFtr 状態 6） | 即反映で消える | ゴミ箱の「消す」に使う（消す対象は模様替え UI で掴んだ 1 個） |
| F104 試験 5（上の物も状態 6） | 一緒に消える | 使わない（上の物の優先は模様替え UI の仕事） |

## 5. 利用者の回答（2026-10-07）

1. リストから出す家具は無制限（ポケットやお金を減らさない）→ **はい**。「かざる」の後半（ポケットから消す sub_2BFE8C）は呼ばない。
2. 捨てた家具はどこにも残らない → **はい**。
3. ゴミ箱は家具だけ → **はい**。壁紙・床はチップとして動かせないので、ゴミ箱側で何もしなくてよい。
4. タブとゴミ箱の位置 → **はい**（HHD の位置そのまま、と解釈。既存ボタンと重なる場合は改めて相談）。
- 方針: **実機確認はどうしても必要な時だけ。ほとんどは静的解析で解明する。**

## 5.5 ゴミ箱の手順の案（静的、F105。未実機）

1. 毎フレーム（ゲームのスレッド）: 模様替え UI が開いている（`g_InteriorEditor` が非 0）なら、ゴミ箱の部品を描き、ドラッグ中のチップ（状態 calc = `Chip_Drag_Calc`）の指 +1084/+1088 がゴミ箱に重なるかで OnTarget / OffTarget を切り替える（HHD-F015 のアニメと音）。
2. 指が離れたフレーム（`Chip_Drag_Calc` の離す分岐 0xB42348 の手前で割り込む）に重なっていれば:
   a. 掴んでいる家具の一覧を控える（g_FtrMgr +4246 = 数、1 なら +20、2 以上なら +1996 から 20 B ずつ。記録 +4 → `FtrGrid`/g_RoomFtrObjects の家具）。
   b. 指の点を押し始めの点（+1068/+1072）に戻してから、ゲームの通常の離す処理（Drop）を通す → 家具は元の位置に戻り、ModuleFtr の掴み状態はゲーム自身が片付ける（**案。戻す経路の音 0x1000525 が鳴る。止めるかは要相談**）。
   c. 控えた家具を `AcFtr_ChangeState`(家具, 6) で消す（F104 で実機確認済み）。記録は自動で外れる。
   d. 対応するチップを状態 Out（`StateObj_ChangeByCalc`(チップ, Chip_Out_Calc, 0)）にする。
   e. ゴミ箱は DroppedTarget（"ok" + 音 dropped）。
- 割り込みには CRO のコードへのフックが要る（ModuleIndoor は場面ごとに読み込まれ番地が変わる。先頭は §F105 の取り込み口から求める）。フックを使わず毎フレームの見張りだけで済ませる方法は、ゲームの更新と gohan の相乗りの順序次第（未確定）。

## 5.6 利用者の回答（家具リスト、2026-10-07）

1. HHD は持っている品だけ出すが、移植では ACNL にもある品を全部出す → **OK**。
2. 家具リストの「服」のタブ → **ACNL でも家具として置けるので出す**（置けない見込みという当方の推測は誤り）。
3. 上段のタブは家具（緑、x −81）と壁紙／床紙（ピンクの家、x −135）の 2 つだけ、HHD の位置で → **はい**。

## 6. 次に調べる順

1. ACNL の模様替え UI（ModuleIndoor）のチップの Drag / Drop で、掴んでいるチップ・指の位置・離した瞬間を読める場所（ゴミ箱の判定に必須）。
2. 家具を消したときのチップの後始末（落ちないための必須条件）。
3. 模様替え UI を開いたまま家具を出したときにチップが出るか。
4. 壁紙・床を替えて反映させるゲームの処理。→ F106 で静的に判明（HouseRoom_SetWallpaper / SetFlooring）。
5. HHD の Tum15・タブの挙動、Kind.bin / ItemSort.bin、曖昧な 1,410 件。
6. HHD のレイアウト（Catalog.arc / Main.arc / IconItem）の ACNL 形式への変換（既存の tools/hhd/build_hhd_arc.py の方式を流用）。

## 7. 段 2（家具リスト・壁紙/床紙リスト）の実装設計（2026-10-07、opus-5.5。実機未確認）

### 7.1 流れ（HHD の動きを写す。根拠 IDA-gpt-6.1-sol-HHD-F001）
1. 模様替え UI が開いている間（DecorTrash と同じ EditorLive）、下画面に上段タブ 2 つ（家具 = min_BtnTop_01 を L_Top_01 の位置、壁紙/床紙 = min_BtnTop_04 を L_Top_04 の位置）を出す。押している間 touch、離して決定 touch_ok + select_ok。
2. タブを決めるとカタログの窓（家具 = ctl_Base_01、壁紙/床紙 = ctl_Base_04）が in で開く。開いている間はゲームへのタッチを止める（GuiMenu::BlockGameTouch）。
3. 窓の中: 上段タブ（家 / お店 / コレクション / 服、または 壁紙 / 床紙）・小分類（L_Kind）・戻る。格子 Tum15 は 3 枚の枠で横送り（ドラッグ・フリック・L/R、端で止まる、定数は F001）。マスに触れると select + touch、離すと決定。選んだマスの上に名前の吹き出し（wit_Slct、名前は ACNL の品名）。
4. 品を決定 → 家具: 空き場所を探して置く（7.3）。成功なら窓を閉じる（HHD の StateID_Ok_、0x36BB9C 系）。失敗なら置けない旨（HHD の StateID_EditError_。表示の中身は未）。
   壁紙/床紙: `HouseRoom_SetWallpaper` 0x2C5FA8 / `SetFlooring` 0x2C6CCC(品, 1)（F106）→ 窓を閉じる。
5. 戻る / B で窓を閉じる（out）。

### 7.2 資源
- レイアウト: tools/hhd/make_catalog_arc.py → hhd_catalog.arc（Codex 依頼 t022_catalog_arc で作成中）。gohan の SD 置き場は hhd_decorate.arc と同じ（common/）。
- アイコン: 3,723 個（15 MB）は arc に入れない。tools/hhd/make_icon_bank.py の束を SD に置き、見える 3 枠 × 15 = 45 個だけを読む（HHD の Catalog_LoadVisibleIcons と同じ考え）。
  置き場所は窓を開くときに nw::lyt の読み込みヒープ [[0x96FC40]+4] から 45 × 4,096 B を借り、閉じたら返す（GuiRenderer::GpuIconCache は 16 KB しかない）。
  絵の差し替えは HiddenIcons.cpp と同じ書き方（TexMap +4 = PA、+8 / +12 = 64|64<<16、+16 の書式 = 11 ETC1A4 → 0x4B9830 → 材質 +0x4D bit2 を落とす）。アイコンの向き（swizzle 8）はペインの UV で直す。
- 品の表: tools/hhd/export_catalog_table.py → Includes/Cheats/DecorCatalogTable.h（服・曲の品番の対は Codex 依頼 t022_pair_ids で決めてから書き出す）。

### 7.3 家具を置く（IDA-gpt-6.1-sol-F001 + 依頼 t022_spawn2 の結果で確定させる）
- 空き場所: HHD の Room_SearchFreeSpot の順（HHD-F016）を ACNL のマスへ写し、各マスで `Room_TryPutFurnitureAt` 0x6920CC（判定のみ）。
- 置く: 戻り 0 のマスで `BsFtrMgr_SpawnFromRecord` 0x68FA84 を 1 回。家具アクター 48・記録 112・チップ 112 の空きを先に確かめる。
- チップ: 記録が生きたら空きチップへ `Chip_Setup` 0xB43160 → 層 1 なら親と結ぶ → N_All をエディターのペインへ（0xB42084）。描画リストへは次のフレームに自動で載る見込み（spawn2 途中経過）。
- 実行はゲームのスレッド（0x1B721C の相乗り、エディターが Neutral で掴み・まとめ選択が無いとき）。

### 7.4 音（HHD の音は ACNL に無いので代用。実機で聞いて利用者に決めてもらう。番号は reference/old_project/SOUND/index/sounds.csv）
| HHD | 代用（案） |
|---|---|
| マスに触れる SE_SYS_BTN_STATIC_ACTIVE_S | SE_SYS_BTN_ACTIVE_S 0x1000399 |
| マスの決定 SE_SYS_UI_DECIDE_LONG | SE_SYS_DECIDE_L 0x100038F（置けたら SE_SYS_FUR_PUT 0x1000525 も候補） |
| 窓の上段タブ・小分類の触れる / 決定 | SE_SYS_CTLG_TOP_BTN_ACTIVE 0x100046B / SE_SYS_CTLG_TOP_BTN_SELECTED 0x100046C |
| 模様替え画面のタブの決定 SE_SYS_ICON_CATALOG | SE_SYS_WIN_SELECT_OPEN 0x10003C2 |
| 前 / 次のページ SE_SYS_PAGE_DEC / INC | SE_SYS_PAGE_DEC 0x100039D / SE_SYS_PAGE_INC 0x100039C（ACNL にある同名） |
| 横スライド・小分類の境界 SE_SYS_SLIDE / _NEXT_CATEGORY | SE_SYS_CTLG_PAGE_CHANGE 0x100046A |
| 戻る | SE_SYS_DECIDE_QUIT 0x1000391 |
| 壁紙・床紙を替えた | ゲーム自身が鳴らす SE_ACT_WALLPAPER_CHANGE / SE_ACT_CARPET_CHANGE（F106） |

### 7.5 決めたこと・確認事項
- オルゴール: HHD は 1 品、ACNL は曲ごとに 91 品 → リストにはいちばん小さい品番 0x21E4（けけさんびか）を出す（F107）。
- メニューの項目: ゴミ箱と同じ「模様替えにゴミ箱」とは別にするか 1 つにまとめるかは実装時に決めて報告する。

### 7.6 実装の状況（2026-10-07 18:40、opus-5.5。gohan work/decor-catalog e6d0334、artifacts/plugins/decor_catalog1、未実機）
- DecorCatalog（メニュー「模様替えに家具リスト」）: 上段タブ（上段タブ用の arc を常に置く）→ 窓（タブを押したときに窓用の arc を読み、閉じたら返す）、格子 DecorSlider（HHD の PageSlider の写し）、アイコン DecorIcons（SD の束から 45 枠）、名前の吹き出し（文字幅はゲームの持ち物欄と同じ測り方）、置く DecorPlace（HHD の順）+ 0x6920CC / 0x68FA84、出した家具のチップ（F002 の手順）、壁紙・床紙は F106 の関数。
- 品の表 DecorCatalogTable.h（3,723 品、対は F003 で 6 / 7 / 47 側）。レイアウトの表 DecorCatalogLayout.h、CRO の表 DecorCatalogCro.h（いずれも生成）。
- 検査: DecorPlace / DecorSlider をパソコンで HHD の逆コンパイルの写しと突き合わせ（壊した写しで効き目も確認）、呼ぶ本体の関数の入口、リンク済みのリテラルの番地。
- 実機で決めること: 音（§7.4）、家具の向き 0 が手前を向くか、タブを押したとき下の模様替え UI が反応しないか、コマンドの器の大きさ（未実測）、チップが掴めるか。
