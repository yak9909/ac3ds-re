# TODO

## 2026-09-12 GitHub転送タスク完了

main/IDA/Ghidraを作成し、指定6フォルダ全件のIDAへの送信・照合完了。Ghidraは将来の解析資料/プロジェクト待ちで今回の転送漏れではない。再開時は [GITHUB_UPLOAD.md](../project_v2/work/GITHUB_UPLOAD.md) の完了記録を読み、初回の認証失敗や送信中メモを再実行しない。

## 2026-09-12 チャット漢字候補：実装・ビルド・PC検証完了

次は新しいgohanの最小実機確認（普通チャットで「かんじ」→自前メニュー「チャット漢字候補」→一覧/取消/再実行、既存UIとしずえ遷移）。まだ適用/Resumeしていない。作業開始前にboot・現行プラグイン・停止状態を取り直す。[手順と復元先](../project_v2/docs/topics/chat_kanji.md)。

## 2026-09-11 環境整備タスク完了

次回は [project_v2/work/STATE.md](../project_v2/work/STATE.md) → [SKILLS.md](../project_v2/SKILLS.md)。内蔵変換研究の残る課題は [keyboard.md](../project_v2/docs/topics/keyboard.md)。以下の古い準備記録を未完了タスクとして再実行しない。

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

### 残る検証

- RAM上の圧縮.code展開をctrtoolの既存出力と全bytes照合する。原本版と315語の再配置表の整合を確認し、想定外の版は実行前に止める。
- 内蔵RomFSの構造から6辞書を切り出す。既知offsetへの決め打ちを本番の解析器にしない。独立context、領域境界、入出力長を検証する。
- 原本関数の引数、stack/VFPの保存とスタック容量を確かめ、まず1入力で候補列を取得する。PCでの原本実行と保存実機候補を独立比較に使う。
- 解放・復帰・処理時間を実測した後に入力数を増やす。F-406の2命令成功をエンジン全経路や全入力の保証にしない。

## F-404 実機成功: 3gxで5 MiB確保・内蔵FS読取り（2026-09-11）

利用者が独立swkbd_probe.3gxを配置しACNLを再起動。新規header/生成コードアンカーを照合、Suspend/bp0を確認してmailboxに1要求を設定。5秒の自動Suspend付きResume後、state2/failure0。5,242,880 bytesを確保して全域write/readback成功、内蔵辞書2,045,891 bytesと圧縮.code 471,668 bytesのOpen/GetSize/全体Read/CRC32一致/Close/handle解放がすべて成功。buffer free完了、ログ書出しも成功。現在Suspend/PC0x00137064、command0、試験buffer保持なし。hardware_result.jsonを保存。3gx側で予定の検証容量を確保できた。エンジン本体はまだ実行していない。次は展開・再配置・実行権限と実機候補取得。詳細DOCS/system_keyboard_plugin_probe.md。


## F-403完了・F-404 3gx検証へ移行（2026-09-11）

最新はDOCS/system_keyboard_plugin_probe.md。全辞書2,045,891 bytesの実機取得と全bytes/SHA照合、6辞書個別照合が完了。一時handle/buffer/wrapperは全復元済み。エンジン実機実行は未実施。
System/lyt heapの空きは小さいが、全heapの調査は未完。利用者の指定で3gx側メモリを検証する。現行pluginの総枠5 MiBは実機headerと一致、Lumaは10 MiB設定に対応。独立のPlugin/SwkbdProbeで5 MiBの一時確保・内蔵FS読取り・全解放を検証予定。10 MiBの実機確保は未確認。辞書SD/3gx同梱や自前メニュー統合はしない。gohan正常版を維持。最終読取りstate=-1/PC0x0014E378。


## F-402 完了後の次工程

実機内蔵FS読取りと一時変更cleanupは完了。code全471668bytesは提供圧縮codeと一致し、展開後770048bytesも既存解析対象と一致。辞書はOpen/Size/先頭256bytes/Close/Release成功。詳細DOCS/system_keyboard_native_fs.md。
次は全辞書読取り・展開/再配置・実機独立contextから候補取得。最終RAM構成/ABI/処理時間も検証する。codeはkind2でファイル全体Readを使う。今回のOS追加確保失敗とgame heap暫定利用を踏まえ、メモリ確保方式は設計し直す。以下のcleanup待ち・キャンセル待ちは完了済み。

## F-402 緊急再開先: デバッガ応答復旧後のcleanup

DOCS/system_keyboard_native_fs.md参照。辞書先頭Read、code全体471668bytes Readは実機成功。kind2を使う。残件はcode RAM0x32DFC000のdump/照合、code handle0x568054のClose/Release確認、一時heap475136bytes解放、frame wrapper復元。Close後の結果照会/Releaseを含むpy_evalがタイムアウトしpendingの可能性があるため、現在値を見ずに再送しない。ユーザーにACNL停止表示/ダイアログを照会中。以下の未実行・キャンセル待ち記録は旧状態。

## 最新 F-402進行中

内蔵FS用の一時frame wrapper適用済み・要求未実行。ユーザーのキーボードキャンセル報告待ち（ACNLはSuspend維持）。RE/STATE.md先頭とscratchpad/MEMO_f402_native_fs.md参照。Open/Size/Read/Close/Releaseを1回ずつ行い、最後は必ず一時フックをrevertする。現状を成功と扱わない。

## 最新 F-401: 静的残件の監査済み、次は内蔵コンテンツ読取りの実測

- 完了: 直接参照243アドレスの追跡、315語の再配置表、25入力×2配置先の一致、7入力のcallback検査。DOCS/system_keyboard_relocation_audit.md参照。
- 完了: Luma公式ソースのFS権限設定照合、内蔵辞書/SWKBDへの読取り専用binary path生成・検査。SD/3gxへのテーブル配置不要な方式を維持。
- 未確認: 現在の本体のFSセッションからOpenFileDirectly/GetSize/Read/Closeが成功するか。まずResult・読取り長・コードの圧縮状態と同一性を記録し、取得コードは実行しない。準備物evidence/f401_builtin_content_requests.json。
- その後: 実機ネイティブのABI/VFP、実行領域、RAM、処理時間、復帰処理を検証。実機適用/ビルド前の検証必須。
- 範囲外の未証明事項: 学習/ユーザー辞書、別言語、並行利用、未観測の間接経路・データ内pointer。現行試験を全経路保証とは扱わない。

以下は各時点の履歴。F-400の「全参照監査・権限確認」は上記の静的調査まで進んだが、実機読取り成功はまだ未観測。

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


## 最新 F-398: PC候補取得完了

- [x] 関数型辞書slot7..9の初期化を特定、実機保存値と照合。
- [x] かんじ17件・文章6件をPCのみで順序込み再現。
- [x] 初期50件を超える追加列挙、取得API、検証器と文書を保存。
- [ ] 個人学習/ユーザー辞書の候補順位への影響を再現。
- [ ] 3DS上でアプレットを起動しない候補取得の初期化・実行環境を調査。

F-397の表記候補追加箇所調査は解決。差はUI段階ではなくPC側の未登録辞書だった。


## 最新 F-397: 今回の未確定入力から候補・文節取得完了

- [x] 新しいswkbd PID50を列挙して確認、停止取得、コード/各領域一致、detach成功。
- [x] 「わたしはねこがすきです」の全6候補の順序を保存。
- [x] 内部文節「わたしは/ねこが/すきです」を原本読みdecoderと独立PC結果で照合。
- [x] mode1文節領域が空でも別の予測内部リストに結果があることを文書化。
- [ ] 別入力でも内部リストとUI対象範囲を比較し、境界変更後の更新条件を検証。
- [ ] 原本wrapper直後1件→実機UI6件となる表記候補追加箇所を特定。

今回の指定入力について、変換ボタン確認や追加の実機操作は不要になった。
現在ACNLはSuspend、SWKBDは取得後detach済み。詳細DOCS/system_keyboard_prediction_segments.md。

## F-396後の現在待ち

- [x] 利用者が移設後の内蔵キーボードで指定入力を未確定保持。
- [x] read_phrase_snapshot.pyと検査器を準備。保存済みapp＋模擬editor、異常7件の検査PASS。
- [ ] 現在のACNL停止状態とswkbd PID/portを確認（状態照会タイムアウト、利用者へ依頼中）。
- [ ] SWKBD側でapp/editor/候補状態を取得し、続いて変換操作後との比較を行う。

## 最新 F-396: 通常チャット用ランチャー移設・再適用完了

- [x] 再起動後の停止/元命令/空き領域確認。旧ケーブとGUI v2の重複を検出。
- [x] SWKBDだけ0x00838200へ移設。ビルド前後検証・実機監査・適用・独立読み戻しPASS。
- [x] F-394正常3gxとGUI/しずえhookの不変確認。Suspendを保持。
- [ ] Resumeして通常チャットから移設版の起動を確認。
- [ ] 「わたしはねこがすきです」未確定時と変換操作後をSWKBD側で取得し、F-395のmode/editor範囲を比較。

旧0x00838D20を使う保存済みスクリプトは実行しない。現行版とmanifestを使う。

## 最新 F-395: 実機の変換modeとeditor対象範囲を比較する

UI経路は単文節指定1、直接連文節試験は55だった。旧「かんじ」dumpはmode0で文節結果なし。
DOCS/system_keyboard_phrase_state.mdに保存位置とPC検証を記録。
次はSWKBD側で予測表示→変換操作後のapp mode/件数/record/editor範囲を読む。
通常チャットで現在も内蔵キーボードを開けるか利用者へ確認中。
他UI経路の不在や全文自動分割は未確定。F-394正常版を変更せず解析する。

## 現在の優先作業: ソフトウェアキーボードの文節境界

F-394は利用者が「復帰しました。しずえスキップも問題なく動作しました」と実機確認済み。
文書と正常版バックアップBACKUP/plugin_f394_hardware_confirmed/を保存。
しずえ復旧作業は完了。以下のF-394実機確認待ち／F-393修正待ちは過去の記録。
日付またぎの副作用比較は別の未検証事項として残すが、キーボード解析の再開を妨げない。

キーボードはF-389で「かんじ」の全17候補を取得済み。次は複数文節入力時のphrase resultと
文節境界を調べる。HANDOFF_SYSTEM_KEYBOARD.mdから再開する。
目的は内蔵辞書・確定前候補の取得。自前メニュー/gohan.3gxへの組込みは目的ではない。
過去のPID・GDBポート割当・フック設置・appポインタを再利用前に現状確認する。

## 最優先更新 F-394: レジスタ保持修正版の実機確認待ち

F-393への修正とビルドは完了。gohan.3gxは846,070 bytes、SHA-256
`157c3159aff40fa54168ed53faa11dfe09941f424d16f1d0e5a1c79a01d77095`。
実機への適用は今回の作業範囲外。IDAのSIGSEGV停止状態は操作していない。
次は新しい版で、まずしずえスキップOFFのまま自前GUIをONにしてしずえ画面へ遷移し、
通常進行・描画を確認する。その後にONでの動作確認。旧F-391/F-392は使用不可。
ビルド前後は統合検査に加えverify_shizue_hook_registers.py [--artifact]を必須とする。
以下F-393の「修正未実施」は履歴。

## 最優先更新 F-393: F-392のOFF時SIGSEGVを修正する

F-392も使用不可。PC=0x0054C438、R4=0。callbackがOFF判定でR0=0を残し、
元関数のthisを破壊する。前回検査は復帰時レジスタの保持を確認していなかった。
現在IDAはSIGSEGVでSuspendのまま。callback境界のレジスタ・フラグ・スタック保持を
設計・検証する必要がある。今回のPC確認では書換え・再開・ビルドなし。
以下のF-392実機確認手順は不具合発覚前の履歴であり、そのまま再試行しない。

## ★最優先: F-392しずえスキップ修正版の実機確認

F-391はMITM callbackが元関数を呼ばず、メニュー表示時に画面停止・音継続となったため使用禁止。
現行`gohan.3gx`は通常の`Hook::Initialize`へ直し、全検査後にクリーンビルドしたF-392版。
846,115 bytes / SHA-256
`cc1d416aebd09a2bb52fc0da22a5f0a6225f0d2f5cad04287b481a1b2a6a1e9c`。

実機へは未配置。次の順に確認する。

1. タイトル起動後も自前GUIの上下描画、Select開閉、入力遮断が正常。
2. ルートの`しずえスキップ`が既定OFFで表示される。OFFのまま通常進行して変化なし。
3. ONにしてプレイヤー選択後、部屋0x63から村へ安全に移動し、通知が1回だけ出る。
4. 村からタイトルへ戻って再度入った場合も1回だけ発火する。
5. 日付またぎの雑草・カブ価・引越し・郵便受けは通常経路と比較する。

ソース契約、一括処理の無引数ABI、通常フックのリンク結果は確認済み。実機での
通常フックと一括処理→退出の連続実行は未確認なので、F-392をHIGHへ上げるには上記実測が必要。
詳細`DOCS/skip_isabelle.md`§10。

**2026-09-09 F-383・現在の対象:** フレンドチャットは利用不可との指定。通常チャット`BsMenuChat`を使う。
入口`0x001938AC`（BL、次の1938B0はSTR）、menuId5/screenId0x23F/mode0。
`DOCS/system_keyboard_normal_chat.md`。静的照合+原本入口6ケースPASS、実機未操作。
次に実装する場合は、子ポインタを保持し、既存APTへ要求を渡す構成とする。
通常チャットの送信後は同じ子で入力を継続するため、再入力の同期/二重入力抑止/文字列置換を合わせて検証する。
F-382のフレンドチャット向け入口/終了契約は現在の実装対象にしない。実機・ビルド前検証の指定は継続。

## ★現在の優先順（2026-09-08）

**2026-09-09 F-382:** 利用者指定の「ゲームのキーボード起動処理にフックする」2点を調査。
`DOCS/system_keyboard_game_hook.md`。mode3の入口BL `0x002AE474`、通知/確定/取消/子画面終了待ちを確認。
原本ARM12ケースPASS。入口では要求を記録しCalc/Draw後の既存APT位置へ渡す構成が候補。
次はTextManagerの文字列置換・二重入力抑止・要求/結果同期を具体化。APT失敗回収/常駐配置も残る。
**実機に触れない指示は継続。実機の状態照会や適用はまだ行わない。**

**最新依頼（F-358の目的訂正）:** 本体内蔵のかな→漢字変換辞書・変換候補の取得。
自前メニューや`gohan.3gx`への組み込みは目的ではない。これらの設計に依存させない。
とび森内/CTRPFからの内蔵キーボード呼び出しと、確定前の候補一覧を取得する経路を調べる。
利用者の知り合いに安全に呼び出した実績あり。具体的経路は不明だが、APT初期化差分だけで不可能と結論しない。
公開APIの通信内容、キーボード本体・辞書資源、ゲーム側のAPT経路を調べる。詳細 `DOCS/system_keyboard.md`。
**ビルド・適用前に必ず検証。依頼されていない用途・組み込み先を調査の前提にしない。**
**F-372の最新指定: ACNL既存APT管理を第一候補として採用。実機にはまだ触れない。**
実機の状態照会も保留。現在は静的解析・PC検証だけを進める。
F-359で本作のAPT起動IPCを特定（`0x0048012C` / `0x0047FF68`）。既存上位呼出しはエラー表示用。
F-362で利用者提供CIAをctrtoolで展開し、SWKBDが日本語共有辞書`0x0004009B00011902`を読むことを確認。
主要2辞書75,770件をCSV化し、元のARM読取処理と全件一致。`DOCS/system_keyboard_dictionary.md`。
F-363で原本ARMのPC実行による候補列挙・学習順位変更・文節変換/境界指定を再現。
頻度/品詞位置・接続表・2文節先読みの探索を確認。`DOCS/system_keyboard_conversion.md`。
残るのは個人学習/直前文脈/callback辞書を含む実機の候補列との比較、
各検索モード・同点/未知語の条件の網羅、njtan/njfzk/njexyomiの単語一覧化など。
F-364でACNLのPrepare/Start/WaitとGPU保存/復帰、共有メモリ・引数契約を具体化。
`DOCS/system_keyboard_launch.md`。原本ARMのIPC18ケースと既存caller ABIの局所照合PASS。
次の実機検証へ進む前に、Start失敗時の`err:f`/回収、ゲーム側の呼出し文脈、
CTRPFの画面pause・SWAPがある場合のコード/共有メモリ寿命を確認する。
実機の未確定候補配列の取得、安全な起動・取消・復帰は未検証。知人の具体的呼出し方法は不明。
F-372で`0x005CE29C`付近を独立要求受付の候補に特定。既存の再帰try-lockと周辺処理、
Prepareの遷移残留/再試行、Startの内部エラー戻り値未判定とfatal分岐を追い、原本ARM33ケースPASS。
`SYSTEM_KEYBOARD/verify_acnl_lifecycle.py`。実行スレッド/常駐配置、周辺状態の保持、失敗回収、
異常通知での共有メモリ寿命を解決してから投入用コードを確定する。実機確認手順は上記DOCS末尾。
以下は既存GUIの残作業として保持する。

引き継ぎは **`HANDOFF_CHEATMENU.md` の冒頭**。入力遮断は **`DOCS/input_block.md`**、
フレーム制御は **`DOCS/frame_pacing.md`**。

1. **3gx で入力遮断の残りを確認**（F-350〜F-355）
   - メニュー開閉でボタン遮断が入る / 抜ける
   - 下画面ロック中のタッチ遮断 + 暗幕のフェード（**二重に暗くならないこと**）
   - **GUI を OFF にしたときの完全復帰**を実機で読んで確認
     （`0x0053CDF4` -> `0xEB001823` / `0x003534E0` -> `0x0B04BECE`）
   ※ SELECT/START の効き分けだけは **3gx で確認済み**
2. **キーボード（F-349）の実機確認**。タッチ・十字キー・編集/取消/確定・表示負荷・手紙
3. スライダー専用バーの移植
4. 通知を 7 件へ（`kNoticeMax` 5->7 / `kMaxRectTop` 74->86。現行 `kPlugBytes` は0x70000。キーボード込みで再見積もりし、旧案0x50000へ縮小しない）
5. 他の重い場面を洗う（`probe_lyt_heap.py`。手紙は 262,528 B）
6. `DeleteCmdLists()` の反復確認
7. 共有バッチ（F-342 案 C）

★戻り先は **`BACKUP/plugin_full_20260907_f346/`**（実機確認済み・手紙も開ける）。
いまの作業版は `BACKUP/plugin_full_20260907_f355/`。

---


> **2026-09-07 F-349:** 今回の依頼でキーボード保留を解除し、移植・ローカル検証・ビルドを完了。
> **残りは実機確認**。`DOCS/keyboard.md`を参照。以下の過去の「移植しない」は当時の方針。

## ~~TODO-124: 色（RGB）の帰属を確定する~~ — **完了**（F-187 / F-189 / F-190）

**達成。** 位置・大きさ・色・アルファのすべてを自前で制御できる。
実装は **`PATCHES/cave_add_sprite2.py`**。

原因は 2 つだった。

1. **相乗り先のバッチを間違えていた。** `+37 = 3` は色を持たないバッチ。
   色を使うなら **`+37 = 7`**（行列 0..2 ＋ 色 3..6）のバッチに乗る
2. **アンカー（基準点）を直していなかった。** 幾何エントリの後ろ 2 ワードは
   中央揃えなら `(-幅/2, +高さ/2)`。幅・高さだけ変えると画面外へ飛ぶ

---

## ~~TODO-125: 自前テクスチャで「絵」を出す~~ — **完了**（F-191）

**達成。** 自前バッファのテクスチャが GPU に読まれ、タイリング込みで絵が出せる。

原因は **`reg 0x083`（ラップ・フィルタ・テクスチャ種別）を上書きしていなかった**こと。
`0x082` / `0x085` / `0x08E` の 3 つだけでは足りず、相乗り先の
64x64 ETC1 用パラメータが残って縞模様になっていた。

**必要な 4 レジスタ:**

```
reg 0x082 = 高さ<<16 | 幅
reg 0x083 = 0        （bit1 拡大 / bit2 縮小フィルタ。0 = ニアレストでくっきり）
reg 0x085 = PA >> 3  （リニア FCRAM なら PA = VA - 0x10000000）
reg 0x08E = 形式     （0=RGBA8, 9=LA4, 12=ETC1 …）
```

---

## ~~TODO-126: 自前スプライトだけ別のテクスチャにする~~ — **完了**（F-192 / F-193）

**達成。** 実装は **`PATCHES/cave_own_batch.py`**。
`DrawCtx_FlushBatch` をラッパで包んで 2 回呼び、自前スプライトを独立したバッチにする。
**ゲームの描画には一切影響しない。**

踏んだ落とし穴 2 つ:

1. **素通り経路で `R1`（cursor）を壊して SIGSEGV**（`DOCS/crash_recovery.md`）。
   判定は `R6` と `R12` だけで行う
2. **フラッシュが配列の `[0].w0` をヘッダで潰す**（F-192）。
   2 回目の前に「配列ポインタ − 4」から復元する

## ~~TODO-127: SD 画像 / ビットマップフォント~~ — **完了**（F-194 / F-195）

**達成。** 実装は **`PATCHES/cave_draw_sprites.py`**。
64x64 の LA4 アトラスに 8x8 グリフを並べ、UV で 1 文字ずつ切り出して
4 枚のスプライトとして「ACNL」を地図の上に描画した。

**★描画順は「フレーム内で何回目のフラッシュか」で決まる**（1 フレーム約 42 回）。
最後のフラッシュで描けば最前面になる。

---

## ~~TODO-128: SD カードから実際の画像を読み込む~~ — **貼り方は完了**（F-196）

**フルカラー画像（RGBA8）の表示を確定。** 64x64 のテスト画像で
バイト順・向き・タイリングをすべて検証した。

- **RGBA8 はメモリ上 `A, B, G, R` の順**（u32 LE で `0xRRGGBBAA`）
- タイリング: `byte = (tile*64 + morton) * バイト数`、
  `tile = (y>>3)*(幅>>3) + (x>>3)`
- 64x64 RGBA8 = 16384 バイト。`ALLOC_SIZE = 0x4000` にちょうど収まる

**残るのはファイルを読む部分だけで、それは TODO-130（プラグイン）に含まれる。**
デバッガからは「SD を読む」こと自体に意味がない。

## ~~TODO-129: 8 枚を超えるスプライトを描く~~ — **完了**（F-198）

**達成。** 「ACNL GUI OK」11 文字を 2 チャンクで描画。

**最後のチャンクを大きさ 0 のダミーで埋めて全チャンクを 7 枚にそろえる**と、
カウンタも索引も定数のままで外側ループを 1 つ足すだけで済む。

あわせて見た目を壊していた **4 つの独立した原因**を潰した（F-198）。
特に **相乗り先の縮尺（0.5）** と **整数倍でない拡大率** はドット絵に必須の条件。

---

## TODO-131: 描画順を安定させる — ★★★★★**完了**（F-203 〜 F-212）

`PATCHES/cave_draw_topmost.py`。**常に最前面に描かれ、メニュー開閉でも順序が変わらない。**
線幅は均一、ノイズなし。実機で確認済み。

### 効いた注入点

**下画面のパス（`Frame_DrawPass1040`）で最後に再生されるレイアウト
（リスト id 15）の「記録本体の直後」= `0x568770` の NOP。**

### 途中でつまずいた 6 点（すべて F- 番号あり）

| 症状 | 原因 | 対策 |
|---|---|---|
| 発火 0 回 | 記録要求フラグが立っていないと記録が走らない | 入口でフラグを立てる（F-204） |
| 上画面に出た | 「最後に再生」は画面ごとに違う | パスごとに測り直す（F-205） |
| 直前のボタンの色になる | マテリアルを自前で積んでいない | `Material_EmitState` を自分で呼ぶ（F-206） |
| テクスチャ全面が貼られる | `drawctx+1692` が 0 で UV が読まれない | 1 にする（F-207） |
| 半端な拡大・ノイズ | レイアウトごとに投影が違う | 縮尺を測り直す（F-208） |
| フックを外しても残像 | 記録済みリストは記録し直すまで残る | フラグを 1 回立てて掃除（F-204） |

### ★その後に見つかって直した 3 点（F-210 〜 F-212）

| 症状 | 原因 | 対策 |
|---|---|---|
| セーブ確認ウィンドウで消える | リスト id を固定で狙っていた | **実行時に追いかける**（F-210） |
| 同上（真因） | マテリアルを「たまたま」で選んでいた | **条件で選ぶ**（F-211） |
| たまに別の色を拾う | 借りたマテリアルが定数色を持っていた（`P_crsl_00`） | **定数色が中立のものだけ選ぶ**（F-212） |

実機で確認済み: **常に真っ白、常に最前面。** どんな場面でも消えない。

### 残っている未確認事項

- 追いかける対象が 1 つも見つからない場面があるか（そのときは前フレームの値を保持する）
- マテリアルの定数色は `+0x10 / +0x14 / +0x18` の 3 つしか見ていない。
  `+0x1C 〜 +0x2C` も色なので、色付きを取りこぼす可能性は残る

---

## TODO-131（旧）: 失敗した 2 案の記録（F-200 〜 F-202）

### ★試して失敗した 2 案

| 案 | 結果 | 原因 |
|---|---|---|
| `GpuCmd_SplitAndSubmit` の直前に積む | **GPU ハング x2** | 呼び出し元がカーソル由来の値を呼び出しをまたいでキャッシュしており、
戻ったあと古い値でカーソルを巻き戻して私たちのデータを潰す（F-201） |
| `Frame_DrawPass1024` の末尾に積む | **何も描かれない＋メニューでフリーズ** | **メインリストの末尾には UI の GPU 状態が無い**（F-202） |

**どちらも「どこに積むか」だけを考えて「そこに正しい GPU 状態があるか」を
考えていなかったのが誤り。**

