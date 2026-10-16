# gohan機能移植・チャット設計

記録: IDA-gpt-6-T001 / IDA-gpt-6-F002、担当GPT-6、2026-10-11。複数静的照合MEDIUM、実機未確認。

## 操作と所有者

FOXXY IDLEは自分のactorだけをstate6へ移す。共有38Bの状態packetをゲームスレッドでコピー・XZを実座標から圧縮しActor_SetStateへ渡す。気絶はstate0x9Dで復帰位置をpacket+0xFへ入れる。他プレイヤー強制、待機Sleep、ネット送信の二重実行は不要。既存Actor_SetStateが送信経路を持つ。

Vapecordの無効位置消失抑制はJPNの0x6FA8A8/0x52734Cだけを可逆patchし、Field_SetItemAtWorldXYフックは5つのThumb callerだけ次段階IDへ進める。元Itemの局所コピーを渡し、保存mapを先に直接変更しない。第5引数はnativeがstackから読むfloatの生bitsをu32として保持し、hardfloatのS0へ移さない。LRはMITMの元callerを__builtin_return_addressで取得する。

チャットは普通チャットの送信通知vc_CALLCHAT(1,2)で原文を捕捉。コマンド以外/OFFは元経路へ返す。送信前の数字フィルタは認識済みコマンドの場合だけBsSkb_ReturnWait_Calcで回避し、元flagsを復元。結果一覧は既存GameListを普通チャット上に出すmodeを追加し、入力欄への挿入はnative TextManager経由でゲームスレッドに予約。既存漢字変換hookとの重複を避ける。

PocketItem::Requestはメニュースレッドからのみ呼び、HHD画面も既存Showを使用。weatherは既存の連動setterと共有する。時間はnative Dateを検証してTime_SetFromDateとTime_StoreToSaveをゲームスレッドで呼ぶ。time set単独はnative Menu_RequestOpen(0x2E,0)。FOXXYのitemselect/actor0x3Fのglobal改変は不要。

## 最新仕様

- 数字1つは分。setは現在の時の分だけ変更、add/subは分差分。HH:mmは時分、MM-dd/YYYY-MM-ddは日付。day/night/noon/midnightは7:00/18:00/12:00/0:00。
- アイテム名はかなで部分一致。原ROM通常名はかな（漢字0/control tag0を確認）、隠し名は既存かな列。候補はnative下画面リスト。command listはプレースホルダを含まない固定文字を挿入。
- MapEditor/BuildingEditorは後に起動した方を優先し、先行を閉じて退場・資源返却後に起動する。最新訂正で両方アクション式、再実行/Bで閉じる。checkboxとarmは廃止し、公共事業エディター設定folder/全7項目を削除する。
- MapEditorカーソルalphaは90/120/60固定。自前GUI有効化で自動openしない。DecorCatalogとTrashは同じ項目のON/OFFで制御。
- メニュー移動とdropID共有は利用者の明示依頼。中断済み参照整理/共有callback統合は再開しない。

## 根拠と反証

PC検証: tools/gohan_chat_ports/verify_prebuild.py（datetime独立4330条件、22入力anchor、13CPP ARM構文）、verify_linked.py（全分岐/LDR境界/重複/hash、原native日時/送信通知、認識6＋通常/OFF2、数字filter3、成長caller/第5引数12、IME pause、状態packet2、メニューの実ARM構造、B/再実行/heldキー/排他/退場待ち、しずえ）。fixtureのGPU/ネット/FS/native副作用は模擬または未実行であり、実機成功の代替ではない。

原callerのfloatをstack bitsで渡すこと、通知先頭のPC相対LDRを補うこと、DateのR2/R3をDB型にも記録することをABI検査へ含める。既存frame callback所有者数を容量16と照合する。フォントは現source文字列と公式BDFから生成し、画素/CMAP・欠字gateを通す。buildの2MiB通知は以前の正常ELFでも同閾値を超えており、今回だけの現象としない。静的メモリ増分は成果物サイズ検査へ保存する。

原FOXXY/Vapecord source・地域表と更新code.binの命令、IDBのcaller/consumerを照合。state0x9D表0x844760は旧IDBに0x672684、入力原本は0x676284。旧patch来歴未確定なので表の復元は保留し差を記録する。実機で座標/復帰/翌日更新/IME共存/未認識チャットに差があればMEDIUMの結論を見直す。

実機操作なし。未確認sourceは独立gohan作業枝に保存しmainへ入れない。commit/pushは最終検証後一括。

## 入力修正（2026-10-12、IDA-gpt-6-T003 / GPT-6）

利用者がMapEditorのみ「camera固定、スライドパッドでplayer移動、下画面無反応」を実機報告。GameList::Presentはlistの存在に加えてfieldがShown以外の状態も含む。MapEditor::Start自身のHoldField(true)によりPresent&&!Wantedが成立し、action wrapperの退場gateが継続Tickを止めていた。両editorの退場待ちをRunning前だけに限定した。排他/B/再実行は維持する。

チャットはcheckbox適用値でhookを有効化し、hotkeyで効果を反転するToggleEffect登録を削除。普通チャットのnative WaitCalc前に適用hotkeyを検出して送信と共通のcapture queueへ原文を渡す。長押しでは繰り返さず、chordの全ボタンreleaseまでnative取消を抑止する（Rを先に離して残ったBでも閉じない）。OFF/menu中はcaptureせず、再束縛にも追従。通常送信経由も保持する。

旧ELFの実Start/HoldField/Present/Wanted/action wrapperによる再現はfield Hidden後の移動/touch転送/game入力遮断が全false。新ELFでは同条件の実Tick/StepMove/PushTouch/BlockGameAllが全true。hotkeyのnative Wait入口からweather実行、保持/部分release/全release再押下/rebind/menu/OFFもPASS。根拠tools/gohan_chat_ports/verify_input_fix.py、work/evidence/gohan_editor_chat_fix/{old_repro,input_runtime,linked_runtime,linked_checks}.json。GPU/FS/OS/scene端点はfixture、修正実機未確認。静的＋ARM1176はMEDIUM、実機で差があれば見直す。

新3gxはartifacts/plugins/gohan_editor_chat_fix1/gohan.3gx、SHA256 9a6d32897b28d8c0cb896244d60083fe5e864c1710ed9771976093292d6eeb8d。4330parser/date・22anchor・13CPP、欠字0、しずえ、linked567関数/35219命令/6548分岐/3294PC参照・元native ABI/通常送信/IME/両editor遷移もPASS。前配布版/通常成果物は保持。pluginのlifecycle/hotkey修正のみで、既知のnative概念/番地/型とDBは更新していない。最新公式XMLのDB/bytes/hashを再照合して保存する。
