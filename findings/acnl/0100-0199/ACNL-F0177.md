---
id: ACNL-F0177
aliases:
- F-140
title: 'F-140: TextBox→TextWriter の描画入口と後処理 — `MEDIUM`（静的）'
summary: '`nwlyt_TextBox_DrawText` (`0x4BB1E8`) の命令列から、標準テキスト描画を再利用する最小の'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 4960744
- 4960816
- 4960832
- 4960884
- 4960888
- 5066412
- 4960892
- 4960904
- 4960908
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:9060-9083
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-140: TextBox→TextWriter の描画入口と後処理 — `MEDIUM`（静的）

`nwlyt_TextBox_DrawText` (`0x4BB1E8`) の命令列から、標準テキスト描画を再利用する最小の
入口と、描画後に必要な状態復元を分離できる。

- `0x4BB230` で 0x64 バイトの一時 `TextWriter` を `sub_7E8488` により初期化し、
  `0x4BB240` (`nwlyt_TextBox_ConfigureTextWriter`) が TextBox の font、サイズ、spacing、
  pane width、flags、描画 context を writer へコピーする。
- `0x4BB274` で `R0=SP`（その一時 writer）を準備し、`0x4BB278` の
  `BL sub_4D5858` が `writer+0x40` の persistent context を用いて texture/shader/
  attribute state を準備する。`sub_4D5858` の後に writer の `+0x44` が batch buffer に
  なる場合は、glyph は `0x4D4EAC` の 44-byte instance 経路へ入る。
- `0x4BB27C`〜`0x4BB288` で `TextBox+0xD4` の UTF-16 文字列と `TextBox+0xFA` の長さを
  `sub_7E7F48` へ渡す。同 wrapper は `nwfont_TextWriter_DrawString` を呼び、各 glyph の
  CMAP/CWDH/TGLP 解決と quad 生成を行う。
- `0x4BB28C` の `sub_4D7730` は draw 後に GPU channel をリセットし、次の UI 部品へ状態が
  漏れないようにする。したがって自前 callback から標準 glyph 経路を呼ぶ場合も、同じ
  render pass の有効な context と、この後処理の対を維持する必要がある。

これは `0x4BB278` で実機 TextWriter/context を捕捉する静的に裏付けられた測定点である。
ただし表示済み会話を保持したままだと TextBox が再描画されず、この BP が未ヒットだった。
`TextBox_DrawText` の仮想呼出し元、live writer/context の所有権、及び自前 `FuncNode` の
render pass から同じ context を使えるかは動的捕捉後に確定する。

