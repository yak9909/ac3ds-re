---
id: ACNL-F0190
aliases:
- F-164
title: 'F-164: `g_GfxAllocator` の正体と呼び出し規約を確定 — `HIGH`（静的解析、assembly まで確認）'
summary: '`Render_InitGlobal`(`0x4E97CC`) が組み立てている:'
date: '2026-08-28'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5150668
- 9438884
- 9436920
- 5173976
- 5675892
- 5675888
- 5675860
- 5675844
- 9751088
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:9797-9888
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-164: `g_GfxAllocator` の正体と呼び出し規約を確定 — `HIGH`（静的解析、assembly まで確認）

### 1. 構造

`Render_InitGlobal`(`0x4E97CC`) が組み立てている:

```c
v5 = Heap_CreateNamed(235520, parent);   // sead::ExpHeap を 0x39800 バイトで作る
v7 = Heap_Alloc(8, v5);                  // 8 バイト
g_GfxAllocator = ssys_ma_Allocator_Ctor(v7);
sub_12D3A4(g_GfxAllocator, v5);          // +4 に heap を結び付ける
```

| | |
|---|---|
| クラス | **`ssys::ma::Allocator`**（vtbl `0x9006A4`） |
| `+0x00` | vtable |
| `+0x04` | **`sead::ExpHeap*`**（vtbl `0x8FFEF8`） |
| 取得 | `GfxAllocator_Get`(`0x4EF2D8`) — `g_GfxAllocator` を返すだけ |

vtable は **4 スロットのみ**:

| slot | offset | 内容 | 実体 |
|---|---|---|---|
| 0 / 1 | +0x00 / +0x04 | デストラクタ 2 種 | `0x569B74` / `0x569B70` |
| **2** | **+0x08** | **`Alloc(size, align)`** | `0x569B54` |
| **3** | **+0x0C** | **`Free(ptr)`** | `0x569B44` |

### 2. ★assembly を見ないと両方とも取り違える

**`Alloc`**:

```
LDR R0, [R0,#4]      ; heap
CMP R2, #0
MOVEQ R2, #1         ; align が 0 なら 1
ADD R1, R1, R2       ; size += align（余分に確保）
LDR R3, [R0]
LDR R3, [R3,#0x18]   ; heap の vtable スロット 6
BX  R3
```

**`R2`（align）は消されずに残る**ので、実際には
`heap->alloc(size + align, align)` としてアラインメントも渡っている。
decompiler は 2 引数の呼び出しと見なして `R2` を落とす。

**`Free`**:

```
LDR R0, [R0,#4]
LDR R2, [R0]
LDR R2, [R2,#0x1C]   ; heap の vtable スロット 7
BX  R2
```

**`BX R2` のテール呼び出しなので `R1`(ptr) が素通しされる。**
decompiler は `sub(int a1)` と 1 引数に見せるが、実態は `Free(ptr)`。

### 3. GPU 可視かどうか（未確定）

**このアロケータが配るメモリは linear である可能性が高いが、まだ確定していない。**

根拠:

- `Render_InitGlobal` は `g_DrawContext` をこのアロケータから作っており、
  実機でその drawctx は **`0x32FF62EC`** だった（本セッションで実測）
- F-124 で `0x30000000+` の窓は **`VA - PA = 0x10000000`** と実測済み
  （テクスチャ VA `0x33076480` / PA `0x23076480`、PICA reg `0x085` から）

**ただしこれは推論であって証明ではない。**
`0x30000000`-`0x40000000` の窓の中で linear な部分と
そうでない部分が混在しない保証は取っていない。
**実際に GPU に読ませるまで断定しないこと。**

`Alloc` は align を渡すので `0x80` 境界の要求は満たせる。
`Render_InitGlobal` 自身が `(g_GfxAllocator, 264, 128)` と align 128 で呼んでいる実例がある。

### 4. これで CTRPF から呼べる形が見えた

```cpp
// フック内（ゲームのスレッド上）で
u32  alloc = *(u32 *)0x0094CA30;              // g_GfxAllocator
u32  vt    = *(u32 *)alloc;
typedef void *(*AllocFn)(u32, u32, u32);
void *p = ((AllocFn)*(u32 *)(vt + 8))(alloc, size, 0x80);
```

F-163 でプラグインからの `linearAlloc` / `svcControlMemory` が
`OutOfMemory` で全滅したので、**これが GPU 可視メモリを得る本命の経路**になる。

---

