<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / _product

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| ACNL-F0001 | 2026-09-12 GitHub保管の検証 | 指定6フォルダの3946files/4557271711bytesを全件SHA照合し、Git LFS28pathsを使用。認証情報の既知パターン検出0。非公開acnl_disassembleのIDAへ送信後、remote全3949files（案内/属性/manifestを含む）のblobとref/treeがローカル検証済み内容に一致。根拠 `_github_upload/upload_result.json`。ゲーム解析上の新しい結論はない。 |  | ? |
| ACNL-F0002 | 2026-09-12 普通チャットの入力所有者・日本語フォント・候補表示 | 通常gohanへ候補列挙を追加。BsMenuChatの所有者照合、ゲーム日本語フォント154シート対応、stock Batch容量、threadJoinの正のtimeoutの扱いを[トピック](../project_v2/docs/topics/chat_kanji.md)へ集約。根拠 `project_v2/work/evidence/chat_kanji/`。字形/幅は全65536コードポイントで元ARMと一致。リンク済み変換候補17/6/143/3/1件が原本と一致し、 | MEDIUM | ? |
| ACNL-F0003 | 2026-09-11 project_v2環境整備 | IDA拡張の採否・互換性・AIからの利用方法は [plugins.md](../project_v2/docs/plugins.md)、入力とCPUの根拠は [platform.md](../project_v2/docs/platform.md)。CXIからのセグメント全bytes照合、Local Types、ARM実行、版間比較とGUIロードの証拠は `project_v2/work/evidence/`。研究上の新しいF番号は追加していない。 |  | ? |
| ACNL-F0004 | F-407 実機成功: キーボード非起動で候補17/6/143件を取得（2026-09-11、最新・HIGH） | 利用者がF407を配置・ACNL再起動/再アタッチ。Suspend/bp0、実機headerと全生成コードアンカー、成果物/現行ソースhashを照合した。要求2の展開・辞書配置・315再配置が成功し全解放された後、要求3で「かんじ」「わたしはねこがすきです」「か」を各1回実行。候補17/6/143件が原本PCと全順位一致。前2入力は保存済み実機SWKBD候補列とも直接一致。「か」は初回50件からgetterが143件まで追加検索し、終端0を確認した。 | HIGH | ? |
| ACNL-F0005 | F-407 PC準備時点の履歴（配置待ちは解消済み） | 独立Plugin/SwkbdEngineProbe/swkbd_engine_probe.3gxを作成。289,985 bytes、SHA50ec21a1bde6d52f13fa916ac23aceb2f81dbb833a5ca4db8ca77c3b96368385。ソース/ホスト/ARM構文を検証してからビルド。生成1301命令/213直接分岐/48PCリテラルの検査、生成ARMから原本エンジンへの一連のPC試験、mailbox誤適用防止10条件までPASS。展開はctrt |  | ? |
| ACNL-F0007 | F-405 解決: キャッシュ処理中のクラッシュ、再起動で一時変更解除 | Plugin/crash_dump_00000004.dmpのPC0xFFF2B3F8はMCR p15,0,R1,c7,c10,1。R1=FAR=0x061BE000が試験arenaと一致し、DFSR0x805はsection translation fault/write。ARM11 core1、SVC mode、保存プロセスsocket/TID0x0004013000002E02。ダンプ解析とidalibの保存命令列を照合（HIGH）。他コアの異なるアドレス空間が原因とい | HIGH | ? |
| ACNL-F0008 | F-404 実機成功: 3gxで5 MiB確保・内蔵FS読取り（2026-09-11） | 利用者が独立swkbd_probe.3gxを配置しACNLを再起動。新規header/生成コードアンカーを照合、Suspend/bp0を確認してmailboxに1要求を設定。5秒の自動Suspend付きResume後、state2/failure0。5,242,880 bytesを確保して全域write/readback成功、内蔵辞書2,045,891 bytesと圧縮.code 471,668 bytesのOpen/GetSize/全体Read/CRC32一致/Close/ |  | ? |
| ACNL-F0009 | F-403完了・F-404 3gx検証へ移行（2026-09-11） | 最新はDOCS/system_keyboard_plugin_probe.md。全辞書2,045,891 bytesの実機取得と全bytes/SHA照合、6辞書個別照合が完了。一時handle/buffer/wrapperは全復元済み。エンジン実機実行は未実施。 |  | ? |
| ACNL-F0010 | F-402 最終: 内蔵code全体Read・バイト同一性・cleanup確認（HIGH） | code kind2で読んだ471668bytesが提供NCCH内.codeと完全一致。SHA09e684ca41504af96b6548f42e8a2a159f07d3865ca7077e1d4f8356b98ec14e、ExeFSエントリhashとも一致。ctrtool再展開770048bytesは従来解析対象SHAa0b78005b0a99116ca703bc9b7625ce1b0f2d4cc45f66fc6fb9ab8a34244d4f0と一致。NCCHheader署 | HIGH | ? |
| ACNL-F0013 | F-401: 静的再配置315語・50比較一致・内蔵FS読取り条件 | 2026-09-10。DOCS/system_keyboard_relocation_audit.md参照。idalibの完全な命令列とxref/原本値から315語（旧52語を包含）を生成。直接参照243アドレスの未取得queue/エラー0、15 switch table、未解決literal/未処理switch 0。出力省略7件は完全版で回収し命令数を照合。静的根拠はMEDIUM、PC試験成功を実機HIGHへ昇格させない。 |  | ? |
| ACNL-F0014 | 最新 F-400: 再配置のPC試験成功・テーブル同梱を避ける方針 | 利用者はSD/3gxへテーブルをリソース同梱する方式を避けたいと指定。 |  | ? |
| ACNL-F0015 | 最新 F-399: 画面・APTなしのエンジン実行をPCで確認 | 初期化から全候補列挙までOS mockなし。原本data/BSSをRO化しても17/6件一致。 |  | ? |
| ACNL-F0016 | F-398: 関数型辞書の登録でPC候補列が実機保存値に一致（HIGH） | 0x18CDDCの日本語分岐はslot7=0x19BECC、8=0x19C334、9=0x16B890を登録。 | HIGH | ? |
| ACNL-F0018 | F-396: 旧SWKBDケーブとGUI v2の重複を回避し再適用 | HIGH（配置の重複と適用内容をソース/実機メモリで照合。移設後の起動動作は未観測）。 | HIGH | ? |
| ACNL-F0020 | F-394: callback境界のレジスタ保存でF-393を修正 | **HIGH（利用者が自前メニュー復帰・しずえスキップ成功を実機確認）。** | HIGH | ? |
| ACNL-F0021 | F-393: 通常フックのR0保持不足によるOFF時SIGSEGV | HIGH（故障箇所と引数破壊。修正は未実施）。利用者のしずえスキップOFF時のSIGSEGVを | HIGH | ? |
| ACNL-F0022 | F-392: しずえスキップの通常フック化（2026-09-09） | **MEDIUM。** フリーズ原因と修正後生成物は静的に確定。修正版の実機確認は未実施。 | MEDIUM | ? |
| ACNL-F0023 | F-391: case 0を含むしずえスキップ常設版（2026-09-09、使用禁止） | **不採用。** case 0の呼出契約は有効だが、MITMフックの契約違反がある。 |  | ? |
| ACNL-F0030 | F-152: commit中の `TextBox_Draw` wrapper再入は不可 — `HIGH`（static＋実機例外） | F-151のdescriptorを渡してcommit hookから `TextBox_Draw (0x73CF48)` を呼ぶ試行は、 | HIGH | ? |
| ACNL-F0031 | F-153: direct-emitter patch generator 監査 — `MEDIUM`（独立の静的照合） | `PATCHES/cave_ui_picture_clone.py` の `MODE=audit` はゲームメモリを書き換えず、生成された | MEDIUM | ? |
| ACNL-F0032 | F-154: TextBox emitter直呼びも live DrawContext を二重更新する — `HIGH`（静的＋同一例外の再現） | F-153を通過したdirect-emitter版（`TextBox_EmitBatchToGpuCommands=0x4B7CE0`）は、wrapperを | HIGH | ? |
| ACNL-F0054 | F-16 v1 の 3x3 ケーブがクラッシュした原因 — バグの存在は `HIGH` / 因果は `MEDIUM` | **原因A（コード上は確定）**: テールジャンプ前に R0-R3 を復元していなかった。 | HIGH | ? |
| ACNL-F0055 | F-17 コードケーブとして使える範囲 — `HIGH` | `Shovel_DecideState` (`0x662E68`-`0x663450`) 内で、パッチ `0x663294 = EA000028` | HIGH | ? |
| ACNL-F0058 | F-20 【訂正】滞留の原因は PUSH 後のスタック引数のずれ — `HIGH` | **当初「滞留 4 件は `0x598688` 由来ではない」と結論したが、これは誤り。** | HIGH | ? |
| ACNL-F0064 | F-26 【成功】直接書き込み方式で隣マスに穴が空いた — `HIGH` | 状態機械・レコードを一切通さず、隣マスのアイテムを直接書き換える。 | HIGH | ? |
| ACNL-F0069 | F-31 【完成】隣マス掘りが中心マスと完全同期 — `HIGH` | 3 箇所のフックで、穴・抉れ・土しぶきのすべてが中心マスと同じタイミングで出る。 | HIGH | ? |
| ACNL-F0070 | F-32 CTRPF の空ページ `0x01E81000` は実行可能 — `HIGH` | CTRPluginFramework が起動時に確保する空メモリページ。 | HIGH | ? |
| ACNL-F0072 | F-34 【完成】3x3 マス掘り — `HIGH` | 周囲 8 マスに穴・抉れパーティクル・土しぶきパーティクルが、 | HIGH | ? |
| ACNL-F0076 | F-38 「揺すると木を切る」パッチと通常経路 — `HIGH` | `Player_BeginFieldObjAction` (`0x595A8C`) の mode 分岐: | HIGH | ? |
| ACNL-F0077 | F-39 【危険】レコード枯渇で範囲外書き込み → SIGSEGV — `HIGH` | セッション4 で**実際にクラッシュした**（`got SIGSEGV signal, exc.code b`）。 | HIGH | ? |
| ACNL-F0080 | F-42 【完成】木にぶつかって切り倒す — `HIGH` | 実機で確認済み。**パッチは 1 つも当てず、フック 1 箇所だけで完結する。** | HIGH | ? |
| ACNL-F0084 | F-46 実機イメージ `code_runtime.bin` を吸い出した — `HIGH` | `dump_code.py` で実行中プロセスから吸い出した。**`NCCH/exefs/code_runtime.bin`、10,485,760 バイト。** | HIGH | ? |
| ACNL-F0086 | F-48 静的 IDB を idalib-mcp で常用する — `HIGH` | `code_runtime.bin` (F-46) を **最小の ARM ELF ヘッダで包んで** idalib-mcp に読ませた。 | HIGH | ? |
| ACNL-F0090 | F-52 静的解析の本体を `code.bin.i64` に移した — `HIGH` | ユーザーが持ち込んだ `code.bin.idb`（IDA が `code.bin.i64` へ自動アップグレード）を | HIGH | ? |
| ACNL-F0091 | F-53 RTTI から全クラス名をデマングルして命名した — `HIGH` | `code.bin.i64`（セッション `acnl_code`）に **クラス 2,895 件・名前 5,481 件**を入れた。 | HIGH | ? |
| ACNL-F0092 | F-54 CTRPF プラグインの地域別アドレス表 — 本ビルドは **JPN 無印** — `HIGH` | `REFERENCES/CTRPF PROJECTS/Vapecord-ACNL-Plugin-master` の解析。 | HIGH | ? |
| ACNL-F0096 | F-58 【訂正】FOXXY はゲーム本来の日付変更ウィンドウを開いていた — `HIGH` | F-57 で「FOXXY にはゲーム内 UI を開く経路は無い」と書いたが**誤り。** | HIGH | ? |
| ACNL-F0097 | F-59 FOXXY 時間変更チートの残り 2 パッチ — 演出をメニュー姿勢に差し替えている — `HIGH` | F-58 で未解析だった `0x6563A8` と `0x670A48` を解明した。 | HIGH | ? |
| ACNL-F0102 | F-64: FOXXY の `pseudoType0x21` と、FOXXY 用 USA→JPN 変換 | confidence: **HIGH**（仕組みとアドレス対応）/ **LOW**（画面上の見た目） | HIGH | ? |
| ACNL-F0110 | F-72: `0x6D6338` はカタログ起動確認点として正しいが、持ち物全体の置換点としては遅すぎる | confidence: **HIGH**（実機画面結果、実行時オブジェクト、`code.bin.i64` のstock初期化/終了経路を照合） | HIGH | ? |
| ACNL-F0111 | F-73: 通常Xのfield側入口は `sub_165B40 -> sub_5C1F08`。診断traceのPC相対LDR移設は不可 | confidence: **HIGH**（実機のLR・trace buffer・SIGSEGV時レジスタと `code.bin.i64` を照合） | HIGH | ? |
| ACNL-F0113 | F-75: 「メニュー切り替え」enter入口なら持ち物UI初期化前に差替えられる | confidence: **HIGH**（状態記述子・関数入口・命令を `code.bin.i64` と実機で照合）、 | HIGH | ? |
| ACNL-F0114 | F-76: stock「メニュー終了まで待機」はcatalog終了の橋渡し候補 | confidence: **HIGH**（状態recordとupdate処理を `code.bin.i64` で確認）、 | HIGH | ? |
| ACNL-F0125 | F-87: room 0の38-bank late allocationがphase 1即時失敗の最有力。容量1版を準備 | confidence: **MEDIUM**（create/destroy経路と確保量は静的確定、容量1版の実機結果は未確認） | MEDIUM | ? |
| ACNL-F0126 | F-88: phase 1公開中にstock previewへ戻るとtype `0xBC`を早期生成してSIGSEGVになる | confidence: **HIGH**（例外PC・全register・stack・actor/manager memoryと静的呼出し経路を照合） | HIGH | ? |
| ACNL-F0129 | F-91: `1UPキノコ` はfamily 3/type `0xBD`でも同じvptr+8 crash。preview特殊type全域を基底化 | confidence: **HIGH**（例外register/stack、ItemParam record、family table、復旧create、実機patch読戻しを照合） | HIGH | ? |
| ACNL-F0139 | F-101: CLAUDE.md 準拠での再精査 — confidence の系統的誤り | confidence: **MEDIUM**（本項自体も静的解析のみ） | MEDIUM | ? |
| ACNL-F0143 | F-105: ★MCP 側から Suspend できる（CLAUDE.md の記述を訂正） | confidence: **HIGH**（実機で制御実験） | HIGH | ? |
| ACNL-F0148 | F-110: ★`Use stepping support` を OFF にしても、ヒットした bp の削除は必要（TODO-54 完了） | confidence: **HIGH**（実機で対照実験。ユーザーの目視確認つき） | HIGH | ? |
| ACNL-F0154 | F-116: ★★TODO-75 第1段達成 — シーンへノードを追加できた。あわせて Suspend の条件を確定 | confidence: **HIGH**（実機。対照実験つき） | HIGH | ? |
| ACNL-F0155 | F-117: ★TODO-79 完了 — `DUP=True` はハングしなかった。F-116 の「ハングの疑い」は誤り | confidence: **HIGH**（実機。ベースラインとの対照実験） | HIGH | ? |
| ACNL-F0156 | F-118: ★★注入した描画が画面に出ることを視覚的に確認。影は「アルファのみ」 | > **【後日訂正】本項 §3 の「重ねがけが濃くならないのは深度テストで落ちるから」という | HIGH | ? |
| ACNL-F0157 | F-119: ★★TODO-80 完了 — 自前の `g3d::FuncNode` を生成し、毎フレーム呼ばせることに成功 | confidence: **HIGH**（実機。生成物の型・コールバック回数を直接確認） | HIGH | ? |
| ACNL-F0158 | F-120: ★★★TODO-81 達成 — 自前の `FuncNode` から実際に画面へ描画できた | confidence: **HIGH**（実機。ユーザーの目視による決定的な A/B） | HIGH | ? |
| ACNL-F0164 | F-126: ★★★TODO-94 達成 — UI 層（`nw::lyt::TextBox`）に自前の 2D テキストを出した | confidence: **HIGH**（実機。住民名が `あんこ` → `テスト` に変わることを目視確認） | HIGH | ? |
| ACNL-F0176 | F-138: ida-pro-mcp の実機接続経路を復旧・検証 — `HIGH` | IDA GUI の Remote GDB 接続や RPC 自体が壊れていたのではなく、Codex のMCP設定から | HIGH | ? |
| ACNL-F0184 | F-158: ★★自前の変換行列でテキストを任意位置に描けた — `HIGH`（静的導出＋実機で視認） | 住民名 `T_nam_00` の **赤い複製が、元の緑の名前から右へずれた位置に描かれた。** | HIGH | ? |
| ACNL-F0188 | F-162: ★★★「好きな位置に好きなテキストを好きな色で」が通った — `HIGH`（実機で視認＋メモリで確認） | 会話ウィンドウの住民名を対象に、画面上に **4 つの「テスト」**が出た。 | HIGH | ? |
| ACNL-F0192 | F-166: ★★★GPU 可視性を証明した。ゲームのアロケータから GPU が読めるメモリを得られる — `HIGH`（実機で視認） | `g_GfxAllocator` から確保したバッファを **GPU が実際に読んだ。** | HIGH | ? |
| ACNL-F0194 | F-168: ★★★任意の大きさの四角形を描けた。TODO-119 達成 — `HIGH`（実機で視認） | 適用: `PATCHES/cave_own_quad.py` | HIGH | ? |
| ACNL-F0195 | F-169: ★★★自前テクスチャを自前サイズの四角形に貼れた。TODO-120 達成 — `HIGH`（実機で視認） | 適用: `PATCHES/cave_own_texture.py` | HIGH | ? |
| ACNL-F0198 | F-172: ★★★TextBox に依らない発行点を特定。答えは自分の記録の中にあった — `HIGH`（静的＋実機で前提を確認） | 「UI が何も出ていない状態では、CTRPF を含めどんな方法でも自前 GUI は不可能か」 | HIGH | ? |
| ACNL-F0199 | F-173: 発行点への注入は成功したが GPU が固まった。捕獲した列は自己完結していない — `HIGH`（実機、フリーズ） | 適用: `PATCHES/cave_replay_draw.py` | HIGH | ? |
| ACNL-F0200 | F-174: 発行点への注入は確立したが、GPU 状態の再現は現実的でない。方針を変えるべき — `HIGH`（実機で反復検証） | 適用: `PATCHES/cave_replay_draw.py`、`scratchpad/dump_frame_cmdlist.py`、 | HIGH | ? |
| ACNL-F0205 | F-179: Vapecord のマップ上プレイヤー表示は OSD（フレームバッファ直描き）だった — `HIGH`（ソース確認） | 出典: `REFERENCES/CTRPF PROJECTS/Vapecord-ACNL-Plugin-master/src/features/PlayerCodes/PlayerCodes.cpp` | HIGH | ? |
| ACNL-F0206 | F-180: ★★★UI 画像を「足す」ことに成功。TODO-122 の主要部達成 — `HIGH`（実機で視認） | 適用: `PATCHES/cave_add_quad.py` | HIGH | ? |
| ACNL-F0208 | F-182: 追加した UI 画像を絶対座標で置けた。複製元は地図の影 — `HIGH`（実機で A/B） | 適用: `PATCHES/cave_add_sprite.py` | HIGH | ? |
| ACNL-F0215 | F-190: ★★★★色・位置・大きさの完全制御を達成。詰まっていた原因は**アンカー** — `HIGH`（実機） | `PATCHES/cave_add_sprite2.py`（色つきバッチに相乗り）。 | HIGH | ? |
| ACNL-F0216 | F-191: ★★★★自前テクスチャの適用に成功。欠けていたのは `reg 0x083` — `HIGH`（実機） | `PATCHES/cave_add_sprite2.py`（`EMIT_TEX = True`）。 | HIGH | ? |
| ACNL-F0220 | F-195: ★★★★★自前ビットマップフォントで文字列を描画。描画順も制御 — `HIGH`（実機） | `PATCHES/cave_draw_sprites.py`。**「ACNL が地図の上に表示され、読めました」**（ユーザー確認）。 | HIGH | ? |
| ACNL-F0221 | F-196: ★★★★フルカラー画像（RGBA8）の表示を確定 — `HIGH`（実機） | 64x64 の RGBA8 テスト画像を自前バッファに置き、120x120 で表示した。 | HIGH | ? |
| ACNL-F0234 | F-209: ★★★★★TODO-131 完了。自前 GUI が常に最前面に描かれる — `HIGH`（実機） | `PATCHES/cave_draw_topmost.py`。フックは 4 つ。 | HIGH | ? |
| ACNL-F0235 | F-210: ★★★★★狙う相手をリスト id で固定してはいけない。実行時に追いかける — `HIGH`（実機） | START のセーブ確認メッセージウィンドウを出すと、自前スプライトが消えた。 | HIGH | ? |
| ACNL-F0238 | F-213: ★★★★CTRPF プラグインへの移植 — ケーブは書き直さずバイト列ごと移す — `HIGH`（ビルド済み・実機未検証） | `Plugin/CTRPluginFramework-BlankTemplate-0.8.0/Sources/OwnGui.cpp`。 | HIGH | ? |
| ACNL-F0242 | F-217: ★★★★SD から任意の画像を読む（TODO-130 完了）— `HIGH`（実機） | 3DS の GPU は **8x8 タイル + Morton 順**で、幅・高さは 2 の冪しか読めない。 | HIGH | ? |
| ACNL-F0244 | F-219: ★★★CTRPF のファイルパスはプラグインのフォルダ基準。ON が早すぎると落ちる — `HIGH`（実機） | `.acgx` を SD に置いてプラグインを ON にしても「ACNL GUI OK」のままだった。 | HIGH | ? |
| ACNL-F0245 | F-220: ★★★TODO-134 段 B 完成 — 上下画面の描き分けとチャンク別の色 — `HIGH`（実機） | 自前チートメニュー（TODO-134）の描画基盤。実機で確認済み。 | HIGH | ? |
| ACNL-F0247 | F-222: ★★★★★自前チートメニューが実機で動いた。ゲームは止まらない — `HIGH`（実機） | TODO-134 の目的そのもの。**メニューを開いている間もゲームが進行する。** | HIGH | ? |
| ACNL-F0250 | F-225: ★★★★「開いている間だけ描く」にすると、閉じても最後の絵が残り続ける — `HIGH`（実機） | ユーザー報告: | HIGH | ? |
| ACNL-F0254 | F-229: ★★★ケーブどうしの重なりは目視では見つからない。機械的に検査する — `HIGH`（実機） | ``` | HIGH | ? |
| ACNL-F0260 | F-235: `Frame_EndDrawPass1024` 主リスト末尾の手製 Drawer-state 版は安全な提出経路ではない — `MEDIUM`（静的＋実機失敗） | `PATCHES/cave_tail_sprite.py` は `0x5A27C8` で、捕獲済み material と inline Drawer を用いて | MEDIUM | ? |
| ACNL-F0263 | F-237: Layout の再生順は `LayoutList_SetDisplay` で局所的に制御できる — `MEDIUM`（静的＋実機 no-draw） | `REFERENCES/TEXTS/render.txt` の gokiro 氏は、描画コマンド追加・再生順変更・コマンド | MEDIUM | ? |
| ACNL-F0281 | F-258: 作業配列を自前バッファへ差し替える案は失敗した — `HIGH`（実機・目視） | > **★F-263 で理由が判明した。** 作業配列は 4 本（`+1640/1644/1648/1652`）あり、 | HIGH | ? |
| ACNL-F0283 | F-260: F-259 の設計を実装し、IDA の逆アセンブルで検証した（実機未適用） — `HIGH`（静的のみ） | `PATCHES/cave_node_record.py`。`cave_node_draw.py` を複製し、F-259 の設計を載せた。 | HIGH | ? |
| ACNL-F0285 | F-262: 再生の複製経路を逆アセンブルで裏取りし、実装の誤り 2 件を追加で直した — `HIGH`（静的のみ） | `GpuCmd_ReplayRecordedListRange` の `if (a7)` 側（`0x7B0E08`〜）を逆アセンブルした。 | HIGH | ? |
| ACNL-F0290 | F-267: 雛形の複製を廃止した。写し元依存が実装から消えた — `HIGH`（静的のみ） | F-259 の実装は、本物の Layout から `+0x28` の 20 語（`0x50` バイト）を写して雛形にしていた。 | HIGH | ? |
| ACNL-F0292 | F-269: TEV を自前で組んだ。**設計から借り物が消えた** — `HIGH`（静的のみ） | F-268 でマテリアルのテンプレートの符号化が全部割れたので、 | HIGH | ? |
| ACNL-F0295 | F-272: F-264〜F-271 の整合監査。独立な結果と突き合わせて 1 件の誤りを訂正し、`SET_PROJECTION` を廃止した — `HIGH` | 新しい結論が既存の独立した結果と矛盾しないかを、6 点について確かめた。 | HIGH | ? |
| ACNL-F0296 | `SET_PROJECTION` を廃止した | 上の 3 番で、**ビューポートは各パスが `RecordChildren` の後・`SetDisplay`（replay）の前に |  | ? |
| ACNL-F0297 | F-273: ★★★★★致命的なバグ。記録スロットのエピローグが `R4` = drawctx のまま `Commit` していた — `HIGH`（静的のみ・未適用） | F-267 の教訓「生成器を変えたらケーブ 1 本を丸ごと IDA に通す」に従って | HIGH | ? |
| ACNL-F0302 | リテラル参照の値まで検証する道具を追加した | `PATCHES/verify_literals.py`。`audit_node_cave.py` は |  | ? |
| ACNL-F0304 | F-279: 検証道具を全ケーブに広げ、死語を 1 本落とした — `HIGH` | `build_v` / `build_pass` / `build_t` は生の語列を返すので、 | HIGH | ? |
| ACNL-F0305 | F-280: ★★★★★メニューを実際に描けるところまで実装した（フォント・レイアウト API・領域拡張） — `HIGH`（静的のみ・未適用） | これまで描いていた「ACNL GUI OK」は**デモ**であって、メニューには足りなかった。 | HIGH | ? |
| ACNL-F0307 | F-282: CTRPF プラグインへ移植した。**ビルド環境なしで移植の正しさを照合できる** — `HIGH`（静的のみ・未ビルド） | `Plugin/CTRPluginFramework-BlankTemplate-0.8.0` の描画まわりを全部書き直した。 | HIGH | ? |
| ACNL-F0308 | F-283: シミュレータ相当の UI へ作り直した（美咲フォント・アニメーション・項目型）— `HIGH`（ビルド済み・未適用） | 利用者の指摘 3 点に対応し、`Plugin/CTRPF-GUI-Simulator` の設計を C++ へ写した。 | HIGH | ? |
| ACNL-F0309 | F-284 (HIGH) — 自前 GUI（F-283 版）のクラッシュ `PC=0x839004` は「.text のゼロ埋めを NOP スライドして飛び出した」結果 | **根拠**（静的。`idalib-mcp` / `code.bin.i64`） | HIGH | ? |
| ACNL-F0310 | F-286 — F-283 / F-285 を捨てて **F-282（実機で描画に成功した版）へ巻き戻した** — `HIGH`（静的検証済み・実機未確認） | 実機で描画に成功した CTRPF プラグインの最後の版は **F-282**（利用者報告 | HIGH | ? |
| ACNL-F0320 | F-296 (HIGH・実機) — ★借りた領域を返せる。**確保 → 解放 → 再確保の往復を実機で成立** | F-295 で `nw::lyt` のヒープから 64KB 借りたが、**返す手段が無かった**。 | HIGH | ? |
| ACNL-F0322 | F-298 (HIGH・静的のみ) — ★TextBox 方式は実装可能。**自前フォントの「コード」はほぼ要らない** | 利用者の指示で、基準仕様を詰める前に TextBox 方式の実現性を静的に判定した。 | HIGH | ? |
| ACNL-F0327 | F-303 (HIGH・実機) — ★借りた nw::lyt ヒープは **GPU 可視**。自前フォント資源の設計を確定（描画は未達） | これまでアトラスは `g_GfxAllocator`（`*(0x0094CA30)`）から `0x4000` 借りていた（F-166 / F-221）。 | HIGH | ? |
| ACNL-F0331 | F-307 (HIGH) — ★基準仕様 v2 を改訂し、**仕様書そのものを機械で検証**した | 制定時（2026-09-05）の §3 は「文字だけ v1 のスプライト表 + 自前ケーブ（`CAVE_TXT`）」だった。 | HIGH | ? |
| ACNL-F0335 | F-311: プラグインを基準仕様 v2 へ書き換えた（3gx 名 = gohan）— 実機未検証 | > 対象: `Plugin/CTRPluginFramework-BlankTemplate-0.8.0` |  | ? |
| ACNL-F0345 | F-318: F-317 の削除を実装。実機で **132,192 B が丸ごと戻った** — HIGH | ``` | HIGH | ? |
| ACNL-F0347 | F-320（2026-09-06）: クラッシュダンプの読み方と `threadCreate` の落とし穴 | **confidence: HIGH**（ダンプの実値 + `gohan.elf` の逆アセンブル） | HIGH | ? |
| ACNL-F0349 | F-323（2026-09-07）: パネルの縁がフェード途中で濃く残る（A案で修正） | **confidence: MEDIUM**（静的根拠 + 検証器 + プレビュー + ビルド。**実機の目視は未確認**） | MEDIUM | ? |
| ACNL-F0350 | F-324（2026-09-07）: リストボックスの背景が後ろの行文字より後ろだった | **confidence: MEDIUM**（静的根拠 + 検証器 + プレビュー + ビルド。**実機の目視は未確認**） | MEDIUM | ? |
| ACNL-F0351 | F-325（2026-09-07）: 段 6（上下リストボックス/ホットキー）・段 7（通知）を実装 | **confidence: MEDIUM**（静的根拠 + 検証器 2 種 0 件 + プレビュー + ビルド。 | MEDIUM | ? |
| ACNL-F0352 | F-326（2026-09-07）: 実機報告の不具合1件と要望 R1〜R5 | **confidence: MEDIUM**（検証器 2 種 0 件 + プレビュー + ビルド。 | MEDIUM | ? |
| ACNL-F0353 | F-327（2026-09-07）: 要望 R6a（縁も赤に）・R6b（適用時の通知を両方抑制） | **confidence: MEDIUM**（検証器 2 種 0 件 + プレビュー + ビルド。 | MEDIUM | ? |
| ACNL-F0354 | F-329（2026-09-07）: 通知題の統一とホットキー・トグルの復帰 | **confidence: MEDIUM**（検証器 2 種 0 件 + ビルド。 | MEDIUM | ? |
| ACNL-F0355 | F-328（2026-09-07）: 関数側連携の窓口（トグル実行は利用者が持つ） | **confidence: MEDIUM**（検証器 2 種 0 件 + ビルド。**実機の目視は未確認**。 | MEDIUM | ? |
| ACNL-F0356 | F-330（2026-09-07）: OFF 通知の縁を帯より暗い赤に | 利用者の指摘：OFF の縁が帯と同じ赤だった。ON は帯（`#63e4a4`）より |  | ? |
| ACNL-F0357 | F-332（2026-09-07）: メニュー側のトグルをやめる | 利用者の指摘：無効なのにホットキーで有効無効が動く。設計は |  | ? |
| ACNL-F0358 | F-333（2026-09-07）: トグル実行エンジン（壁抜け仕様の一般化） | 利用者の壁抜け例をそのまま一般化した設計。直接指示の書き換え許可あり。 |  | ? |
| ACNL-F0359 | F-331（2026-09-07）: トグル実行のライフサイクル連携 | 利用者の設計：ホットキーで ON/OFF を切り替えるとトグル式の有効無効も |  | ? |
| ACNL-F0360 | F-334（2026-09-07）: 効果の実体を関数登録に直す | 利用者の指摘：`RegisterToggleEffect` という名前にアドレスや有効値を |  | ? |
| ACNL-F0361 | F-335（2026-09-07）: 複数パッチ切替と押し続け移動の再設計 | 利用者の壁抜け（複数アドレス×複数値）・座標移動（ホットキー＋押下方向へ |  | ? |
| ACNL-F0362 | F-336（2026-09-07）: 試験2項目へ効果配線（通知確認用） | 利用者の要望：テスト用の無敵モード・壁抜けに通知を入れること。 |  | ? |
| ACNL-F0368 | F-342（2026-09-07）: 共有バッチの設計 — ★費用の 8 割は「コマンド語の器の取りすぎ」 | **confidence: HIGH**（静的解析 + 実機で確認。設計の数字は `PATCHES/design_shared_batch.py`） | HIGH | ? |
| ACNL-F0369 | F-343（2026-09-07）: 空いた容量で通知を Simulator と同じ 7 件にした | **confidence: HIGH**（検証器 8 群が異常 0 件 / ビルド成功。★実機での目視はこれから） | HIGH | ? |
| ACNL-F0372 | F-346（2026-09-07）: ★アトラス以外をプラグインの `.bss` へ移した（借用 442,368 -> 36,864 B） | **confidence: HIGH**（検証器 8 群 異常 0 件 / ビルド成功 / **実機で確認済み**） | HIGH | ? |
| ACNL-F0373 | F-347（2026-09-07）: キーボード UI を足したときの見積もり（実装前の机上計算） | **confidence: MEDIUM**（`CTRPF-GUI-Simulator` のソースから数えた実数 + F-341 の費用式。**未実装**） | MEDIUM | ? |
| ACNL-F0374 | F-348（2026-09-07）: 基準仕様 v3 を制定した | **confidence: HIGH**（`verify_spec_v3.py` 8 群 異常 0 件） | HIGH | ? |
| ACNL-F0375 | F-349（2026-09-07）: Simulatorの文字・数値キーボードをCTRPFへ移植 | **confidence: MEDIUM（ソース照合とホスト試験。実機未確認）**。 | MEDIUM | ? |
| ACNL-F0377 | F-351（2026-09-07）: 入力遮断をプラグインへ実装し、下画面ロックへ一本化した | **confidence: HIGH（実機で機構を確認）/ MEDIUM（プラグイン版は実機未確認）** | HIGH | ? |
| ACNL-F0385 | F-359: 内蔵漢字変換候補取得の目的・共有辞書候補・ゲーム内APT起動経路（2026-09-08） | 調査目的は3DS本体内蔵のかな→漢字変換辞書・変換候補の取得。 | LOW | ? |
| ACNL-F0392 | F-365（2026-09-08）: メニューON/OFF でホットキー判定を送る（opt-in） | 利用者の要求：ホットキーが無いときにチートが ON/OFF されたら、 | MEDIUM | ? |
| ACNL-F0393 | F-366（2026-09-08）: しずえスキップをトグル式チートとして取込 | `DOCS/skip_isabelle.md`（F-361。実機で成功済み）を常設化。 | MEDIUM | ? |
| ACNL-F0394 | F-367（2026-09-08）: しずえスキップ取込後のクラッシュ切り分け（静的監査まで） | 利用者の報告： 新しい 3gx（F-366 取込版）でクラッシュした。 |  | ? |
| ACNL-F0398 | F-371（2026-09-08）: 訂正 pitch—項目OFF・発火なしでも落ちる | 利用者の訂正： 現在の停止は**チートON＋項目OFF**での遷移中のもの。 |  | ? |
| ACNL-F0399 | F-372（2026-09-08）: E1—素では落ちない。チートON状態に絞られた | 再起動直後（チートOFF）でタイトル→しずえ遷移。実機値： |  | ? |
| ACNL-F0400 | F-373（2026-09-08）: ON直後クラッシュ。無罪のものとフック抜きビルド | 利用者の申告： チートONの瞬間にクラッシュ（項目は触っていない）。 |  | ? |
| ACNL-F0401 | F-374（2026-09-08）: タイトルON直後の停止はフォールトではない＋描画系照合の途中経過 | 利用者の申告： タイトル画面で自前メニューONにしただけで動かなくなった。 |  | ? |
| ACNL-F0403 | F-376（2026-09-08）: A1/A2 抜き診断ビルド（遷移クラッシュの切り分け用） | F-375 修正後も切り分け中のため、変数を 1 つずつ潰す診断ビルド。 |  | ? |
| ACNL-F0404 | F-377（2026-09-08）: クラッシュダンプ解読＋対象走行中 | 利用者が `Plugin/crash_dump_00000003.dmp` (604 B) を配置。 |  | ? |
| ACNL-F0405 | F-378（2026-09-08）: 実行構成がどのビルドとも一致しない | 実機値（チートON・メニューOPEN・タイトル待機・正常待機PC）： |  | ? |
| ACNL-F0406 | F-379（2026-09-08）: 訂正 — 謎の構成は自前の診断フラグだった | F-378 を撤回する。A1/A2 素＋shizueフック入り＋入力入り＋メニュー起動中は、 |  | ? |
| ACNL-F0407 | F-380（2026-09-08）: タイトルON後は正常動作。スレッド特定も確定 | 利用者の申告： 現行 3gx では ON だけでは落ちない。 |  | ? |
| ACNL-F0408 | F-381（2026-09-08）: 診断フラグを戻しフルビルドへ。メニュー非表示の説明 | 利用者の指摘の通り、`kDiagNoHooks=true` の間は A1/A2 を入れないため |  | ? |
| ACNL-F0415 | F-390: 破損した3gxをしずえスキップ統合前へ復元（2026-09-09） | **ソースと成果物の復元はHIGH、実機表示の再確認は未実施。** |  | ? |
| ACNL-F0416 | hidden letterの入場座標とCHEATS選択肢（2026-10-14） | GPT-6/idalib、MEDIUM。LetterDragWindowBase_AttachToPane 0x31F2B8はroot+632をparent+976/N_pos_ltrへ繋ぐ。Pane_CalculateMtxはvisible0かつDrawInfo+136 bit2なしなら子も計算しない。原ARM probe/製品FrameStepで、親を入場位置へ移しても[-560,-80,0]に残留し、force bit4で[150,-80,0]へ更新/visible0保 | MEDIUM | ? |
| ACNL-F0417 | T015の再実機訂正（2026-10-13） | GPT-6/idalib、MEDIUM。pocket singleton0x9499ECをLoadStep/Disposeと原STRで照合。screen list先頭だけの取得を修正。trash cleanupはsource有効又はtarget drag可を音条件とするため、消去icon更新/非drag trashの組合せでは音が抑制される。成功時一度明示再生する。 | MEDIUM | ? |
| ACNL-F0418 | UI入口・pocket再入場・非drag trash・青選択（2026-10-13） | GPT-6/idalib、MEDIUM（原JPN ARM＋caller/vtable/source、PC/実機訂正）。通常ActivateSelectedにcheckboxlist入口が無い。既存inline編集/描画へ分岐を追加。manual closet3cheat/Wire/configを削除、chat検索closetは保持。 | MEDIUM | ? |
| ACNL-F0421 | widget画像の参照寿命とcloset帰還・page待ち（2026-10-12） | 2026-10-13追加: 原hand/touch controlは+216 counter/+220 threshold、初回11/連続3を確認。node112/152が決定アニメ。owned pageは待機を省いて親1C38A0を同Calcで完了。退場はchild outer996/pocket1988の終端→元unbind/状態移行→Actor_RequestDestroy。キーボタン解放をchat入場条件にせず、held入力だけ暫定遮断。NativeEngine::L | MEDIUM | ? |
| ACNL-F0422 | closet直通とnative転送・低ID/ウィジェット（2026-10-12） | 最終DB監査: 0x4DD030/0x4DD4A4は原数量merge/predicateとして原ARMと実行検査から2rename追加。周辺9注記も追加し合計9name/26注記、未知のlookup全ABI/choice PMF・数量action/stack第5引数は理由と次の照合をDBへ記し推測renameしない。製品不変、根拠db_peripheral_changes.json・更新XML読戻し。 | MEDIUM | ? |
| ACNL-F0424 | nativeクローゼットとmenu intrusive node（2026-10-12） | IDA（idalib）/GPT-6、MEDIUM。更新SHA c635af8f.../ARM11/ARM32LE/imagebase0/主要10地点T=0を確認。原code.binのARMとRTTI/生table/ctor/索引consumerを独立照合。BsMenuChestは38708B、actualprimary0x8E5BB0（旧Explorer0x8E5BA8はheader）/25method。通常child ChangeStockItemは15528B、prima | MEDIUM | ? |
| ACNL-F0425 | F005のHHD引継ぎ要件を訂正（2026-10-12） | 利用者実機報告: fix2/SHAe2afb75a...のリストは修復、hairは未修復。HHD自身が退場/待機を所有し、コマンドは直接呼ぶよう指定。native chat lifetimeの観察は変更しないが、「style起動前に親/kbd消滅必須」「早期Showが不具合」の推論を撤回する。F005/T007のCPU試験を実機修復の証拠としない。 |  | ? |
| ACNL-F0426 | Controller画素座標/vtableとchat画面引継ぎ（2026-10-12） | GPT-6 / IDA（idalib）、MEDIUM。更新SHA/ARM/imagebase/Tを確認しproducer540870/542D78/542E88とconsumer74F3FC/73BAC0/Matrix/Paneの独立ARM経路・旧input資料/sourceで照合。Controller+276/+280は画素float、TouchState+32/+36とは異なる。F004中心座標注記は撤回。53CDC4のvtable+24 BLXから+0はvtable、t | MEDIUM | ? |
| ACNL-F0429 | gohanへのidle/気絶/消失抑制・チャット移植（2026-10-11） | 2026-10-12修正T003: 利用者のMapEditor入力不能報告を旧実Start/HoldField/Present/Wantedで再現。Presentはfield非Shownも含み、actionの退場gateが自身のHoldFieldで継続Tickを止めていた。Running前だけ待つことで新実Tickの移動/touch/game入力遮断が全true。ChatCommandsはcheckbox適用値で有効化し、hotkeyでnative Wait前に原文captu |  | ? |
| ACNL-F0431 | 全収録チートの意味コメント調査（2026-10-11、利用者指示で中断） | 最新の訂正を受け、コードの一般説明をゲーム内の意味に改める。全2700関数の原資料/notes/calls/operandをcatalogへ記録、全project_v2の対応資料をhash付き検索索引化済み（materials.json、抽出エラー0）。未対応binary/IDA内部形式の全読了とはしない。同一資料のコピーは独立証拠に数えない。 |  | ? |
| ACNL-F0432 | 整理済みチートの挙動保持リファクタリング（2026-10-11） | 解析/検証: Tree-sitter・GNU C++ / gpt-6。元IDA-gpt-6.1-sol-F018と追加TreeSitter-gpt-6-F001の帰属を保持。対象は2700既存関数のみ、新規JOKER/他CTRPF整理は中断。共有設定familyの1関数化は利用者の訂正で撤回。 |  | ? |
| ACNL-F0433 | C++由来107チート本体の局所化と部分集合の実出力照合（2026-10-10） | 2026-10-11 CHEATSのみの追補: message(5).cppは施設状態変更8callbackと8tableを含み、原型CHARS_U8_MAP/items宣言は欠ける。原range-forのiは局所変数なのに旧scoped閉包が別drop.cppのiへ束縛していたため、CHEATS専用contractで原AST/range declarator/table/Write8と字面以外の束縛を照合し当該偽依存を除外。局所u8 id/const char*nameとv | MEDIUM | ? |
| ACNL-F0434 | チップ長押しのstatic記録拒否と選択アニメ再開始（2026-10-10、MEDIUM） | 解析ソフトIDA（idalib-mcp）/解析モデルgpt-6.1-sol。F016配布で利用者が「窓未表示/縞アニメ振動」を実機報告。修正版はPC検査のみ、実機未確認。日本語無印ACNL＋更新、main SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb、ModuleFtr.cro SHA d2a65c85909782a66a5300df7f26f76289db69f7474f563d59 | MEDIUM | A |
| ACNL-F0435 | Editorキャッシュの再記録・チップ複製・内装保存/交換（2026-10-10、MEDIUM、実機未確認） | 追補F017: 長押し窓と縞アニメは利用者実機で不具合。F016のnative Select/取消/親整理stub検査はstatic記録とアニメgateを覆えていなかった。上記F017の原ARM再現/修正で補正。他F016項目の実機結果は未報告。 | MEDIUM | A |
| ACNL-F0436 | リスト背景のフェードと模様替えカメラpan（2026-10-10、MEDIUM、本体非表示はF016で訂正） | 解析ソフトIDA（idalib-mcp）/解析モデルgpt-6.1-sol。原SHA/ARM32 LE/imagebase/ロード範囲・独立した入口命令を確認し、実装前に[設計](../docs/topics/catalog_camera_controls_design.md)を保存。利用者が前版hhd_room_camera1を実機PASSと報告した後の追加要望。 | MEDIUM | A |
| ACNL-F0437 | HHD通常室内カメラの連続操作をACNLの家へ移植（2026-10-09、静的MEDIUM、2026-10-10利用者実機PASS） | 2026-10-10追記: 利用者は提示hhd_room_camera1を実機で確認し問題なしと報告。配布版SHA/sourceに対する確認として扱い、端末上のSHAや各個別ケースは再測定していない。F013同梱の確認待ちも解消。新F015追加の確認ではない。 |  | A |
| ACNL-F0438 | 外観に依存せず室内の壁配置・張替え機能を判定（2026-10-09、静的MEDIUM、2026-10-10利用者実機PASS） | 2026-10-10追記: F014同梱hhd_room_camera1について利用者が実機で問題なく動作と報告。提示版に対する確認として確認待ちを解消し、端末SHA/壁材質別の個別試験一覧は未再測定として扱う。 |  | A |
| ACNL-F0445 | アニメのフレームは実機で進んだ（適用段は IDA-opus-5-F013 で解決）（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。**自前資源のマテリアルアニメのフレームを実機で進めた。** | HIGH | ? |
| ACNL-F0465 | マップエディター第 2 段 — 真ん中のカーソルと A・実行範囲・薄いカーソル（UnitCursor の TEV 段 4 = アルファ × Constant4）（2026-09-29、MEDIUM: 資源の解析＋ホスト試験＋成果物の確認。gohan 実機未確認） | 解析ソフト: IDA（主 IDB）＋ romfs の UnitCursor.bcres / 解析モデル: opus-5.5。利用者指示（2026-09-28）: 盤面に触れていないときは真ん中に UnitCursor、A でモードの操作（FOXXY と同じ）。 | MEDIUM | S |
| ACNL-F0466 | メッセージのあと下画面にエディターが出ない — GameList が「隠した」と思い込んだまま、ゲームが戻した下画面をもう一度戻して止まる（2026-09-28、HIGH: 実機の値＋静的＋書き込みでの確認。経緯の一部は未確認） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的、実機を ida-pro-mcp で動的）/ 解析モデル: opus-5.5。利用者報告: 蚊に刺される等のあと、マップエディターの下画面が出なくなった（実機 Suspend 済み）。 | HIGH | S |
| ACNL-F0468 | マップエディターのスポイトモード（一覧 4 行・窓の拡張）、Y、モードごとの UnitCursor の色、下画面左上の箱、マスの色の手直し（2026-09-28、MEDIUM: 静的＋描画器＋ホスト試験。gohan 実機未確認） | 解析ソフト: IDA（主 IDB）＋ acnl-ui-designer の描画器 / 解析モデル: opus-5.5。利用者指示（5540abf の確認後）: 黄 → 青、真ん中を白（上下とも）、濃さ 50 で決定、 | MEDIUM | S |
| ACNL-F0469 | マップエディターのマスの色 — 上画面の単色の四角形（UnitCursor 資源の別の体）と盤面の 5x5 の輪郭（2026-09-28、MEDIUM: 既存の実機知見の組み合わせ＋描画器。gohan 実機未確認） | 解析ソフト: IDA（主 IDB）＋既存の実機知見 / 解析モデル: opus-5.5。利用者指示: 盤面の中心から 5x5 の輪郭のマスを真っ白に。上画面の 7x7 にマス単位の単色四角形 | MEDIUM | S |
| ACNL-F0470 | マップエディターの盤面を 9x9 へ（chip_room_00 の大きさの規則）と、L / R の音（2026-09-28、MEDIUM: 静的＋描画器。gohan 実機未確認） | 解析ソフト: IDA（主 IDB）＋ romfs の bclan / bclim ＋ acnl-ui-designer / 解析モデル: opus-5.5。利用者指示: 盤面を 9x9 に、真ん中のマスの背景を少し赤く。L / R でも一覧で選んだときの音。 | MEDIUM | S |
| ACNL-F0496 | プラグインから GPU 可視メモリを確保できた＝Luma の svcControlMemoryUnsafe で SYSTEM 領域から空き番地へ貼る（2026-09-25、HIGH: 実機 2 回＋Luma の公式ソース） | **★採用しない（2026-09-25、利用者の判断）**: 他の CFW・エミュレータで使えず、Old 3DS で通るかも分からないため、自前 GUI は従来のゲームのヒープ借用へ戻した | HIGH | S |
| ACNL-F0500 | 複製を画面に固定する方式＝再生直後の late pass で専用カメラ。Scene 1 に積む案は右目が壊れるので不可（2026-09-24、MEDIUM（静的＋別エージェントの実機成功の手順）。gohan 246865a は実機未確認） | **Scene 1 案を退けた理由（静的）**: `Render_DrawScene0 0x4F2334` と `Render_DrawScene1 0x4EA01C` は `byte_94CA2C` で排他（メニューが | MEDIUM | S |
| ACNL-F0501 | 複製を出したまま建物に入ると無限ロード＝管理役が枠の返却を待つ。枠は BankTable_Release で下ろしてから返す（2026-09-24、HIGH（静的＋実機 2 回）。直した gohan 0107a5b は利用者が実機で確認: 出したまま建物に出入りしても止まらない、入ったあと複製は消える、OFF→ON で問題なく再出現） | **利用者の実機確認（gohan fa33556）**: 右隣に完全な複製（装備も同じ）、髪型・髪色は複製だけに適用、OFF で消える。**出したまま建物に入ると無限ロード。** | HIGH | S |
| ACNL-F0508 | 半透明は描画層で後ろへ回し深度は書く／役場の旗とチケットマシン／もとから半透明の材質のアルファ／一枚絵の合成の調査（2026-09-24、HIGH（実機の比較画像）／MEDIUM（一枚絵は設計のみ）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼（実機 Suspend・役場の前、Chokistream 起動済み）。画像 `work/evidence/screens/layer_20260924/`。 | HIGH | S |
| ACNL-F0513 | 親ヒープ *(0x94CC48) の空きは 484 KB。UnitCursor とプレビューを並べると足りない／駅・役場のプレビュー名（2026-09-24、HIGH（実機の読み取り）／MEDIUM（名前、静的）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の報告「切り替えが重い・UnitCursor がすぐ消えた・無限ロードするモデルがある」、実機 Suspend 中に gohan の変数を読んだ。 | HIGH | S |
| ACNL-F0517 | 選んだ建物の青＋透明度の揺れ（gohan BuildingHighlight）が実機で動いた（2026-09-23、HIGH） | 解析ソフト: IDA / 解析モデル: opus-5.5。gohan `58701ac`（work/grid-cursor）。F011〜F013 の方法をプラグインへ移した。 | HIGH | S |
| ACNL-F0518 | 役場・リサイクルショップも集め方どおり全体が青。全段使用の材質は近似、モデルビューアは汎用の書き出し（2026-09-23、HIGH（役場・店）／MEDIUM（モデルビューア、静的）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「役場とリサイクルショップで確かめる」「使われている材質への対応」「モデルビューアの自前モデル」。 | HIGH | S |
| ACNL-F0533 | モデルの一覧は ROM から読める。8,818 本の .bcres とその検算（2026-09-22、HIGH、静的） | 解析ソフト: IDA / 解析モデル: opus-5。利用者の問い「ROMに名前群が存在する可能性はないですか？」への答え。 | HIGH | ? |
| ACNL-F0536 | グリッドカーソルが村の屋外で描けた。見えたものから分かったこと（2026-09-22、実機目視） | 解析ソフト: IDA / 解析モデル: opus-5。F031 の 2 つを直した gohan で、**利用者が実機で | HIGH | ? |
| ACNL-F0537 | gohan のグリッドカーソルが何も描かなかった2つの原因（2026-09-22、HIGH、実機の状態読み＋静的） | 解析ソフト: IDA / 解析モデル: opus-5。利用者の報告「チートをONにしても表示されません。大きさを200にしても | HIGH | ? |
| ACNL-F0538 | グリッドカーソルを gohan へ。起動時クラッシュの診断とケーブ衝突（2026-09-22、HIGH、静的＋クラッシュダンプ） | 解析ソフト: IDA / 解析モデル: opus-5。利用者の指示で、試験チートを**独立プラグインではなく | HIGH | ? |
| ACNL-F0541 | 同じモデル・アニメ12体の同時描画。実機で30.67fpsを維持し、submit先は溢れない（2026-09-21、HIGH、静的＋実機） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T010。 | HIGH | ? |
| ACNL-F0576 | 正常版と統合版の区別 | F394は利用者が描画復帰・しずえスキップを実機確認した復元基準。ソースはgohanのcommit `fa76dfc05bcc8b362829f53ce48b1593c4099a38`、復元成果物は `artifacts/plugins/f394_verified/`。重複バックアップはGitへ集約済み。 |  | ? |
| ACNL-F0577 | 旧プロジェクトの内部保存 | 旧原本・資料・キャッシュ32395ファイル、7271181421 bytesをコピー元とSHA-256照合して保存。 |  | ? |
| ACNL-F0578 | 自立化後の検証 | 構成監査と、親プロジェクトI/O・ネットワークを禁止した既存オフライン検証がPASS。ソース/core/FS、全字形、キーボード10943遷移・15描画場面、しずえ、frontend24ケース、元ARMとの5入力の候補順位、リンク済み命令を照合。gohan/ELFは不変、再ビルド・実機操作なし。根拠はwork/evidence/reorganization/のworkspace_audit.json・isolated_*.json・git_stage.json。Git履歴を保 |  | ? |
| ACNL-F0579 | gohan-gui-simulator のローカル版と公開版が双方向に食い違っていた（解消済み） | `src/CTRPF-GUI-Simulator`（ローカル）を削除し `yak9909/gohan-gui-simulator` の clone へ統一した際に判明。 |  | ? |
| ACNL-F0580 | Volta の shim が引数を改行で切り落とす（このPC全体の問題） | `node` の実体は `C:/Program Files/Volta/node.exe`（Volta 2.0.2 の shim）。 |  | ? |
| ACNL-F0581 | IDA9.3のGhidra XML Exporter導入・主IDB出力 | ローカルGhidra11.0.1の7xx版はIDA9のAPIに非対応。公式Ghidra12.1.3付属9xx版（Exporter 5.0.2）を原本のままユーザーIDAのpython/idaxml.pyとplugins/xml_exporter.pyへ配置。原本manifestと配置先SHAが一致する。IDA SDK930でplugin読み込み・XML出力を確認。 |  | ? |
| ACNL-F0586 | 下位 `0x0C` でgohanの壁抜けを相手へ強制できるか（2026-10-04、MEDIUM） | 解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。gohanの実機確認済み壁抜けは `AcPlayer_UpdatePositionWithFieldChecks 0x64EBE0` 内の3**命令** `0x64F03C/0x64F19C/0x64F1B4` をON/OFFする。gohanのローカルPatchListはコード書換え後にキャッシュを更新する。一方、下位転送種別12の受信 `NetTransfer12_ReceiveTownChunk` | MEDIUM | ? |
| ACNL-F0590 | HHD の顔の画面が ACNL の下画面の最前面に予想どおり出る・必要なメモリ（2026-10-05、HIGH: 実機の画面と designer の予想の照合 + 実機のメモリ） | 解析ソフト IDA（ida-pro-mcp）、解析モデル opus-5.5。T013 段 1。gohan `work/hhd-charcreate` eb79ee7、3gx SHA-256 0021cca0…3cc6、SD /hhd_charcreate.arc 333,096 B。 | HIGH | S |
| ACNL-F0595 | HHD の BFLAN を ACNL の BCLAN に変換できる（書き出しは ACNL の実物 727 本でバイト一致）・不透明度の伝播の旗（2026-10-05、HIGH: 実物との照合） | 解析モデル opus-5.5。段階 2 の遷移（開閉のアニメ）。 | HIGH | S |
| ACNL-F0597 | HHD のキャラクリ画面から ACNL のプレイヤーの見た目を変えられる（実機 全 PASS）（2026-10-05、HIGH: 静的 F080 + 実機） | 解析モデル opus-5.5。gohan work/hhd-charcreate ce17e54、3gx SHA-256 e25dfca4…d8b3、SD /hhd_charcreate.arc 358,184 B。利用者の目視で全項目 PASS: | HIGH | S |
| ACNL-F0606 | 目の形を種別 11 で送る実装（T020、2026-10-06、MEDIUM: 静的のみ。gohan e85bac0 未実機） | 解析モデル opus-5.5。IDB: `sub_581FE0` に注記（プロフィール +21656 の 168 B（Mii まわり、状態 +168）を状態 1 → 2 の送る形にする。戻すのは `sub_582160`）。 | MEDIUM | S |
| ACNL-F0609 | gohan の他機能の「自分のプレイヤー」— 問題が出た所と出なかった所の理由（2026-10-06、MEDIUM: 静的 + 利用者の実機の結果） | 解析モデル opus-5.5。F091 の続き（0xAA7994 = 表の 0 番 = ホスト）。 | MEDIUM | S |
| ACNL-F0610 | gohan のリソースを sdmc:/gohan に（2026-10-06、設計 + 静的検査。実機未確認） | 解析モデル opus-5.5。利用者の依頼: 没アイテムのアイコン・名前表・HHD の arc を SD の gohan フォルダから読む。名前表は人が読める形で、タイトル ID ごと（ローカライズ）。 |  | S |
| ACNL-F0614 | 公共事業エディターのプレビュー切り替えの実測（2026-10-06、HIGH: 実機の計測。gohan work/preview-probe 1836acd） | 解析ソフト: IDA / 解析モデル: opus-5.5。 | HIGH | S |
| ACNL-F0616 | 待ちを外したプレビューの実測と、HHD が開かなくなった原因（2026-10-06、HIGH: 実機の計測と実機の変数） | 解析ソフト: IDA / 解析モデル: opus-5.5。 | HIGH | S |
| ACNL-F0626 | T022 カタログの生成器（Codex 依頼 t022_catalog_arc、gpt-6.1-sol xhigh、2026-10-07。打ち切り。記録 ID なし = 道具と生成物） | tools/hhd/make_catalog_arc.py → work/cache/hhd/catalog/hhd_catalog.arc（5 レイアウト・373 アニメ・57 テクスチャ、構造検査 PASS）、tools/hhd/make_icon_bank.py → hhd_icons.bin（3,723 品。**ETC1A4 3,465 品と ETC1 258 品が混在**: 4,096 B に揃えた版と原本の形の版を作成。ETC1 に不透明のアルファを足す方式の採否 |  | ? |
| ACNL-F0630 | T022 カタログの実機不具合 8 件の原因と修正（2026-10-08、MEDIUM: 静的。実機未確認） | 解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（xhigh）**、Codex（依頼 work/codex/tasks/t022_catalog_fix1.md、--allow-gohan）。採番・照合・commit は親（opus-5.5）。根拠 **work/evidence/t022_catalog_fix1/report.md**。gohan b68e21f（work/decor-catalog）。 | MEDIUM | A |
| ACNL-F0632 | 足したチップが動かない・2 回目の窓のヒープ不足・テントでの壁紙/床タブ（2026-10-08、MEDIUM: 静的。実機未確認） | 解析: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix3。5 時間枠のため停止指示で途中終了、ビルド可の状態）。照合・仕上げ・採番は親（opus-5.5、Codex の枠切れ後）。根拠 **work/evidence/t022_catalog_fix3/report.md**。gohan d059843。 | MEDIUM | A |
| ACNL-F0633 | 改造テントの壁紙/床・自由スクロール・すぐ開く・すぐチップ・位置保持（2026-10-08、MEDIUM: 静的。実機未確認） | 解析: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix4）。照合・commit・採番は親（sonnet-5.5）。根拠 **work/evidence/t022_catalog_fix4/report.md**。gohan 0db52e0（work/decor-catalog）。 | MEDIUM | A |
| ACNL-F0634 | しばらく使うとフリーズする原因 — 読み込みのヒープの枯渇（2026-10-08、実測 + 静的: MEDIUM） | 測定: 親（sonnet-5.5、ida-pro-mcp、固まった状態）。静的洗い出しと修正: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix5）。根拠 **work/evidence/t022_freeze_20261008/README.md**、**work/evidence/t022_catalog_fix5/report.md**。gohan 89a636e。 | MEDIUM | A |
| ACNL-F0635 | 窓が読み込みヒープを食う最大の原因は非表示 TextBox の描画用バッファ（2026-10-09、MEDIUM: 静的。実機未確認） | 解析: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix6）。照合・commit・採番は親（sonnet-5.5）。根拠 **work/evidence/t022_catalog_fix6/report.md**。gohan f43f757（work/decor-catalog）。 | MEDIUM | A |
| ACNL-F0636 | 窓を開けなくなる原因 — 余白の基準（連続空き）が現実の割れ方と合っていなかった（2026-10-09、実測 HIGH + 静的 MEDIUM） | 測定: 親（sonnet-5.5、拒否された後の停止状態）。修正: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix7）。根拠 **work/evidence/t022_heap_20261009/README.md**、**work/evidence/t022_catalog_fix7/report.md**。gohan 1bfb8ca。 | HIGH | A |
| ACNL-F0637 | 家具のチップと窓が読み込みヒープを共有する問題 — 基準の見直しと、アイコン枠を描画命令用ヒープへ（2026-10-09、実測 + 静的 MEDIUM、実機未確認） | 測定: 親（sonnet-5.5、通知が出た後の停止状態）。調査・修正: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix8、枠切れで一度停止して再開）。根拠 **work/evidence/t022_heap_20261009/README2.md**、**work/evidence/t022_catalog_fix8/report.md**。gohan 6ca7158。 | MEDIUM | A |
| ACNL-F0638 | HHD の「壁にかける家具」リストの移植（2026-10-09、静的 MEDIUM、実機未確認） | 調査・実装: Codex gpt-6.1-sol xhigh（依頼 t022_wall_catalog）。照合・commit・採番は親（sonnet-5.5）。根拠 **work/evidence/t022_wall_catalog/report.md**。gohan 3e9654f。 | MEDIUM | A |
| ACNL-F0642 | 通常ドロップをAcBalloon経由へ置換するAR実装 | **確度: MEDIUM（ARM/ABIは静的確認。現行cave移設版は実機未検証）** | MEDIUM | B |
| ACNL-F0643 | crash_dump_00000005 の直接fault | **確度: HIGH（dump＋本体命令列）。根本原因の旧帰属は撤回。** | HIGH | B |
| ACNL-F0649 | type 0x10 completion token案は実機クラッシュで棄却 | **確度: HIGH（crash_dump_00000008＋静的再監査）。** | HIGH | B |
| ACNL-F0652 | 0x838080 dead-cave再利用は実機runtimeと衝突する | **確度: HIGH（crash_dump_00000009＋enable直後再現）。** | HIGH | B |
| ACNL-F0654 | custom guard依存を廃止し、menu-open中の0x16→0x06を直接抑止する | **確度: MEDIUM（静的検証済み、実機未検証）。** | MEDIUM | B |
| ACNL-F0655 | Ghidra-gpt-sol-5.6-F016 AR先頭E blockの最終行が1word欠けていた | **確度: HIGH（ARテキスト構文再検査）。** | HIGH | B |
| ACNL-F0659 | trace領域をARで0固定していたためGhidra-gpt-sol-5.6-F019/Ghidra-gpt-sol-5.6-F020 traceは観測不能だった | **確度: HIGH（AR実行モデルと現行コードの直接確認）。** | HIGH | B |
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
| ACNL-F0679 | inventory completionはnative DropDataではなく非同期synthetic handle 4で十分 | **確度: HIGH（UI/FieldAction構造はGhidra独立静的確認、handle 4成功経路はGhidra-gpt-sol-5.6-F032実機確認）。Ghidra-gpt-sol-5.6-F038実装自体は未実機。** | HIGH | B |
