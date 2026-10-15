---
id: ACNL-F0037
aliases:
- F-147
title: 'F-147: `nw::lyt::Picture` は TextBox と同じ UI command-list 経路を使う — `HIGH`（静的＋実機）'
summary: '`ti_nw_lyt_Picture=0x8C9B9C` / `vtbl_nw_lyt_Picture=0x8FBFFC` の Pane draw slot'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9214876
- 9420796
- 7588696
- 7583012
- 4948832
tags:
- layout
supersedes: []
source: v1:RE/FINDINGS.md:598-629
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-147: `nw::lyt::Picture` は TextBox と同じ UI command-list 経路を使う — `HIGH`（静的＋実機）

`ti_nw_lyt_Picture=0x8C9B9C` / `vtbl_nw_lyt_Picture=0x8FBFFC` の Pane draw slot
`+0x68` は `nwlyt_Picture_DrawToCommandList` (`0x73CB58`) である。親の
`nwlyt_Pane_DrawRecursive` (`0x73B524`) はこの仮想関数へ入力 cursor を `R1` として渡し、
返った `R0` を次の可視 child Pane の `R1` へ渡す。従ってPaneごとの描画は独立した即時
submitではなく、単一のUI command streamを順に伸ばす設計である。

`0x73CB58` は Picture material (`+0x13C`) とPane geometryを描画contextへ蓄積し、容量境界
または必要時に `sub_4B8360` へ渡す。同関数はqueued state/geometryを受け取った `R1` cursorへ
コピーし、更新後cursorを `R0` で返す。assembly上、Picture pathとTextBox pathは同じ
`TextBox_UpdateDrawState` / `sub_4B8360` を共有する。後者の正確なクラス名は未確定のため
IDBではcommentのみとした。

停止中に採取した `scratchpad/trace_picture_draw.py` の旧標本では、`vptr=0x8FBFFC` のPictureが
実際に `0x73CB58` へ入り、会話レイアウトの `P_nam_00` / `P_nam_01` / `P_soft_L/R/T/B` /
`P_allow*` を含むPicture群が list 32へ記録された。例えば `P_nam_00` は128×32、
`P_soft_T/B` は286×16であり、すべてdraw context `0x32FF62EC` / list manager
`0x327DDC2C` / list id 32だった。別の432×240 Pictureはlist 19だった。これはF-145の
TextBox list 32→main list replay経路と独立な、Picture側からのlive照合である。

**含意（限定）**: 画面固定の自前パネルは、既存 `g3d::FuncNode` のworld/shadow passへ
commandを貼るのではなく、native Pictureを所有させるか、list 32のrecord/replay前後に
自己所有のUI command rangeを追加するのが整合する。まだ自前Pictureの生成・所有権・破棄、
あるいはPicture 1枚の正確なcommand byte rangeは未確定であり、FuncNodeから2D panelを
安全に出せたとは結論しない。

**根拠**: Picture RTTI/vtable、`0x73B524` / `0x73CB58` / `0x4B8360` の `code.bin.i64`
assembly、F-145のTextBox list/replay証拠、停止中live traceのPicture vptr・name・size・
draw context・selected list。traceは0件の再構築なし試行後にhook/cave/bufferをstock/zeroへ
復元済み、breakpointは0件。

