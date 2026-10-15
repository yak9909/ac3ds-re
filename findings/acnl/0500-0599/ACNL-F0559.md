---
id: ACNL-F0559
aliases:
- IDA-unknown-F023
- V2-F023
title: 屋外表示の未解明点のうち4件を解決（ホルダ型・Create引数・マス換算・フック候補）（2026-09-18、MEDIUM）
summary: '(1) 資源ホルダ: ScStage ctor 0x7F195C（ScStage は 3504B）から、ScStage+0x418 = ssys::ma::HeapAllocator（8B、ctor HeapAllocator_Ctor 0x5667E8 / dtor 0x317CBC）、ScStage+0x420 = G3D 資源ホルダ（g3d::ResourceLoader＋ResourceSet、**264B**、0x420〜0x528。ctor G3dResHolde'
date: '2026-09-18'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 8329564
- 5662696
- 3243196
- 5167200
- 3243260
- 6972260
- 7099564
- 5369424
- 1798596
- 1798680
tags:
- hook
supersedes: []
source: IDA:work/FINDINGS.md:4239-4242
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0442", "ACNL-F0447"]
---
## IDA-unknown-F023: 屋外表示の未解明点のうち4件を解決（ホルダ型・Create引数・マス換算・フック候補）（2026-09-18、MEDIUM）

(1) 資源ホルダ: ScStage ctor 0x7F195C（ScStage は 3504B）から、ScStage+0x418 = ssys::ma::HeapAllocator（8B、ctor HeapAllocator_Ctor 0x5667E8 / dtor 0x317CBC）、ScStage+0x420 = G3D 資源ホルダ（g3d::ResourceLoader＋ResourceSet、**264B**、0x420〜0x528。ctor G3dResHolder_Ctor 0x4ED860 / dtor G3dResHolder_Dtor 0x317CFC）。ホルダ+232 が読み込み状態。(2) ModelInstance_Create の引数: sub_48E350→sub_736158→nwgfx_Model_Create を追い、a5=マテリアルのコピーマスク→desc+0x10→model+0x188、a6=フラグ(byte)→desc+0x24、a7→desc+0x1C→SceneNode+72/+324 と holder+8。UnitCursor は (0x834,1,3)、木は (0,0,1) で、実装はゲームと同じ値を使う。(3) マス→ワールド: Field_TileToWorld 0x6A6364 が x=32*tileX+16、z=32*tileY+16、y=Field_GetGroundHeight 0x6C54AC。1マス=32単位・中心+16で、地形補正と分離できる。(4) フック候補: BaseObj_RunDrawPhase 0x51EE50 のリストに自前オブジェクトを乗せる（旧F-113の推奨）か、Frame_DrawPass1024 0x1B71C4 のこの呼び出し直後 0x1B7218 に1本フックする。残り: アニメAPIの引数、必要ヒープ量（sub_736158 の問い合わせモードで見積もれる）、非同期読み込みを描画スレッドから回してよいか、実機の描画順・Zファイト・影。反証条件: ホルダが264Bでない、または (0x834,1,3) 以外が必要。根拠 docs/topics/unit_cursor_outdoor.md §7。

