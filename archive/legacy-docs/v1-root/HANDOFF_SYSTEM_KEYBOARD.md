# 内蔵ソフトウェアキーボード解析の再開メモ

## F-407 実機成功: キーボード非起動で候補17/6/143件を取得（2026-09-11、最新・HIGH）

利用者がF407を配置・ACNL再起動/再アタッチ。Suspend/bp0、実機headerと全生成コードアンカー、成果物/現行ソースhashを照合した。要求2の展開・辞書配置・315再配置が成功し全解放された後、要求3で「かんじ」「わたしはねこがすきです」「か」を各1回実行。候補17/6/143件が原本PCと全順位一致。前2入力は保存済み実機SWKBD候補列とも直接一致。「か」は初回50件からgetterが143件まで追加検索し、終端0を確認した。

各要求は既存検証用3gxの独立スレッドで実行。キーボード起動/APTなし、辞書・元codeは内蔵タイトルからRAMへRead、SD/3gxへのリソース同梱なし。内蔵FSのOpen/Size/全Read/CRC/Close/Releaseすべて成功、5 MiB arenaのFree完了。変換3要求はstage10/state2/failure0、prepared1/executed1/exhausted1/stack_guard1/freed1。arenaは各回0x061BE000。各5000ms走行後の観測であり、変換時間そのものの測定ではない。

結果はSYSTEM_KEYBOARD/evidence/f407_engine/hardware_prepare.json、hardware_kanji.json、hardware_phrase.json、hardware_ka.jsonへ個別保存。report全34452 bytesを別の実機読取りで保存し143候補を独立に再デコードして一致。hardware_verified.json、hardware_final_report.bin、hardware_final_state.json参照。ソース・3gx/ELF・検証器・実機証拠をBACKUP/plugin_f407_hardware_confirmedへ保存。

最終ACNL Suspend(-1)、PC0x0056085C、bp0、command0。実機はF407版（SHA50ec21a1bde6d52f13fa916ac23aceb2f81dbb833a5ca4db8ca77c3b96368385、exe258048/heap10227712）、report0x07033AE0、command0x07033ADC、input0x0703212C。試験arena/FS handle保持なし。F407はゲームコードをフックしないため、この試験で追加した復元待ちフックなし。F406の一時変更は前bootで復元済み。正常gohan/F404ファイルも不変。

詳細DOCS/system_keyboard_native_loader.mdとPlugin/SwkbdEngineProbe/README.md。今後追加試験するならengine_probe_live_f407.pyの既定inspectから現在値を確認し、要求を1回だけ設定してrun_timed.pyで走らせる。自前メニュー統合を前提にしない。

残る未確認事項: 個人学習/ユーザー辞書、長文上限や全入力、明示的な文節境界指定APIの実機試験、並行呼出し、ロードと変換の処理時間内訳。今回の文章6候補取得を、文節境界編集APIまで確認したものとは扱わない。キーボード非起動・実機内蔵資源の取得・再配置・独立contextの予測候補列挙という今回の経路は成功済み。以下は準備時点と過去の履歴。

## F-407 PC準備時点の履歴（配置待ちは解消済み）

独立Plugin/SwkbdEngineProbe/swkbd_engine_probe.3gxを作成。289,985 bytes、SHA50ec21a1bde6d52f13fa916ac23aceb2f81dbb833a5ca4db8ca77c3b96368385。ソース/ホスト/ARM構文を検証してからビルド。生成1301命令/213直接分岐/48PCリテラルの検査、生成ARMから原本エンジンへの一連のPC試験、mailbox誤適用防止10条件までPASS。展開はctrtool出力と全bytes一致、6辞書と315再配置も照合。PCで「かんじ」17件、文章6件、「か」143件が原本実行と順序一致。保存対象レジスタ/FPSCR/SPとstack guard、辞書本体不変も確認。

F407は実機未配置・未実行。最後の実機読取りはACNL Suspend/PC0x00463E24/bp0、F404 header exe217088/heap10268672、slot0x07029DD8=0x070012B8。F406の一時変更は全復元済み。F407の予期headerはexe258048/heap10227712なので、旧版へ新mailboxを書かない。PCからSDのタイトルフォルダは見えていない。利用者による検証版の入替え→ACNL再起動→IDAアタッチ/Suspendが必要。実機側のF407変換成功はまだ主張しない。

