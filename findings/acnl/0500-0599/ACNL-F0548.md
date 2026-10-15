---
id: ACNL-F0548
aliases:
- IDA-opus-5-F002
title: 屋外座標の曲面変換は部屋フラグで切り替わる。165部屋中37部屋（2026-09-20、HIGH、静的＋実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。`FieldPosition_ToRenderSpace 0x0052CDD8` は'
date: '2026-09-20'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5426648
- 3110348
- 5980340
- 7719604
- 8925992
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4070-4089
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F002: 屋外座標の曲面変換は部屋フラグで切り替わる。165部屋中37部屋（2026-09-20、HIGH、静的＋実機）

解析ソフト: IDA / 解析モデル: opus-5。`FieldPosition_ToRenderSpace 0x0052CDD8` は
`Room_GetCurrentId 0x002F75CC` → `sub_5B40B4 0x005B40B4` を見て、フラグが無ければ `out = in` の
3語コピー、あれば `CurvedWorld_TransformPosition 0x0075CAB4` を呼ぶ。ゲートは
`g_RoomFlagTable[roomId] & 2`（`0x00883328`、`roomId < 0xA5`）で、**4バイト間隔**は
`LDR R0,[R2,R0,LSL#2]` を逆アセンブルして確認した（間隔の見た目からの推定ではない）。
165エントリ中**37が曲面・128が平ら**で、id 0・1 は曲面側。よって **屋内は変換不要、屋外は必須** で、
呼び出しを省くのではなく常に通すのが正しい（分岐はゲーム側の仕事）。
変換そのものはゲームのsin/cos表を使わずPythonの三角関数で独立に再現し、別エージェントが捕獲した点で
一致した（raw (2158.788330078125, 112.0, 1114.8851318359375) → render y=-318.499/-318.491、
z=370.951/370.942。yで約431、zで約744のずれ）。

根拠: `tools/models3d/verify_curved_pose.py`（PASS）、`work/evidence/models3d/live_20260919/pose_numeric_input.json`、
本文の逆アセンブル。詳細 [arbitrary_model_draw_plan](../docs/topics/arbitrary_model_draw_plan.md) §2。
**2026-09-20 実機で確定（IDA-opus-5-F004）**: 部屋0（`g_RoomFlagTable[0]=0x26`）で実機の角度 `0x5E2E`=24110 が
事前予測 24110 と一致し、その姿勢で置いたモデルが画面に出た。確度を MEDIUM から HIGH へ上げる。

反証条件: フラグ2以外でも曲面経路へ入る呼び出し元がある、`g_RoomFlagTable` が実行時に書き換わる。

