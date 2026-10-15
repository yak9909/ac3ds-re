---
id: ACNL-F0602
aliases:
- IDA-opus-5.5-F086
title: 'プレイヤー本人の目の形をその場で変える手順・レイアウトの色の 1 要素の読み書き・書体の私用領域の記号（2026-10-06、MEDIUM: 静的のみ。gohan は実機未確認）'
summary: '解析モデル opus-5.5。IDB: `nwlyt_Pane_GetColorElement 0x73B508` / `nwlyt_Picture_GetVtxColorElement 0x73CB40` / `nwlyt_Material_SetColorElement 0x4BCC7C` /'
date: '2026-10-06'
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 7582984
- 7588672
- 4967548
- 8160380
- 2562300
- 2176972
- 6634196
tags:
- layout
- player
supersedes: []
source: IDA:work/FINDINGS.md:4630-4650
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F086: プレイヤー本人の目の形をその場で変える手順・レイアウトの色の 1 要素の読み書き・書体の私用領域の記号（2026-10-06、MEDIUM: 静的のみ。gohan は実機未確認）

解析モデル opus-5.5。IDB: `nwlyt_Pane_GetColorElement 0x73B508` / `nwlyt_Picture_GetVtxColorElement 0x73CB40` / `nwlyt_Material_SetColorElement 0x4BCC7C` /
`PlayerHeadSlot_StepDoubleBuffer 0x7C847C` / `PlayerHeadSlot_LoadStep 0x2718FC` を命名・注記。
- 実機（gohan e8a3e3b = hhd_t018d_test）: 全 PASS（目の形の即切り替え）。
- 本人の目の形: 顔のテクスチャは頭を読み込むとき（`PlayerHeadSlot_LoadStep`）に頭の枠 +668（顔 a）/ +672（顔 b）の顔の枠から結ばれる。頭は 2 つの読み込み先を交互に使う
  （`PlayerHeadSlot_StepDoubleBuffer`: 今の番号 [+36]&1、読み込み済みのキー +64+20×番号、違えばもう一方へ読んで ++[+36]）。
  → 顔の倉庫（管理役 +24+156）に新しい枠を `BankTable_Acquire 0x2137CC` で取り、記録から `PlayerFaceSlot_RequestLoad` で読み、頭の +668/+672 を新しい枠へ向け、
  今のキーの先頭を 0xFE にして読み直させる。[+36] が変わり +60 が 0 になったら pm+332/+340 の組を新しい枠に替え、数フレーム後に古い枠を
  `PlayerFaceSlot_Unload` + `BankTable_Release` で返す。表示中の頭と古い顔は入れ替わるまで触らない。頭の枠 = 管理役 +24+4148 の表、1 枠 1,304 B（+12 から）、pm+348/+352 の組。
  他に pm+332 を読む `sub_1AF3AC` / `sub_1A386C` は UI 側で、この差し替えに関係しない（前回確認）。反証条件: 実機で目が変わらない・頭が消える・枠が漏れる（場面転換で無限ロード）。
- レイアウトの色の 1 要素: ペインは仮想 +0x14 `GetColorElement` / +0x18 `SetColorElement`（16 = 不透明度 +0xB4、ほかは +0x1C / +0x20 の頂点色。Picture +0x140+idx、
  TextBox +0xD8 + 4×(idx>>3) + (idx&3)）。材質は `nwlyt_Material_SetColorElement`: [材質 +0x10 + idx]（0..3 黒、4..7 白）。アニメの値は +0.5 して 0..255 に詰めて切り捨て。
  HHD の「かみがた／かお」「けってい」の押下中の色 = 部品の select（1 フレーム）/ select_ok（8 フレーム）の CLMC・CLVC → 整数フレームで焼いて gohan で書く。
- 書体: Garden_msg_size16.bcfnt の CMAP に U+E000〜E07E の 127 字。字形を描いて確認: E000〜E005 = A B X Y L R、E006 / E041 = 十字キー、E049 = スライドパッド、
  E04A = C スティック、E054 / E055 = ZL / ZR、E058 = タッチ、E079〜E07E = 十字の上・下・左・右・上下・左右（利用者の一覧と一致）。
  gohan `Includes/Gui/FontGlyphs.h` と `tools/hhd/make_acnl_layouts.py` の GLYPH に定義し、生成器が両者を突き合わせる。
- 実機（hhd_t018e、gohan 0c231c8）: 音・押下中の色・上画面の文字は PASS（top 6,416/16,384 B）。**本人の目はその場で変わらず、その後の建物の出入りで無限ロード**。
  静的な見直し: `PlayerHeadSlot_StepDoubleBuffer` は呼ばれるたびにキー（`sub_7242EC` = 先頭バイト・+4・+8・+12 Item・+16..19 を比べる）を比べ、違えば裏へ読み、第 3 引数 0 では入れ替えず 3 を返し、全部品がそろったら `PlayerModel_UpdateParts` が第 3 引数 1 で呼び直して入れ替える。この部品の更新は PlayerModel vtbl[5] `sub_1D2CCC` からで、毎フレームの `AcPlayer_UpdateModel 0x653AD4` は呼ばない（複製は gohan が毎フレーム呼んでいた）。`vc_UPDATE` はプレイヤー +371 |= 0x28 を立てるだけ。→ 推定: けってい 1 回の印は顔の読み込み中に使われ、キーを壊した後は誰も頭を読み直さず入れ替わり待ちで止まり、新しい顔の枠を抱えたまま建物へ入って片付けが終わらなかった（F030 と同じ症状）。+371 の印を読んで vtbl[5] を呼ぶ箇所は未特定（LOW。仮想呼び出しで静的に追えていない）。
  対策（gohan 8939b56、hhd_t018f_test、未実機）: キーを壊した直後と 30 フレームごとに vc_UPDATE で印を立て直す。150 フレームで打ち切り、本人の頭・顔の組が変わったら（片付けの開始）即中止し、頭の顔の欄を古い枠へ戻して新しい枠を返す。状態の通知に `rf 段階 r結果 fフレーム k印の回数 d済んだ回数 a中止した段` を出す。

