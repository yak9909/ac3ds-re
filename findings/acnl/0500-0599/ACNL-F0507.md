---
id: ACNL-F0507
aliases:
- IDA-opus-5.5-F024
title: 橋のモデル行列は平行移動 (x, 0, 0) ＋曲面の回転だけ（地面の高さを使わない）（2026-09-24、HIGH）
summary: '**結論**: 村の橋（`12AcStrcBridge`）は、描画用の平行移動が **(x, 0, 0)** で、曲面の回転（X 軸まわり）だけが載る。'
date: '2026-09-24'
category: field
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags:
- model
supersedes: []
source: IDA:work/FINDINGS.md:2349-2363
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F024: 橋のモデル行列は平行移動 (x, 0, 0) ＋曲面の回転だけ（地面の高さを使わない）（2026-09-24、HIGH）

- **結論**: 村の橋（`12AcStrcBridge`）は、描画用の平行移動が **(x, 0, 0)** で、曲面の回転（X 軸まわり）だけが載る。
  半径（高さ）はモデル自身が持っている。通常の建物（平行移動 = `FieldPositionToRenderSpace` の結果）とは違い、
  **地面の高さも実体の y も行列には入らない**。橋のプレビューが見えなかったのは、建物と同じ形（半径 377+y を平行移動に入れる）で
  置いていたので、モデルが持つ半径と二重になり、画面の外へ出ていたため。
- **根拠 1（実機、読み取りのみ）**: `work/evidence/models3d/bridge_probe.json`。実体 `0x3310daa8`（id `0xA3`、pos (1808, 112, 1840)）の
  Model `+0x4C` のローカル行列 = 回転 [1,0,0 / 0,-0.813,0.582 / 0,-0.582,-0.813]、平行移動 (1808, 0, 0)。
- **根拠 2（独立の計算）**: 曲面の角度の式（F023 以前に実測した θ = 360° − (360/3072)·z）に z = 1840 を入れると θ = 144.375°、
  cos = −0.8128、sin = 0.5825。行列の回転と一致する。つまり角度は建物と同じで、違うのは平行移動だけ。
- **gohan への反映**: `BuildingPreview::Pose` で、曲面の部屋で橋なら平行移動の y・z を 0 にする（x と回転は建物と同じ）。
- **役場の付属物（旗・チケットマシン）**: 別モデル（`Other/flag.bcres`・`Other/ticketmachine.bcres`）なので、
  読み込み時間を短くするため**配置プレビューには出さない**（利用者の指示、2026-09-24）。選択中の色合成（F023）は従来どおり対象にする。
- 反証条件: ほかの橋（木・石・吊り橋・斜め）や別の z で、平行移動に y・z が入る例が見つかったら見直す（今回読んだのは 1 本だけ）。

