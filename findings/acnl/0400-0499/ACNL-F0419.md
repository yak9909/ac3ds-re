---
id: ACNL-F0419
aliases:
- IDA-gpt-6-F011
title: 持ち物・trash・selected行の実機不具合訂正（2026-10-13）
summary: GPT-6/idalib、MEDIUM（原JPN ARM＋caller/RTTI/CTRPF/Vapecord＋PC、実機未確認）。CommitのnestedCopyはTLS[15]をCOPYへ変更し、旧GetCurrent再取得がCOMMIT引数でCOPYへ戻る。入口ctx保持で修正。script::WordFix65のnativeCtor/Appendを検証し、row172内word156/UTF16bufferを型に適用。
date: '2026-10-13'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags:
- inventory
supersedes: []
source: IDA:work/FINDINGS.md:24-29
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-F011: 持ち物・trash・selected行の実機不具合訂正（2026-10-13）

- GPT-6/idalib、MEDIUM（原JPN ARM＋caller/RTTI/CTRPF/Vapecord＋PC、実機未確認）。CommitのnestedCopyはTLS[15]をCOPYへ変更し、旧GetCurrent再取得がCOMMIT引数でCOPYへ戻る。入口ctx保持で修正。script::WordFix65のnativeCtor/Appendを検証し、row172内word156/UTF16bufferを型に適用。
- SetPanes第2欄はGroup、LayoutはAddNodeがnode+28へ設定。root+632はPaneでありalphaではなくvisibleでletter subtreeを隠す。ButtonActionNode_HitTestTouchはpixels→layout座標→pane inverse matrixで判定。native押下/離上→実Choice Openとnative窓/Arc/Layout/6node ctorが通過。
- Native listのClearDecidedはTouch/Selectを0へ戻す。現在selectedを基準としてselected行1tap実行・他行focus、cleanup後nativeSetTouchで色を戻す。Vapecordの追加4操作は個別checkboxmaskで編集/適用/保持。source/設計/反証条件はdocs/topics/inventory_controls_design.md、根拠work/evidence/gohan_inventory_fix（old wrong-target、native46、scroll、linked、公式XML）。DB3名10注記3型4prototype保存/最新XML読戻し済み。GPU/音/実機timingは新3gxで未確認。

