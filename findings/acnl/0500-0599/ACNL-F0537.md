---
id: ACNL-F0537
aliases:
- IDA-opus-5-F031
title: gohan のグリッドカーソルが何も描かなかった2つの原因（2026-09-22、HIGH、実機の状態読み＋静的）
summary: '解析ソフト: IDA / 解析モデル: opus-5。利用者の報告「チートをONにしても表示されません。大きさを200にしても'
date: '2026-09-22'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1798684
- 9735792
- 3242076
- 5168280
- 5168244
- 5178508
- 5159956
- 5178112
- 5160524
- 5662696
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:3543-3635
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F031: gohan のグリッドカーソルが何も描かなかった2つの原因（2026-09-22、HIGH、実機の状態読み＋静的）

解析ソフト: IDA / 解析モデル: opus-5。利用者の報告「チートをONにしても表示されません。大きさを200にしても
画面にはなんの変化もありません」に対し、Suspend 中の実機からプラグインの状態を直接読んで切り分けた。

### 0. まず何が起きていたか（実機の実測値）

スタブ・フックは正常だった。`0x001B721C` = `0xEA1A0537`（期待どおりの分岐）、
`0x00838700` の 60 B も生成物と一致、`+0x38` のコールバック語は `0x0700F3FC` = `FrameCallback` の実番地。
`s_frames` = **0xB21（2,849）** なので**スタブは毎フレーム走っていた**。

| 変数 | 値 | 意味 |
|---|---|---|
| `s_stage` | 1 = `AllocHeaps` | 最初の段から一歩も進んでいない |
| `s_loadAttempts` | 0 | `StepBuild()` が**一度も呼ばれていない** |
| `s_failReason` | `kNone` | 失敗もしていない |
| `s_sceneOwner` | 0 | まだ控えていない |
| `[0x00948E70]` | `0x3310B5B8` | 実機のシーン所有者 |

### 1. シーン所有者の検査を、その所有者を控える前にかけていた

`FrameCallback` は毎フレーム

```
owner = *[0x00948E70]
s_sceneOk = IsHeapPointer(owner) && owner == s_sceneOwner && (資源も一致)
if (!s_sceneOk) return;          // ★ここで毎回帰る
if (s_stage != Ready) StepBuild();
```

を回していたが、**`s_sceneOwner` を書き込むのは `StepBuild()` の `AllocHeaps` の中**。
つまり控える前に「控えた値と一致するか」を問うていて、永久に真にならない。
失敗ではないので `Stage::Failed` にもならず、通知も出ない。**沈黙したデッドロック**。

直し方は「控えていない間はこの検査に意味が無い」ことを素直に書く:
`s_sceneOwner == nullptr` なら検査を飛ばし、`stage == AllocHeaps` のときだけ `StepBuild()` を呼ぶ。
`AllocHeaps` は自分で部屋 ID と所有者を検査するので素通しでよい。
ビルド後の逆アセンブルで確認済み（`FrameCallback+0x180`: `ldr r1,[r4,#0x344]` / `cmp r1,#0` /
`bne` 通常経路 / `cmp stage,#1` / `b StepBuild`）。

### 2. `Heap_CreateNamed_0 0x0031785C` の第6引数は s0 ではなくスタック

これは 1 を直しても次に必ず踏んでいた。**ゲームは fill(float) を呼び出し元スタックから読む。**

```
0031785c  push {r4,r5,r6,r7,r8,lr}   ; 24 B
00317860  ...
0031786c  vpush {d8}                 ; +8 = 32 B
00317870  sub sp, sp, #8             ; +8 = 40 B
00317878  ldr  r5, [sp, #40]         ; 第5引数 flag  = 呼び出し元 SP+0
0031787c  vldr s16, [sp, #44]        ; 第6引数 fill  = 呼び出し元 SP+4  ★
```

Python ハーネス（`tools/models3d/arbitrary_model.py`）は `stack=(1, 0)` と**語 2 本**で渡していたので
実機で通っていた。ところが gohan は devkitARM の **`-mfloat-abi=hard`**（`Makefile` の `ARCH`）でビルドされ、
`float fill` と宣言すると AAPCS-VFP で **`s0`** に載る。生成された命令は実際に

```
700f508  str  r3, [sp]        ; flag = 1
700f50c  vldr s0, [pc, #500]  ; fill が s0 へ ★SP+4 には何も書かれない
```

で、ゲームは `[SP+4]` の**ゴミ**を fill として使っていた。
第6引数を `u32` で宣言して `0` を渡すと `str r6,[sp,#4]`（`r6` はこの経路で部屋 ID = 0）になり、
ハーネスと同一の語並びになる。0 は `0.0f` のビット表現。

**同種の取り違えが他に無いことも確かめた**（ここが本題）:

| 関数 | ゲーム側の読み方 | 宣言 |
|---|---|---|
| `AnimSetFrame 0x004EDC98` | `vmov.f32 s16, s0` | `float` で**正しい** |
| `AnimSetRate 0x004EDC74` | `vmov.f32 s16, s0` | `float` で**正しい** |
| `ModelInstanceCreate 0x004F048C` | `ldr r4,[sp,#72]` / `ldm sp+76,{r1,r5}` | 整数 4 レジスタ + 3 スタック語 |
| `MaterialAnimBuildFromRes 0x004EBC14` | `ldr r0,[sp,#40]` | 整数 4 + 1 |
| `BindAnimSlot 0x004F0300` | 整数 3 本、浮動小数なし | 正しい |

**つまり「float を引数に取るゲーム関数」でも s0 とスタックの両方があり、関数ごとに逆アセンブルで確かめるしかない。**

### 3. 併せて足したもの

「失敗ではない停止」は通知が出ないので外から見えない。これが今回の診断を実機依存にしていた。
`root/テスト` に **「状態を見る」**（`ITEM_ACTION`）を足し、段名／理由／体数／提出数／フレーム数を通知で出す。
通知は 1 行・幅 130px でトリムされるので、理由がある時は理由だけ、無い時は段名＋数字にしている。

`MaterialAnimCtor 0x004EBE4C` がハーネスの手書き 32 B と同じ像を作ることも確認した
（`HeapAllocator_Ctor 0x005667E8` が `+4` を 0 にするので `anim+16` も 0 になる）。

根拠: 実機 Suspend 中の `ida-pro-mcp` による `0x07162B80`〜`0x0716303C` の直読み、
`gohan.elf` の `nm` と逆アセンブル、`acnl_jpn_v15_annotated.i64` の `0x0031785C` / `0x004EDC74` /
`0x004F048C` / `0x004EBC14` / `0x004F0300` / `0x005667E8`、`src/gohan/Makefile` の `-mfloat-abi=hard`。
反証条件: `[SP+4]` のゴミがたまたま無害な値ばかりで、ヒープ生成は元から成功していた
（1 の時点で `HeapCreateNamed` に到達していないので、今回は観測できていない）。

