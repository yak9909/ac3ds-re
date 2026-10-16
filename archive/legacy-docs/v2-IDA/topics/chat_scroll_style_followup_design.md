# チャット一覧の座標とスタイル画面への退場待ちを再修正

記録: IDA-gpt-6-T007 / IDA-gpt-6-F005、GPT-6、2026-10-12。PC検証済み、修正版実機未確認。

## T008の実機報告・訂正

利用者はfix2のリスト修復を実機確認、hairは未修復と報告した。HHD自身が退場/待機を所有するため、下記のコマンド側chat退場/親・keyboard消滅待ちの要件はstyleへ適用しない。native lifetimeの観察事実は維持し、旧「早期Show不具合」解釈を撤回する。現行は[HHD直接呼出し](chat_style_direct_design.md)。旧設計・試験は来歴として残す。

## 対象と訂正

利用者が実機でITEMNAME検索とcommand `list`のスクロールバー不動、`hair`等の画面未表示・操作不能を報告した。T005/T006のPC試験はnative座標変換をidentity endpointへ置換しており、その成立を実機へ一般化できなかった。背景入力遮断、検索の連続取得/B終了、command list決定後の挿入、time窓復帰、arc poolと全ID順は保持する。

### Controllerに必要なのは画素座標

- producer: `sead_CtrController_UpdateFromDevice 0x540870` がHIDのunsigned16画素位置をfloat化し、`SetPointerState 0x542D78` がController+276/+280へ格納する。`UpdateEdges 0x542E88` が整数座標+20/+24も作る。
- consumer: `Layout_TransformTouchPixelsToLocal 0x74F3FC` はviewport矩形`0x73BAC0`に従い中央移動・Y反転を行い、layout inverse matrixを通す。pane判定`0x4BE2A4`はmatrix inverse `0x148A64`、point transform `0x148CB0`、local rect `0x73B43C`を使う。
- `Touch_UpdateState 0x1B7874`のTouchState+32/+36は既に中央移動/Y反転した別表現。これをControllerへ渡すT005実装は二重変換になり、native hit-testが外れる。F004 getter注記「同じ中心座標」は撤回する。
- `sead_Controller_Calc 0x53CDC4`の先頭LDRとvtable+24へのBLXで、Controller+0はvtableだと照合できる。T005の+0 touch-bit上書きも除去する。touch holdは+272。

`UpdateChatList`はvt[4]実行中だけControllerの{4,8,16,272,276,280}へtouch edge/valid/holdと未変換画素を渡す。vtableは触らず、非touch bit・Controller全284Bとnative TouchState40Bを元へ戻す。

### hair/styleの引継ぎ

- `ChatWindow_ConsumeInputResult 0x193764`の取消結果1がkeyboard退場へ進む。`RequestKeyboardClose 0x193988`はchild+0xDCとlive keyboardを確認してchild vtable+68へ渡す。
- `WaitKeyboardGone 0x1938D0`は`0x94A654`が消えるまで親を破棄しない。shared-input bindingが外れる時点と、普通chatのowner `*(0x949D4C)+0x1EC`が消える時点は別である。
- AfterCloseはNormalChatOpen=falseだけで起動せず、親chatとkeyboard両方の消滅・field復帰を待つ。既存のnative取消要求/owner復帰を使う。
- HHDのCopy/Entering段階でもBを受ける。起動時保持B・pluginメニューを閉じたBの持越しは抑える。Copy中のfield退場待ちは180frameを超えたら失敗へ進み、次frameで一時arc/clone/field ownerを解放し、通知はメニュー側で一度だけ出す。

これらは静的なlifetime契約と旧版CPU再現で確認した不具合であり、利用者実機でのhair未表示原因をすべて確定したものではない。HHD画面の成功描画・GPU・実タイミングは未確認。メニュー直接起動の可否は任意質問への回答待ち。allocatorのTLS/lockは調査のみで変更しない。

## 独立照合・DB反映

- 対象: JPN無印更新code SHA `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`、ARM32LE/imagebase0/対象T=0。producerとconsumerの独立ARM経路・既存入力資料/sourceを照合しMEDIUM。CPU fixtureを実機証拠へ昇格しない。
- 主DBへ16rename/17prototype、point/int/rect/matrix/controller prefix/flagsの7型、25concept comment、7struct operandを保存・読戻し・close。既存`sead_Controller_UpdateEdges`実名と旧帰属/RTTI/旧patch bytesは保持。Controller型は284Bの部分prefixであり全SDK型ではない。
- 公式XMLは44210functions/33019symbols。全bytes・hashとF005の23function/2global comment、16名/7型のsize/member offset、T=0を読戻す。Exporterが省略するprototype/行列の多次元表現はDB直接読戻しを併記する。
- 未確定: `0x5CDAE4`が読むmanager+16/+4012のゲーム内意味、full arrow/binding型。見た目だけのrenameはしない。owner/writerを追うのが次の検証。

## 検証・配布

- T006旧版で元viewport/matrix/pane矩形/hit-testを実行するとscroll top0とvtable一時書換4回を再現。新版はtop8、drag/track/逆向き/端/release・vtable変更0・全入力復元PASS。LayoutCalcのmatrix publicationは明示endpoint。
- 実ChatBoundの部分解除では旧版が親/kbd存続中にShow、新版は両方0でShow。旧Copy中B不成立/181frame無限待機を再現、新版B/timeout/一度の通知/資源返却/native field復帰PASS。HHDの成功GPU buildは対象外。
- 一覧20case/連続取得12case/Map/hotkey/arc/全ID順、4330parser・23anchor・14CPP、linked570function/35669instruction/6622direct branch/3335PC reference/ABI/SP/VFP/領域/hash PASS。
- 隔離成果物: `artifacts/plugins/gohan_chat_scroll_style_fix2/gohan.3gx`、SHA `e2afb75ae0d8c3ce9a95e82a36a2cd865c063cc739ea771c264533f90c5adf2e`。ELF/32source hash/保存commitは同manifest。正常・全旧配布成果物を保持。
- 根拠: `work/evidence/gohan_chat_scroll_style_followup/`、ログ`work/logs/gohan_chat_scroll_style_followup_*`。ソースは独立gohan作業枝へ、解析はIDA枝へ最後一括保存。実機/SD/mainは操作しない。

利用者の次の確認: 両一覧のバーdrag/track touchと背景入力遮断、`hair/style/eyes`の表示/B閉鎖/再起動、失敗時の下画面復帰。未確認変更はmainへ入れない。
