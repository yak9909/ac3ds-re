---
id: ACNL-F0480
aliases:
- IDA-opus-5.5-F053
title: '模様替えの範囲選択・移動の吸着と音、持ち物の選択窓（ItemSelectWindow）の正しい使い方（2026-09-27、MEDIUM: 静的のみ。gohan のマップエディター段階 3 手直しは実機未確認）'
summary: '解析ソフト: IDA（主 IDB）＋ CRO の逆アセンブル（tools/patches/cro_rtti.py）/ 解析モデル: opus-5.5。利用者の指摘（範囲がマスに吸着しない・音が無い・'
date: '2026-09-27'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 8631272
- 2863040
- 2863420
- 2862152
- 2861232
- 2858844
- 6192116
- 8960640
- 8291464
- 5067184
- 8546528
- 5069772
- 2858852
- 2862920
- 2858908
- 2861996
- 2859676
- 2859680
- 2863008
- 8488232
tags:
- inventory
- map
supersedes: []
source: IDA:work/FINDINGS.md:1811-1848
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F053: 模様替えの範囲選択・移動の吸着と音、持ち物の選択窓（ItemSelectWindow）の正しい使い方（2026-09-27、MEDIUM: 静的のみ。gohan のマップエディター段階 3 手直しは実機未確認）

解析ソフト: IDA（主 IDB）＋ CRO の逆アセンブル（tools/patches/cro_rtti.py）/ 解析モデル: opus-5.5。利用者の指摘（範囲がマスに吸着しない・音が無い・
決定が切り上げ・下線がはみ出す・一覧の動きがゲームと違う）を受け、自前で決めていた所を全部ゲームの実装から取り直した。
検査 `tools/strc/verify_map_editor.py` の群 6・7 が下の番地・命令・リテラルを code.bin / CRO から読み直す（111 項目 0 失敗）。

- **範囲の点の吸着**（CollectChip sub_B359D4、ModuleIndoor）: 指をレイアウト座標にし、`x' = trunc((x + (1 マス×0.5 − 1)·sgn(x) + O) / 1 マス)·1 マス − O`
  （y も同じ。0.5 / 1.0 / −1.0 は VLDR リテラル、切り捨ては VCVT.S32.F32）。1 マス = エディター +129560（20.0）、O = +129568 / +129572。
  **O を書くのはエディターの ctor（0xB3E248、0.0）だけ**（ModuleIndoor 全体で ADD #0xA20 は ctor と sub_B359D4 の 2 か所、ModuleFtr は読むだけ）
  → ゲームの座標では部屋の中心 = 0 で、点は最寄りの格子線へ吸着する（ちょうど半分はやや 0 寄り）。
- **範囲の決め方**（sub_B5923C）: 吸着した始点と終点の四角（B_Group）と、各チップの当たり判定の四角を 1 画素縮めて重ねる → **四角に丸ごと入るマスだけ**。幅か高さが 0 なら何も選ばない。
- **CollectChip Neutral 0xB0AAF0**: 押した瞬間 始点 = 吸着点、音 **SE_SYS_FUR_POLY_START 0x100051D**（F052 の 0x100041D は誤記。訂正）。押している間 終点 = 吸着点で
  枠を更新（sub_B0ABF8: 中点・|差| + 10、**毎フレーム sub_583068(dx·dy)**）。離すと選んで始点・終点を 0 に戻す（枠は消え、選ばれたチップの縞で見せる）。
- **sub_583068**: SE_SYS_FUR_POLY_MOVE_FOR_SLT 0x100051E を鳴らし続ける（sub_6B121C の持続音）。変数 15 = min(|面積| × 0.0037037, 127)。
- 選択の音: 1 個以上選んだ **POLY_ON 0x100051F**（sub_B3D014、各チップに sub_B43330）、選択を解く **POLY_CANCEL 0x1000520**（sub_B3D5B0: 選択数 != 0 かつタッチの押した瞬間）。
- **チップの見た目**（アニメ名の表 CRO 0xB8E1F4: 0 in / 1 ng / 2 drag / 3 drop2 / 4 drop / 5 touch / 6 select / 7 loop / 8 touch_ok / 9 select_ok / 10-13 r90〜r360 / 14 out / 15 ng）:
  選択 = touch と select を G_Btn に結び終わりへ → 計算 → 外す（sub_B43330）。解除 = 同じ 2 本を先頭へ（sub_B2EB04）。loop（P_Btn_01 の縞の流れ 40 フレーム）は常に結ぶ。
  cip_01C_02x02 のアニメは N_All の拡大、P_Btn_00 / P_Btn_01 の表示、P_Btn_01 のマテリアル色・テクスチャ SRT だけを動かす（P_Btn_00 の色は触らない）。
