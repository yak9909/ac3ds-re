---
id: ACNL-F0416
aliases:
- IDA-gpt-6-F014
title: hidden letterの入場座標とCHEATS選択肢（2026-10-14）
summary: GPT-6/idalib、MEDIUM。LetterDragWindowBase_AttachToPane 0x31F2B8はroot+632をparent+976/N_pos_ltrへ繋ぐ。Pane_CalculateMtxはvisible0かつDrawInfo+136 bit2なしなら子も計算しない。原ARM probe/製品FrameStepで、親を入場位置へ移しても[-560,-80,0]に残留し、force bit4で[150,-80,0]へ更新/visible0保
date: '2026-10-14'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:3-9
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-F014: hidden letterの入場座標とCHEATS選択肢（2026-10-14）

- GPT-6/idalib、MEDIUM。LetterDragWindowBase_AttachToPane 0x31F2B8はroot+632をparent+976/N_pos_ltrへ繋ぐ。Pane_CalculateMtxはvisible0かつDrawInfo+136 bit2なしなら子も計算しない。原ARM probe/製品FrameStepで、親を入場位置へ移しても[-560,-80,0]に残留し、force bit4で[150,-80,0]へ更新/visible0保持を確認。実機固有の座標値は未取得。
- T017はletterをvisible-only制限なしで評価（時刻は進めない）し、background DrawInfoのforce bitを一時有効にしてnative LayoutCalc、全flagbyteを復元する。二重AddLayoutなし。旧PCfixtureは完成matrix/Draw/Calcをmockしておりこの未表示を見逃した。
- 利用者訂正: たべる/じめんにおくはCHEATS既存方式。ui.txt/ACNL_ALPCメニューの19C150=NOPとdrop.txt等の19BFB0=NOPを原BEQ0A000009/0A000017と照合。自作2descriptor/文言撤去、native builder生成/文言/PMF使用へ。ON/OFF/64mask/競合時無書込/実STR+flush呼出し、原builder部分のnative text43-action16/text15-action0を確認。
- 根拠work/evidence/gohan_pocket_trash_visibility、設計pocket_trash_visibility_design.md。native57case/75anchor21CPP4334parser/font欠字0/linked/scroll/DB公式XML122名73func注記14構造体2Enum/global/T/hash PASS、DB1func名/8注記/980B prefix+forceEnum/prototype保存・close。実機/GPU成功へ昇格しない。保存結果とartifact SHAはSESSION/manifestを正とする。

