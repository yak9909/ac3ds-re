---
id: ACNL-F0254
aliases:
- F-229
title: 'F-229: ★★★ケーブどうしの重なりは目視では見つからない。機械的に検査する — `HIGH`（実機）'
summary: '```'
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 10161408
- 8622080
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:13621-13647
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-229: ★★★ケーブどうしの重なりは目視では見つからない。機械的に検査する — `HIGH`（実機）

```
4B836C: got SIGSEGV signal (Segmentation fault)
```

`CAVE_V` を 33 語へ伸ばして `0x838880` に置いたが、`CAVE_F` が `0x838900` のままだった。

```
CAVE_V 0x838880 + 33 語 = 0x838904   ← 末尾がリテラル（0x009B0D00）
CAVE_F 0x838900                      ← ★1 語重なる
```

書き込む順が Q → F → ... → V なので、**V のリテラルが F の先頭命令（PUSH）を潰した**。
`DrawCtx_FlushBatch` のフックがそのゴミへ飛んで SIGSEGV。

### 対策

install の中で**総当たりで重なりを検査する**ようにした。
`.text` の空き（`0x838080`-`0x839000`）を出ていないかも同時に見る。

**`CLAUDE.md` は「ケーブの番地は機械的に突き合わせる」と書いていたのに、
人間（こちら）が目視で済ませていた。** 検査は**コードに入れないと守られない。**


---

