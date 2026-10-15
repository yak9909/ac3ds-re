---
id: ACNL-F0038
aliases:
- F-146
title: 'F-146: TextBox batch は固定0x60-byte seedとglyph/state blockから構成される — `MEDIUM`（静的＋停止中live照合）'
summary: '`TextBatch_BuildCommandStream` (`0x4D6570`) の命令列を、F-145 の同一会話名'
date: '2026-09-08'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5072240
- 5072344
- 9099824
- 5074144
- 5074052
- 5067276
- 5078768
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:630-667
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-146: TextBox batch は固定0x60-byte seedとglyph/state blockから構成される — `MEDIUM`（静的＋停止中live照合）

`TextBatch_BuildCommandStream` (`0x4D6570`) の命令列を、F-145 の同一会話名
`T_nam_00` batchの停止中メモリと照合した。入力は描画context (`R0`) とスタック上の
TextWriter (`R1`) で、batchは `TextWriter+0x44` にある。

最初に `0x4D65D8` が定数領域 `0x8ADA30` の **0x60 bytes（24 dwords）**を
`batch+0x10` へコピーして `batch+0x1C=24` とする。live batch
`0x32D22FD8` の source `0x32D23190` 先頭0x60 bytesを実読すると、`0x8ADA30` と
byte-for-byte一致した。従ってこれはTextBoxごとの文字列ではなく、すべてのbatchに
共通の初期PICA command templateである。

以降はglyph instanceのtexture/state切替と頂点情報をcontext側の一時領域へ貯め、
`0x4D6CE0` が必要時および終了時にそのblockを `batch+0x10 + 4*(batch+0x1C)`へ
コピーしてcountを進める。最終的に control byte `+9` のbit1が立つ場合だけ、
`0x4D6C84` で `nwgfx_GspGpu_RangeCacheOp_1F` を発行する。F-145の標本は
`+9=0` であり、`batch+0x10`の158 dwordsがそのまま後段copyされた。

また `0x4D520C` が前置する0x60-byte header内の64-byte色payloadは、
`TextDraw_BuildFourCornerColors` (`0x4D7EF0`) が二つのRGBA8色をfloat化して
四頂点色へ展開したものだった。selector 0/1/2 は順に、単色／corner 1・3を第2色／
corner 2・3を第2色にする。この関数はIDBへrename/comment済みである。

**含意（限定）**: 正規TextBox経路が既に生成したbatchは、固定seedと文字依存blockを
含む再利用可能なcommand sourceであり、F-145のlist 32→main list replayに安全に載る。
ただしこの結果だけでは、描画contextの全field、個々のPICA registerの意味、atlas handleの
materialize時点、または新規TextBoxを安全に所有・破棄する方法は確定しない。独立した
自前テキスト生成にはそれらのどれかを追加で解く必要がある。

**根拠**: `0x4D6570`/`0x4D6CE0`/`0x4D7EF0` のARM assembly、`0x8ADA30`のraw bytes、
停止中の `0x32D22FD8` headerと `0x32D23190` sourceのraw bytes、F-144の実機TextBox
入口観測、およびF-145の後段全byte比較。`0x4D6570`自体をこのbootでbreakpoint捕捉しては
いないため、context内の全PICA stateの意味は `MEDIUM` に留める。

確定した結果と根拠。confidence は `CLAUDE.md` の定義に従う。

---

