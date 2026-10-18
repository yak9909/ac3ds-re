# HHD キャラクリ画面（髪型・目・色の設定）/ IDA-opus-5.5

2026-10-05、IDA（HHD IDB `ida/db/hhd_jpn_v11.i64`）＋ romfs 資源 / 解析モデル opus-5.5。
対象: どうぶつの森 ハッピーホームデザイナー（JPN、TitleID 0x000400000014F000）**v1.1（Rev 1、TitleVersion v2080）だけ**を見る。
目的（利用者）: この画面をとび森の髪型変更チートとして再現する。**プレイヤーモデルは対象外。**
確度: 資源の中身は HIGH 相当（ファイルそのもの）。コードの役割名は MEDIUM（静的のみ・実機未観測）。RTTI が無いのでクラス名はすべて役割から付けた仮名。

参考画像: `inputs/hhd/screenshots/*.bmp`（400x480 = 上 400x240 ＋ 下 320x240）、PNG と上下分割 `work/cache/hhd/screens/`（`tools/hhd/bmp_to_png.py`）。

## 1. 資源（romfs/Layout）

| アーカイブ | 中身 | 使い道 |
|---|---|---|
| `Layout/Face/Face.arc`（SARC、85 本） | bflyt 11・bflan 51・bflim 23 | 画面の全レイアウト・アニメ・共通テクスチャ |
| `Layout/FaceIconEye/FaceIconEye.arc`（48） | `sh_fce_{B,G}Eye_00..11.bflim`（目の形 64x32）＋ `sh_fce_{B,G}EyeB_00..11.bflim`（黒目） | 目の形ボタンの絵（B = 男の子、G = 女の子） |
| `Layout/FaceIconHair/FaceIconHair.arc`（32） | `sh_fce_{B,G}Hair_00..15.bflim`（64x64、白黒マスク） | 髪の形ボタンの絵 |

形式は **FLYT/FLAN 版 7.2.1.0**（BFLYT/BFLAN/BFLIM/BFFNT）。ACNL の `.bclyt`（NW4C）とは別系統なので、ACNL の知見をそのまま当てない。
展開: `python tools/hhd/extract_layouts.py`（3DSkit で `work/cache/hhd/layout/` へ。JSON と PNG ができる）。
ペインの木: `python tools/hhd/layout_tree.py <json>`（全部 → `work/evidence/hhd/layout/Face_trees.txt`）。
アニメ: `python tools/hhd/flan_summary.py <json>`（全部 → `Face_anims.txt`）。色の表: `python tools/hhd/export_palettes.py`（→ `palettes.json`）。

### 1.1 レイアウトの構成（座標は親の中心が原点、y 上向き。下画面 320x240）

- **fce_Top_00**（上画面 400x240）: 黄色の地 `P_Base_00`（my_cmn_Base8_00、白 #FFD400）＋柄 `P_Pattern_00`（my_cmn_ThmE_00、#FFA653、`loop` で V 方向に流れる）、
  吹き出し `W_Balloon_00`（ウィンドウ 512x256、×0.96/1.05）、小円 `N_Ccl_00`、文字 `T_turn_00`（「まわす」、Garden_msg_size16、18x24）。
- **fce_BG_00**（下 320x240）: 上と同じ地と柄。
- **fce_Face_00**（下）: 色パレットと下のボタン 2 つ。
  - `N_EyeColor_00`（顔モード）: 目のアイコン `P_EyeIcon_00`(-114,-42) ＋ `L_EyeColor_00..05` x = -82 + 28n、y = -42。
    肌のアイコン `P_SkinIcon_00`(-114,-70) ＋ `L_SkinColor_00..07` x = -82 + 28n、y = -70。
  - `N_HairSkinColor_00`（髪モード、既定は非表示）: 髪のアイコン `P_HairIconB_00` / `P_HairIconG_00`(-114,-56/-58) ＋
    `L_HairColor_00..07` y = -43、`L_HairColor_08..15` y = -70（x = -82 + 28n）。
  - `L_Btn_00`(-94,-103) = 部品 `fce_Btn_00`（赤い「かみがた」/「かお」ボタン）、`L_Btn_01`(96,-103) = 部品 `cbn_Btn_00`（水色の「けってい」）。
  - アニメ: `kind`（顔 ↔ 髪で N_EyeColor_00 / N_HairSkinColor_00 の表示を入れ替え）、`kindsex`（髪アイコンの男女）、`in` / `out`。
- **fce_EyeBase_00**（下）: 目の形 `L_Eye_00..11`（各 128x64 の部品）。列 x = -117 / -39 / 39 / 117、行 y = 88 / 44 / 0（番号は列ごとに上から）。`in`。
- **fce_HairBase_00**（下）: ページ `L_HairPage_00..02`（274x140、x = -276 / 0 / 276、y = 44）を横に並べ、`B_Page_00`（ページの当たり 322x154）と
  左右の当たり `B_L_00` / `B_R_00`（x = ∓161）。ページ送りは横スクロール（スクショで右端に次ページが覗く）。
