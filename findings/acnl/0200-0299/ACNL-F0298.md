---
id: ACNL-F0298
aliases:
- F-274
title: 'F-274: `sub_2F858C` は **3 引数の memcpy**。decompiler が R1/R2 を落としていた — `HIGH`（アセンブリ）'
summary: '`GpuCmd_ReplayRecordedListRange` の末尾を Hex-Rays で読むと'
date: '2026-09-01'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8064520
- 8064524
- 8064528
- 8064532
- 8064536
- 8064540
- 8064544
- 8064548
- 8064552
- 8064556
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:16732-16803
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-274: `sub_2F858C` は **3 引数の memcpy**。decompiler が R1/R2 を落としていた — `HIGH`（アセンブリ）

`GpuCmd_ReplayRecordedListRange` の末尾を Hex-Rays で読むと

```c
if ( a3 > v19 ) { sub_2F858C(g_GpuCmdPtr); g_GpuCmdPtr += (a3 - v19) & 0xFFFFFFFC; }
```

となっていて、「記録した内容は**場所を予約するだけ**で、実体は GX キューの
エントリが運ぶのではないか」と読めてしまう。**これは誤読である。**

### アセンブリ（`0x7B0E08`〜）

```
0x7b0e08 LDR R0, [SP,#var_C]   ; a2 = off（記録の開始オフセット）
0x7b0e0c LDR R1, [R7,#4]       ; R7 = 送り元リストマネージャ → +0x04 = base
0x7b0e10 LDR R4, off_7B0F44    ; &g_GpuCmdPtr
0x7b0e14 ADD R2, R0, R10       ; off + copied
0x7b0e18 LDR R0, [SP,#var_8]   ; a3 = len
0x7b0e1c ADD R1, R1, R2        ; ★src = base + off + copied
0x7b0e20 SUB R5, R0, R10       ; ★size = len - copied
0x7b0e24 LDR R0, [R4]          ; ★dst = g_GpuCmdPtr
0x7b0e28 MOV R2, R5
0x7b0e2c BL  sub_2F858C
```

`sub_2F858C` の先頭は

```
CMP   R2, #3
BLS   ...
ANDS  R12, R0, #3
BEQ   ...
LDRB  R3, [R1],#1
STRB  R3, [R0],#1
...
```

**サイズ（R2）と宛先のアラインメント（R0）を見てバイト単位で写している。
キャッシュ操作ではなく memcpy である。** `Mem_CopyBytes3(dst, src, size)` と命名した。

CLAUDE.md が警告している decompiler の罠
（`ssys::ma::Allocator::Alloc`／`DrawCtx_FlushBatch` と同じ）にまた当たった形。

### これが意味すること

**自前ノードの記録内容は、replay 時に主リストへ「物理的にコピー」される。**
場所の予約ではない。したがって

- 記録の内容がそのままフレームのコマンド列に入る（順序は replay 順）
- 主リストの容量はゲーム側の `GpuCmd_SplitAndSubmit` 機構が面倒を見る。
  自前ノードも「ただの Layout」なので同じ扱いを受ける

### 他の呼び出し箇所も読み直した

| 場所 | 実際の意味 |
|---|---|
| `GpuCmd_ReplayRecordedListRange` の GX キュー走査内 | エントリごとの範囲を主リストへコピー |
| `sub_4D5D1C`（Drawer 既定列の構築） | 26x96 = 2496 バイトの表を GPU 可視バッファへ写し、直後に `RangeCacheOp(_, 2496)` |

`sub_4D5D1C` の 2496 バイトは、その直前で `unk_AE8554` に組み立てている
**26 個ぶんの索引データ**（`unk_8ADC08` の 6 要素 × 26）。F-268 の読みと矛盾しない。

### F-268〜F-273 への影響

**無い。** いずれもこの関数の引数解釈に依存した結論を出していない。
ただし「記録内容が物理コピーされる」ことが確定したので、
F-259 以降の設計（自前リストへ記録 → ゲームの replay 関数で再生）は
**動作原理として完全に裏付けられた**。

---