### ★確定している構造（F-200 / F-201）

```
Frame_DrawPass1024():             ← 記録＋再生
    BaseObj_RunDrawPhase()
    Render_DrawScene2()
    Render_DrawScene0(1024)
    Render_DrawScene1(1024)
    Frame_EndDrawPass1024()       0x5A27C8（普段は早期リターン）

Frame_DrawPass1040():             ← 再生のみ
    Render_DrawScene0(1040)
    Render_DrawScene1(1040)
    Frame_EndDrawPass1040()       0x5A2894
    Render_FrameEnd()             フレームに 1 回（30fps で実測一致）
```

**UI はレイアウトごとに専用リストへ記録し、再生で差し込む。
GPU の状態もそのサブリストの中にしかない。**

### ★★手順 1 完了 — 最後のレイアウトは固定だった（F-203）

301 フレーム（メニュー開閉 2〜3 回を含む）で、
**最後に再生されたレイアウトは常に `0x32C4CBCC`（リスト id 8）、違ったフレームは 0 回。**

**注入点は `0x568770` の NOP**（`Layout_RecordPaneTree` の記録本体の直後）。
元命令を潰さずに済み、UI の GPU 状態も揃っている。

### ★旧: 次の方針 — 最後に再生されるレイアウトの「記録中」に入る

1. **`ssys_ma_lyt_Layout_ReplayRecordedList`（`0x5682DC`）をフックし、
   各フレームで最後に再生されたレイアウトを記録する。**（読み取りのみ・安全）
2. そのレイアウトが場面をまたいで安定して同じかを確かめる
3. 次フレームで、そのレイアウトの**記録中**（`ssys_ma_lyt_Layout_RecordPaneTree`
   `0x5686D4` の内側）に自前スプライトを積む

状態が整っていて、かつ最前面になる。

**まず 1 の観測だけを行うこと。** 書き込みを伴う実験を先にしない。

### 当面の運用

**`PATCHES/cave_draw_sprites.py`（最初のフラッシュに相乗り）は安定して動く。**
地図やメニューより後ろになる制約はあるが、GUI としては機能する。

## TODO-130: CTRPF プラグインへ移植する — ★★★★★**完了**（F-213 〜 F-217）

`Plugin/CTRPluginFramework-BlankTemplate-0.8.0/Sources/OwnGui.cpp`。
メニュー項目「自前 GUI を最前面に描く」を ON にすると組み込み、OFF で素に戻す。

### できていること

- `cave_draw_topmost.py` の `MODE = "export"` が `includes/GuiCaves.h` を吐く
- **書き出したバイト列が実機のものと一致することを確認済み（不一致 0）**
- 確保用ケーブを実機メモリへ置いて逆アセンブルで検証済み
  （このとき `MOV R1,#0x4000` が `0x1000` になっていた誤りを発見・修正）
- ビルド成功（`CTRPluginFramework-BlankTemplate-0.8.0.3gx`、**762,889 バイト**）
- ★テンプレートの Makefile が `.elf` をリンクし直さない誤りを修正した。
  直すまで「ビルドは通るのに .3gx が数日前のまま」だった

### 実機で 1 回クラッシュして直したこと

`svcFlushDataCacheRange`（Luma 独自 SVC）でカーネル内の書き込みフォルト。
`svcFlushProcessDataCache`（標準 SVC）へ変更した。
**このときバッファの確保（0x329D8500）は成功していた**ので、
ゲームのアロケータをプラグインから呼ぶ部分は実機で動くことが確定した。

途中経過を段階ごとに `/CTRPF_OwnGui.txt` へ書き出すようにしたので、
次にクラッシュしたら「どこまで進んだか」がファイルに残る。

### 実機で確かめること

1. SD の `/luma/plugins/00086200/` へ `.3gx` を置き、Rosalina で plugin loader を ON
2. メニューから「自前 GUI を最前面に描く」を ON
3. 「ACNL GUI OK」が下画面の最前面に出るか → **確認済み**
4. OFF で素に戻るか → **確認済み**
5. `/CTRPF_OwnGui.txt` に確保したアドレスとテクスチャ PA が出るか → **確認済み**
   （ログは `.3gx` と同じ場所に出る）
6. タイトル/ロード画面でも文字として白で出るか → **確認済み**（F-214）

### ★タイトル/ロード画面での不具合を修正（F-214）

「色つきの板」になっていた。原因は**中立なマテリアルが 1 つも無い場面がある**こと
（ロード画面では Picture 320 個中、条件 1 は 295 個、条件 1+3 は **0 個**）。
マテリアルの枠を優先/予備の 2 つに分け、予備は**定数色を一時的に中立化してから積み、
直後に戻す**ようにして解決。実機で確認済み。

### ★しずえ会話の切り替わりで消える件も修正（F-215）

中立化を **`+0x10` 〜 `+0x30` の 9 語**へ広げた（3 語では `P_soft_B` の
アルファ 0x80 と合成モード `0x6AA` が残り、白を描いても見えなかった）。

**★描画後に `Material_EmitState` を呼ぶ「後始末」は誤り。**
内部で `DrawCtx_FlushBatch` を呼ぶので、中身が確定していないバッチが流れて
モザイク状の乱れになる。実機で 1 回踏んで外した。

### ★SD からの任意画像の読み込み — **完了**（F-216 / F-217）

`PATCHES/make_gui_image.py` で PNG を `.acgx` へ変換し、
SD の `/luma/plugins/00086200/gui_image.acgx` に置けば下画面の最前面に描かれる。
無ければ埋め込みのフォントアトラスのまま動く。

**変換は PC 側でやり切る。** 3DS の GPU は 8x8 タイル + Morton 順・2 の冪しか読めず、
展開器をプラグインへ持ち込むと失敗の仕方が増えるため。
PIL は入っていないので **zlib だけで PNG を読む**。

途中で **`reg 0x082` が `(幅<<16)|高さ` だった**ことが判明した（F-216）。
64x64 の正方形しか使っていなかったので、逆に書いていても気付けなかった。

### ★実機で確かめたこと / まだのこと

| 項目 | 状態 |
|---|---|
| タイル化・転送・寸法/形式ワード・スプライト表・UV | ○ 実機で確認（`apply_gui_image.py` 経由） |
| **半透明（アルファブレンド）** | **○ 実機で確認（F-218）** |
| **プラグインが SD からファイルを読む部分** | **○ 実機で確認**（LA4 と RGBA8 の両方。F-219） |

**★CTRPF のパスはプラグインのフォルダ基準**（F-219）。
絶対パス 1 本だけ見ていたので見つからず、黙って埋め込みへ落ちていた。
候補を順に試し、どれで開けたかをログに残すよう直した。

確認するには `.acgx` を **`.3gx` と同じフォルダ**へ `gui_image.acgx` の名前で置く。
`/CTRPF_OwnGui.txt` に「画像を開いた: …」が出れば読み込み経路が通っている。

### 残り

- 起動直後に ON にすると落ちる件は **TODO-133 として保留**（対策コードは外した）
- バッファは 0x4000 バイト固定。RGBA8 なら 64x64、LA4 なら 128x128 まで。
  もっと大きな画像を扱うなら確保の大きさを増やす必要がある（未検証）

---



## TODO-134: 自前チートメニューを GPU 経路で描く（**中断。引き継ぎ書あり**）

### 2026-09-04 追記（F-255 / F-256）— 自前ノードから描けた。フリーズ原因も確定

- `PATCHES/cave_node_draw.py` で上下に描画。**ロード画像より前面**（F-255）
- フリーズの原因は **「ゲームがそのパスで 1 枚も描いていないと GPU 状態が未確立」**（F-256）。
  対策としてゲームの `DrawCtx_FlushBatch` 回数が 0 のパスでは描かないゲートを入れ、実機で無事を確認
- 実機へ入れる前に `python PATCHES/audit_node_cave.py` を必ず通すこと

**次**: 上画面が空のフレームでも描けるよう、**GPU 状態を自前で確立する**
（テクスチャ結び付き・頂点属性の構成・TEV）。材料は F-191 / F-206 / F-207 / F-216。

### 2026-09-03 追記（F-254）— 自前 Layout ノード方式は実機で成立した

`PATCHES/probe_own_layout_node.py` で、上下それぞれのリストに自前の偽 Layout ノードを
毎フレーム優先度 `0xFF` で登録し、**必ず末尾（最前面）**になることを実機で確認した。
replay スロットは 1 フレームに 3 回（`0x400` / `0x410` / `0x401`）呼ばれる。

**次**: replay スロットから主リストへ実際に描画コマンドを積む。無地の四角 1 枚から。

### 2026-09-03 追記（F-253）— F-252 はここで訂正済み

実機で `LayoutList_SetDisplay` の出口を読み取り専用で観測し、
**描画パスが 3 本**あることを確定した（`PATCHES/probe_setdisplay_exit.py`）。

- `0x400` 上画面左目 / `0x410` 上画面右目 / `0x401` 下画面
- **`Frame_DrawPass1040` は下画面ではない**（F-205 の帰属誤りを訂正）
- 描画順は `Layout+0x0C` の優先度バイトで決まる（`LayoutMgr_AddLayout` = `0x56928C`）
- リストは毎フレーム `sead_List_UnlinkAll` される

**次にやること**: 何も描かない空の自前 Layout ノードを優先度 `0xFF` で
1 フレームだけ登録し、クラッシュしないことと末尾になることだけを確かめる。
その後に限り、replay ケーブで主リストへ描画コマンドを積む。

### 2026-09-03 追記（F-252）

`REFERENCES/TEXTS/render.txt` を読み、本作の `code.bin.i64` で独立検証した（F-252）。
**次の注入点の第一候補は `LayoutList_SetDisplay` の出口 `0x566E64`**。
`HANDOFF_CHEATMENU.md` の先頭と §3 に反映済み。

未解決で、動的解析の再接続後に最初にやること:

1. 静的にはリストが 1 本（`mgr+4`）なのに、F-205 は「パスごとに最後の Layout が違う」と実測した。
   **ノードの追加経路が未特定。** これが解けるまで「上下の描き分けはリストで決まる」と結論しない。
2. `0x566E64` を**読み取り専用**でフックし、到達回数・`R5`（display）・主リストの
   `g_GpuCmdPtr` / `g_GpuCmdEnd` を採取する。書き込みはその後。
3. `Layout+0x11D`（記録要求フラグ、F-204）が render.txt の `m_CmdBufferDirty` に当たるかは未検証。


**★再開するときは `HANDOFF_CHEATMENU.md` を読むこと。** これ 1 本で再開できる。
以下は経緯の記録。

### ★2026-09-01 ロード画像表示中の実測（F-234。F-233 より優先）

- ユーザーがロード画像を目視して Suspend した状態から、一回だけ制御再開し上パス末尾で停止
- 低レベル replay は **`id 8 (len 0x180) → id 10 (len 0x2C0)`**
- id 10 Layout から `tc_load_01..03.bclim`、`load_wait_kind.bclan`、
  `Layout/common/save_wait.arc` を直接確認。リンクも id 8 → id 10 で trace と一致
- 従って、現行方式が相乗りする id 8 は、その後のロード画像 id 10 に覆われる
- id 10 の記録リストは size `0x1000`、残量 `0xD40`。小表示には使えても全メニューには不足
- 同じ停止時の上パス主リストは容量 `0x100000`、使用 `0x12B0`、残量 `0xFED50`
- `0x5A27C8` / `0x5A2894` は F-233 の通り通常 submit 点ではなく、guard 0 なら早期 return
- 現行ケーブは投影まで自前確立しておらず、直前の非ゼロ Layout が残した Drawer 状態に依存

根本原因は低レベル trace と、停止中 Layout の vtable・リンク・ロード専用リソース名・
Drawer fingerprint の独立経路で一致した。ただし tail へ積んだ UI 画像が自然提出されるかは未検証。

**次の最小実験:** `0x5A27C8` 入口で、上画面の UI 画像（スプライト）1枚だけを
主リストへ積む。まず自然提出版だけを試し、表示されない場合に限り
`GpuCmd_SplitAndSubmit` 明示版を別に A/B する。最初から19チャンクへ広げない。
1→2→6→19チャンクの順で `g_GpuCmdPtr` 差・残量・表示・クラッシュ有無を表にする。

### 2026-09-02: tail 自然提出最小試験 — **失敗・再適用禁止**

- `PATCHES/cave_tail_sprite.py` の1枚版を、停止中の branch / literal / cave / BSS /
  manager capacity 監査後にのみ適用した。hook 到達は stock `0x5A27C8` の software BP で
  別途確認済みである。
- 実機結果は「UI画像は出ない。通常 Resume 後も画面更新だけ停止し、音声は継続」。
  したがってこの手製 Drawer-state / cursor / flush 経路は安全な提出経路ではない。
- 素材捕獲 `LOG=0x32E30A4C` は得たが、後から見た現行 main list に `-120.0f` が無かった。
  list 切替後の読取りである可能性を除外できないため、**ケーブが描画まで到達しなかった**とは
  断定しない。cave-entry BP の非hitも別の3秒標本だけであり、一般化しない。
- ユーザー Suspend 後に uninstall を実行。hook 2語を stock、LOG を zero、cave 2範囲の
  各320 wordsを bulk read で zero と独立確認した。source は `MODE="audit"` に戻した。
- 次回はこのケーブを改版・再試行しない。まず **読み取り専用 trace** で上 pass 主リストの
  `g_GpuCmdPtr`、list manager、submit 境界を同一フレーム内に採取し、既存の
  `cave_draw_topmost.py` の安全な state 生成経路との差分を確定する。

### 2026-09-02: F-236 record-list buffer 拡張プローブ — **部分成功、描画には未接続**

- `REFERENCES/TEXTS/render.txt` の「バッファ拡張」案を、ゲーム内の
  `LayoutList` record/replay と `GpuCmd_SelectList` assembly で照合した。
  新 id 選択は header だけで buffer を持たないので、capacity だけの書換えは禁止。
- `PATCHES/probe_layout_record_buffer_extend.py` は title 上画面の id `0x10` を限定し、
  `0x568770` で `used = g_GpuCmdPtr - manager->base` をコピーして 0x4000-byte
  replacement buffer へ base/capacity/cursor/end を整合して差し替える。
- 1200 ms の実機 run では id 0x10 manager の base/size 置換が一度成功したが、
  `used=0` だった。hook/cave/LOG は撤去済み。非ゼロ copy / replay / 視覚安定性は
  未確認で、これを renderer 成功と扱わない。

**次の安全な順序:**

1. 非ゼロの上画面 Layout record が実際に発生する場面を、描画を変えない trace で取得する。
2. その Layout の `g_GpuCmdPtr-base` と Commit 後の `Layout+0x108` を同一 frame で比較し、
   copy length と replay range が一致することを確認する。
3. `root+4`（top `LayoutList`）の末尾 node を実行時に選ぶ小型 trace を作り、固定 id
   ではなく最後に replay される Layout を識別する。ロードの id8→id10 を再発見できることを
   成功条件にする。
4. 1〜3 が通って初めて、既存の `cave_draw_topmost.py` の command-add 経路と拡張を
   統合する。最初は UI画像（スプライト）1枚・1 chunk・十分な残量検査だけに限定する。
   `Frame_EndDrawPass1024` tail や直接 SplitAndSubmit を混ぜない。

### 2026-09-02: F-237 record-list 再生順フック — **no-draw 制御経路を確認、視覚的な前面化は未確認**

- `LayoutMgr_RenderTop(0x566DF8)` と `LayoutList_SetDisplay(0x566E30)` は、`code.bin.i64` の
  assembly と stopped software breakpoint の `R0=root+4, R1=0x400, LR=0x001B7294` で照合済み。
  後者は record 処理ではなく、top LayoutList を辿って Layout vslot `+0x08` を replay する。
- gokiro 氏の三分割設計（command-add / ordering / buffer extension）は高価値な設計参考として使う。
  ただし固定 id やそのままの hook 実装は本作の仕様として採用しない。
- `probe_layout_reorder.py` の tail-target 対照 run は `count=0x72`, top match `0x26` で終了し、
  hook/cave/LOG は撤去済み。tail 対象だったため表示順の変化は意図的に無く、前面化の証拠ではない。
- 同ファイルの `MODE_OVERRIDE="inspect"` は read-only の node-chain dump である。現在の title
  標本は id `0x10` の 1 node だけだったため、次の loader 標本の同定にのみ使う。

**次の安全な順序（F-237 を F-236 と統合する前）:**

1. ロード画像を目視した停止状態で、top LayoutList の node chain を読み取り、`id 8 -> id 10`
   の二 node を実機値で再同定する。固定 heap pointer や固定 id を通常場面に持ち込まない。
2. no-draw reorder hook の LOG target をその標本の **non-tail id 8 Layout pointer** にだけ替え、
   replay ring で `id 10` の後に id 8 が再生されたことを確認する。node link は変更しない。
3. 2 の順序 trace と画面上の UI画像（スプライト）の前面化を別々に記録する。片方だけで成功としない。
4. 同一 pointer を command-add hook と buffer-extension hook の共有対象にし、nonzero copy/replay を
   先に証明してから UI画像 1 枚を統合する。F-235 tail / direct Split は混ぜない。

### 2026-09-02: F-238 loader phase の再検証 — **自動選択は必須、transition 前の標本が必要**

- 新しい user-visible loader stopped snapshot は top list に id `0x10` の1 nodeだけ、bottom は空だった。
  続く 300 ms no-draw auto probe は id `0x08` を unique に見たが tail だったため、reorder は 0 回。
  `id 0x08 -> 0x0A` を同一 list の恒久的配置だと見なしてはいけない。
- `probe_layout_reorder_auto.py` は current upper list の unique non-tail id `0x08` だけを移動する。
  この条件を満たさない場面では source-level に stock loop を再現し、command-add / buffer extension は
  一切行わない。現在は uninstall 済み。

**次の単一実験:** 通常画面で auto probe を audit/install し、そのまま loader transition を一度だけ
通す。timed stop 後、`reorders > 0` かつ LOG target/next が有効なら replay ring を別途置いて順序を
読む。`reorders == 0` なら表示には手を出さず、loader の前段フェーズをさらに分離する。

### 2026-09-02 title 再attach後 — F-238 auto-probe は撤去済み、画面状態を再同定

- 実機を title 画面で停止した状態から再監査した。`state=-1`、`PC=0x00137064`、BP 0、
  `0x566E30` は stock、F-236〜F-238 LOG は zero だった。
- static `code.bin.i64` の `0x838C00..0x838E00` zero と、runtime script audit の cave 68 words /
  LOG 8 words zero / top-list link 検査を独立に通してから、`probe_layout_reorder_auto.py` を install した。
- loader へ進めたが画像が見えず、停止時に probe LOG は `0x00000CFF`（3,327 calls）だった。原因を
  probe と断定しないが影響を除外できないため直ちに uninstall した。現在 `0x566E30=0xE92D4070`、
  `0x838C00=0`、`0x9B2F00=0`、BP 0。
- uninstall 後の stopped memory walk は top の id `0x10` node 1 個（length 0）、bottom 空を示した。
  後に user がロード画像を実際に目視して Suspend した第 2 標本でも、同一 root / node
  `0x32FF5F8C -> 0x3225B070`、id `0x10`、start/length/capacity すべて 0、bottom 空を再読した。
  よってこの組成は user-visible loader と両立する。一方 current id `0x10` node のゼロ長だけを
  loader Layout の空記録と解釈してはならない。同 id の manager bucket は
  `base=0x327AE270,size=0x1000,offset=0x2C0` を保持し、F-234 の resource 付き id `0x10`
  Layout pointer `0x3225A2B4` と current node pointer `0x3225B070` も異なる。
  `id=0x08 -> 0x0A` / nonzero lengths は別 phase または別 Layout instance の標本であり、固定配置・
  固定 pointer・id 単独のいずれにも結び付けない。
- LOG の `reorders` / target / next は安全な撤去で zero 化された。今回の画面変化を probe の結果と
  結論付ける材料にはしない。
- 次は order hook を使わず、**record/replay 時の Layout pointer と id-manager の base/size/offset を
  同じ ring に記録して**対応を読み取り専用で同定する。UI画像（スプライト）や buffer extension を
  統合しない。
- F-240 により stopped 時 current top node は `Layout_ReplayRecordedList` の `length<=0` guard で
  replay 不可と分かった。次の transition 標本では、record/replay の対応に加えて final submit / 表示
  バッファ切替を別 ring で記録し、「直前フレーム保持」と「別描画経路」を分離する。現在の visible
  loader stopped 状態を壊すため、ここでは再開・hook install をしない。
- `probe_loader_submit_lifecycle.py` は停止中に install 済み。`0x5683E4` の Layout pointer/range と
  `0x1280CC` の active-manager/cursor を同一 128-entry ring に保存する。LOG が候補 replay
  （nonzero id `0x10`, display `0x400`）で trigger されるまでは game/GPU state を一切変更しない。
  次は user が Resume し、次の loading transition を一度通した後に Suspend する。その後 log を読み、
  必ず uninstall/read-back を先に行う。

### 2026-09-02: F-241 lifecycle trace — **block-copy版は失敗・再適用禁止**

- `LDMIA R2,{R0-R3}; STMIA R1!,{R0-R3}` は LDM が `R1` を stage の Layout pointer で上書きする。
  実機では loader Layout `0x3225A2B4` の先頭16 byte を破損し、SIGSEGV が二段階で発生した。
- LOG `0x9B3000` は static `code.bin.i64` の `.bss` RW であり、RX `.text` 書込み説は不採用。
- hook/cave/LOG は撤去済みだが heap 破損は残る。**ゲーム再起動・再アタッチ完了まで実機作業をしない。**
- 次の trace は (1) destination を `R3` 等の LDM register list 外へ置く、または (2) LDM を使わず
  `LDR/STR` を1 wordずつ行う。(2) を先に採用し、1 wordの LOG 書込みと stock 再開だけを実証する。

#### 最新の実機引き渡し状態（F-234）

- ロード画像表示中の上パス末尾 `PC=0x005A27C8` で安全に停止中、thread 219
- software breakpoint 0 件。ロード用 trace は uninstall、hook・cave・ring は stock/zero
- 現行プラグイン用7フックも stock、`LOG 0x009B0D00` と slot `0x009B0010` は 0
- root `0x32FF5F88`、inline Drawer `0x32FF62EC`、vptr `0x008FBF04`
- この boot の `g_GfxAllocator` から `0x329D7A00` に `0x4000` を確保済み
  （slot は 0、アトラス未転送、再起動後は無効）
- これ以上 Resume するとロードが終わる可能性がある。次の実行は tail 最小版の全機械監査後だけ

#### 最小実験の実装条件

1. 新規の末尾用パッチとして作り、現行プラグインの19チャンクをそのまま流用しない
2. 上画面の UI 画像（スプライト）1枚、1チャンクだけから始める
3. 主リストの `base / ptr / end` が同じ manager 由来であることを確認し、必要量不足なら描画しない
4. `0x5A27C8` の stock 命令を保存し、描画後は早期 return 条件を含めて元経路へ戻す
5. 自然提出版と、明示的 `GpuCmd_SplitAndSubmit(0x1280CC)` 版を分けて A/B する
6. 全 branch target / PC-relative literal / code cave / `.bss` の非重複を generator で assert
7. 1→2→6→19チャンクの各段階で ptr 差、残量、表示、クラッシュ有無を表に残す

現行 `cave_draw_topmost.py` は `CMDEND` / `LISTMGR` の定数を持つが、描画ケーブ内で
残量を実際には検査していない。これを根拠に容量安全と判断してはならない。

**目標（ユーザー）**: CTRPF のチートメニューを自前のものに置き換え、
**メニューを開いている間もゲームが進行する**ようにする。
設計は `Plugin/CTRPF-GUI-Simulator`（ブラウザで動く実物大のプレビュー）。
実装は **CTRPF / C++20**。**上画面と下画面で描き分ける**こと。
ホットキーは、従来のメニューを **Select + DPad Up**、自前メニューを **Select** にする。

### なぜ GPU 経路なのか

CTRPF の既存メニューはゲームを止める。OSD はチカチカしてアルファブレンドが使えない。
**ゲームの GPU 経路に相乗りすれば、止めずに、半透明で描ける**（F-218 まででここは実証済み）。

### 設計の規模（`ui-model.js` 1112 行 / `app.js` 590 行）

- 上画面左 40%（160x240）にメニュー。項目高 18px、10 行表示、選択追従スクロール
- フォルダ / チェックボックス / アクション / インラインリスト / 10 進・16 進・float / スライダー
- リストボックス（インライン 6 行・上下画面 8 行）、ダイアログ、通知（上画面右下）
- 下画面: 数値キーボード、かな 5 段 / QWERTY 文字キーボード、スライダー
- 全項目のホットキー設定。未適用の変更は黄色、X で適用、L で戻す
- アニメーション多数（Cubic Ease Out、選択の明滅、跳ね返り）

### 段階

| 段 | 内容 | 状態 |
|---|---|---|
| A | 計画を文書化 | ○ 完了 |
| B | **描画基盤: 上下画面の描き分け＋チャンク別の色** | **○ 完了（F-220。実機確認済み）** |
| C | 描画基盤: 表を二重化してちらつきを防ぐ | |
| D | C++ の描画器（矩形・8px 文字）とグリフアトラス | **○ 完了（実機確認済み。F-222）** |
| E | メニュー本体の移植（`ui-model.js` の状態機械） | △ v1 が実機で動作。**見た目と機能を Simulator へ寄せる作業が残り** |
| F | 下画面のキーボード類 | |
| G | ホットキー（Select / Select+DPad Up） | **○ 完了（実機確認済み。F-222）** |

### 段 B の設計

いまのケーブは**下画面だけ**を対象にしている（F-205 / F-210）。

```
下画面 = Frame_DrawPass1040 で最後に再生されるレイアウト（実行時追従）
上画面 = Frame_DrawPass1024 で最後に再生されるレイアウト（同）
```

