---
id: ACNL-F0628
aliases:
- IDA-opus-5.5-F108
title: 'HHD と ACNL でアニメのコマ数の数え方が 1 つ違う（2026-10-07、HIGH: 静的＋実機の症状）'
summary: 'ACNL の UiAnim_Step 0x568964: +0x14 bit0（ループしない）なら frame は frameSize(+4) − 1 で頭打ち、bit0 が無ければ frameSize で巻き戻す。UiAnim_IsFinished 0x74F58C も frame >= frameSize − 1。ACNL の BCLAN（ループしない）は最後のキーが frameSize − 1 に 527 件（frameSize ちょうどは 7 件）。'
date: '2026-10-07'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5671268
- 7665036
- 1671168
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4944-4953
by: opus-5.5
original_by: ''
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F108: HHD と ACNL でアニメのコマ数の数え方が 1 つ違う（2026-10-07、HIGH: 静的＋実機の症状）

- ACNL の UiAnim_Step 0x568964: +0x14 bit0（ループしない）なら frame は frameSize(+4) − 1 で頭打ち、bit0 が無ければ frameSize で巻き戻す。UiAnim_IsFinished 0x74F58C も frame >= frameSize − 1。ACNL の BCLAN（ループしない）は最後のキーが frameSize − 1 に 527 件（frameSize ちょうどは 7 件）。
- HHD の BFLAN（ループしない）は最後のキーが frameSize ちょうどに 666 件（frameSize − 1 は 76 件）。→ HHD のアニメをそのまま BCLAN にすると最後のキーに届かない。
- 実機の症状と一致: ゴミ箱のふた on（キー 0 = 閉 / 1 = 開）・off（0 = 開 / 1 = 閉）は frameSize 1 で、0 コマ目で止まる → 重ねても閉じたまま、離すと開く（decor_trash1・2 の 2 回とも利用者の報告どおり）。
- 対処: tools/hhd/clan_pack.read_flan(acnl_frames=True) でループしないアニメの frameSize を +1（make_decorate_arc / make_catalog_arc）。gohan は「最後のコマ」を frames − 1 にする。HhdScreen の生成（make_acnl_layouts / export_gohan_tables）は実機確認済みなので変えていない（そちらの in / out も最後のキーに 1 コマ届いていない可能性がある。未確認）。
- 反証条件: decor_catalog2 でふたが重ねたとき開かない。

- 追記（T022 窓が開かない件、2026-10-07、opus-5.5、ida-pro-mcp）: decor_catalog1 の停止中に gohan の s_win_state ← Loading、s_wantCatFile ← 1 を書いて 3 秒走らせると Closed に戻った（読み込み失敗の道しか Loading → Closed へ行かない）。プラグインのヒープは 0x060A9000〜0x067C1000 で使用 0x198000、517 KB は取れるはず → SD に hhd_catalog.arc が無い・読めないのどちらか。decor_catalog2 は理由を通知する。

