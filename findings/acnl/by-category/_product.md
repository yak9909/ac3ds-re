<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / _product

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| ACNL-F0002 | 2026-09-12 普通チャットの入力所有者・日本語フォント・候補表示 | 通常gohanへ候補列挙を追加。BsMenuChatの所有者照合、ゲーム日本語フォント154シート対応、stock Batch容量、threadJoinの正のtimeoutの扱いを[トピック](../project_v2/docs/topics/chat_kanji.md)へ集約。根拠 `project_v2/work/evidence/chat_kanji/`。字形/幅は全65536コードポイントで元ARMと一致。リンク済み変換候補17/6/143/3/1件が原本と一致し、 | MEDIUM | ? |
| ACNL-F0004 | F-407 実機成功: キーボード非起動で候補17/6/143件を取得（2026-09-11、最新・HIGH） | 利用者がF407を配置・ACNL再起動/再アタッチ。Suspend/bp0、実機headerと全生成コードアンカー、成果物/現行ソースhashを照合した。要求2の展開・辞書配置・315再配置が成功し全解放された後、要求3で「かんじ」「わたしはねこがすきです」「か」を各1回実行。候補17/6/143件が原本PCと全順位一致。前2入力は保存済み実機SWKBD候補列とも直接一致。「か」は初回50件からgetterが143件まで追加検索し、終端0を確認した。 | HIGH | ? |
| ACNL-F0005 | F-407 PC準備時点の履歴（配置待ちは解消済み） | 独立Plugin/SwkbdEngineProbe/swkbd_engine_probe.3gxを作成。289,985 bytes、SHA50ec21a1bde6d52f13fa916ac23aceb2f81dbb833a5ca4db8ca77c3b96368385。ソース/ホスト/ARM構文を検証してからビルド。生成1301命令/213直接分岐/48PCリテラルの検査、生成ARMから原本エンジンへの一連のPC試験、mailbox誤適用防止10条件までPASS。展開はctrt |  | ? |
| ACNL-F0007 | F-405 解決: キャッシュ処理中のクラッシュ、再起動で一時変更解除 | Plugin/crash_dump_00000004.dmpのPC0xFFF2B3F8はMCR p15,0,R1,c7,c10,1。R1=FAR=0x061BE000が試験arenaと一致し、DFSR0x805はsection translation fault/write。ARM11 core1、SVC mode、保存プロセスsocket/TID0x0004013000002E02。ダンプ解析とidalibの保存命令列を照合（HIGH）。他コアの異なるアドレス空間が原因とい | HIGH | ? |
| ACNL-F0008 | F-404 実機成功: 3gxで5 MiB確保・内蔵FS読取り（2026-09-11） | 利用者が独立swkbd_probe.3gxを配置しACNLを再起動。新規header/生成コードアンカーを照合、Suspend/bp0を確認してmailboxに1要求を設定。5秒の自動Suspend付きResume後、state2/failure0。5,242,880 bytesを確保して全域write/readback成功、内蔵辞書2,045,891 bytesと圧縮.code 471,668 bytesのOpen/GetSize/全体Read/CRC32一致/Close/ |  | ? |
| ACNL-F0009 | F-403完了・F-404 3gx検証へ移行（2026-09-11） | 最新はDOCS/system_keyboard_plugin_probe.md。全辞書2,045,891 bytesの実機取得と全bytes/SHA照合、6辞書個別照合が完了。一時handle/buffer/wrapperは全復元済み。エンジン実機実行は未実施。 |  | ? |
| ACNL-F0010 | F-402 最終: 内蔵code全体Read・バイト同一性・cleanup確認（HIGH） | code kind2で読んだ471668bytesが提供NCCH内.codeと完全一致。SHA09e684ca41504af96b6548f42e8a2a159f07d3865ca7077e1d4f8356b98ec14e、ExeFSエントリhashとも一致。ctrtool再展開770048bytesは従来解析対象SHAa0b78005b0a99116ca703bc9b7625ce1b0f2d4cc45f66fc6fb9ab8a34244d4f0と一致。NCCHheader署 | HIGH | ? |
| ACNL-F0014 | 最新 F-400: 再配置のPC試験成功・テーブル同梱を避ける方針 | 利用者はSD/3gxへテーブルをリソース同梱する方式を避けたいと指定。 |  | ? |
| ACNL-F0015 | 最新 F-399: 画面・APTなしのエンジン実行をPCで確認 | 初期化から全候補列挙までOS mockなし。原本data/BSSをRO化しても17/6件一致。 |  | ? |
| ACNL-F0018 | F-396: 旧SWKBDケーブとGUI v2の重複を回避し再適用 | HIGH（配置の重複と適用内容をソース/実機メモリで照合。移設後の起動動作は未観測）。 | HIGH | ? |
| ACNL-F0024 | F-383: 通常チャットのキーボード生成入口（2026-09-09） | MEDIUM。利用者指定でフレンドチャットを除外、通常チャットを対象にする。 | MEDIUM | ? |
| ACNL-F0027 | F-364: ACNLの内蔵キーボード起動候補経路・APT/GSP契約・ABIの検証（2026-09-08） | **confidence MEDIUM。** `code.bin.i64`の静的解析、停止中実機の読み取り、原本ARMの局所実行。 | MEDIUM | ? |
| ACNL-F0065 | F-27 地面更新のダーティビットマップ — `HIGH` | `sub_59DA7C(X, Y)` (`0x59DA7C`) と `sub_599814(X, Y)` (`0x599814`) は | HIGH | ? |
| ACNL-F0083 | F-45 `NCCH/exefs/code.bin` は実機とは別ビルド — アドレスが対応しない — `HIGH` | ExeFS の `.code` は `0x00100000` にロードされ、`.text` / `.rodata` / `.data` が | HIGH | ? |
| ACNL-F0085 | F-47 `0x596890` の実態 — 踏みつけ処理 `FieldObj_TrampleAt` — `HIGH` | `REFERENCES/CHEATS/outdoor.txt` の「歩いた場所の物を消す」が書き換えるアドレス。 | HIGH | ? |
| ACNL-F0087 | F-49 メッセージ表示の仕組みと「メニューアニメーションをカット」の副作用 — `HIGH` | `REFERENCES/CHEATS/ui.txt` の「メニューアニメーションをカット」で | HIGH | ? |
| ACNL-F0090 | F-52 静的解析の本体を `code.bin.i64` に移した — `HIGH` | ユーザーが持ち込んだ `code.bin.idb`（IDA が `code.bin.i64` へ自動アップグレード）を | HIGH | ? |
| ACNL-F0092 | F-54 CTRPF プラグインの地域別アドレス表 — 本ビルドは **JPN 無印** — `HIGH` | `REFERENCES/CTRPF PROJECTS/Vapecord-ACNL-Plugin-master` の解析。 | HIGH | ? |
| ACNL-F0093 | F-55 Vapecord のコードを手がかりにした関数解析（時刻・部屋・通信） — `HIGH` | F-54 の対応表を使い、プラグインが実際に呼んでいる関数を本ビルドで解析した。 | HIGH | ? |
| ACNL-F0095 | F-57 ゲーム内メニューを ID で開く仕組み — 日付変更ウィンドウは `MenuID 0x2E` — `HIGH` | 「ゲーム内の時間変更ウィンドウを呼び出すチートがあったはず」という問いの答え。 | HIGH | ? |
| ACNL-F0096 | F-58 【訂正】FOXXY はゲーム本来の日付変更ウィンドウを開いていた — `HIGH` | F-57 で「FOXXY にはゲーム内 UI を開く経路は無い」と書いたが**誤り。** | HIGH | ? |
| ACNL-F0097 | F-59 FOXXY 時間変更チートの残り 2 パッチ — 演出をメニュー姿勢に差し替えている — `HIGH` | F-58 で未解析だった `0x6563A8` と `0x670A48` を解明した。 | HIGH | ? |
| ACNL-F0098 | F-60: Vapecord の時間設定チートと、ゲーム自身の時計確定経路 | confidence: **HIGH**（静的解析。Vapecord のソースと逆コンパイルが独立に一致） | HIGH | ? |
| ACNL-F0099 | F-61: `REFERENCES/CHEATS/drop.cpp` の「host drop」の正体 | confidence: **HIGH**（静的解析。素の命令・分岐先・Vapecord の表が三方で一致） | HIGH | ? |
| ACNL-F0100 | F-62: チート「ドロップ16x16」（`REFERENCES/CHEATS/drop.txt`） | confidence: **HIGH**（静的解析。off ブロック 113 word が実バイナリと完全一致し、 | HIGH | ? |
| ACNL-F0101 | F-63: `REFERENCES/CHEATS/drop.txt` の「host drop」— `drop.cpp` にない 6 行 | confidence: **HIGH**（静的解析。素の命令・分岐先・Vapecord の表・ID 一覧が整合） | HIGH | ? |
| ACNL-F0103 | F-65: 通常ドロップの入口と、種別を変える AR コード | confidence: **HIGH**（静的解析。チートの復元値と逆コンパイルが一致）/ 実機未検証 | HIGH | ? |
| ACNL-F0104 | F-66: オンライン髪型変更は虫取り網アクションから美容室状態 `0xB9` への迂回 | confidence: **MEDIUM**（独立した複数の静的経路で一致。実機・通信相手を使った動的検証は未実施） | MEDIUM | ? |
| ACNL-F0106 | F-68: オフラインなら profile の HairStyle だけを書いて `vc_UPDATE` すれば即時・装備保持にできる | confidence: **HIGH**（静的経路に加え、オフライン実機で即時反映・衣装8枠維持を確認） | HIGH | ? |
| ACNL-F0118 | F-80: `BsMenuCatalog` は通常下画面メニューの `0x08/0x10` handshakeを実装しない | confidence: **HIGH**（`code.bin.i64` の全直接xref、`BsMenuItem` と | HIGH | ? |
| ACNL-F0138 | F-100: 再々精査 — GX 5 本の type バイト確定、「実装位置」表記の誤りを訂正 | confidence: **MEDIUM**（**静的解析のみ**、F-101 で訂正。表題の「HIGH 化」も撤回） | MEDIUM | ? |
| ACNL-F0140 | F-102: ★実機観測でコマンドバッファ構造を確定（初の HIGH） | confidence: **HIGH**（CLAUDE.md の定義どおり**静的解析と動的観測の双方**で確認） | HIGH | ? |
| ACNL-F0168 | F-130: ResFontのCMAP代替処理を確定。全liveフォントは2種の線形フィルタflagがON | confidence: **CMAPと代替処理 HIGH** / **filter flagの意味 HIGH** | HIGH | ? |
| ACNL-F0181 | F-139: ResFont→CMAP→batch quad の実機経路を確認 — `HIGH`（経路・引数・構造） | 2026-08-28、Remote GDB を停止／再開し、文字更新中の同一呼び出しを breakpoint で採取した。 | HIGH | ? |
| ACNL-F0189 | F-163: ★CTRPF プラグインは GPU 可視メモリを確保できない — `HIGH`（実機で検証、結果コードまで確認） | `Plugin/CTRPluginFramework-BlankTemplate-0.8.0` に検証エントリを追加して実機で実行。 | HIGH | ? |
| ACNL-F0205 | F-179: Vapecord のマップ上プレイヤー表示は OSD（フレームバッファ直描き）だった — `HIGH`（ソース確認） | 出典: `REFERENCES/CTRPF PROJECTS/Vapecord-ACNL-Plugin-master/src/features/PlayerCodes/PlayerCodes.cpp` | HIGH | ? |
| ACNL-F0238 | F-213: ★★★★CTRPF プラグインへの移植 — ケーブは書き直さずバイト列ごと移す — `HIGH`（ビルド済み・実機未検証） | `Plugin/CTRPluginFramework-BlankTemplate-0.8.0/Sources/OwnGui.cpp`。 | HIGH | ? |
| ACNL-F0244 | F-219: ★★★CTRPF のファイルパスはプラグインのフォルダ基準。ON が早すぎると落ちる — `HIGH`（実機） | `.acgx` を SD に置いてプラグインを ON にしても「ACNL GUI OK」のままだった。 | HIGH | ? |
| ACNL-F0245 | F-220: ★★★TODO-134 段 B 完成 — 上下画面の描き分けとチャンク別の色 — `HIGH`（実機） | 自前チートメニュー（TODO-134）の描画基盤。実機で確認済み。 | HIGH | ? |
| ACNL-F0246 | F-221: ★★ゲームのアロケータから取れるのは 0x4000 まで — `HIGH`（実機） | グリフアトラスを 256x128 LA4（32KB）にしようとして `Alloc(0x8000, 0x80)` を試したが | HIGH | ? |
| ACNL-F0247 | F-222: ★★★★★自前チートメニューが実機で動いた。ゲームは止まらない — `HIGH`（実機） | TODO-134 の目的そのもの。**メニューを開いている間もゲームが進行する。** | HIGH | ? |
| ACNL-F0250 | F-225: ★★★★「開いている間だけ描く」にすると、閉じても最後の絵が残り続ける — `HIGH`（実機） | ユーザー報告: | HIGH | ? |
| ACNL-F0258 | F-233: 描画パス末尾と通常場面の実 replay を再監査 — `HIGH`（静的＋実機。ロード画像の順序は未測定） | `HANDOFF_CHEATMENU.md` と F-200 / F-230 の前提を、`code.bin.i64` と | HIGH | ? |
| ACNL-F0263 | F-237: Layout の再生順は `LayoutList_SetDisplay` で局所的に制御できる — `MEDIUM`（静的＋実機 no-draw） | `REFERENCES/TEXTS/render.txt` の gokiro 氏は、描画コマンド追加・再生順変更・コマンド | MEDIUM | ? |
| ACNL-F0281 | F-258: 作業配列を自前バッファへ差し替える案は失敗した — `HIGH`（実機・目視） | > **★F-263 で理由が判明した。** 作業配列は 4 本（`+1640/1644/1648/1652`）あり、 | HIGH | ? |
| ACNL-F0283 | F-260: F-259 の設計を実装し、IDA の逆アセンブルで検証した（実機未適用） — `HIGH`（静的のみ） | `PATCHES/cave_node_record.py`。`cave_node_draw.py` を複製し、F-259 の設計を載せた。 | HIGH | ? |
| ACNL-F0284 | F-261: ★★★★★Layout の初期化 `sub_5685A4` に「自前リストの正しい作り方」が全部書いてある — `HIGH`（静的のみ） | F-260 の実装を静的に検証する過程で見つけた。**私の実装には致命的な誤りが 2 つあった。** | HIGH | ? |
| ACNL-F0285 | F-262: 再生の複製経路を逆アセンブルで裏取りし、実装の誤り 2 件を追加で直した — `HIGH`（静的のみ） | `GpuCmd_ReplayRecordedListRange` の `if (a7)` 側（`0x7B0E08`〜）を逆アセンブルした。 | HIGH | ? |
| ACNL-F0290 | F-267: 雛形の複製を廃止した。写し元依存が実装から消えた — `HIGH`（静的のみ） | F-259 の実装は、本物の Layout から `+0x28` の 20 語（`0x50` バイト）を写して雛形にしていた。 | HIGH | ? |
| ACNL-F0301 | F-277: 記録 → Commit → 再生の連鎖を端から端まで静的に証明した — `HIGH`（静的のみ） | 「実装したものがどう影響するか」を、関数ごとに全部読んで繋いだ。 | HIGH | ? |
| ACNL-F0305 | F-280: ★★★★★メニューを実際に描けるところまで実装した（フォント・レイアウト API・領域拡張） — `HIGH`（静的のみ・未適用） | これまで描いていた「ACNL GUI OK」は**デモ**であって、メニューには足りなかった。 | HIGH | ? |
| ACNL-F0307 | F-282: CTRPF プラグインへ移植した。**ビルド環境なしで移植の正しさを照合できる** — `HIGH`（静的のみ・未ビルド） | `Plugin/CTRPluginFramework-BlankTemplate-0.8.0` の描画まわりを全部書き直した。 | HIGH | ? |
| ACNL-F0308 | F-283: シミュレータ相当の UI へ作り直した（美咲フォント・アニメーション・項目型）— `HIGH`（ビルド済み・未適用） | 利用者の指摘 3 点に対応し、`Plugin/CTRPF-GUI-Simulator` の設計を C++ へ写した。 | HIGH | ? |
| ACNL-F0310 | F-286 — F-283 / F-285 を捨てて **F-282（実機で描画に成功した版）へ巻き戻した** — `HIGH`（静的検証済み・実機未確認） | 実機で描画に成功した CTRPF プラグインの最後の版は **F-282**（利用者報告 | HIGH | ? |
| ACNL-F0317 | F-293 (HIGH・実機) — ★★★正規の手順で描けた。**自前の記録ケーブ 205 語を撤去** | F-292 の設計を実装し実機で成功した。道具は `PATCHES/build_pane_tree.py`。 | HIGH | ? |
| ACNL-F0318 | F-294 (HIGH・静的のみ) — ★自前フォントで `TextBox` を使えることを確認。`Glyph` 構造を確定 | 利用者の要望は「ゲームのフォントではなく**自前フォント**で描くこと」。**可能**である。 | HIGH | ? |
| ACNL-F0322 | F-298 (HIGH・静的のみ) — ★TextBox 方式は実装可能。**自前フォントの「コード」はほぼ要らない** | 利用者の指示で、基準仕様を詰める前に TextBox 方式の実現性を静的に判定した。 | HIGH | ? |
| ACNL-F0329 | F-305 (HIGH・実機) — ★★★自前フォントで実機に描けた。`nw::font` の構造を**全欄**確定 | F-303 / F-304 の 2 度のクラッシュを受けて、**推測を一切残さず**構造を確定してから適用した。 | HIGH | ? |
| ACNL-F0331 | F-307 (HIGH) — ★基準仕様 v2 を改訂し、**仕様書そのものを機械で検証**した | 制定時（2026-09-05）の §3 は「文字だけ v1 のスプライト表 + 自前ケーブ（`CAVE_TXT`）」だった。 | HIGH | ? |
| ACNL-F0332 | F-308: 大量の文字を登録したときの天井（TextWriter 直呼び方式の評価） — HIGH | > 問い: 自前チートメニューで**自前フォントの文字を大量に登録**する可能性がある。 | HIGH | ? |
| ACNL-F0335 | F-311: プラグインを基準仕様 v2 へ書き換えた（3gx 名 = gohan）— 実機未検証 | > 対象: `Plugin/CTRPluginFramework-BlankTemplate-0.8.0` |  | ? |
| ACNL-F0342 | F-316: ★シート記述子 `+0x0C` は **`(幅<<16) \| 高さ`** — HIGH | 256x128 のシートに載せ替えたら、**文字が完全に化けた**（画素が散る）。 | HIGH | ? |
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
| ACNL-F0362 | F-336（2026-09-07）: 試験2項目へ効果配線（通知確認用） | 利用者の要望：テスト用の無敵モード・壁抜けに通知を入れること。 |  | ? |
| ACNL-F0369 | F-343（2026-09-07）: 空いた容量で通知を Simulator と同じ 7 件にした | **confidence: HIGH**（検証器 8 群が異常 0 件 / ビルド成功。★実機での目視はこれから） | HIGH | ? |
| ACNL-F0372 | F-346（2026-09-07）: ★アトラス以外をプラグインの `.bss` へ移した（借用 442,368 -> 36,864 B） | **confidence: HIGH**（検証器 8 群 異常 0 件 / ビルド成功 / **実機で確認済み**） | HIGH | ? |
| ACNL-F0373 | F-347（2026-09-07）: キーボード UI を足したときの見積もり（実装前の机上計算） | **confidence: MEDIUM**（`CTRPF-GUI-Simulator` のソースから数えた実数 + F-341 の費用式。**未実装**） | MEDIUM | ? |
| ACNL-F0375 | F-349（2026-09-07）: Simulatorの文字・数値キーボードをCTRPFへ移植 | **confidence: MEDIUM（ソース照合とホスト試験。実機未確認）**。 | MEDIUM | ? |
| ACNL-F0377 | F-351（2026-09-07）: 入力遮断をプラグインへ実装し、下画面ロックへ一本化した | **confidence: HIGH（実機で機構を確認）/ MEDIUM（プラグイン版は実機未確認）** | HIGH | ? |
| ACNL-F0382 | F-356（2026-09-07）: ★「ゲームスピード変更」チート `0054C6E8` の正体 — フレームペーシングの無効化 | confidence: **HIGH（静的）** / 実機での効果確認は未実施（利用者の報告のみ） | HIGH | ? |
| ACNL-F0385 | F-359: 内蔵漢字変換候補取得の目的・共有辞書候補・ゲーム内APT起動経路（2026-09-08） | 調査目的は3DS本体内蔵のかな→漢字変換辞書・変換候補の取得。 | LOW | ? |
| ACNL-F0388 | F-361（2026-09-08）: ★★★ACNL は CRO 動的モジュールを使う — しずえ画面を静的に解いた | confidence: **HIGH（静的で完結。実機のバイト列と 1 命令も違わず一致）**。 | HIGH | ? |
| ACNL-F0389 | F-362: 内蔵日本語辞書6本の取得・主要辞書75,770件の読み/候補を抽出（2026-09-08） | **confidence: MEDIUM**。複数静的証拠とPC内での元ARM命令実行で検証。 | MEDIUM | ? |
| ACNL-F0390 | F-363: 内蔵キーボードの候補順位・文節変換・学習を原本ARMで再現（2026-09-08） | **confidence: MEDIUM。** SWKBD専用idalib IDBの静的解析＋PC上のUnicorn実行。 | MEDIUM | ? |
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
| ACNL-F0413 | F-388: ACNLのSuspendでは動作中SWKBDプロセスは停止しない（2026-09-09） | 利用者が内蔵キーボードへ未確定の`かんじ`を入力したまま現在のIDAでSuspendしたところ、 |  | ? |
| ACNL-F0415 | F-390: 破損した3gxをしずえスキップ統合前へ復元（2026-09-09） | **ソースと成果物の復元はHIGH、実機表示の再確認は未実施。** |  | ? |
| ACNL-F0416 | hidden letterの入場座標とCHEATS選択肢（2026-10-14） | GPT-6/idalib、MEDIUM。LetterDragWindowBase_AttachToPane 0x31F2B8はroot+632をparent+976/N_pos_ltrへ繋ぐ。Pane_CalculateMtxはvisible0かつDrawInfo+136 bit2なしなら子も計算しない。原ARM probe/製品FrameStepで、親を入場位置へ移しても[-560,-80,0]に残留し、force bit4で[150,-80,0]へ更新/visible0保 | MEDIUM | ? |
| ACNL-F0418 | UI入口・pocket再入場・非drag trash・青選択（2026-10-13） | GPT-6/idalib、MEDIUM（原JPN ARM＋caller/vtable/source、PC/実機訂正）。通常ActivateSelectedにcheckboxlist入口が無い。既存inline編集/描画へ分岐を追加。manual closet3cheat/Wire/configを削除、chat検索closetは保持。 | MEDIUM | ? |
| ACNL-F0422 | closet直通とnative転送・低ID/ウィジェット（2026-10-12） | 最終DB監査: 0x4DD030/0x4DD4A4は原数量merge/predicateとして原ARMと実行検査から2rename追加。周辺9注記も追加し合計9name/26注記、未知のlookup全ABI/choice PMF・数量action/stack第5引数は理由と次の照合をDBへ記し推測renameしない。製品不変、根拠db_peripheral_changes.json・更新XML読戻し。 | MEDIUM | ? |
| ACNL-F0425 | F005のHHD引継ぎ要件を訂正（2026-10-12） | 利用者実機報告: fix2/SHAe2afb75a...のリストは修復、hairは未修復。HHD自身が退場/待機を所有し、コマンドは直接呼ぶよう指定。native chat lifetimeの観察は変更しないが、「style起動前に親/kbd消滅必須」「早期Showが不具合」の推論を撤回する。F005/T007のCPU試験を実機修復の証拠としない。 |  | ? |
| ACNL-F0429 | gohanへのidle/気絶/消失抑制・チャット移植（2026-10-11） | 2026-10-12修正T003: 利用者のMapEditor入力不能報告を旧実Start/HoldField/Present/Wantedで再現。Presentはfield非Shownも含み、actionの退場gateが自身のHoldFieldで継続Tickを止めていた。Running前だけ待つことで新実Tickの移動/touch/game入力遮断が全true。ChatCommandsはcheckbox適用値で有効化し、hotkeyでnative Wait前に原文captu |  | ? |
| ACNL-F0430 | 収録チートの天気返却と島チャット数字制限の意味（2026-10-11） | 解析: IDA/idalib-mcp、実モデルgpt-6。主IDB acnl_jpn_v15_annotated.i64、code SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb。既存gohan.md §17.8/JOKER・Adios・Vapecord原sourceの出自は変更しない。実機は操作せず確度MEDIUM（複数静的根拠）。 | MEDIUM | ? |
| ACNL-F0431 | 全収録チートの意味コメント調査（2026-10-11、利用者指示で中断） | 最新の訂正を受け、コードの一般説明をゲーム内の意味に改める。全2700関数の原資料/notes/calls/operandをcatalogへ記録、全project_v2の対応資料をhash付き検索索引化済み（materials.json、抽出エラー0）。未対応binary/IDA内部形式の全読了とはしない。同一資料のコピーは独立証拠に数えない。 |  | ? |
| ACNL-F0432 | 整理済みチートの挙動保持リファクタリング（2026-10-11） | 解析/検証: Tree-sitter・GNU C++ / gpt-6。元IDA-gpt-6.1-sol-F018と追加TreeSitter-gpt-6-F001の帰属を保持。対象は2700既存関数のみ、新規JOKER/他CTRPF整理は中断。共有設定familyの1関数化は利用者の訂正で撤回。 |  | ? |
| ACNL-F0433 | C++由来107チート本体の局所化と部分集合の実出力照合（2026-10-10） | 2026-10-11 CHEATSのみの追補: message(5).cppは施設状態変更8callbackと8tableを含み、原型CHARS_U8_MAP/items宣言は欠ける。原range-forのiは局所変数なのに旧scoped閉包が別drop.cppのiへ束縛していたため、CHEATS専用contractで原AST/range declarator/table/Write8と字面以外の束縛を照合し当該偽依存を除外。局所u8 id/const char*nameとv | MEDIUM | ? |
| ACNL-F0436 | リスト背景のフェードと模様替えカメラpan（2026-10-10、MEDIUM、本体非表示はF016で訂正） | 解析ソフトIDA（idalib-mcp）/解析モデルgpt-6.1-sol。原SHA/ARM32 LE/imagebase/ロード範囲・独立した入口命令を確認し、実装前に[設計](../docs/topics/catalog_camera_controls_design.md)を保存。利用者が前版hhd_room_camera1を実機PASSと報告した後の追加要望。 | MEDIUM | A |
| ACNL-F0437 | HHD通常室内カメラの連続操作をACNLの家へ移植（2026-10-09、静的MEDIUM、2026-10-10利用者実機PASS） | 2026-10-10追記: 利用者は提示hhd_room_camera1を実機で確認し問題なしと報告。配布版SHA/sourceに対する確認として扱い、端末上のSHAや各個別ケースは再測定していない。F013同梱の確認待ちも解消。新F015追加の確認ではない。 |  | A |
| ACNL-F0438 | 外観に依存せず室内の壁配置・張替え機能を判定（2026-10-09、静的MEDIUM、2026-10-10利用者実機PASS） | 2026-10-10追記: F014同梱hhd_room_camera1について利用者が実機で問題なく動作と報告。提示版に対する確認として確認待ちを解消し、端末SHA/壁材質別の個別試験一覧は未再測定として扱う。 |  | A |
| ACNL-F0439 | 下位送信のBusyは未確認フレーム数、F008待機中拒否の再検証（2026-10-04、静的＋利用者実測） | F008試作で待機中にも`Net=1 Busy=1`が持続し、旧版では同じ接続内で複数回送信できたと利用者が確認。送信バッチ`0x62710C`は管理`+156+peer`のbyteを+1、受信下位ヘッダ低2bitの処理`0x62A0B4`は負deltaで減らす。これは未確認フレーム数であり、F008の「転送枠使用中」だけの解釈を訂正。`SendSegments`も同じゲートを呼ぶため、同じ瞬間の値1なら旧通常送信も失敗する。新事前呼出しが値1を作った証拠はなく、版差/タイミ |  | ? |
| ACNL-F0440 | 送信者の動作中に下位種別12が拒否される送信ゲート（2026-10-04、静的MEDIUM／回避未検証） | 利用者の2台では座標同期がホスト・ゲストの両方向で成立し、拒否は送信者本人の歩行・アクション中に起きる。受信相手の動作状態には依存しないとの訂正を優先する。個別宛先の`NetTransfer_SendSegments 0x616E10`は`NetTransfer_CanQueueForPeer 0x61849C`の拒否で0を返す。同関数は`enforcePeerMasks=1`なら相手別4マスクを検査し、0ならその4条件だけ省く。接続可能性とpeer転送枠のbusy検査は両モ |  | ? |
| ACNL-F0445 | アニメのフレームは実機で進んだ（適用段は IDA-opus-5-F013 で解決）（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。**自前資源のマテリアルアニメのフレームを実機で進めた。** | HIGH | ? |
| ACNL-F0447 | 外部 nw4c ヘッダとの照合。実測は全て一致し、引数の解釈を2点訂正（2026-09-21、HIGH、静的＋実機照合） | 解析ソフト: IDA / 解析モデル: opus-5。利用者提供の [SMBNext/nsmb2-headers](https://github.com/SMBNext/nsmb2-headers) | HIGH | ? |
| ACNL-F0463 | ゆうめいなキノコで大きくなる仕組みと、プレイヤーの大きさは通信に乗らないこと（2026-09-30、MEDIUM: 静的＋Vapecord の送信側の形と受信側の独立一致。実機未観測） | 解析ソフト: IDA（主 IDB）/ 解析モデル: opus-5.5。利用者の問い: 椅子の座る高さはオンラインに反映される（他人にも見える高さ変更チートがある）。 | MEDIUM | S |
| ACNL-F0465 | マップエディター第 2 段 — 真ん中のカーソルと A・実行範囲・薄いカーソル（UnitCursor の TEV 段 4 = アルファ × Constant4）（2026-09-29、MEDIUM: 資源の解析＋ホスト試験＋成果物の確認。gohan 実機未確認） | 解析ソフト: IDA（主 IDB）＋ romfs の UnitCursor.bcres / 解析モデル: opus-5.5。利用者指示（2026-09-28）: 盤面に触れていないときは真ん中に UnitCursor、A でモードの操作（FOXXY と同じ）。 | MEDIUM | S |
| ACNL-F0466 | メッセージのあと下画面にエディターが出ない — GameList が「隠した」と思い込んだまま、ゲームが戻した下画面をもう一度戻して止まる（2026-09-28、HIGH: 実機の値＋静的＋書き込みでの確認。経緯の一部は未確認） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的、実機を ida-pro-mcp で動的）/ 解析モデル: opus-5.5。利用者報告: 蚊に刺される等のあと、マップエディターの下画面が出なくなった（実機 Suspend 済み）。 | HIGH | S |
| ACNL-F0467 | マイデザインは村の物体の「層 1 の一覧」で描かれる — F064 の訂正と、カーソルを「マイデザインより上・それ以外より下」にする設計（2026-09-28、MEDIUM: 静的＋実機の結果と整合。設計は未実装） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的）＋ romfs の Fg.bin / FgShape.bin / 解析モデル: opus-5.5。 | MEDIUM | S |
| ACNL-F0468 | マップエディターのスポイトモード（一覧 4 行・窓の拡張）、Y、モードごとの UnitCursor の色、下画面左上の箱、マスの色の手直し（2026-09-28、MEDIUM: 静的＋描画器＋ホスト試験。gohan 実機未確認） | 解析ソフト: IDA（主 IDB）＋ acnl-ui-designer の描画器 / 解析モデル: opus-5.5。利用者指示（5540abf の確認後）: 黄 → 青、真ん中を白（上下とも）、濃さ 50 で決定、 | MEDIUM | S |
| ACNL-F0469 | マップエディターのマスの色 — 上画面の単色の四角形（UnitCursor 資源の別の体）と盤面の 5x5 の輪郭（2026-09-28、MEDIUM: 既存の実機知見の組み合わせ＋描画器。gohan 実機未確認） | 解析ソフト: IDA（主 IDB）＋既存の実機知見 / 解析モデル: opus-5.5。利用者指示: 盤面の中心から 5x5 の輪郭のマスを真っ白に。上画面の 7x7 にマス単位の単色四角形 | MEDIUM | S |
| ACNL-F0470 | マップエディターの盤面を 9x9 へ（chip_room_00 の大きさの規則）と、L / R の音（2026-09-28、MEDIUM: 静的＋描画器。gohan 実機未確認） | 解析ソフト: IDA（主 IDB）＋ romfs の bclan / bclim ＋ acnl-ui-designer / 解析モデル: opus-5.5。利用者指示: 盤面を 9x9 に、真ん中のマスの背景を少し赤く。L / R でも一覧で選んだときの音。 | MEDIUM | S |
| ACNL-F0471 | 村の下画面の建物一覧（BsMenuMapList）の作りと、マップエディターのモード一覧への流用（2026-09-28、MEDIUM: 静的＋描画器での照合。gohan 実機未確認） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的）＋ acnl-ui-designer の描画器 / 解析モデル: opus-5.5。利用者指示: 地図の右の建物一覧をマップエディターの下画面左端に出し、 | MEDIUM | S |
| ACNL-F0472 | UnitCursor を村の物体の下に描く — 地面に張り付く物の材質と、深度書き込みの出どころ（2026-09-28、MEDIUM: 静的のみ。gohan f47f5af、実機未確認） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的）/ 解析モデル: opus-5.5。利用者指示: マイデザイン等の極薄・地面に吸着したモデルに UnitCursor が被さる → 常に対象マスのモデルより下／背面。公共事業エディターも共通。 | MEDIUM | S |
| ACNL-F0473 | 持ち物の選択窓（ItemSelectWindow）のキー操作 — 十字・A・B の実装（2026-09-28、MEDIUM: 静的のみ。gohan d6b8470 で使用、実機未確認） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的）/ 解析モデル: opus-5.5。利用者指示: 一覧が出ている間、ゲームと同じく十字で選択・A で決定・B でやめる（推測で自前実装しない）。 | MEDIUM | S |
| ACNL-F0474 | 1 つの体を行列だけ変えて何か所にも描く（描画ノード FuncNode）（2026-09-28、MEDIUM: 静的のみ。gohan 4fb9e33 で使用、実機未確認） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的）/ 解析モデル: opus-5.5。利用者指示（2026-09-28）: ヒープの上限を越えたときの扱いを再設計。 | MEDIUM | S |
| ACNL-F0475 | 村の物体の描画の仕組み — 1 体ずつ色を変える入口と、カーソルが消えた原因（2026-09-28、MEDIUM: 静的＋停止中の実機の読み取り。赤の割り込みは実機未確認） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的、停止中の実機を ida-pro-mcp で読み取りのみ）/ 解析モデル: opus-5.5。 | MEDIUM | S |
| ACNL-F0476 | モデルの資源の Setup と後片付け — 自前の体を壊すと元の資源の LUT 参照が外れる（2026-09-28、HIGH: 静的＋停止中の実機の読み取り） | 解析ソフト: IDA（主 IDB を idalib-mcp で静的、停止中の実機を ida-pro-mcp で読み取りのみ）/ 解析モデル: opus-5.5。 | HIGH | S |
| ACNL-F0477 | 村の実体の材質は同じモデルで共有、書き換えるとゲームの書き出しが落ちる／参照表の安全条件（2026-09-28、HIGH: 実機のクラッシュと静的） | 解析ソフト: IDA（ida-pro-mcp で停止中の実機を読み取りのみ、主 IDB）/ 解析モデル: opus-5.5。gohan 165b571 の実機確認で「触っていない同じモデルも赤い」「しばらく使うと落ちる」。 | HIGH | S |
| ACNL-F0478 | 村のアイテムの実体（fgobj）の辿り方とモデルの引き方（2026-09-27、MEDIUM: 静的のみ。gohan 165b571 で使用、実機未確認） | 解析ソフト: IDA（主 IDB）/ 解析モデル: opus-5.5。マップエディターの上画面（赤いハイライト・移動の複製）のため。設計 docs/topics/map_editor_3d.md（D004）。 | MEDIUM | S |
| ACNL-F0480 | 模様替えの範囲選択・移動の吸着と音、持ち物の選択窓（ItemSelectWindow）の正しい使い方（2026-09-27、MEDIUM: 静的のみ。gohan のマップエディター段階 3 手直しは実機未確認） | 解析ソフト: IDA（主 IDB）＋ CRO の逆アセンブル（tools/patches/cro_rtti.py）/ 解析モデル: opus-5.5。利用者の指摘（範囲がマスに吸着しない・音が無い・ | MEDIUM | S |
| ACNL-F0481 | 持ち物の選択窓（ItemSelectWindow）と模様替えの範囲の枠（CollectChip）の作り（2026-09-27、MEDIUM: 静的のみ。gohan のマップエディター段階 3 は実機未確認） | 解析ソフト: IDA / 解析モデル: opus-5.5。マップエディターの範囲選択（利用者の決定: 案 B）のため。 | MEDIUM | S |
| ACNL-F0482 | 村のマスにアイテムを置く・消す手順（2026-09-27、MEDIUM: 静的のみ。gohan のマップエディター段階 2 は実機未確認） | 解析ソフト: IDA / 解析モデル: opus-5.5。マップエディター（gohan Issue #16）の配置・削除モードのため。 | MEDIUM | S |
| ACNL-F0483 | 模様替え UI（BsMenuInteriorEditor）の作りと、持ち物欄の名前の吹き出し（ItemSelectNameWindow）の使い方（2026-09-27、MEDIUM: 静的のみ（逆アセンブル＋romfs）。実機未確認） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「マップエディター（gohan Issue #16）」の下調べ。 | MEDIUM | S |
| ACNL-F0484 | アイテムの名前とアイコンの決まり方、没アイテムの割り出し（2026-09-27、MEDIUM: 静的＋ROM の実データ。Ghidra-gpt-sol-5.6-ITEM-T011 と独立一致。gohan の名前差し替えは実機未確認） | **名前** `ItemName_ResolvePhrase 0x56D274`(phrase, &item, a3): phrase を空に（vt+28）→ 通常の ID は `STR_Item_name` の (ID&0x7FFF)−0x2000 番 | MEDIUM | S |
| ACNL-F0486 | 持ち物へアイテムを入れるゲーム自身の処理と、持ち物画面のアイコンの作り直し（2026-09-26、MEDIUM: 静的＋実機実績のある外部実装と独立一致。gohan の実装は実機未確認） | ポケットアイテム（gohan.md §17.5）の下調べ。資料の ID 一覧に頼らず、ゲーム自身の処理を使う（2026-09-17 の利用者判断）。 | MEDIUM | S |
| ACNL-F0487 | ソフトウェアキーボードのキーの「次の入力までの待ち」の正体（2026-09-26、MEDIUM: 静的のみ（逆アセンブル＋成果物の照合）。実機未確認） | 利用者の指示「ゲーム内のキー入力で、一度入力してから次に入力できるまでの短い待ちを無くす」の下調べ（gohan で対応、下記）。 | MEDIUM | S |
| ACNL-F0488 | キーボードのキーの見た目・テクスチャの取り方・開閉アニメ・切り替え音・カーソル設定の引数（2026-09-26、MEDIUM: 静的＋romfs。実機未確認） | チャットの自前キー（全選択・左右）をゲームのキーで描き、開閉アニメに追従させるための下調べ（gohan 058e1a5）。 | MEDIUM | S |
| ACNL-F0496 | プラグインから GPU 可視メモリを確保できた＝Luma の svcControlMemoryUnsafe で SYSTEM 領域から空き番地へ貼る（2026-09-25、HIGH: 実機 2 回＋Luma の公式ソース） | **★採用しない（2026-09-25、利用者の判断）**: 他の CFW・エミュレータで使えず、Old 3DS で通るかも分からないため、自前 GUI は従来のゲームのヒープ借用へ戻した | HIGH | S |
| ACNL-F0498 | 複製の光＝BsLightMgr の組のフラグメント方向光・アンビエント・半球。向きはゲームのカメラの view で変換されるので専用カメラと食い違う。描く間だけ自前の組に差し替える（2026-09-24、MEDIUM（静的＋実機の読み取り）。gohan の直しは実機未確認） | **利用者の実機確認（gohan 8908f5d）**: ズボンは付いてくる、髪 -1 で戻る（F032 の 2 点は確認済み）。傾きは 45 度ぐらいが良い。傾けるとポリゴンがおかしい／影が変な所に出来る気がする。 | MEDIUM | S |
| ACNL-F0499 | 画面固定の複製でズボンが止まる＝部品のスキニング行列は Scene の更新が計算する。光はフラグメントライティングではない（★光の部分は F033 で訂正：読んだ組が違った）（2026-09-24、MEDIUM（実機の読み取り＋静的）。gohan 8908f5d は実機未確認） | **利用者の実機確認（gohan 246865a）**: 上画面の決まった位置に固定・世界の物に隠れない（2D UI には隠れる）・部品は欠けない・設定は全部効く。 | MEDIUM | S |
| ACNL-F0500 | 複製を画面に固定する方式＝再生直後の late pass で専用カメラ。Scene 1 に積む案は右目が壊れるので不可（2026-09-24、MEDIUM（静的＋別エージェントの実機成功の手順）。gohan 246865a は実機未確認） | **Scene 1 案を退けた理由（静的）**: `Render_DrawScene0 0x4F2334` と `Render_DrawScene1 0x4EA01C` は `byte_94CA2C` で排他（メニューが | MEDIUM | S |
| ACNL-F0501 | 複製を出したまま建物に入ると無限ロード＝管理役が枠の返却を待つ。枠は BankTable_Release で下ろしてから返す（2026-09-24、HIGH（静的＋実機 2 回）。直した gohan 0107a5b は利用者が実機で確認: 出したまま建物に出入りしても止まらない、入ったあと複製は消える、OFF→ON で問題なく再出現） | **利用者の実機確認（gohan fa33556）**: 右隣に完全な複製（装備も同じ）、髪型・髪色は複製だけに適用、OFF で消える。**出したまま建物に入ると無限ロード。** | HIGH | S |
| ACNL-F0504 | 橋の高さは村の中で一定＝「村の川底で一番多い段 + flt_6DE560」（2026-09-24、HIGH（静的＋実機の地形全体・実物の橋 y と一致＋利用者の実機確認）。gohan 1754f62 は利用者が実機で確認: 橋を出しているとき、どこにカーソルがあっても UnitCursor とカメラは同じ高さ） | **利用者の前提**: 橋の描画は海でも陸でも川でも崖でも常に同じ高さ。物理的な位置だけが下の地形で変わる（海へ動かすと下がる）。 | HIGH | S |
| ACNL-F0505 | 橋のカーソルの高さの出どころ（川の判定・ゲームの橋の置き方・岸の高さ）（2026-09-24、HIGH（川の判定: 静的＋実機の地形）／MEDIUM（岸＝最寄りの陸）。gohan へは未実装） | **背景**: F025（足元の四角の地面の最大）は、四角が全部川の中だと川底の高さになり、カーソルとカメラが上下した（利用者の実機確認）。 | HIGH | S |
| ACNL-F0508 | 半透明は描画層で後ろへ回し深度は書く／役場の旗とチケットマシン／もとから半透明の材質のアルファ／一枚絵の合成の調査（2026-09-24、HIGH（実機の比較画像）／MEDIUM（一枚絵は設計のみ）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼（実機 Suspend・役場の前、Chokistream 起動済み）。画像 `work/evidence/screens/layer_20260924/`。 | HIGH | S |
| ACNL-F0509 | 更新データの RomFS は ARCHIVE_ROMFS をファイルパス {5,0,0} で開く（ゲーム自身の開き方）（2026-09-24、MEDIUM（静的＋実機で失敗の側を確認）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の報告「0xFA・0xFB はプレビューが無いと通知されるが、置くとモデルがある」。 | MEDIUM | S |
| ACNL-F0510 | 家の足元は名前表に無い → ゲームが読み込み済みの足元を使う／0x05 は属性を書き換えない（F019・F020 の訂正）（2026-09-24、HIGH（実機の占有＋静的）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の報告「住民の家の UnitCursor が 1x1」「ベンチの周りは物を置ける。花を植えられるは物を置けるの十分条件」。 | HIGH | S |
| ACNL-F0513 | 親ヒープ *(0x94CC48) の空きは 484 KB。UnitCursor とプレビューを並べると足りない／駅・役場のプレビュー名（2026-09-24、HIGH（実機の読み取り）／MEDIUM（名前、静的）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の報告「切り替えが重い・UnitCursor がすぐ消えた・無限ロードするモデルがある」、実機 Suspend 中に gohan の変数を読んだ。 | HIGH | S |
| ACNL-F0517 | 選んだ建物の青＋透明度の揺れ（gohan BuildingHighlight）が実機で動いた（2026-09-23、HIGH） | 解析ソフト: IDA / 解析モデル: opus-5.5。gohan `58701ac`（work/grid-cursor）。F011〜F013 の方法をプラグインへ移した。 | HIGH | S |
| ACNL-F0518 | 役場・リサイクルショップも集め方どおり全体が青。全段使用の材質は近似、モデルビューアは汎用の書き出し（2026-09-23、HIGH（役場・店）／MEDIUM（モデルビューア、静的）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「役場とリサイクルショップで確かめる」「使われている材質への対応」「モデルビューアの自前モデル」。 | HIGH | S |
| ACNL-F0519 | 建物ごとのモデルはゲームのデータから集められる。写しの置き場は gohan 自身のメモリでよい（2026-09-23、HIGH（静的＋実機）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「建物ごとの対応表を自前で用意せず、ゲーム内から取得できないか」「写しの置き場を調査」。 | HIGH | S |
| ACNL-F0523 | 建物の資源は 2 系統。共有 64 枠（公共事業など 7 クラス、1 種類 2 枠）と、役場・店の専用ヒープ（2026-09-23、HIGH（静的＋実機）） | 解析ソフト: IDA / 解析モデル: opus-5.5。F007 の版で「全建物が置くたびに読み直し」「公共事業を複数置いたらクラッシュ（ダンプ 3）」の報告を受けて、 | HIGH | S |
| ACNL-F0533 | モデルの一覧は ROM から読める。8,818 本の .bcres とその検算（2026-09-22、HIGH、静的） | 解析ソフト: IDA / 解析モデル: opus-5。利用者の問い「ROMに名前群が存在する可能性はないですか？」への答え。 | HIGH | ? |
| ACNL-F0536 | グリッドカーソルが村の屋外で描けた。見えたものから分かったこと（2026-09-22、実機目視） | 解析ソフト: IDA / 解析モデル: opus-5。F031 の 2 つを直した gohan で、**利用者が実機で | HIGH | ? |
| ACNL-F0537 | gohan のグリッドカーソルが何も描かなかった2つの原因（2026-09-22、HIGH、実機の状態読み＋静的） | 解析ソフト: IDA / 解析モデル: opus-5。利用者の報告「チートをONにしても表示されません。大きさを200にしても | HIGH | ? |
| ACNL-F0538 | グリッドカーソルを gohan へ。起動時クラッシュの診断とケーブ衝突（2026-09-22、HIGH、静的＋クラッシュダンプ） | 解析ソフト: IDA / 解析モデル: opus-5。利用者の指示で、試験チートを**独立プラグインではなく | HIGH | ? |
| ACNL-F0541 | 同じモデル・アニメ12体の同時描画。実機で30.67fpsを維持し、submit先は溢れない（2026-09-21、HIGH、静的＋実機） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T010。 | HIGH | ? |
| ACNL-F0553 | 行列経路は正常だった。残る差は node+0x228 / +0x22C（2026-09-19、HIGH、実機＋対照） | 設計（`docs/topics/unit_cursor_hw_plan.md` §9）→ 検証（51 件 ok）→ 実装 → 検査（0 failed）→ 適用の順で測定した。 | HIGH | ? |
| ACNL-F0554 | 実機測定で IDA-unknown-F027 を棄却。頂点バッファの束縛は正しい（2026-09-18、HIGH、実機） | 設計（docs/topics/unit_cursor_hw_plan.md）→ 検証（tools/hw/verify_unitcursor_hw.py、45 件 ok）→ 実装（tools/hw/unitcursor_probe.py） | HIGH | ? |
| ACNL-F0556 | メッシュのコマンド列は誰が作るか。「ジオメトリが欠けている」仮説の反証（2026-09-18、HIGH、静的） | IDA-unknown-F025 で「メッシュの GPU コマンド列は 2 本ある」と分かったので、1 本目（頂点属性・バッファ束縛）の出どころを追った。 | HIGH | ? |
| ACNL-F0570 | 店の営業時間判定は店・用途ごとに複製、共通の入口なし（2026-09-17、MEDIUM） | 時刻はDate_GetRaw 0x2FB3A4（&0xACF6B0を返すだけ、466 caller）の[1]>>24、条例はsub_7585A0（[garden+0x621CF] bit1）/sub_7585C4。判定はShopHours_*（IDB命名済み）に複製され、多くはCRO（ModuleDowntown/Outdoor/Indoor/Shop/NpcDt/Club）から匿名インポートで直接呼ばれる。ShopsAlwaysOpenの9語は9関数の「0を返す出口」で関数 | MEDIUM | ? |
| ACNL-F0576 | 正常版と統合版の区別 | F394は利用者が描画復帰・しずえスキップを実機確認した復元基準。ソースはgohanのcommit `fa76dfc05bcc8b362829f53ce48b1593c4099a38`、復元成果物は `artifacts/plugins/f394_verified/`。重複バックアップはGitへ集約済み。 |  | ? |
| ACNL-F0578 | 自立化後の検証 | 構成監査と、親プロジェクトI/O・ネットワークを禁止した既存オフライン検証がPASS。ソース/core/FS、全字形、キーボード10943遷移・15描画場面、しずえ、frontend24ケース、元ARMとの5入力の候補順位、リンク済み命令を照合。gohan/ELFは不変、再ビルド・実機操作なし。根拠はwork/evidence/reorganization/のworkspace_audit.json・isolated_*.json・git_stage.json。Git履歴を保 |  | ? |
| ACNL-F0579 | gohan-gui-simulator のローカル版と公開版が双方向に食い違っていた（解消済み） | `src/CTRPF-GUI-Simulator`（ローカル）を削除し `yak9909/gohan-gui-simulator` の clone へ統一した際に判明。 |  | ? |
| ACNL-F0585 | Pretendoの公表したACNL RCE対策は `0x81` 掲示板パケット（2026-10-04、MEDIUM） | 解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。対象は日本語版更新 `artifacts/update/exefs/code.bin`、SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。Pretendo Nimbusの[公開ソース](https://github.com/PretendoNetwork/nimbus/blob/fc2d813412a6 | MEDIUM | ? |
| ACNL-F0586 | 下位 `0x0C` でgohanの壁抜けを相手へ強制できるか（2026-10-04、MEDIUM） | 解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。gohanの実機確認済み壁抜けは `AcPlayer_UpdatePositionWithFieldChecks 0x64EBE0` 内の3**命令** `0x64F03C/0x64F19C/0x64F1B4` をON/OFFする。gohanのローカルPatchListはコード書換え後にキャッシュを更新する。一方、下位転送種別12の受信 `NetTransfer12_ReceiveTownChunk` | MEDIUM | ? |
| ACNL-F0587 | 屋外XYZを下位 `0x0C` で書くための条件と副作用（2026-10-04、静的MEDIUM／実用性LOW） | 解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。対象は日本語版無印＋更新、原本SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。利用者指定の屋外XYZ `0x33099E50` は2026-09-18のgohan実機記録と、別日のプレイヤー実体 `0x33099E3C` に対する静的 `+0x14` が一致する。前回答の「実体の位置が不明」はこの屋外 |  | ? |
| ACNL-F0590 | HHD の顔の画面が ACNL の下画面の最前面に予想どおり出る・必要なメモリ（2026-10-05、HIGH: 実機の画面と designer の予想の照合 + 実機のメモリ） | 解析ソフト IDA（ida-pro-mcp）、解析モデル opus-5.5。T013 段 1。gohan `work/hhd-charcreate` eb79ee7、3gx SHA-256 0021cca0…3cc6、SD /hhd_charcreate.arc 333,096 B。 | HIGH | S |
| ACNL-F0592 | 実行時のテクスチャ差し替えと性別の読み方を実機で確認（2026-10-05、HIGH: 静的 + 実機） | 解析ソフト IDA（idalib-mcp）、解析モデル opus-5.5。T013 段 3（gohan work/hhd-charcreate 4c6db33、3gx fda07ad4…d0c5）。 | HIGH | S |
| ACNL-F0597 | HHD のキャラクリ画面から ACNL のプレイヤーの見た目を変えられる（実機 全 PASS）（2026-10-05、HIGH: 静的 F080 + 実機） | 解析モデル opus-5.5。gohan work/hhd-charcreate ce17e54、3gx SHA-256 e25dfca4…d8b3、SD /hhd_charcreate.arc 358,184 B。利用者の目視で全項目 PASS: | HIGH | S |
| ACNL-F0599 | 上画面の描画順と「メニューの 3D」モード（Scene 1）、美容室の小物の音、複製の帽子・肌の欄（2026-10-05、MEDIUM: 静的のみ。gohan での使用は実機未確認） | 解析モデル opus-5.5。IDB: `Player_SetHeadGoodsWithSound 0x68B238` を命名・注記。 | MEDIUM | S |
| ACNL-F0600 | 部屋の内部名の表、メッシュ 1 つを半透明で描く命令の挟み方、T018 第 1 段の実機（2026-10-05、HIGH（部屋の表: ID 一覧とゲームの表の 2 経路）/ MEDIUM（半透明: 静的、実機未確認）） | 解析モデル opus-5.5。IDB: `g_RoomInternalNames 0x9515F0`（命名・注記）、`gfx_DrawMesh 0x48D26C` に注記。 | HIGH | S |
| ACNL-F0601 | 目の色は頭のキー、目の形は作るときだけ — 複製の目をすぐ反映する方法（2026-10-05、MEDIUM: 静的のみ。gohan は実機未確認） | 解析モデル opus-5.5。IDB: `PlayerFaceSlot_RequestLoad 0x2711AC` / `PlayerFaceSlot_Unload 0x2711A4` を命名・注記。 | MEDIUM | S |
| ACNL-F0602 | プレイヤー本人の目の形をその場で変える手順・レイアウトの色の 1 要素の読み書き・書体の私用領域の記号（2026-10-06、MEDIUM: 静的のみ。gohan は実機未確認） | 解析モデル opus-5.5。IDB: `nwlyt_Pane_GetColorElement 0x73B508` / `nwlyt_Picture_GetVtxColorElement 0x73CB40` / `nwlyt_Material_SetColorElement 0x4BCC7C` / | MEDIUM | S |
| ACNL-F0604 | 相手側のアクセサリーを残す状態 0xBA、送れなかった件（2026-10-06、MEDIUM: 静的のみ。gohan 未実機） | 解析モデル opus-5.5。IDB: `PlayerState_HeadGoodsExit 0x68A6AC` / `PlayerState_HeadGoodsSyncRemote 0x68C538`（関数を定義）を命名・注記。 | MEDIUM | S |
| ACNL-F0605 | 目の形を通信相手へ伝える経路の調査（T020、2026-10-06、MEDIUM: 静的のみ。実装・実機なし） | 解析モデル opus-5.5。IDB: `sub_61F3DC`（参加時の転送の段階）/ `sub_51C720` / `vc_PLOAD` に注記（意味が LOW のものは改名しない）。 | MEDIUM | S |
| ACNL-F0606 | 目の形を種別 11 で送る実装（T020、2026-10-06、MEDIUM: 静的のみ。gohan e85bac0 未実機） | 解析モデル opus-5.5。IDB: `sub_581FE0` に注記（プロフィール +21656 の 168 B（Mii まわり、状態 +168）を状態 1 → 2 の送る形にする。戻すのは `sub_582160`）。 | MEDIUM | S |
| ACNL-F0608 | 訪問者のプロフィールは固定領域にある（2026-10-06、HIGH: 静的 + 実機の症状が一致） | 解析モデル opus-5.5。 | HIGH | S |
| ACNL-F0609 | gohan の他機能の「自分のプレイヤー」— 問題が出た所と出なかった所の理由（2026-10-06、MEDIUM: 静的 + 利用者の実機の結果） | 解析モデル opus-5.5。F091 の続き（0xAA7994 = 表の 0 番 = ホスト）。 | MEDIUM | S |
| ACNL-F0610 | gohan のリソースを sdmc:/gohan に（2026-10-06、設計 + 静的検査。実機未確認） | 解析モデル opus-5.5。利用者の依頼: 没アイテムのアイコン・名前表・HHD の arc を SD の gohan フォルダから読む。名前表は人が読める形で、タイトル ID ごと（ローカライズ）。 |  | S |
| ACNL-F0613 | 建物プレビューのファイル読み込みは既にゲームの読み込み係のスレッドで非同期（2026-10-06、MEDIUM: 静的） | 解析ソフト: IDA / 解析モデル: opus-5.5。 | MEDIUM | S |
| ACNL-F0614 | 公共事業エディターのプレビュー切り替えの実測（2026-10-06、HIGH: 実機の計測。gohan work/preview-probe 1836acd） | 解析ソフト: IDA / 解析モデル: opus-5.5。 | HIGH | S |
| ACNL-F0615 | ゲームのカタログのプレビューは 2 枠を交互に使い、替えた前の枠は 1 フレーム後にすぐ壊す（2026-10-06、MEDIUM: 静的） | 解析ソフト: IDA / 解析モデル: opus-5.5。 | MEDIUM | S |
| ACNL-F0616 | 待ちを外したプレビューの実測と、HHD が開かなくなった原因（2026-10-06、HIGH: 実機の計測と実機の変数） | 解析ソフト: IDA / 解析モデル: opus-5.5。 | HIGH | S |
| ACNL-F0619 | ACNL の「かざる」の部品と、データだけ書いたときの振る舞い（2026-10-06、静的 + 実機 2 回。置く部品は実機未確認） | 解析ソフト: IDA / 解析モデル: opus-5.5。 | MEDIUM | S |
| ACNL-F0626 | T022 カタログの生成器（Codex 依頼 t022_catalog_arc、gpt-6.1-sol xhigh、2026-10-07。打ち切り。記録 ID なし = 道具と生成物） | tools/hhd/make_catalog_arc.py → work/cache/hhd/catalog/hhd_catalog.arc（5 レイアウト・373 アニメ・57 テクスチャ、構造検査 PASS）、tools/hhd/make_icon_bank.py → hhd_icons.bin（3,723 品。**ETC1A4 3,465 品と ETC1 258 品が混在**: 4,096 B に揃えた版と原本の形の版を作成。ETC1 に不透明のアルファを足す方式の採否 |  | ? |
| ACNL-F0630 | T022 カタログの実機不具合 8 件の原因と修正（2026-10-08、MEDIUM: 静的。実機未確認） | 解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（xhigh）**、Codex（依頼 work/codex/tasks/t022_catalog_fix1.md、--allow-gohan）。採番・照合・commit は親（opus-5.5）。根拠 **work/evidence/t022_catalog_fix1/report.md**。gohan b68e21f（work/decor-catalog）。 | MEDIUM | A |
| ACNL-F0631 | 家具が置けない・壁紙が張り替わらない原因（2026-10-08、HIGH: 実機 BP＋静的） | 解析: 親（opus-5.5）が ida-pro-mcp の BP で測定、Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix2、--allow-gohan）が静的解析と修正。根拠 **work/evidence/t022_catalog_fix2/report.md**。gohan 1746df8。 | HIGH | A |
| ACNL-F0632 | 足したチップが動かない・2 回目の窓のヒープ不足・テントでの壁紙/床タブ（2026-10-08、MEDIUM: 静的。実機未確認） | 解析: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix3。5 時間枠のため停止指示で途中終了、ビルド可の状態）。照合・仕上げ・採番は親（opus-5.5、Codex の枠切れ後）。根拠 **work/evidence/t022_catalog_fix3/report.md**。gohan d059843。 | MEDIUM | A |
| ACNL-F0633 | 改造テントの壁紙/床・自由スクロール・すぐ開く・すぐチップ・位置保持（2026-10-08、MEDIUM: 静的。実機未確認） | 解析: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix4）。照合・commit・採番は親（sonnet-5.5）。根拠 **work/evidence/t022_catalog_fix4/report.md**。gohan 0db52e0（work/decor-catalog）。 | MEDIUM | A |
| ACNL-F0634 | しばらく使うとフリーズする原因 — 読み込みのヒープの枯渇（2026-10-08、実測 + 静的: MEDIUM） | 測定: 親（sonnet-5.5、ida-pro-mcp、固まった状態）。静的洗い出しと修正: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix5）。根拠 **work/evidence/t022_freeze_20261008/README.md**、**work/evidence/t022_catalog_fix5/report.md**。gohan 89a636e。 | MEDIUM | A |
| ACNL-F0635 | 窓が読み込みヒープを食う最大の原因は非表示 TextBox の描画用バッファ（2026-10-09、MEDIUM: 静的。実機未確認） | 解析: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix6）。照合・commit・採番は親（sonnet-5.5）。根拠 **work/evidence/t022_catalog_fix6/report.md**。gohan f43f757（work/decor-catalog）。 | MEDIUM | A |
| ACNL-F0636 | 窓を開けなくなる原因 — 余白の基準（連続空き）が現実の割れ方と合っていなかった（2026-10-09、実測 HIGH + 静的 MEDIUM） | 測定: 親（sonnet-5.5、拒否された後の停止状態）。修正: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix7）。根拠 **work/evidence/t022_heap_20261009/README.md**、**work/evidence/t022_catalog_fix7/report.md**。gohan 1bfb8ca。 | HIGH | A |
| ACNL-F0637 | 家具のチップと窓が読み込みヒープを共有する問題 — 基準の見直しと、アイコン枠を描画命令用ヒープへ（2026-10-09、実測 + 静的 MEDIUM、実機未確認） | 測定: 親（sonnet-5.5、通知が出た後の停止状態）。調査・修正: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix8、枠切れで一度停止して再開）。根拠 **work/evidence/t022_heap_20261009/README2.md**、**work/evidence/t022_catalog_fix8/report.md**。gohan 6ca7158。 | MEDIUM | A |
| ACNL-F0638 | HHD の「壁にかける家具」リストの移植（2026-10-09、静的 MEDIUM、実機未確認） | 調査・実装: Codex gpt-6.1-sol xhigh（依頼 t022_wall_catalog）。照合・commit・採番は親（sonnet-5.5）。根拠 **work/evidence/t022_wall_catalog/report.md**。gohan 3e9654f。 | MEDIUM | A |
| ACNL-F0641 | 村の風船は `AcBalloon` Actorで、生成・破裂・プレゼント配置を既存経路から制御できる | **確度: HIGH（静的実装経路を複数箇所で確認）。チートとしての実機実行は未確認。** | HIGH | B |
| ACNL-F0642 | 通常ドロップをAcBalloon経由へ置換するAR実装 | **確度: MEDIUM（ARM/ABIは静的確認。現行cave移設版は実機未検証）** | MEDIUM | B |
| ACNL-F0679 | inventory completionはnative DropDataではなく非同期synthetic handle 4で十分 | **確度: HIGH（UI/FieldAction構造はGhidra独立静的確認、handle 4成功経路はGhidra-gpt-sol-5.6-F032実機確認）。Ghidra-gpt-sol-5.6-F038実装自体は未実機。** | HIGH | B |
| ACNL-F0680 | 二系統の独立再解析は主要結論で一致し、旧timing説明だけが矛盾していた | **確度: HIGH（main raw bytesのfresh Ghidra decompile + raw ModuleVillage.cro命令列 + 既存hardware observations）。Ghidra-gpt-sol-5.6-F039 AR実装自体は未実機。** | HIGH | B |
