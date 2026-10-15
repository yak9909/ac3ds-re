---
id: ACNL-F0625
aliases:
- IDA-gpt-6.1-sol-F002
title: '模様替え UI を開いたまま家具を出す手順の詰め（2026-10-07、MEDIUM: 静的のみ。利用者の 5 時間枠で打ち切り）'
summary: '解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（推論 xhigh）**、Codex CLI のサブエージェント（依頼 work/codex/tasks/t022_spawn2.md、F001 の続き）。採番・照合・記録は親（opus-5.5）。'
date: '2026-10-07'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6879876
- 5692964
- 5692132
- 5690988
- 8516280
- 5977884
- 4177292
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4917-4928
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F002: 模様替え UI を開いたまま家具を出す手順の詰め（2026-10-07、MEDIUM: 静的のみ。利用者の 5 時間枠で打ち切り）

解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（推論 xhigh）**、Codex CLI のサブエージェント（依頼 work/codex/tasks/t022_spawn2.md、F001 の続き）。採番・照合・記録は親（opus-5.5）。
詳細と根拠は **work/evidence/t022_spawn2/report.md**（JSON 多数）。IDB: 主 49・ModuleIndoor 27・ModuleFtr 9・HHD 14 の命名/コメント（idb_*_changes.json、読み戻し一致の後に Codex 自身が保存・閉鎖。ID は親が F??? → 本 ID に置換）。
- **生成は同じ呼び出しの中で Prepare まで進む**: `BsFtrMgr_SpawnFromRecord` 0x68FA84 → ctor と `AcFtr_CreatePrepare` 0x56DE24（マップ・家具表・ModuleFtr 記録 0xB1CF44 への登録）まで同期。Load / Finalize（`AcFtr_LoadResources` 0x56DAE4 / `AcFtr_CreateFinalize` 0x56D66C、`Actor_RunCreateStages` 0x81F2B8）は後のフレームへ延び得る → `FtrRec_IsAlive` だけでは Chip_Setup してよいと言えない。actor +102 bit1（最終化済み）・破棄要求なし・状態 2・親解決済みを待つ。
- **チップの 1 件追加**: 完成した actor と記録を確かめ、上載せは親解決後の位置更新（AcFtr_Update 内 vslot+208）を 1 回待ってから、未使用チップへ `Chip_Setup` 0xB43160 を 1 回 → 親子は容量（4）を先に確かめて結ぶ → `Editor_AttachActiveChipPanes` 0xB2F6E4。描画リストへは Setup では載らず、次の描画巡回（0xB3DD10 → 0xB430F0）で載る。
- **チップ枠の再利用は不可**（Out/Release 済みの枠は親子・選択・指の欄が残る。ゲーム自身の再利用経路も無い）。使えるのは未使用の枠 = 112 − 生きている記録の数。
- **失敗**: 家具アクター 48（0x5B371C）。TryPut が 0 でも Spawn は失敗し得る。Prepare 後の失敗は完全な巻き戻しを保証できない → 失敗したら同じ決定で再試行しない。
- **向き**: HHD の `Camera_GetFacingQuadrant` 0x3FBD8C（HHD-F016 の名前）は誤り。家具表 66 枠を走査し押し引き中の家具の移動方向を返し、無ければ 4（探索側で 2 に置換）。親が逆コンパイルで照合し `Room_GetMovingFurnitureQuadrant` に改名（Codex の名前 FtrObjectTable_GetPushPullFacingQuadrant を上書き。意味は同じ）。
  → リストから出すときは方向 2。四分円は両作とも 0 = +Z、1 = +X、2 = −Z、3 = −X、マスの X/Z 軸も同じ向き（HHD のワールド 16 単位、ACNL 32 単位）。
- 未確定: フックからの実際の生成、Neutral 中の表示・操作、Prepare 後の失敗の残りもの。全部実測なし。

