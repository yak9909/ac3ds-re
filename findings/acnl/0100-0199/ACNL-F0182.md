---
id: ACNL-F0182
aliases:
- F-156
title: 'F-156: ★★★submit descriptor を静的に全導出。F-155a の observer は不要になった'
summary: 'confidence: **HIGH**（静的。decompile とアセンブリの両方で照合）'
date: '2026-08-28'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5067276
- 4947168
- 5067800
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:9166-9273
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-156: ★★★submit descriptor を静的に全導出。F-155a の observer は不要になった

confidence: **HIGH**（静的。decompile とアセンブリの両方で照合）

### 1. 背景

F-154 で `TextBox_EmitBatchToGpuCommands` の直呼びが
`GpuCmd_SelectList` SIGSEGV を起こし、
「private submit descriptor を作って `TextBatch_CopyToCommandBuffer(..., a3=0)` だけを使う」
方針になった。そのために descriptor のレイアウトを知る必要があり、
F-155a で observer cave を作ったが SIGSEGV し、
I-cache 制約で同一 boot では再注入できない状態だった。

**その descriptor を静的に全部導出できたので、observer は不要になった。**

### 2. ★`TextBatch_CopyToCommandBuffer`(`0x4D520C`) が読むフィールド

アセンブリで確認（`LDR R0,[R0,#0x44]` / `LDR R0,[R0,#0x1C]` /
`LDRB R2,[R4,#0x20]` / `ADD R1,R4,#0x18`）。

| offset | 内容 |
|---|---|
| `+0x00` / `+0x04` | 色 2 つ。reg `0x11B` / `0x133` へ。alpha は `+0x49` で乗算 |
| `+0x08`〜`+0x14` | 4 隅の展開先（`TextSubmitDesc_ExpandCornerColors` が書く） |
| **`+0x18` / `+0x1C`** | **文字色（上 / 下）** |
| **`+0x20`** | **グラデーションフラグ** 0 / 1 / 2 |
| **`+0x44`** | **batch ポインタ。`batch+0x1C` が 0 なら即 return** |
| **`+0x49`** | **alpha 倍率** |

batch 側:

| offset | 内容 |
|---|---|
| `+0x09` | 制御バイト。bit1 と bit2 で経路が分かれる |
| `+0x10` | 直接コピー経路の source |
| `+0x18` | bit2 セット時の source |
| `+0x1C` | command dword 数 |

### 3. ★★`a3`（DrawContext）は bit1 経路でしか使われない

```c
if ( (*(u8*)(batch + 9) & 2) != 0 ) {
    ... sub_348BEC(...) ...
    if (a3) {                      // ★ここだけ
        drawctx[419] ... drawctx[418] ... drawctx[417]   // range bookkeeping
    }
} else {
    Mem_Copy(cursor, *(batch+0x10), 4 * *(batch+0x1C));  // a3 を一切見ない
    return cursor + count;
}
```

**F-145 で実測した会話 TextBox は bit1 クリアの直接コピー経路**（632 バイト）。
したがってこの経路では **`a3` の値は結果に影響しない**。
`a3 = 0` で呼べば bit1 経路でも bookkeeping を飛ばせるので、
**どちらの経路でも安全**になる。

**F-154 の SIGSEGV の正体は、この bookkeeping（`drawctx+0x684/0x688/0x68C`）の
二重更新だった。**

### 4. ★descriptor の組み立て方（`0x4B7CE0` から導出）

```
desc = *(a5 + 128) + 248          ← ゲームは a5 のスクラッチ領域を使う
desc+0x44 = *(textbox + 260)      batch
desc+0x18 = *(textbox + 216)      文字色 上
desc+0x1C = *(textbox + 220)      文字色 下
desc+0x20 = (2 色が違えば 2, 同じなら 0)
desc+0x00 = *(textbox + 272)      （a4 = textbox+0x100 なので a4+16）
desc+0x04 = *(textbox + 276)      （a4+20）
desc+0x49 = *(textbox + 181)      alpha 倍率
TextSubmitDesc_ExpandCornerColors(desc)   ← 色を入れた後に呼ぶ
```

**必要な span は `0x4A` バイトだけ。**
descriptor は CPU が読むだけで **GPU から見える必要がない**ので、
cave ページに置ける。

### 5. `TextSubmitDesc_ExpandCornerColors`(`0x4D5418`)

`+0x20` のフラグでグラデーション方向を選び、`+0x18`/`+0x1C` の 2 色を
`+0x08`/`+0x0C`/`+0x10`/`+0x14` の 4 隅へ配る。

`0x4B7CE0` は色を入れる**前**にも 1 回呼んでいるが、それは無意味（stale）。
2 回目が本番。

なお `TextBatch_CopyToCommandBuffer` 自身は `+0x18`/`+0x20` を見て
`TextDraw_BuildFourCornerColors` で再展開するため、
**`+0x08`〜`+0x14` はこの経路では使われていない可能性がある**（`MEDIUM`）。

### 6. 次の実装方針

1. cave に `0x4A` バイトの descriptor 領域を確保
2. 対象 TextBox から上記 7 フィールドをコピー
3. `TextSubmitDesc_ExpandCornerColors(desc)` を呼ぶ
4. `TextBatch_CopyToCommandBuffer(desc, cursor, 0)` を呼ぶ
5. 戻り値が新しい cursor

**`TextBox_EmitBatchToGpuCommands` も `TextBox_Draw` wrapper も呼ばない。**

### 7. 検証状況

静的のみ。**実機未検証。** 適用は fresh boot 後に行うこと
（F-155a の I-cache 制約は「旧 cave を実行した boot で改版を注入するな」であり、
本項の新規実装も同じ boot では避けるのが安全）。

---

