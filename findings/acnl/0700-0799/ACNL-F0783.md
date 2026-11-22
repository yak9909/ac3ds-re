---
id: ACNL-F0783
aliases: []
title: "単一タブ退場の更新0x6D5110はアニメ進行と後片付けを行い地図復帰を開始しない"
summary: "0x6D5110(tabs,index) は対象なしまたは退場後の後片付け完了で1、アニメ進行中は更新して0を返す。stock の唯一の直接呼出元は index10 の back であり、地図同期状態への遷移は呼出元0x6D4E5Cが行う。"
date: 2026-11-22
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: exports+codebytes
addresses: [0x006D5110, 0x006D4E5C, 0x006D4EE8]
tags: ["menu", "layout"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6.1-sol
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

0x006D5110 に `BsMenuTab_UpdateSingleExit`、prototype `int __fastcall(void *tabs, int index)` を付ける。R0 は生存中の BsMenuTab 先頭、R1 はタブ index、戻り R0 は32bitの0/1。stock の直接呼出元 0x006D4E5C は index=10（back）だけを渡す。

確度 MEDIUM。更新本体、退場アニメを準備する enter 0x006D4EE8、完了後に遷移する caller の独立した静的根拠が一致する。実機追試はない。

## 根拠

一次資料は export/all_functions.txt を rg で検索した ARM と疑似C、および xrefs.tsv。採録は _local/evidence/167/selected_functions.txt と xrefs.txt。サイズ・配列位置の計算は calculations.json。export の symbols_commit は 4914ab98f271092df116b05c38a6183939b88b16。過去コメントは根拠に数えない。

- 0x6D5114/0x6D5120 は R0/R1 を tabs/index として保存する。0x6D5124〜0x6D5134 は tabs+6578 の16bit表示maskを読み、(1 << index) が無ければ即1。配列参照・アニメ更新・フラグ補正も省く。この1は「対象がない」を含む。
- 0x6D5138〜0x6D5144 は tabs+1012 の共通 UiAnim の完了を検査する。未完了なら 0x6D51D8 の UiAnim_Step と 0x6D51E4 の Layout 更新（tabs+640）を行って0。
- 完了時は 0x6D5160 で Layout+640 / UiAnim+1012 / group[index]（tabs+6432、stride4）を渡して binding を外す。0x6D5178 は button[index]（tabs+1948、stride388）の sub_2E016C を呼ぶ。0x6D5184〜0x6D5190 は pane[index]（tabs+6476、stride4）の+183 bit0を消す。
- 0x6D5194〜0x6D51C8 は表示maskから対象bitを除去し、除去後に back bit10 が無ければ tabs+6576 のbit1を立て、残っていれば消す。その後1。+6580の一括退場maskはここでは変更しない。
- enter 0x6D4EE8 は vc_MENU_FLAGS の0x20を立て、back が有効なら group[10] を共通アニメへ bind しフレーム0へ戻す。ボタン側の状態と tabs+6422、tabs+6576 bit0も準備する。0x6D5110 自身はアニメを開始しない。
- caller BsMenuTab_MenuOutUpdate 0x6D4E5C は戻り1の後も Menu_IsIdleAndEmpty 0x6D1074 を待つ。その後 byte_949D88=0、背景leave、地図同期状態へ進む。これらは0x6D5110の副作用ではない。caller の既存型 `void __fastcall(void *tabs)` は維持する。

### 外部からの呼出条件・副作用

外部から更新関数として呼べる契約は、初期化済みで資源・group・pane・buttonが生存する同じ BsMenuTab に対し、index10 の退場アニメを enter 相当のゲーム処理で既に開始した場合まで。対象bitがあるのに未準備の共通アニメを渡すと、別アニメの完了を見て片付ける恐れがある。null や範囲の検査はない。構成上の index は0〜10だが、10以外の外部利用は未検証。

ゲーム自身のタブ更新・Layout更新と同じ直列の UI 更新文脈で呼ぶ。同じフレームに stock の calc と外部側が重ねて呼ぶと共通アニメを余分に進めるため、更新主体を一つにする必要がある。描画や破棄、別アニメの開始と競合する別スレッド呼出は根拠がない。具体的なOSスレッドIDは未測定であり、この条件は共有可変状態と呼出経路からの判断。

1を返してもメニューリスト空・部屋actor消滅・背景退場・地図復帰は保証しない。0x6D5110だけには地図再生成も状態遷移も無いため、その副作用境界は確定できる。ただし地図復帰を省く外部経路全体の成立は、この関数の返値だけでは証明できない。

## 反証条件・未確認点

実機での入力連打、破棄中、別アニメ併走、index10以外の呼出は未確認。export の直接xref以外の動的・間接呼出は網羅しない。静止したフレームで1が返ることとゲーム全体の退場完了を同一視しない。
