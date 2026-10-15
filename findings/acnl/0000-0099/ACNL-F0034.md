---
id: ACNL-F0034
aliases:
- F-145
title: 'F-145: TextBox batch は専用list 32で構築され、メインlistへ再生される — `HIGH`（静的＋実機）'
summary: software BPを使わず、`scratchpad/trace_text_batch_submit.py` で会話名TextBoxのbatch
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5067276
- 9420924
- 4947404
- 5067744
- 5067776
- 5075316
- 7583012
- 5670612
- 8062612
- 5669864
- 1048576
- 8063528
- 8063680
- 5669596
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:484-532
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-145: TextBox batch は専用list 32で構築され、メインlistへ再生される — `HIGH`（静的＋実機）

software BPを使わず、`scratchpad/trace_text_batch_submit.py` で会話名TextBoxのbatch
`0x32D22FD8`だけを比較して `TextBatch_CopyToCommandBuffer` (`0x4D520C`) を採取した。
対象は vptr `0x8FC07C`、pane名 `T_nam_00`、文字列「クロベエ」（4文字）で、停止時の値は:

| 項目 | 実値 |
|---|---:|
| descriptor / batch | `0x32FF609C` / `0x32D22FD8` |
| `0x4D520C` の `R1` | `0x327DEAB8` |
| glyph count / command count | `4` / `158 dword` (`632 bytes`) |
| source | `0x32D23190` (`batch+0x10`) |
| control byte `+8/+9` | `1 / 0` |
| caller LR | `0x4B7DCC` |

`control+9` bit1が0なので、静的命令 `0x4D53E0`〜`0x4D5400` は `Mem_Copy` を選ぶ。
`0x4D520C` は先に `0x60 bytes` のPICA状態コマンドを書き、その後batch sourceを連結する。
実機停止メモリで **source `0x32D23190` の632 bytesと destination
`0x327DEAB8+0x60` が全バイト一致**し、copy終端は `0x327DED90` だった。

同じtraceで、構築中のcommand-listを次のように確認した。

| 項目 | 実値 |
|---|---:|
| selected list id / manager | `32` / `0x327DDC2C` |
| base / size / end | `0x327DDC80` / `0x9000` / `0x327E6C80` |
| `g_GpuCmdPtr` at TextBox entry | `0x327DDC80` |
| TextBox batch write offset | base `+0xE38` |

`nwlyt_DrawPaneTreeToCurrentList` (`0x4D7174`) は最初に `g_GpuCmdPtr` を取り、
`nwlyt_Pane_DrawRecursive` (`0x73B524`) がPane vtable slot `+0x68` の戻りポインタを
子Paneへ順に渡し、ツリー終了後にだけ最終ポインタを `g_GpuCmdPtr`へ書き戻す。
そのためTextBox処理中のglobal pointerがlist baseのままでも矛盾しない。
`ssys_ma_lyt_Layout_RecordPaneTree` (`0x5686D4`) はlist 32へ記録後、
`GpuCmd_CommitListAndCaptureDelta` (`0x7B0694`) でbyte/GX-queue範囲を保存する。

続いて `scratchpad/trace_layout_list_replay.py` で source list 32だけを採取した。
5秒で302回、`LR=0x5683E8`、source offset `0` / length `0x3270` / GX count `0`、
destinationはメインlist 1（manager `0x3229D06C`、base `0x3229D0C0`、size `0x100000`）
だった。`GpuCmd_ReplayRecordedListRange` (`0x7B0A28`) はこの範囲を現在のメインlistへ
統合する。今回 `allow_no_split=1` で、同関数内 `0x7B0AC0` の直接
`GpuCmd_SplitAndSubmit` 回数は0だった。従ってlist 32を個別submitするのではなく、
メインlistへ再生し、既知の通常フレーム終端submit経路（F-104）へ載せる。

**根拠**: 上記2本の対象限定trace、source/destination全632-byte比較、
`0x4D520C` / `0x4D7174` / `0x73B524` / `0x5686D4` / `0x7B0694` /
`0x5682DC` / `0x7B0A28` の `code.bin.i64` assembly。両traceは採取後にhookを先に戻し、
ケーブ・bufferを全ゼロへ復元した。現在BPも0件。

