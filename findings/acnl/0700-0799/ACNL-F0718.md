---
id: ACNL-F0718
aliases: []
title: "文字バッチのヘッダー・字形レコードと必要量"
summary: "文字バッチは0x28バイトの固定ヘッダー、44バイトの字形列、処理済みビット列、16バイト境界のコマンド列を持つ。+4の件数と+6の描画制限は、+0の確保上限とは別である。"
date: 2026-10-19
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # 静的な生産側と独立した消費側。実機なし
tool: IDA
addresses: [0x004D76BC, 0x004D5480, 0x004D76A8, 0x004D4EAC, 0x004D6570, 0x004D6CE0, 0x0013B9A8]
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

`NwFontTextBatchPrefix` の固定ヘッダーを補完し、`NwFontTextBatchGlyph` (0x2C)とInit/必要量関数の型を付けた。ヘッダー型のsizeofは割当全体ではない。確度 MEDIUM：初期化・glyph蓄積と、独立したcommand構築・送出・確保計算が一致。実機なし。

| header offset | 型・役割 |
|---|---|
| +0 | u32 max_chars、蓄積可能数 |
| +4 | u16 glyph_count、現在の蓄積数 |
| +6 | u16 draw_glyph_limit、初期値0xFFFF、構築時min(count,limit) |
| +8/+9 | u8 built / flags |
| +A | 未確認2Bを維持 |
| +C | u8* glyph_bits、グループ構築用の処理済みbit列 |
| +10/+14/+18 | 現在commands / 本来のcommand_buffer / aux_buffer |
| +1C/+20 | u32 command_words / command_word_capacity |
| +24 | u32 first_color_command_word、初回色commandの語offset |

字形は+28から44B刻み。順にfloat width,height_delta,x,y、u32 top_color,bottom_color、float u0,v0,u1,v1、descriptor*。height_deltaは負のglyph高さ×縦scale。bitmapはフォントの画素や字形データ本体ではない。

最大字数N、先頭実アドレスB、alignK(x)=(x+K-1)&~(K-1)、b=(N+7)>>3とすると、Initが置く実ポインタは次のとおり。

```
glyphs = B + 0x28
glyph_bits = B + 0x28 + 44*N
command_buffer = align16(glyph_bits + b)
command_word_capacity = (78*N + 57) & ~3
```

コマンド列末尾までの実アドレス依存サイズは `command_buffer-B + 4*command_word_capacity`。ゲームのCalcDrawBufferBytesが返す式は別途、`align16(0x28+44*N+align4(b)) + 4*command_word_capacity`。ゲーム側の数式を任意のBに対する一般保証としない。Bが16B境界ならこの式で末尾を覆うが、4B境界だけでは実command先頭offsetが同式の前半より大きくなる組がある。道具での例はN=15/B%16=4で実offset716、計算前半704。実際に不足が発生した実機標本ではなく、命令式同士の差である。

通常TextBoxは文字列 `2*(N+1)` Bを別確保する。flags bit3を使う経路はCalcDrawBufferBytesを16Bへ丸めた主領域にさらに `4*word_capacity` Bの補助領域を加え、+18へその先頭を置く。通常flags=0の主領域と二重化経路を混同しない。

ヘッダー末尾の `glyphs[]` は柔軟配列として定義した。IDAでoffset=0x28、固定sizeof=0x28、配列部分size=0を照合した。

## 根拠

- `_local/builds/acnl_jpn_v15/ida/work/100/primary.txt` の0x4D76BC、0x4D4EAC、0x4D6570、0x4D6CE0、0x4D5480、0x4D76A8、0x13B9A8。計算例は `_local/builds/acnl_jpn_v15/ida/work/100/calculations.json`。
- Initの0x4D76D4/D8は+6=0xFFFF、+4=0。0x4D7700..14は44N後のbitmapと、その末尾の16B切上げを保存。0x4D7718..28は必要word数とcommandsを保存する。
- glyph書込0x4D4F50..88は+0のu32上限と+4のu16を比較して蓄積し、レコードの全欄を0x4D4F90..FC0で保存する。xはwriterからのfloatレジスタS0、yはwriter+30。UVはglyphのcell座標とsheet寸法から作る。
- 0x4D6570の冒頭はmin(glyph_count,draw_glyph_limit)を取り、bitmapを0にしてから同sheetのglyphを集め、処理後のbitを立てる。+6は予約容量として使われない。
- 0x4D6CE0は初回の色command位置を+24へ保存し、以後のflushで判定する。+1Cは蓄積word数でありbyte数ではない。0x4D520Cが4倍して送出する。
- 0x4D5480の整数命令はbitmapを4Bへ切上げ、44Nと0x37を足し16Bを切下げる。0x4D76A8の結果を4倍して加算。0x13B9A8は通常align4で確保し、bit3経路ではalign16と補助列を用いる。

## 反証条件・未確認点

- +Aの2B、flags全ビットの意味は未確定のため未命名。+6をallocation capacityへ改名しない。コマンド使用量が常に予約量まで増えるという意味ではない。
- Nが大きいとu16件数と32bit算術の折返しがあり得る。式は非overflow範囲の配置を表し、任意Nで確保/描画成功する保証ではない。
- Bの実機整列分布、算術差が実際にbuffer超過へ至るか、GPU処理完了と寿命は未実測。
