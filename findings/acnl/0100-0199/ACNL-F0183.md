---
id: ACNL-F0183
aliases:
- F-157
title: 'F-157: ★★★テキスト描画コマンドの投入を自前で駆動できた。色バイト順も確定 — `HIGH`（静的導出＋実機で視認）'
summary: 実機の会話ウィンドウで、住民名 `T_nam_00`（「ぺりお」）が
date: '2026-08-28'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7589704
- 7589740
- 4947404
- 4947420
- 4947408
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:9274-9389
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-157: ★★★テキスト描画コマンドの投入を自前で駆動できた。色バイト順も確定 — `HIGH`（静的導出＋実機で視認）

### 1. 結果

実機の会話ウィンドウで、住民名 `T_nam_00`（「ぺりお」）が
**暗い緑から赤に変わった。** これは我々のコードが `TextBatch_CopyToCommandBuffer`
を直接呼んで積んだ 2 枚目である。

`TextBox_Draw` wrapper も `TextBox_EmitBatchToGpuCommands` も呼んでいない。
F-152 / F-154 で詰まっていた「再入と DrawContext 二重更新」を完全に回避した。

適用スクリプト: `PATCHES/cave_text_emit.py`

### 2. F-156 の 2 つの誤りを訂正

**(a) 第 4 引数はマテリアル。`textbox + 0x100` ではない。**

呼び出し元 `sub_73CF48`(0x73CF48) の末尾:

```c
return TextBox_EmitBatchToGpuCommands(a4, v11, a1, *(a1 + 256), a3);
//                                                 ^^^^^^^^^^^^ マテリアル
```

`*(textbox + 256)` は**デリファレンス**であって加算ではない。
IDB コメントが「a4 = textbox + 0x100」と書いていたためこれを取り違え、
`textbox+272` を色だと誤記していた。

live の `textbox+272` は `0x32D208F8` = **textbox 自身 + 0x170 の自己参照ポインタ**で、
色ではない。この 1 点で誤りに気付けた。
`0x73CF6C` の早期 return が `*(a1+256)==0` を弾いていることも裏付けになる。

**(b) descriptor はスタック上に作られていない。**

`desc = *(a5 + 128) + 248` — **描画コンテキストが持つ常設スクラッチ**で、
毎 box 使い回される。末尾で `+0x44` だけ 0 に戻される。

### 3. live 実測した descriptor の出所（会話ウィンドウ 3 pane）

| pane | textbox | material `*(tb+256)` | `mat+20` = desc+0x04 | `tb+181` = desc+0x49 | 見え方 |
|---|---|---|---|---|---|
| `T_msg_00` 本文 | `0x32D20788` | `0x32D208A4` | `FFFFFFFF` | `0xFF` | 白・不透明 |
| `S_msg_00` 影 | `0x32D20488` | `0x32D205A4` | **`FF000000`** | **`0xF0`** | 黒・94% |
| `T_nam_00` 名前 | `0x32D20220` | `0x32D2033C` | `FF0A5500` | `0xFF` | 暗い緑 |

**F-128（ドロップシャドウは別 pane）がこれで機構まで確定した。**
影はフォントの一部でも専用の影描画処理でもなく、
**マテリアル色が黒・alpha 倍率 `0xF0` の 2 枚目の TextBox** である。

### 4. ★色のバイト順は `0xAABBGGRR`（メモリ上 R,G,B,A 順）

`desc+0x04` に `0xFF0000FF` を入れたら **赤**になった。
→ **R が下位バイト。** u32 リテラルとしては `0xAABBGGRR`。

既存の観測すべてと整合する:

- `FF0A5500` → R=00 G=55 B=0A = 暗い緑（実際に暗い緑）
- `FF000000` → 黒（影）
- `FFFFFFFF` → 白（本文）

`TextBatch_CopyToCommandBuffer` は `(color & 0xFFFFFF) | (A*desc[0x49]/255 << 24)` を
reg `0x0F3`（desc+0x04 側）と reg `0x0DB`（desc+0x00 側）のパラメータにする。

### 5. ★実装が大幅に簡単になる発見 — desc を組み立てる必要がない

`0x4B7DCC`（`TextBatch_CopyToCommandBuffer` から戻った直後）では

```
R0 = 進んだ cursor    R4 = 完成済み desc    R6 = textbox    R5 = drawctx
```

で、`desc+0x44` のクリアは **0x4B7DDC まで起きない。**
つまり **その時点の `R4` は全フィールドが埋まった正規の descriptor** である。

色だけ差し替えて `CopyToCommandBuffer` をもう一度呼べば済む。
F-156 で計画した「cave に `0x4A` バイトを確保して 7 フィールドを写す」は不要だった。

### 6. ケーブ（`PATCHES/cave_text_emit.py`、実機で検証済み）

`0x4B7DCC` の `MOV R2,#0`(`0xE3A02000`) を `B 0x01E81C00` に差し替える。

```
+00  E59FC02C  LDR   R12, =TARGET_TB
+04  E156000C  CMP   R6, R12
+08  1A000007  BNE   skip
+0C  E52DE004  PUSH  {LR}
+10  E1A01000  MOV   R1, R0          cursor
+14  E1A00004  MOV   R0, R4          desc（完成済み）
+18  E59F2018  LDR   R2, =COLOR
+1C  E5802004  STR   R2, [R0,#4]     desc+0x04 = 自前の色
+20  E3A02000  MOV   R2, #0          a3 = 0
+24  EB994D78  BL    TextBatch_CopyToCommandBuffer
+28  E49DE004  POP   {LR}            R0 = 進んだ cursor
+2C  E3A02000  skip: MOV R2, #0      ← 元命令
+30  EA98D866  B     0x4B7DD0
+34  .word TARGET_TB
+38  .word COLOR
```

`CopyToCommandBuffer` は AAPCS 準拠で R4-R11 を保存するので、
`R4`/`R5`/`R6` はそのまま使える。壊れるのは R0-R3/R12/LR だけ。

**`a3 = 0` が安全な根拠**: `a3` は `batch+9` の bit1 が立つ indexed 経路でしか
参照されない。会話 TextBox は 3 つとも `batch+9 == 0x00`（直接コピー経路）で、
live で確認済み。これで F-154 の `drawctx[417..419]` 二重更新 SIGSEGV を回避できる。

### 7. 位置について（未解決）

2 枚目は **1 枚目と完全に同じ位置**に重なった。
状態プリフィックス（`TextDraw_EmitStatePrefix`）を積み直していないため、
1 枚目が積んだ変換行列をそのまま使っているからである。

**好きな位置に出すには、自前の状態プリフィックスを積む必要がある。** → F-158 で解決

---

