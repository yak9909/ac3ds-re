<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl の記録

| ID | 題 | 確度 | 格付け | state | consolidated_into | 訂正 |
|---|---|---|---|---|---|---|
| ACNL-F0001 | 2026-09-12 GitHub保管の検証 |  | ? | active |  |  |
| ACNL-F0002 | 2026-09-12 普通チャットの入力所有者・日本語フォント・候補表示 | MEDIUM | ? | active |  |  |
| ACNL-F0003 | 2026-09-11 project_v2環境整備 |  | ? | active |  |  |
| ACNL-F0004 | F-407 実機成功: キーボード非起動で候補17/6/143件を取得（2026-09-11、最新・HIGH） | HIGH | ? | active |  |  |
| ACNL-F0005 | F-407 PC準備時点の履歴（配置待ちは解消済み） |  | ? | active |  |  |
| ACNL-F0006 | F-406 実機ヒープコード実行成功・全復元済み（2026-09-11、最新） | HIGH | ? | active |  |  |
| ACNL-F0007 | F-405 解決: キャッシュ処理中のクラッシュ、再起動で一時変更解除 | HIGH | ? | active |  |  |
| ACNL-F0008 | F-404 実機成功: 3gxで5 MiB確保・内蔵FS読取り（2026-09-11） |  | ? | active |  |  |
| ACNL-F0009 | F-403完了・F-404 3gx検証へ移行（2026-09-11） |  | ? | active |  |  |
| ACNL-F0010 | F-402 最終: 内蔵code全体Read・バイト同一性・cleanup確認（HIGH） | HIGH | ? | active |  |  |
| ACNL-F0011 | F-402 実機結果更新 | HIGH | ? | active |  |  |
| ACNL-F0012 | F-402進行中: ACNL自身の内蔵タイトルFS経路（MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0013 | F-401: 静的再配置315語・50比較一致・内蔵FS読取り条件 |  | ? | active |  |  |
| ACNL-F0014 | 最新 F-400: 再配置のPC試験成功・テーブル同梱を避ける方針 |  | ? | active |  |  |
| ACNL-F0015 | 最新 F-399: 画面・APTなしのエンジン実行をPCで確認 |  | ? | active |  |  |
| ACNL-F0016 | F-398: 関数型辞書の登録でPC候補列が実機保存値に一致（HIGH） | HIGH | ? | active |  |  |
| ACNL-F0017 | F-397: 予測モードにも複合候補の文節リストがある | HIGH | ? | active |  | 訂正あり |
| ACNL-F0018 | F-396: 旧SWKBDケーブとGUI v2の重複を回避し再適用 | HIGH | ? | active |  |  |
| ACNL-F0019 | F-395: UI単文節経路と直接連文節APIの区別 | MEDIUM | ? | active |  |  |
| ACNL-F0020 | F-394: callback境界のレジスタ保存でF-393を修正 | HIGH | ? | active |  |  |
| ACNL-F0021 | F-393: 通常フックのR0保持不足によるOFF時SIGSEGV | HIGH | ? | active |  |  |
| ACNL-F0022 | F-392: しずえスキップの通常フック化（2026-09-09） | MEDIUM | ? | active |  |  |
| ACNL-F0023 | F-391: case 0を含むしずえスキップ常設版（2026-09-09、使用禁止） |  | ? | active |  |  |
| ACNL-F0024 | F-383: 通常チャットのキーボード生成入口（2026-09-09） | MEDIUM | ? | active |  |  |
| ACNL-F0025 | F-382: とび森キーボード入口フックと結果返却の契約（2026-09-09） | MEDIUM | ? | active |  |  |
| ACNL-F0026 | F-372: ACNL既存APTの実行文脈候補と失敗分岐のPC検証（2026-09-08） | MEDIUM | ? | active |  |  |
| ACNL-F0027 | F-364: ACNLの内蔵キーボード起動候補経路・APT/GSP契約・ABIの検証（2026-09-08） | MEDIUM | ? | active |  |  |
| ACNL-F0028 | F-155a: submit-descriptor recorder は描画前のレジスタ連鎖で例外 — `HIGH`（例外位置＋機械的監査） | HIGH | ? | active |  |  |
| ACNL-F0029 | F-151: native TextBox draw の descriptor は `R2=0x330A605C` — `HIGH`（trace＋既存実測照合） | HIGH | ? | active |  |  |
| ACNL-F0030 | F-152: commit中の `TextBox_Draw` wrapper再入は不可 — `HIGH`（static＋実機例外） | HIGH | ? | active |  |  |
| ACNL-F0031 | F-153: direct-emitter patch generator 監査 — `MEDIUM`（独立の静的照合） | MEDIUM | ? | active |  |  |
| ACNL-F0032 | F-154: TextBox emitter直呼びも live DrawContext を二重更新する — `HIGH`（静的＋同一例外の再現） | HIGH | ? | active |  |  |
| ACNL-F0033 | F-144: 会話 TextBox も batch writer 経路 — `HIGH`（静的＋実機） | HIGH | ? | active |  |  |
| ACNL-F0034 | F-145: TextBox batch は専用list 32で構築され、メインlistへ再生される — `HIGH`（静的＋実機） | HIGH | ? | active |  |  |
| ACNL-F0035 | F-149: 会話本文フレームを構成する6 PictureとTextBoxを、相対配置のまま複製できた — `HIGH`（静的＋実機） | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0036 | F-148: 既存Pictureを非所有cloneして、任意座標の2D背景として追加できた — `HIGH`（静的＋実機） | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0037 | F-147: `nw::lyt::Picture` は TextBox と同じ UI command-list 経路を使う — `HIGH`（静的＋実機） | HIGH | ? | active |  |  |
| ACNL-F0038 | F-146: TextBox batch は固定0x60-byte seedとglyph/state blockから構成される — `MEDIUM`（静的＋停止中live照合） | MEDIUM | ? | active |  |  |
| ACNL-F0039 | F-01 ゲーム同定 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0040 | F-02 アイテムは 4 バイト構造 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0041 | F-03 地面オブジェクト定義テーブル — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0042 | F-04 型ID 113-122 は ASCII ではない — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0043 | F-05 アニメ名テーブル基準は `0x0085FFB0` — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0044 | F-06 アニメ再生速度は VFP の S1 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0045 | F-07 アイテムID 158 は「穴」 — `MEDIUM` | MEDIUM | ? | active |  |  |
| ACNL-F0046 | F-08 アクター状態テーブルは基準 `0x00843634` / エントリ `0x1C` — 基準は `HIGH` / 個々の割り当ては混在 | HIGH | ? | active |  |  |
| ACNL-F0047 | F-09 掘れる/掘れないの判定は 4 段構成 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0048 | F-10 掘る経路の後段にアクションID 上書きがある — `MEDIUM` | MEDIUM | ? | active |  |  |
| ACNL-F0049 | F-11 岩・構造物は cat10 経路の末端で脱落 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0050 | F-12 `Field_GetItemAtXY` はポインタを返す — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0051 | F-13 掘削適用は 32 スロットのレコード配列経由 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0052 | F-14 フィールドアクションの実行経路 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0053 | F-15 `Player_StartFieldAction` の呼び出し規約 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0054 | F-16 v1 の 3x3 ケーブがクラッシュした原因 — バグの存在は `HIGH` / 因果は `MEDIUM` | HIGH | ? | active |  |  |
| ACNL-F0055 | F-17 コードケーブとして使える範囲 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0056 | F-18 `Player_StartFieldAction` の呼び出し元は 16 箇所 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0057 | F-19 18B キューのスロットは解放されないと枯渇する — `HIGH` | HIGH | ? | active |  | 訂正あり |
| ACNL-F0058 | F-20 【訂正】滞留の原因は PUSH 後のスタック引数のずれ — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0059 | F-21 `FieldAction_Dispatch` の case 3 へは case 7 から来る — `MEDIUM` | MEDIUM | ? | active |  |  |
| ACNL-F0060 | F-22 隣マスが掘れない原因は対象アイテムの照合 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0061 | F-23 進行中アクションテーブル `0x9AE1A4` — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0062 | F-24 キューに積んでも実行段階は 1 マスしか処理しない — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0063 | F-25 レコードを積んでも反映されない — 反映側は 1 マスしか見ない — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0064 | F-26 【成功】直接書き込み方式で隣マスに穴が空いた — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0065 | F-27 地面更新のダーティビットマップ — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0066 | F-28 マスへのアイテム書き込み API — `MEDIUM` | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0067 | F-29 掘削の実処理は `FieldObj_ApplyRecordByAction` の jumptable — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0068 | F-30 掘る動作のエフェクトは 3 系統 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0069 | F-31 【完成】隣マス掘りが中心マスと完全同期 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0070 | F-32 CTRPF の空ページ `0x01E81000` は実行可能 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0071 | F-33 `Item_Copy` ではオブジェクトが破棄されない — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0072 | F-34 【完成】3x3 マス掘り — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0073 | F-35 【訂正】`FieldObj_RevertRecord` は「結果を確定させる」処理 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0074 | F-36 木にぶつかったときの経路 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0075 | F-37 `FieldObj_InitFallActor` の `kind` が演出を決める — `HIGH` | HIGH | ? | active |  | 訂正あり |
| ACNL-F0076 | F-38 「揺すると木を切る」パッチと通常経路 — `HIGH` | HIGH | ? | active |  | 訂正あり |
| ACNL-F0077 | F-39 【危険】レコード枯渇で範囲外書き込み → SIGSEGV — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0078 | F-40 赤いバラの正体 — `FieldObj_FellObject` の `a2` が空だと `a1` から ID を流用する — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0079 | F-41 `FieldObj_FinalizeRecord` (0x5A10AC) — 伐採の終端処理 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0080 | F-42 【完成】木にぶつかって切り倒す — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0081 | F-43 RTTI からクラス名を引ける — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0082 | F-44 `Item_PlaceItem` (0x59E5B4) — 資料と逆コンパイルが完全一致 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0083 | F-45 `NCCH/exefs/code.bin` は実機とは別ビルド — アドレスが対応しない — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0084 | F-46 実機イメージ `code_runtime.bin` を吸い出した — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0085 | F-47 `0x596890` の実態 — 踏みつけ処理 `FieldObj_TrampleAt` — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0086 | F-48 静的 IDB を idalib-mcp で常用する — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0087 | F-49 メッセージ表示の仕組みと「メニューアニメーションをカット」の副作用 — `HIGH` | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0088 | F-50 UI アニメと画面遷移（Wipe）— 調整点は `0x568BF8` 一箇所 — `HIGH` | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0089 | F-51 フェードの正体は `FaderColor`、`FaderMoment` に差し替えれば消える — `HIGH` | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0090 | F-52 静的解析の本体を `code.bin.i64` に移した — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0091 | F-53 RTTI から全クラス名をデマングルして命名した — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0092 | F-54 CTRPF プラグインの地域別アドレス表 — 本ビルドは **JPN 無印** — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0093 | F-55 Vapecord のコードを手がかりにした関数解析（時刻・部屋・通信） — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0094 | F-56 `ACNL_ID_Lists-master` との照合 — 4 件確定・1 件は資料側が誤り — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0095 | F-57 ゲーム内メニューを ID で開く仕組み — 日付変更ウィンドウは `MenuID 0x2E` — `HIGH` | HIGH | ? | consolidated | topics/acnl/ui.md | 訂正あり |
| ACNL-F0096 | F-58 【訂正】FOXXY はゲーム本来の日付変更ウィンドウを開いていた — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0097 | F-59 FOXXY 時間変更チートの残り 2 パッチ — 演出をメニュー姿勢に差し替えている — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0098 | F-60: Vapecord の時間設定チートと、ゲーム自身の時計確定経路 | HIGH | ? | active |  |  |
| ACNL-F0099 | F-61: `REFERENCES/CHEATS/drop.cpp` の「host drop」の正体 | HIGH | ? | active |  | 訂正あり |
| ACNL-F0100 | F-62: チート「ドロップ16x16」（`REFERENCES/CHEATS/drop.txt`） | HIGH | ? | active |  |  |
| ACNL-F0101 | F-63: `REFERENCES/CHEATS/drop.txt` の「host drop」— `drop.cpp` にない 6 行 | HIGH | ? | active |  |  |
| ACNL-F0102 | F-64: FOXXY の `pseudoType0x21` と、FOXXY 用 USA→JPN 変換 | HIGH | ? | active |  |  |
| ACNL-F0103 | F-65: 通常ドロップの入口と、種別を変える AR コード | HIGH | ? | active |  |  |
| ACNL-F0104 | F-66: オンライン髪型変更は虫取り網アクションから美容室状態 `0xB9` への迂回 | MEDIUM | ? | active |  |  |
| ACNL-F0105 | F-67: 髪型変更状態 `0xB9` が帽子・アクセサリを消し、2 段アニメが反映を遅らせる | MEDIUM | ? | active |  |  |
| ACNL-F0106 | F-68: オフラインなら profile の HairStyle だけを書いて `vc_UPDATE` すれば即時・装備保持にできる | HIGH | ? | active |  |  |
| ACNL-F0107 | F-69: 通常カタログは屋外表示可能。壊れる根因は店内限定の検索 `DICT` | HIGH | ? | active |  |  |
| ACNL-F0108 | F-70: 標準カタログの家具3Dは `BsFtrMgr` 経路。stock屋外はmanagerを生成しない | HIGH | ? | active |  |  |
| ACNL-F0109 | F-71: 通常Xの実入口は `sub_6D62AC` の動的menuId呼出し `0x6D6338` | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0110 | F-72: `0x6D6338` はカタログ起動確認点として正しいが、持ち物全体の置換点としては遅すぎる | HIGH | ? | active |  |  |
| ACNL-F0111 | F-73: 通常Xのfield側入口は `sub_165B40 -> sub_5C1F08`。診断traceのPC相対LDR移設は不可 | HIGH | ? | active |  |  |
| ACNL-F0112 | F-74: field持ち物の開始点はplayer state `0x16`。同位置で公式catalog要求へ置換可能 | HIGH | ? | active |  |  |
| ACNL-F0113 | F-75: 「メニュー切り替え」enter入口なら持ち物UI初期化前に差替えられる | HIGH | ? | active |  |  |
| ACNL-F0114 | F-76: stock「メニュー終了まで待機」はcatalog終了の橋渡し候補 | HIGH | ? | active |  |  |
| ACNL-F0115 | F-77: catalog表示後にstock「上タブをすべてアウト」を走らせる構成 | HIGH | ? | active |  |  |
| ACNL-F0116 | F-78: タブ退場開始条件は要求成功ではなく実画面のmenu flag `0x08` | HIGH | ? | consolidated | topics/acnl/ui.md | 訂正あり |
| ACNL-F0117 | F-79: 実画面生成成功の同期点は `Menu_PollOpen -> UiScreen_OpenById` の戻り | HIGH | ? | consolidated | topics/acnl/ui.md | 訂正あり |
| ACNL-F0118 | F-80: `BsMenuCatalog` は通常下画面メニューの `0x08/0x10` handshakeを実装しない | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0119 | F-81: constructor成功同期版はCatalogを生成後、`0x20`で表示前に自己終了させる | HIGH | ? | active |  |  |
| ACNL-F0120 | F-82: Catalog終了はfield X ownerを戻さず、3D経路には屋外hard rejectがない | HIGH | ? | active |  |  |
| ACNL-F0121 | F-83: `BsFtrMgr` のglobal公開は生成完了より早く、完全readyはobject `+19` の下位2bit | MEDIUM | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0122 | F-84: Catalog actor typeはItemParam由来。`AcFtr` はbank確保、model非同期読込、layer 2登録の3 phase | MEDIUM | ? | active |  |  |
| ACNL-F0123 | F-85: CameraCatalog、Catalog専用3灯、3つのrenderer layerはroom 0にも存在する | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0124 | F-86: parent拒否説を撤回。`ScStage` と`BsMenuTab`はいずれもchild gateを通る | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0125 | F-87: room 0の38-bank late allocationがphase 1即時失敗の最有力。容量1版を準備 | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0126 | F-88: phase 1公開中にstock previewへ戻るとtype `0xBC`を早期生成してSIGSEGVになる | HIGH | ? | active |  |  |
| ACNL-F0127 | F-89: 2回目の同一SIGSEGVはmanager phase 3の屋外map走査。Catalog選択品とは別 | HIGH | ? | active |  |  |
| ACNL-F0128 | F-90: 3回目は選択Item `0x2EA3` のtype `0xBC`。基底`AcFtr`置換でgeneric create完了 | HIGH | ? | active |  |  |
| ACNL-F0129 | F-91: `1UPキノコ` はfamily 3/type `0xBD`でも同じvptr+8 crash。preview特殊type全域を基底化 | HIGH | ? | active |  |  |
| ACNL-F0130 | F-92: rev7は家具3Dには成功。壁紙・絨毯は非表示、服カテゴリは`ModelInstance_SetRenderLayer`でSIGSEGV | HIGH | ? | active |  |  |
| ACNL-F0131 | F-93: ドロップの可否判定は 2 段。F-65 コード B が無効だった理由 | HIGH | ? | active |  |  |
| ACNL-F0132 | F-94: 描画スタックの同定と GSP IPC 層 | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0133 | F-95: GPU コマンドバッファ `g_GpuCmdPtr` の特定 | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0134 | F-96: コマンドリストの終端・提出経路と GX API 一式 | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0135 | F-97: `GpuCmd_GetProperty` と、自前コマンド追加の定石 | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0136 | F-98: TODO-37 の否定と、描画解析の全体精査 | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0137 | F-99: 描画解析の再精査 — 数値変換 2 件とレジスタ名 3 件の誤りを訂正 | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0138 | F-100: 再々精査 — GX 5 本の type バイト確定、「実装位置」表記の誤りを訂正 | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0139 | F-101: CLAUDE.md 準拠での再精査 — confidence の系統的誤り | MEDIUM | ? | active |  |  |
| ACNL-F0140 | F-102: ★実機観測でコマンドバッファ構造を確定（初の HIGH） | HIGH | ? | active |  |  |
| ACNL-F0141 | F-103: ★GX キューを実機で直接読み、1 フレームの構成を観測 | HIGH | ? | active |  |  |
| ACNL-F0142 | F-104: ★single-step 無効なら breakpoint が使える。`GpuCmd_SplitAndSubmit` の呼び出し元を捕捉 | HIGH | ? | active |  |  |
| ACNL-F0143 | F-105: ★MCP 側から Suspend できる（CLAUDE.md の記述を訂正） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0144 | F-106: ★`g3d::FuncNode` — 描画中に任意の関数を呼べるシーンノード | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0145 | F-107: ★`g3d::FuncNode` の実在を確認。コールバック登録 API まで判明 | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0146 | F-108: FuncNode 解析の精査 — 前提の再検証と 1 件の見落とし | MEDIUM | ? | active |  |  |
| ACNL-F0147 | F-109: ★★実機で `g3d::FuncNode` の実在とコールバックを確認（HIGH 達成） | HIGH | ? | active |  |  |
| ACNL-F0148 | F-110: ★`Use stepping support` を OFF にしても、ヒットした bp の削除は必要（TODO-54 完了） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0149 | F-111: ★★TODO-60 解決 — ノードをシーンに載せる仕組み（`Scene_SubmitNode`） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0150 | F-112: ★★実機で F-111 を検証（TODO-64 完了）— 確度 `HIGH` へ。配列 #5 の記述を訂正 | HIGH | ? | active |  | 訂正あり |
| ACNL-F0151 | F-113: ★★TODO-68 完了 — `BsShadowViewMgr` が実例。フレーム描画の全体像と `1024`/`1040` の正体 | HIGH | ? | active |  | 訂正あり |
| ACNL-F0152 | F-114: ★★TODO-71 完了 — 描画コールバックが積むものの全体像（自前描画の手本） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0153 | F-115: ★F-110〜F-114 の精査（TODO-75 の前の検証）— 誤り 2 件・過剰主張 3 件を訂正 | HIGH | ? | active |  |  |
| ACNL-F0154 | F-116: ★★TODO-75 第1段達成 — シーンへノードを追加できた。あわせて Suspend の条件を確定 | HIGH | ? | active |  | 訂正あり |
| ACNL-F0155 | F-117: ★TODO-79 完了 — `DUP=True` はハングしなかった。F-116 の「ハングの疑い」は誤り | HIGH | ? | active |  |  |
| ACNL-F0156 | F-118: ★★注入した描画が画面に出ることを視覚的に確認。影は「アルファのみ」 | HIGH | ? | superseded |  |  |
| ACNL-F0157 | F-119: ★★TODO-80 完了 — 自前の `g3d::FuncNode` を生成し、毎フレーム呼ばせることに成功 | HIGH | ? | active |  |  |
| ACNL-F0158 | F-120: ★★★TODO-81 達成 — 自前の `FuncNode` から実際に画面へ描画できた | HIGH | ? | active |  |  |
| ACNL-F0159 | F-121: ★★TODO-84 第1段 — 積まれたコマンドを自分で解釈・書き換え、描画結果を狙って変えられた | HIGH | ? | active |  |  |
| ACNL-F0160 | F-122: ★★★TODO-84 達成 — 完全自己完結の自前描画。あわせて TODO-83 も解決 | HIGH | ? | active |  |  |
| ACNL-F0161 | F-123: ★★TODO-87 — 影のテクスチャの実体を特定し、書き換えて画面に反映させた | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0162 | F-124: ★★★TODO-90 達成 — 自前の画像を任意のフォーマットで画面に表示した | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0163 | F-125: ★★★テキストを画面に描画した。タイル内 Morton スウィズル順も確定 | HIGH | ? | active |  |  |
| ACNL-F0164 | F-126: ★★★TODO-94 達成 — UI 層（`nw::lyt::TextBox`）に自前の 2D テキストを出した | HIGH | ? | active |  |  |
| ACNL-F0165 | F-127: ★★`nw::lyt::TextBox` の構造を実機で確定 — 位置・色・サイズを自由に変えられる | HIGH | ? | active |  |  |
| ACNL-F0166 | F-128: ★★★ドロップシャドウの正体 — フォントではなく「もう 1 枚のペインを 1 ドットずらして描く」 | HIGH | ? | active |  |  |
| ACNL-F0167 | F-129: `TextBox+224` は `nw::font::ResFont*`。実機には少なくとも4種の初期化済みCFNUがある | HIGH | ? | active |  | 訂正あり |
| ACNL-F0168 | F-130: ResFontのCMAP代替処理を確定。全liveフォントは2種の線形フィルタflagがON | HIGH | ? | active |  |  |
| ACNL-F0169 | F-131: TextBoxの折り返しはpane幅、縦方向は非clip。右端欠けの境界はCWDH glyphWidth | HIGH | ? | active |  |  |
| ACNL-F0170 | F-132: 非整数倍率が右端の不均一さを生む — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0171 | F-133: ResFont の CFNU/CFNT glyph-sheet atlas 経路を静的再監査 — `MEDIUM`（静的構造）/ `LOW`（再利用手順） | MEDIUM | ? | active |  |  |
| ACNL-F0172 | F-134: EmitGlyphQuad の texture handle 選択と batch/immediate 分岐を静的再監査 — `MEDIUM` | MEDIUM | ? | active |  |  |
| ACNL-F0173 | F-135: `code.bin.i64` と `code_runtime.elf.i64` の独立照合 — `HIGH`（同一バイト列・アドレス）/ `MEDIUM`（実機での意味づけ） | HIGH | ? | active |  |  |
| ACNL-F0174 | F-136: atlas flush wrapper の同一視を撤回 — `MEDIUM`（呼び出し規約）/ `LOW`（command 名） | MEDIUM | ? | active |  |  |
| ACNL-F0175 | F-137: `SetGlyphTextureParams` の引数は decompiler 表示より多く使われる — `MEDIUM` | MEDIUM | ? | active |  |  |
| ACNL-F0176 | F-138: ida-pro-mcp の実機接続経路を復旧・検証 — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0177 | F-140: TextBox→TextWriter の描画入口と後処理 — `MEDIUM`（静的） | MEDIUM | ? | active |  |  |
| ACNL-F0178 | F-141: TextWriter wrapper のコピー範囲と reset の実体 — `HIGH`（静的命令列） | HIGH | ? | active |  |  |
| ACNL-F0179 | F-143: TextBox vtable の実描画入口は `0x73CF48` — `HIGH`（静的＋実機） | HIGH | ? | active |  |  |
| ACNL-F0180 | F-142: EmitGlyphQuad は会話外 UI でも共有される — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0181 | F-139: ResFont→CMAP→batch quad の実機経路を確認 — `HIGH`（経路・引数・構造） | HIGH | ? | active |  |  |
| ACNL-F0182 | F-156: ★★★submit descriptor を静的に全導出。F-155a の observer は不要になった | HIGH | ? | active |  | 訂正あり |
| ACNL-F0183 | F-157: ★★★テキスト描画コマンドの投入を自前で駆動できた。色バイト順も確定 — `HIGH`（静的導出＋実機で視認） | HIGH | ? | active |  |  |
| ACNL-F0184 | F-158: ★★自前の変換行列でテキストを任意位置に描けた — `HIGH`（静的導出＋実機で視認） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0185 | F-159: コードケーブに使える領域は `0x01E82000` で終わる — `HIGH`（実機で読み書き検証） | HIGH | ? | active |  |  |
| ACNL-F0186 | F-160: テキスト描画の座標系を確定。F-158 の「1.25 = 400/320」は誤り — `HIGH`（実機で基準行列を採取＋3 枚の配置と照合） | HIGH | ? | active |  |  |
| ACNL-F0187 | F-161: ★★ケーブは `.text` 末尾のゼロ埋めに置く。ただし `.text` へは書けない — `HIGH`（実機の SIGSEGV と復帰で確認） | HIGH | ? | active |  |  |
| ACNL-F0188 | F-162: ★★★「好きな位置に好きなテキストを好きな色で」が通った — `HIGH`（実機で視認＋メモリで確認） | HIGH | ? | active |  |  |
| ACNL-F0189 | F-163: ★CTRPF プラグインは GPU 可視メモリを確保できない — `HIGH`（実機で検証、結果コードまで確認） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0190 | F-164: `g_GfxAllocator` の正体と呼び出し規約を確定 — `HIGH`（静的解析、assembly まで確認） | HIGH | ? | active |  |  |
| ACNL-F0191 | F-165: ゲームのアロケータをフックから呼べた。0x80 境界・linear 窓内 — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0192 | F-166: ★★★GPU 可視性を証明した。ゲームのアロケータから GPU が読めるメモリを得られる — `HIGH`（実機で視認） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0193 | F-167: ★★★テキストのグリフは「定数から四角形を生成するシェーダ」で描かれる。頂点データが存在しない — `HIGH`（実機の batch を解読） | HIGH | ? | active |  |  |
| ACNL-F0194 | F-168: ★★★任意の大きさの四角形を描けた。TODO-119 達成 — `HIGH`（実機で視認） | HIGH | ? | active |  |  |
| ACNL-F0195 | F-169: ★★★自前テクスチャを自前サイズの四角形に貼れた。TODO-120 達成 — `HIGH`（実機で視認） | HIGH | ? | active |  |  |
| ACNL-F0196 | F-170: CTRPF は発行点の問題を解決しない。cursor は値渡しでグローバルに無い — `HIGH`（静的解析、assembly で確認） | HIGH | ? | active |  |  |
| ACNL-F0197 | F-171: ★TextBox の描画は歩行中ゼロ。相乗り方式には大きな穴がある — `HIGH`（実機で計測） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0198 | F-172: ★★★TextBox に依らない発行点を特定。答えは自分の記録の中にあった — `HIGH`（静的＋実機で前提を確認） | HIGH | ? | active |  |  |
| ACNL-F0199 | F-173: 発行点への注入は成功したが GPU が固まった。捕獲した列は自己完結していない — `HIGH`（実機、フリーズ） | HIGH | ? | active |  |  |
| ACNL-F0200 | F-174: 発行点への注入は確立したが、GPU 状態の再現は現実的でない。方針を変えるべき — `HIGH`（実機で反復検証） | HIGH | ? | active |  |  |
| ACNL-F0201 | F-175: ★★★Picture は毎フレーム必ず描かれる。TextBox ではなく Picture に相乗りすべきだった — `HIGH`（実機で計測） | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0202 | F-176: Picture はコマンドを直接吐かず、描画コンテキストに四角形を溜めて一括で流す — `HIGH`（静的解析） | HIGH | ? | active |  |  |
| ACNL-F0203 | F-177: ★★★`nwlyt_Pane_DrawRecursive` は 1 フレームも欠けない。TODO-115 の答え — `HIGH`（実機で計測） | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0204 | F-178: 描画コンテキストの四角形配列を解読。`+1648` は F-167 の `c[0x40]` そのもの — `HIGH`（実機で採取） | HIGH | ? | active |  |  |
| ACNL-F0205 | F-179: Vapecord のマップ上プレイヤー表示は OSD（フレームバッファ直描き）だった — `HIGH`（ソース確認） | HIGH | ? | active |  |  |
| ACNL-F0206 | F-180: ★★★UI 画像を「足す」ことに成功。TODO-122 の主要部達成 — `HIGH`（実機で視認） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0207 | F-181: ★★★自前の UI 画像を毎フレーム 1 枚、画面に出せた。アルファブレンドも効く — `HIGH`（実機で視認） | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0208 | F-182: 追加した UI 画像を絶対座標で置けた。複製元は地図の影 — `HIGH`（実機で A/B） | HIGH | ? | active |  |  |
| ACNL-F0209 | F-183: ★索引エントリの `w3` は「色」。テクスチャはバッチ単位 — `HIGH`（静的解析） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0210 | F-184: 頂点カラーはアルファだけが効いた。RGB は素材の TexEnv 次第 — `HIGH`（実機で A/B） | HIGH | ? | active |  |  |
| ACNL-F0211 | F-185: ★★★フック地点で **`R1` がコマンドカーソル**。任意の GPU コマンドを発行できる — `HIGH`（実機のコマンド列で確認） | HIGH | ? | active |  |  |
| ACNL-F0212 | F-186: ★索引エントリの意味を静的に確定。色は複製先ではなく**複製元**に出る — `HIGH`（静的＋実機 A/B 多数） | HIGH | ? | active |  |  |
| ACNL-F0213 | F-187: ★ゲーム自身の「色つきスプライト」を実測。構造は自前と同一だった — `HIGH`（実機フック） | HIGH | ? | active |  |  |
| ACNL-F0214 | F-189: ★★★色ブロックの並びを確定。4 隅は「左上→右上→左下→右下」 — `HIGH`（実機で直接可視化） | HIGH | ? | active |  |  |
| ACNL-F0215 | F-190: ★★★★色・位置・大きさの完全制御を達成。詰まっていた原因は**アンカー** — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0216 | F-191: ★★★★自前テクスチャの適用に成功。欠けていたのは `reg 0x083` — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0217 | F-192: ★★★★フラッシュは配列の `[0].w0` を破壊する。退避先はポインタ −4 — `HIGH`（静的＋実機） | HIGH | ? | active |  |  |
| ACNL-F0218 | F-193: ★★★★★自前スプライトを独立したバッチで描画。テクスチャも独立 — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0219 | F-194: ★★★UV の座標系を確定。アトラスから切り出せる — `HIGH`（実機で 3 段階の A/B） | HIGH | ? | active |  |  |
| ACNL-F0220 | F-195: ★★★★★自前ビットマップフォントで文字列を描画。描画順も制御 — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0221 | F-196: ★★★★フルカラー画像（RGBA8）の表示を確定 — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0222 | F-197: ★★★コマンドバッファは 1 つではない。`g_GpuCmdPtr` と `g_GpuCmdEnd` は別リストのことがある — `HIGH`（GPU ハングで判明） | HIGH | ? | active |  |  |
| ACNL-F0223 | F-198: ★★★★7 枚超の描画と、ドット絵をきれいに出すための 4 条件 — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0224 | F-199: ★★★★★UI の座標系を確定。**縦横で縮尺が違う（非等方）** — `HIGH`（実機で段階的に測定） | HIGH | ? | superseded | topics/acnl/ui.md |  |
| ACNL-F0225 | F-200: ★★★★★UI は「1 本のコマンド列」ではない。記録と再生に分かれている — 静的解析 |  | ? | active |  | 訂正あり |
| ACNL-F0226 | F-201: F-200 の検証。**1 件の訂正と、GPU ハングの静的な説明** — 静的解析 | HIGH | ? | active |  |  |
| ACNL-F0227 | F-202: ★★★メインリストの末尾に積んでも UI は描かれない。2 回目のクラッシュの原因 — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0228 | F-203: ★★★★★最後に再生されるレイアウトは固定。注入点が確定 — `HIGH`（実機 301 フレーム） | HIGH | ? | superseded | topics/acnl/ui.md |  |
| ACNL-F0229 | F-204: ★★★レイアウトの記録は「記録要求フラグ」が立っているときだけ走る — `HIGH`（静的＋実機） | HIGH | ? | superseded | topics/acnl/ui.md |  |
| ACNL-F0230 | F-205: ★★★★「最後に再生される」は画面（描画パス）ごとに違う — `HIGH`（実機 120 フレーム） | HIGH | ? | superseded | topics/acnl/ui.md | 訂正あり |
| ACNL-F0231 | F-206: ★★★★色とテクスチャの出所は「マテリアル」。自前で積まないと直前のペインのものになる — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0232 | F-207: ★★★★★`drawctx+1692` が 0 だと UV が読まれずテクスチャ全面が貼られる — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0233 | F-208: ★★★★★レイアウトごとに投影が違う。相乗り先を変えたら縮尺を測り直す — `HIGH`（実機） | HIGH | ? | superseded | topics/acnl/ui.md |  |
| ACNL-F0234 | F-209: ★★★★★TODO-131 完了。自前 GUI が常に最前面に描かれる — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0235 | F-210: ★★★★★狙う相手をリスト id で固定してはいけない。実行時に追いかける — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0236 | F-211: ★★★★マテリアルは「たまたま」ではなく条件で選ぶ — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0237 | F-212: ★★★★★マテリアルには名前と定数色が入っている — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0238 | F-213: ★★★★CTRPF プラグインへの移植 — ケーブは書き直さずバイト列ごと移す — `HIGH`（ビルド済み・実機未検証） | HIGH | ? | active |  |  |
| ACNL-F0239 | F-214: ★★★★★中立なマテリアルが 1 つも無い場面がある。定数色は借りる側で中立化する — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0240 | F-215: ★★★★★借りたマテリアルは 9 語まとめて中立化する。ただし描画後に積み直してはいけない — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0241 | F-216: ★★★★★`reg 0x082` は `(幅<<16)\|高さ`。正方形しか試していないと気付けない — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0242 | F-217: ★★★★SD から任意の画像を読む（TODO-130 完了）— `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0243 | F-218: ★★★半透明（アルファブレンド）は使える — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0244 | F-219: ★★★CTRPF のファイルパスはプラグインのフォルダ基準。ON が早すぎると落ちる — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0245 | F-220: ★★★TODO-134 段 B 完成 — 上下画面の描き分けとチャンク別の色 — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0246 | F-221: ★★ゲームのアロケータから取れるのは 0x4000 まで — `HIGH`（実機） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0247 | F-222: ★★★★★自前チートメニューが実機で動いた。ゲームは止まらない — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0248 | F-223: ★★★★描くものが無いのに記録を強制すると、しばらくして GPU コマンドリストが枯れる — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0249 | F-224: ★★★★★確定した対象を「0 以外のときだけ更新」してはいけない — `HIGH`（実機） | HIGH | ? | consolidated | topics/acnl/ui.md | 訂正あり |
| ACNL-F0250 | F-225: ★★★★「開いている間だけ描く」にすると、閉じても最後の絵が残り続ける — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0251 | F-226: ★★★★★相乗り先は「素で記録し直される」ものから選ぶ。強制は廃止 — `HIGH`（実機） | HIGH | ? | consolidated | topics/acnl/ui.md | 訂正あり |
| ACNL-F0252 | F-227: ★★★観測用の領域を、動いている描画の領域と重ねてクラッシュさせた — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0253 | F-228: ★★★★フェードは id 8（上）/ id 9（下）が最後に描く。両方に積めば判別が要らない — `HIGH`（実機） | HIGH | ? | superseded | topics/acnl/ui.md |  |
| ACNL-F0254 | F-229: ★★★ケーブどうしの重なりは目視では見つからない。機械的に検査する — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0255 | F-230: ★★★★相乗り先は「候補のうち最後に再生されたもの 1 つ」。両方に積むと二重になる — `HIGH`（実機） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0256 | F-231: ★★★★★リスト id 0 を「未設定」として弾かないと、id 0 のレイアウトと誤って一致する — `HIGH`（実機） | HIGH | ? | consolidated | topics/acnl/ui.md | 訂正あり |
| ACNL-F0257 | F-232: ★★★★★レイアウトの記録リストには容量がある。積みすぎると落ちる — `HIGH`（実機） | HIGH | ? | consolidated | topics/acnl/ui.md | 訂正あり |
| ACNL-F0258 | F-233: 描画パス末尾と通常場面の実 replay を再監査 — `HIGH`（静的＋実機。ロード画像の順序は未測定） | HIGH | ? | active |  |  |
| ACNL-F0259 | F-234: ロード画像は上画面で id 8 の後に replay される Layout id 10 — `HIGH`（静的＋実機＋リソース同定） | HIGH | ? | superseded | topics/acnl/ui.md |  |
| ACNL-F0260 | F-235: `Frame_EndDrawPass1024` 主リスト末尾の手製 Drawer-state 版は安全な提出経路ではない — `MEDIUM`（静的＋実機失敗） | MEDIUM | ? | active |  |  |
| ACNL-F0261 | F-238: ロード表示中でも top LayoutList の構成はフェーズで変わる — `MEDIUM`（独立した stopped snapshot＋no-draw 実行標本） | MEDIUM | ? | superseded | topics/acnl/ui.md |  |
| ACNL-F0262 | F-241: lifecycle trace の block-copy emitter は loader Layout を破損する — `HIGH`（生成命令＋実機レジスタ＋破損メモリ） | HIGH | ? | active |  |  |
| ACNL-F0263 | F-237: Layout の再生順は `LayoutList_SetDisplay` で局所的に制御できる — `MEDIUM`（静的＋実機 no-draw） | MEDIUM | ? | active |  |  |
| ACNL-F0264 | F-236: Layout record-list のバッファ本体は安全に差し替える必要がある — `MEDIUM`（静的＋ゼロ長実機経路） | MEDIUM | ? | superseded | topics/acnl/ui.md |  |
| ACNL-F0265 | F-242: `GardenSound.bcsar` を解読し、全 4,266 音の名前・ID・カテゴリを確定 — `HIGH`（独立 3 系統の一致） | HIGH | ? | active |  |  |
| ACNL-F0266 | F-243: CSEQ バイトコードの命令表を確定（ラベル境界一致 100.00%） — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0267 | F-244: seq 型サウンド 2,839 件を WAV に合成 — `MEDIUM`（構造は HIGH、包絡の時定数は近似） | MEDIUM | ? | active |  |  |
| ACNL-F0268 | F-245: ループ波形が音符の途中で切れていた — `HIGH`（実機録音との突き合わせで確定） | HIGH | ? | active |  |  |
| ACNL-F0269 | F-246: ポルタメントの2つの誤り — `HIGH`（実機との聴き比べで確定） | HIGH | ? | active |  |  |
| ACNL-F0270 | F-247: 実機との聴き比べで、包絡とビブラートの定数を較正 — `HIGH`（実機一致を利用者が確認） | HIGH | ? | active |  |  |
| ACNL-F0271 | F-248: 包絡の換算 3 箇所を実機録音で確定 — `HIGH`（録音との数値照合＋利用者の耳） | HIGH | ? | active |  |  |
| ACNL-F0272 | F-249: 音量・ベロシティは振幅の 2 乗側 — `HIGH`（実機録音との数値照合 0.3dB 以内） | HIGH | ? | active |  |  |
| ACNL-F0273 | F-250: 未設定の変数に対する比較が 712 件を無音にしていた — `HIGH`（全件バッチで確認） | HIGH | ? | active |  |  |
| ACNL-F0274 | F-251: 合成の 4 つの欠陥を実機との聴き比べで修正 — `HIGH`（利用者が実機一致を確認） | HIGH | ? | active |  |  |
| ACNL-F0275 | F-252: 2D レイアウトの描画は「1 本のリストを画面ごとに 2 回再生」する — `HIGH`（静的。動的照合は未実施） | HIGH | ? | consolidated | topics/acnl/ui.md | 訂正あり |
| ACNL-F0276 | F-253: ★★★★★描画パスは 3 本。`Frame_DrawPass1040` は下画面ではなく「上画面の右目」 — `HIGH`（静的＋実機の独立 2 系統） | HIGH | ? | superseded |  |  |
| ACNL-F0277 | F-254: ★★★★★自前の Layout ノードを登録すれば、上下とも「最前面」に必ず入れる — `HIGH`（実機） | HIGH | ? | superseded | topics/acnl/ui.md |  |
| ACNL-F0278 | F-255: 自前 Layout ノードから実際に描けた。ロード画像より前面 — `HIGH`（実機・目視） | HIGH | ? | superseded | topics/acnl/ui.md |  |
| ACNL-F0279 | F-256: ★★★★★ゲームがそのパスで 1 枚も描いていないと、描画コマンドを積んだ瞬間に GPU が止まる — `HIGH`（実機で二分により確定） | HIGH | ? | active |  |  |
| ACNL-F0280 | F-257: ★★★★F-256 のゲートの正体は「ゲームが**記録し直した**フレームだけ描く」だった — `HIGH`（実機・目視） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0281 | F-258: 作業配列を自前バッファへ差し替える案は失敗した — `HIGH`（実機・目視） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0282 | F-259: ★★★★★UI 描画経路の完全な静的仕様。render.txt は本作と 1:1 で一致する — `HIGH`（静的のみ） | HIGH | ? | active |  |  |
| ACNL-F0283 | F-260: F-259 の設計を実装し、IDA の逆アセンブルで検証した（実機未適用） — `HIGH`（静的のみ） | HIGH | ? | active |  |  |
| ACNL-F0284 | F-261: ★★★★★Layout の初期化 `sub_5685A4` に「自前リストの正しい作り方」が全部書いてある — `HIGH`（静的のみ） | HIGH | ? | active |  |  |
| ACNL-F0285 | F-262: 再生の複製経路を逆アセンブルで裏取りし、実装の誤り 2 件を追加で直した — `HIGH`（静的のみ） | HIGH | ? | active |  |  |
| ACNL-F0286 | F-263: ★★★★★F-257 / F-258 の説明は誤りだった。作業配列は Drawer の**固定メンバ**である — `HIGH`（静的） | HIGH | ? | active |  |  |
| ACNL-F0287 | F-264: 自前ノードの幅・高さは雛形任せにせず画面実寸を明示する — `HIGH`（静的のみ） | HIGH | ? | superseded | topics/acnl/ui.md |  |
| ACNL-F0288 | F-265: ★★★★★UI の投影行列の出所を確定した。**Layout+0x34 の 16 語**であり、記録時ではなく**再生時**に GPU へ流れる — `HIGH`（静的のみ） | HIGH | ? | superseded | topics/acnl/ui.md |  |
| ACNL-F0289 | F-266: ★★★★★`SetupProjectionMatrix` は **`+0x28` / `+0x2C` しか読まない**。だから自前ノードでもそのまま呼べる — `HIGH`（静的のみ） | HIGH | ? | active |  |  |
| ACNL-F0290 | F-267: 雛形の複製を廃止した。写し元依存が実装から消えた — `HIGH`（静的のみ） | HIGH | ? | active |  |  |
| ACNL-F0291 | F-268: ★★★★★Drawer の既定コマンド列には **TEV 段が 1 つも無い**。色は必ずマテリアル由来 — `HIGH`（静的のみ） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0292 | F-269: TEV を自前で組んだ。**設計から借り物が消えた** — `HIGH`（静的のみ） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0293 | F-270: ★★★★DrawBegin1 は **テクスチャユニットを全部無効にする**。自前記録では立て直さないとテクスチャが読まれない — `HIGH`（静的 + 過去の実測列） | HIGH | ? | active |  |  |
| ACNL-F0294 | F-271: ★★★★★`TextBox_UpdateDrawState`(`0x4B7DEC`) が「テクスチャ付き描画へ切り替える」全手順。実測列の全項目がこれで説明できた — `HIGH`（静的 + F-124 の実測列） | HIGH | ? | active |  |  |
| ACNL-F0295 | F-272: F-264〜F-271 の整合監査。独立な結果と突き合わせて 1 件の誤りを訂正し、`SET_PROJECTION` を廃止した — `HIGH` | HIGH | ? | active |  | 訂正あり |
| ACNL-F0296 | `SET_PROJECTION` を廃止した |  | ? | active |  |  |
| ACNL-F0297 | F-273: ★★★★★致命的なバグ。記録スロットのエピローグが `R4` = drawctx のまま `Commit` していた — `HIGH`（静的のみ・未適用） | HIGH | ? | active |  |  |
| ACNL-F0298 | F-274: `sub_2F858C` は **3 引数の memcpy**。decompiler が R1/R2 を落としていた — `HIGH`（アセンブリ） | HIGH | ? | active |  |  |
| ACNL-F0299 | F-275: 自前ノードに対してゲームが呼ぶのは vtable `+0x08` と `+0x14` の 2 つだけ — `HIGH`（静的） | HIGH | ? | active |  |  |
| ACNL-F0300 | F-276: ★★★★★【F-268 の訂正】既定ブロックは **記録時ではなく再生時**に出る。フラグで切り替わる — `HIGH`（アセンブリ） | HIGH | ? | active |  |  |
| ACNL-F0301 | F-277: 記録 → Commit → 再生の連鎖を端から端まで静的に証明した — `HIGH`（静的のみ） | HIGH | ? | active |  |  |
| ACNL-F0302 | リテラル参照の値まで検証する道具を追加した |  | ? | active |  |  |
| ACNL-F0303 | F-278: 座標系を上下とも静的に確定した。**1 単位 = 1px、原点は画面中央**。`c4` は恒久的にゼロ — `HIGH`（静的、実機実測と一致） | HIGH | ? | consolidated | topics/acnl/ui.md | 訂正あり |
| ACNL-F0304 | F-279: 検証道具を全ケーブに広げ、死語を 1 本落とした — `HIGH` | HIGH | ? | active |  |  |
| ACNL-F0305 | F-280: ★★★★★メニューを実際に描けるところまで実装した（フォント・レイアウト API・領域拡張） — `HIGH`（静的のみ・未適用） | HIGH | ? | active |  |  |
| ACNL-F0306 | F-281: ★★★★★実機で描画に成功した。ノイズの原因は**非整数倍の拡大** — `HIGH`（実機） | HIGH | ? | active |  |  |
| ACNL-F0307 | F-282: CTRPF プラグインへ移植した。**ビルド環境なしで移植の正しさを照合できる** — `HIGH`（静的のみ・未ビルド） | HIGH | ? | superseded |  |  |
| ACNL-F0308 | F-283: シミュレータ相当の UI へ作り直した（美咲フォント・アニメーション・項目型）— `HIGH`（ビルド済み・未適用） | HIGH | ? | active |  |  |
| ACNL-F0309 | F-284 (HIGH) — 自前 GUI（F-283 版）のクラッシュ `PC=0x839004` は「.text のゼロ埋めを NOP スライドして飛び出した」結果 | HIGH | ? | active |  |  |
| ACNL-F0310 | F-286 — F-283 / F-285 を捨てて **F-282（実機で描画に成功した版）へ巻き戻した** — `HIGH`（静的検証済み・実機未確認） | HIGH | ? | active |  |  |
| ACNL-F0311 | F-287 (HIGH) — ★明滅と「文字が板になる」の真因は **観測リングが自前 TEV を毎フレーム潰していた**こと | HIGH | ? | active |  |  |
| ACNL-F0312 | F-288 — Chokistream の画面を AI が直接見られる（動的解析の目視確認を自動化） |  | ? | active |  |  |
| ACNL-F0313 | F-289 (HIGH・実機) — ★`nwlyt_Picture_DrawToCommandList` に**自前 Picture** を渡して 1 枚描けた | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0314 | F-290 (HIGH・実機) — CAVE_Q を `Picture_DrawToCommandList` 呼びへ置き換えた。**座標系は手書き経路と同一** | HIGH | ? | active |  |  |
| ACNL-F0315 | F-291 (HIGH・静的のみ) — ★正体は **nw::lyt（NintendoWare Layout）**。Picture / Material の構造を静的に確定し、**既存文書の誤り 6 件を訂正** | HIGH | ? | consolidated | topics/acnl/ui.md | 訂正あり |
| ACNL-F0316 | F-292 (HIGH・静的のみ) — ★F-291 を別関数で再検証（矛盾なし）。**正規の手順なら記録ケーブは丸ごと不要** | HIGH | ? | active |  |  |
| ACNL-F0317 | F-293 (HIGH・実機) — ★★★正規の手順で描けた。**自前の記録ケーブ 205 語を撤去** | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0318 | F-294 (HIGH・静的のみ) — ★自前フォントで `TextBox` を使えることを確認。`Glyph` 構造を確定 | HIGH | ? | active |  |  |
| ACNL-F0319 | F-295 (HIGH・実機) — ★方式 (a) 完成。ヒープから借りて**メニュー全体を正規経路で描いた** | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0320 | F-296 (HIGH・実機) — ★借りた領域を返せる。**確保 → 解放 → 再確保の往復を実機で成立** | HIGH | ? | active |  |  |
| ACNL-F0321 | F-297 (HIGH・実機) — ★下画面のペインツリーを組んだ。**上下 2 画面が独立した輪で同時に描かれる** | HIGH | ? | consolidated | topics/acnl/ui.md | 訂正あり |
| ACNL-F0322 | F-298 (HIGH・静的のみ) — ★TextBox 方式は実装可能。**自前フォントの「コード」はほぼ要らない** | HIGH | ? | active |  | 訂正あり |
| ACNL-F0323 | F-299 (HIGH・静的＋実機の実データ照合) — ★F-298 の検証と**訂正 2 件**。バッチの確保元を特定（残件 1） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0324 | F-300 (HIGH・静的＋実機) — ゲーム内フォントを流用しても **TextBox は自前で要る**。ただしフォント側の合成は丸ごと不要になる | HIGH | ? | active |  | 訂正あり |
| ACNL-F0325 | F-301 (HIGH・静的のみ) — ★F-300 の訂正。**TextBox は必須ではない。**文字描画の本体は `TextWriter` | HIGH | ? | active |  |  |
| ACNL-F0326 | F-302 (HIGH・実機) — ★★TextBox が実機で描けた。**作業オブジェクト = `LayoutMgr + 0x1C`**。コードケーブ 0 語 | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0327 | F-303 (HIGH・実機) — ★借りた nw::lyt ヒープは **GPU 可視**。自前フォント資源の設計を確定（描画は未達） | HIGH | ? | active |  |  |
| ACNL-F0328 | F-304 (HIGH・実機) — ★`FINF+0x07` は**文字ストリーム読み取り器の選択**。1 以外だと PC=0 で落ちる | HIGH | ? | active |  |  |
| ACNL-F0329 | F-305 (HIGH・実機) — ★★★自前フォントで実機に描けた。`nw::font` の構造を**全欄**確定 | HIGH | ? | active |  |  |
| ACNL-F0330 | F-306 (HIGH・実機) — ★★★TextWriter 直呼びで描けた。TextBox の DrawSelf を通さない | HIGH | ? | active |  |  |
| ACNL-F0331 | F-307 (HIGH) — ★基準仕様 v2 を改訂し、**仕様書そのものを機械で検証**した | HIGH | ? | active |  |  |
| ACNL-F0332 | F-308: 大量の文字を登録したときの天井（TextWriter 直呼び方式の評価） — HIGH | HIGH | ? | active |  |  |
| ACNL-F0333 | F-309: nw::lyt のヒープは `sead::ExpHeap`。残量は 1,200,132 バイト — HIGH | HIGH | ? | active |  |  |
| ACNL-F0334 | F-310: 場面転換をまたぐと空きは 1.2MB → 0.6MB まで落ちる — HIGH | HIGH | ? | active |  |  |
| ACNL-F0335 | F-311: プラグインを基準仕様 v2 へ書き換えた（3gx 名 = gohan）— 実機未検証 |  | ? | active |  |  |
| ACNL-F0336 | F-311 追記: 実機で描画されなかった原因（2026-09-06）— HIGH | HIGH | ? | active |  |  |
| ACNL-F0337 | F-311 追記 2: 文字が乱れた原因は「中央整列での半画素」（2026-09-06）— HIGH | HIGH | ? | active |  |  |
| ACNL-F0338 | F-312: Simulator の 2 フォントを `nw::font` へ載せた（日本語 275 字を含む）— HIGH | HIGH | ? | active |  |  |
| ACNL-F0339 | F-313: 「実測でないと決められない」は誤り。静的に決着した — HIGH | HIGH | ? | active |  | 訂正あり |
| ACNL-F0340 | F-314: F-313 の裏取り。1 件は誤り、2 件は独立に裏付けが取れた — HIGH | HIGH | ? | active |  |  |
| ACNL-F0341 | F-315: F-312〜F-314 を実機で検証。**結論はすべて正しかった** — HIGH | HIGH | ? | active |  |  |
| ACNL-F0342 | F-316: ★シート記述子 `+0x0C` は **`(幅<<16) \| 高さ`** — HIGH | HIGH | ? | active |  |  |
| ACNL-F0343 | F-315 追記: 1 度目のクラッシュについて（原因は未確定） |  | ? | active |  |  |
| ACNL-F0344 | F-317: ★取り外しでコマンドリストを削除しておらず nngx ヒープが漏れる — HIGH | HIGH | ? | active |  | 訂正あり |
| ACNL-F0345 | F-318: F-317 の削除を実装。実機で **132,192 B が丸ごと戻った** — HIGH | HIGH | ? | active |  | 訂正あり |
| ACNL-F0346 | F-319（2026-09-06）: UI フォントを CTRPF プラグインへ組み込む | HIGH | ? | active |  |  |
| ACNL-F0347 | F-320（2026-09-06）: クラッシュダンプの読み方と `threadCreate` の落とし穴 | HIGH | ? | active |  | 訂正あり |
| ACNL-F0348 | F-322（2026-09-07）: 文字ペインの**横**にも半画素問題があった | HIGH | ? | active |  |  |
| ACNL-F0349 | F-323（2026-09-07）: パネルの縁がフェード途中で濃く残る（A案で修正） | MEDIUM | ? | active |  |  |
| ACNL-F0350 | F-324（2026-09-07）: リストボックスの背景が後ろの行文字より後ろだった | MEDIUM | ? | active |  |  |
| ACNL-F0351 | F-325（2026-09-07）: 段 6（上下リストボックス/ホットキー）・段 7（通知）を実装 | MEDIUM | ? | active |  |  |
| ACNL-F0352 | F-326（2026-09-07）: 実機報告の不具合1件と要望 R1〜R5 | MEDIUM | ? | active |  |  |
| ACNL-F0353 | F-327（2026-09-07）: 要望 R6a（縁も赤に）・R6b（適用時の通知を両方抑制） | MEDIUM | ? | active |  |  |
| ACNL-F0354 | F-329（2026-09-07）: 通知題の統一とホットキー・トグルの復帰 | MEDIUM | ? | active |  |  |
| ACNL-F0355 | F-328（2026-09-07）: 関数側連携の窓口（トグル実行は利用者が持つ） | MEDIUM | ? | active |  |  |
| ACNL-F0356 | F-330（2026-09-07）: OFF 通知の縁を帯より暗い赤に |  | ? | active |  |  |
| ACNL-F0357 | F-332（2026-09-07）: メニュー側のトグルをやめる |  | ? | active |  |  |
| ACNL-F0358 | F-333（2026-09-07）: トグル実行エンジン（壁抜け仕様の一般化） |  | ? | active |  | 訂正あり |
| ACNL-F0359 | F-331（2026-09-07）: トグル実行のライフサイクル連携 |  | ? | active |  |  |
| ACNL-F0360 | F-334（2026-09-07）: 効果の実体を関数登録に直す |  | ? | active |  |  |
| ACNL-F0361 | F-335（2026-09-07）: 複数パッチ切替と押し続け移動の再設計 |  | ? | active |  |  |
| ACNL-F0362 | F-336（2026-09-07）: 試験2項目へ効果配線（通知確認用） |  | ? | active |  |  |
| ACNL-F0363 | F-337（2026-09-07）: 共有バッチ（§3.2）へ移る前の静的解析 | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0364 | F-338（2026-09-07）: 記録量の式を実機で確定 | HIGH | ? | active |  |  |
| ACNL-F0365 | F-339（2026-09-07）: ★実機ゲート通過「1 本のバッチに複数の文字列」 | HIGH | ? | active |  |  |
| ACNL-F0366 | F-340 — 色替え・書体替えの費用を分解し、記録量の式を完成させた（2026-09-07・実機） | HIGH | ? | active |  |  |
| ACNL-F0367 | F-341（2026-09-07）: 費用の式を「当てはめ」から「逆アセンブルの写し」へ | HIGH | ? | active |  |  |
| ACNL-F0368 | F-342（2026-09-07）: 共有バッチの設計 — ★費用の 8 割は「コマンド語の器の取りすぎ」 | HIGH | ? | active |  |  |
| ACNL-F0369 | F-343（2026-09-07）: 空いた容量で通知を Simulator と同じ 7 件にした | HIGH | ? | active |  |  |
| ACNL-F0370 | F-344（2026-09-07）: ★手紙を開くと落ちる — 借用が nw::lyt ヒープを枯らしていた | HIGH | ? | active |  |  |
| ACNL-F0371 | F-345（2026-09-07）: 手紙は **2 つの大きな塊**を要る — 借りっぱなしでは通せない | HIGH | ? | active |  |  |
| ACNL-F0372 | F-346（2026-09-07）: ★アトラス以外をプラグインの `.bss` へ移した（借用 442,368 -> 36,864 B） | HIGH | ? | active |  |  |
| ACNL-F0373 | F-347（2026-09-07）: キーボード UI を足したときの見積もり（実装前の机上計算） | MEDIUM | ? | active |  |  |
| ACNL-F0374 | F-348（2026-09-07）: 基準仕様 v3 を制定した | HIGH | ? | active |  |  |
| ACNL-F0375 | F-349（2026-09-07）: Simulatorの文字・数値キーボードをCTRPFへ移植 | MEDIUM | ? | active |  |  |
| ACNL-F0376 | F-350（2026-09-07）: ★入力の無効化 — `0x32C85A2D` の正体と、全ボタン／タッチを塞ぐ場所 | HIGH | ? | active |  |  |
| ACNL-F0377 | F-351（2026-09-07）: 入力遮断をプラグインへ実装し、下画面ロックへ一本化した | HIGH | ? | active |  |  |
| ACNL-F0378 | F-352（2026-09-07）: ★実機報告 2 件 — タッチのビットを消していた（修正）／ SELECT は未解決 |  | ? | active |  |  |
| ACNL-F0379 | F-353（2026-09-07）: ★SELECT のビットは `0x800` — libctru の並びと違った（実測で確定） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0380 | F-354（2026-09-07）: ★タッチは 2 か所にある — hold の中のビットも消す（実機確認済み） | HIGH | ? | active |  |  |
| ACNL-F0381 | F-355（2026-09-07）: ★★ゲームは SELECT を START に読み替えている — 真因と正しい直し方 | HIGH | ? | active |  |  |
| ACNL-F0382 | F-356（2026-09-07）: ★「ゲームスピード変更」チート `0054C6E8` の正体 — フレームペーシングの無効化 | HIGH | ? | active |  |  |
| ACNL-F0383 | F-357（2026-09-08）: ★FPS だけ上げてゲーム速度を据え置くことはできない（実機計測つき） | HIGH | ? | active |  |  |
| ACNL-F0384 | F-358: 3DS内蔵ソフトウェアキーボードのAPIとCTRPFの条件（2026-09-08） | MEDIUM | ? | active |  |  |
| ACNL-F0385 | F-359: 内蔵漢字変換候補取得の目的・共有辞書候補・ゲーム内APT起動経路（2026-09-08） | LOW | ? | active |  |  |
| ACNL-F0386 | F-358（2026-09-08）: `BsFgProc::Setup` の正体 — `fgobj::Proc` のセットアップ段（＋しずえ会話スキップの下調べ） | MEDIUM | ? | active |  |  |
| ACNL-F0387 | F-359（2026-09-08）: ★起動シーケンスと「しずえ画面 → 村へ出る」経路（＋未知のコード領域の発見） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0388 | F-361（2026-09-08）: ★★★ACNL は CRO 動的モジュールを使う — しずえ画面を静的に解いた | HIGH | ? | active |  |  |
| ACNL-F0389 | F-362: 内蔵日本語辞書6本の取得・主要辞書75,770件の読み/候補を抽出（2026-09-08） | MEDIUM | ? | active |  |  |
| ACNL-F0390 | F-363: 内蔵キーボードの候補順位・文節変換・学習を原本ARMで再現（2026-09-08） | MEDIUM | ? | active |  |  |
| ACNL-F0391 | F-362（2026-09-08）: case 5 の `0x00606D78` と「準備しています」の出どころ | HIGH | ? | active |  |  |
| ACNL-F0392 | F-365（2026-09-08）: メニューON/OFF でホットキー判定を送る（opt-in） | MEDIUM | ? | active |  |  |
| ACNL-F0393 | F-366（2026-09-08）: しずえスキップをトグル式チートとして取込 | MEDIUM | ? | active |  |  |
| ACNL-F0394 | F-367（2026-09-08）: しずえスキップ取込後のクラッシュ切り分け（静的監査まで） |  | ? | active |  |  |
| ACNL-F0395 | F-368（2026-09-08）: クラッシュ点の特定（実機デバッグ。ida-pro-mcp 直読み） | HIGH | ? | active |  |  |
| ACNL-F0396 | F-369（2026-09-08）: クラッシュ原因は遷移フレームでの発火。安定ゲートで対策 |  | ? | active |  |  |
| ACNL-F0397 | F-370（2026-09-08）: クラッシュ再発。犯人は呼び出し元の this=NULL |  | ? | active |  |  |
| ACNL-F0398 | F-371（2026-09-08）: 訂正 pitch—項目OFF・発火なしでも落ちる |  | ? | active |  |  |
| ACNL-F0399 | F-372（2026-09-08）: E1—素では落ちない。チートON状態に絞られた |  | ? | active |  |  |
| ACNL-F0400 | F-373（2026-09-08）: ON直後クラッシュ。無罪のものとフック抜きビルド |  | ? | active |  |  |
| ACNL-F0401 | F-374（2026-09-08）: タイトルON直後の停止はフォールトではない＋描画系照合の途中経過 |  | ? | active |  |  |
| ACNL-F0402 | F-375（2026-09-08）: タイトルで即クラッシュ — 空リスト＋陳旧リンクの永久スキップ |  | ? | active |  |  |
| ACNL-F0403 | F-376（2026-09-08）: A1/A2 抜き診断ビルド（遷移クラッシュの切り分け用） |  | ? | active |  |  |
| ACNL-F0404 | F-377（2026-09-08）: クラッシュダンプ解読＋対象走行中 |  | ? | active |  |  |
| ACNL-F0405 | F-378（2026-09-08）: 実行構成がどのビルドとも一致しない |  | ? | superseded |  |  |
| ACNL-F0406 | F-379（2026-09-08）: 訂正 — 謎の構成は自前の診断フラグだった |  | ? | active |  |  |
| ACNL-F0407 | F-380（2026-09-08）: タイトルON後は正常動作。スレッド特定も確定 |  | ? | active |  |  |
| ACNL-F0408 | F-381（2026-09-08）: 診断フラグを戻しフルビルドへ。メニュー非表示の説明 |  | ? | active |  |  |
| ACNL-F0409 | F-384: 通常チャットから内蔵ソフトウェアキーボードを呼ぶケーブを適用（2026-09-09） | HIGH | ? | active |  |  |
| ACNL-F0410 | F-385: 通常チャットから内蔵SWKBDの起動・キャンセル復帰に成功（2026-09-09） |  | ? | active |  |  |
| ACNL-F0411 | F-386: 内蔵SWKBDの漢字確定文字を共有メモリから回収（2026-09-09） |  | ? | active |  |  |
| ACNL-F0412 | F-387: SWKBD実機の表示候補キャッシュ位置と読取器（2026-09-09） | MEDIUM | ? | active |  |  |
| ACNL-F0413 | F-388: ACNLのSuspendでは動作中SWKBDプロセスは停止しない（2026-09-09） |  | ? | active |  |  |
| ACNL-F0414 | F-389: 実機SWKBDから「かんじ」の全17候補と順位を回収（2026-09-09） | HIGH | ? | active |  |  |
| ACNL-F0415 | F-390: 破損した3gxをしずえスキップ統合前へ復元（2026-09-09） |  | ? | active |  |  |
| ACNL-F0416 | hidden letterの入場座標とCHEATS選択肢（2026-10-14） | MEDIUM | ? | active |  |  |
| ACNL-F0417 | T015の再実機訂正（2026-10-13） | MEDIUM | ? | active |  |  |
| ACNL-F0418 | UI入口・pocket再入場・非drag trash・青選択（2026-10-13） | MEDIUM | ? | active |  |  |
| ACNL-F0419 | 持ち物・trash・selected行の実機不具合訂正（2026-10-13） | MEDIUM | ? | active |  |  |
| ACNL-F0420 | list再tap・drag倍率・pocket操作（2026-10-13） | MEDIUM | ? | active |  |  |
| ACNL-F0421 | widget画像の参照寿命とcloset帰還・page待ち（2026-10-12） | MEDIUM | ? | active |  |  |
| ACNL-F0422 | closet直通とnative転送・低ID/ウィジェット（2026-10-12） | MEDIUM | ? | active |  |  |
| ACNL-F0423 | 普通チャットのキャンセル・実退場とタブ復帰（2026-10-12） | MEDIUM | ? | active |  |  |
| ACNL-F0424 | nativeクローゼットとmenu intrusive node（2026-10-12） | MEDIUM | ? | active |  |  |
| ACNL-F0425 | F005のHHD引継ぎ要件を訂正（2026-10-12） |  | ? | active |  |  |
| ACNL-F0426 | Controller画素座標/vtableとchat画面引継ぎ（2026-10-12） | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0427 | native scrollの別入力経路とstyle arc一時pool（2026-10-12） | MEDIUM | ? | active |  |  |
| ACNL-F0428 | chat listの決定と時刻窓からのfield復帰（2026-10-12） |  | ? | active |  |  |
| ACNL-F0429 | gohanへのidle/気絶/消失抑制・チャット移植（2026-10-11） |  | ? | active |  |  |
| ACNL-F0430 | 収録チートの天気返却と島チャット数字制限の意味（2026-10-11） | MEDIUM | ? | active |  |  |
| ACNL-F0431 | 全収録チートの意味コメント調査（2026-10-11、利用者指示で中断） |  | ? | active |  |  |
| ACNL-F0432 | 整理済みチートの挙動保持リファクタリング（2026-10-11） |  | ? | active |  |  |
| ACNL-F0433 | C++由来107チート本体の局所化と部分集合の実出力照合（2026-10-10） | MEDIUM | ? | active |  |  |
| ACNL-F0434 | チップ長押しのstatic記録拒否と選択アニメ再開始（2026-10-10、MEDIUM） | MEDIUM | A | active |  |  |
| ACNL-F0435 | Editorキャッシュの再記録・チップ複製・内装保存/交換（2026-10-10、MEDIUM、実機未確認） | MEDIUM | A | active |  |  |
| ACNL-F0436 | リスト背景のフェードと模様替えカメラpan（2026-10-10、MEDIUM、本体非表示はF016で訂正） | MEDIUM | A | active |  |  |
| ACNL-F0437 | HHD通常室内カメラの連続操作をACNLの家へ移植（2026-10-09、静的MEDIUM、2026-10-10利用者実機PASS） |  | A | active |  |  |
| ACNL-F0438 | 外観に依存せず室内の壁配置・張替え機能を判定（2026-10-09、静的MEDIUM、2026-10-10利用者実機PASS） |  | A | active |  |  |
| ACNL-F0439 | 下位送信のBusyは未確認フレーム数、F008待機中拒否の再検証（2026-10-04、静的＋利用者実測） |  | ? | active |  |  |
| ACNL-F0440 | 送信者の動作中に下位種別12が拒否される送信ゲート（2026-10-04、静的MEDIUM／回避未検証） |  | ? | active |  |  |
| ACNL-F0441 | 下位種別12の送信APIと2台同時接続時の座標宛先（2026-10-04、静的＋実測） |  | ? | active |  |  |
| ACNL-F0442 | アニメ機構は ModelInstance_Create の引数で作られる（**a5 ではなく a6。IDA-opus-5-F015 で確定**）（2026-09-21、HIGH、実機A/B） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0443 | アニメ本体は g3d の自前クラス。nw::gfx::AnimEvaluator を使うと落ちる（2026-09-21、HIGH、実機・自己訂正） | HIGH | ? | active |  |  |
| ACNL-F0444 | 自前資源のマテリアルアニメを生成し、自前instanceへ結線できた（2026-09-21、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0445 | アニメのフレームは実機で進んだ（適用段は IDA-opus-5-F013 で解決）（2026-09-21、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0446 | アニメの適用段は sub_48A844。画面で動いた（2026-09-21、HIGH、実機） | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0447 | 外部 nw4c ヘッダとの照合。実測は全て一致し、引数の解釈を2点訂正（2026-09-21、HIGH、静的＋実機照合） | HIGH | ? | active |  |  |
| ACNL-F0448 | ModelInstance_Create の a5/a6/a7 を実機で分離（2026-09-21、HIGH、実機A/B/C） | HIGH | ? | active |  |  |
| ACNL-F0449 | アニメが何を動かすかは資源から読める。UnitCursor は色定数2本とUV平行移動（2026-09-21、HIGH、静的） | HIGH | ? | active |  |  |
| ACNL-F0450 | 骨アニメを実機で結線し、骨が動いた（2026-09-21、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0451 | 骨アニメが結線できる条件と、実機に触れずに選んだ資源の組（2026-09-21、HIGH、静的＋実機読み出し） | HIGH | ? | active |  |  |
| ACNL-F0452 | 自前で作ったものを全部解放できた。ヒープは1バイト単位で元に戻る（2026-09-21、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0453 | セッションで作った全部を解放。親ヒープへ 467,056 B が戻った（2026-09-21、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0454 | 場面転換。自前instanceは無傷で残り、ケーブは自分から描画を止める（2026-09-21、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0455 | 描画中に instance を解放しても何も起きない。ただし理由は2つある（2026-09-21、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0456 | 描画中に資源を潰しても落ちない。モデルが黙って消えるだけ（2026-09-21、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0457 | `G3dResHolder_Dtor` はヒープ破棄の**前**に呼ぶこと。逆にすると SIGILL（2026-09-21、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0458 | 模様替えカーソルは大きさを変えていない。V2-F019 の「範囲の形」は誤り（2026-09-21、HIGH、静的） | HIGH | ? | superseded |  |  |
| ACNL-F0459 | 消した・動かした建物の当たり判定が残る理由と、再起動なしで直す 2 関数（2026-09-23、HIGH（静的）） | HIGH | S | active |  |  |
| ACNL-F0460 | ゲーム共通の 8 行リスト InstSelect<8> を下画面だけ借りる部品の作り（2026-09-25、MEDIUM: 静的＋実機の欄の読み取り。描画は未試験） | MEDIUM | S | consolidated | topics/acnl/ui.md |  |
| ACNL-F0461 | 建物の影の表は一覧 0x67CC と同じ番号で並び、場面を作るときにしか作られない（2026-09-25、HIGH: 静的＋実機のクラッシュ時の値） | HIGH | S | active |  |  |
| ACNL-F0462 | アニメ 0x1E1（seo_down1）を途中で切ると縮んだまま残る — 骨 root の拡大を書くアニメがほぼ無い（2026-09-30、MEDIUM: 資源の全数調査＋静的。実機未観測。ゲームの骨格更新が「書かれない骨を戻さない」ことは推定） | MEDIUM | S | active |  |  |
| ACNL-F0463 | ゆうめいなキノコで大きくなる仕組みと、プレイヤーの大きさは通信に乗らないこと（2026-09-30、MEDIUM: 静的＋Vapecord の送信側の形と受信側の独立一致。実機未観測） | MEDIUM | S | active |  |  |
| ACNL-F0464 | 住民の AI（第 2 段まで）— 行動の要求・行動表・外の住民のクラス・家の出入り・花植え・傘（2026-09-29、MEDIUM: 静的＋Vapecord の使い方と一致。実機未観測） | MEDIUM | S | active |  |  |
| ACNL-F0465 | マップエディター第 2 段 — 真ん中のカーソルと A・実行範囲・薄いカーソル（UnitCursor の TEV 段 4 = アルファ × Constant4）（2026-09-29、MEDIUM: 資源の解析＋ホスト試験＋成果物の確認。gohan 実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0466 | メッセージのあと下画面にエディターが出ない — GameList が「隠した」と思い込んだまま、ゲームが戻した下画面をもう一度戻して止まる（2026-09-28、HIGH: 実機の値＋静的＋書き込みでの確認。経緯の一部は未確認） | HIGH | S | active |  |  |
| ACNL-F0467 | マイデザインは村の物体の「層 1 の一覧」で描かれる — F064 の訂正と、カーソルを「マイデザインより上・それ以外より下」にする設計（2026-09-28、MEDIUM: 静的＋実機の結果と整合。設計は未実装） | MEDIUM | S | active |  |  |
| ACNL-F0468 | マップエディターのスポイトモード（一覧 4 行・窓の拡張）、Y、モードごとの UnitCursor の色、下画面左上の箱、マスの色の手直し（2026-09-28、MEDIUM: 静的＋描画器＋ホスト試験。gohan 実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0469 | マップエディターのマスの色 — 上画面の単色の四角形（UnitCursor 資源の別の体）と盤面の 5x5 の輪郭（2026-09-28、MEDIUM: 既存の実機知見の組み合わせ＋描画器。gohan 実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0470 | マップエディターの盤面を 9x9 へ（chip_room_00 の大きさの規則）と、L / R の音（2026-09-28、MEDIUM: 静的＋描画器。gohan 実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0471 | 村の下画面の建物一覧（BsMenuMapList）の作りと、マップエディターのモード一覧への流用（2026-09-28、MEDIUM: 静的＋描画器での照合。gohan 実機未確認） | MEDIUM | S | consolidated | topics/acnl/ui.md |  |
| ACNL-F0472 | UnitCursor を村の物体の下に描く — 地面に張り付く物の材質と、深度書き込みの出どころ（2026-09-28、MEDIUM: 静的のみ。gohan f47f5af、実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0473 | 持ち物の選択窓（ItemSelectWindow）のキー操作 — 十字・A・B の実装（2026-09-28、MEDIUM: 静的のみ。gohan d6b8470 で使用、実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0474 | 1 つの体を行列だけ変えて何か所にも描く（描画ノード FuncNode）（2026-09-28、MEDIUM: 静的のみ。gohan 4fb9e33 で使用、実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0475 | 村の物体の描画の仕組み — 1 体ずつ色を変える入口と、カーソルが消えた原因（2026-09-28、MEDIUM: 静的＋停止中の実機の読み取り。赤の割り込みは実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0476 | モデルの資源の Setup と後片付け — 自前の体を壊すと元の資源の LUT 参照が外れる（2026-09-28、HIGH: 静的＋停止中の実機の読み取り） | HIGH | S | active |  |  |
| ACNL-F0477 | 村の実体の材質は同じモデルで共有、書き換えるとゲームの書き出しが落ちる／参照表の安全条件（2026-09-28、HIGH: 実機のクラッシュと静的） | HIGH | S | active |  |  |
| ACNL-F0478 | 村のアイテムの実体（fgobj）の辿り方とモデルの引き方（2026-09-27、MEDIUM: 静的のみ。gohan 165b571 で使用、実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0479 | 模様替えの音は屋外では鳴らない（GROUP_HOUSE）と、選択窓の決定音が音程を上げる仕組み（2026-09-27、HIGH: 静的＋利用者の実機確認） | HIGH | S | active |  |  |
| ACNL-F0480 | 模様替えの範囲選択・移動の吸着と音、持ち物の選択窓（ItemSelectWindow）の正しい使い方（2026-09-27、MEDIUM: 静的のみ。gohan のマップエディター段階 3 手直しは実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0481 | 持ち物の選択窓（ItemSelectWindow）と模様替えの範囲の枠（CollectChip）の作り（2026-09-27、MEDIUM: 静的のみ。gohan のマップエディター段階 3 は実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0482 | 村のマスにアイテムを置く・消す手順（2026-09-27、MEDIUM: 静的のみ。gohan のマップエディター段階 2 は実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0483 | 模様替え UI（BsMenuInteriorEditor）の作りと、持ち物欄の名前の吹き出し（ItemSelectNameWindow）の使い方（2026-09-27、MEDIUM: 静的のみ（逆アセンブル＋romfs）。実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0484 | アイテムの名前とアイコンの決まり方、没アイテムの割り出し（2026-09-27、MEDIUM: 静的＋ROM の実データ。Ghidra-gpt-sol-5.6-ITEM-T011 と独立一致。gohan の名前差し替えは実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0485 | ゲームの「持ち物に入れる」は 0xFD 以下の ID を写し替え、空に写しても成功を返す／没アイテムを隠す分岐（2026-09-27、MEDIUM: 静的＋利用者の実機報告と整合。修正版は実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0486 | 持ち物へアイテムを入れるゲーム自身の処理と、持ち物画面のアイコンの作り直し（2026-09-26、MEDIUM: 静的＋実機実績のある外部実装と独立一致。gohan の実装は実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0487 | ソフトウェアキーボードのキーの「次の入力までの待ち」の正体（2026-09-26、MEDIUM: 静的のみ（逆アセンブル＋成果物の照合）。実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0488 | キーボードのキーの見た目・テクスチャの取り方・開閉アニメ・切り替え音・カーソル設定の引数（2026-09-26、MEDIUM: 静的＋romfs。実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0489 | 文字の挿入・削除・選択・確定、キーの経路、チャットの送信、入力欄の「未確定」と「選択」の飾り（2026-09-25、MEDIUM: 静的のみ。実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0490 | 文字入力（チャット・手紙・掲示板共通）の sys::TextManager の欄とカーソル・未確定の扱い（2026-09-25、MEDIUM: 静的のみ。実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0491 | 共通ボタン（cmn_btn / btn_pos）・時計とベルの箱（time_bel_win）の組み立てと状態の規則（2026-09-25、HIGH: 静的＋実機画像 2 枚） | HIGH | S | consolidated | topics/acnl/ui.md |  |
| ACNL-F0492 | 一覧の選択中の行とスクロールバー（CommonScrollBar）の見た目の規則（2026-09-25、HIGH: 静的＋実機画像 1 枚との照合） | HIGH | S | consolidated | topics/acnl/ui.md |  |
| ACNL-F0493 | nw::lyt / nw::font の描画規則（ウィンドウ枠・テクスチャ座標・合成・アルファ・文字配置・アニメ曲線）を静的に確定（2026-09-25、HIGH: 静的＋実機画像 1 枚との照合） | HIGH | S | active |  |  |
| ACNL-F0494 | 一覧の切り抜きは N_frame_00 から作るシザー。一覧の Layout は自前のデータで先に組み立てられる（2026-09-25、MEDIUM: 静的＋利用者の見た目の報告。組み立ては実機未確認） | MEDIUM | S | consolidated | topics/acnl/ui.md |  |
| ACNL-F0495 | 一覧の行の文字の TagProcessor は script::RenderMain。タグ 0x0E/0/2 = 大きさ（縦横）、タブは 4 × 文字幅（2026-09-25、MEDIUM: 静的のみ。実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0496 | プラグインから GPU 可視メモリを確保できた＝Luma の svcControlMemoryUnsafe で SYSTEM 領域から空き番地へ貼る（2026-09-25、HIGH: 実機 2 回＋Luma の公式ソース） | HIGH | S | active |  |  |
| ACNL-F0497 | ゲームの SVC は 32 種類・745 か所（2026-09-25、HIGH: 命令語＋逆アセンブル、名前は libctru と 3dbrew の 2 資料で一致） | HIGH | S | active |  |  |
| ACNL-F0498 | 複製の光＝BsLightMgr の組のフラグメント方向光・アンビエント・半球。向きはゲームのカメラの view で変換されるので専用カメラと食い違う。描く間だけ自前の組に差し替える（2026-09-24、MEDIUM（静的＋実機の読み取り）。gohan の直しは実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0499 | 画面固定の複製でズボンが止まる＝部品のスキニング行列は Scene の更新が計算する。光はフラグメントライティングではない（★光の部分は F033 で訂正：読んだ組が違った）（2026-09-24、MEDIUM（実機の読み取り＋静的）。gohan 8908f5d は実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0500 | 複製を画面に固定する方式＝再生直後の late pass で専用カメラ。Scene 1 に積む案は右目が壊れるので不可（2026-09-24、MEDIUM（静的＋別エージェントの実機成功の手順）。gohan 246865a は実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0501 | 複製を出したまま建物に入ると無限ロード＝管理役が枠の返却を待つ。枠は BankTable_Release で下ろしてから返す（2026-09-24、HIGH（静的＋実機 2 回）。直した gohan 0107a5b は利用者が実機で確認: 出したまま建物に出入りしても止まらない、入ったあと複製は消える、OFF→ON で問題なく再出現） | HIGH | S | active |  |  |
| ACNL-F0502 | 髪は毎フレームの部品更新が pm+548 から読む。複製は本物のプロフィールで作り pm+548/+552 を書くだけでよい（F028 の一部訂正）（2026-09-24、MEDIUM（静的。複製での実機確認は未実施）） | MEDIUM | S | active |  |  |
| ACNL-F0503 | PlayerModel と部品バンク。複製はゲーム自身の作成・片付け関数と「プロフィールの写し」で作れる（2026-09-24、HIGH（静的＋実機 BP・実機の読み取り）。複製の作成は未実施） | HIGH | S | active |  |  |
| ACNL-F0504 | 橋の高さは村の中で一定＝「村の川底で一番多い段 + flt_6DE560」（2026-09-24、HIGH（静的＋実機の地形全体・実物の橋 y と一致＋利用者の実機確認）。gohan 1754f62 は利用者が実機で確認: 橋を出しているとき、どこにカーソルがあっても UnitCursor とカメラは同じ高さ） | HIGH | S | active |  |  |
| ACNL-F0505 | 橋のカーソルの高さの出どころ（川の判定・ゲームの橋の置き方・岸の高さ）（2026-09-24、HIGH（川の判定: 静的＋実機の地形）／MEDIUM（岸＝最寄りの陸）。gohan へは未実装） | HIGH | S | active |  |  |
| ACNL-F0506 | 地形のマス情報は 10 バイト（角の高さ 4 個＋属性）で、足元データと同じ形／橋の四角の外周は必ず端のマス（2026-09-24、MEDIUM（静的＋romfs 全 24 本）。実機の見た目は未確認） | MEDIUM | S | active |  |  |
| ACNL-F0507 | 橋のモデル行列は平行移動 (x, 0, 0) ＋曲面の回転だけ（地面の高さを使わない）（2026-09-24、HIGH） | HIGH | S | active |  |  |
| ACNL-F0508 | 半透明は描画層で後ろへ回し深度は書く／役場の旗とチケットマシン／もとから半透明の材質のアルファ／一枚絵の合成の調査（2026-09-24、HIGH（実機の比較画像）／MEDIUM（一枚絵は設計のみ）） | HIGH | S | active |  |  |
| ACNL-F0509 | 更新データの RomFS は ARCHIVE_ROMFS をファイルパス {5,0,0} で開く（ゲーム自身の開き方）（2026-09-24、MEDIUM（静的＋実機で失敗の側を確認）） | MEDIUM | S | active |  |  |
| ACNL-F0510 | 家の足元は名前表に無い → ゲームが読み込み済みの足元を使う／0x05 は属性を書き換えない（F019・F020 の訂正）（2026-09-24、HIGH（実機の占有＋静的）） | HIGH | S | active |  |  |
| ACNL-F0511 | 建物の衝突判定 = 花を植えられない属性（byte_957A35 == 0）。利用者の正解と一致／プレビューが作れないのは親ヒープの断片化（2026-09-24、HIGH（利用者の正解と静的な表の一致）／HIGH（実機の読み取り）） | HIGH | S | active |  |  |
| ACNL-F0512 | 物を置ける／花を植えられる属性の表と、それで決める建物の衝突判定（2026-09-24、MEDIUM（静的）。定義は利用者） | MEDIUM | S | active |  |  |
| ACNL-F0513 | 親ヒープ *(0x94CC48) の空きは 484 KB。UnitCursor とプレビューを並べると足りない／駅・役場のプレビュー名（2026-09-24、HIGH（実機の読み取り）／MEDIUM（名前、静的）） | HIGH | S | active |  |  |
| ACNL-F0514 | 衝突判定（歩けないマス）= 足元の属性コードをゲームの分類表 byte_957B34 で引いて 0 でないマス／プレビューの無限ロードとクラッシュの原因（2026-09-24、MEDIUM（静的＋利用者の説明と一致。実機の歩行では未確認）） | MEDIUM | S | active |  |  |
| ACNL-F0515 | 設置プレビューはゲーム自身の公共事業プレビューと同じ 3 資源で組める／衝突判定の「一回り小さい」形（2026-09-23、MEDIUM（静的。実機未確認）） | MEDIUM | S | active |  |  |
| ACNL-F0516 | 建物エディターの下調べ — カメラ・プレイヤーの停止・占有マップ・足元の読み方（2026-09-23、MEDIUM（静的。実機未確認）） | MEDIUM | S | active |  |  |
| ACNL-F0517 | 選んだ建物の青＋透明度の揺れ（gohan BuildingHighlight）が実機で動いた（2026-09-23、HIGH） | HIGH | S | active |  |  |
| ACNL-F0518 | 役場・リサイクルショップも集め方どおり全体が青。全段使用の材質は近似、モデルビューアは汎用の書き出し（2026-09-23、HIGH（役場・店）／MEDIUM（モデルビューア、静的）） | HIGH | S | active |  |  |
| ACNL-F0519 | 建物ごとのモデルはゲームのデータから集められる。写しの置き場は gohan 自身のメモリでよい（2026-09-23、HIGH（静的＋実機）） | HIGH | S | active |  |  |
| ACNL-F0520 | 灯り・プレイヤーの家（テント本体・柵・ポスト）まで全部を薄い青にできた。環境光に関係なく同じ明るさ（2026-09-23、HIGH（静的＋実機で表示確認）） | HIGH | S | active |  |  |
| ACNL-F0521 | モデル単位の色ハイライトは「TEV の空き最終段で定数色と混ぜる」でできる（2026-09-23、**HIGH（静的＋実機で表示確認）**。材質 1 つで確認） | HIGH | S | active |  |  |
| ACNL-F0522 | 読み直しへ逃がしても必要量は同じ。ゲームでも落ちる状態は置く前に断る。地図は星アイコンまでゲームと同じに（2026-09-23、**HIGH（静的＋実機）**） | HIGH | S | active |  |  |
| ACNL-F0523 | 建物の資源は 2 系統。共有 64 枠（公共事業など 7 クラス、1 種類 2 枠）と、役場・店の専用ヒープ（2026-09-23、HIGH（静的＋実機）） | HIGH | S | active |  |  |
| ACNL-F0524 | その場で作った建物は資源の枠を部屋が片付くまで返さない。尽きると読み込みスレッドが落ちる（2026-09-23、MEDIUM（静的＋実機のクラッシュダンプ）） | MEDIUM | S | active |  |  |
| ACNL-F0525 | 地図のアイコン枠は数を見ずに割り当てられ、溢れると星アイコン・柵の消滅・クラッシュになる（2026-09-23、HIGH（静的＋実機のクラッシュダンプ）） | HIGH | S | active |  |  |
| ACNL-F0526 | 足元のアイテムは Field_MarkDirty で、下画面の地図は作成段 9 の呼び直しで更新できる（2026-09-23、**HIGH（静的＋実機）**） | HIGH | S | consolidated | topics/acnl/ui.md |  |
| ACNL-F0527 | 村の建物の実体は BsStrcMgr が作る。1 件分を写せば読み直さずに出せる（2026-09-23、**HIGH（静的＋実機）**） | HIGH | S | active |  |  |
| ACNL-F0528 | 建物の高さは属性ブロックから。カタログ表示の読み込み手順（2026-09-23、MEDIUM（静的）） | MEDIUM | S | active |  |  |
| ACNL-F0529 | 公共事業は ID → 名前 1 つでモデルと足元が引ける。設置関数は見た目を作らない（2026-09-23、静的） | HIGH | S | active |  |  |
| ACNL-F0530 | 更新タイトルの RomFS は開けなかった（2026-09-22、HIGH（事実）、原因は未解明） | HIGH | ? | active |  |  |
| ACNL-F0531 | `ARCHIVE_ROMFS` が返すのは **base だけ**。8,629 本（2026-09-22、HIGH、実機計測） | HIGH | ? | active |  |  |
| ACNL-F0532 | RomFS の開き方を 3 箱所間違えていた（2026-09-22、HIGH、実機＋libctru ソース） | HIGH | ? | active |  |  |
| ACNL-F0533 | モデルの一覧は ROM から読める。8,818 本の .bcres とその検算（2026-09-22、HIGH、静的） | HIGH | ? | active |  |  |
| ACNL-F0534 | マス数変更中のクラッシュと、縞模様の 45 度（2026-09-22、HIGH、クラッシュダンプ＋静的） | HIGH | ? | active |  |  |
| ACNL-F0535 | 村の 1 マス = world 32 単位。UnitCursor の原点は quad の中心（2026-09-22、HIGH、実機＋CGFX） | HIGH | ? | active |  |  |
| ACNL-F0536 | グリッドカーソルが村の屋外で描けた。見えたものから分かったこと（2026-09-22、実機目視） | HIGH | ? | active |  |  |
| ACNL-F0537 | gohan のグリッドカーソルが何も描かなかった2つの原因（2026-09-22、HIGH、実機の状態読み＋静的） | HIGH | ? | active |  |  |
| ACNL-F0538 | グリッドカーソルを gohan へ。起動時クラッシュの診断とケーブ衝突（2026-09-22、HIGH、静的＋クラッシュダンプ） | HIGH | ? | active |  |  |
| ACNL-F0539 | 姿勢を直接書くだけでは描かれない。骨格の更新が要る（2026-09-21、HIGH、実機。**F017 の訂正**） | HIGH | ? | active |  |  |
| ACNL-F0540 | park の BP は焼き付かない。直前に外した番地だけが一時的に拒む（2026-09-21、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0541 | 同じモデル・アニメ12体の同時描画。実機で30.67fpsを維持し、submit先は溢れない（2026-09-21、HIGH、静的＋実機） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0542 | 骨・アニメの構造。node+0x228 は AnimGroup で、F029 の2語の正体（2026-09-21、HIGH、静的＋実機） | HIGH | ? | active |  |  |
| ACNL-F0543 | SkeletalModelも描けた。node+0x228/+0x22C は不可視の原因ではない（2026-09-21、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0544 | 親ヒープの残りは実測できる。確保量は35倍過大だった（2026-09-21、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0545 | park 用の BP は `0x1B721C` では張れなくなる。`0x1B7220` が同値（2026-09-21、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0546 | 任意bcresの読み込み→ワールド描画が実機で成立（2026-09-20、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0547 | モデルのクラスは資源が決める。ゲーム内のCMDLは2種類しかない（2026-09-20、MEDIUM、静的） | MEDIUM | ? | active |  |  |
| ACNL-F0548 | 屋外座標の曲面変換は部屋フラグで切り替わる。165部屋中37部屋（2026-09-20、HIGH、静的＋実機） | HIGH | ? | active |  |  |
| ACNL-F0549 | 不可視だった UnitCursor は生のゲーム座標に置かれていた（2026-09-20、HIGH、静的＋実機、自己訂正） | HIGH | ? | active |  |  |
| ACNL-F0550 | 木1体の専用材質で透明度変更（2026-09-20、HIGH） | HIGH | ? | active |  |  |
| ACNL-F0551 | 専用view/projectionで画面固定、pixel配置・倍率・alpha併用（2026-09-20、HIGH） | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0552 | 独立した木を表示・非表示。ゲーム座標には曲面変換が必要（2026-09-20、HIGH） | HIGH | ? | active |  |  |
| ACNL-F0553 | 行列経路は正常だった。残る差は node+0x228 / +0x22C（2026-09-19、HIGH、実機＋対照） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0554 | 実機測定で IDA-unknown-F027 を棄却。頂点バッファの束縛は正しい（2026-09-18、HIGH、実機） | HIGH | ? | active |  |  |
| ACNL-F0555 | 頂点バッファの番地は VA→GPU 変換を通り、対応外の領域では黙って 0 になる（2026-09-18、HIGH、静的） | HIGH | ? | superseded |  |  |
| ACNL-F0556 | メッシュのコマンド列は誰が作るか。「ジオメトリが欠けている」仮説の反証（2026-09-18、HIGH、静的） | HIGH | ? | active |  |  |
| ACNL-F0557 | 過去の静的解析の誤り 2 件と見落とし 1 件（2026-09-18、HIGH） | HIGH | ? | active |  | 訂正あり |
| ACNL-F0558 | 描画順は静的に確定できる。描画状態は bcres の PICA コマンド列にある（2026-09-18、MEDIUM） | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0559 | 屋外表示の未解明点のうち4件を解決（ホルダ型・Create引数・マス換算・フック候補）（2026-09-18、MEDIUM） | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0560 | Scene_SubmitNode のシーン番号は 0=通常描画・1=別モード・2=影マップ（2026-09-18、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0561 | UnitCursor を屋外で出すための足場と不足（2026-09-18、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0562 | 家具モデルは屋外でも出る（部屋ごとの収容数）。UnitCursor だけが屋内限定（2026-09-18、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0563 | 模様替えの家具の下の範囲表示は UnitCursor モデル、屋外では資源もクラスも無い（2026-09-18、MEDIUM） | MEDIUM | ? | superseded |  | 訂正あり |
| ACNL-F0564 | 手紙の ID 種別 3=名前差し込み無しのプレイヤー・4=同住民・6=自分自身（2026-09-18、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0565 | 郵便ポストの手紙は「通信相手から」を判定できる／sub_6070CC・sub_606964 はデバッグ判定（2026-09-18、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0566 | sub_5C9C24 は夢見の館で落とした町を読み込んだ直後の作り直し（2026-09-18、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0567 | 日替わり処理の成長・郵便・「アイテム消えない」の中身（2026-09-18、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0568 | 準備中の日替わり処理に掲示板・雑草・住民の引っ越しがある（2026-09-17、MEDIUM＋実機傍証） | MEDIUM | ? | active |  |  |
| ACNL-F0569 | しずえ画面「準備中」の仕事はSvProc種別4、中で日替わり処理と寝癖（2026-09-17、HIGH） | HIGH | ? | consolidated | topics/acnl/ui.md |  |
| ACNL-F0570 | 店の営業時間判定は店・用途ごとに複製、共通の入口なし（2026-09-17、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0571 | 木と家具の共通モデル生成・姿勢設定（2026-09-14、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0572 | 木の実体とSeason資源を原本照合（2026-09-17、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0573 | Create全引数・instance共有範囲・更新/破棄（2026-09-17、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0574 | サイズqueryとOOM・ready・owner寿命（2026-09-17、MEDIUM） | MEDIUM | ? | active |  | 訂正あり |
| ACNL-F0575 | resource描画属性・scene番号・画面を区別（2026-09-14、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0576 | 正常版と統合版の区別 |  | ? | active |  |  |
| ACNL-F0577 | 旧プロジェクトの内部保存 |  | ? | active |  |  |
| ACNL-F0578 | 自立化後の検証 |  | ? | active |  |  |
| ACNL-F0579 | gohan-gui-simulator のローカル版と公開版が双方向に食い違っていた（解消済み） |  | ? | active |  |  |
| ACNL-F0580 | Volta の shim が引数を改行で切り落とす（このPC全体の問題） |  | ? | active |  |  |
| ACNL-F0581 | IDA9.3のGhidra XML Exporter導入・主IDB出力 |  | ? | active |  |  |
| ACNL-F0582 | 通信パケット種別番号 `0x00`～`0x84` の受信表（2026-10-03、MEDIUM/一部LOW） | MEDIUM | ? | active |  |  |
| ACNL-F0583 | 通信中の村データ転送と屋外再読み込みは別経路（2026-10-03、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0584 | 下位種別12の受信に町サイズ上限がない（2026-10-04、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0585 | Pretendoの公表したACNL RCE対策は `0x81` 掲示板パケット（2026-10-04、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0586 | 下位 `0x0C` でgohanの壁抜けを相手へ強制できるか（2026-10-04、MEDIUM） | MEDIUM | ? | active |  |  |
| ACNL-F0587 | 屋外XYZを下位 `0x0C` で書くための条件と副作用（2026-10-04、静的MEDIUM／実用性LOW） |  | ? | active |  |  |
| ACNL-F0588 | nw::lyt の Window は 1 枠でも描ける（2026-10-05、MEDIUM: 静的 + designer の再現がスクショと一致） | MEDIUM | S | consolidated | topics/acnl/ui.md |  |
| ACNL-F0589 | 自前の DARC をメモリから渡して下画面にレイアウトを出せる（2026-10-05、HIGH: 静的 + 実機） | HIGH | S | consolidated | topics/acnl/ui.md |  |
| ACNL-F0590 | HHD の顔の画面が ACNL の下画面の最前面に予想どおり出る・必要なメモリ（2026-10-05、HIGH: 実機の画面と designer の予想の照合 + 実機のメモリ） | HIGH | S | active |  |  |
| ACNL-F0591 | ウィンドウの中身にテクスチャがあるなら UV の組が要る（無いと nwlyt_CalcTexCoordsForGpu が落ちる）（2026-10-05、HIGH: 実機のクラッシュ + 静的） | HIGH | S | active |  |  |
| ACNL-F0592 | 実行時のテクスチャ差し替えと性別の読み方を実機で確認（2026-10-05、HIGH: 静的 + 実機） | HIGH | S | active |  |  |
| ACNL-F0593 | カタログを開くときの遷移は BsMenuBg の切り替え（クロスフェード）と画面自身の in アニメ。Fade / Wipe / Fader は使わない（2026-10-05、HIGH: 静的 + 実機の否定観測） | HIGH | S | consolidated | topics/acnl/ui.md |  |
| ACNL-F0594 | HHD の「ペインに投影」の座標生成を ACNL の UV で再現する規則（HHD-T006 の水玉の謎の答え）（2026-10-05、MEDIUM: レイアウトのデータ 2 種と HHD のスクショの照合。HHD のコードは未読） | MEDIUM | S | consolidated | topics/acnl/ui.md |  |
| ACNL-F0595 | HHD の BFLAN を ACNL の BCLAN に変換できる（書き出しは ACNL の実物 727 本でバイト一致）・不透明度の伝播の旗（2026-10-05、HIGH: 実物との照合） | HIGH | S | active |  |  |
| ACNL-F0596 | ACNL の見た目の記録と色の表。HHD の番号がそのまま使える（2026-10-05、MEDIUM〜HIGH: 静的 2 経路（命令の復元と HHD のデータ）の一致。実機での反映は未） | MEDIUM | S | active |  |  |
| ACNL-F0597 | HHD のキャラクリ画面から ACNL のプレイヤーの見た目を変えられる（実機 全 PASS）（2026-10-05、HIGH: 静的 F080 + 実機） | HIGH | S | active |  |  |
| ACNL-F0598 | レイアウトの材質の TEV の段と座標生成の意味（2026-10-05、HIGH 相当: 逆アセンブル + ACNL の実在の材質 215 個と照合。実機の描画は未確認） | HIGH | S | active |  |  |
| ACNL-F0599 | 上画面の描画順と「メニューの 3D」モード（Scene 1）、美容室の小物の音、複製の帽子・肌の欄（2026-10-05、MEDIUM: 静的のみ。gohan での使用は実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0600 | 部屋の内部名の表、メッシュ 1 つを半透明で描く命令の挟み方、T018 第 1 段の実機（2026-10-05、HIGH（部屋の表: ID 一覧とゲームの表の 2 経路）/ MEDIUM（半透明: 静的、実機未確認）） | HIGH | S | active |  |  |
| ACNL-F0601 | 目の色は頭のキー、目の形は作るときだけ — 複製の目をすぐ反映する方法（2026-10-05、MEDIUM: 静的のみ。gohan は実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0602 | プレイヤー本人の目の形をその場で変える手順・レイアウトの色の 1 要素の読み書き・書体の私用領域の記号（2026-10-06、MEDIUM: 静的のみ。gohan は実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0603 | オンラインで見た目を伝える経路 — 美容室状態 0xB9 と状態 0 の抜け、プロフィール丸ごとの転送（2026-10-06、MEDIUM: 静的のみ。実機・通信未検証） | MEDIUM | S | active |  |  |
| ACNL-F0604 | 相手側のアクセサリーを残す状態 0xBA、送れなかった件（2026-10-06、MEDIUM: 静的のみ。gohan 未実機） | MEDIUM | S | active |  |  |
| ACNL-F0605 | 目の形を通信相手へ伝える経路の調査（T020、2026-10-06、MEDIUM: 静的のみ。実装・実機なし） | MEDIUM | S | active |  |  |
| ACNL-F0606 | 目の形を種別 11 で送る実装（T020、2026-10-06、MEDIUM: 静的のみ。gohan e85bac0 未実機） | MEDIUM | S | active |  |  |
| ACNL-F0607 | 0xAA7994 はホストの枠 — 自分のプレイヤーは [自分の通信番号]（2026-10-06、HIGH: 静的（vc_PLAYERINSTANCE の索引）＋実機の症状が一致） | HIGH | S | active |  |  |
| ACNL-F0608 | 訪問者のプロフィールは固定領域にある（2026-10-06、HIGH: 静的 + 実機の症状が一致） | HIGH | S | active |  |  |
| ACNL-F0609 | gohan の他機能の「自分のプレイヤー」— 問題が出た所と出なかった所の理由（2026-10-06、MEDIUM: 静的 + 利用者の実機の結果） | MEDIUM | S | active |  |  |
| ACNL-F0610 | gohan のリソースを sdmc:/gohan に（2026-10-06、設計 + 静的検査。実機未確認） |  | S | active |  |  |
| ACNL-F0611 | Layout ノード 1 つにつき 1 枚のシザー（自前の候補欄の切り抜きに使う）（2026-10-06、HIGH: 静的 + 実機。縦の向きは実機で訂正） | HIGH | S | consolidated | topics/acnl/ui.md |  |
| ACNL-F0612 | ゲームのフォント（Garden_msg_size16）で描けない文字 = 代わりの字形 0xE03A（2026-10-06、MEDIUM: 実機の写し + 元の ARM との照合。候補の除外は実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0613 | 建物プレビューのファイル読み込みは既にゲームの読み込み係のスレッドで非同期（2026-10-06、MEDIUM: 静的） | MEDIUM | S | active |  |  |
| ACNL-F0614 | 公共事業エディターのプレビュー切り替えの実測（2026-10-06、HIGH: 実機の計測。gohan work/preview-probe 1836acd） | HIGH | S | active |  |  |
| ACNL-F0615 | ゲームのカタログのプレビューは 2 枠を交互に使い、替えた前の枠は 1 フレーム後にすぐ壊す（2026-10-06、MEDIUM: 静的） | MEDIUM | S | active |  |  |
| ACNL-F0616 | 待ちを外したプレビューの実測と、HHD が開かなくなった原因（2026-10-06、HIGH: 実機の計測と実機の変数） | HIGH | S | active |  |  |
| ACNL-F0617 | ACNL の品番 → モデル名の表と、HHD との品物の突き合わせ（2026-10-06、MEDIUM〜HIGH: 静的 2 本 + ROM の実データ） | MEDIUM | S | active |  |  |
| ACNL-F0618 | ACNL の部屋の家具の持ち方と「かざる」「拾う」の入口（2026-10-06、LOW〜MEDIUM: 静的 + 先行資料。途中） | LOW | S | active |  |  |
| ACNL-F0619 | ACNL の「かざる」の部品と、データだけ書いたときの振る舞い（2026-10-06、静的 + 実機 2 回。置く部品は実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0620 | 家具をその場で消すゲーム自身の手順（2026-10-06、MEDIUM: 静的。実機は試験 4 待ち） | MEDIUM | S | active |  |  |
| ACNL-F0621 | 模様替え UI のドラッグ・離す・チップと家具の記録の関係（2026-10-07、MEDIUM: 静的のみ。ModuleIndoor.elf / ModuleFtr.elf と主 IDB） | MEDIUM | S | active |  | 訂正あり |
| ACNL-F0622 | 家の部屋の壁紙・床をその場で替えるゲーム自身の手順（2026-10-07、MEDIUM: 静的 2 経路。実機未確認） | MEDIUM | S | active |  |  |
| ACNL-F0623 | 模様替え UI を開いたまま家具を出す材料（2026-10-07、MEDIUM: 静的のみ。途中で打ち切り） | MEDIUM | A | active |  |  |
| ACNL-F0624 | HHD と ACNL の品の名前での突き合わせと、ACNL の Item.bin のカテゴリ（2026-10-07、MEDIUM: 静的 + ROM の実データ） | MEDIUM | S | active |  |  |
| ACNL-F0625 | 模様替え UI を開いたまま家具を出す手順の詰め（2026-10-07、MEDIUM: 静的のみ。利用者の 5 時間枠で打ち切り） | MEDIUM | A | active |  |  |
| ACNL-F0626 | T022 カタログの生成器（Codex 依頼 t022_catalog_arc、gpt-6.1-sol xhigh、2026-10-07。打ち切り。記録 ID なし = 道具と生成物） |  | ? | active |  |  |
| ACNL-F0627 | 服・ワンピース・K.K. の曲を部屋に置くときの品番（2026-10-07、MEDIUM: 静的 2 経路） | MEDIUM | A | active |  |  |
| ACNL-F0628 | HHD と ACNL でアニメのコマ数の数え方が 1 つ違う（2026-10-07、HIGH: 静的＋実機の症状） | HIGH | S | consolidated | topics/acnl/ui.md |  |
| ACNL-F0629 | T022 の窓が開かないのは読み込みのヒープ不足（2026-10-08、HIGH: 実機の値＋静的） | HIGH | S | active |  |  |
| ACNL-F0630 | T022 カタログの実機不具合 8 件の原因と修正（2026-10-08、MEDIUM: 静的。実機未確認） | MEDIUM | A | active |  |  |
| ACNL-F0631 | 家具が置けない・壁紙が張り替わらない原因（2026-10-08、HIGH: 実機 BP＋静的） | HIGH | A | active |  |  |
| ACNL-F0632 | 足したチップが動かない・2 回目の窓のヒープ不足・テントでの壁紙/床タブ（2026-10-08、MEDIUM: 静的。実機未確認） | MEDIUM | A | active |  |  |
| ACNL-F0633 | 改造テントの壁紙/床・自由スクロール・すぐ開く・すぐチップ・位置保持（2026-10-08、MEDIUM: 静的。実機未確認） | MEDIUM | A | active |  | 訂正あり |
| ACNL-F0634 | しばらく使うとフリーズする原因 — 読み込みのヒープの枯渇（2026-10-08、実測 + 静的: MEDIUM） | MEDIUM | A | active |  |  |
| ACNL-F0635 | 窓が読み込みヒープを食う最大の原因は非表示 TextBox の描画用バッファ（2026-10-09、MEDIUM: 静的。実機未確認） | MEDIUM | A | active |  |  |
| ACNL-F0636 | 窓を開けなくなる原因 — 余白の基準（連続空き）が現実の割れ方と合っていなかった（2026-10-09、実測 HIGH + 静的 MEDIUM） | HIGH | A | active |  |  |
| ACNL-F0637 | 家具のチップと窓が読み込みヒープを共有する問題 — 基準の見直しと、アイコン枠を描画命令用ヒープへ（2026-10-09、実測 + 静的 MEDIUM、実機未確認） | MEDIUM | A | active |  |  |
| ACNL-F0638 | HHD の「壁にかける家具」リストの移植（2026-10-09、静的 MEDIUM、実機未確認） | MEDIUM | A | active |  |  |
| ACNL-F0639 | 村を通過する電車は位置状態を持つ `AcStrcTrain` オブジェクトである | MEDIUM | B | active |  |  |
| ACNL-F0640 | パチンコ弾はPlayer内の固定3スロットで管理される | MEDIUM | B | active |  |  |
| ACNL-F0641 | 村の風船は `AcBalloon` Actorで、生成・破裂・プレゼント配置を既存経路から制御できる | HIGH | B | active |  |  |
| ACNL-F0642 | 通常ドロップをAcBalloon経由へ置換するAR実装 | MEDIUM | B | active |  | 訂正あり |
| ACNL-F0643 | crash_dump_00000005 の直接fault | HIGH | B | active |  | 訂正あり |
| ACNL-F0644 | crash_dump_00000006 の直接fault | HIGH | B | active |  |  |
| ACNL-F0645 | balloon ARの旧code caveが既存描画caveと衝突していた | HIGH | B | active |  |  |
| ACNL-F0646 | カスタム風船drop中にinventory Player stateが0x16→0x06へ遷移する | HIGH | B | active |  |  |
| ACNL-F0647 | 持ち物画面はBsMenuItem UI stateとPlayer state 0x16の二重state machineで成立する | HIGH | B | active |  |  |
| ACNL-F0648 | inventory drop完了はFieldAction handleのstatus 2待ちで成立する | HIGH | B | active |  |  |
| ACNL-F0649 | type 0x10 completion token案は実機クラッシュで棄却 | HIGH | B | active |  |  |
| ACNL-F0650 | synthetic completion handleでinventory完了契約だけをエミュレートする | MEDIUM | B | active |  |  |
| ACNL-F0651 | custom balloon drop中のinventory state 0x16→0x06をmenu-open guardで抑止する | MEDIUM | B | active |  | 訂正あり |
| ACNL-F0652 | 0x838080 dead-cave再利用は実機runtimeと衝突する | HIGH | B | active |  |  |
| ACNL-F0653 | Ghidra-gpt-sol-5.6-F013 guardは遅すぎた — ActorFactory前にarmする必要がある | HIGH | B | active |  |  |
| ACNL-F0654 | custom guard依存を廃止し、menu-open中の0x16→0x06を直接抑止する | MEDIUM | B | active |  |  |
| ACNL-F0655 | Ghidra-gpt-sol-5.6-F016 AR先頭E blockの最終行が1word欠けていた | HIGH | B | active |  |  |
| ACNL-F0656 | stock inventory dropはPlayer stateを変更しない。state 0x16はmenu open時に明示設定される | HIGH | B | active |  |  |
| ACNL-F0657 | menu-open中にstate 0x16から離れる最初のActor_SetStateを記録する診断AR | HIGH | B | superseded |  |  |
| ACNL-F0658 | shared page書込み可否とActor_SetState hook到達を分離診断 | HIGH | B | superseded |  |  |
| ACNL-F0659 | trace領域をARで0固定していたためGhidra-gpt-sol-5.6-F019/Ghidra-gpt-sol-5.6-F020 traceは観測不能だった | HIGH | B | active |  |  |
| ACNL-F0660 | AcBalloon terminal dropがPlayer state 0xA4 reactionを明示要求し、desired=0x06へ戻る | HIGH | B | active |  |  |
| ACNL-F0661 | Ghidra-gpt-sol-5.6-F022後に残るdirect 0x16→0x06を観測する | HIGH | B | active |  |  |
| ACNL-F0662 | Actor_SetState無条件hit + state 0x16 first-departure trace |  | B | active |  |  |
| ACNL-F0663 | custom AcBalloon* identityでterminal A4だけ抑止 |  | B | active |  | 訂正あり |
| ACNL-F0664 | actor identity guard keeps inventory Player state 0x16 |  | B | active |  |  |
| ACNL-F0665 | terminal landingをcustom AcBalloon identityで識別し、元Inventory Itemをpayloadにする |  | B | active |  |  |
| ACNL-F0666 | landing identityをstate helper内でpre-arm |  | B | active |  | 訂正あり |
| ACNL-F0667 | custom Item substitutionをstock landing persistence経路へ戻す |  | B | superseded |  |  |
| ACNL-F0668 | direct falling visualを維持し、impact時だけground itemを確定 |  | B | active |  | 訂正あり |
| ACNL-F0669 | action 0x12誤用を撤回し、stock action 0x0Aでimpact定着 |  | B | active |  |  |
| ACNL-F0670 | Player-origin updaterを外し、balloon impact位置からpersistent ground objectを生成 |  | B | active |  | 訂正あり |
| ACNL-F0671 | 0x0A visual生成を外し、stock post-visual field commitだけ再利用 |  | B | active |  |  |
| ACNL-F0672 | custom falling objectをbusy tokenにしてdrop queueをlock |  | B | active |  | 訂正あり |
| ACNL-F0673 | dit (post Ghidra-gpt-sol-5.6-F032) |  | B | active |  |  |
| ACNL-F0674 | native DropData queue integration |  | B | superseded |  |  |
| ACNL-F0675 | stock inventory-call signature for native queue interception |  | B | superseded |  |  |
| ACNL-F0676 | native DropData allocation from the Ghidra-gpt-sol-5.6-F032 callsite context |  | B | superseded |  |  |
| ACNL-F0677 | Ghidra-gpt-sol-5.6-F036 crash-dump root cause and ABI-safe bridge |  | B | superseded |  |  |
| ACNL-F0678 | e-analysis after Ghidra-gpt-sol-5.6-F037 |  | B | active |  |  |
| ACNL-F0679 | inventory completionはnative DropDataではなく非同期synthetic handle 4で十分 | HIGH | B | active |  |  |
| ACNL-F0680 | 二系統の独立再解析は主要結論で一致し、旧timing説明だけが矛盾していた | HIGH | B | active |  |  |
| ACNL-F0681 | remote chat Size/Color tags survive transport and render | HIGH | B | superseded |  |  |
| ACNL-F0682 | local/self and inline tag scope | HIGH | B | active |  |  |
| ACNL-F0683 | 0x958108 is pointer storage |  | B | active |  |  |
| ACNL-F0684 | direct 0x958108-pointee test negative; parse is still post-submit |  | B | active |  |  |
| ACNL-F0685 | normal chat strips embedded tags |  | B | active |  |  |
| ACNL-F0686 | mode1 sender bypass preserves tags on hardware |  | B | active |  |  |
| ACNL-F0687 | sender local Color render hardware success |  | B | active |  |  |
| ACNL-F0688 | player/town name tag sanitizer |  | B | active |  |  |
| ACNL-F0689 | dedicated ruby font |  | B | active |  |  |
| ACNL-F0690 | item name/icon resource pipeline |  | B | active |  |  |
| ACNL-F0691 | low field-object display fallback |  | B | active |  |  |
| ACNL-F0692 | AcObjUnitCursor の尺度は家具サイズ、Rotate アニメは UV 回転で決まる（F0563 再解析） | MEDIUM | A | active |  |  |
| ACNL-F0693 | Layout 描画は上左右目と下の三パスで、上下の二リストを使う（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0694 | Layout の優先度は安定な昇順挿入であり、末尾は登録時点に依存する（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0695 | Layout 再生時の主リスト記帳は条件付きで未提出範囲を取り込む（再解析） | MEDIUM | A | active |  |  |
| ACNL-F0696 | Layout の正射影とペインから画素への換算は Layout 寸法と viewport の比で決まる（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0697 | Layout 再生の通常シザーは mode 0 であり寸法不一致だけでは切り抜きを有効にしない（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0698 | Layout 投影 uniform の c4 は毎再生前に設定され初期化後のゼロ固定ではない（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0699 | Layout の記録要求と保存範囲の再利用（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0700 | Layout と記録 ID の生成・解放・再利用および ID 0（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0701 | 記録 manager の容量・保存 offset と live cursor は異なる（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0702 | Fade とロード画像の登録順・状態別の描画元（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0703 | loader ID の十進10と0x10は異なり、旧bucket照合は0x0Aを指す（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0704 | Fade の記録保持とゼロ長Layoutから画像源を判定する限界（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0705 | Picture・Material の別確保と可変長ブロックの実配置（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0706 | TexMap のレジスタ派生値と Picture の UV キャッシュ（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0707 | Pane 木の可視走査と Layout 記録・Picture 描画（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0708 | Picture の材質共有は無効化・所有と資源寿命の条件を持つ（再解析） | MEDIUM | A | consolidated | topics/acnl/ui.md |  |
| ACNL-F0709 | GPU コマンドリストの生成・領域確保・削除と引数型 | MEDIUM | A | active |  |  |
| ACNL-F0710 | Pane・Picture・Material の描画用構造と vtable 型 | MEDIUM | A | active |  |  |
| ACNL-F0711 | TextBox と ResFont の文字描画用構造および既定 TagProcessor | MEDIUM | A | active |  |  |
| ACNL-F0712 | DrawInfo・Layout ノード・LayoutMgr の描画用構造 | MEDIUM | A | active |  |  |
| ACNL-F0713 | Layout アロケータと ExpHeap の空きリスト構造 | MEDIUM | A | active |  |  |
| ACNL-F0714 | Layoutの仮想関数型と視点・アニメーション・再生状態欄 | MEDIUM | A | active |  |  |
| ACNL-F0715 | Material可変領域の要素型と容量・件数の区別 | MEDIUM | A | active |  |  |
| ACNL-F0716 | PaneとMaterialのアニメーションリンク番兵 | MEDIUM | A | active |  |  |
| ACNL-F0717 | ResFontシート記述子とCWDH・CMAP可変長要素 | MEDIUM | A | active |  |  |
| ACNL-F0718 | 文字バッチのヘッダー・字形レコードと必要量 | MEDIUM | A | active |  |  |
| ACNL-F0719 | 既定TagProcessorは起動時の相対初期化表から構築される | MEDIUM | A | active |  |  |
| ACNL-F0720 | GPUリスト領域確保は失敗を戻り値で通知しない | MEDIUM | A | active |  |  |
| ACNL-F0721 | 入力遮断点と旧状態の扱いを再解析：holdだけではreleaseが残る | MEDIUM | A | active |  | 訂正あり |
| ACNL-F0722 | タッチ遮断は画面ロックではなく共有入力の変更である | MEDIUM | A | active |  |  |
| ACNL-F0723 | SELECTとSTARTの条件付き統合と読み替え前のSELECT除去 | MEDIUM | A | active |  | 訂正あり |
| ACNL-F0724 | 更新 RomFS は ARCHIVE_ROMFS とファイルパス {5,0,0} で実機から開け、背景の画像 2 枚を読めた（2026-10-20、HIGH（実機の表示＋呼び出しの静的な確認）） | HIGH | C | active |  |  |
| ACNL-F0725 | 実機で描画の資源のヒープの空きは、背景の確保の前に合計 3,196,648 バイト・最大の塊 3,196,535 バイトだった（2026-10-20、HIGH（実機の表示）） | HIGH | C | active |  |  |
| ACNL-F0726 | 描画の確保先は 2D UI・graphic FCRAM・VRAM A/B に分かれる | MEDIUM | A | active |  |  |
| ACNL-F0727 | 手紙の画像生成は UI ヒープから別画像を確保し、結果を検査せず複製する | MEDIUM | A | active |  |  |
| ACNL-F0728 | 画像キャッシュは ArcResourceAccessor 単位で、破棄時に参照が無効になる | MEDIUM | A | active |  |  |
| ACNL-F0729 | 通常の字形シートは専用 FontHeap にあり、CMAP と状態を通して参照できる | MEDIUM | A | active |  |  |
| ACNL-F0730 | nw::lyt は最大6段のTEVと3組の通常テクスチャ・UVを記録へ送る | MEDIUM | A | active |  |  |
| ACNL-F0731 | タイトルの地は16角の2画像を6枚のPictureで重ね、150フレームで動かす | MEDIUM | A | active |  |  |
| ACNL-F0732 | VRAM ExpHeap の空き・使用中リストと整列後の最大枠 | MEDIUM | A | active |  |  |
| ACNL-F0733 | 通常フォントの未収録文字と追加 JIS 書体の補完範囲 | MEDIUM | A | active |  |  |
| ACNL-F0734 | GX 完了カウンタと Framework の前回リスト待ち | MEDIUM | A | active |  |  |
| ACNL-F0736 | 手紙停止標本の空きと使用中合計、所有量の逆算条件 | MEDIUM | A | active |  |  |
| ACNL-F0737 | 入力の部分型を解析番号の無い名前に統一しメンバー位置を照合 | MEDIUM | A | active |  |  |
| ACNL-F0738 | パッド履歴保存前の共通境界は全体ゼロ化の合流後にある | MEDIUM | A | active |  |  |
| ACNL-F0739 | 装置パッドの読取りは成功旗に従いボタンとタッチを別々に更新する | MEDIUM | A | active |  |  |
| ACNL-F0740 | パッドbit13は正常読取りで除去されコントローラー保持に転写されない | MEDIUM | A | active |  |  |
| ACNL-F0741 | Controller計算の装置更新直後に必要な値はR4と旧状態R8/R9である | MEDIUM | A | active |  |  |
| ACNL-F0742 | 保持0x800はSTARTでありSELECTは読み替え前なら0x1000へ転写される | MEDIUM | A | active |  |  |
