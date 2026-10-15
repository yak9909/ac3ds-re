---
id: ACNL-F0168
aliases:
- F-130
title: 'F-130: ResFontのCMAP代替処理を確定。全liveフォントは2種の線形フィルタflagがON'
summary: 'confidence: **CMAPと代替処理 HIGH** / **filter flagの意味 HIGH**'
date: '2026-08-24'
category: text
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7616360
- 7617100
- 7616692
- 5076084
- 7617064
- 7617048
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:8671-8729
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-130: ResFontのCMAP代替処理を確定。全liveフォントは2種の線形フィルタflagがON

confidence: **CMAPと代替処理 HIGH** / **filter flagの意味 HIGH**

### 1. CMAP lookupと代替glyph

`nwfont_ResFont_MapCharToGlyph`(`0x743768`) は、`ResFont+8` の内部情報 `+16` から
CMAP連結リストを辿り、次の3方式でUTF-16 codeをglyph indexへ変換する。

| method | 実装 |
|---:|---|
| 0 | 範囲先頭glyphからの連番 |
| 1 | code範囲に対応するu16テーブル |
| 2 | `(code, glyph)` ペアを二分探索 |

見つからなければ `0xFFFF`。`nwfont_ResFont_HasGlyph`(`0x743A4C`) はこの戻り値を
そのまま判定する。`nwfont_ResFont_GetGlyph`(`0x7438B4`) は `0xFFFF` の場合、
内部情報 `+2` のalternate glyphへ置き換えてからCWDH/TGLPを解決する。

実機CMAP/CWDHの直接読出し:

| font | U+0030 / U+0036 / U+0037 | alternate glyph | alternate逆引き |
|---|---|---:|---|
| 通常24px | `0x0010 / 0x0016 / 0x0017` | `0x140B` | `U+E03A` |
| 7px | **全て `0xFFFF`** | `0x0000` | **`U+3041「ぁ」`** |
| 大40px | `0x0002 / 0x0008 / 0x0009` | `0x0000` | `U+0020` |
| counter26 | `0x0005 / 0x000B / 0x000C` | `0x0000` | `U+0020` |

したがって7px試験で見えた2つの「あ」状の文字は、元の `0` と `6` がともに欠落し、
各々が正確には **`U+3041「ぁ」`** のglyph 0へ置換されたもの。2文字が同じglyphへ
置換されたことと、7pxを `18 x 24` へ拡大したことが折り返しの原因になる。

### 2. 幅と位置差

| font | linefeed / cell系3値 | `0` CWDH | `7` CWDH |
|---|---|---|---|
| 通常 | `24 / 24,18,18` | `(left=0,glyph=11,advance=12)` | `(1,10,12)` |
| counter | `26 / 26,24,17` | `(0,15,16)` | `(1,14,16)` |

時計TextBoxの要求サイズ `18 x 24` に対し、counterは横 `18/24 = 0.75`、縦
`24/26 ≈ 0.923` に縮小される。advanceは `16 * 0.75 = 12` で通常版の12と一致するため、
文字列バッファやadvanceが増えたのではない。baseline系の値は18→17へ変わるため、
縮小と合わせた上方向の可視位置差、および輪郭・丸めによる横方向の見え方の差が残る。

### 3. 線形フィルタ

全4個のlive ResFontで `ResFont+16 = 0x00000006`。`nwfont_ResFont_SetLinearFilter`
(`0x4D7474`) は
ここへ `(a2 << 2) | (a3 << 1)` を保存し、全glyph-sheet texture descriptorを破棄・再生成する。
vtableの続く2関数 `0x743A28` / `0x743A18` はそれぞれbit2 / bit1を返す。

2個のboolをともにOFFにして7px版を再生成すると、拡大された「ぁ」はぼやけなくなり、
輪郭がくっきりしたドット表示へ変化した。文字置換・大きさ・折り返しは変わらなかった。
静的なtexture再生成処理とこの直接視覚比較が一致するため、拡大時・縮小時のLINEAR filter設定と
確定し、関数を `nwfont_ResFont_SetLinearFilter` へrenameした。**HIGH**。
読出しスクリプトは `scratchpad/dump_font_maps.py`。

---