- **fce_HairPage_00**: 1 ページ = `L_Hair_00..07`（70x70）。列 x = -102 / -34 / 34 / 102、行 y = 35 / -34（番号は列ごとに上から）。

### 1.2 部品（実行時にコードが中身を割り当てる）

ファイル内で部品名が入っているのは `L_Btn_00`→`fce_Btn_00`、`L_Btn_01`→`cbn_Btn_00` だけ。目・髪・色の部品はコードが作る（2 章）。

| 部品 | ペイン | 色の付け方 |
|---|---|---|
| **fce_Eye_00**（目の形ボタン 128x64） | `P_Base_00`（sh_fce_Skin_00 = 肌の板）、`P_Eye_00`（白目と輪郭 = sh_fce_{B,G}Eye_NN を差し替え）、`P_Iris_00`（黒目 = sh_fce_{B,G}EyeB_NN）、`W_Frame_00`（枠 78x38）、当たり `B_Btn_00` 77x38 | 肌 = P_Base_00 の白色、目の色 = P_Iris_00 の白色 |
| **fce_Hair_00**（髪の形ボタン 70x70） | `W_Frame_00`、`P_Skin_00`（sh_fce_Head_00 = 頭、白/黒 2 色）、`P_Face_00`（sh_fce_Face_00）、`P_Hair_00`（sh_fce_{B,G}Hair_NN を差し替え）、当たり 66x66 | 髪 = P_Hair_00 の白色（明部）と黒色（暗部）、肌 = P_Skin_00 の白黒 |
| **fce_Color_00**（色見本 32x32） | `P_Color_00`（sh_fce_Color_00）、`P_HighLight_00`（小さな円の光、-20°、α50）、`P_Frame_00`（選択枠、既定非表示）、当たり 26x26 | P_Color_00 の白色、光は色ごとに別色 |
| **fce_Btn_00 / cbn_Btn_00**（128x32） | 影 `P_BtnSh_00`、`P_Btn_00`（my_cmn_BtnCmn_00 ＋ Stripe）、`P_BtnFre_00`、文字 `T_Btn_00` / `TW_Btn_00`（Garden_msg_size16） | fce = 赤 #C81C00、cbn = 水色 #C8FFFA |

### 1.3 色の表（色番号 = アニメのフレーム番号）

`palettes.json` が正本。ボタンに付く値（白色 = 主の色）:

- 目の色 6: #000000, #B05838, #387860, #506870, #3858B0, #2068B0
- 肌の色 8: #FFBD94, #F8B68D, #F0AE8D, #E19F76, #D18F66, #C17F56, #B16F46, #A15F36
- 髪の色 16（髪ボタンの白色 / 黒色）: 0 #5A3939/#462828, 1 #945A29/#804615, 2 #EF5A31/#DB441E, 3 #42A5DE/#2E91C0, 4 #FFE77B/#E6C967,
  5 #8CCE63/#78BA4F, 6 #EF798C/#DB6578, 7 #F5EDD4/#E1CFB6, 8 #1B1B0F/#070700, 9 #5F0604/#370000, 10 #BE0C0C/#A00000, 11 #001056/#00062E,
  12 #DEA511/#CA9100, 13 #005825/#003A11, 14 #A977BE/#9563AA, 15 #7D795A/#696546
  （色見本の P_Color_00 では 7 = #FFF7DE、9 = #550604、11 = #00104C と少し違う）

### 1.4 状態のアニメ（ボタン共通の作り）

| タグ | 目・髪のボタン | 色見本 | 下のボタン |
|---|---|---|---|
| touch（押している） | N_Btn_00 を y −2 | y −2、選択枠を表示 | y −2、P_Btn_00 を 180° |
| touch_ok（離した） | y 戻し、縦 0.96→0.92→1.0 | 1.02→1.04→1.0 | 1.02→1.04→1.0 |
| select（選択中になる） | 枠を白 → 橙（白 #FF2300 系） | 枠 #FF3C00 | 文字を白 → 橙 |
| select_ok | 枠が黄 → 橙へ明滅 4 フレーム | 同 | 文字・地の明滅 |
| ng（選べない） | 全体を灰色 | 枠を灰 | 文字・地を暗く |
| loop | 枠の縞（Stripe）を斜めに流す | 同 | — |

## 2. コード（HHD IDB、静的のみ）