再生を控えるケーブ（`CAVE_V`）は既にパスの印を見ているので、
**上画面用の枠を 1 つ増やすだけ**で両方追える。
描画ケーブは「どちらの対象と一致したか」で
**スプライト表の先頭とチャンク数を .bss から選ぶ**ようにする
（いまはリテラルに焼いてある）。

### 旧: 段B中断時点の状態（2026-09-01。現在値ではない）

以下は履歴。現在の引き渡し状態は上の「F-234」を正とする。

#### 実機

| 項目 | 値 |
|---|---|
| GPU 可視バッファ | `0x329D8500`（`cave_gfxalloc_probe.py` で確保。0x4000）。フォントアトラス転送済み |
| 確保スロット | `0x009B0010`（probe は uninstall 済みなので **0 に戻っている**。番地は上の値） |
| `cave_draw_topmost.py` | **install 済み**（`TEX_VA = 0x329D8500`、`TOP_ENABLE = True`） |
| 見えているもの | 上下両画面に「ACNL GUI OK」。下 = 白/赤、上 = 緑/水色（チャンク別の色の確認用） |

**再起動すると全部消える。** 再開手順は下の「再開のしかた」を見ること。

#### ★プラグインは段 B を**まだ取り込んでいない**

`includes/GuiCaves.h` は段 B より前の版。
`.3gx`（765,128 バイト）も同じ。**段 B を入れるには再度 export → make が要る。**
export は `python PATCHES/export_caves.py` で **IDA 無しでもできる**。

ただし export される `kGuiTexPaValue` は `TEX_VA` の値なので、
export 前に `cave_draw_topmost.py` の `TEX_VA` を
**その boot の確保番地**に合わせておくこと（プラグインは実行時に差し替えるので
値そのものは何でもよいが、ケーブ内で一意である必要がある）。

またプラグイン側は段 B の新しい .bss（表の先頭・チャンク数・色配列）を
**まだ書いていない**。`OwnGui.cpp` の `InstallCaves()` に
以下を足す必要がある（`cave_draw_topmost.py` の install と同じこと）。

```
LOG+0x80 = 下画面の表      LOG+0x84 = 下画面のチャンク数
LOG+0x88 = 上画面の表      LOG+0x8C = 上画面のチャンク数
LOG+0x98 = 下画面の色配列  LOG+0x9C = 上画面の色配列
```

#### LOG（`0x009B0D00`）の割り当て

```
+0x00 発火回数            +0x04 drawctx
+0x10 カーソル前          +0x14 カーソル後   +0x1C 残りチャンク数
+0x20 最後に見たマテリアル +0x24 優先        +0x28 予備
+0x2C 下画面 集め中        +0x30 パスの印    +0x34 下画面 確定
+0x44 復元フラグ          +0x48 使用マテリアル
+0x50..+0x70 マテリアルの退避 9 語
+0x78 今回使う表          +0x7C 今回使うチャンク数
+0x80 下画面 表           +0x84 下画面 チャンク数
+0x88 上画面 表           +0x8C 上画面 チャンク数
+0x90 上画面 確定         +0x94 上画面 集め中
+0x98 下画面 色配列        +0x9C 上画面 色配列   +0xA0 いま読む色の位置
```

#### ケーブの配置（`.text` の空きは `0x838080`〜**`0x839000`**）

```
0x838080 確保ケーブ（probe。常設ではない）
0x838400 記録要求フラグ強制   14 語
0x838500 マテリアル捕獲        7 語
0x838600 下画面パス入口       13 語
0x838680 上画面パス入口       13 語
0x838700 再生を控える         11 語
0x838780 マテリアル選定       35 語
0x838900 drawctx 記録          7 語
0x838AC0 トランポリン          2 語
0x838B00 描画ケーブ          301 語（末尾 0x838FC4）
```

#### .bss の使い方

```
0x009B0010 確保スロット
0x009B0D00 LOG（48 語）
0x009B0E00 下画面 スプライト表（1 件 0x50 バイト）
0x009B1400 上画面 スプライト表
0x009B1C00 下画面 色配列（1 チャンク 0x40 バイト）
0x009B1E00 上画面 色配列
0x009B1200-0x009B1C00 は空きを確認済み
```

#### 再開のしかた（実機を再起動した場合）

1. `PATCHES/cave_gfxalloc_probe.py` を `MODE = "install"` で実行
   （`CAVE = 0x838200` / `SCRATCH = 0x009B0020` / `ALLOC_SIZE = 0x8000` に
   なっているので、**0x4000 と 0x009B0010 に戻してから**使う）
2. `run_timed.py` を 1500ms で走らせ、確保できた番地を読む
3. probe を `MODE = "uninstall"`
4. `font_atlas_64x64_la4.bin` をその番地へ転送
5. `cave_draw_topmost.py` の `TEX_VA` をその番地にして `MODE = "install"`

### ★段 D / E / G の実装（ビルド済み・実機検証待ち）

| ファイル | 役割 |
|---|---|
| `Sources/GuiRender.cpp` | GPU 経路の 2D 描画器。`FillRect` / `DrawText` |
| `Sources/GuiMenu.cpp` | 自前チートメニュー（v1）。専用スレッドで毎 16ms 描く |
| `includes/MisakiGothic2nd8.hpp` | `GetGlyph` / `NextCodepoint` を公開（GPU 経路から読むため） |

#### GuiRender の作り

- **グリフアトラス 128x128 LA4**（16KB。`Alloc` の上限。F-221）。8x8 セルが 256 個
- **出てきた文字から順にセルを割り当てる**ので、362 字あっても足りる
  （同時に 256 種類出なければよい）
- 最後のセルは無地の不透明。矩形塗りに使う
- 座標は **画面左上原点・+Y 下・px**。ケーブ側（画面中央原点・+Y 上）へは描画器が変換する
- **表はプラグインの `new` で確保する。** CPU（ケーブ）が読むだけで GPU は触らないので
  物理アドレスは要らない。.bss の狭い空きに収める必要はない
- **表は 2 面**。書き終えてからポインタ、最後にチャンク数の順に差し替える。
  さらに両面とも全域を「大きさ 0 のダミー」で埋めてあるので、
  チャンク数が多めに読まれても何も描かれない
- **色はチャンク（7 枚）単位**なので、`Flush()` が同じ色のスプライトをまとめて詰める

#### ★テクスチャ寸法の差し替えを忘れない

書き出したケーブは 64x64 の値を持っている。グリフアトラスは 128x128 なので、
`OwnGui.cpp` が `kGuiTexSizeWord` / `kGuiTexFmtWord` を差し替える。
**reg 0x082 は `(幅<<16)|高さ`**（F-216）。

#### 段 G — ホットキー（CTRPF 本体にパッチ不要）

`PluginMenu::OnOpening`（`bool (*)(void)`）が **false を返すと CTRPF のメニューが開かない**。
CTRPF は Select で開こうとするので、そのとき DPad Up が押されていなければ止めて
自前メニューを開閉する。

```
Select 単独        -> 自前メニュー（ゲームは止まらない）
Select + DPad Up   -> 従来の CTRPF メニュー
```

#### ★実機で確認できたこと（F-222）

> Select で上画面の左からメニューが滑り込み、**ゲームも動き続け**、
> DPad 上下で選択が動き、選択帯が追従・明滅しています。
> A でチェックが切り替わり黄色になり、X で適用されています。
> Select + DPad Up では従来のメニューも開きます。

**目的（メニューを開いている間もゲームが進行する）は達成。**

直した不具合: 「未適用」を旗で覚えていたので ON→OFF と戻しても黄色のままだった。
**適用済みの値と比べる**方式へ変更（設計の `isDirty` と同じ）。L で戻す操作も追加。

#### ★実機で出た不具合 — しばらく遊ぶとクラッシュ（F-223）

`g_GpuCmdListMgr` が壊れて `Layout_RecordPaneTree` の中で落ちる。
**描くものが無いのに上画面のレイアウト（id 8）の記録を毎フレーム強制していた**のが原因。
id 8 は素ではほとんど記録し直されないので、少しずつ食い潰していた。

対策: **チャンク数が 0 のときは強制しない**（メニューを閉じている間は素の挙動）。

実機の結果: **メニューを開いたまま放置しても落ちない**（懸念は外れた）。
ただし**上画面に UI が無くなると、まだ落ちた** -> F-224 へ。

#### ★真因は「確定した対象を 0 以外のときだけ更新」していたこと（F-224）

再生が 1 つも無いフレームでは古いレイアウトのポインタが残り続け、
**その番地に別のオブジェクトが再確保されると誤って一致**して、
無関係なレイアウトの記録リストへ書き込んでいた。

対策: **無条件に確定させる**（0 でも入れる）。
0 なら一致せず、その画面には何も描かないだけで済む。

副作用: 上画面に UI が無い場面では自前メニューも描かれない。
常時出したいなら、上画面でも素で記録し直されるレイアウトを探すか下画面へ出す。

#### ★閉じても絵が残る不具合（F-225）— クラッシュにも寄与していた

描画スレッドが「開いている間だけ `Render()` を呼ぶ」作りだったため、
閉じ終わった瞬間に **.bss のチャンク数が最後の値のまま残り**、
ケーブが同じ絵を描き続けていた。

さらにチャンク数が 0 に戻らないので、**F-223 の「描くものが無いときは強制しない」
という条件から抜けられず**、記録の強制が止まらずコマンドリストを食い潰していた。

対策: **毎回必ず `Render()` を呼ぶ**（閉じているときは 0 チャンクになる）。

#### ★★根本対策 — 相乗り先を「素で記録し直される」ものにした（F-226）

`PATCHES/probe_top_natural.py` で上画面パスの中身を測った。

```
id38 → id37 → id28 → id29 → id16 → id6 → id8
 ○     ○      ×      ×      ○      ×     ×     （○ = 素で記録し直される）
```

**id 16 が「素で記録し直されるものの中で最後」**で、後ろの id 6 / id 8 は記録長 0。
つまり **id 16 に相乗りすれば実質最前面**で、**強制が要らない**。

- 相乗り先を **リスト id で選ぶ**（下 15 / 上 16。.bss の LOG+0xA4 / +0xA8）
- **記録要求フラグの強制フックを廃止**（フック 8 個 -> 7 個）
- これで F-223 の原因が構造的に消える

#### 旧: 描画順の当時の解釈（F-226 / F-228 / F-230）

**訂正:** F-233 では未立証へ戻したが、F-234 でロード画像は別描画系ではなく
`Layout_ReplayRecordedList` の id 10 と確定した。id 8 の後に replay されるため覆われる。

相乗り先は **「候補のうち最後に再生されたもの」** を実行時に選ぶ。
候補は下画面が id 15 / id 9、上画面が id 16 / id 8（.bss から変えられる）。
**記録の強制はしない**（どれも素で記録し直される）。

| 場面 | 結果 |
|---|---|
| 通常 | ○ 上下とも最前面 |
| フェード中 | ○ フェードの上に出る |
| **上画面のロード画像** | **✕ 隠れる**（下画面は正常） |

**ロード画像は `Layout_ReplayRecordedList` より後の別経路**で描かれる。
次の手は **`Frame_EndDrawPass1024`（描画パスの末尾）へ積む**こと。
F-202 で失敗した場所だが、当時足りなかった UI の GPU 状態は
F-206 〜 F-215 で自前に確立できるようになっている。

#### ★プラグイン側の .bss 初期化を漏らさない（F-231）

デバッガ版の install が書く値と、プラグインの `GuiRender::Init` が書く値は
**一致させること**。フェード候補の id を書き忘れて、
「フェードに隠れる」「ロード画面でクラッシュ」の両方が起きた。

`.bss` へ書くべきもの（ケーブが読む）:

```
LOG+0x80 下 表      LOG+0x84 下 チャンク数   LOG+0x98 下 色配列
LOG+0x88 上 表      LOG+0x8C 上 チャンク数   LOG+0x9C 上 色配列
LOG+0xA4 下 通常 id (15)   LOG+0xBC 下 フェード id (9)
LOG+0xA8 上 通常 id (16)   LOG+0xC0 上 フェード id (8)
```

ケーブ側も **id が 0 なら未設定として飛ばす**ようにした（番兵の検査）。

#### ★★積める量に上限がある（F-232）— **設計上の宿題**

レイアウトの**記録リスト**へ追記しているので容量がある。
実機では **19 チャンク（133 スプライト）で落ちた**（`Mem_Copy(dst=0)`）。
11 文字＝2 チャンクの試験では長時間安定していた。

当面 1 フレーム **6 チャンク（42 スプライト）**に制限した。

★**「GUI が出ない」の正体はおそらく座標系**。クラッシュ時の `.bss` は
上画面の確定対象が **id 8（フェード用）**、チャンク 19 だった。
つまり描いてはいるが、フェード用レイアウトの座標系で描かれて画面外へ出ている。
**メニューは本来 130 スプライト程度必要なので、これでは足りない。**

次に決めること:

- リストの残量を実測し、上限を根拠のある値にする
- あるいは **自前のコマンドリストを持つ**（記録リストへの追記をやめる）
- あるいは 1 フレームに描く量を減らす（文字を間引く・描画を分割する）

#### 旧: 当時の次設計（F-233 で前提を訂正済み）

以下の「3つとも消える」「投影も自前」「すべての描画の後」は未検証の旧記述。
実装判断には冒頭の F-234 と `HANDOFF_CHEATMENU.md` を使う。

いまは **レイアウトの記録リストへ追記**している。この方式には構造的な限界が 3 つある。

| 限界 | 症状 |
|---|---|
| **容量が小さい** | 19 チャンクで落ちる（F-232）。メニューには 130 スプライト要る |
| **候補ごとに座標系が違う** | フェード用（id 8/9）に積むと横に潰れる・画面外へ出る（F-230） |
| **後から別経路が描く** | 上画面のロード画像に隠れる（F-230） |

**`Frame_EndDrawPass1024`（`0x5A27C8`）＝描画パスの末尾へ積めば 3 つとも消える。**

- 容量はメインのコマンドリスト（レイアウトのものより桁違いに大きい）
- 座標系は**自分で決める**（投影行列も自分で積む）ので、場面によって変わらない
- **すべての描画の後**なので、フェードにもロード画像にも隠れない

★F-202 で一度失敗した場所だが、当時の敗因は
「メインリストの末尾には UI の GPU 状態が無い」だった。
その状態は F-206（マテリアル）/ F-207（UV セット数）/ F-214・F-215（定数色の中立化）で
**自前に確立できるようになっている。**

★★F-201 の注意は生きている。`GpuCmd_SplitAndSubmit` の直前に積むと、
呼び出し元がカーソル由来の値をキャッシュしていて巻き戻される。
**`Frame_EndDrawPass1024` の入口（提出より前）**に入れること。

#### 手順（次に着手するとき）

1. `Frame_EndDrawPass1024` の入口をフックし、**発火回数だけ**数える（描かない）
2. その時点の `g_GpuCmdPtr` / 残量 / drawctx が使えるかを読む
3. 無地の四角 1 枚だけ描いてみる（最小構成。F-168 と同じ進め方）
4. 座標系を目盛りで測る（F-208 の方法。**非対称な入力で試す**）
5. 文字・複数チャンクへ広げ、**量を段階的に増やして**壊れないか確かめる（F-232）

#### 残り — Simulator と同じ見た目・機能にする

`Plugin/CTRPF-GUI-Simulator/ui-model.js`（1112 行）と `app.js`（590 行）が正。

| 未実装 | 場所 |
|---|---|
| フォルダの出入り（木構造） | `createMenuTree` |
| インラインリスト / 上下画面リストボックス | `LISTBOX` |
| ダイアログ（閉じる確認・全戻し確認） | `DIALOG_DEFINITIONS` |
| 通知（上画面右下・キュー・Ease Out） | `NotificationTimeline` |
| 下画面の数値キーボード・スライダー | `numericKeys` / `textKeyLayout` |
| 下画面のかな 5 段 / QWERTY キーボード | `KANA_COMMON_KEYS` ほか |
| ホットキー設定と入力待ちウィンドウ | `HOTKEY_BUTTON_ORDER` |
| 跳ね返り（値変更 100ms / 決定 80ms） | `valueBounceDuration` ほか |
| 数値は PixelMplus10 で描く | `PixelMplus10Numeric8` |

#### 実機で確かめること（済）

1. `.3gx`（774,042 バイト）を SD へ置き、ゲームが動き出してから ON
2. **Select** で上画面の左からメニューが滑り込むか（Cubic Ease Out 320ms）
3. **メニューを開いたままゲームが動き続けるか**（これが目的）
4. DPad 上下で選択が動き、選択帯が追従して明滅するか
5. A でチェックが切り替わり、黄色（未適用）になるか。X で黄色が消えるか
6. **Select + DPad Up** で従来の CTRPF メニューが開くか
7. `/CTRPF_OwnGui.txt` に「テクスチャを 128x128 LA4 へ差し替えた」が出ているか

### 段 D の設計

- **グリフアトラス**は 128x128 LA4（16KB = 8x8 セル 256 個）。
  `Alloc` は 0x4000 までしか取れない（F-221）。
  フォントの実体は既に C++ にある（`Sources/MisakiGothic2nd8.cpp`。
  `{codepoint, width, height, offsetX, offsetY, advance, rows[7]}`、
  rows は LSB が左端のビット列）
- **LA4 にする**（A4 ではない）。A4 だと RGB が 0 になり、頂点カラーで色を付けられない
- 描画の素は 2 つだけ
  - `FillRect(x,y,w,h,色)` … 無地セルを引き伸ばす
  - `DrawText(x,y,文字列,色)` … 1 文字 = 1 スプライト
- **色はチャンク単位**なので、プラグインは**同じ色のスプライトをまとめて**
  7 枚ずつのチャンクに詰める

### 段 C の設計（ちらつき対策）

プラグインは自分のスレッドで表を作るので、ケーブが読んでいる最中に書くと崩れる。
**表を 2 面持ち、書き終えてから「使う面」のポインタを 1 語だけ差し替える。**
ケーブは毎回 .bss からポインタを読む。

### 2026-09-07 追記（F-323〜F-336。実機未確認分あり）

- 段 5（アニメーション）・段 5+（インライン・ダイアログ）・
  段 6（上下リスト・ホットキー・入力待ち）・段 7（通知）は実機確認済み。
  残りは F-323（枠の重なり）・F-324（描画順）・F-325〜F-336 の各確認項目
  （`HANDOFF_CHEATMENU.md` の「次にやること」1 項）。
- 関数側連携（`GuiMenu.hpp`）： 発火 hook・トグル実行・トグルエンジン・
  パッチ表・通知・`IsVisible`。試験配線は無敵モード・壁抜け
  （`WireTestEffects()`。ゲームメモリ無接触）。
- 予算： 借用 0x6C000 / 上 LIST_SIZE 0x20000 / Picture 56 枚/画面 /
  スロット上 63＋下 11 本。ゲームへ約 296KB 残し（目安 300KB を割る。
  場面転換の soak が要る）。
- 未解決のまま： `DeleteCmdLists()` の反復確認 / §3.2 共有バッチ移行 /
  `threadCreate()` の安全化 / ボタン立ち上がりの明示確認。

### 2026-09-08 追記（F-365・F-366。実機未確認）

- メニューON/OFF でホットキー判定を送る（opt-in）。
  `ToggleEvaluate()` をホットキー押下と共用。`SetEffectMenuJudgment()` で
  項目ごとに送る/送らないを切る（既定 OFF）。束縛の有無は問わない。
- しずえスキップをトグル式チートとして取込。木にチェック追加＋
  `0x0054C424` へ CTRPF フック 1 本（先頭 PUSH を確認。素でなければ掛けない）。
  部屋 0x63 で case 1 相当を自動発火＋通知。case 0（一括処理）は飛ぶ
  （成長への影響は未検証。HANDOFF_MESSAGE.md §7-3 が実機作業として残る）。
  使う字 14 字を BDF から追加しアトラス再生成（美咲 362→377、総字形 390→405）。

### 2026-09-08 追記（F-375。実機で要再試行）

- タイトルでチートON→即クラッシュ。犯人は空リスト＋陳旧リンクの
  永久スキップ（自前ノード prev が死リスト残骸で (b) が真になり、
  head=0 のまま `RenderTop`+0x0C が落ちた）。
- `build_a` を修正（head==0 なら stale 消去→挿入直行）。
  A2=`0x00838CE8`・N=`0x00838CF0` へ配置換え（A1 据え置き）。
  監査・リテラル・objdump・ビルド・検証器 2 種・プレビューは通過。
- 新しい 3gx でタイトルON→メニュー表示→しずえ遷移を再試行すること。

---

## TODO-133: プラグインを ON にするのが早すぎるとクラッシュする — **保留**（F-219）

プラグインが ready になった瞬間にチートを有効化すると落ちる。
**2 回目（ゲームが動いてから ON）は正常。** 実用上は回避できるのでユーザー判断で保留。
**対策を外した版（765,128 バイト）でも再現することを確認済み。**

```
PC 0551C928   （どこにも属さない番地）
LR 061CFCEC   （プラグイン内）
SP 0FFFFE00   （ゲームのメインスレッドのスタック）
R0 32FF62EC   （drawctx）  R4/R9 3225B070（レイアウト）
```

### 試して効かなかったこと

- `g_GfxAllocator`（`0x0094CA30`）が 0 なら中止する
- 払い出しが linear の窓（`0x30000000` 台）に無ければ使わない

**★効かなかった対策はコードから外した。** 残すと「対策済み」と誤解する。

### 次に調べるなら

- **こちらのケーブを 1 つも置かない状態**（確保フックすら置かない）でも落ちるかを見る。
  落ちるならプラグイン/CTRPF 側の初期化の問題で、こちらの領分ではない
- `PatchProcess` と `main` のどちらで組み込むかによる違い
- CTRPF の `Hook` を使う方式へ変えると変わるか

---

## ★中断チェックポイント（2026-08-30 セッション終了）

**ゲームは素の状態に戻してある。** 再開は `HANDOFF_RENDERING.md` の冒頭から。

### 次の一手 — 自前テクスチャへの差し替え（TODO-123 の残り）

色もテクスチャも、これ 1 つで取れる。根拠は F-185。

1. `g_GfxAllocator`（`0x94CA30`）から 256 バイト確保
   （**リニア FCRAM なので `PA = VA - 0x10000000`**。VRAM ではない）
2. 8x8 の RGBA8 単色を詰める（単色なのでタイリング無関係）
3. `DrawCtx_FlushBatch`（`0x4B8360`）のケーブから 3 組を発行:
   ```
   [0x00080008][0x000F0082]   大きさ 8x8
   [PA >> 3   ][0x000F0085]   アドレス
   [0x00000000][0x000F008E]   形式 0 = RGBA8
   ```
   発行位置はマテリアルのテクスチャ設定の**直後**なので上書きが効く（F-169 と同じ手法）
4. 通れば**色・アルファ・大きさ・位置・絵のすべてが自前**になる。
   SD から読んだ画像もビットマップフォントも同じ経路で貼れる

### 確定済みの土台

| 要素 | 状態 |
|---|---|
| 常時描ける相乗り点（ゼロフレーム 0.00%） | 済 F-177 |
| UI 画像を足す（GPU コマンドを書かずに） | 済 F-180 |
| 毎フレーム 1 枚に制御 | 済 F-181 |
| アルファブレンド | 済 F-181 / F-184 |
| 大きさ・位置 | 済 F-181 / F-182 |
| アルファ値の指定 | 済 F-184 |
| **任意の GPU コマンドの発行** | **済 F-185** |
| 色（RGB）・テクスチャ | 未 → 上記の手順で取る |

---

## TODO-123 [進行中 / F-180 / F-181] 追加した UI 画像を制御下に置く

**★1 フレーム 1 枚に絞れた。画面にも出た（F-181）。**
下画面に 400x240 の半透明の画像が毎フレーム 1 枚描かれる。
**アルファブレンドが効いている**＝ OSD を避けた目的が達成された。

適用は `PATCHES/cave_add_sprite.py`。
`Render_FrameEnd`(`0x4F1CE4`) でフラグを立て、1 枚足したら降ろす。

**残り:**

**★位置指定は達成（F-182）。** 複製した行列の
`ptr+48+12`（X）/ `ptr+48+28`（Y）へ絶対値を書けば、
複製元がどこにあっても固定位置に置ける。複製元は**地図の影**だった。

**★アルファの指定も達成（F-184）。** 索引エントリの `w3` を
自前の 4 隅色ブロック（`+1644` の索引 6..9）へ向ければ、アルファを自由に決められる。
**ただし RGB は効かない** — 地図の影の素材は頂点カラーをアルファにしか使っていない。

**残り:**

0. **★色は「自前テクスチャ」で取る（F-185 で方針が確定）。**
   フック地点で `R1` がコマンドカーソルなので**任意の GPU コマンドを発行できる**。
   TexEnv 定数色 6 段は効かなかった。相乗り先のテクスチャは **8x8 の LA4**（色なし）。
   → **reg `0x082`（大きさ）/ `0x085`（PA>>3）/ `0x08E`（形式）を自前の値で上書きする。**
   バッファは `g_GfxAllocator`（F-165/F-166）から取る（リニア FCRAM = `PA = VA - 0x10000000`）

1. ~~色（RGB）を効かせる~~ — 3 案（F-184）。
   **(a) 頂点カラーの RGB を使う素材のバッチに相乗りする（最も安い）**、
   (b) 出力コマンドの TexEnv（`0x0DB`/`0x0F3`）を書き換える（F-157 の手法）、
   (c) 自前マテリアルでバッチを分ける（自由度は最大だが重い）
2. **自前のテクスチャにする** — (c) と同じ問題。**1 バッチ = 1 テクスチャ**（F-183）
3. **レイヤーを選ぶ** — 相乗り先のバッチで描画順が決まる（F-181/F-182）
4. `(1,3,2)` 以外のバッチにも対応（整数→float 変換に VFP の `VMOV`/`VCVT`）

