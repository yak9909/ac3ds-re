---
id: ACNL-F0425
aliases:
- IDA-gpt-6-T008
title: F005のHHD引継ぎ要件を訂正（2026-10-12）
summary: '利用者実機報告: fix2/SHAe2afb75a...のリストは修復、hairは未修復。HHD自身が退場/待機を所有し、コマンドは直接呼ぶよう指定。native chat lifetimeの観察は変更しないが、「style起動前に親/kbd消滅必須」「早期Showが不具合」の推論を撤回する。F005/T007のCPU試験を実機修復の証拠としない。'
date: '2026-10-12'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:71-75
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-T008: F005のHHD引継ぎ要件を訂正（2026-10-12）

- 利用者実機報告: fix2/SHAe2afb75a...のリストは修復、hairは未修復。HHD自身が退場/待機を所有し、コマンドは直接呼ぶよう指定。native chat lifetimeの観察は変更しないが、「style起動前に親/kbd消滅必須」「早期Showが不具合」の推論を撤回する。F005/T007のCPU試験を実機修復の証拠としない。
- Sourceの既存HhdScreen::Show→HoldField/Copyの所有経路に従い、4aliasはTickで直接Show、CloseChat/AfterCloseはTimeMenuのみへ。主DB3注記へ訂正追記/save/close/XML読戻し、native code/names/typesは維持。詳細chat_style_direct_design.md、根拠gohan_chat_style_direct。新呼出し版の成功GPU表示/実機timingは未確認。

