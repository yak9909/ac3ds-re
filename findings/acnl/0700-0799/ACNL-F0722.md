---
id: ACNL-F0722
aliases: []
title: "タッチ遮断は画面ロックではなく共有入力の変更である"
summary: "タッチはpointer validとheld内pointer bitの二系統で読まれる。sead入力での除去は共有TouchState・スクロール・全登録Wrapperと入力idle判定に及び、下画面UIだけを選択するロックではない。"
date: 2026-10-19
category: input
build: acnl_jpn_v15
confidence: MEDIUM
tool: "関数書き出し / codebytes / 元ARMのUnicorn実行 / IDA型反映"
addresses: [0x0053CDC4, 0x00542D78, 0x005475D4, 0x00304A44, 0x001B7874, 0x001B7A18, 0x0029915C, 0x00298664]
tags: [touch, button, sead]
supersedes: [ACNL-F0377]
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

ACNL-F0377のゲーム側の機構を再解析で確認し、対象範囲を訂正した。
入力層には「下画面ロック」というゲームの欄はない。タッチの有効性とheld内pointer bitの両方を落とす必要があり、その変更は共有入力を読む機構全体に及ぶ。
MEDIUM。producer、直接consumer、Wrapperとidle判定という独立した静的経路を照合。元ARMの人工入力実行でも二重表現を確認。今回の実機検証はない。

## 根拠

- `sead_CtrController_UpdateFromDevice` は装置 `+0x15D4` のuint16 X/Yと `+0x15D8` の接触byteを読み、`0x00540B1C` で `SetPointerState(controller, valid, 1, pixels)` を呼ぶ。
- `SetPointerState` は `0x00542E08..0x00542E20` で `controller+0x10` bit0を更新し、`0x00542E24..0x00542E48` で `controller+0x108` のbit番号を読み、`valid & held` に従って `+0x110` の該当bitも更新する。
- CtrControllerのctor経路はpointer bit番号15。CPU fixtureでも `valid=1, held=1, pixels=(87,122)` で `flags=1, held=0x8000` を得た。flagsだけ0にしてもheld bitは残る。
- pointerだけを落とすときは、現在heldと保存された旧heldのpointer bit、現在validと保存された旧validの双方を整合させる必要がある。ボタン全体の遮断とは別に扱えるが、旧状態を残すと解放edgeが出る（ACNL-F0721）。
- Wrapper `0x005476A8..0x005476BC` はsourceのvalidと画素座標をSetPointerStateに渡す。別に `0x00547620..0x0054764C` でheldを写す。BsMenuMgrの表 `0x0084B4FC` は19要素で15を含まず、設定処理 `0x005475A8..0x005475CC` により同Wrapperのpointer bit番号は-1になる。それでもsourceのpointer validはコピーされる。
- 共有入力getter `vc_CONTROLLERINPUTCHECK` (`0x00304A44`) は管理体 `+0xD8` の先頭controller `+0x110` を読む（`0x00304A5C..0x00304A80`）。menu Wrapperだけを読んでいるわけではない。
- `Touch_UpdateState` (`0x001B7874`) はこのgetterに `0x8000` を渡し、`0x001B78CC..0x001B78E4` で共有TouchStateのheld/changedを更新する。座標とpressed/releasedも個別getterから読む。呼出し元 `0x001B6C40` は共有領域 `0x00ACF6E0` を渡す。
- `CommonScrollBar_SelectInputMode` は現在held `0x8000` またはTouchStateの前回held `+0x1A` によりtouchモードに入る（`0x00299164..0x00299198`）。現在値の遮断開始後も、前回状態が一時的に残る。
- `Touch_IsDragHoldReady` は現在held `0x8000` とTouchStateの継続フレーム `+0x0E>=3` を検査する（`0x001B7A20..0x001B7A38`）。座標を固定するだけではドラッグを止められない。
- `CommonScrollBar_UpdateDrag` はこの判定を通った後、controllerのfloat画素座標を取得しレイアウト座標へ変換する（`0x002986B4..0x002986D8`）。
- Calcは `0x0053CE54` で無入力判定slotを呼び、`+0x10C` を更新する。CtrControllerのslot `+0x1C=0x005429EC` はheld、pointer valid、軸値を検査する。したがってタッチ除去は入力idleの判定にも影響し得る。
- これらの処理には表示先画面IDの検査や下画面描画の停止は無い。描画を暗くすることと入力の除去は別処理である。
- 加工前の装置キャッシュ `CtrHidDevice+0x15D4` 自体はCalc内で書き換えられない。装置更新はcontrollerより先（ACNL-F0721）。HIDを独立に読む利用者やOSへの非影響は、その読取り位置を別途確認する必要がある。

証拠: `_local/evidence/103/exports/` の各先頭アドレスの書き出し、`manifest.json`、`native_replay.json`。

## 訂正

- ACNL-F0377の「下画面ロック」は旧製品の制御方針を表す語であり、ゲームに存在する画面別ロックではない。
- 旧記録のスライドパッドを残す方針は、全入力遮断の証拠にはならない。heldを0にしても軸floatは別欄で残る。
- 旧ケーブの適用・撤去、利用者の成功報告、暗幕の一本化、ビルド検査結果は今回の一次証拠では再確認できず、ゲーム機構の確度に加算しない。
- `0x009B7010` は旧製品が使った作業領域という手がかりであり、ゲーム本来の入力ロック変数として命名・型付けしない。

## 反証条件・未確認点

- 下画面UI専用とする解釈は、共有controllerの直接読取り・idle判定が存在するため成立しない。一方、上画面の具体的な機能や全場面への影響の列挙までは未確認。
- 全scene/全raw HID読取りを調べたわけではない。ここで確認した共有経路の外まで「全部止まる」とは主張しない。
- 既存TouchStateのchanged/履歴、押し始め座標、独自ドラッグ状態の扱いと、遮断中・解除直後の実画面での挙動は実機未確認。
