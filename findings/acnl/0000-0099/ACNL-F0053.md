---
id: ACNL-F0053
aliases:
- F-15
title: F-15 `Player_StartFieldAction` の呼び出し規約 — `HIGH`
summary: '`0x598660`-`0x598688` の assembly から確定。'
date: '2026-09-08'
category: actor
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5867104
- 5867144
- 9789428
- 5866060
- 5866072
- 5866100
tags:
- player
supersedes: []
source: v1:RE/FINDINGS.md:930-954
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-15 `Player_StartFieldAction` の呼び出し規約 — `HIGH`

`0x598660`-`0x598688` の assembly から確定。

| 引数 | 位置 | 呼び出し時の値 | キューの格納先 |
|---|---|---|---|
| a1 | R0 | actionID (R4) | `[14]` |
| a2 | R1 | 対象アイテム* (R6) | `[0..3]` |
| a3 | R2 | 結果アイテム* (SP+0x1C のローカル) | `[4..7]` |
| a4 | R3 | `&g_EmptyItem` = `0x955FF4` | `[8..11]` |
| a5 | [SP+0x00] | **X** (R8) | `[12]` |
| a6 | [SP+0x04] | **Y** (R9) | `[13]` |
| a7-a11 | [SP+0x08..0x18] | **すべて 0** (R7) | `[17]` にビット合成 |

R8 = 第2引数 X、R9 = 第3引数 Y（`0x59824C` / `0x598258`）。
a7-a11 が 0 であることは、`0x598274 : MOV R7,#0` が
`FieldObj_ResolveDigAction` 内で R7 に書き込む**唯一の命令**であることを
命令走査で確認して裏を取った（Rd フィールド == 7 の書き込み系命令は 1 件のみ）。

**含意**: X/Y はスタック引数なので、フックから追加呼び出しする際は
スタック引数領域を作り直さず、`[SP+0]`/`[SP+4]` を書き換えて呼び、
元に戻すだけでよい。

---

