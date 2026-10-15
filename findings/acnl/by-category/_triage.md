<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / _triage

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| ACNL-F0001 | 2026-09-12 GitHub保管の検証 | 指定6フォルダの3946files/4557271711bytesを全件SHA照合し、Git LFS28pathsを使用。認証情報の既知パターン検出0。非公開acnl_disassembleのIDAへ送信後、remote全3949files（案内/属性/manifestを含む）のblobとref/treeがローカル検証済み内容に一致。根拠 `_github_upload/upload_result.json`。ゲーム解析上の新しい結論はない。 |  | ? |
| ACNL-F0003 | 2026-09-11 project_v2環境整備 | IDA拡張の採否・互換性・AIからの利用方法は [plugins.md](../project_v2/docs/plugins.md)、入力とCPUの根拠は [platform.md](../project_v2/docs/platform.md)。CXIからのセグメント全bytes照合、Local Types、ARM実行、版間比較とGUIロードの証拠は `project_v2/work/evidence/`。研究上の新しいF番号は追加していない。 |  | ? |
| ACNL-F0011 | F-402 実機結果更新 | ACNLから内蔵辞書のOpen/Size2045891/先頭256byte Read/Close/Releaseが成功。読取りsampleは提供NCCHの0x1200と一意一致（HIGH:静的経路と実測）。SWKBD codeはkind1OpenがE0E046BE、kind2 .codeはOpen/Size471668成功。先頭256byte ReadはE0C046F9、全体471668byte Readは成功。FSのRead返信byte数も471668。全bytes同一性は | HIGH | ? |
| ACNL-F0012 | F-402進行中: ACNL自身の内蔵タイトルFS経路（MEDIUM） | idalib code.bin.i64: sub_1304C8はIPC0x08030204、TLS+0x80へarchive/fileのbinary pathを詰めSVC32。sub_346AB8はarchive0x2345678A/16byte archive/20byte file/READ1で同関数を呼び、sessionはdword_96EF28。独立caller sub_1290C4も同sessionを使用。libctru fs.cのOpenFileDirectly定 | MEDIUM | ? |
| ACNL-F0013 | F-401: 静的再配置315語・50比較一致・内蔵FS読取り条件 | 2026-09-10。DOCS/system_keyboard_relocation_audit.md参照。idalibの完全な命令列とxref/原本値から315語（旧52語を包含）を生成。直接参照243アドレスの未取得queue/エラー0、15 switch table、未解決literal/未処理switch 0。出力省略7件は完全版で回収し命令数を照合。静的根拠はMEDIUM、PC試験成功を実機HIGHへ昇格させない。 |  | ? |
| ACNL-F0016 | F-398: 関数型辞書の登録でPC候補列が実機保存値に一致（HIGH） | 0x18CDDCの日本語分岐はslot7=0x19BECC、8=0x19C334、9=0x16B890を登録。 | HIGH | ? |
| ACNL-F0017 | F-397: 予測モードにも複合候補の文節リストがある | HIGH（今回の未確定入力について）。実機「わたしはねこがすきです」はmode0/予測6件。 | HIGH | ? |
| ACNL-F0019 | F-395: UI単文節経路と直接連文節APIの区別 | MEDIUM。UI caller 0x10996Cは111FD4(ctx,1,text,0,0,55)を呼ぶが、最下層1145ACの | MEDIUM | ? |
| ACNL-F0020 | F-394: callback境界のレジスタ保存でF-393を修正 | **HIGH（利用者が自前メニュー復帰・しずえスキップ成功を実機確認）。** | HIGH | ? |
| ACNL-F0021 | F-393: 通常フックのR0保持不足によるOFF時SIGSEGV | HIGH（故障箇所と引数破壊。修正は未実施）。利用者のしずえスキップOFF時のSIGSEGVを | HIGH | ? |
| ACNL-F0022 | F-392: しずえスキップの通常フック化（2026-09-09） | **MEDIUM。** フリーズ原因と修正後生成物は静的に確定。修正版の実機確認は未実施。 | MEDIUM | ? |
| ACNL-F0023 | F-391: case 0を含むしずえスキップ常設版（2026-09-09、使用禁止） | **不採用。** case 0の呼出契約は有効だが、MITMフックの契約違反がある。 |  | ? |
| ACNL-F0026 | F-372: ACNL既存APTの実行文脈候補と失敗分岐のPC検証（2026-09-08） | **MEDIUM、実機アクセスなし。** 利用者が既存APT経路を第一候補に指定し、実機操作を保留。 | MEDIUM | ? |
| ACNL-F0029 | F-151: native TextBox draw の descriptor は `R2=0x330A605C` — `HIGH`（trace＋既存実測照合） | `scratchpad/trace_textbox_draw_args.py` を `nwlyt_TextBox_DrawToCommandList` | HIGH | ? |
| ACNL-F0030 | F-152: commit中の `TextBox_Draw` wrapper再入は不可 — `HIGH`（static＋実機例外） | F-151のdescriptorを渡してcommit hookから `TextBox_Draw (0x73CF48)` を呼ぶ試行は、 | HIGH | ? |
| ACNL-F0031 | F-153: direct-emitter patch generator 監査 — `MEDIUM`（独立の静的照合） | `PATCHES/cave_ui_picture_clone.py` の `MODE=audit` はゲームメモリを書き換えず、生成された | MEDIUM | ? |
| ACNL-F0032 | F-154: TextBox emitter直呼びも live DrawContext を二重更新する — `HIGH`（静的＋同一例外の再現） | F-153を通過したdirect-emitter版（`TextBox_EmitBatchToGpuCommands=0x4B7CE0`）は、wrapperを | HIGH | ? |
| ACNL-F0033 | F-144: 会話 TextBox も batch writer 経路 — `HIGH`（静的＋実機） | 会話表示中に `0x4BAFFC`（`sub_4BAFB0` 内の `sub_7E7F48` 呼出し）へ software | HIGH | ? |
| ACNL-F0034 | F-145: TextBox batch は専用list 32で構築され、メインlistへ再生される — `HIGH`（静的＋実機） | software BPを使わず、`scratchpad/trace_text_batch_submit.py` で会話名TextBoxのbatch | HIGH | ? |
| ACNL-F0035 | F-149: 会話本文フレームを構成する6 PictureとTextBoxを、相対配置のまま複製できた — `HIGH`（静的＋実機） | F-148のcommit点を使い、list 32の末尾へ `P_bg_L_00` / `P_bg_R_00` / `P_soft_L` / | HIGH | ? |
| ACNL-F0036 | F-148: 既存Pictureを非所有cloneして、任意座標の2D背景として追加できた — `HIGH`（静的＋実機） | F-147で確定したPane-treeのcommit直前、`nwlyt_DrawPaneTreeToCurrentList` (`0x4D7174`) の | HIGH | ? |
| ACNL-F0037 | F-147: `nw::lyt::Picture` は TextBox と同じ UI command-list 経路を使う — `HIGH`（静的＋実機） | `ti_nw_lyt_Picture=0x8C9B9C` / `vtbl_nw_lyt_Picture=0x8FBFFC` の Pane draw slot | HIGH | ? |
| ACNL-F0038 | F-146: TextBox batch は固定0x60-byte seedとglyph/state blockから構成される — `MEDIUM`（静的＋停止中live照合） | `TextBatch_BuildCommandStream` (`0x4D6570`) の命令列を、F-145 の同一会話名 | MEDIUM | ? |
| ACNL-F0039 | F-01 ゲーム同定 — `HIGH` | とびだせ どうぶつの森 (Animal Crossing: New Leaf)。 | HIGH | ? |
| ACNL-F0040 | F-02 アイテムは 4 バイト構造 — `HIGH` | ``` | HIGH | ? |
| ACNL-F0042 | F-04 型ID 113-122 は ASCII ではない — `HIGH` | `FieldObj_ResolveResultItem` (`0x597148`) が比較する 113-122 は | HIGH | ? |
| ACNL-F0043 | F-05 アニメ名テーブル基準は `0x0085FFB0` — `HIGH` | 16B × 約1028（終端未検証）。`+0` 未使用 / `+4` 本体名 / `+8` `_e1` / `+12` `_m1`。 | HIGH | ? |
| ACNL-F0044 | F-06 アニメ再生速度は VFP の S1 — `HIGH` | `Actor_PlayAnim` (`0x0068D0EC`) の引数: | HIGH | ? |
| ACNL-F0045 | F-07 アイテムID 158 は「穴」 — `MEDIUM` | **根拠**: 多くの掘る系アクションの結果として 158 が生成され、 | MEDIUM | ? |
| ACNL-F0046 | F-08 アクター状態テーブルは基準 `0x00843634` / エントリ `0x1C` — 基準は `HIGH` / 個々の割り当ては混在 | 状態 N のエントリ関数 = `[0x843634 + N*0x1C]`。 | HIGH | ? |
| ACNL-F0047 | F-09 掘れる/掘れないの判定は 4 段構成 — `HIGH` | スコップ振り下ろしから穴が空くまでに、少なくとも 4 段のガードがある。 | HIGH | ? |
| ACNL-F0048 | F-10 掘る経路の後段にアクションID 上書きがある — `MEDIUM` | 掘る経路 `0x5984F0` (`R4=19`, `R1=158`) に入った**後**、 | MEDIUM | ? |
| ACNL-F0049 | F-11 岩・構造物は cat10 経路の末端で脱落 — `HIGH` | 対象 ID 153（cat10）は `0x59836C` で cat10 経路へ分岐し、 | HIGH | ? |
| ACNL-F0051 | F-13 掘削適用は 32 スロットのレコード配列経由 — `HIGH` | `sub_5A16B0(actionID, playerIdx, item0, item1, item2, X, Y, a8, a9, a10)` が | HIGH | ? |
| ACNL-F0052 | F-14 フィールドアクションの実行経路 — `HIGH` | スコップのアクション決定から掘削レコード登録までの全経路が判明した。 | HIGH | ? |
| ACNL-F0053 | F-15 `Player_StartFieldAction` の呼び出し規約 — `HIGH` | `0x598660`-`0x598688` の assembly から確定。 | HIGH | ? |
| ACNL-F0054 | F-16 v1 の 3x3 ケーブがクラッシュした原因 — バグの存在は `HIGH` / 因果は `MEDIUM` | **原因A（コード上は確定）**: テールジャンプ前に R0-R3 を復元していなかった。 | HIGH | ? |
| ACNL-F0055 | F-17 コードケーブとして使える範囲 — `HIGH` | `Shovel_DecideState` (`0x662E68`-`0x663450`) 内で、パッチ `0x663294 = EA000028` | HIGH | ? |
| ACNL-F0056 | F-18 `Player_StartFieldAction` の呼び出し元は 16 箇所 — `HIGH` | `0x590000`-`0x5B0000` の BL 全走査で 16 件。 | HIGH | ? |
| ACNL-F0057 | F-19 18B キューのスロットは解放されないと枯渇する — `HIGH` | `0x595EA8`-`0x595EC0` がスロットの確保・初期化を行う: | HIGH | ? |
| ACNL-F0058 | F-20 【訂正】滞留の原因は PUSH 後のスタック引数のずれ — `HIGH` | **当初「滞留 4 件は `0x598688` 由来ではない」と結論したが、これは誤り。** | HIGH | ? |
| ACNL-F0059 | F-21 `FieldAction_Dispatch` の case 3 へは case 7 から来る — `MEDIUM` | ``` | MEDIUM | ? |
| ACNL-F0060 | F-22 隣マスが掘れない原因は対象アイテムの照合 — `HIGH` | 複数マス掘りで隣マスに穴が空かず、かつキューが詰まる原因は**同一**だった。 | HIGH | ? |
| ACNL-F0061 | F-23 進行中アクションテーブル `0x9AE1A4` — `HIGH` | 5 バイト × 32 エントリ。`g_FieldActionQueue`(`0x9AE15C`, 18B×4) の直後に隣接する | HIGH | ? |
| ACNL-F0062 | F-24 キューに積んでも実行段階は 1 マスしか処理しない — `HIGH` | F-22 の修正でケーブは正しく動くようになった。実機で確認できたこと: | HIGH | ? |
| ACNL-F0063 | F-25 レコードを積んでも反映されない — 反映側は 1 マスしか見ない — `HIGH` | v5（`0x59E9CC` = `BL FieldObj_ApplyDigRecord` をフックし X+1 で再度呼ぶ）の実測: | HIGH | ? |
| ACNL-F0064 | F-26 【成功】直接書き込み方式で隣マスに穴が空いた — `HIGH` | 状態機械・レコードを一切通さず、隣マスのアイテムを直接書き換える。 | HIGH | ? |
| ACNL-F0066 | F-28 マスへのアイテム書き込み API — `MEDIUM` | `sub_168E08(X, Y, flag, pNo, item)` (`0x168E08`): | MEDIUM | ? |
| ACNL-F0067 | F-29 掘削の実処理は `FieldObj_ApplyRecordByAction` の jumptable — `HIGH` | `0x5A06D4`-`0x5A0C1C`。`rec[16]`（actionID）で 29 ケースに分岐する。 | HIGH | ? |
| ACNL-F0068 | F-30 掘る動作のエフェクトは 3 系統 — `HIGH` | 状態 79 (`ShovelState_DigUpdate` = `0x65BC7C`) がアニメ ID で分岐して出す。 | HIGH | ? |
| ACNL-F0069 | F-31 【完成】隣マス掘りが中心マスと完全同期 — `HIGH` | 3 箇所のフックで、穴・抉れ・土しぶきのすべてが中心マスと同じタイミングで出る。 | HIGH | ? |
| ACNL-F0070 | F-32 CTRPF の空ページ `0x01E81000` は実行可能 — `HIGH` | CTRPluginFramework が起動時に確保する空メモリページ。 | HIGH | ? |
| ACNL-F0072 | F-34 【完成】3x3 マス掘り — `HIGH` | 周囲 8 マスに穴・抉れパーティクル・土しぶきパーティクルが、 | HIGH | ? |
| ACNL-F0073 | F-35 【訂正】`FieldObj_RevertRecord` は「結果を確定させる」処理 — `HIGH` | F-28 で「レコードをキャンセルするときに元のアイテムへ戻す処理」と記録したが**誤り**。 | HIGH | ? |
| ACNL-F0074 | F-36 木にぶつかったときの経路 — `HIGH` | **`Player_BeginFieldObjAction` も `FieldObj_ResolveResultItem` も通らない**別系統だった | HIGH | ? |
| ACNL-F0076 | F-38 「揺すると木を切る」パッチと通常経路 — `HIGH` | `Player_BeginFieldObjAction` (`0x595A8C`) の mode 分岐: | HIGH | ? |
| ACNL-F0077 | F-39 【危険】レコード枯渇で範囲外書き込み → SIGSEGV — `HIGH` | セッション4 で**実際にクラッシュした**（`got SIGSEGV signal, exc.code b`）。 | HIGH | ? |
| ACNL-F0078 | F-40 赤いバラの正体 — `FieldObj_FellObject` の `a2` が空だと `a1` から ID を流用する — `HIGH` | **衝突経路で「赤いバラの見た目をしたオブジェクト」が倒木演出中ずっと表示され、 | HIGH | ? |
| ACNL-F0079 | F-41 `FieldObj_FinalizeRecord` (0x5A10AC) — 伐採の終端処理 — `HIGH` | レコードが完了したときに `FieldObj_FellObject` を呼ぶ側。斧経路の呼び出し元 `0x5A1198` | HIGH | ? |
| ACNL-F0080 | F-42 【完成】木にぶつかって切り倒す — `HIGH` | 実機で確認済み。**パッチは 1 つも当てず、フック 1 箇所だけで完結する。** | HIGH | ? |
| ACNL-F0081 | F-43 RTTI からクラス名を引ける — `HIGH` | 出典: `REFERENCES/TEXTS/classes.txt` / `2.txt` / `1.txt`。**実機メモリで裏取り済み。** | HIGH | ? |
| ACNL-F0084 | F-46 実機イメージ `code_runtime.bin` を吸い出した — `HIGH` | `dump_code.py` で実行中プロセスから吸い出した。**`NCCH/exefs/code_runtime.bin`、10,485,760 バイト。** | HIGH | ? |
| ACNL-F0086 | F-48 静的 IDB を idalib-mcp で常用する — `HIGH` | `code_runtime.bin` (F-46) を **最小の ARM ELF ヘッダで包んで** idalib-mcp に読ませた。 | HIGH | ? |
| ACNL-F0089 | F-51 フェードの正体は `FaderColor`、`FaderMoment` に差し替えれば消える — `HIGH` | F-50 で「`0x568BF8` が唯一の調整点」と書いたが、**フェードには効かない。** | HIGH | ? |
| ACNL-F0091 | F-53 RTTI から全クラス名をデマングルして命名した — `HIGH` | `code.bin.i64`（セッション `acnl_code`）に **クラス 2,895 件・名前 5,481 件**を入れた。 | HIGH | ? |
| ACNL-F0094 | F-56 `ACNL_ID_Lists-master` との照合 — 4 件確定・1 件は資料側が誤り — `HIGH` | Vapecord 作者による ID 一覧 `REFERENCES/IDS/ACNL_ID_Lists-master` と、 | HIGH | ? |
| ACNL-F0102 | F-64: FOXXY の `pseudoType0x21` と、FOXXY 用 USA→JPN 変換 | confidence: **HIGH**（仕組みとアドレス対応）/ **LOW**（画面上の見た目） | HIGH | ? |
| ACNL-F0105 | F-67: 髪型変更状態 `0xB9` が帽子・アクセサリを消し、2 段アニメが反映を遅らせる | confidence: **MEDIUM**（削除先・同期先・アニメ分岐を静的に確認。提案パッチは実機未検証） | MEDIUM | ? |
| ACNL-F0109 | F-71: 通常Xの実入口は `sub_6D62AC` の動的menuId呼出し `0x6D6338` | confidence: **HIGH**（`code.bin.i64` の制御フローと実機breakpoint・引数・LRを照合） | HIGH | ? |
| ACNL-F0110 | F-72: `0x6D6338` はカタログ起動確認点として正しいが、持ち物全体の置換点としては遅すぎる | confidence: **HIGH**（実機画面結果、実行時オブジェクト、`code.bin.i64` のstock初期化/終了経路を照合） | HIGH | ? |
| ACNL-F0111 | F-73: 通常Xのfield側入口は `sub_165B40 -> sub_5C1F08`。診断traceのPC相対LDR移設は不可 | confidence: **HIGH**（実機のLR・trace buffer・SIGSEGV時レジスタと `code.bin.i64` を照合） | HIGH | ? |
| ACNL-F0113 | F-75: 「メニュー切り替え」enter入口なら持ち物UI初期化前に差替えられる | confidence: **HIGH**（状態記述子・関数入口・命令を `code.bin.i64` と実機で照合）、 | HIGH | ? |
| ACNL-F0114 | F-76: stock「メニュー終了まで待機」はcatalog終了の橋渡し候補 | confidence: **HIGH**（状態recordとupdate処理を `code.bin.i64` で確認）、 | HIGH | ? |
| ACNL-F0121 | F-83: `BsFtrMgr` のglobal公開は生成完了より早く、完全readyはobject `+19` の下位2bit | confidence: **MEDIUM**（`code.bin.i64` のvtable、create wrapper、3 phaseを静的照合） | MEDIUM | ? |
| ACNL-F0122 | F-84: Catalog actor typeはItemParam由来。`AcFtr` はbank確保、model非同期読込、layer 2登録の3 phase | confidence: **MEDIUM**（Item.bin loader、family table、AcFtr vtableと各phaseの静的照合） | MEDIUM | ? |
| ACNL-F0124 | F-86: parent拒否説を撤回。`ScStage` と`BsMenuTab`はいずれもchild gateを通る | confidence: **HIGH**（`UiScreen_OpenChild` の静的条件と停止中実機byteの精密再読を照合） | HIGH | ? |
| ACNL-F0125 | F-87: room 0の38-bank late allocationがphase 1即時失敗の最有力。容量1版を準備 | confidence: **MEDIUM**（create/destroy経路と確保量は静的確定、容量1版の実機結果は未確認） | MEDIUM | ? |
| ACNL-F0126 | F-88: phase 1公開中にstock previewへ戻るとtype `0xBC`を早期生成してSIGSEGVになる | confidence: **HIGH**（例外PC・全register・stack・actor/manager memoryと静的呼出し経路を照合） | HIGH | ? |
| ACNL-F0129 | F-91: `1UPキノコ` はfamily 3/type `0xBD`でも同じvptr+8 crash。preview特殊type全域を基底化 | confidence: **HIGH**（例外register/stack、ItemParam record、family table、復旧create、実機patch読戻しを照合） | HIGH | ? |
| ACNL-F0131 | F-93: ドロップの可否判定は 2 段。F-65 コード B が無効だった理由 | confidence: **HIGH**（実機で検証。コード A・B の結果が予測と一致／不一致を確定させた） | HIGH | ? |
| ACNL-F0133 | F-95: GPU コマンドバッファ `g_GpuCmdPtr` の特定 | confidence: **MEDIUM**（逆コンパイルでヘッダ定数と書き込み手順を直接確認。**静的解析のみ**、F-101 で訂正） | MEDIUM | ? |
| ACNL-F0134 | F-96: コマンドリストの終端・提出経路と GX API 一式 | confidence: **MEDIUM**（型値と引数位置を直接確認。**静的解析のみ**、F-101 で訂正） | MEDIUM | ? |
| ACNL-F0135 | F-97: `GpuCmd_GetProperty` と、自前コマンド追加の定石 | confidence: **MEDIUM**（getter の switch を逆コンパイルで直接確認。**静的解析のみ**、F-101 で訂正） | MEDIUM | ? |
| ACNL-F0139 | F-101: CLAUDE.md 準拠での再精査 — confidence の系統的誤り | confidence: **MEDIUM**（本項自体も静的解析のみ） | MEDIUM | ? |
| ACNL-F0141 | F-103: ★GX キューを実機で直接読み、1 フレームの構成を観測 | confidence: **HIGH**（静的 + 動的。TODO-48） | HIGH | ? |
| ACNL-F0142 | F-104: ★single-step 無効なら breakpoint が使える。`GpuCmd_SplitAndSubmit` の呼び出し元を捕捉 | confidence: **HIGH**（実機で breakpoint ヒットを観測） | HIGH | ? |
| ACNL-F0143 | F-105: ★MCP 側から Suspend できる（CLAUDE.md の記述を訂正） | confidence: **HIGH**（実機で制御実験） | HIGH | ? |
| ACNL-F0145 | F-107: ★`g3d::FuncNode` の実在を確認。コールバック登録 API まで判明 | confidence: **MEDIUM**（静的解析のみ。ただし独立した 2 経路から裏付け） | MEDIUM | ? |
| ACNL-F0146 | F-108: FuncNode 解析の精査 — 前提の再検証と 1 件の見落とし | confidence: **MEDIUM**（静的解析のみ） | MEDIUM | ? |
| ACNL-F0147 | F-109: ★★実機で `g3d::FuncNode` の実在とコールバックを確認（HIGH 達成） | confidence: **HIGH**（CLAUDE.md の定義どおり**静的解析と動的観測の双方**で確認） | HIGH | ? |
| ACNL-F0148 | F-110: ★`Use stepping support` を OFF にしても、ヒットした bp の削除は必要（TODO-54 完了） | confidence: **HIGH**（実機で対照実験。ユーザーの目視確認つき） | HIGH | ? |
| ACNL-F0149 | F-111: ★★TODO-60 解決 — ノードをシーンに載せる仕組み（`Scene_SubmitNode`） | confidence: **HIGH**（当初 MEDIUM。**F-112 の実機観測で昇格**） | HIGH | ? |
| ACNL-F0150 | F-112: ★★実機で F-111 を検証（TODO-64 完了）— 確度 `HIGH` へ。配列 #5 の記述を訂正 | confidence: **HIGH**（静的解析と実機観測の双方で一致。CLAUDE.md の `HIGH` 定義を満たす） | HIGH | ? |
| ACNL-F0153 | F-115: ★F-110〜F-114 の精査（TODO-75 の前の検証）— 誤り 2 件・過剰主張 3 件を訂正 | confidence: **HIGH**（訂正内容はいずれも一次証拠で確認） | HIGH | ? |
| ACNL-F0154 | F-116: ★★TODO-75 第1段達成 — シーンへノードを追加できた。あわせて Suspend の条件を確定 | confidence: **HIGH**（実機。対照実験つき） | HIGH | ? |
| ACNL-F0155 | F-117: ★TODO-79 完了 — `DUP=True` はハングしなかった。F-116 の「ハングの疑い」は誤り | confidence: **HIGH**（実機。ベースラインとの対照実験） | HIGH | ? |
| ACNL-F0156 | F-118: ★★注入した描画が画面に出ることを視覚的に確認。影は「アルファのみ」 | > **【後日訂正】本項 §3 の「重ねがけが濃くならないのは深度テストで落ちるから」という | HIGH | ? |
| ACNL-F0157 | F-119: ★★TODO-80 完了 — 自前の `g3d::FuncNode` を生成し、毎フレーム呼ばせることに成功 | confidence: **HIGH**（実機。生成物の型・コールバック回数を直接確認） | HIGH | ? |
| ACNL-F0158 | F-120: ★★★TODO-81 達成 — 自前の `FuncNode` から実際に画面へ描画できた | confidence: **HIGH**（実機。ユーザーの目視による決定的な A/B） | HIGH | ? |
| ACNL-F0163 | F-125: ★★★テキストを画面に描画した。タイル内 Morton スウィズル順も確定 | confidence: **HIGH**（実機。文字が読めた＝スウィズル順が正しいことの証明） | HIGH | ? |
| ACNL-F0164 | F-126: ★★★TODO-94 達成 — UI 層（`nw::lyt::TextBox`）に自前の 2D テキストを出した | confidence: **HIGH**（実機。住民名が `あんこ` → `テスト` に変わることを目視確認） | HIGH | ? |
| ACNL-F0165 | F-127: ★★`nw::lyt::TextBox` の構造を実機で確定 — 位置・色・サイズを自由に変えられる | confidence: **HIGH**（実機。1 項目ずつ A/B で目視確認） | HIGH | ? |
| ACNL-F0169 | F-131: TextBoxの折り返しはpane幅、縦方向は非clip。右端欠けの境界はCWDH glyphWidth | confidence: **折り返し・縦方向非clip・描画矩形 HIGH** / **右端の見た目の最終原因 MEDIUM** | HIGH | ? |
| ACNL-F0170 | F-132: 非整数倍率が右端の不均一さを生む — `HIGH` | F-131 の折り返しを除くため `T_time_0` の pane width を 40.0px にした状態で、同じ | HIGH | ? |
| ACNL-F0173 | F-135: `code.bin.i64` と `code_runtime.elf.i64` の独立照合 — `HIGH`（同一バイト列・アドレス）/ `MEDIUM`（実機での意味づけ） | 前回の「確定」を、別 IDB と別経路で再監査した。`code_runtime.elf.i64` は実機から取得した | HIGH | ? |
| ACNL-F0174 | F-136: atlas flush wrapper の同一視を撤回 — `MEDIUM`（呼び出し規約）/ `LOW`（command 名） | 再監査で、従来 `0x143718` を `GSPGPU_FlushDataCache`、`0xFFFF8001` を「flush command」と | MEDIUM | ? |
| ACNL-F0176 | F-138: ida-pro-mcp の実機接続経路を復旧・検証 — `HIGH` | IDA GUI の Remote GDB 接続や RPC 自体が壊れていたのではなく、Codex のMCP設定から | HIGH | ? |
| ACNL-F0178 | F-141: TextWriter wrapper のコピー範囲と reset の実体 — `HIGH`（静的命令列） | `sub_7E7F48` (`0x7E7F48`) は caller が渡した writer から **0x64 bytes 全体**を stack-local | HIGH | ? |
| ACNL-F0180 | F-142: EmitGlyphQuad は会話外 UI でも共有される — `HIGH`（実機） | 会話を開いていない状態で `0x4D4EAC` に software breakpoint を置くと実際に停止した。 | HIGH | ? |
| ACNL-F0182 | F-156: ★★★submit descriptor を静的に全導出。F-155a の observer は不要になった | confidence: **HIGH**（静的。decompile とアセンブリの両方で照合） | HIGH | ? |
| ACNL-F0184 | F-158: ★★自前の変換行列でテキストを任意位置に描けた — `HIGH`（静的導出＋実機で視認） | 住民名 `T_nam_00` の **赤い複製が、元の緑の名前から右へずれた位置に描かれた。** | HIGH | ? |
| ACNL-F0185 | F-159: コードケーブに使える領域は `0x01E82000` で終わる — `HIGH`（実機で読み書き検証） | `0x01E82000`-`0x01E821FF` は **128 ワードすべて `0xFFFFFFFF`**、 | HIGH | ? |
| ACNL-F0187 | F-161: ★★ケーブは `.text` 末尾のゼロ埋めに置く。ただし `.text` へは書けない — `HIGH`（実機の SIGSEGV と復帰で確認） | これまで全ケーブが使っていた `0x01E81000`-`0x01E81FFF` は、 | HIGH | ? |
| ACNL-F0188 | F-162: ★★★「好きな位置に好きなテキストを好きな色で」が通った — `HIGH`（実機で視認＋メモリで確認） | 会話ウィンドウの住民名を対象に、画面上に **4 つの「テスト」**が出た。 | HIGH | ? |
| ACNL-F0190 | F-164: `g_GfxAllocator` の正体と呼び出し規約を確定 — `HIGH`（静的解析、assembly まで確認） | `Render_InitGlobal`(`0x4E97CC`) が組み立てている: | HIGH | ? |
| ACNL-F0191 | F-165: ゲームのアロケータをフックから呼べた。0x80 境界・linear 窓内 — `HIGH`（実機） | 適用: `PATCHES/cave_gfxalloc_probe.py` | HIGH | ? |
| ACNL-F0192 | F-166: ★★★GPU 可視性を証明した。ゲームのアロケータから GPU が読めるメモリを得られる — `HIGH`（実機で視認） | `g_GfxAllocator` から確保したバッファを **GPU が実際に読んだ。** | HIGH | ? |
| ACNL-F0193 | F-167: ★★★テキストのグリフは「定数から四角形を生成するシェーダ」で描かれる。頂点データが存在しない — `HIGH`（実機の batch を解読） | 適用: `scratchpad/decode_text_batch.py` | HIGH | ? |
| ACNL-F0194 | F-168: ★★★任意の大きさの四角形を描けた。TODO-119 達成 — `HIGH`（実機で視認） | 適用: `PATCHES/cave_own_quad.py` | HIGH | ? |
| ACNL-F0195 | F-169: ★★★自前テクスチャを自前サイズの四角形に貼れた。TODO-120 達成 — `HIGH`（実機で視認） | 適用: `PATCHES/cave_own_texture.py` | HIGH | ? |
| ACNL-F0196 | F-170: CTRPF は発行点の問題を解決しない。cursor は値渡しでグローバルに無い — `HIGH`（静的解析、assembly で確認） | 「発行点の問題は CTRPF で実行すれば解決するのでは」という指摘を受けて確かめた。 | HIGH | ? |
| ACNL-F0198 | F-172: ★★★TextBox に依らない発行点を特定。答えは自分の記録の中にあった — `HIGH`（静的＋実機で前提を確認） | 「UI が何も出ていない状態では、CTRPF を含めどんな方法でも自前 GUI は不可能か」 | HIGH | ? |
| ACNL-F0199 | F-173: 発行点への注入は成功したが GPU が固まった。捕獲した列は自己完結していない — `HIGH`（実機、フリーズ） | 適用: `PATCHES/cave_replay_draw.py` | HIGH | ? |
| ACNL-F0200 | F-174: 発行点への注入は確立したが、GPU 状態の再現は現実的でない。方針を変えるべき — `HIGH`（実機で反復検証） | 適用: `PATCHES/cave_replay_draw.py`、`scratchpad/dump_frame_cmdlist.py`、 | HIGH | ? |
| ACNL-F0201 | F-175: ★★★Picture は毎フレーム必ず描かれる。TextBox ではなく Picture に相乗りすべきだった — `HIGH`（実機で計測） | 適用: `PATCHES/measure_picture_draws.py` | HIGH | ? |
| ACNL-F0203 | F-177: ★★★`nwlyt_Pane_DrawRecursive` は 1 フレームも欠けない。TODO-115 の答え — `HIGH`（実機で計測） | 適用: `PATCHES/measure_pane_draws.py` | HIGH | ? |
| ACNL-F0206 | F-180: ★★★UI 画像を「足す」ことに成功。TODO-122 の主要部達成 — `HIGH`（実機で視認） | 適用: `PATCHES/cave_add_quad.py` | HIGH | ? |
| ACNL-F0208 | F-182: 追加した UI 画像を絶対座標で置けた。複製元は地図の影 — `HIGH`（実機で A/B） | 適用: `PATCHES/cave_add_sprite.py` | HIGH | ? |
| ACNL-F0209 | F-183: ★索引エントリの `w3` は「色」。テクスチャはバッチ単位 — `HIGH`（静的解析） | F-180 で索引エントリの `w3` を「マテリアル関連」と書いたが、**誤り。** | HIGH | ? |
| ACNL-F0210 | F-184: 頂点カラーはアルファだけが効いた。RGB は素材の TexEnv 次第 — `HIGH`（実機で A/B） | 適用: `PATCHES/cave_add_sprite.py` | HIGH | ? |
| ACNL-F0211 | F-185: ★★★フック地点で **`R1` がコマンドカーソル**。任意の GPU コマンドを発行できる — `HIGH`（実機のコマンド列で確認） | ``` | HIGH | ? |
| ACNL-F0212 | F-186: ★索引エントリの意味を静的に確定。色は複製先ではなく**複製元**に出る — `HIGH`（静的＋実機 A/B 多数） | ```c | HIGH | ? |
| ACNL-F0213 | F-187: ★ゲーム自身の「色つきスプライト」を実測。構造は自前と同一だった — `HIGH`（実機フック） | `PATCHES/probe_vertex_color.py`（`0x4B8348` と `0x73CD1C` の 2 点フック）で、 | HIGH | ? |
| ACNL-F0214 | F-189: ★★★色ブロックの並びを確定。4 隅は「左上→右上→左下→右下」 — `HIGH`（実機で直接可視化） | 色つきバッチ（カウンタ `+36=1 +37=7 +38=2`）で、 | HIGH | ? |
| ACNL-F0215 | F-190: ★★★★色・位置・大きさの完全制御を達成。詰まっていた原因は**アンカー** — `HIGH`（実機） | `PATCHES/cave_add_sprite2.py`（色つきバッチに相乗り）。 | HIGH | ? |
| ACNL-F0216 | F-191: ★★★★自前テクスチャの適用に成功。欠けていたのは `reg 0x083` — `HIGH`（実機） | `PATCHES/cave_add_sprite2.py`（`EMIT_TEX = True`）。 | HIGH | ? |
| ACNL-F0217 | F-192: ★★★★フラッシュは配列の `[0].w0` を破壊する。退避先はポインタ −4 — `HIGH`（静的＋実機） | `TextDraw_EmitStatePrefix`（`0x4D5CB0`）も `DrawCtx_FlushBatch`（`0x4B8360`）も、 | HIGH | ? |
| ACNL-F0219 | F-194: ★★★UV の座標系を確定。アトラスから切り出せる — `HIGH`（実機で 3 段階の A/B） | 追加幾何エントリ（索引エントリの `w2` が指す先）の 4 float が UV。 | HIGH | ? |
| ACNL-F0220 | F-195: ★★★★★自前ビットマップフォントで文字列を描画。描画順も制御 — `HIGH`（実機） | `PATCHES/cave_draw_sprites.py`。**「ACNL が地図の上に表示され、読めました」**（ユーザー確認）。 | HIGH | ? |
| ACNL-F0221 | F-196: ★★★★フルカラー画像（RGBA8）の表示を確定 — `HIGH`（実機） | 64x64 の RGBA8 テスト画像を自前バッファに置き、120x120 で表示した。 | HIGH | ? |
| ACNL-F0222 | F-197: ★★★コマンドバッファは 1 つではない。`g_GpuCmdPtr` と `g_GpuCmdEnd` は別リストのことがある — `HIGH`（GPU ハングで判明） | 「そのフレームの最後のフラッシュ」を予測する方式が破綻したので | HIGH | ? |
| ACNL-F0224 | F-199: ★★★★★UI の座標系を確定。**縦横で縮尺が違う（非等方）** — `HIGH`（実機で段階的に測定） | \| 項目 \| 値 \| | HIGH | ? |
| ACNL-F0225 | F-200: ★★★★★UI は「1 本のコマンド列」ではない。記録と再生に分かれている — 静的解析 | > **2026-09-01 訂正（F-233）:** 記録／再生の構造は維持するが、下の |  | ? |
| ACNL-F0226 | F-201: F-200 の検証。**1 件の訂正と、GPU ハングの静的な説明** — 静的解析 | F-200 を疑って再検証した。**ユーザーの指示「confidence HIGH でも信用しきらない」に従う。** | HIGH | ? |
| ACNL-F0227 | F-202: ★★★メインリストの末尾に積んでも UI は描かれない。2 回目のクラッシュの原因 — `HIGH`（実機） | F-200 / F-201 の静的解析に基づき、**`Frame_DrawPass1024` の末尾** | HIGH | ? |
| ACNL-F0230 | F-205: ★★★★「最後に再生される」は画面（描画パス）ごとに違う — `HIGH`（実機 120 フレーム） | > **★F-253 で一部訂正した。単体で読まないこと。** 描画パスは 2 本ではなく **3 本**あり、 | HIGH | ? |
| ACNL-F0231 | F-206: ★★★★色とテクスチャの出所は「マテリアル」。自前で積まないと直前のペインのものになる — `HIGH`（実機） | `nwlyt_Picture_DrawToCommandList` は必ず先頭でこう呼ぶ。 | HIGH | ? |
| ACNL-F0232 | F-207: ★★★★★`drawctx+1692` が 0 だと UV が読まれずテクスチャ全面が貼られる — `HIGH`（実機） | `nwlyt_Picture_DrawToCommandList` より: | HIGH | ? |
| ACNL-F0234 | F-209: ★★★★★TODO-131 完了。自前 GUI が常に最前面に描かれる — `HIGH`（実機） | `PATCHES/cave_draw_topmost.py`。フックは 4 つ。 | HIGH | ? |
| ACNL-F0235 | F-210: ★★★★★狙う相手をリスト id で固定してはいけない。実行時に追いかける — `HIGH`（実機） | START のセーブ確認メッセージウィンドウを出すと、自前スプライトが消えた。 | HIGH | ? |
| ACNL-F0236 | F-211: ★★★★マテリアルは「たまたま」ではなく条件で選ぶ — `HIGH`（実機） | F-206 では「そのフレームで最初のフラッシュ時点のマテリアル」を流用していた。 | HIGH | ? |
| ACNL-F0237 | F-212: ★★★★★マテリアルには名前と定数色が入っている — `HIGH`（実機） | 自前スプライトが「たまに別の色を拾う」症状の正体。 | HIGH | ? |
| ACNL-F0239 | F-214: ★★★★★中立なマテリアルが 1 つも無い場面がある。定数色は借りる側で中立化する — `HIGH`（実機） | プラグインで動くようになった後、**タイトル画面とロード画面だけ** | HIGH | ? |
| ACNL-F0241 | F-216: ★★★★★`reg 0x082` は `(幅<<16)\|高さ`。正方形しか試していないと気付けない — `HIGH`（実機） | 自前 GUI はずっと `((TEX_H << 16) \| TEX_W, 0x082)` と書いていた。 | HIGH | ? |
| ACNL-F0242 | F-217: ★★★★SD から任意の画像を読む（TODO-130 完了）— `HIGH`（実機） | 3DS の GPU は **8x8 タイル + Morton 順**で、幅・高さは 2 の冪しか読めない。 | HIGH | ? |
| ACNL-F0243 | F-218: ★★★半透明（アルファブレンド）は使える — `HIGH`（実機） | OSD を避けた理由の 1 つが「アルファブレンドが使えない」ことだった（ユーザー指摘）。 | HIGH | ? |
| ACNL-F0248 | F-223: ★★★★描くものが無いのに記録を強制すると、しばらくして GPU コマンドリストが枯れる — `HIGH`（実機） | 自前 GUI を ON にして**しばらく遊ぶと**クラッシュした。 | HIGH | ? |
| ACNL-F0249 | F-224: ★★★★★確定した対象を「0 以外のときだけ更新」してはいけない — `HIGH`（実機） | F-223 の対策を入れてもまだ落ちた。ただし条件がはっきりした。 | HIGH | ? |
| ACNL-F0251 | F-226: ★★★★★相乗り先は「素で記録し直される」ものから選ぶ。強制は廃止 — `HIGH`（実機） | F-223 / F-224 の対策を入れても、しばらく遊ぶとまだ落ちた。 | HIGH | ? |
| ACNL-F0253 | F-228: ★★★★フェードは id 8（上）/ id 9（下）が最後に描く。両方に積めば判別が要らない — `HIGH`（実機） | ロード時のフェードで自前 GUI も一緒に暗くなる、という報告から。 | HIGH | ? |
| ACNL-F0254 | F-229: ★★★ケーブどうしの重なりは目視では見つからない。機械的に検査する — `HIGH`（実機） | ``` | HIGH | ? |
| ACNL-F0255 | F-230: ★★★★相乗り先は「候補のうち最後に再生されたもの 1 つ」。両方に積むと二重になる — `HIGH`（実機） | F-228 で「通常用（id 15 / id 16）とフェード用（id 9 / id 8）の**両方に積む**」ことにした。 | HIGH | ? |
| ACNL-F0260 | F-235: `Frame_EndDrawPass1024` 主リスト末尾の手製 Drawer-state 版は安全な提出経路ではない — `MEDIUM`（静的＋実機失敗） | `PATCHES/cave_tail_sprite.py` は `0x5A27C8` で、捕獲済み material と inline Drawer を用いて | MEDIUM | ? |
| ACNL-F0266 | F-243: CSEQ バイトコードの命令表を確定（ラベル境界一致 100.00%） — `HIGH` | `SOUND/cseq.py`。引数長は推測せず、**CSEQ が自前で持つ 33,344 個の `LABL` オフセットが | HIGH | ? |
| ACNL-F0267 | F-244: seq 型サウンド 2,839 件を WAV に合成 — `MEDIUM`（構造は HIGH、包絡の時定数は近似） | `SOUND/synth.py` + `SOUND/render.py`。CSEQ を実行してボイスを取り出し、 | MEDIUM | ? |
| ACNL-F0269 | F-246: ポルタメントの2つの誤り — `HIGH`（実機との聴き比べで確定） | `SOUND/synth.py` / `SOUND/render.py`。**命令表の一致率 100%・検証 20/20 を通っても | HIGH | ? |
| ACNL-F0270 | F-247: 実機との聴き比べで、包絡とビブラートの定数を較正 — `HIGH`（実機一致を利用者が確認） | 実機の対応表が無い箇所は、**変種を書き出して利用者に選んでもらう**形で決めた。 | HIGH | ? |
| ACNL-F0274 | F-251: 合成の 4 つの欠陥を実機との聴き比べで修正 — `HIGH`（利用者が実機一致を確認） | 全件バッチの成果物を聴いた利用者が 3 件の異常を報告し、そこから 4 つの欠陥が出た。 | HIGH | ? |
| ACNL-F0275 | F-252: 2D レイアウトの描画は「1 本のリストを画面ごとに 2 回再生」する — `HIGH`（静的。動的照合は未実施） | > **★F-253 で大幅に訂正した。単体で読まないこと。** リストは 1 本ではなく 2 本（`mgr+0x04`=上画面 / `mgr+0x10`=下画面）、 | HIGH | ? |
| ACNL-F0276 | F-253: ★★★★★描画パスは 3 本。`Frame_DrawPass1040` は下画面ではなく「上画面の右目」 — `HIGH`（静的＋実機の独立 2 系統） | F-252 で「Layout 用のリストは 1 本だけ」「投影は上下とも 400x240」と書いたのは**誤り**である。 | HIGH | ? |
| ACNL-F0280 | F-257: ★★★★F-256 のゲートの正体は「ゲームが**記録し直した**フレームだけ描く」だった — `HIGH`（実機・目視） | > **★F-263 で説明を訂正した。** 「作業配列はフレームごとに使い回される」という説明は**誤り**。 | HIGH | ? |
| ACNL-F0286 | F-263: ★★★★★F-257 / F-258 の説明は誤りだった。作業配列は Drawer の**固定メンバ**である — `HIGH`（静的） | Drawer（＝drawctx）のコンストラクタ `sub_4D7364`（`nw::font::RectDrawer` 派生）が | HIGH | ? |
| ACNL-F0289 | F-266: ★★★★★`SetupProjectionMatrix` は **`+0x28` / `+0x2C` しか読まない**。だから自前ノードでもそのまま呼べる — `HIGH`（静的のみ） | F-265 では投影行列を手で組み立てたが、その前提 | HIGH | ? |
| ACNL-F0291 | F-268: ★★★★★Drawer の既定コマンド列には **TEV 段が 1 つも無い**。色は必ずマテリアル由来 — `HIGH`（静的のみ） | 「`DrawBegin1` の既定 TEV で LA4 アトラス × 頂点カラーが合成されるか」（F-260 の未検証項目）に | HIGH | ? |
| ACNL-F0292 | F-269: TEV を自前で組んだ。**設計から借り物が消えた** — `HIGH`（静的のみ） | F-268 でマテリアルのテンプレートの符号化が全部割れたので、 | HIGH | ? |
| ACNL-F0293 | F-270: ★★★★DrawBegin1 は **テクスチャユニットを全部無効にする**。自前記録では立て直さないとテクスチャが読まれない — `HIGH`（静的 + 過去の実測列） | 自前記録の設計（F-259 以降）に残っていた穴。**これは `OWN_TEV` とは独立の問題である。** | HIGH | ? |
| ACNL-F0295 | F-272: F-264〜F-271 の整合監査。独立な結果と突き合わせて 1 件の誤りを訂正し、`SET_PROJECTION` を廃止した — `HIGH` | 新しい結論が既存の独立した結果と矛盾しないかを、6 点について確かめた。 | HIGH | ? |
| ACNL-F0296 | `SET_PROJECTION` を廃止した | 上の 3 番で、**ビューポートは各パスが `RecordChildren` の後・`SetDisplay`（replay）の前に |  | ? |
| ACNL-F0297 | F-273: ★★★★★致命的なバグ。記録スロットのエピローグが `R4` = drawctx のまま `Commit` していた — `HIGH`（静的のみ・未適用） | F-267 の教訓「生成器を変えたらケーブ 1 本を丸ごと IDA に通す」に従って | HIGH | ? |
| ACNL-F0298 | F-274: `sub_2F858C` は **3 引数の memcpy**。decompiler が R1/R2 を落としていた — `HIGH`（アセンブリ） | `GpuCmd_ReplayRecordedListRange` の末尾を Hex-Rays で読むと | HIGH | ? |
| ACNL-F0299 | F-275: 自前ノードに対してゲームが呼ぶのは vtable `+0x08` と `+0x14` の 2 つだけ — `HIGH`（静的） | `CAVE_N`（安全スタブ、常に `R0 = 0` を返す）が危険なスロットに置かれていないかを確認した。 | HIGH | ? |
| ACNL-F0300 | F-276: ★★★★★【F-268 の訂正】既定ブロックは **記録時ではなく再生時**に出る。フラグで切り替わる — `HIGH`（アセンブリ） | F-268 で「Drawer の既定 begin ブロックは記録の先頭で出る」と書いたのは**誤り**だった。 | HIGH | ? |
| ACNL-F0302 | リテラル参照の値まで検証する道具を追加した | `PATCHES/verify_literals.py`。`audit_node_cave.py` は |  | ? |
| ACNL-F0304 | F-279: 検証道具を全ケーブに広げ、死語を 1 本落とした — `HIGH` | `build_v` / `build_pass` / `build_t` は生の語列を返すので、 | HIGH | ? |
| ACNL-F0309 | F-284 (HIGH) — 自前 GUI（F-283 版）のクラッシュ `PC=0x839004` は「.text のゼロ埋めを NOP スライドして飛び出した」結果 | **根拠**（静的。`idalib-mcp` / `code.bin.i64`） | HIGH | ? |
| ACNL-F0313 | F-289 (HIGH・実機) — ★`nwlyt_Picture_DrawToCommandList` に**自前 Picture** を渡して 1 枚描けた | `0x73CB58 nwlyt_Picture_DrawToCommandList(picture, cursor, a3, drawctx)` は | HIGH | ? |
| ACNL-F0314 | F-290 (HIGH・実機) — CAVE_Q を `Picture_DrawToCommandList` 呼びへ置き換えた。**座標系は手書き経路と同一** | 2026-09-04 深夜〜2026-09-05。設計は `scratchpad/DESIGN_caveq_picture.md`、 | HIGH | ? |
| ACNL-F0316 | F-292 (HIGH・静的のみ) — ★F-291 を別関数で再検証（矛盾なし）。**正規の手順なら記録ケーブは丸ごと不要** | 全文は `scratchpad/MEMO_f292_proper_way.md`。 | HIGH | ? |
| ACNL-F0319 | F-295 (HIGH・実機) — ★方式 (a) 完成。ヒープから借りて**メニュー全体を正規経路で描いた** | 道具は `PATCHES/alloc_lyt_heap.py`（確保）と `PATCHES/build_pane_tree.py`（組み立て）。 | HIGH | ? |
| ACNL-F0320 | F-296 (HIGH・実機) — ★借りた領域を返せる。**確保 → 解放 → 再確保の往復を実機で成立** | F-295 で `nw::lyt` のヒープから 64KB 借りたが、**返す手段が無かった**。 | HIGH | ? |
| ACNL-F0323 | F-299 (HIGH・静的＋実機の実データ照合) — ★F-298 の検証と**訂正 2 件**。バッチの確保元を特定（残件 1） | \| 主張 \| 裏取り \| | HIGH | ? |
| ACNL-F0325 | F-301 (HIGH・静的のみ) — ★F-300 の訂正。**TextBox は必須ではない。**文字描画の本体は `TextWriter` | 利用者の指摘を受けて詰め直したところ、F-300 の | HIGH | ? |
| ACNL-F0327 | F-303 (HIGH・実機) — ★借りた nw::lyt ヒープは **GPU 可視**。自前フォント資源の設計を確定（描画は未達） | これまでアトラスは `g_GfxAllocator`（`*(0x0094CA30)`）から `0x4000` 借りていた（F-166 / F-221）。 | HIGH | ? |
| ACNL-F0330 | F-306 (HIGH・実機) — ★★★TextWriter 直呼びで描けた。TextBox の DrawSelf を通さない | F-301 で「TextBox は必須ではない」と結論した経路を実機で成立させた。 | HIGH | ? |
| ACNL-F0334 | F-310: 場面転換をまたぐと空きは 1.2MB → 0.6MB まで落ちる — HIGH | > F-309 の残件。**利用者に操作してもらって**測った（タイトル画面から進める・住民に話しかける等）。 | HIGH | ? |
| ACNL-F0339 | F-313: 「実測でないと決められない」は誤り。静的に決着した — HIGH | > F-312 D で `LIST_SIZE` を上げられるか・1 文字あたり何バイトかを | HIGH | ? |
| ACNL-F0340 | F-314: F-313 の裏取り。1 件は誤り、2 件は独立に裏付けが取れた — HIGH | > 「決め付けず裏取りする」ため、F-313 の結論を他の点・他のプログラムと突き合わせた。 | HIGH | ? |
| ACNL-F0341 | F-315: F-312〜F-314 を実機で検証。**結論はすべて正しかった** — HIGH | 自前ノードのコマンドリストが両画面とも作れた。 | HIGH | ? |
| ACNL-F0343 | F-315 追記: 1 度目のクラッシュについて（原因は未確定） | 同じ構成（借用 `0x50000` + `LIST_SIZE 0x10000`）が **2 回目は問題なく動いた**。 |  | ? |
| ACNL-F0361 | F-335（2026-09-07）: 複数パッチ切替と押し続け移動の再設計 | 利用者の壁抜け（複数アドレス×複数値）・座標移動（ホットキー＋押下方向へ |  | ? |
| ACNL-F0363 | F-337（2026-09-07）: 共有バッチ（§3.2）へ移る前の静的解析 | **confidence: MEDIUM〜HIGH**（すべて idalib で逆アセンブル。実機の裏取りはこれから） | MEDIUM | ? |
| ACNL-F0364 | F-338（2026-09-07）: 記録量の式を実機で確定 | **confidence: HIGH**（実機 4 点 + 見せる本数 4 通り。コードは新規注入なし） | HIGH | ? |
| ACNL-F0366 | F-340 — 色替え・書体替えの費用を分解し、記録量の式を完成させた（2026-09-07・実機） | **confidence: HIGH**（実機 15 点で誤差 0。うち 2 点は**式を作ったあとに予言してから測った**） | HIGH | ? |
| ACNL-F0367 | F-341（2026-09-07）: 費用の式を「当てはめ」から「逆アセンブルの写し」へ | **confidence: HIGH**（実機 19 点で誤差 0。うち **3 点は式を書いたあとに予言してから測った**） | HIGH | ? |
| ACNL-F0368 | F-342（2026-09-07）: 共有バッチの設計 — ★費用の 8 割は「コマンド語の器の取りすぎ」 | **confidence: HIGH**（静的解析 + 実機で確認。設計の数字は `PATCHES/design_shared_batch.py`） | HIGH | ? |
| ACNL-F0371 | F-345（2026-09-07）: 手紙は **2 つの大きな塊**を要る — 借りっぱなしでは通せない | **confidence: HIGH**（実機の停止位置・オブジェクトの中身 + `sub_1FC55C` の逆コンパイル） | HIGH | ? |
| ACNL-F0374 | F-348（2026-09-07）: 基準仕様 v3 を制定した | **confidence: HIGH**（`verify_spec_v3.py` 8 群 異常 0 件） | HIGH | ? |
| ACNL-F0379 | F-353（2026-09-07）: ★SELECT のビットは `0x800` — libctru の並びと違った（実測で確定） | **confidence: HIGH（実機で実測。基準値も取った）** | HIGH | ? |
| ACNL-F0381 | F-355（2026-09-07）: ★★ゲームは SELECT を START に読み替えている — 真因と正しい直し方 | **confidence: HIGH（逆アセンブル + 実機で確認。利用者「START が効き、SELECT が効きません。成功です」）** | HIGH | ? |
| ACNL-F0383 | F-357（2026-09-08）: ★FPS だけ上げてゲーム速度を据え置くことはできない（実機計測つき） | confidence: **HIGH**（静的にループ構造を確定 + 実機で周期を計測） | HIGH | ? |
| ACNL-F0386 | F-358（2026-09-08）: `BsFgProc::Setup` の正体 — `fgobj::Proc` のセットアップ段（＋しずえ会話スキップの下調べ） | confidence: **MEDIUM〜HIGH（静的のみ）**。**この作業中デバッガは切断されていた**（`is_debugger_on()==False`）。 | MEDIUM | ? |
| ACNL-F0387 | F-359（2026-09-08）: ★起動シーケンスと「しずえ画面 → 村へ出る」経路（＋未知のコード領域の発見） | confidence: **HIGH**（静的 + 実機 bp で確定）。詳細は `scratchpad/MEMO_f359_boot_sequence.md`。 | HIGH | ? |
| ACNL-F0391 | F-362（2026-09-08）: case 5 の `0x00606D78` と「準備しています」の出どころ | 詳細は `scratchpad/MEMO_f362_savemsg.md`。 | HIGH | ? |
| ACNL-F0395 | F-368（2026-09-08）: クラッシュ点の特定（実機デバッグ。ida-pro-mcp 直読み） | F-367 の静的監査に続き、ライブセッションへ接続して PC・レジスタ・ | HIGH | ? |
| ACNL-F0396 | F-369（2026-09-08）: クラッシュ原因は遷移フレームでの発火。安定ゲートで対策 | F-368 からの続き。利用者の申告： 項目ON・通知なし・ |  | ? |
| ACNL-F0397 | F-370（2026-09-08）: クラッシュ再発。犯人は呼び出し元の this=NULL | 前回と同じ PC=`0x0054C438`（`LDR R0,[R4,#0x148]`）だが今回は R4=`0x0`。 |  | ? |
| ACNL-F0402 | F-375（2026-09-08）: タイトルで即クラッシュ — 空リスト＋陳旧リンクの永久スキップ | 利用者の申告： タイトル画面で自前メニューONにしただけで動かなくなる。 |  | ? |
| ACNL-F0410 | F-385: 通常チャットから内蔵SWKBDの起動・キャンセル復帰に成功（2026-09-09） | F-384を適用した実機で通常チャットを開くと、内蔵ソフトウェアキーボードが起動した。 |  | ? |
| ACNL-F0417 | T015の再実機訂正（2026-10-13） | GPT-6/idalib、MEDIUM。pocket singleton0x9499ECをLoadStep/Disposeと原STRで照合。screen list先頭だけの取得を修正。trash cleanupはsource有効又はtarget drag可を音条件とするため、消去icon更新/非drag trashの組合せでは音が抑制される。成功時一度明示再生する。 | MEDIUM | ? |
| ACNL-F0421 | widget画像の参照寿命とcloset帰還・page待ち（2026-10-12） | 2026-10-13追加: 原hand/touch controlは+216 counter/+220 threshold、初回11/連続3を確認。node112/152が決定アニメ。owned pageは待機を省いて親1C38A0を同Calcで完了。退場はchild outer996/pocket1988の終端→元unbind/状態移行→Actor_RequestDestroy。キーボタン解放をchat入場条件にせず、held入力だけ暫定遮断。NativeEngine::L | MEDIUM | ? |
| ACNL-F0424 | nativeクローゼットとmenu intrusive node（2026-10-12） | IDA（idalib）/GPT-6、MEDIUM。更新SHA c635af8f.../ARM11/ARM32LE/imagebase0/主要10地点T=0を確認。原code.binのARMとRTTI/生table/ctor/索引consumerを独立照合。BsMenuChestは38708B、actualprimary0x8E5BB0（旧Explorer0x8E5BA8はheader）/25method。通常child ChangeStockItemは15528B、prima | MEDIUM | ? |
| ACNL-F0426 | Controller画素座標/vtableとchat画面引継ぎ（2026-10-12） | GPT-6 / IDA（idalib）、MEDIUM。更新SHA/ARM/imagebase/Tを確認しproducer540870/542D78/542E88とconsumer74F3FC/73BAC0/Matrix/Paneの独立ARM経路・旧input資料/sourceで照合。Controller+276/+280は画素float、TouchState+32/+36とは異なる。F004中心座標注記は撤回。53CDC4のvtable+24 BLXから+0はvtable、t | MEDIUM | ? |
| ACNL-F0434 | チップ長押しのstatic記録拒否と選択アニメ再開始（2026-10-10、MEDIUM） | 解析ソフトIDA（idalib-mcp）/解析モデルgpt-6.1-sol。F016配布で利用者が「窓未表示/縞アニメ振動」を実機報告。修正版はPC検査のみ、実機未確認。日本語無印ACNL＋更新、main SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb、ModuleFtr.cro SHA d2a65c85909782a66a5300df7f26f76289db69f7474f563d59 | MEDIUM | A |
| ACNL-F0435 | Editorキャッシュの再記録・チップ複製・内装保存/交換（2026-10-10、MEDIUM、実機未確認） | 追補F017: 長押し窓と縞アニメは利用者実機で不具合。F016のnative Select/取消/親整理stub検査はstatic記録とアニメgateを覆えていなかった。上記F017の原ARM再現/修正で補正。他F016項目の実機結果は未報告。 | MEDIUM | A |
| ACNL-F0441 | 下位種別12の送信APIと2台同時接続時の座標宛先（2026-10-04、静的＋実測） | NEW 3DS LLとOLD 3DSを同じ村に同時接続した屋外で、両機とも `Town=0x31F49A80`、`XYZ=0x33099E50` と実測。Python計算で下位種別12の累積オフセットは `0x11514BA`、16B本文は `[u32 streamOffset, X, Y, Z]`。汎用 `NetTransfer_SendSegments 0x616E10` は町サイズで制限しないが、通常町送信 `0x61FE5C` は制限する。送信の9引数ABI、2Bヘッ |  | ? |
| ACNL-F0442 | アニメ機構は ModelInstance_Create の引数で作られる（**a5 ではなく a6。IDA-opus-5-F015 で確定**）（2026-09-21、HIGH、実機A/B） | 解析ソフト: IDA / 解析モデル: opus-5。**同じ資源・同じモデルで第5引数だけ変えた対照実験**を実機で行った。 | HIGH | ? |
| ACNL-F0443 | アニメ本体は g3d の自前クラス。nw::gfx::AnimEvaluator を使うと落ちる（2026-09-21、HIGH、実機・自己訂正） | 解析ソフト: IDA / 解析モデル: opus-5。**F009 に「未検証の仮説」と書いた箇所を実機で突いて反証された。** | HIGH | ? |
| ACNL-F0444 | 自前資源のマテリアルアニメを生成し、自前instanceへ結線できた（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。**自分で読み込んだ `UnitCursor.bcres` のアニメを、 | HIGH | ? |
| ACNL-F0448 | ModelInstance_Create の a5/a6/a7 を実機で分離（2026-09-21、HIGH、実機A/B/C） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-F014 の仮説を実機で検証。 | HIGH | ? |
| ACNL-F0449 | アニメが何を動かすかは資源から読める。UnitCursor は色定数2本とUV平行移動（2026-09-21、HIGH、静的） | 解析ソフト: IDA / 解析モデル: opus-5。外部資料（[captainsouthbird/CGFXModel](https://github.com/captainsouthbird/CGFXModel)）は | HIGH | ? |
| ACNL-F0450 | 骨アニメを実機で結線し、骨が動いた（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T009。資源は IDA-opus-5-F018 が選んだ | HIGH | ? |
| ACNL-F0451 | 骨アニメが結線できる条件と、実機に触れずに選んだ資源の組（2026-09-21、HIGH、静的＋実機読み出し） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T009 の前段。**実機へは一切書いていない**（読み出しのみ）。 | HIGH | ? |
| ACNL-F0458 | 模様替えカーソルは大きさを変えていない。V2-F019 の「範囲の形」は誤り（2026-09-21、HIGH、静的） | 解析ソフト: IDA / 解析モデル: opus-5。**既存記録 V2-F019 の訂正**（`work/evidence/unit_cursor/README.md` §5.3〜5.4、 | HIGH | ? |
| ACNL-F0459 | 消した・動かした建物の当たり判定が残る理由と、再起動なしで直す 2 関数（2026-09-23、HIGH（静的）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の実機検証:「Vapecord で設置した建物には当たり判定があった。 | HIGH | S |
| ACNL-F0460 | ゲーム共通の 8 行リスト InstSelect<8> を下画面だけ借りる部品の作り（2026-09-25、MEDIUM: 静的＋実機の欄の読み取り。描画は未試験） | 公共事業のリストは `PWorkList : InstSelect<8> : SelectBase : CatalogBase`（RTTI）。`InstSelect<8>`（vtbl `0x8E54B4`、ctor `sub_7C6EB0`、4,812 B）は派生 10 種が共有する**ゲーム共通の 8 行リスト**で、純粋仮想は vt[13]（一覧を作る・件数 +2500）と vt[25]（i 行目の語）だけ。 | MEDIUM | S |
| ACNL-F0462 | アニメ 0x1E1（seo_down1）を途中で切ると縮んだまま残る — 骨 root の拡大を書くアニメがほぼ無い（2026-09-30、MEDIUM: 資源の全数調査＋静的。実機未観測。ゲームの骨格更新が「書かれない骨を戻さない」ことは推定） | 解析ソフト: IDA（主 IDB）＋ romfs の HumanAnim / 解析モデル: opus-5.5。利用者の観察: 骨格アニメ 0x1E1 で小さくなっている途中にアクション解除（0x06）や他のアクションへ | MEDIUM | S |
| ACNL-F0489 | 文字の挿入・削除・選択・確定、キーの経路、チャットの送信、入力欄の「未確定」と「選択」の飾り（2026-09-25、MEDIUM: 静的のみ。実機未確認） | F043 の続き。かな入力のコンポジションと漢字変換（利用者の依頼）の土台。 | MEDIUM | S |
| ACNL-F0490 | 文字入力（チャット・手紙・掲示板共通）の sys::TextManager の欄とカーソル・未確定の扱い（2026-09-25、MEDIUM: 静的のみ。実機未確認） | 漢字変換の候補欄とかな入力のコンポジション（利用者の依頼）の下調べ。取っ掛かりは AnimalBytes `Sources/ACNL/Chat.cpp`（入力欄の UTF-16 = [0x958108]、文字数 = [0x958114]+8）。 | MEDIUM | S |
| ACNL-F0491 | 共通ボタン（cmn_btn / btn_pos）・時計とベルの箱（time_bel_win）の組み立てと状態の規則（2026-09-25、HIGH: 静的＋実機画像 2 枚） | 設計ツール `src/acnl-ui-designer`（ef9b19c）の `cmnbutton.mjs` / `timebel.mjs` の根拠。表は同リポジトリ `docs/verification.md`。 | HIGH | S |
| ACNL-F0492 | 一覧の選択中の行とスクロールバー（CommonScrollBar）の見た目の規則（2026-09-25、HIGH: 静的＋実機画像 1 枚との照合） | 設計ツール `src/acnl-ui-designer`（3af30a5）の `instselect.mjs` / `scrollbar.mjs` の根拠。表は同リポジトリ `docs/verification.md`。 | HIGH | S |
| ACNL-F0493 | nw::lyt / nw::font の描画規則（ウィンドウ枠・テクスチャ座標・合成・アルファ・文字配置・アニメ曲線）を静的に確定（2026-09-25、HIGH: 静的＋実機画像 1 枚との照合） | UI 設計ツール `src/acnl-ui-designer`（利用者指示: 規則は静的解析で割り出し、画像は検証だけに使う）の描画器の根拠。全規則と番地の表は同リポジトリの `docs/verification.md`。 | HIGH | S |
| ACNL-F0497 | ゲームの SVC は 32 種類・745 か所（2026-09-25、HIGH: 命令語＋逆アセンブル、名前は libctru と 3dbrew の 2 資料で一致） | 再現 `tools/svc/scan_svc.py` → `work/evidence/svc/svc_sites.json`。文書 `docs/topics/svc.md`。 | HIGH | S |
| ACNL-F0502 | 髪は毎フレームの部品更新が pm+548 から読む。複製は本物のプロフィールで作り pm+548/+552 を書くだけでよい（F028 の一部訂正）（2026-09-24、MEDIUM（静的。複製での実機確認は未実施）） | `PlayerModel_UpdateParts 0x1D0AEC`（旧 vc_UPDATETANOFFSET）: 各バンクの枠の部品と望む値を比べ、違えば入れ替え式で読み直す。頭の望む値は | MEDIUM | S |
| ACNL-F0503 | PlayerModel と部品バンク。複製はゲーム自身の作成・片付け関数と「プロフィールの写し」で作れる（2026-09-24、HIGH（静的＋実機 BP・実機の読み取り）。複製の作成は未実施） | **構造**: AcPlayer+436 = PlayerModel（RTTI 11PlayerModel、vtbl 0x8E5F74、624 B）。pm+548 髪型 / +552 髪色 / +556 目の色 / +512 服 8 枠。 | HIGH | S |
| ACNL-F0506 | 地形のマス情報は 10 バイト（角の高さ 4 個＋属性）で、足元データと同じ形／橋の四角の外周は必ず端のマス（2026-09-24、MEDIUM（静的＋romfs 全 24 本）。実機の見た目は未確認） | **地形の高さ**: `Field_GetGroundHeightAtWorld 0x6C69C0` -> `sub_6C6A60` -> `sub_6A8C80`。区画ブロック + 28 から | MEDIUM | S |
| ACNL-F0507 | 橋のモデル行列は平行移動 (x, 0, 0) ＋曲面の回転だけ（地面の高さを使わない）（2026-09-24、HIGH） | **結論**: 村の橋（`12AcStrcBridge`）は、描画用の平行移動が **(x, 0, 0)** で、曲面の回転（X 軸まわり）だけが載る。 | HIGH | S |
| ACNL-F0511 | 建物の衝突判定 = 花を植えられない属性（byte_957A35 == 0）。利用者の正解と一致／プレビューが作れないのは親ヒープの断片化（2026-09-24、HIGH（利用者の正解と静的な表の一致）／HIGH（実機の読み取り）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の正解: ベンチ 2x1、街灯 1x1、噴水 3x3、交番 [[1,1,1],[1,1,1],[1,1,1],[0,1,0]]（3x3 と下段中央の突起）。 | HIGH | S |
| ACNL-F0514 | 衝突判定（歩けないマス）= 足元の属性コードをゲームの分類表 byte_957B34 で引いて 0 でないマス／プレビューの無限ロードとクラッシュの原因（2026-09-24、MEDIUM（静的＋利用者の説明と一致。実機の歩行では未確認）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の報告（配置の切り替えで無限ロード・SIGSEGV、UnitCursor が衝突判定準拠でない ほか）。 | MEDIUM | S |
| ACNL-F0516 | 建物エディターの下調べ — カメラ・プレイヤーの停止・占有マップ・足元の読み方（2026-09-23、MEDIUM（静的。実機未確認）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「Vapecord の MapEditor のカメラを参考に、建物を遠隔で建てる。プレイヤーは操作不可」。 | MEDIUM | S |
| ACNL-F0522 | 読み直しへ逃がしても必要量は同じ。ゲームでも落ちる状態は置く前に断る。地図は星アイコンまでゲームと同じに（2026-09-23、**HIGH（静的＋実機）**） | 解析ソフト: IDA / 解析モデル: opus-5.5。F008 の版の実機結果（利用者）: 建物はその場で出るようになった。置き続けると | HIGH | S |
| ACNL-F0524 | その場で作った建物は資源の枠を部屋が片付くまで返さない。尽きると読み込みスレッドが落ちる（2026-09-23、MEDIUM（静的＋実機のクラッシュダンプ）） | 解析ソフト: IDA / 解析モデル: opus-5.5。番人方式（F006 §4 旧版）の実機確認（利用者）:「枠を越えても置けるが、 | MEDIUM | S |
| ACNL-F0525 | 地図のアイコン枠は数を見ずに割り当てられ、溢れると星アイコン・柵の消滅・クラッシュになる（2026-09-23、HIGH（静的＋実機のクラッシュダンプ）） | 解析ソフト: IDA / 解析モデル: opus-5.5。F005 の実機確認（利用者）で (1)〜(5) は OK。ただし: | HIGH | S |
| ACNL-F0528 | 建物の高さは属性ブロックから。カタログ表示の読み込み手順（2026-09-23、MEDIUM（静的）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の指摘「建物配置における地面判定の高さ算出方法」に対する途中経過。 | MEDIUM | S |
| ACNL-F0529 | 公共事業は ID → 名前 1 つでモデルと足元が引ける。設置関数は見た目を作らない（2026-09-23、静的） | 解析ソフト: IDA / 解析モデル: opus-5.5。（旧表記 `IDA-opus-5-F039`、次の TODO は `IDA-opus-5-T026`〜`T028`。担当モデルを取り違えていたのを 2026-09-23 に訂正。番号は再利用しない） | HIGH | S |
| ACNL-F0530 | 更新タイトルの RomFS は開けなかった（2026-09-22、HIGH（事実）、原因は未解明） | 解析ソフト: IDA / 解析モデル: opus-5。利用者の実機報告： | HIGH | ? |
| ACNL-F0531 | `ARCHIVE_ROMFS` が返すのは **base だけ**。8,629 本（2026-09-22、HIGH、実機計測） | 解析ソフト: IDA / 解析モデル: opus-5。利用者が実機で「一覧を作る」を押した結果。 | HIGH | ? |
| ACNL-F0532 | RomFS の開き方を 3 箱所間違えていた（2026-09-22、HIGH、実機＋libctru ソース） | 解析ソフト: IDA / 解析モデル: opus-5。利用者報告:「一覧を作るを押すと | HIGH | ? |
| ACNL-F0534 | マス数変更中のクラッシュと、縞模様の 45 度（2026-09-22、HIGH、クラッシュダンプ＋静的） | 解析ソフト: IDA / 解析モデル: opus-5。 | HIGH | ? |
| ACNL-F0535 | 村の 1 マス = world 32 単位。UnitCursor の原点は quad の中心（2026-09-22、HIGH、実機＋CGFX） | 解析ソフト: IDA / 解析モデル: opus-5。**独立な 2 経路が一致したので確定とする。** | HIGH | ? |
| ACNL-F0539 | 姿勢を直接書くだけでは描かれない。骨格の更新が要る（2026-09-21、HIGH、実機。**F017 の訂正**） | 解析ソフト: IDA / 解析モデル: opus-5。**利用者の指摘（「UnitCursor が画面内に描画されていない」）から判明した。** | HIGH | ? |
| ACNL-F0540 | park の BP は焼き付かない。直前に外した番地だけが一時的に拒む（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。 | HIGH | ? |
| ACNL-F0542 | 骨・アニメの構造。node+0x228 は AnimGroup で、F029 の2語の正体（2026-09-21、HIGH、静的＋実機） | 解析ソフト: IDA / 解析モデル: opus-5。**アニメを結線するには instance 側に「アニメ枠」が要る。** | HIGH | ? |
| ACNL-F0543 | SkeletalModelも描けた。node+0x228/+0x22C は不可視の原因ではない（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。**`UnitCursor`（`0x40000092` = `nw::gfx::SkeletalModel`）を | HIGH | ? |
| ACNL-F0545 | park 用の BP は `0x1B721C` では張れなくなる。`0x1B7220` が同値（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。同じ boot の前半では `0x001B721C` への | HIGH | ? |
| ACNL-F0548 | 屋外座標の曲面変換は部屋フラグで切り替わる。165部屋中37部屋（2026-09-20、HIGH、静的＋実機） | 解析ソフト: IDA / 解析モデル: opus-5。`FieldPosition_ToRenderSpace 0x0052CDD8` は | HIGH | ? |
| ACNL-F0549 | 不可視だった UnitCursor は生のゲーム座標に置かれていた（2026-09-20、HIGH、静的＋実機、自己訂正） | 解析ソフト: IDA / 解析モデル: opus-5。`tools/hw/unitcursor_hw.py:356` は node行列を | HIGH | ? |
| ACNL-F0550 | 木1体の専用材質で透明度変更（2026-09-20、HIGH） | 解析ソフト: IDA / 解析モデル: gpt-6-astra。ゲームのcopy関数0x4ADD44(mask0x800)で専用ResMaterialを作りMaterial+80をredirect。SimpleMaterialActivator0x4A17B8はMaterial+8のみを読むので、それだけでは無効。このinstanceのRTTI/vtable4slotを複製しActivateだけgeneric0x49C08Cへ替えると、constant-alpha RGB b | HIGH | ? |
| ACNL-F0552 | 独立した木を表示・非表示。ゲーム座標には曲面変換が必要（2026-09-20、HIGH） | 解析ソフト: IDA / 解析モデル: gpt-6-astra。実機の準備済みSeason資源から `fg_treeA_4` のordinary Modelを独立生成し、player右36・倍率0.5で表示、OFFで消去を確認。マップの設置データは変更していない。主題・限界は [tree_live_plan](../docs/topics/tree_live_plan.md)。 | HIGH | ? |
| ACNL-F0555 | 頂点バッファの番地は VA→GPU 変換を通り、対応外の領域では黙って 0 になる（2026-09-18、HIGH、静的） | IDA-unknown-F026 で「頂点属性コマンド列は sub_7E5710 が組み立てる」と分かったので中身を読んだ。 | HIGH | ? |
| ACNL-F0557 | 過去の静的解析の誤り 2 件と見落とし 1 件（2026-09-18、HIGH） | 自前の UnitCursor が「描画経路のふるいを全部通るのに画素が 1 つも出ない」という実機結果を受けて、記録済みの静的結論を洗い直した。3 件の瑕疵が見つかった。 | HIGH | ? |
| ACNL-F0559 | 屋外表示の未解明点のうち4件を解決（ホルダ型・Create引数・マス換算・フック候補）（2026-09-18、MEDIUM） | (1) 資源ホルダ: ScStage ctor 0x7F195C（ScStage は 3504B）から、ScStage+0x418 = ssys::ma::HeapAllocator（8B、ctor HeapAllocator_Ctor 0x5667E8 / dtor 0x317CBC）、ScStage+0x420 = G3D 資源ホルダ（g3d::ResourceLoader＋ResourceSet、**264B**、0x420〜0x528。ctor G3dResHolde | MEDIUM | ? |
| ACNL-F0560 | Scene_SubmitNode のシーン番号は 0=通常描画・1=別モード・2=影マップ（2026-09-18、MEDIUM） | Render_InitGlobal 0x4E97CC が SceneContext/SceneTraverser を 3 本作る（g_SceneContexts 0x9C3098 / g_SceneTraversers 0x9C30A4）。Scene_DrawLayers 0x4EB840 の呼び出し元は 2 つで、Render_DrawScene2 0x4E976C が影マップ（g_SceneContext_2、IDA-unknown-F008）、Render_DrawSc | MEDIUM | ? |
| ACNL-F0561 | UnitCursor を屋外で出すための足場と不足（2026-09-18、MEDIUM） | 資源読み込みの入口を確定: G3dResHolder_RequestLoad 0x317920 → FileRes_RequestLoadAligned 0x569D94 → FileRes_RequestLoadAsync 0x569BA0。後者は**非同期**でホルダ+232 が状態（0未要求/1要求/2同期/3,4,5完了）、+68 パス・+204 ヒープ・+228 アライン・+233 非同期旗。戻り値は完了か。完了まで毎フレーム呼び直す必要があり（ScStage_Pr | MEDIUM | ? |
| ACNL-F0562 | 家具モデルは屋外でも出る（部屋ごとの収容数）。UnitCursor だけが屋内限定（2026-09-18、MEDIUM） | 利用者の指摘（オートキャンプは屋外判定で家具モデルを表示）を受けて IDA-unknown-F019 の表現を訂正。Room_GetFurnitureCapacity 0x5B5E18 が引く g_RoomFurnitureCapacity 0x8835BC は屋外でも非0で、村 0x00=38、Downtown 0x01=2、オートキャンプ場 0x9F/0xA0=10、カー内部 0xA1/0xA2=36、家1F 0x03=48。BsFtrMgr_CreateResource | MEDIUM | ? |
| ACNL-F0563 | 模様替えの家具の下の範囲表示は UnitCursor モデル、屋外では資源もクラスも無い（2026-09-18、MEDIUM） | 正体はパーティクルでなく 3D モデル romfs/Ftr/Chip/UnitCursor.bcres（モデル UnitCursor/UnitCursorLine/UnitCursorNG/UnitCursorRotate、m_UnitCursor の Visibility/MaterialColor アニメ）。読み込みは ScStage_LoadIndoorRes 0x611928 が部屋フラグ8（屋内、ItemIndoor.bin と同条件）のときだけ専用ヒープ Unit | MEDIUM | ? |
| ACNL-F0566 | sub_5C9C24 は夢見の館で落とした町を読み込んだ直後の作り直し（2026-09-18、MEDIUM） | Dream_RebuildDownloadedTown 0x5C9C24 の呼び出し元は DreamNet_ApplyDownloadedTown 0x6E205C だけ。こちらは受信 465024 B（0x71880）を TownBase へ複写し vc_PLOAD の後に呼ぶ。そこへ入る状態を設定する DreamNet_BeginDownloadTown 0x6E2850 / DreamNet_BeginDownloadListedTown 0x6E2774 の呼び出し元 | MEDIUM | ? |
| ACNL-F0567 | 日替わり処理の成長・郵便・「アイテム消えない」の中身（2026-09-18、MEDIUM） | Field_GrowUp 0x104B54 のコールバックを romfs Fg/Param/Fg.bin（16B×254、tools/fg_param_dump.py、旧実測カテゴリ7件一致）と IDS のアイテムIDで特定。苗の成長 Field_GrowUpSaplings 0x2FD778→Field_GrowUpAdvanceStage（+6の次段階、最大4段）、無効な位置（外周・草地以外・周囲障害物・密集）の苗は Field_GrowUpWiltSapling 0x3 | MEDIUM | ? |
| ACNL-F0571 | 木と家具の共通モデル生成・姿勢設定（2026-09-14、MEDIUM） | 木を含むfieldオブジェクトはItem_GetFieldObjDef→def+0xC→manager+0x414の22-byte shape表→名前+5→0x5992D4→0x4A5F20→0x58EEC0→0x4F048C。家具も同じModelInstance_Createに到達する。holder経由のtranslation/matrix/scaleと破棄入口を特定・命名。Create返値成功だけではholder+4非nullを保証しない。 | MEDIUM | ? |
| ACNL-F0572 | 木の実体とSeason資源を原本照合（2026-09-17、MEDIUM） | 更新Fg.binのItem0x26→shape0x25→base FgShape.binのfg_treeA_4。strideは元ARMの索引コードで決定。全23 Season00..22のモデル辞書と自身の名称が一致し、type0x40000012・mesh/material各1。ctrtool展開済み25資源を独立RomFS parserで原本bytesと照合PASS。base展開全体は10753/12938のPARTIAL、updateは4150/4150完了であり、全展 | MEDIUM | ? |
| ACNL-F0573 | Create全引数・instance共有範囲・更新/破棄（2026-09-17、MEDIUM） | 正常callerのR0=holder、R1=ResModel、R2/R3=HeapAllocator、stack=mask0/flag0/count1をassembly照合。普通Model本体0x220、holderのRTTIとは別。mesh記述子等はinstanceへコピーするがgeometry/textureとmask0のmaterial fieldは共有。Material_GetResourceForMaskが資源/privateを選ぶ。world更新→条件付き骨格更新 | MEDIUM | ? |
| ACNL-F0574 | サイズqueryとOOM・ready・owner寿命（2026-09-17、MEDIUM） | 元命令を原本codeと照合し、ARM11MPCoreでquery経路のみ実行。独立allocation ledgerと23 Season×mask0/0x10の46ケース一致。932/1664 bytes・最大alignment32はbuilder見積もりで、heap管理・size+align・資源/GPUメモリを除く。OOM時は0x4AB4A0でnull vtable参照、Setup結果も伝播されず事後検査だけでは安全でない。fgobj::ProcはSetup完了前にglo | MEDIUM | ? |
| ACNL-F0575 | resource描画属性・scene番号・画面を区別（2026-09-14、MEDIUM） | 0x317BD0の旧名ModelInstance_SetRenderLayerは誤解を招く。0x58E978のcallerは資源lookup結果を渡した後でinstanceを作り、関数内も相対辞書を変更する。ResModel_SetRenderLayerへ改名。共有資源を個別instanceの設定として変更しない。 | MEDIUM | ? |
| ACNL-F0577 | 旧プロジェクトの内部保存 | 旧原本・資料・キャッシュ32395ファイル、7271181421 bytesをコピー元とSHA-256照合して保存。 |  | ? |
| ACNL-F0580 | Volta の shim が引数を改行で切り落とす（このPC全体の問題） | `node` の実体は `C:/Program Files/Volta/node.exe`（Volta 2.0.2 の shim）。 |  | ? |
| ACNL-F0581 | IDA9.3のGhidra XML Exporter導入・主IDB出力 | ローカルGhidra11.0.1の7xx版はIDA9のAPIに非対応。公式Ghidra12.1.3付属9xx版（Exporter 5.0.2）を原本のままユーザーIDAのpython/idaxml.pyとplugins/xml_exporter.pyへ配置。原本manifestと配置先SHAが一致する。IDA SDK930でplugin読み込み・XML出力を確認。 |  | ? |
| ACNL-F0584 | 下位種別12の受信に町サイズ上限がない（2026-10-04、MEDIUM） | 解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。日本語版更新 `artifacts/update/exefs/code.bin`、SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。通常送信 `sub_61FE5C` は町全量 `0x71880` Bで止まるが、非ホスト受信 `sub_187030` は先頭4Bオフセットが `>=0x10EA` なら  | MEDIUM | ? |
| ACNL-F0588 | nw::lyt の Window は 1 枠でも描ける（2026-10-05、MEDIUM: 静的 + designer の再現がスクショと一致） | 解析ソフト IDA（idalib-mcp）、解析モデル opus-5.5。HHD の画面を ACNL で再現する作業（D005 / T011）の周辺で確認。 | MEDIUM | S |
| ACNL-F0591 | ウィンドウの中身にテクスチャがあるなら UV の組が要る（無いと nwlyt_CalcTexCoordsForGpu が落ちる）（2026-10-05、HIGH: 実機のクラッシュ + 静的） | 解析ソフト IDA（ida-pro-mcp / idalib-mcp）、解析モデル opus-5.5。T013 段 2 の実機試験。 | HIGH | S |
| ACNL-F0593 | カタログを開くときの遷移は BsMenuBg の切り替え（クロスフェード）と画面自身の in アニメ。Fade / Wipe / Fader は使わない（2026-10-05、HIGH: 静的 + 実機の否定観測） | 解析ソフト IDA（idalib-mcp / ida-pro-mcp）、解析モデル opus-5.5。段階 2（上画面と遷移）の下調べ。**既存資料**: 旧 RE/FINDINGS.md F-50（Wipe、UiAnim のレート）/ F-51（Fade・Fader 9 個と Fader_SetKind の種類）、 | HIGH | S |
| ACNL-F0595 | HHD の BFLAN を ACNL の BCLAN に変換できる（書き出しは ACNL の実物 727 本でバイト一致）・不透明度の伝播の旗（2026-10-05、HIGH: 実物との照合） | 解析モデル opus-5.5。段階 2 の遷移（開閉のアニメ）。 | HIGH | S |
| ACNL-F0596 | ACNL の見た目の記録と色の表。HHD の番号がそのまま使える（2026-10-05、MEDIUM〜HIGH: 静的 2 経路（命令の復元と HHD のデータ）の一致。実機での反映は未） | 解析ソフト IDA（idalib-mcp）、解析モデル opus-5.5。段階 3（プレイヤーへの反映）。利用者指示: 反映するのは髪型・髪色・目の形・目の色・肌の色、まずオフラインだけ。 | MEDIUM | S |
| ACNL-F0598 | レイアウトの材質の TEV の段と座標生成の意味（2026-10-05、HIGH 相当: 逆アセンブル + ACNL の実在の材質 215 個と照合。実機の描画は未確認） | 解析モデル opus-5.5。IDB: `nwlyt_Material_EmitTevStages 0x4B8790`（命名・注記）、`nwlyt_CalcTexCoordsForGpu 0x73B650`（注記）。 | HIGH | S |
| ACNL-F0607 | 0xAA7994 はホストの枠 — 自分のプレイヤーは [自分の通信番号]（2026-10-06、HIGH: 静的（vc_PLAYERINSTANCE の索引）＋実機の症状が一致） | 解析モデル opus-5.5。 | HIGH | S |
| ACNL-F0622 | 家の部屋の壁紙・床をその場で替えるゲーム自身の手順（2026-10-07、MEDIUM: 静的 2 経路。実機未確認） | 解析ソフト: IDA / 解析モデル: opus-5.5。T022 の壁紙・床紙リストの前提。主 IDB に命名・注記・保存済み。 | MEDIUM | S |
| ACNL-F0627 | 服・ワンピース・K.K. の曲を部屋に置くときの品番（2026-10-07、MEDIUM: 静的 2 経路） | 解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（推論 xhigh）**、Codex CLI のサブエージェント（依頼 work/codex/tasks/t022_pair_ids.md、アプリサーバー経由）。採番・照合・記録は親（opus-5.5）。根拠 **work/evidence/t022_pair_ids/report.md**。主 IDB に命名 13 関数・2 表、型 19、構造体 2、カテゴリの Enum、コメント 58（ID  | MEDIUM | A |
| ACNL-F0628 | HHD と ACNL でアニメのコマ数の数え方が 1 つ違う（2026-10-07、HIGH: 静的＋実機の症状） | ACNL の UiAnim_Step 0x568964: +0x14 bit0（ループしない）なら frame は frameSize(+4) − 1 で頭打ち、bit0 が無ければ frameSize で巻き戻す。UiAnim_IsFinished 0x74F58C も frame >= frameSize − 1。ACNL の BCLAN（ループしない）は最後のキーが frameSize − 1 に 527 件（frameSize ちょうどは 7 件）。 | HIGH | S |
| ACNL-F0640 | パチンコ弾はPlayer内の固定3スロットで管理される | **確度: MEDIUM（複数の独立した静的証拠。実機メモリ観測は未実施）** | MEDIUM | B |
| ACNL-F0643 | crash_dump_00000005 の直接fault | **確度: HIGH（dump＋本体命令列）。根本原因の旧帰属は撤回。** | HIGH | B |
| ACNL-F0644 | crash_dump_00000006 の直接fault | **確度: HIGH（dump＋本体命令列）。timing raceという旧帰属は撤回。** | HIGH | B |
| ACNL-F0647 | 持ち物画面はBsMenuItem UI stateとPlayer state 0x16の二重state machineで成立する | **確度: HIGH（添付Ghidra XML/bytesの独立静的解析＋実機state観測）。state 0x16→0x06のcallerだけ未確定。** | HIGH | B |
| ACNL-F0649 | type 0x10 completion token案は実機クラッシュで棄却 | **確度: HIGH（crash_dump_00000008＋静的再監査）。** | HIGH | B |
| ACNL-F0652 | 0x838080 dead-cave再利用は実機runtimeと衝突する | **確度: HIGH（crash_dump_00000009＋enable直後再現）。** | HIGH | B |
| ACNL-F0654 | custom guard依存を廃止し、menu-open中の0x16→0x06を直接抑止する | **確度: MEDIUM（静的検証済み、実機未検証）。** | MEDIUM | B |
| ACNL-F0655 | Ghidra-gpt-sol-5.6-F016 AR先頭E blockの最終行が1word欠けていた | **確度: HIGH（ARテキスト構文再検査）。** | HIGH | B |
| ACNL-F0659 | trace領域をARで0固定していたためGhidra-gpt-sol-5.6-F019/Ghidra-gpt-sol-5.6-F020 traceは観測不能だった | **確度: HIGH（AR実行モデルと現行コードの直接確認）。** | HIGH | B |
| ACNL-F0660 | AcBalloon terminal dropがPlayer state 0xA4 reactionを明示要求し、desired=0x06へ戻る | **確度: HIGH（実機trace＋ModuleVillage.cro＋main static call chainが一致）。** | HIGH | B |
| ACNL-F0661 | Ghidra-gpt-sol-5.6-F022後に残るdirect 0x16→0x06を観測する | **確度: HIGH（hook ABI/分岐/cave collision静的検証。caller実機値待ち）。** | HIGH | B |
| ACNL-F0663 | custom AcBalloon* identityでterminal A4だけ抑止 | Ghidra-gpt-sol-5.6-F024実機trace: |  | B |
| ACNL-F0664 | actor identity guard keeps inventory Player state 0x16 | **確度: VERIFIED ON HARDWARE.** |  | B |
| ACNL-F0666 | landing identityをstate helper内でpre-arm | Ghidra-gpt-sol-5.6-F026 hardware result: |  | B |
| ACNL-F0669 | action 0x12誤用を撤回し、stock action 0x0Aでimpact定着 | Ghidra-gpt-sol-5.6-F029 hardware result: |  | B |
| ACNL-F0670 | Player-origin updaterを外し、balloon impact位置からpersistent ground objectを生成 | Ghidra-gpt-sol-5.6-F030 hardware result: |  | B |
| ACNL-F0671 | 0x0A visual生成を外し、stock post-visual field commitだけ再利用 | Ghidra-gpt-sol-5.6-F031 hardware result: |  | B |
| ACNL-F0672 | custom falling objectをbusy tokenにしてdrop queueをlock | Ghidra-gpt-sol-5.6-F032 hardware success後の残課題: |  | B |
| ACNL-F0673 | dit (post Ghidra-gpt-sol-5.6-F032) | User correction accepted: ACNL already owns the drop queue; adding a second custom busy lock before fully understanding the native lifecycle was the wrong integration direction. |  | B |
| ACNL-F0674 | native DropData queue integration | Ghidra-gpt-sol-5.6-F032 remains the hardware-verified visual/persistence baseline. Ghidra-gpt-sol-5.6-F033's independent busy flag is retired. |  | B |
| ACNL-F0676 | native DropData allocation from the Ghidra-gpt-sol-5.6-F032 callsite context | Hardware results leading here: |  | B |
| ACNL-F0677 | Ghidra-gpt-sol-5.6-F036 crash-dump root cause and ABI-safe bridge | Hardware: |  | B |
| ACNL-F0678 | e-analysis after Ghidra-gpt-sol-5.6-F037 | Current implementation status: |  | B |
| ACNL-F0682 | local/self and inline tag scope | **確度: HIGH (static JPN v1.5 path analysis; hardware tagged-chat test still pending).** | HIGH | B |
| ACNL-F0683 | 0x958108 is pointer storage | `0x958108` is a global dword pointer slot, not inline UTF-16 storage. |  | B |
| ACNL-F0684 | direct 0x958108-pointee test negative; parse is still post-submit | **Hardware observation:** a valid Color-tag sequence written to the current pointee read from `0x958108` did not visibly decorate chat. |  | B |
| ACNL-F0686 | mode1 sender bypass preserves tags on hardware | **Hardware-confirmed.** |  | B |
| ACNL-F0687 | sender local Color render hardware success | **Hardware-confirmed.** |  | B |
| ACNL-F0688 | player/town name tag sanitizer | group5/type0 current player name -> Insert method 0x5ECAB8. |  | B |
| ACNL-F0691 | low field-object display fallback | User hardware observation: Item IDs 0x0000..0x00FA appear with one shared furniture/default icon and name `???`. |  | B |
