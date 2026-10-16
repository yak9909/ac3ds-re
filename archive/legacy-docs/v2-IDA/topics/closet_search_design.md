# ネイティブクローゼットとチャット検索

訂正（IDA-gpt-6-F007/T010、2026-10-12）: T009は利用者実機で背景のみ/開始タイムアウト。以下のchat凍結・手動detach・元actor復元方式は撤回し、[実退場修正](closet_exit_fix_design.md)のnativeキャンセル→親/keyboard破棄→tab復帰、終了後native chat再起動へ変更。storage/slot/取得解析は保持。前CPU fixtureはtabを初めからidleへ置いたため実chat退場をカバーしていなかった。

記録: IDA-gpt-6-F006 / T009、IDA、GPT-6、2026-10-12。対象は日本語版無印＋更新、code SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb。静的照合MEDIUM、実機未確認。

## 要件と設計（実装前）

利用者の指定により、取得はnativeの掴む／持ち物移動をそのまま使う。チート側で決定ボタンからPocketItemを呼ばない。名前検索はhitのみ、ID検索は1tabと本来の6page制限を外した全有効ID一覧から指定ID付近へ入る。下方向だけでなく小さいIDへも戻れる。名前・IDの検索前にメニュー開始要求を出し、入場アニメの終了は待たない。閉じたら元のチャットへ戻す。

- `ClosetMenu`はゲームthreadでnative request61→BsMenuChestを生成。Ctorの原先頭PUSHをMITMし、要求中の個体だけprimary vtableを私有複製。通常の家具クローゼットには影響しない。
- BsMenuChest+76のChangeStockItemにgetter/setter/empty lookupを私有providerとして渡す。native drag・pocket・名前表示・pageアニメ・閉じる処理を保持。検索結果で実保存クローゼットを上書きしない。
- 私有providerは4byte ItemID配列。ページ内10slot、1based page。名前hitをID順に並べ、ID検索は全既知有効IDをID順に並べlower_bound付近を初期pageにする。有限のアイテム領域には端があるが、nativeの6page固定上限は設けない。
- 通常3tabのうち1つだけをbindし、残りのpaneも非表示。pageCountを配列件数から算出。指定位slot/itemsは空きslotを含む配列として同providerへ渡せる。設定slotとitemを複数回指定し、開くactionで表示する。
- ephemeral検索領域への持ち物の預入で元アイテムを失わせないため、既に埋まったpocket widgetはnativeのdisabled状態へ。空きpocketへのnative転送を使える。取得後もその枠をdisabledへ更新する。保存クローゼットの書込み関数は呼ばない。
- チャットを破棄せずparent/keyboardのprimary Calc/Drawを一時停止し、native intrusive menu listから2個体のnodeを一時remove。live keyboard/binding/manager chat pointerを一時外し、nativeの3つのmenu key labelを通常値584へ戻す。原順序/値を記録して戻す。native RequestOpenの空list条件を守る。scene変更/元個体の破棄では古いpointerを復元しない。dtorを監視する。
- field hide ownerを専有し、隠れた後にnative requestを1回だけ発行。native bodyが生きている間は全ゲーム入力遮断をしない。終了・creation失敗後はfieldを返し、元chat nodes/vtables/globalsを戻す。保持したキー/touchの解放まではchatを再開しない。
- list表示は確認済みGameList入力を保持。検索開始前に検索中の仮行をShowし、その直後に同期検索、結果をSetItemsへ。表示設定の既定はlist、IDのlistモードは従来の直接取得を保持する。

## native契約

