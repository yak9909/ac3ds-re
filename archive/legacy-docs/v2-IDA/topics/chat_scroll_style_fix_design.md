# リストscroll・スタイルarc・検索順の追加修正

記録: IDA-gpt-6-T005 / IDA-gpt-6-F004、GPT-6、2026-10-12。修正版は実機未確認。

## T007/F005による訂正

下記T005の「+0 held」「+276/+280 centered float」は誤り。+0はvtable、float pairは画素座標でありnative側が中央移動/Y反転する。T005試験のidentity geometry endpointが二重変換を隠していた。元viewport/matrix/hit-testでT006のscroll不動とvtable一時書換を再現し、修正した。旧記述・根拠は来歴として残す。現行契約とhair退場待ちの修正は[再修正設計](chat_scroll_style_followup_design.md)、根拠`work/evidence/gohan_chat_scroll_style_followup/`を参照。

## 原因と修正

- `CommonScrollBar_SelectInputMode 0x29915C` はControllerのtouch hold、`UpdateTouch 0x29823C` はpressed/released、`UpdateDrag 0x298664` はvalidなfloat座標を読む。行BAC用のTouchState40Bだけを渡したT004では不足。Controllerは`0x96F2EC`の管理体+208の個数と+216のtable経由。+0/+272 held、+4 pressed、+8 released、+16 bit0 pointer valid、+276/+280 centered float pairを一覧vt[4]の間だけ差し込み、7wordとTouchState40Bを全て復元する。chat list中/退場中の背景入力遮断は保持。
- ドラッグ開始はnative hit-testとedge、継続はholdが3frame以上、終了はreleaseによる行位置の丸め。`CommonScrollBar_ApplyDragPoint 0x299F7C` のpointはR1、deltaは次のvirtualへVFP s0。旧decompileはR1を省略していたため型と注記を訂正。row位置/境界/音/文字更新は既存native処理を使う。
- styleの「arcを読む領域が取れない」はFile Open後の大領域new失敗。常駐漢字変換arenaとnewlib heapを共有する。新たにheapを拡張せず、CTRPFが既に予約したpoolへ一時arcを置く。ゲームheapへコピー後・組立前取消・不正arc・hook失敗・組立失敗でpoolへ返す。保存先/arc形式は従来通り。CTRPF pool不足もエラーとして扱う。
- 検索は通常ROM名と補完名（fgobj等）を集めた後、ID昇順sort/uniqueしてからページ分割する。補完名を末尾別枠にしない。左の小さいID欄とA/touch決定/B終了は保持。

## 根拠と検証

- 更新日本語版code SHA `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`、ARM32LE/imagebase0、対象T=0。既存F041/F054とinput_block資料、native ARM、sourceの独立経路を照合。MEDIUM。主DBへ確認した関数名/型/コメントを保存し、公式XMLから読戻す。詳細 `work/evidence/gohan_chat_scroll_fix/static.json` / `db_changes.json`。
- `verify_scroll_style_fix.py` は元code.binのscroll更新・touch mode/edge・drag clamp・行位置計算・release/SetPosを実行する。GPU幾何/アニメ/音・SD・allocatorは明示endpoint。旧配布版でscroll不動/大領域new失敗/fgobj末尾を再現し、新版のdrag/track/逆向き/端/入力全bytes復元/保持指・GUI無効、pool解放、検索全ID順/重複/ページ境界を検査する。
- 前回20case（focus/決定/退場/背景遮断/time復帰）とMapEditor/hotkeyの回帰検査、prebuild/linked分岐・LDR・ABI・しずえ/hashも維持。成果物は隔離 `artifacts/plugins/gohan_chat_scroll_fix1/`。元正常ELF/旧配布版を保持、実機/SD/mainは操作しない。Gitは修正・検証終了後一括で作業枝に保存。
