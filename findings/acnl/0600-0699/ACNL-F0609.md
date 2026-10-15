---
id: ACNL-F0609
aliases:
- IDA-opus-5.5-F093
title: 'gohan の他機能の「自分のプレイヤー」— 問題が出た所と出なかった所の理由（2026-10-06、MEDIUM: 静的 + 利用者の実機の結果）'
summary: 解析モデル opus-5.5。F091 の続き（0xAA7994 = 表の 0 番 = ホスト）。
date: '2026-10-06'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 11172244
tags:
- player
supersedes: []
source: IDA:work/FINDINGS.md:4720-4726
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F093: gohan の他機能の「自分のプレイヤー」— 問題が出た所と出なかった所の理由（2026-10-06、MEDIUM: 静的 + 利用者の実機の結果）

解析モデル opus-5.5。F091 の続き（0xAA7994 = 表の 0 番 = ホスト）。
- 実機（利用者、ゲストで操作）: 建物エディターの開始時の高さがずれる（指摘どおり）。屋内外の判定・グリッドカーソル・モデルビューアは問題なし。
- 理由（静的）: (1) 高さ = `FieldCamera::FrameStep` が開始時に「カメラの基準 − 0xAA7994 の位置」の高さを控える → ホストの高さ。(2) 判定 `Available()` は 0xAA7994 が空でないかだけ。表は相手が別の部屋にいてもアクターを持ち続け、部屋の一致は `vc_PLAYERINSTANCE` が別に見る → ゲストでも通る。(3) エディターのカーソルは `PublicWorks::PlayerTile`（`GetWorldCoords(…, 自分の番号)`）のマスを `GridCursor::ShowTiles` に渡す → 自分に追従。0xAA7994 の足元を使うのは単独の `GridCursor::Show`（テストのグリッドカーソル）だけ。(4) モデルビューアは 0xAA7994 の位置に置く → ゲストではホストの所に出るはず。問題が見えなかったのは試した条件（ホストとゲストが近い／ホストで試した等）によると推定（LOW）。
- 修正（gohan 8ea5325）: 全部 [自分の通信番号] の枠へ（GridCursorGameApi::LocalPlayer / FieldCamera::LocalPlayer）。オフライン・ホストでは変化なし。

