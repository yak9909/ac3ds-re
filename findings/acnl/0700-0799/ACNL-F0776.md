---
id: ACNL-F0776
aliases: []
title: "CommonScrollBarの開始フレームのドラッグ抑止フラグ"
summary: "CommonScrollBar+0x6FBは1の間、そのUpdate内の通常ドラッグ更新を抑止し、次のUpdate冒頭で消される。drag_blocked_this_frameとして1バイト整数で定義する。"
date: 2026-11-21
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: export-static
addresses: [0x002990C8, 0x00298664, 0x00299C34]
tags: []
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

CommonScrollBar+0x6FBは unsigned __int8 drag_blocked_this_frame。
1の間は通常ドラッグ更新を抑止する。書き込み側、消費側、更新寿命の独立した静的根拠によりMEDIUM。実測なし。ACNL-F0774の未命名部分を細分化する補足であり既存結論は変更しない。

## 根拠

- 書き出し functions/00200000/002990C8_sub_2990C8.txt: 0x2990D0 MOV R7,#1、0x2990E0 STRB R7,[R0,#0x6FB]。関数入口から条件分岐なしで1を書く。
- 同関数は0x2990F4でknob_paneを取得、0x299114で原点を変換。0x299118..130で入力点のyとつまみ原点yの差をS0へ置き、vt+0x14へ渡す。0x29913Cでdrag_active=1、0x299140でsub_299864(this,1)、0x299144で+0x718を0にする。通常更新とは別の初期位置処理を伴う開始経路である。
- 0x298674..84: LDRB/CMPで+0x6FA==0または+0x6FB==1なら復帰へ分岐し、座標取得・vt+0x10の更新を実行しない。+0x6FBは終了処理ではなく当該更新の抑止である。
- 0x299C54..5C: LDRB/CMP #1/STRBEQで1を0へ戻す。これは入力処理前。0x299D64のvt+0xC呼出し後、0x299D6CでUpdateDragを呼ぶ。この間に開始経路が1を書けば、そのUpdateの通常更新だけを抑止できる。
- UpdateTouchの0x29828C..90は押下0x8000を検査。三つのpaneに当たらず+0x784のpaneに当たる場合、0x298364..374でvt+8へ点を渡す。一方、つまみ側の開始0x2982F8はdrag_activeだけを立て+0x6FBを書かない。全てのドラッグ開始を示す名前にはしない。
- xrefs.tsvの2990C8項目には定数参照のみがあり、直接callerはない。vt+8と2990C8の対応はこの資料だけでは確定しないため、中立の名前を採用した。
- all_functions.txtをripgrepで検索し、2990C8の書込、299C34のクリア、299FE8の初期化のほか、派生候補31C7E0にも同オフセットへの1書込を確認。ただし全関数の同オフセットは別型も含み、同じ実体とは断定しない。
- 旧版Sources/Gui/GameList.cpp 364..378も+1787==1ならドラッグ半速処理をせず元処理に任せる。これは命令読解の補助資料でありゲーム動作の実測ではない。

## 反証条件・未確認点

実機未検証。トラック押下の仮想呼出し対応、派生クラスでの同フラグの意味、全書込元の網羅は未確認。初期位置処理の直後に通常ドラッグ位置計算を重ねない効果は静的に分かるが、作者の意図や具体的な表示不具合は断定しない。
「このフレーム」はCommonScrollBar_Updateの呼出し単位であり、同一描画フレームで複数回Updateが呼ばれる場合は描画フレーム全体の保証ではない。
