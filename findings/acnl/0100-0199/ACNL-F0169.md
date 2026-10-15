---
id: ACNL-F0169
aliases:
- F-131
title: 'F-131: TextBoxの折り返しはpane幅、縦方向は非clip。右端欠けの境界はCWDH glyphWidth'
summary: 'confidence: **折り返し・縦方向非clip・描画矩形 HIGH** / **右端の見た目の最終原因 MEDIUM**'
date: '2026-08-24'
category: text
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4959608
- 4959676
- 8290212
- 8291192
- 8291204
- 8291208
- 8291216
- 8291256
- 8291304
- 7616692
- 5066412
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:8730-8783
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-131: TextBoxの折り返しはpane幅、縦方向は非clip。右端欠けの境界はCWDH glyphWidth

confidence: **折り返し・縦方向非clip・描画矩形 HIGH** / **右端の見た目の最終原因 MEDIUM**

### 1. TextBoxのpane幅がそのまま折り返し幅になる

時計本文 `T_time_0` と影 `S_time_0` を再起動後にも再探索し、いずれも次のstock値を確認した。

| field | 値 |
|---|---:|
| pane width / height (`TextBox+72/+76`) | `26.0 / 21.6` |
| requested font width / height (`+228/+232`) | `18.0 / 24.0` |
| char spacing / line spacing (`+236/+240`) | `0.0 / 0.0` |
| string capacity / current chars (`+248/+250`) | `6 bytes / 2` |

`nwlyt_TextBox_ConfigureTextWriter` (`0x4BAD78`) は `TextBox+72` のpane widthを
`TextWriter+76` へコピーする (`0x4BADBC`)。`nwfont_TextWriter_DrawString`
(`0x7E7FA4`) は、scaled line widthがこの値を超えると (`0x7E8378-0x7E8384`)、
現在文字を一時的に `0x000A` として扱って改行経路へ入れる (`0x7E8388-0x7E8390`)。

7px版fallback glyph 0のCWDHは `(left=0, glyphWidth=6, advance=7)`。
要求横幅18ではscaleが `18/7`、1文字のadvanceは `7*(18/7)=18`、2文字は36。
**36 > pane width 26** なので2文字目の前で自動折り返しされる。filterとは独立。

### 2. pane heightは描画をclipしない

`nwlyt_TextBox_ConfigureTextWriter` はpane widthだけをwriterへコピーし、pane heightは渡さない。
改行時はFont virtual `+0x4C` のlinefeedをvertical scale倍してY cursorへ加える
(`0x7E83B8-0x7E83E8`) が、`nwfont_TextWriter_DrawString` 内に高さとの比較はない。
1行stepは `7*(24/7)=24` で、pane height 21.6より大きい。

目視結果も「TextBox内で下側が切られた」のではなく、2行目がそのまま画面下端の外へ出た、
というユーザーの訂正と一致する。したがってこの経路のTextBoxは縦方向にpane clipしていない。

### 3. 右端の1〜3pxは文字列bufferやpane境界ではない

`nwfont_ResFont_GetGlyph` (`0x7438B4`) はCWDHのleft/glyphWidth/advanceをglyph record
`+4/+5/+6`へ格納する。`nwfont_CharWriter_EmitGlyphQuad` (`0x4D4EAC`) は
**glyphWidth byteだけ**を使い、次の両方を決める。

- quad右端: `currentX + glyphWidth * horizontalScale`
- texture U右端: `(cellX + glyphWidth) / sheetWidth`

7px glyph 0はTGLP cell width 7に対してglyphWidth 6なので、18px指定時のquad本体は
`6*(18/7)=15.43px`、cursor advanceは18px。残り約2.57pxはadvance側の余白になる。
これはユーザーが見た1〜3pxという量と一致し、文字列buffer容量6 bytesやpane幅26を越えて
メモリ上で描画した結果ではない。`EmitGlyphQuad` はそれらを参照しない。

ただし、見た目上「本来の右端のinkが失われた」のか、「1 source pixel分のadvance余白が
ドット拡大で目立つだけ」かは静的情報だけでは分離できない。次は折り返しを消した上で
`glyphWidth=6/7` またはnative `7 x 7` 表示を比較する。

---

