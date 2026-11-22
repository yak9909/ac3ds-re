---
id: ACNL-F0780
aliases: []
title: "通常フィールドの全タブ退場7と地図同期復帰2は別命令の組合せで成立する"
summary: "命令7は有効タブmaskの退場だけ。通常フィールドでは地図0/部屋0を併用し、復帰2は状態18の0x01待ちから状態7の0x02待ちへ進む。"
date: "2026-11-22"
category: "ui"
build: "acnl_jpn_v15"
confidence: "MEDIUM"          # LOW / MEDIUM / HIGH
tool: "exports+codebytes"
addresses: [0x6d3f04, 0x6d6b88, 0x6d5da8, 0x6d6528, 0x6d6a98, 0x6d701c, 0x6d6f60, 0x6d67f0]
tags: ["menu", "map"]
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

同じ部屋で通常フィールドが静止している条件では、地図0・部屋0・タブ7で退場し、後でタブ2により現在条件の地図/部屋とタブを再生成できる。全UIを無条件に原状復元する単命令ではない。MEDIUM（命令producer/consumer・out/in完了の複数静的経路）。

## 根拠

- 0x949D24の消費0x6D3F04は先に11へ戻す。7→0x6D6A98、enter0x6D6B88。
- enterは+6578の11有効bitを+6580へOR、0x6D5DA8でoutを開始する。
- 0x6D6528はアニメ完了でpane/ボタンを片付け、+6578 &= ~mask、+6580=0。0x6D6AB8はBsMenuTab_TabSelectUpdateへのstate変更callsite。
- 退場完了は命令0x949D24/25/29が11/2/2、タブcalc=0x6D474C/adjustor0、+6578/+6580=0、manager+484/+488=0を合わせて確認する。manager+56が0ならタブ+6416も0となり0x6D7F58の命令消費・calc更新が止まる（転送は0x6D35C4〜0x6D35D4）。背景・手カーソル・+492・+504の退場とメニューリスト空はこの判定に含まれない。
- 地図0x949D25=0は0x6D1428→BsMenuMgr_MapOutByKind（0x6D0B54）。部屋0x949D29=0は0x6D1E14→0x2257E8。各々ゲートと非同期破棄がある。
- 0x6D1E14はsub_565794()!=0かつmanager+57==1が入口の条件。命令0の分岐は+488!=0かつbyte_949D34!=0を待つため、生成直後などのbyte_949D34==0では一時保留され得る。1の書き手は0x31630C〜0x316310・0x326D20〜0x326D30、0の書き手は0x6D156C・0x6D20E4・0x6D3560。別の部屋条件分岐による命令上書き/消費とは区別する。
- 2→状態18 enter0x6D701C（地図1/部屋1）→calc0x6D6F60（0x01待ち）→状態7 enter0x6D6AC4（タブin）→calc0x6D67F0（アニメと0x02待ち、0x20解除、BsMenuTab_TabSelectUpdateへ）。
- 地図既存かつ部屋なしなら0x6D1428の命令1は新規inを出さない。0x01なしで18へ重ねれば止まり得る。
- ゲームの0x1A0F80はmap0/other0/chat等へ0x20/tab0、待ち0x1A0F28は実体なしとリスト空を待つ。0x6D4E5Cの通常menu-outはback退場とリスト空の後18へ。
- 今回の追加根拠は_local/evidence/164/revision-evidence.json（export命令列とxref）。
- _local/evidence/164/selected_functions.txt・xrefs.tsv。F0771/F0772の低位契約と一致。詳しい条件はtopics/acnl/bottom-screen-widgets.md §2〜5。

## 反証条件・未確認点

特殊部屋では命令2が18→7を通らない。退場前の任意のタブmaskやチャット入力まで同一に復元する保証はない。全場面の実測なし。
