---
id: ACNL-F0342
aliases:
- F-316
title: 'F-316: ★シート記述子 `+0x0C` は **`(幅<<16) | 高さ`** — HIGH'
summary: 256x128 のシートに載せ替えたら、**文字が完全に化けた**（画素が散る）。
date: '2026-09-06'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8388864
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:20944-20996
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-316: ★シート記述子 `+0x0C` は **`(幅<<16) | 高さ`** — HIGH

### 症状

256x128 のシートに載せ替えたら、**文字が完全に化けた**（画素が散る）。
CMAP も CWDH も UV も正しい（F-315 D）のに絵にならない。

### 真因

`own_font_data.py` は記述子 `+0x0C`（PICA reg 0x082）を

```
(SHEET_H << 16) | SHEET_W
```

と書いていた。**正しくは `(SHEET_W << 16) | SHEET_H`。**

実機で 1 語だけ `0x00800100` → `0x01000080` に入れ替えたら、
**「チートメニュー」「変更を適用しますか？」「プレイヤー ABC 0123」が正しく出た。**

### なぜ今まで気付かなかったか

**F-303 / F-305 のアトラスは 128x128 の正方形**だったので、
`(H<<16)|W` と `(W<<16)|H` が**同じ値**になる。
非正方形のシートを載せて初めて露呈した。

> ★**正方形で検証した値は、非正方形で崩れる可能性がある。**
> 幅と高さを詰める順序は、**寸法が違う値で 1 度は確かめる。**

### Picture の texMap は正しかった

同じ疑いがあったので、Picture の UV を 'A' の字形セルに向けて実機で確かめた。
320x70 のパネルに 'A' が 3 列 x 8 行で拡大表示され、**期待する字形と完全一致**した。

```
texMap +0x08 = (H<<16)|W   +0x0C = (H<<16)|W   +0x18 = (W<<16)|H
```
はこのままでよい（記述子 `+0x0C` とは詰め方が違う）。

★このとき最初「1 行違う」と読み違えた。原因は**標本点に上の白文字が掛かっていた**こと。
  重ね描きしたものの上から画素を測らない。

### 直した場所

| ファイル | |
|---|---|
| `PATCHES/own_font_data.py` | `_p32(de, 0x0C, (W<<16)|H)` へ |
| `Plugin/.../Sources/GuiV2.cpp` | `W32(desc + 0x0C, (kFontSheetW << 16) | kFontSheetH)` へ |

`verify_own_font.py` / `verify_plugin_port_v2.py` とも 0 件。`gohan.3gx` も再ビルド済み。

---

