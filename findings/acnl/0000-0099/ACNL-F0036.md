---
id: ACNL-F0036
aliases:
- F-148
title: 'F-148: 既存Pictureを非所有cloneして、任意座標の2D背景として追加できた — `HIGH`（静的＋実機）'
summary: F-147で確定したPane-treeのcommit直前、`nwlyt_DrawPaneTreeToCurrentList` (`0x4D7174`) の
date: '2026-09-08'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5075316
- 5075384
- 9420796
- 7583012
- 7588696
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:556-597
by: unknown
original_by: ''
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ''
---
## F-148: 既存Pictureを非所有cloneして、任意座標の2D背景として追加できた — `HIGH`（静的＋実機）

F-147で確定したPane-treeのcommit直前、`nwlyt_DrawPaneTreeToCurrentList` (`0x4D7174`) の
`0x4D71B8` は、recursive Pane drawが返した最終cursorを `R1` に保持し、直後のstock codeが
`g_GpuCmdPtr`へcommitする境界である。ここでselected list idが32の場合だけ、会話Pane
`P_nam_00`をprivate caveへ0x158 bytesコピーし、リンクせずに
`nwlyt_Picture_DrawToCommandList(clone, final_cursor, original_R2, DrawContext)` を呼んだ。
返りcursorをstock commitへ渡すことで、既存treeの後ろに1枚のPictureを正規UI command stream
として追加できる。

cloneのPane transform `+0x80..+0xAC` はGPU command streamのuniform `0x20` payloadと同形であり、
今回 `+0x8C/+0x9C` を観測元の約`-126.0/-5.0`から`-50.0/-20.0`へ変更した。実機では元の
会話名前欄を変更せず、その少し右下に名前欄背景の別コピーが表示された。停止中にcloneは
`vptr=0x8FBFFC`、name=`P_nam_00`、material=`0x32D20170`、書換え後のtranslation値であることを
読み戻した。したがってこれはworld/shadow FuncNodeではなく、native 2D UI pass上での自前背景
panelの最小実証である。

`trace_picture_range.py` は同一Pictureの入口/出口cursorも対で取得した。今回の会話layoutの
代表範囲は以下（**stream stateに依存する観測値であり固定サイズではない**）。

| Pane | size | list | input→output差分 |
|---|---:|---:|---:|
| `P_bg_L_00` | 202×128 | 32 | `0xC8` bytes |
| `P_bg_R_00` | 202×128 | 32 | `0x1C0` bytes |
| `P_soft_L` | 64×128 | 32 | `0x200` bytes |
| `P_soft_R` | 64×128 | 32 | `0x1C0` bytes |
| `P_soft_T` | 286×16 | 32 | `0x200` bytes |
| `P_soft_B` | 286×16 | 32 | `0x1C0` bytes |
| `P_nam_01` | 128×32 | 32 | `0x1E8` bytes |
| `P_nam_00` | 128×32 | 32 | `0x120` bytes |
| `P_base_0` | 432×240 | 19 | `0x90` bytes |

**限定**: cloneはlive `P_nam_00`のmaterial/textureを借り、毎回コピーするため所有権・破棄を
持たない。一つの会話layout/list 32でのみ確認済みであり、任意の画像、境界の9-slice化、他UIとの
z順、会話終了後のsource lifetimeは未解決である。`SRC_PICTURE`はbootごとのruntime pointerなので
再起動後はrange traceから再取得し、名前/vtable検証を通してから適用する。

**根拠**: `0x4D7174` / `0x73B524` / `0x73CB58` のstatic assembly、F-147のcursor/thread証拠、
entry/epilogue traceで採った各range、`PATCHES/cave_ui_picture_clone.py`のread-back、実機での
移動済み名前欄背景の可視確認。traceとclone patchはいずれも検証後にuninstall済みで、
hook/cave/cloneはstock/zeroへ復元した。

