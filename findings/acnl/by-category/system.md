<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / system

| ID | 題 | summary | 確度 | 格付け | 訂正 |
|---|---|---|---|---|---|
| ACNL-F0006 | F-406 実機ヒープコード実行成功・全復元済み（2026-09-11、最新） | F-405の停止はユーザー提供dumpでカーネルのD-cache clean by MVAに確定。F-406では全体cache SVC 0x92/0x94へ変更し、組立前ソース検査・全4リテラル/1分岐・4条件ABI試験・実機の領域/アンカー照合後に1回だけ実行した。plugin heap 0x061BE000の2命令から0x5Aが返り、control phase4を確認（HIGH）。後続の5 MiB全域照合、内蔵辞書/code全Read/CRC/Close/Release/ | HIGH | ? |  |
| ACNL-F0011 | F-402 実機結果更新 | ACNLから内蔵辞書のOpen/Size2045891/先頭256byte Read/Close/Releaseが成功。読取りsampleは提供NCCHの0x1200と一意一致（HIGH:静的経路と実測）。SWKBD codeはkind1OpenがE0E046BE、kind2 .codeはOpen/Size471668成功。先頭256byte ReadはE0C046F9、全体471668byte Readは成功。FSのRead返信byte数も471668。全bytes同一性は | HIGH | ? |  |
| ACNL-F0012 | F-402進行中: ACNL自身の内蔵タイトルFS経路（MEDIUM） | idalib code.bin.i64: sub_1304C8はIPC0x08030204、TLS+0x80へarchive/fileのbinary pathを詰めSVC32。sub_346AB8はarchive0x2345678A/16byte archive/20byte file/READ1で同関数を呼び、sessionはdword_96EF28。独立caller sub_1290C4も同sessionを使用。libctru fs.cのOpenFileDirectly定 | MEDIUM | ? |  |
| ACNL-F0026 | F-372: ACNL既存APTの実行文脈候補と失敗分岐のPC検証（2026-09-08） | **MEDIUM、実機アクセスなし。** 利用者が既存APT経路を第一候補に指定し、実機操作を保留。 | MEDIUM | ? |  |
| ACNL-F0027 | F-364: ACNLの内蔵キーボード起動候補経路・APT/GSP契約・ABIの検証（2026-09-08） | **confidence MEDIUM。** `code.bin.i64`の静的解析、停止中実機の読み取り、原本ARMの局所実行。 | MEDIUM | ? |  |
| ACNL-F0081 | F-43 RTTI からクラス名を引ける — `HIGH` | 出典: `REFERENCES/TEXTS/classes.txt` / `2.txt` / `1.txt`。**実機メモリで裏取り済み。** | HIGH | ? |  |
| ACNL-F0083 | F-45 `NCCH/exefs/code.bin` は実機とは別ビルド — アドレスが対応しない — `HIGH` | ExeFS の `.code` は `0x00100000` にロードされ、`.text` / `.rodata` / `.data` が | HIGH | ? |  |
| ACNL-F0142 | F-104: ★single-step 無効なら breakpoint が使える。`GpuCmd_SplitAndSubmit` の呼び出し元を捕捉 | confidence: **HIGH**（実機で breakpoint ヒットを観測） | HIGH | ? |  |
| ACNL-F0173 | F-135: `code.bin.i64` と `code_runtime.elf.i64` の独立照合 — `HIGH`（同一バイト列・アドレス）/ `MEDIUM`（実機での意味づけ） | 前回の「確定」を、別 IDB と別経路で再監査した。`code_runtime.elf.i64` は実機から取得した | HIGH | ? |  |
| ACNL-F0185 | F-159: コードケーブに使える領域は `0x01E82000` で終わる — `HIGH`（実機で読み書き検証） | `0x01E82000`-`0x01E821FF` は **128 ワードすべて `0xFFFFFFFF`**、 | HIGH | ? |  |
| ACNL-F0187 | F-161: ★★ケーブは `.text` 末尾のゼロ埋めに置く。ただし `.text` へは書けない — `HIGH`（実機の SIGSEGV と復帰で確認） | これまで全ケーブが使っていた `0x01E81000`-`0x01E81FFF` は、 | HIGH | ? |  |
| ACNL-F0189 | F-163: ★CTRPF プラグインは GPU 可視メモリを確保できない — `HIGH`（実機で検証、結果コードまで確認） | `Plugin/CTRPluginFramework-BlankTemplate-0.8.0` に検証エントリを追加して実機で実行。 | HIGH | ? | 訂正あり |
| ACNL-F0190 | F-164: `g_GfxAllocator` の正体と呼び出し規約を確定 — `HIGH`（静的解析、assembly まで確認） | `Render_InitGlobal`(`0x4E97CC`) が組み立てている: | HIGH | ? |  |
| ACNL-F0191 | F-165: ゲームのアロケータをフックから呼べた。0x80 境界・linear 窓内 — `HIGH`（実機） | 適用: `PATCHES/cave_gfxalloc_probe.py` | HIGH | ? |  |
| ACNL-F0196 | F-170: CTRPF は発行点の問題を解決しない。cursor は値渡しでグローバルに無い — `HIGH`（静的解析、assembly で確認） | 「発行点の問題は CTRPF で実行すれば解決するのでは」という指摘を受けて確かめた。 | HIGH | ? |  |
| ACNL-F0246 | F-221: ★★ゲームのアロケータから取れるのは 0x4000 まで — `HIGH`（実機） | グリフアトラスを 256x128 LA4（32KB）にしようとして `Alloc(0x8000, 0x80)` を試したが | HIGH | ? | 訂正あり |
| ACNL-F0248 | F-223: ★★★★描くものが無いのに記録を強制すると、しばらくして GPU コマンドリストが枯れる — `HIGH`（実機） | 自前 GUI を ON にして**しばらく遊ぶと**クラッシュした。 | HIGH | ? |  |
| ACNL-F0333 | F-309: nw::lyt のヒープは `sead::ExpHeap`。残量は 1,200,132 バイト — HIGH | > F-308 の残件（実残量が未確定）の解決。**推測ではなく取得子の逆アセンブルで確定**した。 | HIGH | ? |  |
| ACNL-F0334 | F-310: 場面転換をまたぐと空きは 1.2MB → 0.6MB まで落ちる — HIGH | > F-309 の残件。**利用者に操作してもらって**測った（タイトル画面から進める・住民に話しかける等）。 | HIGH | ? |  |
| ACNL-F0339 | F-313: 「実測でないと決められない」は誤り。静的に決着した — HIGH | > F-312 D で `LIST_SIZE` を上げられるか・1 文字あたり何バイトかを | HIGH | ? | 訂正あり |
| ACNL-F0340 | F-314: F-313 の裏取り。1 件は誤り、2 件は独立に裏付けが取れた — HIGH | > 「決め付けず裏取りする」ため、F-313 の結論を他の点・他のプログラムと突き合わせた。 | HIGH | ? |  |
| ACNL-F0341 | F-315: F-312〜F-314 を実機で検証。**結論はすべて正しかった** — HIGH | 自前ノードのコマンドリストが両画面とも作れた。 | HIGH | ? |  |
| ACNL-F0343 | F-315 追記: 1 度目のクラッシュについて（原因は未確定） | 同じ構成（借用 `0x50000` + `LIST_SIZE 0x10000`）が **2 回目は問題なく動いた**。 |  | ? |  |
| ACNL-F0344 | F-317: ★取り外しでコマンドリストを削除しておらず nngx ヒープが漏れる — HIGH | `detach` → `Free` → フック復帰 → ゼロ埋め、で | HIGH | ? | 訂正あり |
| ACNL-F0370 | F-344（2026-09-07）: ★手紙を開くと落ちる — 借用が nw::lyt ヒープを枯らしていた | **confidence: HIGH**（実機の停止位置・レジスタ・オブジェクトの中身 + 逆アセンブルの双方） | HIGH | ? |  |
| ACNL-F0371 | F-345（2026-09-07）: 手紙は **2 つの大きな塊**を要る — 借りっぱなしでは通せない | **confidence: HIGH**（実機の停止位置・オブジェクトの中身 + `sub_1FC55C` の逆コンパイル） | HIGH | ? |  |
| ACNL-F0382 | F-356（2026-09-07）: ★「ゲームスピード変更」チート `0054C6E8` の正体 — フレームペーシングの無効化 | confidence: **HIGH（静的）** / 実機での効果確認は未実施（利用者の報告のみ） | HIGH | ? |  |
| ACNL-F0383 | F-357（2026-09-08）: ★FPS だけ上げてゲーム速度を据え置くことはできない（実機計測つき） | confidence: **HIGH**（静的にループ構造を確定 + 実機で周期を計測） | HIGH | ? |  |
| ACNL-F0387 | F-359（2026-09-08）: ★起動シーケンスと「しずえ画面 → 村へ出る」経路（＋未知のコード領域の発見） | confidence: **HIGH**（静的 + 実機 bp で確定）。詳細は `scratchpad/MEMO_f359_boot_sequence.md`。 | HIGH | ? | 訂正あり |
| ACNL-F0388 | F-361（2026-09-08）: ★★★ACNL は CRO 動的モジュールを使う — しずえ画面を静的に解いた | confidence: **HIGH（静的で完結。実機のバイト列と 1 命令も違わず一致）**。 | HIGH | ? |  |
| ACNL-F0395 | F-368（2026-09-08）: クラッシュ点の特定（実機デバッグ。ida-pro-mcp 直読み） | F-367 の静的監査に続き、ライブセッションへ接続して PC・レジスタ・ | HIGH | ? |  |
| ACNL-F0396 | F-369（2026-09-08）: クラッシュ原因は遷移フレームでの発火。安定ゲートで対策 | F-368 からの続き。利用者の申告： 項目ON・通知なし・ |  | ? |  |
| ACNL-F0397 | F-370（2026-09-08）: クラッシュ再発。犯人は呼び出し元の this=NULL | 前回と同じ PC=`0x0054C438`（`LDR R0,[R4,#0x148]`）だが今回は R4=`0x0`。 |  | ? |  |
| ACNL-F0402 | F-375（2026-09-08）: タイトルで即クラッシュ — 空リスト＋陳旧リンクの永久スキップ | 利用者の申告： タイトル画面で自前メニューONにしただけで動かなくなる。 |  | ? |  |
| ACNL-F0413 | F-388: ACNLのSuspendでは動作中SWKBDプロセスは停止しない（2026-09-09） | 利用者が内蔵キーボードへ未確定の`かんじ`を入力したまま現在のIDAでSuspendしたところ、 |  | ? |  |
| ACNL-F0452 | 自前で作ったものを全部解放できた。ヒープは1バイト単位で元に戻る（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T005。**このプロジェクトで初めての解放。** | HIGH | ? |  |
| ACNL-F0453 | セッションで作った全部を解放。親ヒープへ 467,056 B が戻った（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-F022 の手順を**このセッションで作った全オブジェクト**へ広げた。 | HIGH | ? |  |
| ACNL-F0457 | `G3dResHolder_Dtor` はヒープ破棄の**前**に呼ぶこと。逆にすると SIGILL（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。**こちらの手順ミスで踏んだ。再現条件と復帰手順ごと残す。** | HIGH | ? |  |
| ACNL-F0497 | ゲームの SVC は 32 種類・745 か所（2026-09-25、HIGH: 命令語＋逆アセンブル、名前は libctru と 3dbrew の 2 資料で一致） | 再現 `tools/svc/scan_svc.py` → `work/evidence/svc/svc_sites.json`。文書 `docs/topics/svc.md`。 | HIGH | S |  |
| ACNL-F0509 | 更新データの RomFS は ARCHIVE_ROMFS をファイルパス {5,0,0} で開く（ゲーム自身の開き方）（2026-09-24、MEDIUM（静的＋実機で失敗の側を確認）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の報告「0xFA・0xFB はプレビューが無いと通知されるが、置くとモデルがある」。 | MEDIUM | S |  |
| ACNL-F0530 | 更新タイトルの RomFS は開けなかった（2026-09-22、HIGH（事実）、原因は未解明） | 解析ソフト: IDA / 解析モデル: opus-5。利用者の実機報告： | HIGH | ? |  |
| ACNL-F0531 | `ARCHIVE_ROMFS` が返すのは **base だけ**。8,629 本（2026-09-22、HIGH、実機計測） | 解析ソフト: IDA / 解析モデル: opus-5。利用者が実機で「一覧を作る」を押した結果。 | HIGH | ? |  |
| ACNL-F0532 | RomFS の開き方を 3 箱所間違えていた（2026-09-22、HIGH、実機＋libctru ソース） | 解析ソフト: IDA / 解析モデル: opus-5。利用者報告:「一覧を作るを押すと | HIGH | ? |  |
| ACNL-F0540 | park の BP は焼き付かない。直前に外した番地だけが一時的に拒む（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。 | HIGH | ? |  |
| ACNL-F0544 | 親ヒープの残りは実測できる。確保量は35倍過大だった（2026-09-21、HIGH、実機） | 解析ソフト: IDA / 解析モデル: opus-5。2 体目の資源ヒープ `0x40000` が **0 を返して失敗**した。 | HIGH | ? |  |
| ACNL-F0613 | 建物プレビューのファイル読み込みは既にゲームの読み込み係のスレッドで非同期（2026-10-06、MEDIUM: 静的） | 解析ソフト: IDA / 解析モデル: opus-5.5。 | MEDIUM | S |  |
| ACNL-F0629 | T022 の窓が開かないのは読み込みのヒープ不足（2026-10-08、HIGH: 実機の値＋静的） | decor_catalog2 の実機（ida-pro-mcp、停止中に s_win_state ← Loading を書いて観測）: 窓の arc は読めている（s_catFile あり、517,032 B）。OpenWindow のレイアウト 3 つ・アニメ 9 つ・格子のペイン 45 は全部できていて、 | HIGH | S |  |
| ACNL-F0644 | crash_dump_00000006 の直接fault | **確度: HIGH（dump＋本体命令列）。timing raceという旧帰属は撤回。** | HIGH | B |  |
