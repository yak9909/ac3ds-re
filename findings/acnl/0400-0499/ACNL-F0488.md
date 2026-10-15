---
id: ACNL-F0488
aliases:
- IDA-opus-5.5-F045
title: 'キーボードのキーの見た目・テクスチャの取り方・開閉アニメ・切り替え音・カーソル設定の引数（2026-09-26、MEDIUM: 静的＋romfs。実機未確認）'
summary: チャットの自前キー（全選択・左右）をゲームのキーで描き、開閉アニメに追従させるための下調べ（gohan 058e1a5）。
date: '2026-09-26'
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1183060
- 9438692
- 4937796
- 5666096
- 5666504
- 4968104
- 4954160
- 4946020
- 5754628
- 7627216
- 5382176
- 5753632
- 8721416
- 5755972
- 8060996
tags:
- keyboard
supersedes: []
source: IDA:work/FINDINGS.md:1996-2042
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F045: キーボードのキーの見た目・テクスチャの取り方・開閉アニメ・切り替え音・カーソル設定の引数（2026-09-26、MEDIUM: 静的＋romfs。実機未確認）

チャットの自前キー（全選択・左右）をゲームのキーで描き、開閉アニメに追従させるための下調べ（gohan 058e1a5）。

- **キーの組み立て**（`swkbd_kana.arc` の `Keytop_50on.bclyt`）: 1 キー = Picture（`Ktp50onKey00` 24x22 / `Ktp50onKeyBsp` 38x22 など）+ TextBox + 当たり判定（bnd）+ グループ。
  見た目 = テクスチャ x (material 色[0]·(1−tex) + 色[1]·tex) x 頂点色（上下のグラデーション）。例 `P_key_Bsp`: 色[0] (140,65,35,0)、頂点 上 (210,138,70) 下 (150,95,45)。
  押下は `Keytop_50on_n0s1` / `s1t0` の CLTP で `…on.bclim` へ差し替え（押下テクスチャはレイアウトではなくアニメのファイル一覧にある）。
- **かなの部品はかなキーボードの間しか無い**（`BsSkb_InitStep` 段 3 が今のキー配列の arc だけを読む）。常にあるのは `swkbd_common.arc`（段 1、BsSkb+788）の
  `KeytopModeSelect`（「ABC」「あいう」「記号」「ケータイ」）: `P_ktpMode_00..03`（`KtpModeL` / `C` / `C` / `R`）。material 色[0] (80,45,25,0)、頂点 上 (185,105,45) 下 (82,40,8)、
  文字 色[1] (255,240,185)。選択中（`KeytopModeSelect_n0s1` フレーム 1）: `KtpModeCon`、頂点 上 (255,160,102) 下 (255,237,210)、文字 (184,94,58)。無効（`_i0`）: 頂点 146 灰・文字 100 灰。
- **文字色 = TextBox の material 色[1]**（画面の画素で照合: 消去 (57,20,0) ≒ `T_key_BspJP` 色[1] (60,20,0)、かな (90,28,0) ≒ `T_key_00` (90,30,0)）。キーボードの枠 (82,40,16) = #522810。
- **テクスチャの取り方**: `ssys::ma::lyt::ArcResAccReader`（ctor `0x120D54`）の +12 に `ArcResourceAccessorVRAM`（vtbl 0x9005E4）。vtable +0x10 =
  `nwlyt_ArcResourceAccessor_GetTexture 0x4B5844`(out TextureInfo 20 B, this, 名前): 控え（this+48）から、無ければ +0x14（`ssys_ArcResourceAccessorVRAM_LoadTexture 0x567530`
  → `ssys_LoadBclimToVram 0x5676C8`）で読み込んで控える。TextureInfo = {?, 番地, 使う大きさ w|h<<16, 2 の冪の大きさ, 書式 byte}。
  Material の ctor（`0x4BCEA8`）はこれを TexMap +0x00..+0x0C へ写し、+0x10 = 書式<<8 & 0xF00 | ラップ | フィルタ（資源の texMap バイト 2・3 から）にして
  `nwlyt_TexMap_UpdateGpuRegs 0x4B9830` を呼ぶ。KeytopModeSelect の material は rawS/rawT = 4 → +0x10 の下位 = 0x90（線形・クランプ）。
  swkbd_common のアクセサ = BsSkb+800（`BsSkb_InitStep` の `sub_4B3FD4(a1+800, …)` と一致）。
- **Material_EmitState 0x4B7864** は +0x4D bit2 を見ない。テクスチャのレジスタは TexMap から出る → 共有 Material の写しに TexMap を入れ替えればよい。
- **開閉アニメ**: `BG_in`（10 フレーム、N_All の y −240 → 5 → 0）/ `BG_out`（5 フレーム、0 → −240）は `swkbd_common.arc` の `BG.bclyt`（BsSkb+1372）の `N_All` だけを動かす。
  `BsSkb_WindowOut_Calc 0x57CF04` は `lyt_Object_FindPane 0x7461D0`(BG, "N_All") の平行移動（ペイン +0x28..+0x30）を、キーボードのほかのレイアウトの根
  （+4364 KeytopModeSelect、+1384、+1428、+4368、キー配列 +4416 vt+32）へ写す → 同じ値を読めば追従できる。`lyt::Object`+72 = 根のペイン。ペインの名前は +0xB8、子リストの番兵は +0x14。
