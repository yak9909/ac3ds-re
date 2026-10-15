---
id: ACNL-F0299
aliases:
- F-275
title: 'F-275: 自前ノードに対してゲームが呼ぶのは vtable `+0x08` と `+0x14` の 2 つだけ — `HIGH`（静的）'
summary: '`CAVE_N`（安全スタブ、常に `R0 = 0` を返す）が危険なスロットに置かれていないかを確認した。'
date: '2026-09-01'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5664416
- 5664304
- 8611584
- 8611840
- 8612096
- 8612352
- 8622080
tags:
- rtti
supersedes: []
source: v1:RE/FINDINGS.md:16804-16866
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-275: 自前ノードに対してゲームが呼ぶのは vtable `+0x08` と `+0x14` の 2 つだけ — `HIGH`（静的）

`CAVE_N`（安全スタブ、常に `R0 = 0` を返す）が危険なスロットに置かれていないかを確認した。

| 呼び出し元 | 何を呼ぶか |
|---|---|
| `LayoutList_RecordChildren`（`0x566EA0`） | `for (i = *(list+4); i; i = i[2]) (*(*i + 20))(i)` → **Layout vtable `+0x14`** |
| `LayoutList_SetDisplay`（`0x566E30`） | `for (…) { i[77] = token; (*(*i + 8))(i); }` → `+0x134` に display を書いて **`+0x08`** |

**この 2 つ以外に Layout の vtable を叩く経路は無い。**
`+0x18`（SetupProjectionMatrix）は `Layout_RecordPaneTree` の中からしか呼ばれず、
我々はその関数を使っていない（自前の記録スロットを使う）。
したがって `CAVE_N` は通常動作では一度も実行されない。

### 登録の二重挿入は**ゲーム側にも防護がある**

`sub_13F84C(list, node)`（push_back）の先頭は

```c
if ( !*(_QWORD *)(a2 + 4) )   // node+0x04（prev）と node+0x08（next）が両方 0 のときだけ
```

- **空でないリストへの挿入**: `node->prev = 旧 tail`（≠ 0）→ 我々の判定 (b) が効く
- **空リストへの挿入**: prev も next も 0 → 判定 (b)(c) は効かないが、
  `list->tail == node` になるので判定 (a) が効く

**さらにゲーム自身の `!*(u64*)(node+4)` があるので、三重に守られている。**

### 自前ノードの `+0x10`（ペインツリー）は一度も参照されない

- `SetupProjectionMatrix` は `sub_73BAC0(&rect, this+0x10)` を呼ぶが、
  中身は `*(float*)(a2+24)` と `*(float*)(a2+28)` すなわち **`this+0x28` / `this+0x2C`** を
  読むだけで、`+0x10` をポインタとして辿らない（F-266）
- `nwlyt_DrawPaneTreeToCurrentList`（`+0x10` の `+0x20` をルートとして辿る）は
  `Layout_RecordPaneTree` からしか呼ばれない。我々は使わない
- `Layout_ReplayRecordedList` は `+0x10` を触らない

**したがって自前ノードの `+0x10` 付近が `.bss` のゼロのままでも安全。**

### 小さいケーブ 4 本を IDA で全命令確認した

空き `.text`（`0x836700` / `0x836800` / `0x836900` / `0x836A00`）へ相対位置ごと当てて
逆アセンブルし、直後に元バイトへ復元した。

```
CAVE_F  PUSH {R0-R3,R12,LR} / LDR R12,=LOG / STR R0,[R12,#4] (drawctx)
        LDR R1,[R12,#0xE8] / ADD R1,#1 / STR R1,[R12,#0xE8]
        POP {R0-R3,R12,LR} / PUSH {R4-R8,LR} / B loc_4B8364
CAVE_T  PUSH {R4-R8,LR} / B loc_4B8364
CAVE_N  PUSH {R0-R3,R12,LR} / LDR R0,=0xFFFF8001 / LDR R1,=0x329D8500 / LDR R2,=0x1000
        SVC 0x54 (svcFlushProcessDataCache) / POP {R0-R3,R12,LR} / MOV R0,#0 / BX LR
CAVE_M  PUSH {R0-R3,R12,LR} / LDR R12,=LOG / STR R2,[R12,#0x20]
        POP {R0-R3,R12,LR} / PUSH {R4-R11,LR} / B loc_4B7868
```

- `CAVE_F` / `CAVE_M` は引数レジスタ（R0-R3）と R12 を保存・復元しており、
  元命令を実行してから元関数の +4 へ戻る。**引数を壊さない**
- `CAVE_T` は `DrawCtx_FlushBatch` を `BL` で呼べるようにするトランポリン
- **`.text` の `0x838200`-`0x839000`（ケーブ領域）は `code.bin.i64` に未マップ**である。
  IDA で検証するときは必ずマップ済みの空きへ相対位置ごと移して当てること

---