次はSYSTEM_KEYBOARD/engine_probe_live_f407.py（既定inspect）でheader/全アンカー照合。action prepareで要求2を一度だけ設定→run_timed.py→inspect、prepared1/executed0/freed1と全FS成功を保存。それからaction convert/text「かんじ」の要求3を一度だけ設定して最小候補照合。driverは成功した準備結果が現bootにないとconvertを拒否。Resumeは別操作、要求の再送をしない。state1ならstageを記録して進捗を確認。辞書/元codeをSDや3gxに同梱しない。gohan/F404ファイルは不変。BACKUP/plugin_f407_pc_verifiedへソース/ELF/3gx/検証結果を保存した。

詳細DOCS/system_keyboard_native_loader.md、Plugin/SwkbdEngineProbe/README.md、証拠SYSTEM_KEYBOARD/evidence/f407_engine/。以下はF406以前の完了記録。学習/ユーザー辞書/並行利用/全入力の保証は残る。

## F-406 実機ヒープコード実行成功・全復元済み（2026-09-11、最新）

F-405の停止はユーザー提供dumpでカーネルのD-cache clean by MVAに確定。F-406では全体cache SVC 0x92/0x94へ変更し、組立前ソース検査・全4リテラル/1分岐・4条件ABI試験・実機の領域/アンカー照合後に1回だけ実行した。plugin heap 0x061BE000の2命令から0x5Aが返り、control phase4を確認（HIGH）。後続の5 MiB全域照合、内蔵辞書/code全Read/CRC/Close/Release/freeもstate2/failure0で成功。これは最小コードの実行成功であり、変換エンジン本体/VFP/実機候補取得は未検証。

結果をSYSTEM_KEYBOARD/evidence/f406_exec/hardware_result.jsonへ保存後、vtable slot0x07029DD8を0x070012B8へ復元。cave0x00838600の予約全0x200 bytes、control0x009BE840の全0x20 bytesはbackup一致。別の読取りでもゼロ/元vtable/command0を確認しrestored.jsonへ保存。最終ACNL Suspend(-1)、ARM32、PSR0x20000010、PC0x00463E24、SP0x32283B98、bp0。map APIの空リストは未マップ判定に使わない。試験buffer/handles保持なし。F-396 launcherは再起動後に未再適用。

現行の実機プラグインと3gxファイルは独立Plugin/SwkbdProbeのF-404版。gohan正常版は変更なし。次は内蔵取得codeのRAM展開/再配置・辞書context初期化・実機候補照合。辞書やcodeのSD/3gxリソース同梱、自前メニュー統合はしない。詳細DOCS/system_keyboard_plugin_probe.md。

## F-405 解決: キャッシュ処理中のクラッシュ、再起動で一時変更解除

Plugin/crash_dump_00000004.dmpのPC0xFFF2B3F8はMCR p15,0,R1,c7,c10,1。R1=FAR=0x061BE000が試験arenaと一致し、DFSR0x805はsection translation fault/write。ARM11 core1、SVC mode、保存プロセスsocket/TID0x0004013000002E02。ダンプ解析とidalibの保存命令列を照合（HIGH）。他コアの異なるアドレス空間が原因というdispatch仮説はLOW、svc0x91/0x93のどちらかは不明。ユーザー再起動後に旧cave/controlゼロ、元vtable、mailbox idleを確認した。F-405を再実行しない。以前の「結果未回収」は解消済み。pending_state.jsonに解決を記録し、旧記録はpending_state_before_resolution.jsonに保存。

## F-404 実機成功: 3gxで5 MiB確保・内蔵FS読取り（2026-09-11）

利用者が独立swkbd_probe.3gxを配置しACNLを再起動。新規header/生成コードアンカーを照合、Suspend/bp0を確認してmailboxに1要求を設定。5秒の自動Suspend付きResume後、state2/failure0。5,242,880 bytesを確保して全域write/readback成功、内蔵辞書2,045,891 bytesと圧縮.code 471,668 bytesのOpen/GetSize/全体Read/CRC32一致/Close/handle解放がすべて成功。buffer free完了、ログ書出しも成功。現在Suspend/PC0x00137064、command0、試験buffer保持なし。hardware_result.jsonを保存。3gx側で予定の検証容量を確保できた。エンジン本体はまだ実行していない。次は展開・再配置・実行権限と実機候補取得。詳細DOCS/system_keyboard_plugin_probe.md。


