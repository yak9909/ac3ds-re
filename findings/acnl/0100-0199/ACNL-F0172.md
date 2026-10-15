---
id: ACNL-F0172
aliases:
- F-134
title: 'F-134: EmitGlyphQuad の texture handle 選択と batch/immediate 分岐を静的再監査 — `MEDIUM`'
summary: '`nwfont_CharWriter_EmitGlyphQuad` (`0x4D4EAC`) の全分岐を静的に再読した。'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5066412
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:8899-8930
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-134: EmitGlyphQuad の texture handle 選択と batch/immediate 分岐を静的再監査 — `MEDIUM`

`nwfont_CharWriter_EmitGlyphQuad` (`0x4D4EAC`) の全分岐を静的に再読した。

### descriptor あり（通常の immediate 経路）

`glyph+0x14` が 0 でない場合、その先の descriptor `+0` を texture handle として読む。
handle が 0 なら `sub_7A8B08(1, &local_handle)` で 1 個だけ遅延生成し、descriptor `+0`
へ書き戻す。既存・新規いずれの場合も `sub_7A6558(3553, handle)` で texture target
3553 を bind し、`nwfont_CharWriter_SetGlyphTextureParams` へ sheet 寸法・format・raw
base・filter flags を渡す。

### descriptor なし（共有 texture context 経路）

`glyph+0x14 == 0` の場合は writer `+0x40` context の `+4` にある共有 handle を使う。
raw sheet pointer を context `+0xE4` と比較・更新し、変化した場合だけ texture parameter
設定を更新してから draw へ進む。

### batch 経路

writer `+0x44`（`a1+68`）が非 nullなら、texture bind/parameter設定を行わず、44-byte の
glyph instance（位置・色・UV・descriptor pointer）を配列へ追記して即 return する。
この場合の texture 処理は後段の batch submit 側が担当する。即時経路は最後に
`sub_7A7FAC(6, 0, 4)` へ tail-call する。

従って自前 GPU callback へ native text を移植する際は、まず **descriptor を直接使う
immediate 1 glyph** に限定するのが安全である。batch instance を再利用する場合は、
descriptor pointer と後段の submit/状態復元まで別途追跡しなければならない。これは
静的な branch/引数からの結論で、実機の handle 生成時点と batch 側の描画結果は未検証。

---

