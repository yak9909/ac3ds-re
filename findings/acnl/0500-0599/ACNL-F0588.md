---
id: ACNL-F0588
aliases:
- IDA-opus-5.5-F072
title: 'nw::lyt の Window は 1 枠でも描ける（2026-10-05、MEDIUM: 静的 + designer の再現がスクショと一致）'
summary: 解析ソフト IDA（idalib-mcp）、解析モデル opus-5.5。HHD の画面を ACNL で再現する作業（D005 / T011）の周辺で確認。
date: '2026-10-05'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 7584580
- 7584628
- 7584956
- 9930276
- 4945104
- 4945612
- 4945356
- 4944848
tags:
- layout
supersedes: []
source: IDA:work/FINDINGS.md:4435-4446
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F072: nw::lyt の Window は 1 枠でも描ける（2026-10-05、MEDIUM: 静的 + designer の再現がスクショと一致）

解析ソフト IDA（idalib-mcp）、解析モデル opus-5.5。HHD の画面を ACNL で再現する作業（D005 / T011）の周辺で確認。

- `nwlyt_Window_GetFrameSize 0x73BB44`: 枠数 1 のとき l = r = 枠 0 のテクスチャ幅、t = b = 同じく高さ（`0x73BB74`）。4 / 8 は従来どおり枠ごと。
- `nwlyt_Window_DrawSelf 0x73BCBC` の `switch (+360)` の case 1: 枠 0 の材質で 4 回描く。LT = 反転 0、RT = 1、RB = 4、LB = 2。四角の位置・大きさは 4 枠と同じ式。中身は枠数によらず必ず描く。
- 反転表 `g_nwlyt_WindowFrameFlipTable 0x978624`（命名）: 10 B × 6。[0..7] = 4 隅の UV（TLu TLv TRu TRv BLu BLv BRu BRv、0/1）、[8] = 四角の幅に沿う成分、[9] = 高さに沿う成分。
  読むのは `nwlyt_Window_CalcFrameTexCoordLT/RT/RB/LB`（0x4B74D0 / 0x4B76CC / 0x4B75CC / 0x4B73D0）。
- 照合: acnl-ui-designer の `drawWindow` をこの 4 関数と表の 1 対 1 の写しに置き換え、(1) ACNL の 4 枠ウィンドウを含む既存場面 7 本の描画がバイト一致（退行なし）、
  (2) HHD の 1 枠ウィンドウ（目・髪の白い枠）がスクショと一致。ACNL 自身にも 1 枠のウィンドウがある（chip_room_00 の W_Wall_00 など。実機では未観測）。
- 反証条件: 1 枠のウィンドウを実機で出して、角の向きが designer と違えば誤り（T012 以降で確認）。