## F-403完了・F-404 3gx検証へ移行（2026-09-11）

最新はDOCS/system_keyboard_plugin_probe.md。全辞書2,045,891 bytesの実機取得と全bytes/SHA照合、6辞書個別照合が完了。一時handle/buffer/wrapperは全復元済み。エンジン実機実行は未実施。
System/lyt heapの空きは小さいが、全heapの調査は未完。利用者の指定で3gx側メモリを検証する。現行pluginの総枠5 MiBは実機headerと一致、Lumaは10 MiB設定に対応。独立のPlugin/SwkbdProbeで5 MiBの一時確保・内蔵FS読取り・全解放を検証予定。10 MiBの実機確保は未確認。辞書SD/3gx同梱や自前メニュー統合はしない。gohan正常版を維持。最終読取りstate=-1/PC0x0014E378。


## F-402 完了（最新）

DOCS/system_keyboard_native_fs.md。ACNLから内蔵辞書Read成功、code kind2の全471668bytes Readと全bytes照合成功。展開後も既存解析対象と一致。一時heap/handlesは解放済み、追加wrapper全域を復元済み。frame hookは0xEB09A7E7、既存launcher維持。ACNL最終Suspend/PC0x004EF364/bp0。gohan.3gx不変。現在一時FS試験は未設置。
次は全辞書読取り→code展開/再配置→実機context/候補取得。エンジン実機実行はまだ行っていない。codeパスkind1は失敗、kind2 .codeで全体Readが成功した。OS追加RAM不足のため今回の全体Readだけgame heapを借りて返却した。以降の設計を自前メニューへ依存させない。以下の未cleanup状態は解消済みの履歴。

## F-402 最新: 実機全体Read成功、後片付け未確認

RE/STATE.md先頭・DOCS/system_keyboard_native_fs.md・scratchpad/MEMO_f402_native_fs.mdを読む。辞書Readとcode全471668byte Read成功。codeはkind2。v3frame wrapper336bytesは未復元、scratch一時buffer0x32DFC000/475136bytesは未解放。code handle0x568054にCloseをarmしてResumeした後、capture+Releaseと停止状態照会がタイムアウト。ユーザーへ停止表示/ダイアログ確認を依頼中。pending callの状態を確認し、dump/照合→handle cleanup→heap_free→revertを完了する。取得したSWKBDコードは未実行、プラグインファイル変更なし。以下のキャンセル待ち/v1未実行は過去記録。

## 最新 F-402進行中: 実機試験用wrapper適用済み

RE/STATE.md先頭を必ず読む。追加frame wrapper0x838400とscratch0x9BE800、hook0x5CE29C=0xEB09A857。既存launcherへtail-chain、要求state0で未実行。ACNLはSuspendのまま。ユーザーに内蔵キーボードキャンセル報告を依頼中。native_fs_live.pyとevidence/f402_step/backup.jsonで実行/復元。終了後は一時フックをrevertする。プラグインファイル変更なし。

## 最新 F-401（2026-09-10）

再開先はDOCS/system_keyboard_relocation_audit.md。静的な直接参照を243アドレスまで追跡し、再配置表315語を検証。25入力×2配置先の50比較で候補列・順位が原本一致。7入力の間接callback検査もPASS。ただし実行されたBLXは22箇所中5箇所で、全経路保証ではない。

LumaのFS権限設定を公式の固定commitで確認し、内蔵辞書RomFSとSWKBD ExeFS codeをarchive 0x2345678AからRAMへ読むパスを準備した。実機のOpen/Read成功とネイティブ実行は未検証。次は読取り専用試験でResult/サイズ/同一性を取得する段階。SDや3gxへのテーブル同梱はしない。今回実機接続・適用・ビルド・プラグイン変更なし。

完全な静的証拠はSYSTEM_KEYBOARD/evidence/f401_static_scan.json。中間checkpointには省略された出力が残るため、最終証拠を上書きしない。再現はexpand_static_relocations.py、verify_static_relocation.py、verify_relocated_callbacks.py、prepare_builtin_content_paths.py。過去の実機アドレスや停止状態を現在値と仮定しない。

## 最新 F-400: 再配置のPC試験成功・テーブル同梱を避ける方針