## TODO-122 [★主要部達成 / F-176 / F-178 / F-180] Pane 走査に相乗りして UI 画像を足す

**達成。** ゲームの UI 画像が複製され、大きさを変えて追加表示された。
**コマンドは 1 バイトも書いていない。** 描画コンテキストの 3 配列に
エントリを足してカウンタを増やすだけで、`sub_4B8360` が正しく描いた。

適用は `PATCHES/cave_add_quad.py`。

残りは制御（TODO-123）。

## TODO-121 [新規 / F-169] 描画の幅を広げる

土台は揃った（F-169）。ここから先は同じ仕組みの応用。

- **半透明の単色矩形** — バッファを全部 `0xF` にして `reg 0x0F3` で色と alpha を決める。
  追加の解析は不要。すぐ書ける
- **自前ビットマップフォント** — グリフごとに UV を変えて複数枚出す。
  `reg 0x228` = 6 * 枚数、定数を枚数分積む必要がある。
  **1 枚分より長いコマンド列を積むので、コピー先を伸ばす仕組みが要る**
- **SD から読んだ画像** — RGBA8 か RGB565 で置く。
  `reg 0x08E`（形式）と `reg 0x082`（寸法）を変える。
  **アルファのみ前提の TexEnv（`reg 0x0D8`/`0x0F0` 系）の調整が要る**

## TODO-120 [★達成 / F-169] 自前テクスチャを四角形に貼る

**達成。** 自前で確保したメモリに自前で詰めた市松模様が、
自前サイズ（80x80）の四角形に貼られて表示された。

適用は `PATCHES/cave_own_texture.py`。
`(オフセット, 値)` のテーブル駆動なので、値だけ差し替えれば実験できる。

## TODO-119 [★達成 / F-168] 自前の四角形を 1 枚描く

**達成。** 時計の分の 1 文字目を幅 40 / 高さ -40 に書き換えて拡大表示させた。
`CopyToCommandBuffer` で 2 枚目を追加する経路と、
ゲーム自身のコピーを直接書き換える経路の**両方で成立**。

適用は `PATCHES/cave_own_quad.py`（`WHICH` で 2 経路を切替）。

**★位置を動かす実験では、まず大きさだけを変えて位置は据え置くこと。**
`(X, Y)` は pane の変換行列に対する相対座標なので、大きく動かすと
画面外やシザー矩形の外に出て「描けていない」と誤診する（F-168 で実際に踏んだ）。

## TODO-118 [★解決 / F-167] 頂点属性（regs 0x200-0x22F）

**前提が外れていた。2D の矩形に頂点属性の解析は不要。**

テキストの batch には `reg 0x200`-`0x226` が**一つも入っていない**。
グリフは**頂点シェーダの float 定数から四角形を生成**して描かれる。

```
c[0x40 + 2k]     = (u0, v0, u1, v1)        UV。0..1
c[0x40 + 2k + 1] = (幅, 高さ, X, Y)         レイアウト単位。高さは負
reg 0x228 NUMVERTICES = 6 * グリフ数
reg 0x22E DRAWELEMENTS = 1
```

解読は `scratchpad/decode_text_batch.py`。詳細は F-167。

## TODO-117 [★解決 / F-163〜F-166] GPU 可視メモリの入手経路

**解決した。** `g_GfxAllocator->Alloc(size, 0x80)` をフック内（ゲームのスレッド上）から
呼べば、**GPU が実際に読めるメモリ**が得られる。実機で証明済み（F-166）。

```cpp
u32  alloc = *(u32 *)0x0094CA30;
u32  vt    = *(u32 *)alloc;
typedef void *(*AllocFn)(u32, u32, u32);
void *p = ((AllocFn)*(u32 *)(vt + 8))(alloc, size, 0x80);
u32   pa = (u32)p - 0x10000000;      // reg 0x085 に入れるのは pa >> 3
```

- プラグインからの `linearAlloc` / `svcControlMemory` は**カーネルが `OutOfMemory`**（F-163）
- 証明は「フォントアトラスの記述子（`table + 0x14*i + 8` = PA>>3）を
  自前バッファに向けたら時計の文字が四角になった」（F-166）
- キャッシュ flush は `svcFlushProcessDataCache(CUR_PROCESS_HANDLE, ...)`（未実測）

## TODO-116 [新規] 自前テキストを IPS で恒久化する

現在の 2 つのケーブはメモリパッチなのでゲーム再起動で消える。
`.text` 末尾のゼロ埋め `0x00838018`（F-161）は**ファイル上にも存在する領域**なので、
`code.ips` に落とせば恒久化できる。`DOCS/patches.md` の書式に合わせること。

ただし `TARGET_TB` は live アドレスで boot ごとに変わりうる（実測では同一だったが保証はない）。
恒久化するなら **pane 名（`T_nam_00` など）で照合する**か、
`TARGET_TB = 0` にして全 TextBox を対象にするなどの一般化が要る。

## TODO-115 [★解決 / F-147 / F-171 / F-175 / F-176 / F-177] UI の有無に依らず描く

**★解決。相乗り点は `nwlyt_Pane_DrawRecursive` (`0x73B524`)。**

実測（60 秒、建物の出入り・メニュー開閉を含む、1785 フレーム）:

| 経路 | 関数 | ゼロフレーム |
|---|---|---|
| TextBox | `sub_73CF48` | 83.8% |
| Picture | `nwlyt_Picture_DrawToCommandList` (`0x73CB58`) | 3.3% |
| **Pane 走査** | **`nwlyt_Pane_DrawRecursive` (`0x73B524`)** | **0.00%** |

**1 フレームも欠けない。** ロード中の「読み込み中」画像も
Picture ではない Pane 型で描かれており、その区間も Pane は 9 枚/フレーム走る。

F-147 より、この関数は cursor を `R1` で受け取り各 Pane の draw slot(+0x68) へ渡し、
戻り `R0` を次の可視 child へ渡す。**UI command stream を伸ばす走査本体。**

**次の作業（TODO-122 へ）**: ここに相乗りして自前の四角形を 1 枚出す。
F-176 より Picture は `drawctx+1640/1644/1648` の配列に四角形を溜め、
26 個で `sub_4B8360` が一括で流す。**カウンタを 1 増やして 1 エントリ足せばよい。**

## TODO-114 [新規 / F-158 / F-162] 自前 batch を組んで字形の制約を外す

現在は字形をゲームの batch 生成に依存している。
`SetString` フック（F-126）で内容は差し替えられるが、
**容量（pane の `cap`）と生成タイミング（F-162: 会話の最後のメッセージで発火）は
元 pane のものに縛られる。**

`TextBox_RebuildBatchWriter`(0x4BAFB0) が batch を作る経路を解き、
自前の TextBox もしくは自前 batch を用意できれば、この制約が外れる。
TODO-111 の「完全自前経路」と同じ問題。

## TODO-110 [主要部完了 / F-145] 会話 batch の後段 submit

会話TextBoxは専用list 32（0x9000 bytes）へ構築され、sourceと`R1+0x60`の632-byte一致を確認。
記録済みlist 32は `GpuCmd_ReplayRecordedListRange` でメインlist 1へ再生されることも実測した。
今回のreplayは同関数内で即時Splitせず、メインlistの通常フレームsubmitへ合流する。

残る任意の追加確認は「特定フレームのlist 1 submit直前に、再生済みTextBox commandを
byte tagで再同定する」こと。ただし自前テキスト実装に必要な構築先・再生経路は解決済み。

## TODO-111 [F-146] 自前TextBox生成か、既存batch再生かの分岐を決める

F-146により、正規TextBoxが作る `batch+0x10` は固定0x60-byte seedとglyph/state blockを
含むcommand sourceであり、F-145のlist 32録画・replayで表示されることまで繋がった。
次は次の二経路を混同せずに選ぶ。

- **既存TextBoxを借りる経路**: 安定して存在するTextBoxの文字列・位置・色を更新し、dirty化して
  正規batch再構築へ通す。自前GUIの最初の文字表示には最も低リスクだが、pane所有権と表示順を
  借りる。
- **完全自前経路**: `TextBatch_BuildCommandStream` の描画contextの生成・必要field、または
  atlas descriptor/texture bindをさらに解き、自前FuncNodeでbatch/quadを生成する。GPU command
  の所有権は明確になるが、atlas materializeとstate restoreの追加調査が必要。

まずは前者で「専用に確保した既存TextBoxを自前GUIノードの表示期間だけ利用できるか」を
静的に調べるか、後者を選ぶなら `0x4D6570` の描画contextの構成側と、batch内のtexture state
切替を追う。直接 `0x4D6570` を孤立して呼ぶ実験は、context fieldの契約が未確定なので行わない。

## TODO-112 [F-147] 2D panelをlist 32へ追加する最小経路を確定する

`nw::lyt::Picture` とTextBoxはともにPane treeのcursorを伸ばし、会話layoutではlist 32へ記録後、
main list 1へreplayされる。次は `nwlyt_Picture_DrawToCommandList` (`0x73CB58`) の入口/出口cursorを
同一Pictureについて採取し、1枚のPictureが占める正確なcommand rangeと、batch flush境界を取る。
再描画が起きない画面ではtraceが0件になり得るため、会話遷移・選択変更などlayoutがdirtyになる
操作で採取する。

その結果を使い、次の二案を比較する。

- native `nw::lyt::Picture` を既存Layoutに安全に追加して正規record/replayへ乗せる（所有権・破棄を要解析）。
- self-owned command rangeをlist 32 record/replayの明確な境界へ追加する（state restore・容量管理を要解析）。

いずれもscene `FuncNode` のworld/shadow pipelineを2D UI templateとして流用しない。F-147は
UI list 32を正規の画面固定panel候補として裏付けたが、新規panelの実装自体は未着手である。

**主要部完了（F-149）**: `0x4D71B8`で本文フレーム6 Pictureと`T_msg_00`を相対配置のまま
追加し、実機で別位置の整列したフレーム/本文を確認した。cursor rangeも入口/出口traceで取得済み。
残りは話者名・汎用asset・lifetimeを含む一般化である。

## TODO-113 [F-149] 会話依存でない自前GUI panelへ一般化する

- `SRC_PICTURE`をbootごとの固定pointerにせず、active Layout/Panesから名前で安全に取得する。
- `P_nam_00`の借用materialではなく、背景用Pictureのtexture/material契約を解き、自前assetまたは
  既存の安定assetを選べるようにする。
- clone transformのX/Y/size、表示条件、重なり順を明示的なパラメータにし、会話終了後にsourceを
  参照しない安全なlifetimeへする。
- 話者名を含めるなら `P_nam_00/01` と `T_nam_00` も本文と同じ背景基準の差分移動で追加する。
  名前TextBoxの既存batch（dirty=0、batch+8=1）を利用する最小実験は未実施。

**次回の最小再開手順**: 会話の途中でSuspend → source Pane/TextBoxのvtable/name/batchを再検証 →
`P_nam_00/01`と`T_nam_00`だけを既存成功版へ追加する。再起動済みならruntime `SRC_*` は無効なので、
先にtraceで再取得する。本文6 Picture＋`T_msg_00`の成功版は必ずuninstall状態から開始する。

## ★次のエージェントへ（2026-08-26 引き継ぎ）

**★まず `HANDOFF_RENDERING.md` を読むこと。これ 1 本で再開できる。**

自前描画は**画面に絵を出すところまで到達済み**（F-120 / F-121）。
残っているのは「自前のジオメトリ／テクスチャを描く」段階。
**当初目標「テクスチャの描画」は完全達成 (F-124)。**
自前ノード → 自前コマンド列 → 自前フォーマット → 自前画像、まで通っている。
着手しやすい順に **TODO-93（スウィズル順） → TODO-88（行列で任意位置） →
TODO-89（複数・形状） → TODO-92（カラー）**。

---


---

## TODO-00 [完了] 3x3 フックを外す

セッション2開始時に確認したところ `0x598688` は `EB0017C9`（未設置）だった。
ゲーム再起動でメモリパッチが消えていたため対応不要。

---

## TODO-01 [完了] 3x3 マス掘り

周囲 8 マスに穴・抉れ・土しぶきが中心マスと同期して発生する。実機確認済み。
構成は F-34、経緯は F-31、`Field_SetItemAt` が要る理由は F-33、
CTRPF ページについては F-32。

**残るのは恒久化のみ（TODO-06）。**

---

## TODO-01b [完了] `FieldAction_Dispatch` の case 3 到達経路

`FieldObj_ApplyRecordByAction` (`0x5A06D4`) の jumptable
（`0x5A0754`、base = `0x5A075C`、29ケース）で解決した。
**case 19（掘る）= `0x5A09D8`** で、`Item_InitWithId(&tmp, 0x9E)` の後
`FieldObj_SpawnActor` を呼ぶ。詳細は F-29。

---

## TODO-02 アイテム名の確定

ID 158（穴と推定）、38、43、`0x20A1`-`0x20A6` の実体が未確定。
アイテム名テーブルは romfs 側にあり `.code` からは引けない。
ROM を展開して名前テーブルを参照する必要がある。

`A:\Disassemble\acnl\ROM\` が既にある。中身を確認すること。

---

## TODO-03 コード走査範囲の拡大

以下はいずれも `0x100000`-`0x600000` が**未走査**。他経路が残っている可能性。

- `Actor_PlayAnim` への BL（スコップ以外の道具の速度も同様に取れる）
- `Player_BeginFieldObjAction` の呼び出し元（既知は 3 箇所）

MCP は 30 秒タイムアウト、読み速度は約 77KB/s。**1.5MB 以下**に分割すること。

---

## TODO-04 スコップ速度の未検証分

`DOCS/shovel_speed.md` の「未検証」3 件。

- `0x663466` / `0x680F4E` — `scoop_swing_wait1`(72)。保持モーションで体感しにくい。
  極端な値（`4180` = 16.0x）を入れて振り下ろし後の硬直が消えるかで切り分ける。
- `0x67DEC2` — `scoop_hane1`(74) の別経路。

---

## TODO-05 パッチの最小化

8 件は**まとめて適用した状態**でしか確認していない。個々の必要性は未検証。
1 つずつ外して確認し、不要なものを削る。

現時点で分かっている手掛かり:

| # | アドレス | 状況 |
|---|---|---|
| 3 | `0x598478` | **岩・構造物の両方がこれで直った**（実機）。必要 |
| 4 | `0x5984EC` | 構造物ケースでは通らない経路。不要の可能性 |
| 5 | `0x598550` | **岩には効かなかった**（実機で否定済み）。何に効くか不明 |
| 6 | `0x662E88` | #7 と同時適用で段差・アイテムが直った。単独効果は未分離 |
| 7 | `0x663294` | 同上 |
| 8 | `0x680F10` | #6 と対になる bit5 チェック。#6 で状態 74 に入った後、
`0x680EBC` が `Player_BeginFieldObjAction` を呼ぶために必要と推測。**未検証** |

`0x5984EC` と `0x598550` から外して試すのが早い。

---

## TODO-06 恒久化

`code.ips` を生成して `luma/titles/<TitleID>/code.ips` に置く。
ファイルオフセット = 仮想アドレス − `0x100000`（`DOCS/patches.md` に一覧あり）。
`.code` のファイルサイズが必要。

### 障害: 土しぶきケーブが `.code` の外にある

土しぶきケーブは CTRPF の空ページ `0x01E81000` にあり、
**`.code` の一部ではないので IPS に含められない**（F-32）。
`.text` 内の死にコードへ移す必要がある。

現在の空き:

| 領域 | 範囲 | 命令 |
|---|---|---|
| C | `0x663298`-`0x6632B7` | 8 |
| D | `0x598298`-`0x5982B3` | 7 |
| E | `0x59847C`-`0x5984AF` | 13 |
| A の残り | `0x663414`-`0x663453` | 16 |

土しぶきは 19 命令なので、**A の残り 16 命令 + 橋渡し**か、
D/E を繋ぐ形になる。

**未走査の候補**: パッチ #9 (`0x5982C4` を無条件 B) により
`0x5982C8`-`0x598327` (約 24 命令) が新たに死んだ可能性がある。
F-17 と同じ手順（B/BL 全走査 + 制御フロー解析）で確認すること。

---

## TODO-07 未解明の関数

役割が未確定のまま結論に使っているもの。裏取りが望ましい。

| アドレス | 使われ方 | 現在の理解 |
|---|---|---|
| `0x7237D8` | `0x59853C` から。非0で岩が跳ね返る | 在庫/容量チェック？ `RSBS R0,R0,#0x10` が見える |
| `0x767D80` | cat10 経路の分岐 | 不明 |
| `0x2FE984` | cat10 経路の分岐 | 不明 |
| `0x59FAF4` | `(x, y, 165)` で呼ばれる | 位置に何かあるかの検索 |
| `0x300A84` | 空マス時の地面種別 | 0/1=掘れる, 2=不可 |
| `0x6A53DC` | マップマネージャ取得 | 引数なし |

---

## TODO-08 [一部完了] 状態テーブルの未読エントリ

`g_ActorStateTable` (`0x843634`, `0x1C` 刻み) の構造が判明した:
`+00`=enter / `+08`=update / `+10`,`+18`=未確認（`+04`,`+0C`,`+14` は 0）。
状態 73 の `+08` が `Shovel_DecideState` であることが裏付けになる。

**状態 79 の役割が確定**（旧「役割未検証」）:
- enter `0x6691E0` = `ShovelState_DigEnter`。`Actor_PlayAnim(_, 73 or 76, _)`
- update `0x65BC7C` = `ShovelState_DigUpdate`。アニメIDで分岐し 3 系統のエフェクトを出す

状態 74 update = `0x674B10` (`ShovelState_SwingUpdate`) が
`unk_709FEC` でアニメ到達を検知して状態 79 へ遷移させる。

**未確認のまま**:
- 状態 76 (`0x4C`) の記述子 `0x843E84`（enter = `0x67AD24`）
- 記述子の `+10` / `+18` の役割

---

## TODO-09 [完了] 木にぶつかって切り倒す

実機で確認済み。**パッチは 1 つも当てず、`0x59BBB0` のフック 1 箇所だけで完結する。**
詳細は F-40 / F-41 / F-42。

| 項目 | 状態 |
|---|---|
| ぶつかって一撃で切り倒す | 動作 |
| 対象に応じた結果アイテム（木→切り株、竹→切断竹） | 動作 |
| 倒れる演出（物理・壁との当たり判定込み） | 動作 |
| **倒れる方向がぶつかった側に追従** | **動作** |
| 「揺する」が素の挙動（揺れるだけ） | 動作 |
| 斧が素の挙動（3 回） | 動作 |
| キューが詰まらない | 動作 |

`PATCHES/cave_tree.py`（`MODE = "install" / "uninstall" / "status"`）。ケーブは `0x01E81200`、40 ワード。

### 残っている検討事項

1. **恒久化 (`code.ips`)** — `0x01E81200` は CTRPF の空ページで `.code` の一部ではないため
   IPS に含められない。`.text` 内の死にコードへ移す必要がある。40 ワード必要。
   土しぶきケーブ（19 ワード）と合わせて **59 ワード**。TODO-06 を参照。
2. **木以外への影響** — `kind == 0` で分岐しているので、低木など他の
   フィールドオブジェクトにぶつかったときも介入する。実害は確認していないが未検証。
   必要なら `Item_IsGrowableCategory` で絞る。
3. **打撃カウンタの残留** — ぶつかったマスのカウンタを 3 にするので、
   万一そのまま倒れなかった場合、そのマスは次の斧一撃で倒れる状態が残る。
   ぶつかれば倒れるので実用上は問題にならない。

---

## TODO-10 [完了] 実機と同じ `.code` イメージを用意する

`dump_code.py` で吸い出した。**`NCCH/exefs/code_runtime.bin`、10,485,760 バイト、
VA `0x100000` - `0xB00000`。** アンカー 17 件すべて一致（F-46）。

`VA = ファイルオフセット + 0x100000`。IDA で新規に開くときは
ARM little endian / 32bit / ARMv6K、ロードアドレス `0x00100000`。

### 残っていること

1. ~~IDA で新規 IDB を作る~~ **完了。** `make_elf.py` で ARM ELF ヘッダを被せ、
   idalib-mcp のセッション `acnl` で開いた（`code_runtime.elf.i64`）。
   関数 73 件・型 6 件・コメント 14 件を反映済み。**`xrefs_to` が使える**（F-48）。
2. **`.code` 外のマップ領域の同定**（F-46）—
   `0xB10000`-`0xBD0000` / `0xBF0000`-`0xC40000` / `0xC50000`-`0xC60000`。
   `0xC00000` は ARM コード。CTRPF 側か、ゲームの別セグメントか未確認。
3. **`romfs/` を ACNL のものへ差し替える** — アイテム名・アニメ尺は romfs 側にある。
   現在置かれているのはマリオカート 7。

- **TODO-11** Vapecord `Daytime` / `EnvironmentDaytime`（採光パッチ、時刻とは別物）。
  JPN `DAY1 0x4AFD84` / `DAY2 0x1E6CB4`(float 1.25 を書く) / `DAY3 0x4AFD8C` / `DAY4 0x4AFDA8`。
  素の値と、`E3A01788` = `MOV R1,#0x2200000` / `E8871015` = `STM R7,{R0,R2,R4,R12}` が
  何を書き換えているのかは未確認 (F-60 §7)。
- **TODO-12** `g_TimeOffsetNs`(0x9564F8) を直接動かす時間変更が成立するか実機で確認する。
  静的には最も筋が良いはずだが、`Time_AnchorFromSave` がいつ張り直すかを観測していない。

- **TODO-13** `sub_596C84`（HOST5/6 の包含関数）の正体。呼び出し元 8 件以上の汎用処理で、
  drop.cpp の作者も「unnecessary?」と書いている (F-61)。
- **TODO-14** host drop を実機で検証していない。静的解析のみ。
  ホストを騙るパッチなので**オンラインでは相手側の状態を壊しうる**。試すならローカル限定で。

- ~~**TODO-15**~~ 解決 (F-63)。`sub_598EC4` = `Drop_FindAdjacentHole`
  「隣接 3 マスから ID 158 = Hole を探す」判定。「ドロップ15x15」とは実際に衝突する。
- **TODO-16** `Drop_FindTargetTile` の第 5 引数 `a5` の呼び出し元。
  非 0 だと添字が `(i+1) % 9` のままで 15x15 化が効かない (F-62)。
- **TODO-17** 「ドロップ15x15」の副作用を実機で確認する。
  `0x859248`（斧・スコップ）と `0x859254`（植物エフェクト、ID 159-215）が潰れるはず (F-62)。

- **TODO-18** `sub_5E284C`（`0x5E284C`）がメニュー項目追加関数かの確認。
  `ItemMenu_Build` の命名根拠なので確定させたい (F-63, 現状 MEDIUM)。
- **TODO-19** `Item_CanPlant` / `Item_CanPlaceHere` が呼ぶ
  `sub_5B3CD4` / `sub_76BD4C` / `sub_769FB4` / `sub_767930` の中身 (F-63)。

- **TODO-20** FOXXY `pseudoType0x21` の画面上の効果。静的には 2 レコードの合成が追えない (F-64)。
- **TODO-21** `g_DigRecordArray` の `state = 2` になったレコードを後段で処理するものの特定 (F-64)。
- **TODO-22** FOXXY の USA→JPN 差分 `0x16C8` が有効な帯域の境界。
  `0x594000`-`0x5A3000` では確認済みだが、`CLEARLOCKED` だけ `0x2C44` なので単純な一定差ではない (F-64)。

- **TODO-23** ドロップ種別 1-0x22 の各意味の対応付け。
  `0x0A` ドロップ / `0x0B` スコップ / `0x0C` 花植える / `0x0D` マイデザ /
  `0x0F` 置いても見えない / `0x21` 無検証・無演出 は確定 (F-65)。残りは未確認。
- ~~**TODO-24**~~ 完了 (F-93)。A は何も起きず、B は変化なし。原因は判定が 2 段だったこと。
- ~~**TODO-25**~~ 完了 (F-93)。2 行とも当てれば通常ドロップでも重ね置き可。実機確認済み。
- **TODO-25** オンライン髪型変更チートを隔離環境で動的検証する (F-66)。
  - `player+0x148` を監視し、状態キック先が `+0x1A8` / `+0x2D4` のどちらになるか確認。
  - `DD000000 00000100` は標準 CTRPF では R。配布文の A と実際の入力順（R 状態キック → A アクションか）を確認。
  - 判定 NOP 3 箇所と `0x70→0xB9` のうち必要最小限、および `0x060D0600` が必須かを切り分ける。
  - remote sync が存在するため、野良オンラインでは行わずローカル通信か同意済みの検証相手だけで試す。
  - F-67 の頭装備保持＋1 tick 即時化候補を実機で確認する。自分側の Hat/Accessory、セーブ再読込後、
    パッチ済み相手、未パッチ相手の 4 条件を分けて観測する。
  - 即時化中に通常の目色変更・Mii マスク変更を行い、状態 `0xB9` 全体への副作用を確認する。

- **TODO-26 [主要項目完了]** `PATCHES/cave_hair_instant.py` のA入力後を実機確認する (F-68)。
  - **確認済み**: 男「けだるいゆるさ」 (`0x0C`) が即時表示される。
  - **確認済み**: Hat、Accessoryを含む衣装8枠が全て維持される。
  - **確認済み**: Uninstall後にゲート3箇所・hook・caveが全て元へ戻る。
  - 保存後の再読込でも HairStyle `0x0C` が維持されるか。
  - オンライン人数が0以外の隔離テストでは元の虫取り網処理へ戻り、profileを変更しないか。

