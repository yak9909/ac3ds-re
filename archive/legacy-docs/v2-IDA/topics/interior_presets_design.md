# 模様替えUI修正・チップ複製・内装保存

解析: IDA / gpt-6.1-sol / 2026-10-10。IDA-gpt-6.1-sol-T003、F016。対象は日本語無印ACNL＋更新、main入力SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb。

## 先に実装するUI/カメラ修正

- F015はdraw時globalAlphaだけを変えたが、`ssys_ma_lyt_Layout_RecordPaneTree 0x5686D4`はouterLayout+285のdirty byteが0ならDrawHookまで到達せず保存済みGPU列を再利用する。命令0x568704..0x56870Cと終了時0x5687B0のclearを照合。Editor_SubmitLayoutsのmain outerLayout+664という範囲自体はARMで一致。利用者実機の「チップだけ隠れる」と一致する経路だがdirty byteの実測はなし（原因MEDIUM）。
- 不透明度変更時、正しいscene/editor所有者のLayoutのdirtyを立て、通常の記録経路でキャッシュを再生成する。閉窓/Reset時も不透明な列を再記録。GPU列へ直接追記しない。各paneのalpha復元とnative Submit順を維持。
- リストのゲーム入力遮断を維持し、HHD式InputHookでリスト表示時だけCTRPFの生十字入力をnative方向bitへ変換する。スライドパッドもリストで許可する。通常室内はnative入力経路、パッド移動はmode25＋実際の模様替えUIのみ。メニュー/他ダイアログ/遷移の停止を維持。
- パッドの最大速度は2から6 world units/frameへ（3倍）。方向基底/15% deadzone/斜め正規化/Y不変/毎frameのnative基準への加算は維持。

## チップと内装の実装設計

- 選択窓はMapEditor範囲選択で使用するnative ItemSelectWindowを再利用する。固定2行「複製」「やめる」、B取消、状態/キー注入/音/幅合わせは同じ契約。チップのnative Selectは6frameまたは24 world UI units移動でdrag開始するため、安定した押下だけを長押し候補にする。ドラッグ・短いタップ回転・親子選択を壊さない設計が必要。
- 内装は現在の家具Item（リメイク情報を含むflags）、現在anchor/向き/層、壁紙・床とvariantを保存。roomサイズ/部屋所有情報そのものは読み込みで変更しない。宛先は現在部屋。版/長さ/checksum/全配置を検証してから変更する。
- 保存サイズと現在サイズが違う場合、全footprint/壁位置/上載せ親の範囲を検査し、範囲外を削って配置するか確認する。取消は部屋不変。既存家具actor/記録/衝突の通常破棄を完了してから床層→上載せ層の順で生成し、エディターのチップも更新する。単なるsave-data memcpyは即反映ではない。
- ネイティブ再構築は非同期Loadを含む。部屋/scene/ownerの固定、処理中入力遮断、失敗時に直前内装へ戻す経路を調べる。サイズ違いの座標対応は部屋の共通中心基準とし、壁を宛先の同じ側へ対応させるか要確認。

### 確定した契約/採用手順（MEDIUM: 複数静的経路）

- GUIに内装の保存枠1〜8と保存/読み込み/入れ替えを追加。利用者回答で保存枠との交換も必要。交換は反映完了後に旧内装をその枠へ書く。失敗時は旧内装へ戻し、枠を保持する。
- 家具の正本は現在FieldMapの2層にあるanchor Item。`BsFtrMgr_PopulateRoom 0x68F1C0`の走査・record組立と`AcFtr_CreatePrepare 0x56DE24`の書込先で一致。家具族を持つanchorだけを読んでflagsの上2bitを向きへ分ける。12B記録の+4=x,+5=z,+6=rot,+7=layer,+8=requestKind、残り0。保存時は家具actor表の全数/完成/状態2と照合し、操作中は拒否。
- サイズは現在のinclusive boundsをファイルへ保存。座標は共有16×16mapの絶対anchorを維持し、自動移動や壁側変更はしない。範囲外削除はnative Footprint Init/GetCount/GetOffsetの全セルと実Field壁sideを検査し、範囲外の親が消えた上載せも削る。サイズ違いなら削除数0でも確認を出す。同じサイズの不正配置を勝手に削らない。
- 長押しはnative Select状態のみ。固定点から24未満の間だけnative+1092の6frame drag猶予を延長し、18frameでChipのnative取消0xB432DC→Neutralと同じ指のcaptureを行って窓を開く。24以上動いたらnative dragを即許可、短いreleaseはnative回転のまま。native Select Enter0xB42C70が同じ開始点とカウンタを初期化することもARMと状態表で照合。複製はraw Item flags/向きを保持して既存TryPut/Spawnとpendingチップ追加を通す。
- 長押し複製は家具リストのON/OFFやSDリスト素材に依存させない。リストの通常frame処理が動いていない間だけ、常設InteriorToolsのframe処理から複製pendingのチップ追加を進める。リスト解放で複製pendingを消さず、Editor所有者変更/期限切れは既存ChipStepで取消する。通常リスト配置の処理順は維持する。
- 変更前snapshotをSDの復元ファイルへ検証付き保存してからactor state7（0x5731F8→0x51F4C0→破棄要求）を使う。DestroyBeginはstate7でもmap/ModuleFtr/親を解除し、Finalizeはactor表から解除する。全table空きと3描画frame待機後に生成する。Load待ちはframe状態機械で行い、ゲームを止めるループを作らない。床層→上載せ層、床族→壁族の順にnative TryPutしてSpawn。異常時は部分生成を同じ経路で片付け旧snapshotを再生成する。背景は既存の機能/所有判定と下位setterの毎frame反映を使う。
- Editorが開いている場合、操作がないNeutralだけで開始。使用中chipだけRelease→3frame後に全112枠DtorInPlace/Ctorして親子/記録handle/アニメを初期化。生成完了後native Editor_CreateChipsで全recordと親子を再構築、新品rootだけ自身へ戻す。Out枠のSetupだけで再利用する方式は不採用。Editor閉/scene変化では所有者を再検査して異なる部屋へ書かない。
- snapshotはversion/固定size/count/予約0/checksum/全Itemの家具族/footprint/層・向き・占有重複を検証。SD操作はメニュースレッド、ゲームの読書きはFrameStep。atomic mailboxでデータ受渡し、保存は一時ファイル書込→読戻し→旧ファイル退避→rename、取消では宛先に触れない。
- 選択窓の新しい指はnative窓へ渡すため、全タッチ遮断だけではEditorとの競合を防げない。操作前のNeutral calc/adj（editor+52/+56）を退避し、待機calcへ一時切替えてEditorの入力更新を止める。scene/owner/ポインタが同じかつ自分の待機calcの間だけ元へ戻す。Submitメソッドは別経路で維持し、ItemSelectWindowだけ独立更新する。EditorLiveを待機calcでも有効とする共有関数を用意し、タブの不要な再読込/解放を防ぐ。

## 検証/配布

ソース→ビルド→linked ARMのキャッシュdirty/復帰、list入力、速度と基底、長押しと取消、file検証・clipping・復元を検査する。新変更は未実機、gohan work/interior-presetsへ保存する。実機に適用/Resumeはしない。
