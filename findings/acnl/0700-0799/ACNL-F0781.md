---
id: ACNL-F0781
aliases: []
title: "通常チャットはkeyboardと親actorの退場完了を別々に通知する"
summary: "チャット0x193764は終了要求0x20を処理し、keyboard Releaseでliveポインタが0、その後親Releaseでmanager+492が0になる。タブ命令7だけではチャットは退場しない。"
date: "2026-11-22"
category: "ui"
build: "acnl_jpn_v15"
confidence: "MEDIUM"          # LOW / MEDIUM / HIGH
tool: "exports+codebytes"
addresses: [0x193764, 0x193988, 0x1938d0, 0x193c3c, 0x57f944, 0x6d5510, 0x57cc9c, 0x57ca00]
tags: ["chat", "keyboard", "menu"]
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

通常チャットの完了は入力bindingの解除だけでは決まらず、子keyboard・親chat・メニューリスト・タブ状態に分かれる。MEDIUM（親の要求/待ち、子と親のRelease、およびvtable/state表を独立照合）。

## 根拠

- LoadStep0x193A40でmanager+492を公開、0x193890で子screen0x23Eを生成。
- 0x193764が0x20を読む。Out enter0x193988が子+220のvt+68へ閉じる要求。
- keyboard Out0x57CF04はアニメ完了後破棄要求。Release0x57F944は0x94A654=0、MENU_FLAGS &=0xFFFFFFC7。
- 親0x1938D0はlive0を待ってActor_RequestDestroy、0x193C3Cがmanager+492=0。
- タブ0x6D5510はbyte_949D3Bを見てChatReturn0x6D5FB0へ。そこではoutとメニュー空を待つ。無条件にTabSelectを待つだけではこの経路を代替しない。
- チャット再生成はtab index6→0x6D6214/0x6D72C0→menu5→screen0x23F。古いactorの再利用ではない。
- 元code.bin状態record0x851430はenter0x57CC9C/update0x57CA00。enterが0x10を立て、update完了が0xC0を立てる。親0x193850は0x80を待つ。
- したがって既存F008関数コメントの「normal chatに0x10を要求してはいけない」を、update単独からの結論としては採用しない。0x10の生産元はenterにある。
- _local/evidence/164/selected_functions.txt・tables.json（SHA256はmeta/builds.tomlと一致）。topics/acnl/bottom-screen-widgets.md §4。

## 反証条件・未確認点

入力内容・選択状態を含めた完全復帰、friend-chat別寿命、実機の連打時順序は未確認。F0423等の過去実測を今回の実測としては数えない。
