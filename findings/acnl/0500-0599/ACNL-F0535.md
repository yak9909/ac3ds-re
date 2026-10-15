---
id: ACNL-F0535
aliases:
- IDA-opus-5-F033
title: 村の 1 マス = world 32 単位。UnitCursor の原点は quad の中心（2026-09-22、HIGH、実機＋CGFX）
summary: '解析ソフト: IDA / 解析モデル: opus-5。**独立な 2 経路が一致したので確定とする。**'
date: '2026-09-22'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:3434-3481
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F033: 村の 1 マス = world 32 単位。UnitCursor の原点は quad の中心（2026-09-22、HIGH、実機＋CGFX）

解析ソフト: IDA / 解析モデル: opus-5。**独立な 2 経路が一致したので確定とする。**

### 1. 実機の合わせ込み（利用者）

「1マスの間隔=32、カーソルの拡大率=100 でした」。
拡大率 100% で小道のタイルに重なり、間隔 32 で 1 マス移動が隣に乗った。
つまり **1 タイル = 32、モデル素寸 U = 32 / (100/100) = 32**。

### 2. ファイル側（`artifacts/update/romfs/Ftr/Chip/UnitCursor.bcres`）

CMDL は `0x150`。実体の shape は **SOBJ `0xDB0`**（typeId `0x10000001`。
`0x810` にも SOBJ のマジックがあるが typeId `0x01000000` で中身は空）。
そのバウンディングボックス（`0xE00` から 15 float）:

| 欄 | 値 |
|---|---|
| centre | **(0, 0, 0)** |
| orientation | `(0,1,0) (0,0,1) (1,0,0)`、行列式 **1.0**（正規直交） |
| size | **(32, 32, 0)** |

**size が 32x32 で、利用者が実機で出した 32 と完全に一致する。**
平らな quad（厚み 0）なのもカーソルとして整合する。

### 3. これが決めること：丸め先はマスの**中心**

**centre が (0,0,0) で size が 32 ということは、モデルの原点が quad の中心**（−16〜+16 に広がる）。
だから `floor(p/32)*32` で丸めるとカーソルの**中心がマスの境界に乗る**。
利用者が見た「大きさの半分ズレる」はこれ。正しくは `floor(p/32)*32 + 16`。

### 4. もう一つの報告：間隔を変えるとカーソルが飛ぶ

丸めを `PoseAll` のたびにかけていたので、間隔を変えると `floor` の落ち先が変わり、
基点がその都度 0〜間隔 の幅で飛んでいた。**丸めるのは出した瞬間の 1 回だけ**でよく、
そうすれば利用者の要望「グリッドに合わせた状態で出現してほしい」とも一致する。

### 5. F032 の候補は外れていた

F032 で「3 マスでズレが消える」から T = 36/k として 9 か 18 と書いたが、**正解は 32**。
観測を厳密な倍数関係として扱ったのが誤りで、実際は 3x12 = 36 が 32 に近いために
「重なったように見えた」だけだった。**目視の「ちょうど合う」を数式の等式にしないこと。**

根拠: `tools/models3d/model_extent.py`（出力 `work/evidence/models3d/model_extent.json`）、
利用者の実機報告（2026-09-22）。
反証条件: ボックスが頂点の実範囲と違う（頂点ストリームを復号していない）、
小道のタイルとカーソルの一マスが別寸法、マス目の位相が world 0 基準ではない。

