---
id: ACNL-F0032
aliases:
- F-154
title: 'F-154: TextBox emitter直呼びも live DrawContext を二重更新する — `HIGH`（静的＋同一例外の再現）'
summary: F-153を通過したdirect-emitter版（`TextBox_EmitBatchToGpuCommands=0x4B7CE0`）は、wrapperを
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4947168
- 1185500
- 5670696
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:421-437
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-154: TextBox emitter直呼びも live DrawContext を二重更新する — `HIGH`（静的＋同一例外の再現）

F-153を通過したdirect-emitter版（`TextBox_EmitBatchToGpuCommands=0x4B7CE0`）は、wrapperを
通らないにもかかわらずF-152と同じ `PC=0x001216DC (GpuCmd_SelectList)` でSIGSEGVした。
例外時LR=`0x00568728` は `ssys_ma_lyt_Layout_RecordPaneTree` の list選択直後、stackは
`sub_566EA0` → frame draw passへ連なる。従ってwrapper固有の事故ではない。

静的にemitterは末尾で `TextBatch_CopyToCommandBuffer(v13, v11, drawctx)` を呼ぶ。
同関数は `a3!=0` のとき `a3+0x684/+0x688/+0x68C`（decompiler offsets 417..419）を更新し、
command rangeの開始・終端・後処理pointerを追跡する。native textの後に同じdrawctxへclone textを
二重submitするとこの所有状態を破壊し、後段のlist selectionが無効nodeを辿る。

よって安全な次候補はemitter/wrapperを呼ばず、`TextBatch_CopyToCommandBuffer` を直接使い
**第3引数を0**にすること。必要なper-submit descriptor (`v13`) はnativeのものをprivate copyして
batch pointerなどを設定する。この仮説はまだ未実装・未検証である。危険なdirect-emitter版は
`ALLOW_UNSAFE_DIRECT_TEXT_EMIT=False` によりinstallを拒否する。