- 画面の組み立て **CharaCreate_LoadArchivesAndBuildLayouts 0x1EE5B8**: Face.arc / FaceIconEye.arc / FaceIconHair.arc を読み、
  fce_Face_00（CharaFaceLayout_Ctor 0x360B34、448 B）・fce_EyeBase_00（0x353180、412 B）・fce_HairBase_00（0x35EFF4、452 B、+244 = 髪アイコンの arc）・
  fce_BG_00（0x38C308）・fce_Top_00（0x38CA88）を作り、vtbl+72 で組み立てる。基底 LayoutObj_BaseCtor 0x3432F0（+24 = 資源、+32 = アニメ制御）。
- **目の形の絵**: CharaEyeBaseLayout_SetEyeIcons 0x352BA4 → EyeButtonPart_SetEyeTextures 0x3B1800(部品, arc, 番号, 性別) が
  `sh_fce_%sEye_%02d.bflim` を `P_Eye_00`、`sh_fce_%sEyeB_%02d.bflim` を `P_Iris_00` に差し替える（%s = g_EyeIconSexLetters {"B","G"}、性別はセーブの bit）。
- **髪の形の絵**: HairPageLayout_SetHairTexture 0x3BB190 が `sh_fce_%sHair_%02d.bflim` を `P_Hair_00` へ。**髪の番号 16 以上は女の子の組（番号 − 16）**。
- **色の反映**: 各部品の Set*Color（例 EyeButtonPart_SetEyeColor 0x3B1968）が値を控え（+0x1B4/+0x1B8/+0x1BC）、
  変わったときだけ **番号を float にしてアニメ枠 11〜13 のフレーム**にする（LayoutObj_SetAnimSlotFrame 0x3534C4）。
  枠の割り当て: 目 = 11 eyecolor / 12 skincolor、髪 = 11 haircolor / 12 skincolor、色見本 = 11 haircolor / 12 eyecolor / 13 skincolor
  （BindAnims 0x3BB0B0 / 0x3C08EC / 0x3D0A30。基本の枠 10 = "empty"、ButtonPart_BindBaseAnims 0x3AE668）。
- **色パレットの選択**: CharaFaceLayout_BuildColorGroups 0x35F5EC が選択グループ 3 つ（容量 {6, 16, 8}、g_CharaColorGroupCapacity）を作り、
  並び順の番号で各見本の色を設定する。SelectGroup_Update 0x3B8A38 はボタンの「押された」印（+270）を見て選択中（+20）を 1 つに切り替え、前のボタンを戻す。
  押されていなければ入力（+16、vtbl+164）で有効な次のボタンへ巡回する。SelectGroup_SetSelected 0x3B8920 = 番号を直接選ぶ。
  下ボタン L_Btn_01 には効果音 "SYS_2D_UI"。

## 3. とび森で再現するときの要点

- 絵（PNG）・座標・大きさ・色の表・アニメの値は 1 章とファイルからそのまま取れる。ACNL の acnl-ui-designer で並べるときは 1.1 の座標（中心原点）を使う。
- 髪の絵は白黒マスク。ボタンの色は「白い所 = 白色、黒い所 = 黒色」の 2 色で塗る（BFLYT のマテリアル色。ACNL の .bclyt でも同じ考えのマテリアル色が使える見込み・未確認）。
- 選択中の表現は枠の色（白 → 橙）＋縞の流れ、押下は y −2 と縮み。
- 未確定（TODO）: 十字キーでのカーソル移動の細部（選択グループの +16 入力）、回転部品 +280 の中身（ページの動き方・速さ）、シーン +8 の意味（新規作成か変更か）。

## 4. ボタンの状態機械（IDA-opus-5.5-HHD-F004、MEDIUM）

ボタンは実名 **ButtonBaseActor**（`StaticInit_ButtonBaseActorStates 0x5BC318` の文字列 "ButtonBaseActor::StateID_Init"）。状態機械はボタン +388、
状態は 17 個（各 48 B、g_ButtonBaseActor_StateID_*）: Init / In / Wait / Select / TouchSelect / UnSelect / TouchUnSelect / Decide / TouchDecide / DecideEnd /
Cancel / Invalidate / Validate / OnTarget / OffTarget / Float / Out。状態ごとに 4 つの仮想関数（vtable の +148〜+420）。

- アニメの枠（g_ButtonStandardAnimNames 0x78F328）: 0 ng / 1 touch / 2 touch_ok / 3 select / 4 select_ok / 5 in / 6 out / 7 drag / 8 drop / 9 drop2 / 10〜13 r90〜r360 / 14 kind。
  色の部品はこれに枠 11〜13 の色アニメを足す（2 章）。
