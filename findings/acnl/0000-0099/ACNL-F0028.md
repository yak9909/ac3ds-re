---
id: ACNL-F0028
aliases:
- F-155
title: 'F-155a: submit-descriptor recorder は描画前のレジスタ連鎖で例外 — `HIGH`（例外位置＋機械的監査）'
summary: '`scratchpad/trace_main_text_submit_descriptor.py` の初版は'
date: '2026-09-08'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5067276
- 4947404
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:349-372
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-155a: submit-descriptor recorder は描画前のレジスタ連鎖で例外 — `HIGH`（例外位置＋機械的監査）

`scratchpad/trace_main_text_submit_descriptor.py` の初版は
`TextBatch_CopyToCommandBuffer (0x004D520C)` の入口で本文 `T_msg_00` の descriptor を
記録するだけのobserverだった。しかし初回実行で `PC=0x01E81A54` にSIGSEGVした。
この位置は記録cave内の descriptor field読取りであり、native `TextBatch_Copy` 本体には
まだ到達していない。

原因は初版が `LDR R0,[R0,#0]` の後も `R0` をdescriptorとして使い、次の
`LDR R0,[R0,#4/#0x18...]` をfield値から連鎖参照したことだった。停止時stackに保存された
元引数は `R0=0x32FF609C`、`R1=0x327DF6F8`、`R2=0x32FF62EC`、
`R3=0xBF800000`、`LR=0x004B7DCC` で、例外前のnative呼出し文脈自体は有効だった。

フックをstock `0xE92D41F0`へ戻し、保存済み `R0-R3/R12/LR`、`SP+0x18`、
`PC=0x004D520C` を復元してからcave/bufferをzero化した。これはこのPC・PUSH mask・
副作用なしを確認した例外だけに有効な復旧である。Resume後、ゲームが正常復旧したことを
ユーザーが確認した。以後の修正版はdescriptorをR0に保持し、
全fieldをR12へ読むようにした。generator auditは140 bytes・branch/literal・全7fieldの
非連鎖loadを確認するが、**旧caveを実行した同一bootではI-cacheのため再適用しない**。
`ALLOW_TRACE_INSTALL=False` のまま、fresh bootで再監査するまでinstallを拒否する。

この失敗ではdescriptor値を取得できていない。従ってprivate descriptorによる
`TextBatch_CopyToCommandBuffer(..., a3=0)` 仮説（F-154）は未検証のままである。