- **切り替え音**: `BsSkb_InitStep` が KeytopModeSelect のキーに渡す音 16778208 = 0x10003E0 = `SE_SYS_SWK_CHANGE_KEY_SET`（音の一覧で確認。16778200 = 0x10003D8 = `SE_SYS_SWK_KEY`）。
- **`TextManager_SetCursor 0x522020`(tm, 位置, 選択を解く, 起点も動かす)**: 最後が 0 だと起点（+28）を残して +32 = 1（選択中）。全選択 = (0,1,1) → (文字数,1,0)。
- 反証条件: 実機でキーが別の色・別の形に出る、押下の見た目にならない、音が違う、開閉のずれが目に見えて遅れる。
- IDB: 上の関数を命名・注記。
- **追記（2026-09-26、利用者の実機確認を受けて）**: 見た目は切り替えキーではなく**今のキー配列の空白キー**に変えた。空白キーはどのキー配列も色が同じ
  （P_key_Spc: 色[0] (140,65,35,0)、頂点 (210,138,70)/(150,95,45)、T_key_Spc 色[1] (60,20,0)。*_n0s1 フレーム 1: 頂点 (255,177,129)/(255,232,195)、文字 (184,94,58)、
  文字 +1,+1）。テクスチャ名: かな Ktp50onKeySpc / qwerty KtpQweKeySpc / grid KtpGrdKeySpc / cell KtpCellKeyOpt01min1（+on）。どれも rawS/rawT 4。
  キー配列の arc のアクセサ = BsSkb+1436 の ArcResAccReader +12 = **BsSkb+1448**（`BsSkb_InitStep` 段 3 の `sub_4B3FD4(a1+1448, …)` と一致）。
  キー配列の種類 = dword_AD0544、キー配列の実体 = BsSkb+4416。開くアニメの間は BsSkb 状態 #0 "window in" の calc `0x57CB20`（表 0x851408）が回る。
  音 `SE_SYS_SWK_BACKSPACE` = 0x10003DA（`TextManager_Backspace` が消せたときに鳴らす 16778202。消せないとき 16778203 = `SE_SYS_SWK_ERROR`）。
- **追記 2（2026-09-26）**: キー配列の背面 = Window ペイン `W_ktpShade`（4 種とも RootPane/N_keytop/N_key の子、木の順 3（キーは 6 から）= キーより先に描く、320x142、
  平行移動 (0,-27)、中の色 (82,42,23)、枠 `KtpShade`）。画面では上端 y65（透明）、縁 y66..67、キー y68。キー配列の vt+0x20 は 4 種とも `LDR R0,[R0,#0x110]`
  = キー配列+0x110 がそのレイアウト（lyt::Object、+72 が根のペイン）。`sub_4B6530` = Pane の平行移動（+0x28..+0x30）を書き +0xB7 の bit4-5 を落とす（行列の作り直し）。
- **追記 3（2026-09-26）**: キーの角の丸みはテクスチャのアルファで、**キーボードの外周に面した角だけ**（Ktp50onKeyBsp = 消去 → 右上、Ktp50onKeySpc = 空白 → 右下、
  Ktp50onOpt01 = カナ → 左下。LA4）。BCLIM の行は上から（`tools/layout/bclim_png.py` の `px.reverse()` は F040 の訂正と同じく上下が逆になる。行 0 を下として読んだ）。
  qwerty / grid / cell の空白キーは L4（アルファ無し）。角の形の例（Bsp 右上）: 角 0、横隣 0.73、縦隣 0.73、縦にもう 1 つ 0.87。
- **追記 4（2026-09-26）**: キー配列の切り替え = BsSkb 状態 #25 "keyset load" の calc `0x57D444`: 今の種類（BsSkb+4360）の arc を `ArcResAccReader_LoadArcStep`(BsSkb+1436)
  で読み終えた回に `sub_57B2E0`(BsSkb, 種類) を呼ぶ。`sub_57B2E0` は古いキー配列を vt[0] で破棄して BsSkb+4416 = 0、新しいもの（qwerty sub_4F8744 / kana sub_4F582C /
  grid sub_4F4074 / cell sub_4FC4B8）を作って init が通れば +4416 に入れる。その後 wait（`BsSkb_Wait_Calc`）へ。モード切替キーの `sub_57C7F4` は dword_AD0544 を書くだけ。
  → +4416 は calc の間で解放済みを指さない。

- **追記 5（2026-09-26）**: **VRAM への読み込みは非同期**。`ssys_LoadBclimToVram 0x5676C8` は VRAM を取ってから `GxQueue_AddRequestDma 0x7B0044`(src, dst, 大きさ)
  で GX の命令（種類 0）を `g_GpuCmdListMgr` の列（28 B / 件）へ積むだけ（列が止まっていれば `GxQueue_Dispatch` を起こす）。
  → `GetTexture` で初めて取ったテクスチャ（押下の `…on` など）は、直後にはまだ VRAM に無い。gohan は取った直後に写していたので押下のキーが乱れた（利用者の報告）。
  取ってから 10 フレームは VRAM のものを使い、その後に写すよう直した（gohan b4bae7f）。反証条件: 直したあとも押下の見た目が乱れる。

