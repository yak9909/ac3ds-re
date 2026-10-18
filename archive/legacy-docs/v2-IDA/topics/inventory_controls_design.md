# リスト再タッチ・持ち物操作 / IDA-gpt-6-F010・T013

最新のT014実機訂正（checklist未表示、pocket再入場trash/priority、trash自身drag/crash、青保持・A取得後旧行残留、manualcloset3cheat削除）は [F012/T015](inventory_ui_fix_design.md) を正とする。下記F011のSetTouchによる色保持と旧fixtureの成功範囲は訂正された。

## 2026-10-13 実機報告による訂正 / IDA-gpt-6-F011・T014（GPT-6）

- T013の実機報告: 手紙widgetが残る、trashクリック/pocketクリックでcrash、追加選択肢のUIが一括toggle、selected行が2tap必要、再tapで選択色が消える。T013PC fixtureは文字列・選択窓・決定入力の一部をmockしており、実機成功の根拠ではなかった。
- 利用者の契約は「現在selectedの項目へ1tapで実行」。未選択項目はfocusだけ。DPad/プログラムで選んだ項目も1tap。Native WaitCalcは旧rowをdeselectし、ClearDecidedでtouch/selectを0へ戻す。GameListは事前selectedとdecidedを読み、native完了後node vt+28で選択色を戻し+217をenable。候補barも現在m_selだけで判定する。
- Vapecord SettingsButton/citemsettingsは4項目の個別設定。ITEM_CHECKBOX_LIST/bitmaskへ訂正し、Applyと保持/復元/正規化にもcheckboxlistを加える。元row/cancelを保存、実capacityと6の小さい方が上限。ベル袋以外には返済を出さず、決定時にもそのbitを確認する。
- CTRPF SetHookContextInTLSはtls[15]をnested call後に復元しない。旧CommitはCopyOptionを呼んだ後GetCurrentを取り直し、COMMITの1引数でCOPYを呼ぶ。旧ELFで誤ったOriginal targetを再現（fixtureではその時点でfaultにはならず、実機crashの同一性は未確認）。全callbackは入口ctxを保持する。native RowCtor/WordFix65/Appendを実行し、元action42/cancel41/UTF16ラベルを照合した。
- SetPanesの第2欄はnwlyt Group。LayoutはAddNodeがnode+28へ設定する。trashがLayoutをGroupとして渡した誤りをnullGroupへ訂正する。手紙Layoutのroot+632は確かにPane（FindPane/teardown RemoveChildを独立照合）；alphaだけでは子の非表示を保証しないため、visible flagを使いOFFで戻す。実GPUの確認は利用者の実機確認が必要。
- InteriorChoiceは背景を止めても私有窓へ完全なTouchState40を渡し、呼出し後にゲームの値を戻す。開いた指は離すまで新しい入力にしない。private Arc/GPU/font payloadはPC fixtureのendpoint、実Touch/BAC/Word/option/checkbox状態はARMで検証する。

根拠: `work/evidence/gohan_inventory_fix/static.json`、`db_expected.json`、`old/old_nested_failure.json`、native/scroll/linked/XML各report。確度MEDIUM（原JPN ARM＋caller/vtable/CTRPF/Vapecord＋PC照合）。HIGHへの昇格は新3gxの実機操作/結果とSHAの記録後。正常・旧12配布版を保持し、作業枝へ最後一括保存、main/SD/実機を操作しない。

担当 GPT-6、2026-10-13。対象 JPN無印更新版、PCで照合し実機では未確認。原入力hash/セグメントはF009と同一。主DBacnl_v2はrootが単独所有する。

## 入力

- GameListのselected行はnative WaitCalcがnode+217を0へして再タッチを禁止する。所有する行だけ再enableし、初tapはfocus、同じfocusへ再tapはaction。AはButtonActionNode_StartDecideで決定音と2本のアニメを再生する。native listを全体patchしない。
- 漢字候補はtouchfocusとApply/Enterを分ける。キーでの候補切替は従来通り。候補のfocus/決定音はゲームスレッドへ要求する。
- scrollbarのknob pressとtrack pressはCommonScrollBar_UpdateTouchの別経路。owned GameListのUpdateDragだけ初期localpointから変位0.5倍へ変換し、native vt+16へ渡す。毎tap初期値を取り直す。track click/解放/他のnative scrollbarは元処理。利用者は時間補間を却下し1回drag距離半分を指定した。
- 検索closetのDPadは初回即時、200msからrepeat、その後1500msかけinterval200→50msへ減らす。メニュースレッドで実時間/方向を読み、page要求をゲームスレッドへ送る。押下中native DPadを遮断して二重操作を避ける。native item drag・touch pageボタンは維持。

## 持ち物

- Vapecordは複製/ラッピング/収納/ローン返済を追加する。gohanでは単一checkboxで有効化し、既存の選択肢とcancelを保存しつつnative6行容量内で追加する。builderのscope内helperだけ拡張し、全体text IDやregisterに依存するtail hookを使わない。raw itemの複製は空き枠のみへ。返済はnative暗号化/チェックサム、収納は現在playerの実180枠を使う。slotが変わった場合や空き/残債不足では書き換えない。
- 手紙icon置換は通常BsMenuItemだけに限定。家具listと同じarc/layout/on/off/ok/loopアニメを使い、native letterbuttonのpaneを隠す。drag完了はnative DragControlのsource/targetと後片付けを使う。クリックは同じItemSelectWindowで全削除/やめるを出し、窓が所有している間の背景操作を止める。
- 資源の寿命、disabled時のletterbutton復元、退場中の解放とGPU登録の3frame猶予、6行容量/元cancel/壁掛けaction42保持、保存品/没icon不変を検証する。正常・全旧配布版は保持、専用build/output。commit/pushは全作業完了後一括、main/SD/実機には触れない。

## 根拠と反証

- ベルのcategoryは2。Item_GetParamCategoryと財布回収0x2BFB5C/Vapecord enumを照合し、41/42案は却下。ベルでは返済を先に加え、他の品では複製/包装/収納順。返済0x6BD218と返済可否0x76D888はplayer+0x6B94、利息/郵便賞品0x62FD58はplayer+0x6B8C、native storage0x71A0B8はplayer+0x92F0。全体save構造の注記を無補正で使わず、Vapecordの0xA0差を独立照合した。
- UiAnimの既存型は28Bの部分型。実際に確保する40Bと混ぜず、F010は40Bのopaque型を定義して既存型を上書きしない。DragIconGroup320B/PartsDragIconNode304B/descriptor32B/row172B/system prefix220B/control prefix264Bを型読戻しで照合。group登録はcontrol+228へgroup+12、nodeはmain listへ移る（原ARM0x29BC24）。
native decompileはwork/evidence/gohan_inventory_controls。原code.binのARMと既存source/RTTI/caller/Vapecord地域表を独立照合する。MEDIUM=複数静的、LOWの新しい意味はrenameしない。hardwareの描画/音/タイミング確認で異なる結果が出れば本設計を訂正する。