- **TODO-27 [第7版・服preview crash静的解析待ち]** 通常カタログ mode 0 の屋外統合 (F-69～F-92)。
  - `BsMenuMgr` の常設子、11タブ、27状態、command byte、`MENU_FLAGS`契約、Catalogの
    init/update/end、field X ownerとの非対称を `code.bin.i64` で再構築済み。
    詳細は `DOCS/menu_system.md`。
  - **訂正済み:** `BsMenuMgr+500` は `BsHandCursor`、`+480` が `BsMenuTab`。
    Catalog初期化はcursorだけを隠し、fieldタブを退場させない（F-80）。
  - **訂正済み:** Catalogは通常持ち物用 `MENU_FLAGS 0x08/0x10`を立てない。
    そのため「メニュー終了まで待機」`0x6D7194` はgenericな待機として流用できない（F-80）。
  - **最新失敗の原因確定:** constructor成功後にタブを退場させた版は、退場完了後
    `0x08==0` を見て `0x20`を即時発行し、生成済みCatalogを表示前に終了させた（F-81）。
    ghost閉じるbuttonはCatalogではなく `BsMenuTab` index 10。
  - **終了後lockの原因確定:** Catalogは自身と背景だけを終了し、field Xが開始したplayer
    state `0x16`、controller state 5、タブ、cursor、地図を戻さない。開始ownerと終了ownerの
    不一致であり、Catalog destructorの失敗ではない（F-82）。
  - **3Dの静的判定:** stock room 0は `BsFtrMgr` type `0xEE`を生成しないが、容量38枠と
    Item.bin家具family用の固定actor factoryは利用できる（F-83/F-84）。
  - **F-86訂正:** active `ScStage` とsaved `BsMenuTab` は精密再読で共に
    `+14=1/+15=0`。両者ともchild gateを通り、parent拒否説は撤回した。
  - **二つ目の不具合:** `g_BsFtrMgr` はphase 1中に公開されるため、nonnullだけでcacheを
    無効化すると早過ぎる。Catalogは失敗後に同一品を再試行しない（F-83/F-84）。
  - **除外済み:** `CameraCatalog`、Catalog専用3灯、renderer layer 2はroom 0にも存在する。
    camera/light/pass欠落を再調査しない（F-85）。詳細は `DOCS/furniture_rendering.md`。
  - saved `BsMenuTab` parent＋完全ready待ちの第2版でも、実機は
    `owned=0/status=3/g_BsFtrMgr=0/actor=0` で3Dなし。
  - **F-87静的最有力:** room 0容量38はphase 1でCPU 3,648,000 bytes＋VRAM 988,000 bytesを
    late allocationする。CPU bank heapが1件でもnullならnew childは同一呼出し中に破棄される。
  - 第3版はadapter activeかつpreview status 0の間だけ `0x68FD2C` で容量を1へ制限し、
    `(byte[19]&3)==3` 待ちとCatalog `+8160` cacheの1回再試行を維持する。適用・読戻し済み。
  - **F-87動的裏付け:** 容量1でmanager `+24=1`、`+19=1`、published pointer nonnullまで
    到達した。以前の38-bank phase 1即時失敗説を支持する。
  - **F-88クラッシュ原因確定:** 第3版はready待ち中もstock preview bodyへ戻ったため、phase 1
    公開直後にtype `0xBC` actorを生成し、`BLX` targetが命令語 `0xE1A04000`になった。
    例外actorを基底vtableへ戻してstock破棄へ渡し、クラッシュ状態は回収済み。
  - 第4版はmanager生成frameとstatus 1の未ready期間にpreview update全体からreturnする。
    例外停止中にprivate stateを保持して差し替え、読戻し後に再開済み。
  - **F-89:** 2回目はmanager phase 3のfield map走査が屋外Item `0x2090`をdefault
    type `0xBC`で生成した別経路。Catalog cached Item `0x2EA3`ではない。
  - 第5版はadapter-owned phase 3だけ `Field_GetMapManager`を0にし、map走査を省く。
    進行中actorはstock破棄し、走査後へ戻してmanager完了bit `3`を命令stepで確認済み。
  - **F-90:** 3回目は選択Item `0x2EA3`自身。record family 1が正規にtype `0xBC`
    (`AcFtrLoop`)を選ぶが、屋外objectのgeneric create vptr+8は `0xE1A04000`だった。
  - 同objectの4 vptrを基底`AcFtr`へ戻して例外直前から再実行すると、pre/create/postは
    `0x6E3A10 / 0x81F2B8 / 0x307D08`、create result 2、preview actor attachまで成功。
  - 第6版はadapter active中のpreview openだけtype `0xBC -> 0xBB`にする。Item requestは不変。
  - **3D成功:** 第6版で `0x2EA3`「0のランプ」と `0x2E78`「12つぶのぶどう」を連続表示。
    どちらもfamily 1/type `0xBC`を基底`0xBB`へ置換したactorである。
  - **F-91:** `0x2C89`「1UPキノコ」はfamily 3/type `0xBD`で、同じprimary
    `vptr+8=0xE1A04000`によりSIGSEGV。モデル固有ではなく特殊actor family共通の生成契約差。
  - 第7版はadapter active中のpreview openだけ、特殊家具type範囲 `0xBC..0xEB -> 0xBB`とする。
    例外actorは基底vptrでcreate result 2、Item `0x2C89`としてattach済み。
  - **家具3D確認完了:** 1UPキノコを含む家具は一通り表示された。通常家具に対する基底化は有効。
  - **F-92:** 壁紙・絨毯などは非表示。服カテゴリへ移動すると
    `0x317BD0` (`ModelInstance_SetRenderLayer`) でSIGSEGV。以前の無効vtable crashとは別段階。
  - 作業中断・電源断のため、服crash時のregister、stack、actor、個別Itemは未採取。
  - **次回は静的解析から開始:** `CatalogPreview_UpdateActor`のカテゴリ3/4/41変換、mannequin分岐、
    `AcFtr_CreateFinalize -> ModelInstance_SetRenderLayer`のcallerと引数を追う。
  - rev7の範囲fallbackが服用派生actorまで基底化した影響か、屋外で服model instanceが
    未初期化なのかを静的に分離してから、guardを家具だけへ狭めるか服専用初期化を追加する。
  - 壁紙・絨毯がstock室内Catalogでどのpreview経路を使うかも別途比較する。
  - 3DS電源断後はruntime patchが消える。Remote GDB再接続後、必要時にrev7を再installする。
  - 現在部屋ID `0x3C` の偽装や、室内のactor/factory/light pointerの屋外持越しは行わない。

## 描画 / GPU（F-94 以降）

- ~~**TODO-26**~~ 完了 (F-95)。`g_GpuCmdPtr`(`0x96EA94`) がコマンドバッファ書き込み位置。
  専用 AddCommand は無く各所でインライン生成。
- **TODO-31** `sub_121E2C`(`0xCA4`, `0x121E2C`) の解析。GPU コマンド層で最大。
  状態更新かコマンド列フラッシュの本命 (F-95)。
- ~~**TODO-32**~~ 完了 (F-96)。`GpuCmd_SplitAndSubmit`(`0x1280CC`) が終端して提出する。
- **TODO-33** `sub_13B5AC` / `sub_1372B8` の確認。GSP 共有メモリへの実際の書き込みと通知。
- **TODO-34** `GX_SetMemoryFill` / `SetDisplayTransfer` / `SetTextureCopy` の引数を
  逆コンパイルで確定させる（現状は switch 位置からの同定で MEDIUM-HIGH）。
- **TODO-35** フレームごとに `GpuCmd_SplitAndSubmit` を呼ぶのは誰か。描画ループの入口。
  鎖 `sub_16A130` → `sub_15504C` → `sub_1534A8` → `sub_4DE7F4` は辿ったが、
  **画像コーデック側の疑いがあり未確定** (F-97)。
- **TODO-36** `0x153000`-`0x176000` の正体を確定させる。
  `sub_14A9C8`(YUV→RGB) が同居しており、描画ループでなく画像処理の可能性 (F-97)。
- ~~**TODO-37**~~ 否定 (F-98)。`sub_11CE64` は文字列 `"sead::DefaultGfxMemoryMgrCtr"` を持つ
  **sead のグラフィクス初期化**だった（`sead_GfxMemoryMgr_InitBuffers` に改名）。
- **TODO-38** ★フレームループの実体を `sead::UlcdDoubleCmdGameFrameworkCtrNw4c`
  (vtbl `0x8FFC74`, 実装 `0x53F000`-`0x561000` / `0x74B000`-`0x750000`) の
  vtable から特定する (F-98)。
- **TODO-39** `sead::MethodTreeMgr` / `MethodTreeNode` の毎フレーム呼び出し木を辿る (F-98)。
- **TODO-40** `sead::PrimitiveDrawer`(`0x544E54` 付近) の描画メソッド。
  **自前描画の最有力候補**なので優先度高 (F-98)。
- ~~**TODO-41**~~ 完了 (F-100)。5 本とも impl の type バイトを確認し HIGH 化。
- **TODO-43** `sead::PrimitiveDrawer` の**描画メソッド**を特定する。
  `0x544E54` は dtor であって実装位置ではない (F-100)。
- **TODO-44** `sead::UlcdDoubleCmdGameFrameworkCtrNw4c` の実インスタンスが
  生成・使用されているかを確認する（現状はクラスの存在のみ実測）(F-100)。
- ~~**TODO-27**~~ 完了 (F-96)。`GxQueue_Dispatch`(`0x12E7D8`) が 28B キューを型で振り分け、
  `GX_SetCommandList`(`0x136F0C`) が GSP 共有メモリへ積む。GX API 5 本を同定。
- **TODO-28** 毎フレームの描画ループ入口の特定。
- **TODO-29** `nw::font::RectDrawer`(`0x4D7418`) の描画経路 — テキスト描画の本命。
- **TODO-30** `nw::lyt::Drawer`(`0x4D7414`) の描画経路 — テクスチャ/2D の本命。
- **TODO-42** `registers.h` を使って、これまで観測した全ヘッダのレジスタ名を洗い直す (F-99)。
  今後 GPU コマンドを読むときは必ずこの表を引く。
- ~~**TODO-45**~~ 完了 (F-102)。実機で恒等式 `mgr[1]+mgr[3] = g_GpuCmdPtr` と
  二重バッファのスワップを直接観測。コマンドバッファ関連は `HIGH` へ。
- **TODO-47** `mgr[7]`(`0xC00`) と `mgr[11]`(`0x300`) の意味。両インスタンスで同値の定数。
- ~~**TODO-48**~~ 一部完了 (F-103)。GX キューをメモリから直接読み、
  type 1/2/3 の実機発火を確認して `HIGH` へ。
  **type 0 `RequestDma` と type 4 `TextureCopy` は未観測（MEDIUM のまま）。**
- **TODO-49** `0x32677600`（size `0x26070`）の固定コマンドリストの中身。
  毎フレーム 2 回 `flags=2` で提出される。自前コマンド列の手本になりうる (F-103)。
- **TODO-50** `DisplayTransfer` の `dim=0x01A00100` と画面サイズの対応を確定する。
  上下画面の割り当ては現状 LOW (F-103)。
- **TODO-46** `g_GpuCmdListMgr` の `mgr[10]` の役割を確定する。
  `mgr[9]`（処理カーソル）とは別物 (F-101)。実機では両標本とも 0 だった (F-102)。
- ~~**TODO-51**~~ 完了 (F-106)。`Scene_DrawLayers` = レイヤー別 4 周のシーン走査。
  **`g3d::FuncNode`（`+0x148`/`+0x14C` コールバック、`+0x150` ユーザーデータ）を発見。**
- ~~**TODO-55**~~ 完了 (F-107)。呼び出し元 12 箇所。常用されている。
  登録 API `g3d_FuncNode_SetCallbacks`(`0x4EFF58`) も判明。
- ~~**TODO-59**~~ 完了 (F-109)。実機で FuncNode の実在・vptr 一致・
  コールバックの中身まで確認。**描画解析で 2 例目の `HIGH`。**
- **TODO-63** `sub_4EEDD8` / `a1 == 1024` 経路のシーン構成を実機で見る (F-109)。
- ~~**TODO-60**~~ 完了 (F-111)。**繋がない。`Scene_SubmitNode`(`0x4ED630`) を毎フレーム呼ぶ。**
  `Create` の第 1 引数は holder で、`holder[1]` にノードが入る。
  `Scene_SubmitNode(holder, sceneIndex)` が `Accept(traverser)` を呼び、
  `SceneContext` の配列 #0 へ push される。`Render_FrameEnd` が毎フレーム空にする。
- **TODO-62** レイヤー 0 を使う FuncNode は**見つかった** — `SortMeshGroup_InitAll`(`0x4EDF60`) が
  `cb0 = sub_4ED1C0` / `cb1 = sub_4ED458` の両方を設定している。中身の解析は未了。
- ~~**TODO-64**~~ 完了 (F-112)。実機で全項目一致。**F-111 は `HIGH` へ昇格。**
  `n: 0 → 1` と要素の一致で push を直接確認。誤り 2 件（配列 #5 の用途、
  `Accept` の visitor スロット）も見つけて訂正した。
- **TODO-65** `byte_94CA2C`(`0x94CA2C`) の意味。sceneIndex 0 と 1 を切り替えるモードフラグ。
  実機で値を読み、画面との対応を取る。
- **TODO-66** 半分解決 (F-115)。Visit 6 本を全部読み、**どの配列を誰が埋めるかは判明**
  （#1←vtbl[5] / #2←vtbl[6],[7] / #3←vtbl[7] / #4←vtbl[8]=カメラ / #5←vtbl[9] / #14←[6][7][8][9]）。
  **残り: どのノードクラスがどのスロットを使うか**（＝各配列の中身の意味）。
  各クラスの `Accept`（vtable[4]）が呼ぶ visitor スロットを列挙すれば出る。
  `Render_DrawSceneIndexed` の配り先 `0x9C3088`（4 個）の正体も未確定。
- **TODO-76** `Frame_DrawPass1024` / `1040` が `vtbl_SystemTask` のスロット 25/26 なのか、
  デリゲートの vtable 基点なのかを決着させる（F-115 で両論併記のまま）。
  実機で `*(node+0x2C)` の値を読めば一発で分かる。
- **TODO-77** `sub_148E94(dst, mtx, header)` の中身（F-114 で未検証のまま説明した）。
  14 dword 進むことしか確認できていない。
- **TODO-78** `sub_7E4A18`（配列 #2 への push）が `nwut_Array_PushBack` と何が違うか。
- ~~**TODO-68**~~ 完了 (F-113)。持ち主は **`BsShadowViewMgr`**。
  生成 = vtable[3](`0x28FE24`)、登録 = vtable[12](`0x28FE0C`)。
  `sceneIndex` は `*(this+200)`（部屋カテゴリで 0 か 2）。実機で `2` を確認。
  **フレーム描画の全体像と `Base` の 4 フェーズ構造まで判明。**
- **TODO-69** `Base` のフェーズ B（slot 5/6/7）と C（slot 8/9/10）が何か。
  走査関数 `sub_51EEA0` / `sub_51F024` / `sub_51F1A8` のフェーズ番号と呼び出し元を見る。
- **TODO-70** `Frame_DrawPass1024` と `Frame_DrawPass1040` が
  上画面 / 下画面に対応するかを実機で確認する（現状は仮説）。
  `unk_9C30B0` 周りのターゲット情報を両パスで比較すれば分かるはず。
- ~~**TODO-71**~~ 完了 (F-114)。**① 既製ブロック 4128 バイトを `Mem_Copy`
  → ② 色＋アルファと行列だけ組む → ③ 頂点属性を完全リセット**、の 3 段構成。
  F-109 の「頂点属性バッファの設定」は**方向が逆で実際はリセット**だった（訂正）。
- **TODO-73** ① の既製ブロック（実機 `0x308950D4`、1032 dword）を**誰がいつ作るか**。
  `*(this+0xB4)` / `*(this+0xB8)` に入れる側を特定する。
  自前描画でも同じ「作り置き＋ memcpy」をやりたいので、その作り方を知りたい。
- **TODO-74** `BsShadowViewMgr_BuildShadowCmds` の 27 カテゴリ表
  （`unk_98F628` の 356 バイト構造体、`unk_991B80` の 28 バイト記述子、
  `dword_ABB854` のリスト配列）の中身。影の種類とモデルの対応。
- **TODO-75** 第1段達成 (F-116)。`PATCHES/cave_scene_node_dup.py` で
  **任意のシーンへノードを 1 個追加できた**（`ctx[1] n=1` を実機で確認）。
  **残り: 自前のコールバックを実際に描画させる。**
- ~~**TODO-79**~~ 完了 (F-117)。**ハングしない。** `ctx[2] n=2` で正常動作を確認。
  F-116 の「ハングの疑い」は、1 フレームに 1 回の bp が未ヒットだったのを
  誤読したもの。**自前ノードを足しても描画は破綻しない**ことが確定した。
- ~~**TODO-80**~~ 完了 (F-119)。`PATCHES/cave_own_funcnode.py`。
  **自前ノードを生成し、自前コールバックが毎フレーム呼ばれることを実機で確認**
  （`COUNTER = 62 / 2 秒 ≒ 31fps`）。アロケータは `g_GfxAllocator` を採用。
- ~~**TODO-81**~~ 達成 (F-120)。**自前ノードから実際に画面へ描画できた。**
  本来の影ノードの登録を NOP 化しても影が出た＝描いていたのは自前ノード。
  ひな型は `PATCHES/cave_own_funcnode.py` の STUB（`0x01E81680`）。
- ~~**TODO-83**~~ **解決 (F-122)。** 影インスタンスのリストは**最初の呼び出しで消費され、
  2 回目は 1 個も描かない**（`DRAWELEMENTS` が 0 回）。深度でもブレンドでもなかった。
- ~~**TODO-84**~~ **達成 (F-122)。完全自己完結の自前描画。**
  ゲームの描画関数を一切呼ばず、既製ブロック 4128B ＋ 自前テンプレート 432B を積むだけで
  画面に描画。選んだインスタンスと見えたもの（テント前の柵の影）が一致。
- ~~**TODO-87**~~ **達成 (F-123 / F-124)。** 影のテクスチャの実体を特定し、
  自前の絵に差し替えて画面に反映させた。
  **★カテゴリごとにテクスチャと寸法が違う**（32×32 `0x33076480` / 32×64 `0x3307EF80`）。
  テンプレートを作るときは切り出したカテゴリ設定が指すテクスチャを見ること。
- ~~**TODO-90**~~ **達成 (F-124)。任意の自前画像を画面に表示できた。**
  `0x08E` を `0x0A`(L4)、`0x083` の ETC1 フラグを落とし、
  テクスチャ本体（仮想 `0x3307EF80`、32×64、1024B）を自作の市松模様に差し替え。
  **当初目標「テクスチャの描画」完全達成。**
- **TODO-92** カラー画像を出す。現在の枠（1024B）は 4bpp までしか入らない。
  `RGBA8` 32×64 には 8192B 必要なので、**GPU 可視の大きなバッファを確保する**方法を探す。
- ~~**TODO-93**~~ **達成 (F-125)。** タイル内 Morton 順を確定し、テキストが読めた。
  `i = x0|y0<<1|x1<<2|y1<<3|x2<<4|y2<<5`、タイルは行優先、L4 は下位ニブルが先。
- ~~**テキスト描画**~~ **達成 (F-125)。** 8×8 グリフで `"ACNL"` を表示。
  wrap を CLAMP_TO_EDGE にして鏡文字も解消。
- ~~**TODO-94**~~ **達成 (F-126)。UI 層に自前の 2D テキストを表示した。**
  `nwlyt_TextBox_SetString`(`0x4BACBC`) をフックして引数を差し替える。
  わずか 9 ワード。住民名が `あんこ` → `テスト` に変わることを確認。
  `PATCHES/cave_textbox.py`（`trace` / `dump` / `install` / `uninstall`）。
- ~~**TODO-95**~~ **不要と判断。** 文字数が増えるだけで、位置・フォント・装飾のどれにも
  寄与しない。ユーザーの目標には貢献しないので取り下げ。
- ~~**TODO-96**~~ 前進 (F-127)。**位置は `+40`/`+44` を書けば動く**（要 `+254` bit0）。
  自前生成は不要で、既存の箱を移動させれば足りる。
- ~~**TODO-97**~~ **解決 (F-128)。影は独立した `TextBox` ペインの重ね描き。**
  本文 `T_itm_na` (0,0) / 影 `S_itm_na` (1,-1)。ペイン名の接頭辞で判別できる。
  **フォント側ではない。** 色・ずれ幅・有無をすべて制御できる。
- ~~**TODO-98**~~ **解決 (F-129)。** `+224` は `nw::font::ResFont*` と確定。
  時計本文だけを7px版へ差し替えると、本文 `06` がぼやけた「あ」に変化し、影 `06` は
  未変更だった。実描画まで差し替わることと、本文・影の独立性を目視でも確認した。
  counter26px版の1行表示も確認後、通常版へ復元済み。
- **TODO-99** 前進 (F-131)。横の折り返しと縦方向非clipは解決。
  `TextBox+72` のpane width 26がwriterのwrap limitになり、7px glyph 2文字のscaled advance
  36が超えるため2行になる。pane height 21.6はwriterへ渡らず、2行目はclipされず画面外へ出る。
  残りは右端1〜3pxの見た目がCWDH `glyphWidth=6`によるink欠落かadvance余白かの比較試験。
- ~~**TODO-100**~~ **解決 (F-130)。** 7px版の数字CMAP欠落、alternate `U+3041「ぁ」`、
  `nwfont_ResFont_SetLinearFilter` (`0x4D7474`) を確定。両filter bitをOFFにすると拡大glyphが
  くっきりしたドット表示へ変化した。試験後は両bitをstock `0x6`へ復元済み。
- ~~**TODO-101**~~ **解決 (F-132)。** 7px fallback glyphの右端比較。
  pane widthを40へ広げて折り返しを除いた上で、要求size `18 x 24`（`18/7`、`24/7`の
  非整数倍率）と `14 x 14`（横・縦2倍の整数倍率）をNEARESTでA/B比較した。
  font/CWDH/string/pane/filterは固定し、サイズだけを変更。整数倍率で右端の欠け・不均一さが
  改善したため、原因はbuffer越境ではなく非整数倍率の最近傍ラスタライズ境界と判断した。
  CWDH `glyphWidth=6`→7改変やnative 7x7試験は不要とし、stock資源を維持する。

**F-135 再監査メモ:** `code.bin.i64` と `code_runtime.elf.i64` の6つのfont/GPU関数は
同じVAで raw bytes の差分が0、vtable・magic文字列・主要xref・2つのloader callerも一致した。
したがって静的なビルド対応と分岐記述に反例はない。ただし `code_runtime` はライブ実機ではなく、
このセッションには `ida-pro-mcp` のGDBメモリ endpointが公開されていなかったため、実機値の
動的確認とは扱わない。この接続制約は F-138 で解消し、F-139 でCMAP/glyph/batchの実機値を
別途採取した。F-135自体のbyte/xref照合という結論は変更しない。

**F-136 補正メモ:** 旧記述で `0x143718` を `GSPGPU_FlushDataCache`、`0xFFFF8001` を
flush command としていたのは過剰だった。`0x143718`→`0x144C44` は IPC header
`0x001F0082` を使う別 request で、`0xFFFF8001` は process handle 値。既知の
`0x13B6A4` (`0x00080082`) と同じ API とは断定せず、`nwgfx_GspGpu_RangeCacheOp_1F`
（正確な flush/invalidate semantics は未確定）として扱う。

**F-137 補正メモ:** `0x4D8484` の decompiler が `0x7ABDBC` の packed 引数を省略するため、
filter-only と誤読しない。assembly では `0x4D5118` の width/height/format/raw が同関数の
format switch と `0x7ABDBC` dispatcher に入る。texture setup と wrap/filter state の複合経路
であることは静的に支持されるが、backend の実 GPU side effect・format enum・live 値は未確認。

**F-138 接続メモ:** GUI IDA の `127.0.0.1:13337` は正常で、explicit `--ida-rpc` の
standalone proxy から `server_health`/`py_eval`/live memory を検証済み。初回自動検出は
Codex sandbox の `APPDATA` 欠落で失敗したため、プロジェクト `.codex/config.toml` に
`mcp_servers.ida_pro_mcp`（`--ida-rpc http://127.0.0.1:13337`）を追加した。現在は通常の
MCP namespaceとしてロード済み。

**F-139 動的照合メモ:** 会話中の `0x743768` で `R1=0x904A` → 終端 `R0=0x0A01` を採取し、
`ResFont+0x14/+0x16` のキャッシュ更新を確認した。`0x4D4EAC` では descriptor 付き glyph
record と `writer+0x44 != 0` を読み、batch 分岐と44-byte instance生成を確定した。
`0x4D5118` はこの経路では呼ばれない。4フォントの descriptor handle は5秒走行後も全て0で、
後段 submit または immediate 経路での materialize 観測が残る。

- **TODO-102** 前進 (F-139)。ResFont/TGLP/descriptor の live 値を読み取り専用で採取済み。
  17×24 font は154 sheets/stride `0x2000`/format `0x0B`、glyph descriptor は0x14 bytesで
  owner/raw/寸法/formatが静的値と一致した。全handleは0で、後段での materialize 時点は未確定。
- **TODO-103** 1 glyph の最小 native GPU draw を実装する。
  `nwfont_ResFont_GetGlyph` → `nwfont_CharWriter_EmitGlyphQuad` の値をトレースし、
  既存 `FuncNode` callback へ quad/UV/texture state を最小移植する。cache flush と
  descriptor 所有権を壊さないことを優先し、まずは一文字・一フォントに限定する。
- **TODO-104** TextBox alignment byte (`+0xFC/+0xFD`) の enum 名と、font filter/format の
  実値を動的に照合する。静的な bit mapping は F-133 に記録したが、UI enum の意味付けは未確定。
