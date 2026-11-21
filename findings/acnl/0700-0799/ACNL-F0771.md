---
id: ACNL-F0771
aliases: []
title: "MenuFlags 下位三ビットは地図側の入場開始・完了・退場完了を通知し、状態7は0x02を待つ"
summary: "0x01=地図側入場開始、0x02=入場完了、0x04=退場完了または対象なし。状態18は0x01、状態7は0x02を待つ。F0756のbit2という記述はマスク0x02へ訂正する。"
date: "2026-11-21"
category: "ui"
build: "acnl_jpn_v15"
confidence: "MEDIUM"
tool: "exports"
addresses: [0x949D68, 0x2B2720, 0x2B266C, 0x6D0E30, 0x6D1428, 0x22556C, 0x225778, 0x326720, 0x6D67F0, 0x6D6F60, 0x6D701C, 0x6D6AC4, 0x6D4700]
tags: ["menu", "map", "layout"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: auto
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

MenuFlags の下位三ビットは地図側（地図を使わない部屋・manager+488 の補助画面も含む）の入退場通知である。
0x01=MapEnterStarted、0x02=MapEnterDone、0x04=MapOutDone とした。
0x04 はポインタ不存在そのものではなく「退場完了／対象なしとして完了扱い」の通知。
書き手と独立したタブ側待機先を照合したため MEDIUM。今回新たな実測はない。

F0756 の状態7 calc の「bit2確認」は誤記。0x6D6810 の ARM は TST R0,#2（ビット位置1、マスク0x02）。
同記録の命令バイト・状態表・関数名・状態切替機構に関する他の結論は変更しない。

## 根拠

書き出しは依頼指定の版。現在名は symbols と F0756 の表を使用。
全体索引・all_functions.txt に対する ripgrep から候補を絞った。
抽出・検算: _local/evidence/154/check_menu_flags.py。
候補一覧: _local/evidence/154/candidates.txt。
主要関数の命令列と疑似C: _local/evidence/154/selected_functions.txt。

|通知|立てる関数|消す関数|読む・待つ関数|
|---|---|---|---|
|0x01 入場開始|地図 In enter 0x2B2720（G_inout・地図リスト準備後）、地図を作らない部屋の代替通知 0x6D701C、命令2の部屋分岐 0x6D3F04|入場完了 0x2B266C、0x22556C、0x326720、0x6D1428 の代替完了、0x6D6AC4・0x6D78F4 の地図なし完了|状態18 calc 0x6D6F60 が非0を待ち状態7へ。0x22556C は0x01が無い時だけ0x02を補う|
|0x02 入場完了|地図 In update 0x2B266C（UiAnim_IsFinished後）、部屋側 0x22556C、0x326720、0x6D1428 の補助画面/地図不要分岐、0x6D6AC4・0x6D78F4 の地図なし分岐、0x1A07C8|地図 In enter 0x2B2720、0x6D701C の代替開始、退場/対象なし通知 0x6D0E30・0x225778・0x6D1428・0x6D3144・0x6D34AC・0x6D4CB4・0x6D6B18・0x6D6F90 など|状態7 calc 0x6D67F0（タブ入場アニメ完了も必要）、0x6D68A0 case5、0x6D783C。旧版 GameList.cpp の復帰待ちも0x02|
|0x04 退場完了/対象なし|地図解放 0x6D0E30（地図種別ごとの実体を解放してmanager+484=0）、部屋側解放 0x225778（+488=0）、manager初期化 0x6D3144、更新0x6D34AC、地図なし分岐0x6D1428・0x6D4CB4・0x6D6B18・0x6D6F90 など|開始0x2B2720・0x6D701C は0x04を落とす。0x02を立てる書き方は0x04を保存する|0x6D4700 はタブ退場完了かつ Menu_IsIdleAndEmpty かつ0x04で次へ。0x6D6214 BsMenuTab_ChatTabsOutUpdate も同様。Menu_PollOpen の要求ゲート、およびロード段 0x2F045C・0x315C8C にも0x04判定|

正確な更新マスク:
- 開始: (flags & ~7) | 1。
- 完了: (flags & ~3) | 2。0x04は保存する。
- 退場/対象なし: (flags & ~6) | 4。0x01は保存する。
従って全書き手で三ビットを厳密な排他値にしているわけではない。単独ビット・組合せ値のみから実体の有無を判定しない。

状態6 enter 0x6D4EE8 は0x20を立てる。calc 0x6D4E5C はボタン退場とメニュー空を待ち、状態18へ。
状態18 enter 0x6D701C は通常屋外なら地図命令1を出す。calc 0x6D6F60 が0x01を待ち状態7へ。
状態7 enter 0x6D6AC4 はタブ入場を開始し、manager+484が無い場合は0x02を補う。
calc 0x6D67F0 はタブ入場完了後0x02を待ち、0x20を消して入力を戻し、タブ選択0x6D474Cへ。
地図が既にあり+488が無い場合、0x6D1428 の命令1は入場を始めず命令だけ待機へ戻す。
この条件では0x01が新たに来ないので状態18は待ち続ける（F0466の既存実機観察と一致）。

## 反証条件・未確認点

- 全185関数を精読していない。低位マスクを持つ候補と依存先を確認した。別名ポインタ・演算結果経由の全書き手を網羅したとの主張ではない。
- 地図不要室やmanager+488にも同じ通知が使われるので、Mapという列挙名は地図側復帰系の略称。物理的な地図表示のみを表すものではない。
- 0x80・0x200など上位ビットの意味、F0113/F0115の停止値の因果は未確認。0x6D1428に0x200分岐も見えるが今回命名しない。
- 本記録はF0756のbit2記述のみ訂正し、その他を撤回しない。旧版製品の実装変更は扱わない。
