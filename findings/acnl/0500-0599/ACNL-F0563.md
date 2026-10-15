---
id: ACNL-F0563
aliases:
- IDA-unknown-F019
- V2-F019
title: 模様替えの家具の下の範囲表示は UnitCursor モデル、屋外では資源もクラスも無い（2026-09-18、MEDIUM）
summary: 正体はパーティクルでなく 3D モデル romfs/Ftr/Chip/UnitCursor.bcres（モデル UnitCursor/UnitCursorLine/UnitCursorNG/UnitCursorRotate、m_UnitCursor の Visibility/MaterialColor アニメ）。読み込みは ScStage_LoadIndoorRes 0x611928 が部屋フラグ8（屋内、ItemIndoor.bin と同条件）のときだけ専用ヒープ Unit
date: '2026-09-18'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6363432
- 6362648
- 5178508
- 6884200
- 5166996
- 5165036
- 8925992
tags:
- model
supersedes: []
source: IDA:work/FINDINGS.md:4255-4259
by: unknown
original_by: ''
reviewed_by: []
state: superseded
consolidated_into: ''
duplicate_of: ''
superseded_by: ACNL-F0692
corrected_by: ["ACNL-F0562"]
---
## IDA-unknown-F019: 模様替えの家具の下の範囲表示は UnitCursor モデル、屋外では資源もクラスも無い（2026-09-18、MEDIUM）

正体はパーティクルでなく 3D モデル romfs/Ftr/Chip/UnitCursor.bcres（モデル UnitCursor/UnitCursorLine/UnitCursorNG/UnitCursorRotate、m_UnitCursor の Visibility/MaterialColor アニメ）。読み込みは ScStage_LoadIndoorRes 0x611928 が部屋フラグ8（屋内、ItemIndoor.bin と同条件）のときだけ専用ヒープ UnitCursorRes 20480B（ScStage+0x418）へ、資源は ScStage+0x420、解放は ScStage_Cleanup 0x611618。表示は ModuleIndoor.cro の AcObjUnitCursor（RTTI 15AcObjUnitCursor、プロファイル 0x270、Actor 派生）で、CursorObjList 64 枠×124B。初期化 0xB19CEC が枠ごとに ModelInstance_Create 0x4F048C でモデルとアニメ3本（表 0xB8E124 = UnitCursor/UnitCursorNG/UnitCursorRotate）を作りシングルトン 0xB8E118 に自身を置く。0xB19FFC が空き枠に家具オブジェクト番号（枠+121）と種類（枠+120）を入れ、家具の大きさ 0x690B68 でアニメのフレームを決める。更新 0xB1A15C は ModuleFtr の家具配列（seg0+0x1CF2C、112×32B）から位置と向きを取り TransformNodeHolder_SetMatrix3x4 0x4ED794→0x4ECFEC。屋外で出せない理由は (1) 資源が屋内でしか読まれない (2) クラスが ModuleIndoor.cro にあり屋外では載らない（全CROで UnitCursor を持つのはこの1本） (3) 位置が家具オブジェクト依存で任意座標の入口が無い。道筋は IDA-unknown-F007/F010（docs/topics/models3d.md）の自前モデル表示で bcres を自分で読む方法。LOW: 部屋フラグ8=屋内の断定、枠+120 の値とアニメの対応、大きさとフレームの具体値。反証条件: 屋外の場面で UnitCursor.bcres が読まれている、または屋外CROに同等クラスがある。根拠 work/evidence/unit_cursor/README.md。
追記（2026-09-18、同 IDA-unknown-F019）: 未確認点を詰めた。(1) 部屋フラグ 8 = 屋内。g_RoomFlagTable 0x883328 で 200 部屋中 118 件が bit8 を持ち、駅・家・店など室内だけ（村・Downtown・島の外は非該当、RoomID.txt と照合）。(2) UnitCursor.bcres のモデルは CMDL 1 つ（UnitCursor / mdl_UnitCursor / m_UnitCursor）で、UnitCursorLine 等はノード名。アニメは 3 本 UnitCursor(150F) / UnitCursorNG(150F) / UnitCursorRotate(3F) で IsBranchVisible とマテリアル色を動かす（明滅は資源側）。(3) 初期化 0xB19CEC が 3 本を枠+24+32k へ割り当て、追加 0xB19FFC は枠+88（UnitCursorRotate）にフレームを入れて速度 0 で止める。(4) 0x690B68 は v=(id>>12)&0xF から (v+2)>>2 を返し（0,1→0 / 2-5→1 / 6-9→2 / 以降→3）、その 0〜3 がフレーム 0.0〜3.0＝範囲の形。よって UnitCursorRotate は回転ではなく 4 コマの形選択。(5) 追加 0xB19FFC・削除 0xB1A2F0 は ARM/Thumb の呼び出しもポインタ参照も 0 件で呼び出し元不明（更新は vtable slot 9）。残る LOW は枠+120 に入る実値と、屋外表示の描画順・Z ファイト・影（実機要）。