- **移動**（ModuleFtr）: 行き先の単位 sub_B147EC = 世界座標を単位へ、境目から 2.0（CMP #0x40000000 ×4）以内なら前の値のまま。下画面のチップは単位の位置に描く。
  単位が変わるたび sub_B06E44 が **sub_5827D0(POLY_MOVE 0x1000527 / 置けなければ POLY_MOVE_OUT 0x1000528, s0 = 行き先の世界 x × 0.00625)**（VLDR 0x3BCCCCCD。
  1 個のときは sub_B08D8C が FUR_MOVE 0x1000522 / FUR_MOVE_OUT 0x1000523）。離すと sub_B07108 が置ければ **PUT 0x1000525**、置けなければ BACK 0x1000526 で戻す。
- **sub_5827D0 → sub_6B1530**: BGM に合わせた音程で鳴らす。+0xC5C != 0、+0xC5D == 0、+0xCB8 == 2（部屋を読み込むと sub_58231C → sub_6B11E8 が入れる）、
  +0xCCC != 0（+0xCB8 != 0 の間 毎フレーム +1、鳴らすと 0）のときだけ。連続すると音程表 0x83B3E8 で上がる。
- **ItemSelectWindow の使い方**（唯一の使い手 script::ChoiceStandardItem、ChoiceStandardItem は窓を +220 に持つ）:
  ctor **0x2BAFC0**（2,832 B）/ 壊す vt[0] **0x2BB13C** / 読込 **0x2BAC48**（自分の +36 に itm_slct_win.arc）/ 組立 **0x2BA8B0**(窓, 0)（済むと +12 = 待機 0x2B9F5C）。
  開く前（vt[12] 0x5E7BF4 → **sub_5E7838**）: 行 i の文字箱 *(+956+12i)（T_slct_cntnt）に文字、**文字箱と下線 *(+960+12i)（P_undrLine）の幅 +72 = 測った文字の幅**、
  決定音 *(+964+12i) = 表 0x88BA80[種類]（0 DECIDE / 1 CANCEL / 7 WIN_SELECT_ITEM_DECIDE / 8 ERASE / 9 COPY …）。使わない行は空文字列（+250 = 0 で出ない）。
  幅の測り方 **sub_5E9430**: TextWriter ctor 0x7E8488、+60 = 文字箱 +0xE0（書体）、RecomputeScale 0x4D51B0(s0 = +0xE4, s1 = +0xE8)、+84 = +0xEC、+80 = +0xF0、+76 = FLT_MAX、
  幅 = **0x8268E0**(writer, 文字列, 長さ)（写しで CalcStringRect → 右 − 左、s0）、dtor 0x4D5BCC。
  持ち物欄（sub_23FB5C）: 基準 +1236/+1240/+1244 = 項目のペインの大域位置（sub_71A250）、**+1204 = 項目のペイン**（sub_2B9D1C が +72/+76 の大きさを読む。0 だと落ちる）、
  名前の欄を隠す **0x2B9F64**(窓, 0)。開く **0x2BAF48**(窓, 取消の行)（待機のときだけ +1224 = 取消の行、状態 Select In 0x2B9F9C）。
  毎フレーム **0x2BABAC**（状態 → ButtonActionControl → Layout 計算）、描画 AddLayout(mgr, 窓 + 624, 1)。決定 = *(+12) == 0x2BA29C（+1212 = 行、+1228 = 窓の外のタッチで取消・音 0x10003C6）。
  閉じる = ChangeState(窓, 0x2BA2A0, 0)（vt[13] 0x2BAFA0 と同じ。ChangeState **0x818528** は状態表 +28 から enter を引いて呼ぶ）。閉じ終わりで +1231/+1232 = 1、行の音 = 0x10003C5 に戻る。
  開くと BsMenuMgr +508 = 11・手カーソルを隠し +64 を保存（閉じ終わりに戻す）。入力はゲームのタッチ（sub_520D4C(0x8000) と ButtonActionControl）。
- **F052 の訂正**: 「ゲームは文字箱の幅 130 のまま」（会話中の推定）は誤りで、ChoiceStandardItem が毎回測った幅にしていた。下線がはみ出した原因は、自前の窓で下線 P_undrLine の幅を変えていなかったこと。
- 主 IDB: ItemSelectWindow_* 15 個、ChoiceStandardItem_SetRows / _MeasureText、nwfont_TextWriter_CalcStringWidth / _Ctor を命名、注記 6、保存。
- 反証条件: 実機で一覧が開かない・落ちる（+1204 や状態の値の読み違い）、範囲がゲームと違う格子に吸着する（O が 0 以外に書かれる経路がある）。

