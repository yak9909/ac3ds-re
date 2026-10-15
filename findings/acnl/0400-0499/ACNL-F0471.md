---
id: ACNL-F0471
aliases:
- IDA-opus-5.5-F062
title: '村の下画面の建物一覧（BsMenuMapList）の作りと、マップエディターのモード一覧への流用（2026-09-28、MEDIUM: 静的＋描画器での照合。gohan 実機未確認）'
summary: '解析ソフト: IDA（主 IDB を idalib-mcp で静的）＋ acnl-ui-designer の描画器 / 解析モデル: opus-5.5。利用者指示: 地図の右の建物一覧をマップエディターの下画面左端に出し、'
date: '2026-09-28'
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 2248716
- 2249232
- 2246580
- 2246060
- 2243964
- 2829804
- 2246400
- 2245428
- 2827112
- 2247560
- 2831580
- 2831800
- 2245096
- 3109572
- 2834072
- 2242860
- 3106832
- 3104500
- 3107880
- 3106452
tags:
- map
supersedes: []
source: IDA:work/FINDINGS.md:1634-1655
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F062: 村の下画面の建物一覧（BsMenuMapList）の作りと、マップエディターのモード一覧への流用（2026-09-28、MEDIUM: 静的＋描画器での照合。gohan 実機未確認）

解析ソフト: IDA（主 IDB を idalib-mcp で静的）＋ acnl-ui-designer の描画器 / 解析モデル: opus-5.5。利用者指示: 地図の右の建物一覧をマップエディターの下画面左端に出し、
項目は配置・削除・選択のモードだけ。ゲームとの違いは「開閉できない・ずっと開いた・選択を解除できない・アイコンを描かない」の 4 つだけ（推測で解析しない）。詳細と表は work/evidence/map_editor/mode_list/analysis.md。
- **作り**: BsMenuMapList（ctor 0x22500C / dtor 0x225210、村の地図 BsMenuMapVillage +48744）。地図の生成段 4〜6 = SetupLayout 0x2247B4（list_00.bclyt・アニメ 6 本・優先度 0x81）/
  SetupRows 0x2245AC（MapIcon・N_icon・T_msg）/ SetupButtons 0x223D7C（開閉 +7608・ページ +8060・行 +8736 の ButtonActionControl）。書体は地図の組み立て sub_222BC8 がスロット 0/1 を保持体 +12 へ。
  ListIn: FillListEntries 0x2B2DEC（AddEntry 0x224700 = {id, 種類, アイコン}、最大 28）→ UpdatePageButtons 0x224334 → FillListRows 0x2B2368（SetRow 0x224B88。空の行は項目 27・非表示）。
- **選択**: 行の決定（ListProc 0x2B34DC〜0x2B35B8）= 前の行 SetSelected 0x2241E8(0) → 行 BAC +212 &= ~8 → ClearDecided 0x2F72C4 → SetSelected(行, 1)。
  見た目 = N_slct_00（帯）を行へ・P_base_00 の α と、ノード +215・select_ok（文字色 (25,155,20)）。**一覧は選択を持たず、村では地図アイコン +608 が持つ**（決まらないフレームは ClearListSelection 0x2B3E98）。
  地図アイコンからの選択 = SelectById 0x22392C（末尾で +215 = 1 と touch_ok / select_ok を最後へ）。
  行 BAC（ButtonActionControl）: 待ち 0x2F6810 → タッチ 0x2F5EF4（**押した瞬間、当たっていないノードは全部 SetSelect(0)**）→ 離した所が当たりなら Decide 0x2F6C28 → 決定アニメ 0x2F6694 → +212 bit0。
  タッチは 0xACF6E0 の構造体（Touch_UpdateState 0x1B7874。+0 押している、+26 = 前のフレームの +0、+10/+12 位置）。当たり判定 sub_4BE2A4 はペインの矩形だけ。
- **開いたまま**: 部屋 164（ID 一覧 Room_IDS: Amiibo Camera）でゲーム自身が OpenFixed 0x224E4C（in_list を最後のフレームで当てて矢印 P_list_arrow_00 を隠す）を使う。
- **レイアウト**（romfs 更新版 map_village.arc、描画器で村の画面 09-14-02 と照合）: 窓 W_list_win_00 は行・紙の親（行のアニメは N_icon の y を絶対値で書く）。
  紙 P_list_note_00 は 8x256 の 1 枚絵（細縞 周期 4、罫線 t = 108 + 20k）、オレンジ中段 P_list_win_01 は周期 4.111px。窓の辺は角の端を伸ばし中身は単色。
  nw::lyt Pane::InsertChild(next, child) = 0x4B6100、Picture: +0xD4 = UV 済み（0 で作り直し、0x73CB88）、+0x13C マテリアル、+0x140 頂点色、+0x154 座標（4 隅 × (u,v)）。TextBox +0xFC 寄せ。
- **gohan（MapModeList.cpp、実機未確認）**: 上の関数で組み、OpenFixed で開いたまま、行 BAC だけ回す（その呼び出しの間だけ 0xACF6E0 に一覧の上で始まった指を書いて戻す）。決まった行 → モード。
  L / R で変わったら SelectById、離して取り消したら SelectById の末尾と同じく見た目を戻す（= 解除できない）。アイコンは組むが描かない（Draw は Layout だけ）。
  形: ページボタンを隠す、窓は基準点を下・高さ 90.5（90.5 詰め）、中段を 57.5 に（周期 22 回分とほぼ同じ）、紙は上 t<148 と下 t≥240 の 2 枚（下は矢印の Picture にマテリアルを差し替え、N_slct_00 の直前へ）、
  文字を右寄せ、N_list x = −221.6（タグの右端が盤面の枠 67）、優先度 2 で盤面の先に登録。数値は tools/layout/mode_list_preview.mjs と verify_map_editor 群 13 が突き合わせる。
- 反証条件: 実機で一覧が出ない・落ちる（Setup の前提の読み違い）、タッチで選べない（0xACF6E0 の欄の読み違い）、切った所に継ぎ目・ずれ、選択が消える。