- **TODO-105** 前進 (F-139)。descriptorあり・batch (`writer+0x44`) 経路を実機で確認したが、
  5秒走行後も `descriptor+0` は全て0。lazy handle生成・bindは immediate または後段 submit
  の別経路に残るため、完了扱いにはしない。
- **TODO-106** `0x4BB278` で TextBox 描画直前の live `TextWriter`（SP）と
  `writer+0x40` context を採取する。表示済みメッセージを保持しただけでは再描画されず
  未ヒットだったため、会話を閉じて開き直す／次のメッセージへ進めて測定する。
- **TODO-107** live writer/context の採取後、`sub_4D5858`→`sub_7E7F48`→`sub_4D7730` を
  自前 `FuncNode` の同一 render pass から安全に再利用できるか検証する。最初は一 glyph・
  immediate (`writer+0x44=0`) に限定し、batch submit と atlas handle の所有権は別途確認する。
- **TODO-108** `0x4D4EAC` で捕捉した会話外 UI の writer は `+0x40==0` / `+0x44!=0` だった。
  `+0x44=0` 強制は null context 参照になるため行わない。有効な `writer+0x40` を持つ
  TextBoxまたは描画パスを特定し、そこから immediate texture setup (`0x4D5118`) を観測する。
- **TODO-109 [完了 / F-144]** TextBox vtable slot `+0x68` (`0x73CF48`) を捕捉できた。今回の実測は時計
  (`UTF-16 "00"`) だったため、会話を開いた直後に同じBPを再設置し、TextBox+0xD4 の文字列
  と `TextBox+0x104` batch bufferを会話ケースで取得する。会話側も `+0x40==0` のbatch経路
  なら、immediateではなくbatch submitを自前描画の第一候補にする。
- **TODO-91** ETC1 のバイト順を確定し、圧縮のまま自前の絵を作る（TODO-90 の代替）。
- **TODO-114 [BLOCKED / F-150]** dialogue clone のlive transform版を、次回のゲーム再起動後に
  再試行する。runtime Pane pointerをtraceで再取得・vtable/name検証すること。停止中に同じ
  code caveを改版するとARM I-cacheが旧命令を実行し得るため、修正反映にはタイトル再起動
  （または実証済みのI-cache flush経路）が必須。現在は全hook/caveをstock/zeroへ復元済み。
- **TODO-115 [次回検証]** native `0x73CF48` のR2 descriptorはF-151で `0x330A605C` と確定した。
  `TextBox_Draw` wrapperはF-152、emitter直呼びはF-154で不可と確定。次はnative submit descriptor
  をprivate copyし、`TextBatch_CopyToCommandBuffer(a1=clone descriptor,a2=cursor,a3=0)`のみを呼ぶ
  最小実験を設計する。本文/影/名前を一度に戻さない。F-155aでdescriptor recorder初版は
  cave内 `0x01E81A54` で例外（R0連鎖読取り）となり、値は未取得。修正版のgenerator auditは通るが、
  `ALLOW_TRACE_INSTALL=False` のまま。次回は**タイトル再起動後**に修正版を独立監査してから
  observerだけを1回実行し、読出し直後にuninstallする。初版例外からのstock入口復帰は成功し、
  ユーザーがゲームの正常動作を確認済み。現在のdebugger stateは次エージェントが再取得する。
- **TODO-116 [完了 / F-153]** direct-emitter patchの生成値をゲーム書込みなしで監査する
  `MODE=audit` を追加。適用前に必ず実行し、失敗すれば適用しない。
- **TODO-88** 行列を自前で組む。`0x2C1` の 3×4（`w,z,y,x` 順）を任意の位置・大きさに。
  ワールド座標との対応を掴めば任意の場所に置ける。
- **TODO-89** インスタンスブロック 144B を並べて複数描く。
  頂点/インデックスを差し替えれば任意形状。
- **TODO-85** 影はテクスチャ投影で描かれている (F-121)。
  参照しているテクスチャの実体と、ラップモード（REPEAT）の設定箇所を特定する。
  自前でテクスチャを描くときの最短経路になる。
- **TODO-86** uniform c25-c27 の 3x4 行列が何から作られるか。
  `BsShadowViewMgr_BuildShadowCmds` の低速経路（`sub_135C28` / `sub_28F0DC`）を読む。
  自前で行列を組んで任意の位置に描くために必要。
- **TODO-82** 影の TexEnv combiner を読み、なぜ定数色の RGB が効かないのかを確定する
  (F-118)。自前描画で色を出すときに必要になる。
- **TODO-72** `Base` オブジェクトのリスト（`mgr+0xD014`）を実機で走査し、
  何個いるか・どのクラスかを列挙する。自前オブジェクトを足す余地の確認。
- **TODO-67** `sub_48E384`(`0x48E384`, 0x19D8 バイト) — `SceneContext` の生成側。
  15 本の配列それぞれの容量と用途がここで決まっているはず。
- **TODO-56** `dword_94CA48`（描画コンテキスト）の実体を特定する (F-106)。
- **TODO-57** `sub_48D26C`(`0x48D26C`) — メッシュ提出。`nw::gfx` 領域 (F-106)。
- ~~**TODO-58**~~ 概念的に解決 (F-108)。`Scene_DrawLayers` の `i` は
  `ModelInstance_SetRenderLayer`(F-92) の「レンダーレイヤー」と同じ。具体値の対応は未確認。
- ~~**TODO-61**~~ 完了 (F-113)。`a1` の `1024` / `1040` は
  **フレーム内の 2 つの描画パスを区別するタグ**。`Frame_DrawPass1024`(`0x1B71C4`) と
  `Frame_DrawPass1040`(`0x1B72E4`) がリテラルで渡す。
  `1024` のパスだけが `Scene_DrawLayers` とコマンド提出を行う。`1025` は現れない。
- **TODO-52** `sub_4EEDD8` の `a1`（1024 / 1025 / 1040 …）と画面・ターゲットの対応 (F-104)。
- ~~**TODO-53**~~ 完了。CLAUDE.md の「breakpoint の扱い」をユーザーの実機検証に基づき全面改訂。
- ~~**TODO-54**~~ 完了 (F-110)。`Use stepping support` を OFF にしても
  **ヒットした bp の削除は依然として必要**。実機の対照実験で確定。
  フリーズの正体は「bp 位置での永久停止」だった。CLAUDE.md 訂正済み。
- ~~**MCP 側 Suspend の検証**~~ 完了 (F-105)。両 API とも有効。CLAUDE.md 訂正済み。

---

## ~~TODO-135: シーケンスを「曲・効果音」として合成する~~ — **効果音は完了**（F-243 / F-244）

**達成。** BGM を除く seq 型 2,839 件を WAV 化（`SOUND/out/seq_wav/`、100.2 分）。
CSEQ 命令表はラベル境界一致 **100.00%**。残りは `SEQ_BGM_*` 595 曲（同じ仕組みで出せる）と、
包絡の時定数の精密化。以下は着手時のメモ。

F-242 で素材は全部揃った。残るのは **CSEQ のバイトコードを解釈して、
CBNK の楽器定義と CWAR の波形で合成する**こと。

これができると 2 つ手に入る:

1. `SEQ_BGM_*` 595 曲と、内蔵シーケンスの効果音を音として書き出せる
2. **1 効果音 ↔ 1 波形の対応が確定する**（現状は bank 経由の候補集合どまり）

### 分かっていること

- CSEQ = `0x5000 DATA`（バイトコード）+ `0x5001 LABL`（名前 + オフセット）
- sound の開始位置は `SOUND/index/sounds.csv` の `seq_offset`（DATA 先頭からのバイト）
- `0xFE` + u16 = AllocateTrack（トラックのビットマスク、3 バイト）。
  BCSAR の `seq_offset` はこれを**読み飛ばした後**を指す（F-242 で 449 件から確定）
- 観測されたシーケンス先頭バイト: `0x80` `0x81` `0x88` `0x89` `0x8A` `0xA0` `0xA1`
  `0xB1` `0xB4` `0xB6` `0xC0` `0xC1` `0xC3` `0xC7` `0xCA` `0xCC` `0xCD` `0xD0` `0xD1`
  `0xD3` `0xD4` `0xE1` `0xF0` `0xFF`（`0xFF` は終端）
- CBNK INFO は `{u32 count, {u32 warcItemId, u32 waveIndexInWarc}[count]}` の波形スロット表を持ち、
  楽器エントリ（`0x5900`）はそのスロット番号を持つ（実測: bank 335 が 0/1、bank 405 が 4/5）

### 進め方

1. まず**楽器エントリ（`0x5900`）の全フィールド**を確定する。
   スロット番号の位置は掴めているが、キー範囲・エンベロープ・ルート音は未確定。
   1 波形しか持たないバンク（多数ある）を使えば当たりを取りやすい。
2. 次にバイトコードを**逆アセンブルだけ**する（音にしない）。
   `SOUND/index/sequences.csv` の 33,344 ラベルが正解データになる。
   ラベル位置から次のラベルまでを 1 シーケンスとして、命令長が矛盾なく埋まるかで検証できる。
3. 合成は最後。プログラム番号 → スロット → 波形が引ければ、
   単発の効果音は「その波形をピッチ変更して鳴らすだけ」で足りることが多い。

**注意:** 5 件（`SE_SYS_WIN_SELECT_ITEM_CLOSE` / `SE_OBJ_FISH_STRUGGLE_HAND` /
`SE_IND_SICK_CLOSE` / `SE_FUR_DARU_MATORYOSIKA_OPEN` / `SE_FUR_DARU_MATORYOSIKA_CLOSE`）は
自分と同名のラベルとは別のシーケンスを鳴らす。ラベル名を信じて対応付けないこと。

## TODO-136: `Game_PlaySound` の即値を洗い出して名前を付ける

F-242 で「音 ID → 名前」の逆引き表 (`SOUND/index/sounds.csv`) が手に入った。
`Game_PlaySound` / `Actor_PlaySound` の呼び出し元を静的 IDB で全部洗い、
即値を名前に解決して IDB へコメントとして入れると、機能の入口探しが大幅に速くなる。

`0x1000000` 以上の即値を見たら音 ID を疑う。`Sound_Play` は `0x2504FC` 経由（F 既出）。

## TODO-137: tie 中のベロシティ更新の食い違い（F-249）

`SE_ACT_FOOT_ERASE` の実機録音は音符の境目でくっきり段差を持ち、ベロシティ
70/60/56 の 2 乗比と 0.3dB 以内で一致する。**データ上は実機が tie 中もベロシティを
効き直しているように見える**が、聴感では効き直さない側が選ばれた
（`SE_SYS_WIN_TEXT_OPEN` は tie 中にベロシティが 100→127 と上がり、
効き直すと途中で音が膨らむ）。

切替: `render.VEL_PER_NOTE` / `render.VEL_DOWN_ONLY`。
決着させるには **ノイズ床の低い実機録音**（特に `WIN_TEXT_OPEN`）が要る。
現在の `out/open.wav` は末尾が -13.9dB で基準に使えない。

## TODO-138: `0xBC`-`0xBF` の第 2 引数の解釈（F-250）

varint(128〜142) か BE s16(-32512〜) か。全 3,494 箇所で先頭バイトが 0x80 以上のため
長さが同じで、`cseq.fit()` では区別できない。決めるにはゲーム側のコードで
シーケンス変数 1 に何を入れているかを追う必要がある（静的 IDB）。
現状は「未設定なら判定を変えない」で回避しており、音の書き出しには支障がない。

## TODO-139: `SE_SYS_AMIIBO_CAMERA_LIGHT_NORMAL` の止め方（F-251）

`note [80, 0]`（長さ 0 = ノートオフ無し）＋ 1.9ms の単一波形ループ ＋ `sustain=127` で
鳴り止まない。利用者はこの音をゲーム内で聞いたことがなく、正解が分からない。
`SOUND/out/compare35/` に hold / oneshot / fade0.4 / fade1.0 の 4 版がある。
切替は `render.NOFF_LOOP` と `render.NOFF_FADE`。
同じ形が 151 件あり、蝉（実機一致確認済み）は `hold` が正しいので既定は `hold`。

## 2026-09-04 追加（F-267 以降）

- [ ] `sub_4D5D1C`（Drawer の既定コマンド列の構築）を読む。
      `DrawBegin1` の既定 TEV で LA4 アトラス × 頂点カラーが合成されるかを決める。
      → マテリアルの控え（`MATCMD`）が要るかどうかがここで決まる
- [ ] `drawer+0x28`（uniform index）と `drawer+0x78..0x84`（c4）を誰が入れるか
- [ ] `SET_PROJECTION`（記録内の `SetDisplaySize`）を落とせるか静的に判断する
- [ ] `build_v` / `build_pass` / `build_t` も `Asm` 経由に揃える
      （監査のリテラル境界が推定に落ちている 4 本）

## 2026-09-04 追加（F-277 以降）

- [ ] `drawer+0x78..0x84`（投影 uniform の c4）の中身を特定する
- [ ] 上画面のレイアウト矩形を 400 幅としてよいかの裏取り
      （現状は各パスの `SetDisplaySize(400,240)` と揃えただけ）
- [ ] `build_v` / `build_pass` / `build_t` を `Asm` 経由に揃える
      （`verify_literals.py` / 監査が「Asm 由来でない」と報告する 4 本）
- [ ] 死語リテラル `TABP` を削除する（`TEXBLK` は `RESTORE_TEX` 用なので残す）

## 2026-09-04 追加（F-280 以降）

- [ ] プラグイン側で `GuiFontAtlas128.h` を使うよう `OwnGui.cpp` を更新する
      （確保バッファへ 16384 バイトを書く。**確保サイズが 0x4000 あるか要確認**）
- [ ] メニューの選択行を CPU から書き換える経路（表を作り直して `.bss` へ書くだけ）
- [ ] 文字サイズを 14px のままにするか 16px（8 の整数倍）にするか、実機で見て決める

---

# ★2026-09-04 — TODO-134 の「描画基盤」は完了（F-281）

実機で上下画面とも常時・最前面・非破壊で描けることを確認した。
利用者確認: 「全てあなたの想定通りに出ています」。

## 完了

- [x] 上画面に描く / 下画面に描く / 上下の描き分け
- [x] 常に最前面（優先度 `0xFF`）
- [x] 常時表示（ロード・メニュー・フェードで消えない）
- [x] ゲームを止めない
- [x] 座標系の確定（1 単位 = 1px、原点は画面中央）
- [x] ASCII フォント（128x128 LA4、61 文字）
- [x] メニューのレイアウト（枠・タイトル帯・カーソル・6 項目）
- [x] 拡大率の整数倍化（線幅の不揃いを解消）

## 次にやること（チートメニューの機能面）

- [ ] **入力**: Select で開閉、Select + 上 で従来の CTRPF メニュー。
      十字キーで行移動、A で決定。CTRPF プラグイン側に置く
- [ ] **開閉**: 閉じているときは表を空（チャンク 0）にするだけでよい。
      `update_tables.py` と同じ要領で `.bss` を書き換える
- [ ] **選択行の反映**: `MENU_SEL` を変えて表を作り直すだけ。ケーブは触らない
- [ ] **各項目の実装**（歩行速度・時間停止など）。既存のチートコード資産を使う
- [ ] `LIST_SIZE` を `0x4000` から上げる（項目を増やすときに必要。1 枚約 127 バイト）
- [ ] プラグインへの移植（`OwnGui.cpp` を `GuiFontAtlas128.h` に合わせる。
      確保サイズ 0x4000 を確認済み）

## 積み残し（優先度低）

- [ ] 主リストの消費量と毎フレーム記録の CPU コストを実測する
- [ ] `build_v` / `build_pass` / `build_t` を `Asm` 経由に揃える
      （`verify_literals.py` が生の語列としても検査するので実害は無い）

## 2026-09-04 追加（F-282。プラグイン移植）

- [x] `GuiCaves.h` の自動生成（`PATCHES/export_gui.py`）
- [x] `GuiRender` / `OwnGui` / `GuiMenu` の書き直し
- [x] ビルドせずに移植を照合する道具（`PATCHES/verify_plugin_port.py`）
- [x] ビルド（警告 0 件）
- [ ] **実機で試す。** 手順は次のとおり
      1. 実機に入っている 1 つ前の版を `MODE="uninstall"` で外す
         （下画面メニュー・`LIST_SIZE 0x4000` の版が入っている）
      2. 新しい `.3gx` を `/luma/plugins/00086200/` へ置く
      3. CTRPF メニューの「自前 GUI を組み込む」を ON
      4. Select で開閉、Select + 十字上 で従来メニュー、十字上下で行移動
- [ ] 開閉の動作確認（閉じたときに絵が消えるか。F-282 の不備 2 の検証）
- [ ] アニメーション・スクロール・日本語フォント・値項目（シミュレータの残り）

## 2026-09-04 追加（F-283。シミュレータ相当の UI）

- [x] 十字キーの連続入力（200ms / 60ms）とスライドパッドの無効化
- [x] 美咲ゴシック第2 8px（グリフを実行時にアトラスへ焼く）
- [x] 登場・退場／選択追従／明滅／跳ね返りのアニメーション
- [x] 項目型（フォルダ・チェック・アクション・10進・16進・小数・スライダー・リスト）
- [x] 未適用の黄色表示・X で適用・L で全戻し・閉じる確認
- [x] 説明とホットキーの常時表示
- [x] 通知（チェックボックスの適用が変わったときだけ）
- [ ] **実機で試す**（先に 1 つ前の版を外すこと）
- [ ] リストボックスの画面表示（いまはインラインで左右切り替え）
- [ ] ホットキーの入力待ちウィンドウ（いまは Y で候補を回す）
- [ ] PixelMplus10 の数字（いまは数値も美咲）
- [ ] 自前キーボード（利用者の指示により保留）

## 2026-09-04 追加（F-284。実機クラッシュの原因追及）★次はここから

**現象**: 「自前 GUI を組み込む」を ON → Select で開くと真っ黒の GUI →
直後開けなくなる → Select で開閉を試している最中にクラッシュ（`PC=0x839004`）。

**確定**: `PC=0x839004` は `.text` のゼロ埋めを NOP スライドして `.rodata` へ
飛び出した結果（F-284）。`LR=0x1B7294` から **`BL RenderTop` 以降 `BL` が 1 本も
実行されていない**＝ `0x566DF8` の分岐先（`0x838950`）が既にゼロだった。
組み込みログ（`/CTRPF_OwnGui.txt`）は正常なので **`LIST_SIZE` 説は否定**。

- [ ] **`Enable()` に `if (g_enabled) return true;` を入れる**（二重組み込みで即死する）
- [ ] **`InstallHooks()` 失敗時のクリーンアップからケーブのゼロ埋めを外す**
      （フックが生きたままケーブを消すのが最有力の死因）
- [ ] `Disable()` を Pause 中でも安全にする。`Process::Patch` の戻り値を検査し、
      **ゲームが実際に数フレーム進んだこと**を確かめてからゼロ埋めする
- [ ] CTRPF 本体で `MenuEntry` コールバックが Pause 中に走るのかを確認する
- [ ] 「真っ黒（文字が出ない）」の机上検証 —
      矩形だけでチャンク上限 64／枚数上限 460 を食い潰していないかを
      `preview_layout.py` / `verify_plugin_port.py` を F-283 へ更新して数える
- [ ] 「直後開けなくなり」— `GuiMenu::Close()` の `AnyDirty()` が初期状態で真に
      なっていないか（`vi/ai`・`vf/af`・`hotkey/ahotkey` の初期値ずれ）を確認
- [ ] ケーブ全数の逆アセンブル検証（`0x836700` へ平行移動。F-284 の注意書き参照）

## 2026-09-04 追加（F-286。F-282 へ巻き戻した）

- [x] F-283 / F-285 を `BACKUP/f283_f285_20260904/` へ退避
- [x] `cave_node_record.py` の容量・`.bss`・`LIST_SIZE` を F-282 へ差し戻し
- [x] `GuiCaves.h` 再生成（下 38 枚 / 上 134 枚 / 色 24 / LIST 0x8000）
- [x] `GuiRender.cpp` / `GuiMenu.cpp` を F-282 版へ書き直し（焼き込みアトラス・アニメ無し）
- [x] `OwnGui.cpp` の取り外し順序を修正（`LOG+0xE8` を**フックを外す前に**見る）
- [x] 検証 5 本（照合・監査・リテラル・プレビュー・成果物）＋ビルド
- [ ] **実機で描画を確認する**（★先に F-285 の版を外して本体を再起動すること）
- [ ] F-285 の「文字が板」「明滅」が消えたことを確認（消えるまで原因を断定しない）
- [ ] F-284 の「誰がケーブをゼロにしたか」は未確定のまま。F-282 では再発しない構造だが原因未特定
- [ ] F-283 の要素（美咲フォント・アニメ・項目型）を**1 つずつ**入れ直す

## 2026-09-04 追加（F-287。明滅の真因）

- [x] 記録されたコマンド列を直読みし、先頭 144 バイトがリングのゴミだと確定
- [x] `RING`(0x200) と `MATCMD` の重なりを解消（`0x9B5800` / `0x9B5A00`）
- [x] `_check_layout()` の RING を `0x80` → `0x200` に是正（再発防止）
- [x] `OwnGui.cpp` の `ZeroBss(kGuiRing, ...)` も `0x200` へ
- [x] 再生成・検証 3 本・ビルド
- [x] 実機の生きているプロセスへ最小修正（リテラル 1 語 + TEV 書き戻し）
- [ ] **利用者に再開してもらい、明滅と「板」が消えたかを確認する**
- [ ] 消えたら新しい `.3gx` を入れ直して同じ結果になることを確認
- [ ] `.bss` の各領域の大きさを **1 箇所から生成**するよう作り直す（同じ事故の再発防止）

## 2026-09-04 追加（F-287 確定・基準版の固定）

- [x] 実機で復旧を確認（利用者「直りました」）
- [x] `BASELINE/gui_render_ok_f287/` へ基準版を保存（21 ファイル + SHA-256 + README）
- [x] `PATCHES/verify_baseline.py`（差分検出 / `--restore`）
- [x] `CLAUDE.md` に索引と教訓 2 件を追加
- [ ] `.bss` の各領域の大きさを **1 箇所から生成**する形に作り直す（F-287 の再発防止）
- [ ] F-283 の要素を **1 つずつ**入れ直す（美咲フォント → アニメ → 項目型）。
      1 要素ごとに検査 7 本 + 実機確認。壊れたら `verify_baseline.py --restore` で戻す

## 2026-09-04 追加（F-288。画面キャプチャ）

- [x] Chokistream の画面ウィンドウを AI が読めることを確認
- [x] `PATCHES/grab_screen.ps1`（上下切り出し・連写・画素差 %）
- [ ] 次に描画を試すときは **適用前後を連写して差分で確かめる**（利用者に聞く前に自分で見る）

## 2026-09-04 追加（F-289。Picture 描画関数の最小実験）

- [x] 実物の Picture を捕獲し、構造（幅/高さ/行列/UV/材質埋め込み）を実測
- [x] 複製した自前 Picture で `nwlyt_Picture_DrawToCommandList` を呼び、**1 枚描けた**
- [x] 位置・大きさが自前の値で効くことを 3 通りで確認
- [x] 片付け（フック復元・ケーブとクローンをゼロ埋め・自前 GUI 無傷を確認）
- [ ] **`Material_EmitState`(0x4B7864) を逆コンパイルし、マテリアル内オフセット →
      PICA レジスタ（0x082/0x083/0x085/0x08E）の対応表を作る**
- [ ] 自前アトラスを正しく貼れることを確認（いまは番地は効くが書式が合わない）
- [ ] `+0x254` 系の外部参照が実際に読まれるかを確認（読まれないなら寿命問題は無い）
- [ ] 通ったら CAVE_Q のスプライトループをこの関数呼び出しへ置き換える設計を書く

## 2026-09-04 追加（F-289 段 2 の続き）

- [x] `TextBox_UpdateDrawState`(0x4B7DEC) から記述子 → PICA レジスタの対応表を確定
- [x] `unk_97B74C` の実測ヘッダで裏取り（ユニット0 = 082/085/08E/083）
- [x] **自前アトラスを貼って実機で確認**（文字がそのまま出た）
- [ ] マテリアルの色の欄（`+16` / `+20` / `+48 & 3`）で**色を自前で決められる**ことを確認
      ★状態キャッシュ `0x97B6FC` / `0x97B714` / `0x97B72C` を潰すこと（F-157）
- [ ] `+0x254` 系の外部参照が読まれないことを確認（読まれないなら完全に自前で持てる）
- [ ] CAVE_Q のスプライトループを Picture の呼び出しへ置き換える設計を書く

## 2026-09-04 追加（F-289 段 3）

- [x] 色の欄を特定（`*(mat+48)&3` で分岐、モード1 は `*(mat+16)`→0x0DB / `*(mat+20)`→0x0F3）
- [x] **実機で色を変えられることを確認**（`0xFF0000FF` で赤。書式は `0xAABBGGRR`）
- [x] **外部参照 5 語を 0 にしても描画継続**＋12 秒の走行に耐えることを確認
      （★「場面変化に耐えた」と書いていたが根拠が無かった。場面変化は未検証）
- [ ] **世代依存の原因を潰す**。`sub_73B650` を読み `*(pic+212)`/`*(pic+216)`/`*(mat+77)` を確定
      → 自前 Picture を**最初から組み立てられる**ようにする（複製に頼らない）
- [ ] 借り物 TEV の合成を確認し、**文字だけ色を付けられるか**を判定
      （できないなら自前 TEV を併用する設計にする）
- [ ] Picture を N 個並べ、CAVE_Q のスプライトループを置き換える設計を書く

## 2026-09-04 追加（F-289 段 4）

