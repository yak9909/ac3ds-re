---
id: ACNL-F0601
aliases:
- IDA-opus-5.5-F085
title: '目の色は頭のキー、目の形は作るときだけ — 複製の目をすぐ反映する方法（2026-10-05、MEDIUM: 静的のみ。gohan は実機未確認）'
summary: '解析モデル opus-5.5。IDB: `PlayerFaceSlot_RequestLoad 0x2711AC` / `PlayerFaceSlot_Unload 0x2711A4` を命名・注記。'
date: '2026-10-05'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 2560428
- 2560420
- 3316116
- 2564852
- 3127584
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4618-4629
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F085: 目の色は頭のキー、目の形は作るときだけ — 複製の目をすぐ反映する方法（2026-10-05、MEDIUM: 静的のみ。gohan は実機未確認）

解析モデル opus-5.5。IDB: `PlayerFaceSlot_RequestLoad 0x2711AC` / `PlayerFaceSlot_Unload 0x2711A4` を命名・注記。
- 実機（gohan e0e5960）: 全 PASS（フェードイン・位置・色見本・かみがた/かおの音）。利用者: Y の音は軽いポップ音に（美容室でも）、目の色・形もリアルタイムに、キャラクリの ON/OFF 通知を消す。
- `PlayerHeadKey_Build 0x329994` は pm+548 の [4..11] = 髪色 +552・**目の色 +556** をキーに入れる → 目の色を書けば頭が読み直される（髪と同じ二重読み込み）。
- 目の形（顔のテクスチャ）は `PlayerFaceSlot_RequestLoad(枠, 記録, 男の子か, a/b)` が Player/face_tex を読む。既に読んであれば 1 を返すだけで、呼び元は `PlayerModel_CreateStep` だけ。
  顔の枠（pm+332 / +340）は `PlayerModel_Setup` の `PlayerHeadBank_SetSources 0x2722F4(頭, 顔 a, 顔 b, 記録, …)` で頭に結ばれ、二重化されていない（表示中に下ろすと使用中のテクスチャが消える）。
  → 複製は目の形が変わったら片付けて作り直す。作る関数は「見た目の記録」（profile+4）と性別を取る（`PlayerModel_CreateFromProfile` = `CreateStep(pm, profile+4, !(profile+21946 & 1), …)`）ので、
  プロフィールの写しの記録 +2 を書き換えて渡す。記録は表示中も pm+452 と頭の枠から読まれるので写しは持ち続ける。
- 実機（gohan 0bbbcc7、2026-10-05）: 全 PASS（目の色はすぐ変わる、目の形は消えてフェードインして変わる）。利用者の希望で、目の形は裏で 2 体目を作って即入れ替える方式へ（未実機）。
- プロフィールは 1 人 **42,112 B**（`vc_PLAYER_1_PPOFFSET 0x2FB920` が `unk_A7E790 + 42112 × n`）。作成は記録 +21652（profile+21656）まで読む（`sub_582160`）。