- 入力から次の状態（`ButtonBaseActor_DecideNextStateFromInput 0x3983BC`、入力は +4 の物: +36 タッチ押し始め / +37 押している / +38 離した / +4 座標 / +12 離した座標 / +56・+40 ボタンの欄。どちらが押し始めかは未確定 → F007）:
  - Wait・UnSelect 系: 当たり（B_Btn_00）の中でタッチ開始 → **TouchSelect**。カーソルが自分に来た → **Select**。登録キー（+252、20 = 無し）→ **Decide**。
  - TouchSelect: 当たりの中で離す → **TouchDecide**、指が外へ → **TouchUnSelect**、ドラッグ可（+426）で動かす → **Float**。
  - Select: A（bit0）→ **Decide**、カーソルが外れる → **UnSelect**。
- 状態の処理は「入った最初のフレームでアニメを流し、+68 で数える」形。**TouchDecide**（0x399BA0）= touch_ok ＋ select_ok を流し、決定の印 +270 = 1 →
  touch_ok が終わったら DecideEnd。select 系の状態は select（3）、TouchSelect は touch（1）、In / Out は in / out、Float は drag を流す（呼び出しの定数から）。
- 選択グループ（2 章）は決定の印 +270 を見て、選択中を 1 つにする。`ButtonBaseActor_ToWait 0x398D20` = 前の選択を Wait へ戻す。

## 5. 髪のページ（IDA-opus-5.5-HHD-F005、MEDIUM）

`CharaHairBaseLayout_RefreshPages 0x35D954`:
- 髪は全 32 個（男の子 0〜15 / 女の子 16〜31）、1 ページ 8 個（ページ部品 +244）。+304 が立っていれば自分の性別の 16 個（2 ページ）だけ。
- 3 枚のページ枠（L_HairPage_00..02 = 左・中・右）を回転部品（+280）が回し、枠ごとに見せるページ番号を持つ（sub_567988）。
  枠 j の髪 = （女の子で絞り込みなら 16）＋ページ × 8 ＋ k（k = 0..7）を HairPageLayout_SetHairTexture で貼る。
- 選択の番号 = 枠内番号 ＋ 枠 × 8（選択グループ +256）。髪の色（+292）・肌の色（+296）はページの全ボタンへ一括（0x39BCF0 / 0x39BD7C）。

## 6. 画面全体の流れ（IDA-opus-5.5-HHD-F006、MEDIUM）

`CharaCreate_MainCalc 0x1EE0F8`（シーン: +1164 顔、+1168 目の一覧、+1172 髪の一覧）が毎フレーム、上から順に 1 つだけ処理する:
1. 「かみがた / かお」（L_Btn_00）が押された（顔 +308）→ 顔 +304 のモードで、0 = 顔なら目の一覧をプレイヤーの見た目で作り直して出し（vtbl+84）髪の一覧を引っ込める（vtbl+88）、
   1 = 髪なら髪の一覧を作り直して出し目の一覧を引っ込める（`CharaCreate_RefreshHairBaseFromPlayer 0x1EDECC`）。
2. 目の色が変わった（顔の選択グループ 0）→ 目の一覧の全ボタンへ。3. 髪の色（グループ 1）→ 髪の一覧へ。4. 肌の色（グループ 2）→ 目と髪の両方へ。
5. 目の形が選ばれた（目の一覧の選択グループ）→ 印を立て「けってい」を有効化（`CharaFaceLayout_UnlockDecideButton 0x360380`）。
6. 髪が選ばれた／ページ移動中は顔のボタンを無効／「けってい」→ 全部を無効にして次の状態（0x772860）へ。
- 「けってい」（L_Btn_01）は最初、シーン +8 == 0 なら無効（灰色）で始まる（`CharaFaceLayout_SetDecideButtonLocked 0x3603E8`）。スクショ `face_eye0_eyecolor0_skin3` の灰色の「けってい」はこれ。
- プレイヤーの見た目（`PlayerLook_Get*`、範囲の上限で照合）: +0 髪型（< 32）/ +1 肌（< 8）/ +2 髪の色（< 16）/ +3 目の形（< 13）/ +4 目の色（< 6）。性別はセーブの bit。

## 7. キーとページ送り（IDA-opus-5.5-HHD-F007、MEDIUM）

- キー番号 → sead のボタン（`PadKeyId_ToSeadMask 0x43E23C`、ACNL の実測ビット表と照合）: 0 A / 1 B / 2 X / 3 Y / 4 L / 5 R / 6 SELECT / 7〜10 十字 上下左右 /
  11〜14 スライドパッド / 15〜18 十字かパッド / 19 タッチ / 20 = 無し。ボタンは +252 にキー番号の配列を持てる（押すと Decide）。
- 髪のページ送り（`PageScrollLayout_Build 0x3931E4`、fce_HairBase_00 の基底）: ページ全体の当たり `Page_00`（ドラッグで Float）、
  キーだけのボタン 4 つ（A / B / **L / R**。L/R は +416 = 1）、当たり `B_L_00` / `B_R_00` があれば左右ボタン `L_00` / `R_00`。
  → ページは **L/R・左右の端のタップ・ドラッグ**で送る。
