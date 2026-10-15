---
id: ACNL-F0552
aliases:
- IDA-gpt-6-astra-F001
title: 独立した木を表示・非表示。ゲーム座標には曲面変換が必要（2026-09-20、HIGH）
summary: '解析ソフト: IDA / 解析モデル: gpt-6-astra。実機の準備済みSeason資源から `fg_treeA_4` のordinary Modelを独立生成し、player右36・倍率0.5で表示、OFFで消去を確認。マップの設置データは変更していない。主題・限界は [tree_live_plan](../docs/topics/tree_live_plan.md)。'
date: '2026-09-20'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5832756
- 5426648
- 5662876
- 7719604
- 9420032
- 1798684
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4126-4140
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-astra-F001: 独立した木を表示・非表示。ゲーム座標には曲面変換が必要（2026-09-20、HIGH）

解析ソフト: IDA / 解析モデル: gpt-6-astra。実機の準備済みSeason資源から `fg_treeA_4` のordinary Modelを独立生成し、player右36・倍率0.5で表示、OFFで消去を確認。マップの設置データは変更していない。主題・限界は [tree_live_plan](../docs/topics/tree_live_plan.md)。

- 正常caller `0x590034` は `FieldPosition_ToRenderSpace(out, gameXYZ)` (`0x52CDD8`) → `Matrix3x4_AppendRotationX16(matrix, angle)` (`0x56689C`) → SetMatrix/Update。曲面変換本体 `0x75CAB4` は `x'=x, y'=cos(angle)*(y+radius), z'=sin(angle)*(y+radius)`。返値は地面の傾き。**ゲーム座標をrawのままnode行列へ渡すだけでは、この村で木は画面に現れなかった。**
- 生成契約は `ModelInstance_Create(holder,model,allocator,allocator,0,0,1)`、128KiB専用heap。ordinary Modelのvtableは `0x8FBD00`、MaterialActivator非0、mesh/material各1。生成とpose設定は描画スレッドの `0x1B721C` で行い、同地点の監査済hookでscene0へ登録。
- 座標 `(2158.788330078125,112,1114.8851318359375)` → `(2158.788330078125,-318.4910583496094,370.9418640136719)`、角 `0x5CE8`。ゲームの結果と、実測係数/三角関数表を使う独立Pythonのfloat32計算が行列まで完全一致。原本assemblyも照合。
- 対照: raw座標は不可視（counter46）、曲面変換後は木が見える（counter92）、OFFで木が消える（counter92のまま）。各試験1500msでSuspend、BP0。`curved_enabled.png` / `curved_disabled.png` を実見。PrintWindowは非前面からゲーム画像を取得できたが、Image Sequenceとの直接比較は未実施。
- 追加試験: 同じnodeをplayer左48・Z+32、倍率1.0に変更して表示、OFFで消去。counter139→139。`tree_pose.py` の段階APIと `second_{enabled,disabled}.png`、`pose_second_observed.json`。追加確保なし。
- 制限: 屋外の1種類・2位置・倍率0.5/1.0の最小試験。owner解放/GPU参照終了後の破棄、場面遷移、常用3gx、家具/人間は未確認。画面固定の後続結果はF003。現bootのheap/nodeを再起動後に再利用しない。

根拠: `work/evidence/models3d/live_20260919/` の `pose_static.json`、`pose_numeric_verification.json`、`events.jsonl`、`tree_state.json`、`display_audit.json`、画面。再現計算: `python tools/models3d/verify_curved_pose.py`。呼出しguardは異常停止を強制復帰せず、全VFP/FPSCRとcoreを保存。表示hookは元NOPへ復元済み、割当は未解放。

F029の「入力された行列がworldへ届く」は維持するが、**入力座標の意味まで正常と証明した結果ではない**。SkeletalModel末尾の差を不可視の原因と断定しない。ordinary Modelにはその末尾自体がない。UnitCursorへ同じ修正を適用した実機試験はまだ行っていない。

