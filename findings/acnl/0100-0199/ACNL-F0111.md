---
id: ACNL-F0111
aliases:
- F-73
title: 'F-73: 通常Xのfield側入口は `sub_165B40 -> sub_5C1F08`。診断traceのPC相対LDR移設は不可'
summary: 'confidence: **HIGH**（実機のLR・trace buffer・SIGSEGV時レジスタと `code.bin.i64` を照合）'
date: '2026-08-24'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 6663228
- 1465192
- 1465188
- 1465224
- 6037256
- 6037380
- 6037264
- 11172564
- 1465204
- 1465208
- 1465228
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:4768-4803
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-73: 通常Xのfield側入口は `sub_165B40 -> sub_5C1F08`。診断traceのPC相対LDR移設は不可

confidence: **HIGH**（実機のLR・trace buffer・SIGSEGV時レジスタと `code.bin.i64` を照合）

`Actor_SetState` 全体を実機traceすると、通常Xの開閉ではプレイヤー状態が
`0x06 -> 0x16 -> 0x06` と遷移した。開く側は `sub_5C1F08` 内の
`sub_65945C`（state `0x16` helper）へのtail-call、閉じる側は
`sub_672CAC` 内の `sub_650F3C`（state `0x06` helper）へのtail-callである。
以前bpを置いた `0x65AC3C` はstate `0x16` のupdate処理 `sub_65ABBC` 内であり、
通常Xの開始点ではないため未到達だった。

`sub_5C1F08` の呼出し元を記録した実測値は `LR=0x165B68`。従って通常Xのfield側入口は
`sub_165B40` の `0x165B64: BL sub_5C1F08` で確定した。`sub_165B40` は成功後に
`0x165B88: BL Menu_RequestOpen` を持つが、同呼出しのmenuIdはまだ実測できていない。

診断用 `scratchpad/trace_inventory_x_path.py` の初版は `0x5C1F08` の先頭命令
`LDR R0,[PC,#0x74]` を命令語のまま `0x01E8151C` へ移した。PC相対アドレスが
`0x5C1F84` からcave側へずれ、R0が0になったため、復帰後の
`0x5C1F10: LDRB R0,[R0]` でSIGSEGVした。

停止時はTID 220、`PC=0x5C1F10`、`LR=0x165B68`、`R0=0`、例外code 11
(`SIGSEGV`, `can_cont=True`)。bufferはcommon hits=1、early hits=0だった。
本来 `0x5C1F84` のliteralは `0xAA7AD4`。スクリプトはcave-local literalから
`0xAA7AD4` をロードするよう修正した。証拠採取後、両hookを純正値へ戻し、cave/bufferを
ゼロ化してからTID 220のR0だけを `0xAA7AD4` へ補正した。同じPCからContinueすると
デバッガはRUNNINGを返し、再起動せず例外から復帰した。

復旧後、`0x165B88: BL Menu_RequestOpen` だけを副作用なしで計数するtraceを設置し、
通常の屋外Xで持ち物を開閉した。結果は **hits=0**。`sub_165B40` の実行時オブジェクトは
`a1+0x1B = 0x8B` であり、`0x165B74: CMP R0,#0x8B` → `0x165B78: BEQ 0x165B8C`
によって直接要求を意図的に飛ばす。従って前版 `0x165B88` フックが無反応だった理由は、
入口が違うのではなく、このfield用sentinel分岐だった。traceは読出し後に完全撤去し、
hookを `EB15ADE8`、cave/bufferを全ゼロへ戻した。

---