利用者はSD/3gxへテーブルをリソース同梱する方式を避けたいと指定。
内蔵辞書RomFSとSWKBD ExeFS .codeを実行時にRAMへ読む方式を候補とし、実機権限は未検証。
52箇所の観測絶対参照を全件idalib xrefで照合。callback3個と合わせ移設し、
元VAをunmapして0x04100000/0x06100000から候補列が一致。未修正コピーは旧19094Cで停止。
これはPCでの再配置可能性の確認。全経路閉包/学習/異なる版の対応は未完。
DOCS/system_keyboard_relocation.md、probe_relocated_engine.pyとf400証拠JSON参照。
今回実機アクセス/ビルド/SD/3gx変更なし。次は全参照の静的網羅と内蔵タイトル読取り権限の確認。


## 最新 F-399: 画面・APTなしのエンジン実行をPCで確認

初期化から全候補列挙までOS mockなし。原本data/BSSをRO化しても17/6件一致。
data/BSSを除去し0x1B8000の静的表1ページだけ保持しても一致。全除去は0x19BFA8で停止。
idalibの0x19BF00→0x1B8FD0参照と対応。書込みは独立context/stack/io/辞書poolのみ。
実機保存候補との照合6試験PASS。原本は絶対jump table/定数pointer/VFPを使用。
3DS上の独立モジュール化は有力だが、再配置・実行領域・RAM/ABI/時間の検証が必要。
今回実機接続/ビルド/3gx変更なし。DOCS/system_keyboard_engine_only.mdと
SYSTEM_KEYBOARD/audit_engine_only.py、evidence/f399_engine_dependencies.jsonを参照。


## 最新 F-398: UIなしのPC候補取得が完成

DOCS/system_keyboard_full_candidates.mdを参照。query_candidates.py TEXTで全候補をJSON出力。
原本callback辞書slot7..9を追加し、実機保存のかんじ17件・文章6件と順序まで一致。
旧Probe既定値は維持、新APIはui_callbacks=True。原本getterが追加検索し初期50件も超えられる。
verify_full_candidates.py PASS。未学習baselineであり個人学習/実機アプレット非起動は今後の課題。
今回実機アクセス/ビルド/プラグイン変更なし。F-397の1→6件をUI段階差とした解釈は訂正済み。


## 最新 F-397: 未確定の全文候補と内部文節を取得

今回の「わたしはねこがすきです」はmode0、候補6件、先頭「私は猫が好きです」。
mode1文節件数は0だが、予測type0x1012の別リストapp+0x2E6DC、u16件数app+0x2F9C4に3件。
読み境界0,4,7,11（わたしは/ねこが/すきです）、独立PC変換片は私は/猫が/好きです。
全recordがポインタ等8 bytes以外一致し、連結も実機表示と一致。UI対象範囲は全文[0,11)。
現在のACNLはSuspend（PC0x00137064、bp0、state2/run1）、SWKBD PID50は取得後detach済み。
入力確定・候補選択は行っていない。今回の指定入力は追加操作なしで取得完了。
下記の「観測待ち」「移設後未起動」は過去の記録。
詳細DOCS/system_keyboard_prediction_segments.md。生証拠evidence/phrase_prediction/。
verify_prediction_segments.pyで原本ARM読取＋独立PC照合を再現できる。

## 最新 F-396: 再起動後、移設して再適用済み

