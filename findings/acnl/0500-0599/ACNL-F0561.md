---
id: ACNL-F0561
aliases:
- IDA-unknown-F021
- V2-F021
title: UnitCursor を屋外で出すための足場と不足（2026-09-18、MEDIUM）
summary: '資源読み込みの入口を確定: G3dResHolder_RequestLoad 0x317920 → FileRes_RequestLoadAligned 0x569D94 → FileRes_RequestLoadAsync 0x569BA0。後者は**非同期**でホルダ+232 が状態（0未要求/1要求/2同期/3,4,5完了）、+68 パス・+204 ヒープ・+228 アライン・+233 非同期旗。戻り値は完了か。完了まで毎フレーム呼び直す必要があり（ScStage_Pr'
date: '2026-09-18'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 3242272
- 5676436
- 5675936
- 3242328
- 4874016
- 5166640
- 10236068
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4247-4250
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F021: UnitCursor を屋外で出すための足場と不足（2026-09-18、MEDIUM）

資源読み込みの入口を確定: G3dResHolder_RequestLoad 0x317920 → FileRes_RequestLoadAligned 0x569D94 → FileRes_RequestLoadAsync 0x569BA0。後者は**非同期**でホルダ+232 が状態（0未要求/1要求/2同期/3,4,5完了）、+68 パス・+204 ヒープ・+228 アライン・+233 非同期旗。戻り値は完了か。完了まで毎フレーム呼び直す必要があり（ScStage_PrepareStep がそうしている）、完了後に G3dResHolder_Setup 0x317958（GPU割り当てと DefaultShader 以外のマテリアル差し替え）を必ず通す。モデル取得は G3dResource_FindModelByName 0x4A5F20（*res+32 の相対辞書）。描画登録 Scene_SubmitNode 0x4ED630 は旧 F-111/F-112 で実機確認済みの汎用API（g_SceneTraversers 0x9C30A4、SceneContext は3本、配列#0が描画対象）で、最小実例は sub_1F9A6C 生成＋sub_1F9BC4 が毎フレーム index 0 で登録。屋外でも BsFtrMgr が家具枠を作る（IDA-unknown-F020）ので描画基盤は生きており、足りないのは UnitCursor 資源と自前の描画処理だけ。未確定: シーン番号の意味、毎フレーム呼ぶフック位置、資源ホルダの型と確保サイズ、ModelInstance_Create の 0x834/1/3 の意味、アニメ割り当てAPIの引数、マス→ワールド換算、実機での描画順・Zファイト・影・必要ヒープ量。反証条件: 非同期状態機械が上記と違う、または Setup 無しでモデルが引ける。根拠 work/evidence/unit_cursor/outdoor_plan.md。

