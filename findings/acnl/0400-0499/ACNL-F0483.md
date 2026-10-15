---
id: ACNL-F0483
aliases:
- IDA-opus-5.5-F050
title: '模様替え UI（BsMenuInteriorEditor）の作りと、持ち物欄の名前の吹き出し（ItemSelectNameWindow）の使い方（2026-09-27、MEDIUM: 静的のみ（逆アセンブル＋romfs）。実機未確認）'
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「マップエディター（gohan Issue #16）」の下調べ。'
date: '2026-09-27'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 8324104
- 1379468
- 6961880
- 3269296
- 3269228
- 3268300
- 3267464
- 3267428
- 8861532
- 3267708
- 3267588
- 3267852
- 3266588
- 3266824
- 3132604
tags:
- inventory
supersedes: []
source: IDA:work/FINDINGS.md:1878-1915
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F050: 模様替え UI（BsMenuInteriorEditor）の作りと、持ち物欄の名前の吹き出し（ItemSelectNameWindow）の使い方（2026-09-27、MEDIUM: 静的のみ（逆アセンブル＋romfs）。実機未確認）

解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「マップエディター（gohan Issue #16）」の下調べ。

### 1. 模様替え UI は ModuleIndoor.cro にあり、村では使えない
- `BsMenuInteriorEditor`（プロファイル 0x265、129,592 B）の生成 `0x7F0408` が呼ぶ `0x150C8C` は CRO への中継。行き先は **ModuleIndoor seg0 0xB3E0F8**（`tools/patches/crs_import_slots.py`）。
  ModuleIndoor は部屋フラグ bit8 のときだけ積まれる（Room_SelectModules 0x6A3AD8、docs/topics/unit_cursor_outdoor.md）。
- CRO を IDA で読む道具 `tools/patches/cro_to_elf.py`（再配置済み ELF。取り込みスタブに `imp_<主 IDB の名前>` の記号）と、
  名前付き状態表の一覧 `tools/patches/cro_state_tables.py` を足した。番地は cro_rtti と同じ便宜上の基準（text 0x00B00000）。
- 状態表（ModuleIndoor）: エディター 0xB6240C（Idle/In/Neutral/Out/CommonButtonIn/Out）、Chip 0xB62778（Idle/In/Neutral/Out/Select/Decide/Rotate/Drag/Drop）、
  CollectChip（範囲選択の枠）0xB62894（Idle/Neutral）。
- エディター Neutral（0xB3D1E4）は 112 個（0x70）のチップを **上に載っている物 → それ以外** の順に回して入力を配る（上の物が優先）。
  どのチップも取らなければ CollectChip（範囲選択）へ。
- チップ（1,120 B、ctor 0xB433E4）: +36 Layout / +368 アニメ 16 本（名前表 0xB8E1F4）/ +1008 N_All / +1012 B_Btn_00 / +1016 N_Rotate_00。
  Select 状態（0xB429BC）: **6 フレーム押し続けるか、押した点から 24.0 以上動くとドラッグ**（0x41C00000）。それより前に離すと Decide → Rotate（タップ = 回転）。
  範囲選択（CollectChip Neutral 0xB0AAF0）: 押した点から枠を伸ばし、離して確定。
- 位置: N_All の平行移動 = ModuleFtr 0xB0F758 の式 `x = 原点x + (世界x − 部屋の原点x)/32 × 20`、`y = 原点y − (世界z − 原点z)/32 × 20`
  （エディター +129560 = 1 マスの大きさ 20.0、+129568/+129572 = 原点）。向きは N_Rotate_00 の z 回転 = 向き × 90。
- チップの種類（Chip の組み立て 0xB420C4 が sub_B5A70C で表 0xB8E1C0 の番号を選ぶ）: 大きさ = ItemParam+23 & 0xF（0 1x1 / 1 1x2 / 2 2x2 / 3 2x3 / 4 3x3、sub_303128）。
  P（上に物を置ける）= sub_768448、W（壁）= sub_303BA0、ほかは `!sub_769D14 && sub_30B7BC` なら N、そうでなければ C（上に置ける物）。
  レイアウトは chip.arc の cip_01{N,P,C}/02W_{02x02,02x04,04x04,04x06,06x06}。P は 1x1/1x2/2x2 だけ、2x3/3x3 は N だけ。
- 盤面 chip_room_00.bclyt。アニメ chip_room_00_kind のフレーム 0/1/2 = 80/120/160 四方 = 4x4/6x6/8x8 マス（フレーム 3/4 は入口の位置だけ）。

### 2. 持ち物欄の名前の吹き出し = ItemSelectNameWindow（code.bin、約 1,264 B）
- 資源 `Layout/ItemWin/itm_slct_win.arc` の itm_slct_win.bclyt の **N_itm_nm_00**（枠 W_itm_nm_00・文字 T_itm_nm_00、アニメ in_itm_nm / out_itm_nm、群 G_name）。
- ctor 0x31E2B0 / arc 読み込み 1 段 0x31E26C（終わると +1261 = 1）/ 組み立て **0x31DECC(窓, 保持体 or 0)**（Vapecord の FACE_EXPRESSION は誤名）/
  表示 **0x31DB88(窓, 語, 基準ペイン, &ずれ[3])**（+964 = 基準ペイン、+1248 = ずれ。出ていなければ状態 1 へ）/ 隠す 0x31DB64 /
  状態表 0x87375C（0 待機・1 入場 enter 0x31DC7C calc 0x31DC04・2 退場 calc 0x31DD0C）。毎フレームは +12 の calc を呼ぶ。
- 幅合わせ 0x31D81C（文字幅 + 30、N は × 0.94）、位置 0x31D908（基準ペインの大域位置 +140/+156 + ずれ。上下は y > 120 で反転、横は ±160 に収める）。
- 同じ形で下画面の地図（BsMenuMapVillage、sub_2B3624）が施設名を出している。アイテム名の語は sub_2FE9FC(buf, &item, 0)（チャットの頭上の吹き出し sub_215EA4 と同じ）。
- ※ itm_balloon.arc はチャット管理（vc_CHATPOINTER）の頭上の吹き出しで、持ち物欄のものではない。
- ModuleIndoor にも同名クラスの写しがある（収納の画面用）。模様替えのタップ自体は回転で、名前は出さない。

### 3. fgobj と村のアイテム
- fgobj = Item_IsFieldObj 0x2FCCBC（ID & 0x7FFF <= 0xFD）。書き込みは Field_SetItemAtWorldXY 系＋Field_MarkDirty（IDA-opus-5.5-F005）。

反証条件: ModuleIndoor が屋外で積まれている、チップの位置が別の式、名前の吹き出しが別の資源から出ている。