旧SWKBDケーブは現在のGUI v2 A2/Nと重なる。旧0x00838D20の適用/消去は禁止。
現行SYSTEM_KEYBOARD/*.pyは0x00838200..0x00838400へ更新済み。
chat hook 0x001938AC=0xEB1A9253、frame hook 0x005CE29C=0xEB09A7E7。
事前/事後/旧版差分/実機監査/独立読み戻し検証を通過。GUI/しずえhookと正常3gxは不変。
現在Suspend、PC=0x00137064、bp=0、state=0/run_count=0。移設後はまだResumeしていない。
次は通常チャット起動後、「わたしはねこがすきです」を確定せず、予測状態の観測から進める。
新しいSWKBD PID/ポインタを取り直すこと。詳細scratchpad/MEMO_f396_swkbd_reapply.md。
以下「利用者へ現在の起動可否を確認中」はF-395時点の履歴。

## 最新 F-395

UIが呼ぶ0x1145ACはR3=1、F-363の直接連文節試験は55。原本PC実行でも結果が異なる。
複数語を入力すれば自動的に文節一覧が得られる、という前提は置かない。
文節record app+0x36890、件数app+0x37B7Aを特定し、保存dump検査器を作成。
旧実機「かんじ」はmode0、予測17、文節0だった。
次は実機で変換操作前後のmodeとeditor対象範囲を比較する。
詳細DOCS/system_keyboard_phrase_state.md、再現SYSTEM_KEYBOARD/verify_ui_phrase_route.py。
現在の通常チャットが内蔵キーボードを起動するか利用者へ確認中。新規実機操作なし。

## 目的と現在地

目的は3DS内蔵のかな漢字変換辞書・確定前候補の取得。
自前メニューやgohan.3gxへの組込みは目的ではなく、その設計に依存させない。
フレンドチャットは使えないため、ACNLの通常チャットと既存APT管理を使用する。
しずえスキップの復旧対応を挟んだが、F-394で自前メニュー復帰とスキップ成功を
利用者が実機確認した。正常版はBACKUP/plugin_f394_hardware_confirmed/。

## 完了した確認

- 通常チャットを開くと内蔵キーボードが起動し、取消後にゲームへ安全に復帰（利用者報告とAPT結果照合）。
- 「漢字テスト」を確定し、UTF-16の返却と正常復帰を確認。チャットへ投稿する設計とは別。
- 入力「かんじ」を未確定のままSWKBD側を読取り、全17候補を回収（F-389）。
- 順序: 感じ、頑丈、感情、元日、幹事、感じる、肝心、勘定、患者、漢字、監事、寛治、完治、寛二、かんじ、カンジ、ｶﾝｼﾞ。
- 先頭6件はUTF-16表示cacheと候補recordで一致。index 0..13は実行時アドレス欄を除き
  F-363のPC結果と一致。末尾3件は実機recordを原本ARM decoderで復号。
- SWKBD実行コード655,360 bytesが提供イメージと一致。ACNLをSuspendしてもSWKBDは
  別プロセスで動くため、候補取得ではSWKBD側の停止・状態確認が必要。

## 次の調査

複数文節入力時のphrase result領域と文節境界を追う。
既存の表示cache/17候補列だけから文節境界を推測しない。
まずDOCS/system_keyboard_conversion.mdのF-363とF-389、SYSTEM_KEYBOARD/probe_conversion.pyを
確認し、既にPC上で再現済みの文節変換・境界指定を実機観測へ対応付ける。
読取り領域・検証手順を設計した後で、対象プロセスと実行状態を確認して観測する。
ビルド・実機適用の前には検証を行う。今回は文書化とバックアップのみで実機アクセスなし。

## 読むファイル

- scratchpad/MEMO_swkbd_normal_chat_apply.md: 起動・取消・確定・全17候補取得の詳細。
- DOCS/system_keyboard_conversion.md: 順位・文節変換の静的/PC証拠、F-387/F-389。
- DOCS/system_keyboard_normal_chat.md: 通常チャットの既存ゲーム経路。
- SYSTEM_KEYBOARD/evidence/live_candidates_kanji.json と同名の各bin: 一次取得物。
- SYSTEM_KEYBOARD/parse_live_candidate_dump.py: 保存済み候補dumpのオフライン復号。
- SYSTEM_KEYBOARD/read_live_candidates.py: 停止したSWKBDプロセスの読取り専用取得。
- SYSTEM_KEYBOARD/live_candidate_layout.py、verify_live_candidate_reader.py: 配置・検証。
- SYSTEM_KEYBOARD/native_chat_launcher.S と検証/適用スクリプト: 試験用ランチャー。

## 過去の実機値は再利用前に確認する

旧記録のSWKBD PID 60、GDB port 4001、app pointer 0x08292880はその取得時点だけの値。
ACNL側の旧設置記録: chat hook 0x001938AC、APT hook 0x005CE29C、
cave 0x00838D20..0x00838F20、control 0x009BDD00、config 0x009BE000/0x009BE400、
shared page 0x009BF000..0x009C0000。現在も設置済みとは仮定しない。
新しいbootでは、フック素値、ケーブ/.bssの利用状況、GUIとの重なりを改めて検証する。
F-393のSIGSEGV停止PCも過去の記録。今回の利用者報告は復帰済みで、現在のPC等は未取得。
