---
id: ACNL-F0232
aliases:
- F-207
title: 'F-207: ★★★★★`drawctx+1692` が 0 だと UV が読まれずテクスチャ全面が貼られる — `HIGH`（実機）'
summary: '`nwlyt_Picture_DrawToCommandList` より:'
date: '2026-09-01'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:12645-12679
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-207: ★★★★★`drawctx+1692` が 0 だと UV が読まれずテクスチャ全面が貼られる — `HIGH`（実機）

`nwlyt_Picture_DrawToCommandList` より:

```c
v10 = *(picture + 216);                     // UV セット数
if (*(drawctx+1692) != v10) { flush; *(drawctx+1692) = v10; }
if (v10) { *(drawctx+1632) = +38; UV を配列へ; +38 += v10; }
```

**`drawctx+1692` が 0 のままだと UV 属性そのものが構成されず、
積んだ UV エントリは読まれない。** 記録の末尾では直前のペイン（UV 無し）の値が残る。

### 実機での見え方が決め手だった

- 「**OK の K で改行され、1 文字目の下に K が来る**」
  → アトラス（1 行目に 8 グリフ、2 行目先頭に K）が**そのまま**貼られている
- 「白い四角が中央から離れて**右下**に出る」
  → 校正用に塗り潰した**マス (7,7)＝アトラス右下**がそこに見えている

どちらも「UV 窓が効かず全面が貼られている」なら必ず起きることで、独立に一致した。

### 対策（ゲームと同じ手順）

```
LDR R1,[R4,#1692] ; CMP R1,#1 ; BEQ uvok
  LDRB R2,[R4,#36] ; CMP R2,#0 ; BEQ noflush
    BL DrawCtx_FlushBatch          溜まっているぶんを先に流す
noflush:
  MOV R1,#1 ; STR R1,[R4,#1692]
uvok:
```

---

