---
id: ACNL-F0560
aliases:
- IDA-unknown-F022
- V2-F022
title: Scene_SubmitNode のシーン番号は 0=通常描画・1=別モード・2=影マップ（2026-09-18、MEDIUM）
summary: Render_InitGlobal 0x4E97CC が SceneContext/SceneTraverser を 3 本作る（g_SceneContexts 0x9C3098 / g_SceneTraversers 0x9C30A4）。Scene_DrawLayers 0x4EB840 の呼び出し元は 2 つで、Render_DrawScene2 0x4E976C が影マップ（g_SceneContext_2、IDA-unknown-F008）、Render_DrawSc
date: '2026-09-18'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5150668
- 10236056
- 10236068
- 5158976
- 5150572
- 5172696
- 5186356
- 5152796
- 1798596
- 1798884
- 5167088
tags:
- map
supersedes: []
source: IDA:work/FINDINGS.md:4243-4246
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F022: Scene_SubmitNode のシーン番号は 0=通常描画・1=別モード・2=影マップ（2026-09-18、MEDIUM）

Render_InitGlobal 0x4E97CC が SceneContext/SceneTraverser を 3 本作る（g_SceneContexts 0x9C3098 / g_SceneTraversers 0x9C30A4）。Scene_DrawLayers 0x4EB840 の呼び出し元は 2 つで、Render_DrawScene2 0x4E976C が影マップ（g_SceneContext_2、IDA-unknown-F008）、Render_DrawSceneIndexed 0x4EEDD8 が Render_DrawScene0 0x4F2334（byte_94CA2C==0 のとき index 0）と Render_DrawScene1 0x4EA01C（byte_94CA2C==1 かつ sub_5CD770()==0 のとき index 1）から呼ばれる。index 0 と 1 は byte_94CA2C で排他。上画面パス Frame_DrawPass1024 0x1B71C4 と 1040 0x1B72E4 の両方が 2→0→1 の順で同じ SceneContext を使うので、番号は画面ではなく描画パスの種類。よって屋外で普通に描くなら **0**（旧 F-111/F-112 の実機実例も 0）。byte_94CA2C の getter 0x4ED7F0 の呼び出し元に BsMenuCatalog_End 等のメニュー系があり、1 はプレビュー用と推定（LOW）。反証条件: 実機で index 0 に積んだノードが屋外で描かれない。根拠 docs/topics/unit_cursor_outdoor.md。

