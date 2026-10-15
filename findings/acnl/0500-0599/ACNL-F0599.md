---
id: ACNL-F0599
aliases:
- IDA-opus-5.5-F083
title: '上画面の描画順と「メニューの 3D」モード（Scene 1）、美容室の小物の音、複製の帽子・肌の欄（2026-10-05、MEDIUM: 静的のみ。gohan での使用は実機未確認）'
summary: '解析モデル opus-5.5。IDB: `Player_SetHeadGoodsWithSound 0x68B238` を命名・注記。'
date: '2026-10-05'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6861368
- 1798596
- 5664248
- 5172696
- 5173680
- 1854108
- 8155220
- 1903340
tags:
- menu
supersedes: []
source: IDA:work/FINDINGS.md:4590-4604
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F083: 上画面の描画順と「メニューの 3D」モード（Scene 1）、美容室の小物の音、複製の帽子・肌の欄（2026-10-05、MEDIUM: 静的のみ。gohan での使用は実機未確認）

解析モデル opus-5.5。IDB: `Player_SetHeadGoodsWithSound 0x68B238` を命名・注記。
- **上画面の描画順**（`Frame_DrawPass1024 0x1B71C4`）: 影（Scene 2）→ 世界（`Render_DrawScene0`）→ **上画面の 2D（`ssys_ma_lyt_LayoutMgr_RenderTop 0x566DF8`）** → **メニューの 3D（`Render_DrawScene1`）**。
  Scene 0 と Scene 1 は `byte_94CA2C` で排他（0 = 世界、1 = メニュー。Scene 0 は 1 のとき `sub_6EE96C`（一覧を空にするだけ）で描かず、更新もしない）。
  → 2D の上に 3D を出すには Scene 1 モードで Scene 1 に積む（持ち物 `sub_1959D0`・カタログ `sub_21B1CC` と同じ）。
- 切り替え: `sub_4EF5DC` = カメラ（vc_POINT1）+424 ← +768（BsCamera_ActivateContext が Scene 1 へ積む印）、`byte_94CA2C = 1`、`dword_94C9D4 +360` を保存して 1。
  戻し: `sub_4EF27C` = +424 ← 0、`byte_94CA2C = 0`、+360 を保存値へ。+360 の意味は未確認（持ち物が使う順をそのまま借りる）。
- `Render_DrawSceneIndexed 0x4EEDD8` は Scene の番号ごとにカメラ（`sub_4E9EDC`、無ければ描かない）・更新・記録・再生をし、再生直後の late pass（0x4EF1B0）は Scene 0 / 1 共通。
  プレイヤーの部品の表は `BsPlayerMgr_SubmitPartLists 0x1C4A9C` → `PartList_SubmitAndClear 0x7C7054(list, 1)` で **Scene 0 にだけ**出る → Scene 1 で描く複製は体と部品を自分で Scene 1 にも積む。
- 美容室で頭の小物（帽子 +0x920・アクセサリー +0x924）を付け替える `Player_SetHeadGoodsWithSound 0x68B238`: 両方空なら `SE_ACT_BARBER_GOODS_OFF 0x10006B6`、それ以外は `_ON 0x10006B7`（Actor_PlaySound）。
  音の組は GROUP_SHOP / GROUP_MUSEUM（SEQSET_SE_ACTOBJ_SHOP）→ 村の外では読み込まれていない可能性（未確認。F054 の模様替えの音と同じ事情）。
- 複製の見た目の欄（`PlayerModel_UpdateParts 0x1D0AEC` と `sub_1D05B0`）: 帽子・アクセサリーは **pm+512 の服の欄の 0 / 1 枠**（`sub_719AF0(pm+128)` / `sub_719B24`）から毎フレーム読む、
  肌は **pm+448**（`PlayerLook_GetSkinRGB`）を帽子・頭・上着・脚へ毎フレーム。目の色（pm+556）はここでは使わない（顔のテクスチャ側。未確認）。

