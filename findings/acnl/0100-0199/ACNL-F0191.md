---
id: ACNL-F0191
aliases:
- F-165
title: 'F-165: ゲームのアロケータをフックから呼べた。0x80 境界・linear 窓内 — `HIGH`（実機）'
summary: '適用: `PATCHES/cave_gfxalloc_probe.py`'
date: '2026-08-28'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5184740
- 9751088
- 9436920
- 9438884
- 5675860
- 5675844
- 10158080
tags:
- hook
supersedes: []
source: v1:RE/FINDINGS.md:9889-9946
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-165: ゲームのアロケータをフックから呼べた。0x80 境界・linear 窓内 — `HIGH`（実機）

適用: `PATCHES/cave_gfxalloc_probe.py`

### 1. 手順

`Render_FrameEnd`(`0x4F1CE4`、先頭 `PUSH {R4-R6,LR}`) にケーブを置き、
`.bss` のスクラッチが 0 のときだけ 1 回だけ呼ぶ:

```
LDR R0, =0x0094CA30 ; LDR R0,[R0]      g_GfxAllocator
LDR R3, [R0] ; LDR R3, [R3,#8]         vtable スロット 2 = Alloc
MOV R1, #0x1000 ; MOV R2, #0x80
BLX R3
STR R0, [scratch]
```

`PUSH {R0-R3,R12,LR}` / `POP` で挟むので元の処理には影響しない
（6 ワード = 24 バイトで 8 境界も保たれる）。

### 2. 結果

| | |
|---|---|
| `g_GfxAllocator`（live） | `0x329A4820` |
| heap（live） | `0x329A4778`、vtable `0x008FFEF8` = `sead::ExpHeap` |
| **`Alloc(0x1000, 0x80)` の戻り** | **`0x329D8500`** |
| `0x80` 境界 | **満たす**（下位 7bit = 0） |
| linear の窓 `0x30000000`-`0x3FFFFFFF` | **中にある** |
| F-124 に従った物理アドレス | `0x229D8500` |

live の値は静的解析（F-164）と完全に一致した
（vtable `0x009006A4` / Alloc `0x00569B54` / Free `0x00569B44`）。

### 3. ★副産物: `.bss` はケーブから書き込める

`0x009B0000`（`.bss` のゼロ領域）へケーブ内から `STR` して**フォルトしなかった**。

F-161 で `.text` へ `STR` して SIGSEGV になったのと対になる結果。
**ケーブの書き込み先は `.bss` に置けばよい**ことが確定した。

| 領域 | ケーブから | 用途 |
|---|---|---|
| `.text` `0x00838080`〜 | 実行 / 読み **のみ** | コード、リテラル、パラメータ表 |
| `.bss` `0x009B0000`〜 | **読み書き可** | ログ、観測バッファ、状態 |

### 4. まだ証明されていないこと

**「linear の窓の中にある」ことと「GPU が読める」ことは同じではない。**
`0x30000000`-`0x40000000` の窓の中で linear な部分とそうでない部分が
混在しない保証は取っていない。

証明には **実際にこのバッファへテクスチャを置き、PICA の `reg 0x085` を
`PA = VA - 0x10000000` に向けて、絵が出ることを確認する**必要がある。
F-123 / F-124 で影テクスチャに対して成立させた手順がそのまま使える。→ TODO-117

---

