---
id: ACNL-F0514
aliases:
- IDA-opus-5.5-F017
title: 衝突判定（歩けないマス）= 足元の属性コードをゲームの分類表 byte_957B34 で引いて 0 でないマス／プレビューの無限ロードとクラッシュの原因（2026-09-24、MEDIUM（静的＋利用者の説明と一致。実機の歩行では未確認））
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。利用者の報告（配置の切り替えで無限ロード・SIGSEGV、UnitCursor が衝突判定準拠でない ほか）。'
date: '2026-09-24'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6083520
- 6083544
- 6083868
- 6083908
- 6083932
- 6084288
- 7097308
- 9796149
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2473-2490
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F017: 衝突判定（歩けないマス）= 足元の属性コードをゲームの分類表 byte_957B34 で引いて 0 でないマス／プレビューの無限ロードとクラッシュの原因（2026-09-24、MEDIUM（静的＋利用者の説明と一致。実機の歩行では未確認））

解析ソフト: IDA / 解析モデル: opus-5.5。利用者の報告（配置の切り替えで無限ロード・SIGSEGV、UnitCursor が衝突判定準拠でない ほか）。

### 1. 衝突判定の分類表
- 属性コード 1 バイトを引く表が 6 本ある（`code >= 0xFF` なら 0 番を引く同じ形の関数: 0x5CD3C0/0x5CD3D8/0x5CD51C/0x5CD544/0x5CD55C/0x5CD6C0）
- **`FieldAttr_CollisionClass 0x5CD3C0` = `byte_957B34[code]`**。`Field_GetCollisionClassAt 0x6C4BDC`（位置 → マスの属性 → この分類。末尾呼び出し）が使う
- 値: 建物本体 0x02/0x03/0x04・ベンチ等の外周 0x05・橋板 0x17 などは 2/3、**柵・橋・交番の外周 0x31/0x32/0x33・橋の角 0xA0 は 0**
- 利用者の説明「2x1 ベンチは 4x3 など一回り大きいものが大半、衝突判定と論理サイズが同じ建物もある」と一致（ベンチ 4x3、交番は本体 3x3＋入口 = 10 マス、南北の橋は橋板 2x4）
- **0 でないマス = 歩けない**と解釈（MEDIUM）。反証条件: 分類 0 のマスに入れない／分類 2 のマスを歩ける
- 以前の「0x957A35（sub_5CD55C）」は大物アイテムを消す判定用（0x05/0x31〜0x3B 等が 1）で、別物

### 2. プレビューの無限ロードとクラッシュ（gohan 側の原因）
- 無限ロード: 種類の切り替えで、**ゲームの読み込みが途中のまま読み込み先のヒープを返していた**。読み込み係は返されたヒープへ書き続け、
  以後の読み込みが終わらない（画面遷移でリロードすると直る、と一致）。→ 読み込みは 1 本読み終わった切れ目でしか止めない
- SIGSEGV: PC=`0x07011AE8`（gohan の `BuildingPreview::FrameStep` → MakeTranslucent）、R8=`0x3F248A94`。材質の配列の先のゴミを範囲判定だけで番地とみなした（F014 と同じ種類）
  → svcQueryMemory で読めるか確かめる

