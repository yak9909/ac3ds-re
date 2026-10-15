---
id: ACNL-F0426
aliases:
- IDA-gpt-6-F005
title: Controller画素座標/vtableとchat画面引継ぎ（2026-10-12）
summary: GPT-6 / IDA（idalib）、MEDIUM。更新SHA/ARM/imagebase/Tを確認しproducer540870/542D78/542E88とconsumer74F3FC/73BAC0/Matrix/Paneの独立ARM経路・旧input資料/sourceで照合。Controller+276/+280は画素float、TouchState+32/+36とは異なる。F004中心座標注記は撤回。53CDC4のvtable+24 BLXから+0はvtable、t
date: '2026-10-12'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags:
- chat
- rtti
supersedes: []
source: IDA:work/FINDINGS.md:76-82
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-F005: Controller画素座標/vtableとchat画面引継ぎ（2026-10-12）

- GPT-6 / IDA（idalib）、MEDIUM。更新SHA/ARM/imagebase/Tを確認しproducer540870/542D78/542E88とconsumer74F3FC/73BAC0/Matrix/Paneの独立ARM経路・旧input資料/sourceで照合。Controller+276/+280は画素float、TouchState+32/+36とは異なる。F004中心座標注記は撤回。53CDC4のvtable+24 BLXから+0はvtable、touch holdは+272。元幾何で旧T006 top0/vtable書換4を再現、新版top8/vtable変更0と全bytes復元PASS。
- ChatBound解除は親chat/kbd退場完了より早い。193764/193988/1938D0/1939B8と848BE0 descriptorから退場lifetimeを照合。style引継ぎはmenu-manager+0x1ECと94A654両方0を待つ。旧早期Show/Copy中B不成立/181frame待機をCPU再現、新版B/timeout/通知一度/field復帰PASS。実機未表示の原因全体・成功HHD GPU表示は未確定。
- 16rename/17prototype、point/int/rect/mtx/controller部分prefix/flags計7型、25comment/7struct operandを主DBsave/readback/close。旧実名/帰属/RTTI/patch bytes保持。公式XML44210functions/33019symbols/全bytes/hashとF005名/型/23function・2global comment/T=0を読戻す。根拠gohan_chat_scroll_style_followup、設計chat_scroll_style_followup_design.md。
- 反証条件: 正規input producerが中心変換済みfloatを供給する経路、親/kbd存続中でも競合しない画面handoffの実測、native geometryで新版のhit miss。5CDAE4の+16/+4012 gate意味とfull arrow/binding型は未確定、writer追跡まで推測renameしない。HIGHへは対応新版の実機観測が必要。

