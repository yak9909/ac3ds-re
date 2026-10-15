---
id: ACNL-F0067
aliases:
- F-29
title: F-29 掘削の実処理は `FieldObj_ApplyRecordByAction` の jumptable — `HIGH`
summary: '`0x5A06D4`-`0x5A0C1C`。`rec[16]`（actionID）で 29 ケースに分岐する。'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5899988
- 5901340
- 5900112
- 5900116
- 5900124
- 5900120
- 5900760
- 5900780
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1456-1489
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-29 掘削の実処理は `FieldObj_ApplyRecordByAction` の jumptable — `HIGH`

`0x5A06D4`-`0x5A0C1C`。`rec[16]`（actionID）で 29 ケースに分岐する。

```
0x5A0750  CMP R0, #0x1D          ; switch 29 cases
0x5A0754  LDRCC PC, [PC,R0,LSL#2]
```

**jumptable の base は `0x5A075C`**（命令 `0x5A0754` + 8）。
`0x5A0758` から数えると 1 つずれるので注意（実際に一度誤った）。

**case 19（掘る）= `0x5A09D8`**:

```
MOV  R1, #0x9E                 ; 158 = 穴
ADD  R0, SP, #4
BL   Item_InitWithId           ; ローカルに 158 を構築
LDRB R2, [R4,#0xF]             ; Y
LDRB R1, [R4,#0xE]             ; X
BL   FieldObj_SpawnActor       ; 0x5A09EC ★穴のアクターを生成
EOR  R5, R0, #1                ; 戻り値を使う
CMP  R5, #0
BEQ  loc_5A0A3C                ; 成功なら
  → Field_SetItemAt(X, Y, flag, pNo, g_EmptyItem)   ; マスを「空」にする
  → Field_MarkDirty(X, Y)
  → Effect_ItemRemoved(item, X, Y, 1)               ; sub_175898 (cat 9/21 のみ)
; 失敗なら FieldObj_RevertRecord / FieldObj_RequeueCase4 でキャンセル
```

`R4` = 22B レコード。`R4[0xE]` = X、`R4[0xF]` = Y。

---

