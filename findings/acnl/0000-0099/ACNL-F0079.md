---
id: ACNL-F0079
aliases:
- F-41
title: F-41 `FieldObj_FinalizeRecord` (0x5A10AC) — 伐採の終端処理 — `HIGH`
summary: レコードが完了したときに `FieldObj_FellObject` を呼ぶ側。斧経路の呼び出し元 `0x5A1198`
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5902508
- 5902744
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1896-1930
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-41 `FieldObj_FinalizeRecord` (0x5A10AC) — 伐採の終端処理 — `HIGH`

レコードが完了したときに `FieldObj_FellObject` を呼ぶ側。斧経路の呼び出し元 `0x5A1198`
はこの関数の中にある。**伐採の引数がここで組み立てられる。**

```
005A10AC  PUSH {R4-R7,LR}        ; R4 = レコード*  R5 = a2(フラグ)
005A10E4  BL   unk_2FC8F0        ; [SP+0xC] <- g_EmptyItem (a2 の初期値)
005A10F4  LDRB R0, [R4,#0xC]     ; レコードの flags
005A10FC  TST  R0, #0x20
005A1100  BEQ  loc_5A114C        ; ★flags bit5 が立っていなければ a2 は空のまま
005A1104  ADD  R1, R4, #4        ; レコードの item1
005A110C  BL   Item_Copy         ; ★a2 <- item1
005A1110  LDRB R0, [R4,#0xC]
005A1114  TST  R0, #2
005A1118  MOVNE R5, #5           ; ★kind = 5（逆向き）
005A111C  MOVEQ R5, #4           ; ★kind = 4
005A114C  ...
005A1154  BL   unk_2FC8F0        ; a1 <- レコードの item0
005A1180  STR  R5, [SP,#4]       ; a6 = kind
005A1198  BL   FieldObj_FellObject
```

確定したこと:

| 値 | 出どころ |
|---|---|
| `a2`（切り倒した後に残すもの） | **レコードの `item1`**（`flags & 0x20` のとき） |
| `kind`（倒れる向き） | **レコードの `flags` bit1**。1 なら 5、0 なら 4 |

キューの `[17]` とレコードの `[12]` は同じ flags で、実測でも両方 `0xE2` だった。
したがって**キューの段階でも同じ bit から向きが読める。**

---

