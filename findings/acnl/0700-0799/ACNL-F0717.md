---
id: ACNL-F0717
aliases: []
title: "ResFontシート記述子とCWDH・CMAP可変長要素"
summary: "ResFontのシート記述子は0x14バイトで、変換後GPUアドレス>>3と高さ/幅を持つ。CWDH幅列は+8から3バイト刻み、CMAP方式2は+0xCのu16件数に続き+0xEから4バイトの文字/glyph対を置く。"
date: 2026-10-19
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # 静的な生産側と独立した消費側。実機なし
tool: IDA
addresses: [0x00141B48, 0x001426C8, 0x0013C518, 0x00743768, 0x007438B4]
tags: ["font", "layout"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: auto
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

`NwFontGlyphTextureDescriptor`、`NwFontCmapScanPair`、`NwFontCmapScanPrefix` を型にし、ResFont/Glyphのvoid*をdescriptorポインタへ置き換えた。CWDH/CMAPは正規化された資源本体の固定先頭型で、配列を含む総サイズではない。確度 MEDIUM：初期化ループ・取得関数と独立したバッチ消費・文字検索が一致。実機なし。

| descriptor offset | 型・役割 |
|---|---|
| +0 | u32 texture_handle（通常のsheet初期化では0） |
| +4 | NwFontResFont *font |
| +8 | u32 physical_address_div8 |
| +C / +E | u16 height / width（低16bitが高さ） |
| +10 | u8 gpu_format |
| +11..13 | 未確認3B。Initは書かない |

CWDHは本体+8から `NwFontCharWidths[last_glyph-first_glyph+1]`、stride3。CMAP方式2は本体+0xCにu16 pair_count、本体+0xEに `NwFontCmapScanPair[pair_count]`。対は `{u16 character;u16 glyph;}`、文字順。件数と先頭対の間に2Bのpaddingを入れない。方式0は+0xCのu16差分起点、方式1は+0xCから範囲内文字のu16直表。元ファイルではこれら本体の前に8Bのchunk headerがある [ACNL-F0711]。

CWDHの `widths[]` と方式2先頭型の `pairs[]` は柔軟配列として定義した。IDAで各配列のoffset=8/0xE、固定sizeof=8/0xE、配列部分size=0を照合した。

## 根拠

- `_local/builds/acnl_jpn_v15/ida/work/100/primary.txt` の0x1426C8はTGLPの枚数だけ20B刻みでdescriptorを作り、引数にResFont自身、sheet_data+i*sheet_bytes、書式、幅、高さを渡す。
- 0x141B48はsheetが非nullなら0x143B54による変換後の値をLSR #3し+8へ保存。生の仮想ポインタを直接右シフトする説明は誤り。+10はSTRB、+E/+CはSTRHで幅/高さ。
- 0x7438B4はResFont+0xCをsheet_index*20で引いてGlyph+0x14へ置く。0x4D6570はdescriptor+8をテクスチャアドレス、+Cを寸法、+10のbyteをGPU書式として読む。
- 0x7438B4の字幅選択は範囲内glyphについて `cwdh+8+3*(glyph-first_glyph)` を読む。範囲外はFINFの既定幅。
- 0x743768はmethod=2で+0xCからu16件数を取り、+0xEを探索先頭、4B刻みの先頭u16を比較、続くu16を返す。method=0/1の入口も別に確認した。

## 反証条件・未確認点

- GPUへ数値書式を無変換で渡すことは確認したが、LA4という色成分名と数値9の対応は今回の一次命令だけでは独立に証明していない。推定Enum `LA4=9` は追加せずgpu_formatをu8に保つ。TexMap側のnw::lyt書式9と混同しない。
- descriptor末尾3Bの意味、CMAPの整列paddingやchunk総サイズは全資源で実測していない。探索が要求する文字順と上記内部配置を示す。