- [x] `sub_73B650` を読み、UV キャッシュ（`*(pic+212)` / `*(mat+77)` bit2 / `*(pic+216)`）を特定
- [x] テクスチャ記述子の全欄を確定（`+0x08`/`+0x0C` が UV 倍率。段 1 の記述を訂正）
- [x] **UV 再計算を強制して 15 秒の走行に耐えることを実機で確認**
      （★「場面変化」は未検証。放置では場面は変わらない）
- [ ] 借り物 TEV の合成を確認し、**文字だけ色を付けられるか**を判定
      （いまはアルファ 0 の画素まで不透明になる）
- [ ] Picture を使い回す設計（1 枚ごとに 0x320 バイト持つのは重い。
      行列・幅・高さ・UV・色だけ差し替える）
- [ ] 呼ぶ場所を**自前ノードの記録内**へ移す設計（いまはゲームの呼び出しの前に割り込み）

## 2026-09-04 追加（F-289 段 5）

- [x] 判定をフレーム基準にして、元の Picture に依存しない形にした
- [x] **ロードを跨いでクローンが生き残ることを実測**（外部参照を全部 0 にした状態で）
- [x] 見えない原因を特定 = **乗り込む位置**（下画面の全画面背景の直前に割り込んでいた）
- [ ] **`Picture_DrawToCommandList` の呼び出しを CAVE_Q（自前ノードの記録）へ移す**
      - 自前ノードは優先度 0xFF なので順序を自分で握れる
      - Picture は 1 個を使い回し、行列・幅・高さ・UV・色だけ差し替える
- [ ] 借り物 TEV の合成（アルファ 0 の画素まで不透明になる件）

## 2026-09-05 追加（F-290。CAVE_Q の Picture 呼び置換）

- [x] `build_q` のスプライトループを `Picture_DrawToCommandList` 呼びへ置換（`Q_PICTURE_CALL`）
- [x] 再利用 Picture 雛形 `PIC = 0x9B6000`（0x400）と packed 色配列 `0x9B6400` / `0x9B6460`
- [x] マテリアル消失ガード（`LOG+0x08`。実測 0 発火 / 記録 4823 回）
- [x] 実機で 3 矩形 → 全メニューまで表示成功（前エージェント）
- [x] **Picture 経路の座標系を実測で確定**＝手書き経路と同一（F-290）
- [ ] **H-1: チャンク 0 の残像を直す**（判定を StartSave のあとへ。F-256 のガードは残す）
- [ ] 雛形生成に**単位行列の明示**を入れる（いまの雛形はたまたま無回転）
- [ ] Phase 2: 文字（UV 切り出し）。借り物 TEV のアルファ 0 不透明化の判定が先
- [ ] 観測用ケーブ P/V/M/B/U を本番前に外す
- [ ] プラグインへの移植（Phase 1 が固まってから）

## 2026-09-05 追加（H-1 修正と監査器の欠陥）

- [x] **H-1（チャンク 0 の残像）を修正**（判定を StartSave のあと・`endrec` へ）。実機 A/B/C で確認
- [x] **`audit_node_cave.py` の既定対象が旧ファイルだった欠陥を修正**（+ `PIC_FN` を許容）
- [ ] 雛形の単位行列を明示的に焼く
- [ ] Phase 2: 文字（UV 切り出し）。借り物 TEV のアルファ 0 不透明化の判定が先
- [ ] 観測用ケーブ P/V/M/B/U を本番前に外す
- [ ] プラグインへの移植

## 2026-09-05 追加（F-291。nw::lyt の静的解明）

- [x] RTTI で `nw::lyt::Picture` / `Pane` / `Material` と確定。継承も確定
- [x] ペイン工場から **Picture = 344 バイト**を確定（文書の「約 0x320」を訂正）
- [x] Pane / Picture / Material / TexMap の全フィールドを ctor と取得子から確定
- [x] TexMap の `+0x14/+0x18/+0x1C` が**派生キャッシュ**であることを確定（`sub_4B9830`）
- [x] アンカーの旧 IDB コメントの誤り（縦 1 の分岐落ち）を訂正
- [x] IDB へコメント反映・保存
- [ ] **雛形を「捕獲して複製」から「必要な欄だけ組み立てる」へ作り直す**
      （Picture 344B + Material 80B + 可変長ブロックを自前で用意する）
- [ ] TexMap は `+0x04/+0x08..+0x0E/+0x10` を書いて `sub_4B9830` を呼ぶ形にする
- [ ] 雛形の `+0xB6` 下位ニブル = 4（中央揃え）を明示する
- [ ] TexMap `+0x00` の意味、`sub_73D0C8` の戻り（tevStage か alphaCompare か）を詰める

## 2026-09-05 追加（F-292。正規の手順）

- [x] F-291 の結論を別関数 7 系統で再検証 → **矛盾 0**
- [x] 本物の `ssys::ma::lyt::Layout` vtable を特定し、自前 vtable と一致することを確認
- [x] `Layout_RecordPaneTree` / `DrawPaneTreeToCurrentList` / `Pane_DrawRecursive` を読み切り、
      **レイアウトに必要な欄が 10 個ほどしかない**ことを確定
- [ ] **段 1: Picture を「捕獲複製」から「組み立て」へ**（344 バイトを自前で埋める）
- [ ] **段 2: root Pane を 1 個組み、Picture を子に繋ぐ**
- [ ] **段 3: vtable +0x14 を `0x5686D4` へ差し替え、CAVE_Q(205 語)を撤去**
- [ ] 段 4: N 枚へ拡張 / 段 5: A1・A2 の縮小を検討
- [ ] DrawInfo（`+0x30` 以降）の中身を詰める（TextBox を使うなら必須）

## 2026-09-05 追加（F-292 の実機検証）

- [x] **実機のレイアウト・Pane 木・Material・TexMap で静的結論を全数検証 → 矛盾ゼロ**
- [x] `ROR32(+0x0C,16) = +0x18` と 書式表`[2]=9` を**触っていない実データ**で確認
- [x] 実物が派生 `6Layout` であること、`+0x18` を上書きしていることを把握
- [x] Material の位置は規則的（常に +416）と訂正
- [ ] **段 1: Picture を「組み立て」へ**（344 バイト。basePosition は 0x14 を明示）
- [ ] 段 2: root Pane を組み、Picture を子に繋ぐ
- [ ] 段 3: vtable +0x14 を `0x5686D4` へ差し替え、CAVE_Q(205 語)を撤去

## 2026-09-05 追加（F-293。正規経路で描画成功）

- [x] **`.bss` に nw::lyt のオブジェクトを自前で組み、ゲームの `Layout_RecordPaneTree` に描かせた**
- [x] **CAVE_Q(205 語) を撤去**。前エージェントの残骸（下画面の白帯）も解消
- [x] 位置が画素単位で一致することを実測
- [x] **色は頂点カラー `+0x140` で 1 枚ずつ変えられる**（F-280 の制約が消滅）
- [ ] 文字を Picture N 枚で並べる。**1 枚ごとにオブジェクトが要る**（木を歩くのはゲーム側）
- [ ] `.bss` の確保計画（Picture は詰めれば 1 枚 0x160 程度）。上画面 119 枚で約 42KB
- [ ] A1 / A2 を縮める（投影の直接呼び出しは vtable +0x18 に任せられる）
- [ ] プラグインへの移植
- [ ] `mat+0x4D` bit1 の意味を詰める（立てると描画が止まる）

## 2026-09-05 追加（F-294。自前フォント）

- [x] 利用者が実機でロード・操作を跨いで正常動作を確認（F-293 追記）
- [x] `nw::font::Font` が抽象インタフェース（24 純粋仮想）＝**自前フォントが可能**と確定
- [x] `Glyph` 構造を `nwfont_ResFont_GetGlyph` から確定（テクスチャ番地 / セル UV / 幅 / 書式）
- [ ] **方針をどちらかに決める**
      (a) Picture 方式のまま。容量はゲームのアロケータから借りて解決（追加コード 0 語）
      (b) TextBox ＋ 自前 Font。容量 6.6 倍節約だが stub 60〜90 語が要る
- [ ] (b) なら: 自前 Font の vtable 27 語 ＋ 取得子 stub ＋ `GetGlyph` の実装
- [ ] (b) なら: セル座標の +1 余白（`(セル幅+1)×列+1`）をアトラス側か GetGlyph 側で吸収
- [ ] TextBox のフォント欄は `+0x100`。`+0xFA` 文字数 / `+0xE0` / `+0x104` も要調査

## 2026-09-05 追加（F-295。方式 a 完成）

- [x] `nw::lyt` のアロケータ（`sub_4B8CF0`）から **64KB を借りられた**
- [x] **F-221 の訂正**: 0x4000 上限は g_GfxAllocator のヒープの性質。Alloc 関数の制限ではない
- [x] 共有 Material + 共有 texMap + Picture[N] の配置で **メニュー全体 74 枚を描画**
- [x] 一括転送（bytearray → 0x1000 ずつ）で書き込み時間切れを解消
- [ ] 借りた領域を返す手段（アロケータ vtable +0x0C）
- [ ] 下画面の木（いまは空）
- [ ] 枚数の見積り: 64KB で 185 枚。日本語を入れるなら増やすか方式 b（TextBox）へ
- [ ] **プラグインへの移植**（確保も組み立ても C++ から直接できる）

## 2026-09-05 追加（F-296。借りた領域を返す）

- [x] **アロケータ vtable +0x0C = `ssys::ma::Allocator::Free` `0x00569B44` を特定**
- [x] `Alloc` / `Free` が対称（ヘッダ無し）であることを静的に確認
- [x] `alloc_lyt_heap.py MODE="free"` を実装（17 語、事前監査つき）
- [x] `build_pane_tree.py MODE="detach"`（描画だけ止める。vtable は触らない）
- [x] **実機で 確保 → 解放 → 再確保 → 組み直し の往復を成立させた**
      解放後に同一番地が返る＝空きリストへ戻った裏取り

### 次にやること

- [x] **下画面のペインツリーを組む**（F-297。上 74 枚 / 下 110 枚が独立した輪で同時描画）
- [x] **容量**: F-296 の解放機構で `0x10000` → `0x20000` へ借り直した（371 枚ぶん）
- [ ] **日本語**: ASCII 61 文字のアトラスでは足りない。
      方式 (b)（`TextBox` + 自前 `nw::font::Font`）か、アトラスの多面化へ
- [ ] **プラグインへ移植**。同一プロセスなので確保も構築も解放も C++ で直接書ける
      （`0x004B8CF0` / `0x00569B44` / `*(u32*)0x0096F150`）。ケーブは不要
- [ ] 観測用ケーブ P / V / M / B / U を本番前に撤去する
- [ ] `mat+0x4D` の bit1（立てると描かれなくなる）と `DrawInfo`（+0x30）の
      投影行列より後ろの中身を詰める

## 2026-09-05 追加（基準仕様 v2）

- [x] `BASELINE/gui_spec_v2/README.md` を制定（**探索では書き換えない**）
- [x] `DrawSelf` の呼び出し規約を静的に確定（`0x73B524`）
- [x] Picture のバッチ遅延と `DrawCtx_FlushBatch(drawctx, cursor)` を静的に確定

### 次にやること — 文字を従来方式へ移す（`CAVE_TXT`）

- [ ] スプライト表の生成を `build_pane_tree.py` に足す（**表はヒープに置く**。`.bss` に出さない）
      同じ色の文字を 7 枚チャンクに詰め、端数は空き枠で埋める
- [ ] `CAVE_TXT` を書く。v1 の CAVE_Q から
      **SelectList / Clear / StartSave / DrawBegin1 / DrawEnd1 / Commit を全部落とす**
      （記録サイクルはゲームがやる）。残すのは TEV + テクスチャ結び付け + スプライトループ
- [ ] 冒頭で `drawctx[36] != 0` なら `DrawCtx_FlushBatch(drawctx, cursor)` を呼ぶ
- [ ] 自前テキスト Pane を root の**子リストの最後**に繋ぐ（vtable スロット 26 = `CAVE_TXT`）
- [ ] `audit_node_cave.py` と `verify_literals.py` を通してから実機へ
- [ ] 通ったら仕様書 7 節の実測値と 8 節の実装状況を更新する

## 2026-09-06 方式比較の現在地

- [x] 最新の到達点F-302と基準仕様v2の未実装CAVE_TXTを区別。F-299の容量式を静的IDBと実装で照合。
- [x] TextBoxのバッチ再利用分岐を確認。容量からCPU/GPUの速さを断定しない。
- [x] 実機の既知GUIフックが素、管理スロットがゼロであることを確認。STATE先頭を更新。
- [ ] 速度で方式を選ぶ場合、同一の自前アトラス・文字列・色・寸法で比較する。
      文字変更時と変更なし時を分け、記録生成時間、記録長、描画回数、GPU時間を測定する。
      本セッションは方式比較の回答までで、実装や適用は行っていない。

## 2026-09-06 TextWriter実装（ユーザー選択済み・途中で中断指示）

**次回は `HANDOFF_TEXTWRITER.md`。再度方式選択を質問せずTextWriterで進める。**

- [x] 独立Pane＋TextWriter/標準バッチの経路を静的に調査。
- [x] Init/Reset/DrawString/Build/提出prefix/提出/suffixの引数を標準TextBox経路のassemblyと照合。
- [x] ResFontの取得子とCMAP/GetGlyph、writer座標処理を確認し証拠JSONへ保存。
- [ ] 自前行列・writer座標の最小1文字設計を詰める（baselineとY反転を二重適用しない）。
- [ ] 専用の実装・フォント生成・監査スクリプトを作る。新しいコードはまだ無い。
- [ ] 領域の使用状況と重なりを確認し、確保・読戻し・全LDR/分岐/リテラル値の監査。
- [ ] 片画面1文字→複数字→上下の順に実機描画、画面/バッチ/記録列で検証。
- [ ] 文字変更時の再構築と変更なし時の再利用、取り外しを検証。

実機は書込み・Resumeなしで停止中。ユーザーがリミット対策として中断を指示したため、この先は未実施。

## 2026-09-06 追加（F-303。自前フォント）

- [x] 借りた nw::lyt ヒープが GPU 可視であることを実機で確認（アトラス専用確保が不要に）
- [x] 自前アトラス生成器 `make_font_nwfont.py`（nw::font の 1 画素余白・CMAP 方式 0 に対応）
- [x] 倍率と Y の式を静的に確定し、ゲームのフォントで検算
- [x] `own_font.py`（フォント資源 + TextBox をデータだけで組む）。領域の重なり検査つき
- [ ] **3DS を再起動**してから `RE/STATE.md` の手順で入れ直す
- [ ] **自前フォントで実機に描く**（まず TextBox 経路。フォントだけを変数にする）
- [ ] 描けたら **TextWriter 直呼び**へ移す。必要なのは
      DrawSelf ケーブ 1 本（Flush → Init → 各欄 → DrawString → BuildCommandStream →
      提出記述子 → CopyToCommandBuffer）。`HANDOFF_TEXTWRITER.md` に契約表がある
- [ ] 整列 0（左上基準）での座標を 1 文字で実測してから複数字・上下へ広げる
- [ ] 小文字と記号を字形表へ足す（いまは 61 字。ASCII 95 字中 34 が空セル）

## 2026-09-06 追加（F-305。自前フォント完成）

- [x] `ResFont` vtable 26 スロットの全数解析（推測ゼロ）
- [x] `FINF[0x07]` = 読み取り器の選択（必ず 1）を確定。F-304 の PC=0 の真因
- [x] `FINF[0x01]` = 行送り、CWDH は 0 でよい、倍率と Y の式を確定
- [x] 実機なしの検算 2 本（`verify_own_font.py` 8 検査 / `verify_font_deps.py` 番地照合）
- [x] **実機で自前フォント描画に成功**（コードケーブ 0 語）

### 次にやること

- [ ] **TextWriter 直呼び**へ移す。DrawSelf ケーブ 1 本:
      Flush → `sub_7E8488` → 各欄 → `sub_7E7F48` → `TextBatch_BuildCommandStream`
      → 提出記述子 → `TextBatch_CopyToCommandBuffer`
      ★ケーブを書いたら **`audit_node_cave.py` / `verify_literals.py` と
        idalib の逆アセンブルを通してから**実機へ
- [ ] 整列 0（左上基準）の座標を 1 文字で実測（いまは ALIGN=4 の中央揃え）
- [ ] 小文字と記号を字形表へ足す（いま 61 字 / ASCII 95 字中 34 が空セル）
- [ ] 上画面にも自前フォントの TextBox を置く
- [ ] 日本語は別途（自前アトラスに字形が要る。CMAP を足せば方式 0 で引ける）

## 2026-09-06 追加（F-306。TextWriter 直呼び）

- [x] ケーブが呼ぶ 9 関数の引数と副作用を静的に確定
- [x] TextWriter のひな型 25 語を全語確定（`sub_4D5B18` + `sub_7E8488`）
- [x] `.text` の空きをゼロ連続で機械測定（`0x838810` は空きではなかった）
- [x] ケーブ 75 語を実装 → 監査 → objdump → **実機のバイトを逆アセンブルして確認**
- [x] **実機で TextWriter 直呼びの描画に成功**
- [x] import 経路の `sys.exit()` を塞ぎ、`importlib.reload()` を入れた

### 次にやること

- [ ] 整列 0（左上基準）で 1 文字の座標を実測し、任意位置へ置けるようにする
- [ ] 複数行（`FINF+0x01` の行送りが効く経路）を確認する
- [ ] 文字列の差し替え（制御+0x10 に 1 を立てるだけ）が効くか実測する
- [ ] 上画面にも置く / メニューの文字を全部この経路へ移す
- [ ] 小文字と記号を字形表へ足す（いま 61 字 / ASCII 95 字中 34 が空セル）
- [ ] どちらを本採用にするか決める（F-306 G の比較表）。基準仕様 v2 の改訂はそのあと

## 2026-09-06 追加（F-308。大量文字の天井）

### ★先にやるべき（方式の決定より前）

- [ ] **`LIST_SIZE` を 0x8000 から上げる**。いま下画面は残り 9,472B ＝ 約 114 文字しか無い。
      **溢れても検査が無く静かにバッファ外を壊す**（`0x4B8364` / `0x7B0694` に境界比較なし）
- [ ] **記録長の監視を入れる**。`Layout+0x108`（記録長）を毎フレーム読み、
      `LIST_SIZE` の 8 割を超えたら描画を打ち切る安全弁。**無検査の代わりを自前で持つ**
- [x] **nw::lyt ヒープの実残量を確定させた**（F-309）。正体は **`sead::ExpHeap`**、
      `+0x1C`=先頭 / `+0x20`=総量 で解釈は**正しかった**（先頭を推測したのが誤りだった）。
      **空き 1,200,132 B (1.14 MB)、空きブロックは 1 個。** 1,200 文字の 445KB は余裕で入る。
      測り直しは `PATCHES/probe_lyt_heap.py`（読み取り専用）
- [x] **場面をまたいで最小の空きを測った**（F-310。利用者にタイトルから進める・
      住民に話しかける等をしてもらった）。**空きは 3.16MB 〜 0.61MB まで動く。**
      最悪時に配れるのは **738,876 B**、断片化で空きが 5 個に割れる場面もある。
      → **上限は 1,000 文字前後。1,200 文字は破綻するのでやめる**
- [ ] 観測間隔 1874 ms は粗く、真の最小はもっと低い可能性がある（F-310 F）。
      精度が要るなら**最小値を追うだけの毎フレーム記録ケーブ**を書く。
      いまの予算は余裕を取ってあるので急がない
- [ ] 次に測るときは `MODE="mark"` で操作の区切りを残す（今回は紐付けを取り損ねた）
      建物に入る・地図・メニュー等でゲームがレイアウトを確保する可能性がある。
      **空きブロックは 1 個しかないので取り切るとゲーム側の確保が失敗する**。
      予算はこの最小値から決めること

### 大量登録そのもの

- [ ] 1 本のバッチへ複数の `DrawString` を積む（静的には可能。`0x4D4F78` で件数が単調増加）。
      実機で 2 文字列以上・色違いを 1 バッチに入れて確認する
- [ ] バッチの最大文字数を実運用値（例 512）にして、満杯時に落ちず字が消えるだけかを実測
      （`0x4D4F6C BLS` の枝。静的には安全）

## 2026-09-06 追加（F-311。プラグインを基準仕様 v2 へ）

- [x] 3gx の名前を `gohan` に統一（`Makefile` の `TARGET`、`plgInfo`、`PluginMenu`）
- [x] v1 のファイルを `_v1_retired/` へ退避（ビルドされない。正本は BASELINE）
- [x] `export_gui_v2.py` / `export_font_nw.py` でヘッダを生成（ケーブは書き直さない）
- [x] `GuiV2.cpp`（描画本体）/ `OwnGui.cpp`（組み込み）/ `GuiMenu.cpp`（最小 GUI）
- [x] 記録コマンドリストの安全弁を実装（§4.7 / 仕様書 §8 の未実装項目）
- [x] `verify_plugin_port_v2.py` 7 群 すべて 0 件
- [x] `gohan.3gx` までビルド（警告 0）
- [x] ケーブを objdump で逆アセンブルして確認

### ★次: 実機で確かめる（**この版はまだ 1 度も実機で動かしていない**）

- [ ] SD の `/luma/plugins/00086200/` へ `gohan.3gx` を置き、Rosalina で plugin loader を ON
- [ ] メニューの「自前 GUI を組み込む」を ON
- [ ] `/gohan_owngui.txt` を読む（借用・ヒープ残量・ケーブ・フック・記録長）
- [ ] `/gohan_gui.txt` を読む（配置と重なり検査）
- [ ] 上下ノードの `list` が 0 でないこと、記録長が LIST_SIZE の 8 割未満であること
- [ ] Select で開閉、十字上下で選択が動くこと
- [ ] 文字が自前フォント（5x7）で出ること。にじみ・ずれの有無
- [ ] OFF にして記録長が 0 になり、ヒープが返り、ケーブがゼロ埋めされること
- [ ] 場面転換をまたいで落ちないこと（借用は F-310 で `freeAll` に巻き込まれないと確認済み）

### 実機で問題が出たときの切り分け

- 画面に何も出ない → 記録長 `node+0x108` が 0 か。0 なら `+0x11D`(記録要求) と `+0x20`(root)
- 文字だけ出ない → `node+0xB0`（DrawInfo+0x80 = LayoutMgr+0x1C）が入っているか
- 落ちる → `FINF+0x07` が 1 か（1 以外だと PC=0）。`/gohan_gui.txt` の重なり検査

### F-311 追記（2026-09-06）: 描画されなかった原因を修正

- [x] 真因: `InitBss()` が `GuiV2::Install()` の**あと**にあり、`node+0x20` を消していた
      （実機ログの「list は非 0 なのに記録長 0」で確定）
- [x] `Enable()` の順序を修正 + `node+0x20` の検査を組み込みに追加
- [x] `Commit()` が生きているオブジェクトを `memset` しないよう分離（`BLX 0` 予防）
- [x] 輪は `root+0x14` を最後に公開
- [x] `node+0xB0` を Install でも設定
- [x] アトラスに塗り潰しのマス（列 15/行 15）を追加し、矩形の UV をマス内側へ
- [x] `FillSlot` で TextBox の `+0xFE`(dirty) を立て直す
- [x] `verify_plugin_port_v2.py` に**群 8（順序と禁止事項）**を追加
- [ ] ★実機で再確認（ON にした直後にメニューが開いた状態で出るはず）
      - 記録長が 0 でないこと（`/gohan_owngui.txt`）
      - 矩形と文字が出ること / Select で閉じられること

### F-311 追記 2（2026-09-06）: 文字の乱れ

- [x] 原因は中央整列での半画素（ペイン高にセル高 7 を入れていた。正しくは行送り 8）
- [x] `FillSlot()` のペイン高を `kFontLinefeed` へ
- [x] 仕様書 §3.1 と検証器 2 本に条件を追加
- [ ] ★実機で字形が 7 行そろって出ることを確認（`A` が `A`、`C` が `C` に見えるか）

## 2026-09-06 追加（F-312。Simulator の本格移植）

- [x] 段 1: フォント基盤（美咲 362 字＋PixelMplus 27 字を 1 枚に。CMAP 方式 2 + CWDH）
      `PATCHES/make_font_ui.py` 検証 6 本 0 件 / `Includes/GuiFontUi.h` を生成

### 段 2 の前提（★実測は不要だった。F-313 で静的に決着）

- [x] **`LIST_SIZE` を上げられるか** → **上げられる。** `BL 0x5685A4` 129 箇所の R3 を走査し、
      ゲーム自身が `0x10000` を 3 箇所、`0x11000` を 1 箇所、**`0x18000` を 1 箇所**で使用
- [x] **記録の 1 文字あたり** → `sub_4D6CE0` の語数を式にして **約 61 B/字**。
      式（338 語）と F-308 の実測（306 語、17 字）が 10.5% 以内で一致
- [x] **1 本のバッチに複数文字列** → `sub_4D6570` が全件をマテリアルごとにまとめる設計そのもの

### 決まった構成（F-313 D。★予算は F-314 で訂正）

| | |
|---|---|
| `LIST_SIZE` | 上 `0x10000` / 下 `0x8000` |
| 借用（nw::lyt ヒープ） | `0x50000`（327,680 B）。配置は 87% |
| バッチ | 上 512 字 / 下 128 字（共有 1 本ずつ） |
| Picture | 48 枚 |
| 1 枚 / 1 字の記録量 | **Picture 204 B / 文字 82.8 B**（F-314 で取り直した） |

★**`LIST_SIZE` は nw::lyt とは別のヒープ**（`graphic::MemoryMgr` +0x14 の ExpHeap、
  総量 7,008,256 / 空き 1,220,172）から取る。予算は独立に数える。

| 予算 | 使う | 残る |
|---|---|---|
| nw::lyt（最悪時 738,876） | 借用 327,696 | **411,180** |
| nngx（いま 1,220,172） | LIST 98,336（現行から +32,768） | 1,121,836 |

