---
id: ACNL-F0346
aliases:
- F-319
title: 'F-319（2026-09-06）: UI フォントを CTRPF プラグインへ組み込む'
summary: '**confidence: HIGH**（静的検証 8 群 + **実機で描画を確認**）'
date: '2026-09-06'
category: text
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags:
- font
supersedes: []
source: v1:RE/FINDINGS.md:21148-21207
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-319（2026-09-06）: UI フォントを CTRPF プラグインへ組み込む

**confidence: HIGH**（静的検証 8 群 + **実機で描画を確認**）

> 利用者確認: 2026-09-06「実際には問題なく描画されました」。
> 一式は **`BASELINE/gui_v2_ok_f319/`** に凍結（退避は `BACKUP/f319_uifont_20260906/`）。

`GuiV2.cpp` が使うフォントを `GuiFontNw.h`（5x7 ASCII 61 字 / 128x128 /
CMAP 方式 0 / CWDH 無し）から **`GuiFontUi.h`** へ入れ替えた。
F-315 でデバッガ側が実機成功させた資源と同一。

```
美咲ゴシック第2 362 字 + PixelMplus 数字 27 字 + 塗り潰し 1 = 390 字形
256x128 LA4 の 1 枚に同居。CWDH 1 ノード（両書体で共有）
CMAP は書体ごとに 1 本（方式 2 = ソート済みの対を二分探索）
ResFont / FINF / TGLP / 記述子 は書体ごとに 1 組（0x80 刻み）
```

### 呼び出し側から見た変化

| | 前 | 後 |
|---|---|---|
| `DrawText` | ASCII をそのまま UTF-16 へ | **UTF-8 を復号**。`GuiV2::Font` で書体を選ぶ |
| 幅 | `字数 x 送り` | **CWDH の送りの合計**（可変幅） |
| `TextBox +0xE0` | 1 つの ResFont | **行ごとに切り替え** |
| `+0xE4/+0xE8` | `kFontGlyphW`/`kUiCellH` | `kUiMetricW`/`kUiMetricH` -> 倍率 1 |
| 安全弁 | `204 x 枚 + 48 x バイト数` | **`552 x 本数 + 48 x 字数 + 204 x 枚数`** |
| `LIST_SIZE` | ケーブ既定 `0x8000` | **A1 `0x10000` / A2 `0x8000`** に焼き直す |

### 落とし穴

1. **CMAP 方式 2 のノード長は `0x0E + 4n`**（`0x0C + 4n` ではない）。
   `+0x0C` が対の件数 2 バイト、対は `+0x0E` から。
2. **字形の無いコードは書かずに飛ばす。** 書くとゲームは代替字形
   （`FINF+0x02` = 0）を描くのに、こちらは幅 0 と数えるので
   **ペイン幅が足りず中央揃えがずれる**（F-311 の半画素ずれと同型）。
3. 要求サイズは `FINF+0x15/+0x14`（= `kUiMetricW/H` = 8）と同値にする。
   セル幅 7 を入れると倍率 8/7 になる。

### 実行時に書き換える 1 語（A1/A2 の語 79）

**リテラルであることを静的に確認した**（`verify_plugin_port_v2.py` 群 1）。
全 `LDR Rd,[PC,#±imm]` を復号して参照先を集め、語 79 を読む LDR が語 19 に
あること・リテラル領域が語 74 から始まることを確かめている。
★マスクは `w & 0x0F7F0000 == 0x051F0000`。**U ビット(bit23)を含めない**
（F-318 で `0x059F0000` と書いて「LDR 0 本」を「異常 0 件」と誤読した）。

### 検証

`own_font_data.py` に **`build_ui` / `build_ui_cwdh` / `build_ui_cmap` /
`ui_map_char` / `ui_advance` / `ui_measure`** を足し、そちらを正本にした。
`verify_plugin_port_v2.py` の群 2/3 を書き直して、`GuiV2.cpp` の
`WriteOneFont` / `WriteCwdh` / `WriteCmap` を 1 バイトずつ突き合わせる。
照合 3 本（`verify_plugin_port_v2` / `verify_spec_v2` / `make_font_ui` 内蔵）
すべて 0 件。**実機で描画を確認**（2026-09-06）。

詳細: `scratchpad/MEMO_f319_ui_font_plugin.md`

---

