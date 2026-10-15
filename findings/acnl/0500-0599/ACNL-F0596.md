---
id: ACNL-F0596
aliases:
- IDA-opus-5.5-F080
title: 'ACNL の見た目の記録と色の表。HHD の番号がそのまま使える（2026-10-05、MEDIUM〜HIGH: 静的 2 経路（命令の復元と HHD のデータ）の一致。実機での反映は未）'
summary: '解析ソフト IDA（idalib-mcp）、解析モデル opus-5.5。段階 3（プレイヤーへの反映）。利用者指示: 反映するのは髪型・髪色・目の形・目の色・肌の色、まずオフラインだけ。'
date: '2026-10-05'
category: actor
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 7413532
- 7413564
- 7413516
- 7413548
- 7413580
- 7413608
- 7954232
- 11335128
- 11335146
- 2151208
- 11335170
- 6856156
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4546-4564
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F080: ACNL の見た目の記録と色の表。HHD の番号がそのまま使える（2026-10-05、MEDIUM〜HIGH: 静的 2 経路（命令の復元と HHD のデータ）の一致。実機での反映は未）

解析ソフト IDA（idalib-mcp）、解析モデル opus-5.5。段階 3（プレイヤーへの反映）。利用者指示: 反映するのは髪型・髪色・目の形・目の色・肌の色、まずオフラインだけ。

- **見た目の記録**（profile+4。`LookRecord_Get*` を命名）: +0 髪型 <34（LookRecord_GetHairStyle 0x711F1C）/ +1 髪色 <16（0x711F3C）/ **+2 顔＝目の形 <12（LookRecord_GetFace 0x711F0C）**/
  +3 目の色 <6（0x711F2C）/ **+4 日焼け 0..15、見た目は >>1 で 8 段階**（vc_GETTANDATAOFFSET 0x711F4C）。16 / 33 は寝癖（LookRecord_IsBedHair 0x711F68）。
  旧資料（F-66〜F-68）の profile +4 / +5 / +7 と一致。+6（顔）・+8（日焼け）は今回確定。
- **色の表**: `PlayerLook_InitColorTables 0x795F38`（命名）が即値で書く（MOV / STRB / ADD だけ。tools/acnl_look/decode_look_colors.py が命令から復元、
  出力 work/evidence/hhd/acnl_look_colors.txt）: 目の色 6×RGB `g_LookEyeColorRGB 0xACF5D8`、肌 8×RGB `g_LookSkinColorRGB 0xACF5EA`（PlayerLook_GetSkinRGB 0x20D328 が段階で引く）、
  髪の色 16×RGB `g_LookHairColorRGB 0xACF602`。
- **HHD との照合**: HHD の色見本（palettes.json）と番号ごとに比べ、目の色 6/6・肌 7/8（2 番の B が ACNL 0x85 / HHD 0x8D）・髪の色 16/16（色見本 fce_Color_00_haircolor の値。
  髪の絵の色 fce_Hair_00_haircolor とは 3 色が違う）→ **番号の並びは同じ**。髪型は HHD-F008（k → k / 17+(k−16)）、目の形は 0〜11 が同じファイル名。
- 対応: HHD 髪 k → 髪型 k (<16) / 17+(k−16)、髪色 = そのまま、目の形 = そのまま（性別の組は ACNL のプレイヤーの性別のまま）、目の色 = そのまま、肌 s → 日焼け 2s。
- 反映の手順（既知）: 髪型・髪色・目の色は profile に書いて vc_UPDATE 0x689DDC（旧 F-68、実機確認済み）。**vc_UPDATE は顔（+6）と日焼け（+8）を読み直さない**
  → 顔と日焼けの即時反映の経路は未調査（PlayerModel_UpdateParts は pm+448 の段階で肌の色を作る。顔の絵の読み込みは未確認）。
- **追記（同日）**: 顔の絵は `sub_2711AC`（LookRecord_GetFace を読み Player/face_tex/{boy|girl}%02d{a|b}.bcres）が **PlayerModel_CreateStep からだけ**呼ばれる → 目の形はモデルが作り直されたときに出る。
  日焼けは PlayerModel_Setup が `pm+448 = vc_GETTANDATAOFFSET(記録)`・`pm+452 = 記録` に入れ、PlayerModel_UpdateParts が毎フレーム `PlayerLook_GetSkinRGB(pm+448)` で肌の色を作る
  → pm+448 を書けば次の部品更新で頭・体が作り直される見込み（実機未確認）。gohan に「けってい」で反映（記録 +4..+8、pm+448、vc_UPDATE。通信中は書かない）を実装（未実機）。