- [x] F-313 の結論を他の点と突き合わせた（F-314）。誤り 1 件を訂正、2 件は独立に裏付け
- [ ] nngx ヒープの**場面ごとの最小空き**を測る（増分 32,768 B と小さいので優先度は低い）。
      `PATCHES/sample_lyt_heap.py` に nngx 側を足す

### 段 3 以降（Simulator の移植。★キーボード＝文字入力・数値入力は移植しない）

- [ ] 段 3: 描画基盤（可変幅・2 フォント使い分け・UTF-8・クリップ・α・スクロールバー）
- [ ] 段 4: メニュー本体（項目木 20＋フォルダ・10 行表示・選択追従スクロール）
- [ ] 段 5: アニメーション（登場/退場 Cubic Ease Out 320ms・選択追従 100ms・
      明滅 1800ms 周期・値変更の跳ね 100ms・決定の跳ね 80ms・長押し 200ms/60ms）
- [ ] 段 6: 説明パネル・インラインリスト・上下画面リストボックス・ダイアログ・ホットキー設定
- [ ] 段 7: 通知（右下・Cubic Ease Out・40ms ずらしのキュー・最大 7 件）

## 2026-09-06 追加（F-315〜F-317。実機検証と仕様書 改訂 3）

- [x] `LIST_SIZE 0x10000` を実機で確認（`list=42/43`）
- [x] `LIST_SIZE` が nngx ヒープからだけ減ることを実機で確認（nw::lyt は ±0）
- [x] 借用 `0x50000` を実機で確認
- [x] **CMAP 方式 2 / CWDH / 256x128 / 日本語**を実機で確認（字形番号 7/7 一致）
- [x] **F-316**: シート記述子 `+0x0C` は `(幅<<16)|高`。正方形では露呈しない誤りを訂正
- [x] 記録量の模型を実測から作り直した（**552 B/文字列 + 48 B/字 + 204 B/Picture**）
- [x] 仕様書 v2 を**改訂 3**（検証器 31 項目・命令 26 件で 0 件）

### ★次にやる（CTRPF 開発。段 3 以降）

- [ ] **F-317 の取り外し手順を実装**（`sub_127D98(1,&node+0x100)` のケーブ）。
      これを入れないと ON/OFF 9 回で nngx が枯れる
- [ ] `GuiFontUi.h`（美咲＋PixelMplus）をプラグインへ組み込む
      （いまは旧 `GuiFontNw.h` の 5x7 ASCII）
- [ ] `LIST_SIZE` を上 `0x10000` / 下 `0x8000` へ（ケーブのリテラルを実行時に差し替え）
- [ ] 借用を `0x30000` → `0x50000` へ
- [ ] **文字を §3.2（TextWriter 直呼び・共有バッチ 1 本）へ**
      上画面 43 本では TextBox 方式が `LIST_SIZE 0x10000` を 6% 超える
      ★「1 本のバッチに複数文字列」は静的には確定・**実機未確認**。最初にここを確かめる
- [ ] Simulator の UI 本体（段 4 メニュー / 段 5 アニメーション / 段 6 リスト・ダイアログ / 段 7 通知）

### 実機の状態

素に戻してある（フック 4 本すべて素、`.bss`・ケーブはゼロ、nw::lyt は完全復帰）。
**nngx だけ 955,800 B（本来 1,220,172）。F-317 の漏れ。再起動で戻る。**

### F-318（2026-09-06）: F-317 の削除を実装・実機検証

- [x] 削除ケーブ 43 語（束縛中を避ける守りつき）を作り、objdump と idalib で検証
- [x] 実機で **132,192 B が丸ごと戻る**ことを確認（`g_GpuCmdPtr` 等は無傷）
- [x] 仕様書 §5.3 の順序を訂正（**フックを外してから削除**）
- [x] 監査が LDR を 1 件も見ていなかったのを修正（検査件数を必ず出すようにした）
- [x] `OwnGui.cpp` に `DeleteCmdLists()`、`Disable()` の順序を訂正
- [x] 検証器に `kDelCave` の照合と `Disable()` の順序検査を追加
- [ ] ★プラグイン側の実機検証（ON/OFF を数回して nngx が減らないこと）

### F-319（2026-09-06）: UI フォントのプラグイン組み込み

- [x] `GuiFontUi.h`（美咲 362 + PixelMplus 27 + 塗り潰し 1）を `GuiV2.cpp` へ
- [x] `DrawText` / `MeasureText` を UTF-8 + CWDH 可変幅 + 書体選択に
- [x] 安全弁を `552 x 本数 + 48 x 字数 + 204 x 枚数` に（F-315 の実測式）
- [x] `WriteCaves` が A1/A2 の `LIST_SIZE` を上 `0x10000` / 下 `0x8000` へ
- [x] 書き換える語 79 がリテラルであることを静的に検査（群 1 に追加）
- [x] 検証器の群 2/3 を UI フォント用に書き直し（`own_font_data.build_ui` が正本）
- [x] ★実機で確認（2026-09-06「実際には問題なく描画されました」）
- [x] 一式を `BASELINE/gui_v2_ok_f319/` と `BACKUP/f319_uifont_20260906/` へ凍結
- [ ] ON/OFF を数回して nngx が減らないこと（`DeleteCmdLists`）はまだ未確認

### F-320（2026-09-06）: `threadCreate` の呼び出し文脈

- [x] クラッシュダンプの読み方を `DOCS/crash_recovery.md` に文書化
- [x] `__createThread` が TLS の magic を確かめないことを逆アセンブルで確定
- [ ] ★`GuiMenu::Initialize()` の `threadCreate()` を安全にする
      （案 1: TLS の magic を見て違えば延期／案 2: 自前スレッドをやめて
       CTRPF の `Task` か既存のフレーム処理に相乗りする）
      いまは「plugin ready の直後に ON にしない」で回避している

### F-321（2026-09-07）: Simulator の本格移植

- [x] 段 4a GuiV2 の枠を作り直す（不均一スロット 50+2 / Picture 24 枚/画面 /
      借用 0x60000 / LIST_SIZE 上 0x18000）
- [x] ★`OwnGui` の `BorrowHeap(0x30000)` 直書きと `kBorrowBytes 0x50000` の
      食い違いを潰した（検証器が片方しか見ていなかった）
- [x] 段 4b メニュー木・選択・スクロール・説明パネル・下帯
- [x] 段 5 アニメーション（開閉 320 / 追従 100 / スクロール 100 / 脈動 1800 /
      値の跳ね 100 / 起動の跳ね 80 / 端の跳ね 100 / 連続入力 200→60）
- [x] インラインリスト（180ms・6 行）とダイアログ（160ms）
- [x] `PATCHES/preview_menu.py`（実機なしで見た目を PNG 確認）
- [x] 検証器の群 5 を **Simulator の ui-model.js / app.js との突き合わせ**へ
- [ ] 段 6 上下画面リストボックス / ホットキー設定 / 入力待ち
- [ ] 段 7 通知（右下・キュー・押し上げ）
- [x] ★実機で確認（2026-09-07。メニュー・行・値・2 書体の使い分けが出た）
- [x] 一式を `BASELINE/gui_v2_ok_f322/` と `BACKUP/f322_simulator_menu_20260907/` へ凍結
- [ ] アニメーション（開閉・跳ね・脈動）の目視確認は取れていない
- [ ] ★移植しない: 自前キーボード / 文字入力 / 数値入力（利用者の指示）

### F-322（2026-09-07）: 文字ペインの横の半画素

- [x] 症状の切り分け（画素幅の偶奇と一致。字数ではない）
- [x] 経路を idalib で確認（アンカー -幅/2 / 整列 +幅*0.5 / 原点 -文字幅/2）
- [x] 横を左アンカー + 左寄せにして `/2` を経路から消した
- [x] 検査を群 8 に追加、仕様書 §3.1 を書き直し
- [x] ★実機で確認（2026-09-07「問題なく表示されました」）

### 共有バッチ移行（2026-09-07 起票）: §3.2（TextWriter 直呼び）へ

★当初「F-326」と呼んでいたが、その番号は別エージェントのプラグイン側が使っている。
  この項の検討メモは `scratchpad/MEMO_f326_textwriter_migration.md`（FINDINGS 番号なし）。

通知が予算の都合で 2 件（Simulator は 7 件）に制限されている。
借用 `0x6C000` の配置が **99%**、上画面の記録が上限の 78%。**これ以上広げられない。**
`TextBox` 1 本の領域の **91% がバッチ**なので、共有バッチにすれば
上画面で領域 -171KB / 記録 -51KB の見込み（`scratchpad/MEMO_f326_textwriter_migration.md`）。

★この項の調査は **F-337〜F-340** に改番した（別エージェントのプラグイン側 F-323〜F-336 と
番号がぶつかっていたため）。旧 F-327→F-337 / F-328→F-338 / F-329→F-339 / F-330→F-340。

- [x] 移行で何がどれだけ変わるかを機械で見積もり
- [x] 静的に確定していることの棚卸し（色・書体・位置が**字ごと**にバッチへ入る）
- [x] 静的（F-337。`scratchpad/MEMO_f337_textwriter_static.md`）
      `DrawString` はカーソル 2 欄しか壊さない / 吐き出しは 16 字ごと・色の連 6 本ごと /
      提出は 1 フレームに何度でも呼べる / バッチは通常メモリ
      （★「書体を混ぜると群が分かれる」は誤り。群の鍵は**記述子 +0x08**＝
        テクスチャの物理番地なので、同じアトラスなら 1 群のまま。F-339 で実機確認）
- [x] 記録の式を実測で確定（F-338）
- [x] ★**実機で「1 本のバッチに複数文字列」を確かめた（F-339。通過）**
      34 字・3 本・色 3 種・書体 2 種が 1 本のバッチから正しく出た
- [x] ★色替え・書体替えの費用を分解した（**F-340**。実機 15 点）
- [x] ★★費用の式を**逆アセンブルの写し**に置き換えた（**F-341**。実機 19 点で誤差 0、
      うち 3 点は予言してから測った）。正本 `PATCHES/batch_cost_exact.py`
      字 12 語 / 吐き出し 28 語（16 字ごと・色替え 6 回ごと）/ 色替え 16 語 / 書体替え 0
      ★現在色の初期値は **writer+0x18＝最後に描いた文字列の色**
- [x] あふれたときの守りを静的に確定（F-340。超えた字は静かに捨てられる／
      `batch+0x06` で語数の上限を外から縛れる／コマンド語の器は最悪でも 73%）
- [x] ★★設計を数字で決めた（**F-342**。`PATCHES/design_shared_batch.py`）
      ★費用の 8 割は**コマンド語の器の取りすぎ**（1 字 312 B 取って 48 B しか使わない）。
      `batch+0x20` は誰も読まないので詰められる（5 関数を読んで確認・実機でも確認）
- [x] **第 1 段（案 B）をプラグインへ投入**: `GuiV2::BatchCmdWords()`。
      配置 438,784 -> 231,552 B（借用の 99.2% -> 52.3%）。検証器 群 4 を更新し異常 0 件
      ★**まだビルドしていない**
- [ ] ★ビルドして実機で確かめる（`make clean && make` -> 3gx 差し替え -> 目視）
- [x] 空いた 207,296 B の使い道を決めた（**F-343**。利用者の判断）
      **通知 2 -> 7 件**（借用は据え置き）+ 上画面 `LIST_SIZE` 0x20000 -> 0x28000
      配置 271,616 B（61%）/ 上の記録 103,728 B（0x28000 の 79%）。検証器 0 件・ビルド成功
      ★矩形の枠を画面ごとに分けた（上 86 / 下 56）。共通のままだと下画面が上限を超えた
- [x] ★**手紙で落ちる件を直した（F-344）**。借用 0x6C000 -> 0x50000 / 通知 7 -> 5 /
      矩形 上 86 -> 74。配置 255,616 B（78%）。検証器 0 件・ビルド成功
- [x] ★**実機で確認済み: 手紙が開ける**（F-346。利用者「手紙が開けました」）
      アトラス以外をプラグインの `.bss` へ移し、借用を 442,368 -> 36,864 B にした
      退避 `BACKUP/plugin_full_20260907_f346/`
- [ ] 通知を 7 件へ（**画面に入る上限**。F-347）。`kNoticeMax` 5->7 /
      `kTopSlotCaps` に 16 字x2 + 24 字x2 / `kMaxRectTop` 74->86 / `kPlugBytes` 0x50000
- [x] **キーボードの移植・ローカル検証・ビルド**（F-349。今回の依頼で過去の保留を解除）
      通常/小型×かな/カナ/QWERTY、数値DEC/HEX/小数。`DOCS/keyboard.md`。
      重なりなし5矩形の枠、`oIdx`をu16化。借用0x9000維持、plugin0x70000、下LIST_SIZE0x2D000。
      C++とSimulatorの10,943入力遷移/15描画場面/既存検証群/ARM構文検査後に3gx生成。
- [ ] **キーボード移植版の実機確認**。タッチ・十字キー・編集/取消/確定・ホットキー、表示負荷、手紙を開くこと。
      実機未適用。F-346を戻り先として維持。実機適用前にも検証と成果物SHAを確認する。
- [ ] スライダー専用バーの移植（slider項目も今回は数値キーボードで編集）。
- [ ] 通知を 3 件以上出して重なり・押し出しを目視（まだ）
- [x] ★**入力の無効化を実装した（F-350〜F-355）**。ケーブ 2 本 + 制御ブロック。
      A `0x0053CDF4`（ボタン一括 + タッチ）/ B `0x003534E0`（SELECT を読み替えの手前で消す）
      ★真因: ゲームは `sub_483020` で **SELECT を START に読み替えて bit2 を消す**
- [ ] ★3gx で残りを確認: ボタン一括遮断 / タッチ遮断 / 暗幕のフェードと二重描画 /
      GUI を OFF にしたときの完全復帰（`0x0053CDF4` と `0x003534E0` が素に戻るか）
- [ ] キーボード（F-349）の実機確認
- [ ] ★根治: **閉じているときは借用を返す**（空きが 490,004 B に戻る）。
      通知は閉じていても出るので「通知の間だけ借りる」仕組みが要る
- [ ] 他の重い場面を洗う（手紙は 131,456 B。これより重い確保がないか）
      `probe_lyt_heap.py` を場面ごとに走らせて一番きつい空きを測る
- [ ] 実機で確認できたら `BACKUP/plugin_full_20260907_f343/` を取る
- [ ] 借用 `kBorrowBytes` を下げるかは保留（いま 61% なので 0x50000 まで下げられる）
- [ ] 第 2 段（案 C）共有バッチ: ★単位は「画面 1 本」ではなく
      **表示リスト中で連続する文字列のかたまり 1 つ**（輪は描画順そのままなので重ね順が壊れる）
- [ ] 検証器: 群 3/4/6/8 を新方式へ。新ケーブを監査対象に。安全弁を `batch_cost_model` へ寄せる
- [ ] 実装: プラグインへ（通知だけ → メニュー）
- [ ] 中止する場合の代案（通知の枠だけ TextBox で増やす / キューで順に見せる）
- [x] **「ゲームスピード変更」チート `0054C6E8` の解析（F-356）**。
      `sub_54C684` = フレームペーシング（`sead::GameFrameworkCtrNw4c` vtable スロット 31、
      本作の派生は `UlcdFramework` / `sub_24F0A8`）。
      `MVN R0,#0xFF000000` で「前フレームの VBlank カウンタ」を巨大定数に置き換え、
      待ちループへ入らせない = フレーム制限の撤廃。
- [ ] `this+0x70`（1 フレームに要る VBlank 数。30fps なら 2）を実機で確定する。
      `sub_54C684`（`0x0054C684`）入口に bp → `[R4+0x70]` を読むだけ。静的走査では出なかった。
- [ ] `REFERENCES/CHEATS/speed.txt` のキーは `0x110`/`0x120`（R+→ / R+←）が正しい。
      利用者の貼り付け `0x012`/`0x022` は B+→ / B+← になる（F-356 §5）。
- [x] **`this+0x70` を実機で確定 = 2（2 VBlank 待ち = 30fps）**（F-357）。
- [x] **「FPS だけ上げて進行速度は据え置き」は不可能と確定**（F-357）。
      メインループ `sub_54C818` が 1 反復 = Calc 1 回 = 提示 1 回で、
      Calc へ dt が渡らない（`MethodTree_WalkAndInvoke(node)` のみ）。
      実測: `+0x70` 2->1 で周期 33.751->17.770 ms（1.899 倍速）。
- [ ] フレームワークオブジェクト（この boot は `0x32939880`）への
      **静的な入口からのポインタチェーン**を作る。いまは bp で R0 を拾っている。
- [ ] `+0x70` を初期化しているコードは未特定（`STR Rd,[Rn,#0x70]` 339 件に該当なし）。
      スローモーション（`+0x70` = 3/4）を作るならデータ 1 語で足りるので急がない。

## しずえ会話スキップ（2026-09-08 開始・F-358）

- [x] `BsFgProc::Setup` の正体を確定（`fgobj::Proc` のスロット 3 = `0x0059C974` ＋同名ヒープ）。
      **フィールド読み込み（準備中）の 1 ステップで、しずえ会話とは無関係**。
- [ ] ★実機でルート確定: `0x00951338`〜`0x0095133C` を
      タイトル / プレイヤー選択 / しずえ会話中 / 準備中 / 村に出た直後 の 5 点で読む。
      **要デバッガ再接続 + タイトルから起動**（この作業時は切断されていた）。
- [ ] 部屋 `0x63`（`PlayerSelect` = しずえのスポットライト）の進行を回している主体を特定する。
      `script::FlowEngine` / `libms::FlowNode*` の線が濃い。
- [ ] 部屋遷移の要求 API を確定（`word_94A3D0` = `0x0094A3D0` が候補。`0xFFFF` = 要求なし）。
- [ ] スキップの当て先を決める（会話フローを終わらせる側。★部屋 ID の直接偽装は非推奨）。
- [x] しずえ会話スキップ: 経路を端から端まで確定（F-359）。
      `Room_UseExit(vc_ROOMDAT(), プレイヤー番号, 1, 0, 1, 1.0f)` を呼べば村へ出る。
      部屋 0x63 の出口表は 4 本で出口番号 = プレイヤー番号 0..3。
- [ ] ★**安全に撃てる最速のタイミング**を実機で詰める（部屋 0x63 に入って N フレーム後の N）。
      会話の段階にセーブ読み込み・プレイヤー生成が混ざっている可能性がある。
      大きい N（300 フレーム程度）から始めて下げる。
- [ ] 選択されたプレイヤー番号を持つグローバルの特定（個人用なら設定値で足りる）。
- [ ] ★高位領域（0x00B00000〜0x00C50000）は**起動ごとに配置が変わる**。
      番地を焼き込まないこと。何のセグメントか（オーバーレイ？）も未確定。
- [x] ★**しずえ会話スキップ 実機で成功**（F-361。2026-09-08）。手順は `DOCS/skip_isabelle.md`。
- [ ] ★**副作用の確認**: この近道では「準備しています」が出ない＝`BsSvMgr` mode 7
      「成長処理後のセーブ関係処理」を飛ばしている。
      **飛ばしているのが起動時のセーブだけか、成長処理（日付変わりの処理）まで含むか未確認。**
      日付をまたいで使い、草・カブ・住民の更新を見る／通常経路と `byte[BsSvMgr+168]` を比べる。
- [ ] 常設チート化（CTRPF プラグイン）。★ゲームのメインスレッド（フレーム境界）から呼ぶこと。
- [ ] `ModulePlSelect` の case 5 が呼ぶ `0x00606D78`（BsSvMgr 系）を読む
      — 会話中にセーブが走る経路があるかの確認。

## F-362 の残件（メッセージ経路 / しずえスキップ）— 2026-09-08

- **`sub_30C9C4` `0x0030C9C4` の中身を読む。** `byte_956231` で boot 中 1 回だけ走る
  「村へ入る前の一括処理」。`sub_10D980` / `sub_110CFC` / `sub_10FF58` /
  `sub_10DBA0` / `sub_10CCB8` / `sub_110668` が日付変更の成長処理（草・カブ・引越し）を
  含むかどうかが未確定。**`DOCS/skip_isabelle.md` の副作用評価がこれに依存する。**
- **しずえスキップを安全側にする。** `Room_UseExit` の前に `sub_30C994` `0x0030C994` を
  呼ぶ版を作り、日付をまたいで実機で比較する（雑草・カブ価・引越し・郵便受け）。
- メッセージ経路の索引を `DOCS/structures.md` へ移す
  （要求スロット `mgr+864` / 表示スロット `mgr+860` の 124 バイト構造、
  `sub_6019A4` `0x006019A4` が唯一の合流点）。
  ★トレースを仕掛けるなら `sub_5DC940` ではなく **`sub_6019A4`**。
- `ModulePlSelect.cro` の残り 11 分岐（case 2〜12）は未読。
**2026-09-09 F-384・現在の実機状態:** 通常チャットから内蔵SWKBDを一回呼ぶケーブを
検証後に適用済み。実機はSuspend中、state=0/run count=0で未発火。

- [x] Resumeし、フレンドチャットではなく通常チャットを一回開く。
- [x] 内蔵ソフトウェアキーボードが表示されたら、最初はキャンセルしてゲーム復帰を確認する。
- [x] 再度Suspendし、`0x009BDD00` のstate/run count、Prepare/Start/Wait結果、
  `0x009BE138` のSwkbdResult、`0x009BE144/148` のtext offset/lengthを読み取る。
- [x] キャンセル復帰が安全なら、かな入力→漢字確定を一回試し、共有ページのUTF-16結果と
  入力中の候補表示を別々に評価する。現在版は確定文字をゲーム内チャットへ送らない。
## 2026-09-09 F-385 内蔵SWKBD初回起動後

- [x] 通常チャットを入口に内蔵ソフトウェアキーボードを起動。
- [x] 最初はキャンセルし、APT状態0・ハンドル解放成功・ゲーム復帰を確認。
- [x] パッチを残したまま通常チャットを閉じて再度開き、かなを入力して漢字候補を選ぶ。
- [x] 右ボタンで確定後にSuspendし、`SYSTEM_KEYBOARD/read_native_chat_result.py` で
  `SwkbdResult`、text offset/length、共有ページのUTF-16確定文字を回収する。
- [ ] 候補順位・文節変換の取得には、確定文字とは列と結果とは別に、SWKBD実行中の候補生成・
  描画・辞書参照を観測する必要がある。今回の0x400-byte戻り設定だけで候補一覧が返るとは扱わない。

## 2026-09-09 F-386 内蔵SWKBD漢字確定後

- [x] パッチを残したまま通常チャットを再度開き、`漢字テスト` を入力して右ボタンで確定。
- [x] `read_native_chat_result.py` で結果コード2、offset=0、length=5 UTF-16単位、
  共有ページの `漢字テスト`、APT状態0、run count=2を回収。
- [x] 利用者の正常復帰報告と、結果コード・UTF-16共有メモリ・APT状態を照合。
- [x] 候補一覧・候補順位・文節境界を得るため、SWKBD実行中に候補生成・描画・辞書参照の
  どこを観測するかを、F-363の静的番地と今回の実機起動経路を使って設計する。
- [ ] 次の実機書込み前に、観測パッチの全分岐・全PC相対LDR・領域重複・失敗時復帰を
  機械検証し、停止中実機の現行パッチ/BSSと突き合わせる。

## 2026-09-09 F-387 SWKBD表示候補の読取準備後

- [x] 入力変更経路と表示経路の2経路から、SWKBD内のapp pointer、表示候補cache、
  全候補数、選択index、表示件数を確定。
- [x] 書込み・Resume・breakpointを行わない `read_live_candidates.py` を作成。
- [x] 元ARM 8語、12候補fixture、折返しindex、異常系5件をオフライン検証してPASS。
- [x] ACNLをResumeして内蔵SWKBDを開き、候補を表示したままRosalinaのProcess Listで
  `swkbd`を空いている通常GDBポート（第一候補4001）へ割り当てる。
- [x] GDB接続でSWKBDをSuspendし、`read_live_candidates.py`相当の検証付き取得で入力・全候補数・
  選択index・表示中候補を取得する。ACNL用番地/スクリプトをSWKBDへ使わない。
- [x] 表示候補の実機順位をF-363のPC再現と比較した。今回の差3件は候補末尾の文字種変換と確定。
- [ ] 文節境界は表示候補cacheと別に、選択確定経路`0x18C414`およびphrase result領域を追う。

## 2026-09-09 F-388 別プロセス確認後

- [x] ACNLをSuspendしてもSWKBDが動き続けることを画面とACNL state=2で確認。
- [x] 未確定`かんじ`を維持し、Rosalina Process Listで`swkbd`をport 4001へ割り当てた。
- [x] port 4001へ`arm-none-eabi-gdb`で接続してSWKBD自身を一時Suspendした。
- [x] 検証付き読取を行い、全17候補を回収後にdetachしてSWKBDをResumeした。

## 2026-09-09 F-389 実機SWKBD候補順位の回収後

- [x] `swkbd`をGDB port 4001へ割り当て、PID 60へ読み取り専用でattach。
- [x] 実行コード全量照合、app pointer、入力cache、全候補数、選択index、表示cacheを回収。
- [x] app全域から17件の88-byte候補recordを回収し、F-363の独立PC結果と照合。
- [x] 特殊record 3件を供給済み原本ARMでローカル復号し、全17件の順位を確定。
- [x] 各取得後にdetachしてSWKBDを再開。対象への書込み・breakpoint設置なし。
- [ ] 複数文節入力を使う次回観測に向け、phrase resultの位置・件数・境界表現を
  `0x18C414`の選択確定経路と`0x1145AC`以下の生成経路から独立に確定する。
- [ ] 文節読取器を作成し、原本ARM・fixture・異常系でオフライン検証してから実機で読む。
