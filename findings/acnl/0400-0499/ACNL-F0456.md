---
id: ACNL-F0456
aliases:
- IDA-opus-5-F026
title: 描画中に資源を潰しても落ちない。モデルが黙って消えるだけ（2026-09-21、HIGH、実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T017b。**意図的に安全手順を破った試験の第2段。**'
date: '2026-09-21'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags:
- model
supersedes: []
source: IDA:work/FINDINGS.md:1119-1166
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F026: 描画中に資源を潰しても落ちない。モデルが黙って消えるだけ（2026-09-21、HIGH、実機）

解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T017b。**意図的に安全手順を破った試験の第2段。**
IDA-opus-5-F025（instance 側）の続きで、今度は **GPU が番地で直接読む資源側**を壊した。

### 段取りと結果

対象はカブトムシ1体、`bufferOption 0x834` で生成、ケーブが毎フレーム submit している状態。

| 段 | やったこと | 結果 |
|---|---|---|
| 1 | 描画中に**資源ヒープを解放**（`HeapAllocator_DestroyHeap`） | **何も起きない。** 描画も継続（`runs`/`submits` とも増え続ける） |
| 2 | 同じ大きさのヒープを親から作り直す | **別番地（`0x30F9E7B0`）に来た**ので同じ塊は返ってこなかった |
| 3 | 旧資源領域 **49,152 B を `0xDEADBEEF` で全部潰す** | **落ちない。ゲーム無傷。カブトムシだけが画面から消える** |
| 4 | 保存しておいた元の 49,152 B を書き戻す | **カブトムシがそのまま戻る** |

段1で何も起きないのは当然で、**解放はメモリの中身を消さない**。
危ないのは「解放」ではなく「**再利用されて上書きされる**」瞬間だと分かる。

### なぜ潰しても落ちないのか

`0xDEADBEEF` を float32 として読むと **-6.259853e+18**。
頂点座標がその桁になれば、三角形は視錐台のはるか外に出るので**何も描かれない**。
GPU は与えられた番地を読むだけで、中身が何であっても止まらない。

そして CPU 側も落ちない。`bufferOption = 0x834` で作った instance は
**マテリアルを自分側へ複製し、mesh ポインタ配列も自前で持つ**（IDA-opus-5-F023）。
描画時にコマンドを組む側が資源のポインタを辿ることが無いので、
資源が丸ごとゴミでも CPU は何も踏まない。**残るのは GPU が読む頂点・索引データだけ**で、
それが F022 の「instance は CPU だけ / 資源は GPU が直接読む」という分解の直接の裏付けになった。

### 3gx に持っていくべき教訓

- **失敗の形は「落ちる」ではなく「黙って消える」。**
  モデルが出ないとき、描画の呼び出しを疑う前に**資源の記憶が再利用されていないか**を見ること。
- 「submit をやめてから解放する」規則は、**この形の instance については落ちないための規則ではない**。
  絵を正しく保つための規則である。
- **ただし一般化しない。** 試したのは `0xDEADBEEF` 一様というパターン1種類だけで、
  もっともらしい浮動小数やポインタに化けるパターンなら別の壊れ方があり得る。
  別の `bufferOption`（材質を共有する形）なら CPU 側が資源を辿る可能性も残る。

根拠: `events.jsonl` の `t017b_*`、`t017b_before.json`、
`t017b_resource_original.bin`（sha `6752e2ed…`、書き戻しも一致）、
画像 `t017_drawing_before_free_top.png` / `t017b_resource_overwritten_top.png` /
`t017b_resource_restored_top.png`。
反証条件: 別のパターン、別の `bufferOption`、テクスチャを含むモデル、
資源が**未マップ**になる場合（ヒープ内の再利用では常にマップされたまま）。