|対象|番地／欄|根拠|
|---|---|---|
|BsMenuChest|factory0x7EAF50、ctor0x1C42D4、38708byte、vt address point0x8E5BB0／25method|原ARM allocator、ctor、RTTI。旧Explorer0x8E5BA8はheader|
|ChangeStockItem|ctor0x297BDC、15528byte、vt0x8EAB34／17method|RTTI、ctor、LoadStep、原table bytes|
|items|uiBase+6から10slot。通常pocket16／controls6／itemBase22|SetupSlots0x297980、Contains0x71A054、UiToSlotIndex0x71A080|
|保存先|base+4*(slot+10*(page0+6*tab))|getter0x71A0B8→0x76E680、setter0x297B28→0x6CC194、独立原ARM。setterのR0はstack-local旧copyで有用な返値と見なさない|
|ページ|currentTab+6236、pageByTab[4]+6240、pageCount+6256|step0x267A50とcounter0x267660、初期6以外の上限なし|
|タブ／スクロール|groups+2664、native page/tab handler0x267A50／0x267B54、scroll anim+3284／+3324|build0x267CE0、layout group/table、原ARM|
|native転送|Get0x70CBB0、Set0x1C4238、WaitInput0x1C32F4|保存pocketを直参照する0x723854／0x26FF50との照合|
|pocket disabled|0x26F030→0x2B9470、widget+217／+301をclear|元LoadStepが不適合アイテムの入力拒否に使用。save書込なし|
|終了|WaitLeave0x1C3214→Actor_RequestDestroy、Release0x1C41A8、Dtor0x1C4408／DeletingDtor0x1C4380|native state table0x848C88／6state×20byte、原call/所有経路|
|menu list|list0x9864FC、head+4／tail+8はnode。actor+20 nodeのpayload+12がactor|Contains0x139750、Remove0x13F718、PushBack0x13F84Cとprepare/release/parent選択|
|chat保持|parentvt0x8E5120／25、kbdvt0x8F1D28／25|RTTI、生table、ctor/prepare/Calc/Draw/releaseとF383/F005|

0x6D102CはAttach、0x6D1B34はDetach。従来のRegister/Unregisterは逆でありF003の保留を解決してDB名を訂正。過去記録の解析者は付け替えない。

## 検証／反証条件

原code.binのARM・RTTI/生vtable・callerと保存providerを独立照合。DBへ型/名前/概念commentを反映しsave、公式XMLへ出力して読戻す。実装後は指定slot、ページ6超、指定ID未満、名前集合、native転送と保存クローゼット不変、list入力回帰、chat保持/失敗/退場とキー解放をPCで検査する。リンク済み全分岐/LDR/ABI/SP/VFP/領域/hashとしずえhookも確認する。

GPU/layoutの成功描画、SD/FS/OSと実機timingはPC fixtureで確定しない。実機でpage/tab/drag/chat復帰が異なれば本設計を修正する。成果物は新しい専用folderへ、旧正常版・全配布版・旧整理dirtyは保持。保存は全作業完了後一括、gohanのwork枝のみ、mainへ入れない。

## 実装・PC検証結果

`artifacts/plugins/gohan_closet_search1/`へ専用BuildClosetSearchで出力。製品の確定hash/ソース版はmanifest、保存結果はwork/evidence/gohan_closet_search/publication.jsonを参照。

- ビルド前4334parser/date条件（0x形式4件追加）、33原命令anchor、15CPP ARM構文PASS。
- 新Closet18scenarioと原保存索引180枠PASS。native getter/setter/WaitInputによるprivate source→real empty pocket転送、元closet不変、occupied pocketのdisabled/アニメ再開始なし、6page超/前後/循環、chat原node順/vptr/binding/登録値復帰、別UI拒否、begin→search、名前hitのみ/ID全域lower_bound、入場中Publish、field owner分離/B解放、creation失敗/scene復帰loop防止、ctor個体限定/vtableheader/LoadStep R1/削除中provider維持を確認。
- 既存Map/hotkey、list20、repeat12、native scroll/arc/全ID順、style直接Show6scenario PASS。成功GPU表示を保証する試験ではない。nativeカタログ分類・FS/GPU・actor生成/削除は明示endpoint。
- linked全分岐/LDR/命令・定数境界/ABI/SP/VFP/領域重複/hash/しずえhook PASS。14frame owner対容量16、正常ELFと旧7配布版のELF/3gx不変。
- DB37name/5型の全member/ARM T=0/根拠comment、公式XML/全bytes/input/保存DB hash読戻しPASS。LOWの内部条件は未命名理由と契約を保持。

次の実機確認は、表示設定→かな検索／0x2100検索、前後page/単一tab、掴んで空き持ち物枠へ移動、B／閉じるボタン→同じchat復帰、指定複数slotの表示。今回版の実機確認前にmainへ入れない。
