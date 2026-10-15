---
id: ACNL-F0500
aliases:
- IDA-opus-5.5-F031
title: 複製を画面に固定する方式＝再生直後の late pass で専用カメラ。Scene 1 に積む案は右目が壊れるので不可（2026-09-24、MEDIUM（静的＋別エージェントの実機成功の手順）。gohan 246865a は実機未確認）
summary: '**Scene 1 案を退けた理由（静的）**: `Render_DrawScene0 0x4F2334` と `Render_DrawScene1 0x4EA01C` は `byte_94CA2C` で排他（メニューが'
date: '2026-09-24'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5186356
- 5152796
- 5172696
- 5184740
- 6875748
- 5173680
- 5172712
- 4803900
- 5158976
- 1854108
tags:
- camera
supersedes: []
source: IDA:work/FINDINGS.md:2236-2257
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F031: 複製を画面に固定する方式＝再生直後の late pass で専用カメラ。Scene 1 に積む案は右目が壊れるので不可（2026-09-24、MEDIUM（静的＋別エージェントの実機成功の手順）。gohan 246865a は実機未確認）

- **Scene 1 案を退けた理由（静的）**: `Render_DrawScene0 0x4F2334` と `Render_DrawScene1 0x4EA01C` は `byte_94CA2C` で排他（メニューが
  `sub_4EF5DC` で 1 にし `sub_4EF27C` で 0 に戻す。呼び元に持ち物 `sub_1959D0`・カタログ `sub_21B1CC`・`BsMenuCatalog_End`）。
  `Render_DrawSceneIndexed 0x4EEDD8` は左目（1024）でだけ記録し、右目（1040）は同じ格納先を再生するが、格納先の番号 `dword_94CA54` は
  `Render_FrameEnd 0x4F1CE4` がフレームごとに 0/1 を入れ替えるだけで Scene 間で共有。同じフレームに Scene 0 と 1 を描くと右目の世界が消える。
- **SceneContext の欄（実機、`tools/models3d/probe_scene_contexts.py` → `work/evidence/models3d/scene_contexts.json`）**: 3 つとも
  `nw::gfx::SceneContext`、{allocator, begin, end, cap} の vector 並び。+76 カメラ（cap 1）、+92 フォグ（cap 4、`sub_4A41EC` をカメラと呼ぶ）、
  +124 ライト（cap 8、LightSet `dword_9C3088[4]` の +64 へ配る）、+156 / +172（LightSet +16 / +12）。フレームの切れ目では全部空（毎フレーム積み直し）。
  カメラもノードとして積まれる（`BsCamera_ActivateContext 0x68EA64` は +424 が無ければ +20 を Scene 0、あれば +220 を Scene 1 へ）。
- **late pass（採用）**: 再生直後の NOP `0x4EF1B0`。R10 は 0x4EEDE8 で `g_SceneContexts[n]` を読んだ後書き換えなし（objdump）。
  `CameraBind 0x494D3C` は view（+328、3x4）を c90、projection（+424、4x4）を c86 として頂点・ジオメトリシェーダの定数へ送るだけで深度の変換は触らない。
  メッシュの判定は `Scene_DrawLayers 0x4EB840` の写し（ノード +0x170/+0x174 メッシュ、+0x17C/+0x180 見える表〈add #380; ldm〉、+0x164 マテリアル、
  メッシュ +28/+36/+38、ResModel +180/+184/+208、層 = マテリアル +8 → +32 の下位バイト）。
- **ゲームの projection（IDA-gpt-6-astra の実機記録 before_movement_state.json）**: 行 0 = [0, 5.1446, 0, 0]、行 1 = [-3.0867, 0, 0, 0]、
  行 2 = [0, 0, 1.0294, 51.47]、行 3 = [0, 0, -1, 0] → near 50（z/w = 0）、far 1750（z/w = -1）。z の行に 0.01 を掛ければ複製は near のすぐ前（世界より手前）。
- **部品の表**: 生の管理役 +76768 から 32 おき 8 本（各 7 件、数 +28）。`BsPlayerMgr_SubmitPartLists 0x1C4A9C` の即値の合計で 8 本とも照合。
  頭は通常この表へ積まれる（`sub_27148C`）。今の読み込み先 +0x2A8 が 0 でない（Mii マスク）ときだけ Mii 専用の描画 `unk_9A4E30` へ回る。
- **gohan 246865a**: 上の手順を C++ で実装。スタブ `0x838780`（`tools/models3d/build_late_pass_stub.py`、監査 27 項目 PASS）。
  検査 `tools/models3d/verify_player_clone.py` に late pass の欄・部品の表・スタブの照合を追加（0 failed）。**環境光はまだ世界のまま**。
- 反証条件: 実機で複製が画面に出ない／世界に隠れる／右目だけ崩れる／部品が欠ける。

