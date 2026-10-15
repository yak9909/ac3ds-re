---
id: ACNL-F0474
aliases:
- IDA-opus-5.5-F059
title: '1 つの体を行列だけ変えて何か所にも描く（描画ノード FuncNode）（2026-09-28、MEDIUM: 静的のみ。gohan 4fb9e33 で使用、実機未確認）'
summary: '解析ソフト: IDA（主 IDB を idalib-mcp で静的）/ 解析モデル: opus-5.5。利用者指示（2026-09-28）: ヒープの上限を越えたときの扱いを再設計。'
date: '2026-09-28'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5158976
- 5159516
- 5159548
- 5159532
- 4807184
- 4773272
- 4773276
- 4807464
- 5831044
- 5831052
- 5831296
- 11260800
- 7412368
- 5174940
- 5177268
- 5177328
- 5166696
- 5888172
- 5885392
- 9890456
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:1693-1708
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F059: 1 つの体を行列だけ変えて何か所にも描く（描画ノード FuncNode）（2026-09-28、MEDIUM: 静的のみ。gohan 4fb9e33 で使用、実機未確認）

解析ソフト: IDA（主 IDB を idalib-mcp で静的）/ 解析モデル: opus-5.5。利用者指示（2026-09-28）: ヒープの上限を越えたときの扱いを再設計。
- **層とコールバック**: `Scene_DrawLayers 0x4EB840` は層 i = 0..3 を外側で回し、Model はメッシュごとに「可視（mesh+38 の s16 < 0 なら mesh+36、そうでなければ
  可視表 体+0x17C..+0x180 の 8 B 項目、空なら資源+208 の辞書 +16×i+40 の先）の +4 && mesh+36」かつ「材質（体+0x164[mesh+28]）+8 の ResMaterial+32 の下位バイト == i」のとき `gfx_DrawMesh(g_DrawContext, mesh, 体)`。
  FuncNode は i = 0 で +0x148、i = 1 で +0x14C を (g_DrawContext, +0x150) で呼ぶ（0x4EBA5C / 0x4EBA7C / 0x4EBA6C）。UnitCursor の材質は層 1（既存 V2-F024）。
- **行列の送り方**: `sub_48D51C` は ctx[2]+28 が同じ体なら `RenderContext_SendModelMatrices 0x495A10` を省く（0x48D598 / 0x48D59C）。送るのは c0-c2 = 体+140、c3-c5 = 体+444 の**値**で、最後に ctx[2]+28 = 体（0x495B28）。
  → 同じ体を続けて描くには毎回 ctx[2]+28 = 0 にする。書いたコマンドは値の写しなので、描いたあとに行列を書き換えてよい。
- **体+444**: シーンの更新が作る欄。描画リストへ出さない体では更新されない。fgobj と同じく `fgobj_Object_SetModelView 0x58F984(obj, 視点)` を使う。読むのは obj+0x108（体）と +0x10C（0 なら骨の物体なし）だけ（0x58F98C / 0x58FA80）。
  視点は `sub_711A8C(&unk_ABD380, 1024)` = 0xABD380 + 164（0x711A90）。世界行列の計算 `0x4EF69C` は親の無い体でも正しい（既存 V2-F026）。
- **FuncNode の作成と片付け**: `g3d_FuncNode_Create 0x4EFFB4(holder, alloc)` は 340 B（0x4EFFF0 `MOV R1,#340`）を確保して null を確かめない → 呼ぶ前にヒープの残りを見る。
  片付けは `SceneNodeHolder_Destroy 0x4ED668`（`fgobj_Proc_Destroy` 0x59D8AC が +0x45B0 のホルダに対して。Setup 側 0x59CDD0 と同じ場所）。
- **gohan 4fb9e33**: InstancedDraw = FuncNode 1 つ + 束（体のホルダ, 行列の並び）。1 か所ごとに SetMatrix3x4 → UpdateWorldAndSkeleton → SetModelView（偽の物体）→ ctx[2]+28 = 0 → 層の合うメッシュを gfx_DrawMesh。
  1 か所ごとにコマンドバッファの残り（g_GpuCmdEnd 0x96EA98 − g_GpuCmdPtr）が 4 KB 以上あるかを見る。GridCursor は体 1 つ・ヒープ固定・置き場 256、マップエディターのカーソル 128、複製はモデル 1 種類に体 1 つ。
- 反証条件: 実機でカーソル・複製が 1 か所にしか出ない（+28 の送り直しが効かない）、位置がずれる（+444 の作り方が違う）、描画が崩れる・落ちる。

