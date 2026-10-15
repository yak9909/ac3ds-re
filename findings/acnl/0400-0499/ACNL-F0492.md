---
id: ACNL-F0492
aliases:
- IDA-opus-5.5-F041
title: '一覧の選択中の行とスクロールバー（CommonScrollBar）の見た目の規則（2026-09-25、HIGH: 静的＋実機画像 1 枚との照合）'
summary: 設計ツール `src/acnl-ui-designer`（3af30a5）の `instselect.mjs` / `scrollbar.mjs` の根拠。表は同リポジトリ `docs/verification.md`。
date: '2026-09-25'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1767840
- 3109960
- 2847392
- 1767512
- 2847016
- 2846880
- 5671208
- 4941064
- 4939996
- 5667408
- 7455536
- 9350036
- 2727912
- 2726160
- 2726752
- 2722728
- 2721704
- 2719992
- 2719768
- 2214696
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2093-2110
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F041: 一覧の選択中の行とスクロールバー（CommonScrollBar）の見た目の規則（2026-09-25、HIGH: 静的＋実機画像 1 枚との照合）

設計ツール `src/acnl-ui-designer`（3af30a5）の `instselect.mjs` / `scrollbar.mjs` の根拠。表は同リポジトリ `docs/verification.md`。

- 選択の準備 `InstSelect_SetupRows 0x1AF9A0`: ButtonActionControl（一覧+2560）が `<layout>_touch/_select/_touch_ok/_select_ok` を読み（`ButtonActionControl_LoadAnims 0x2F7448`）、行ノード（ButtonActionNode 224 B、ctor `0x2B72A0`、アニメ +32 touch / +72 select / +112 touch_ok / +152 select_ok）に N_list_XX と G_list_XX を持たせる。select_ok を最終フレームで G_slct_00 に当て（P_slct_00 の α = 255）、P_slct_00 を親から外す。
- 選択 `InstSelect_SetSelectVisual 0x1AF858`（新, 旧）: 見えている行 = 番号 − 先頭（+2368）。旧行 vt+32（`0x2B7128`）→ +215 = 0・select をフレーム 0。新行 +215 = 1、touch_ok と select_ok を最終フレーム（`ButtonActionNode_PlayAnim 0x2B70A0`: グループへ結合 → フレーム 0 → 必要なら `UiAnim_SetFrameToEnd 0x568928`（frameSize − 1）→ 当てる → 外す。補間しない）。最後に P_slct_00 を N_list_XX の**先頭の子**へ（`nwlyt_Pane_PrependChild 0x4B6508`。`AppendChild 0x4B60DC` は番兵の前＝末尾）→ 行の文字の奥に描かれる。
- グループへの結合 `vc_ACSYSTEM_DATA1 0x567A50`: グループの各ペインに Pane vt+60（再帰 0）→ そのペインと自分のマテリアルだけ。G_list_XX = T_itm_XX だけなので、select_ok の CLMC で文字の色[1] が (25,165,210)、P_slct_00 は動かない。
- 行ノード +217 = 有効（vt+8 `ButtonActionNode_IsEnabled 0x71C330` = LDRSB +0xD9、ctor で 1）。選択中の行と最後の 2 行は 0。
- スクロールバー = RTTI `CommonScrollBar`（vtbl 0x8EAB94、ctor `0x299FE8`、`Layout/common/scrl_bar.arc` の `scrl_bar.bclyt`）。一覧+548。
  - 引数（`SelectBase_SetupStep` 段 2）: 種類 = 一覧+2492（CatalogBase ctor で 2）、行間 = 行0.y − 行1.y、V = 行数 − 1、件数 N（2 回）、コールバック 2 本。
  - `CommonScrollBar_Init 0x299910`: scrl_bar_kind をフレーム = 種類で G_bar/G_triT/G_triB に。R = max(0, N − V + 1)。上 = N_barT_pos_00.y、下 = N_barB_pos_00.y。N_All の表示 = N > V − 1（符号なし）。基準 +1812 = 上 − つまみ高さ × 0.5（`FNMACS` at 0x299B60。デコンパイラは符号を誤って表示する）。
  - `CommonScrollBar_CalcKnob 0x298BA8`: L = 上 − 下、長さ = L / N × (V − 1)（float のビットを 0x3F800000 と符号付き比較し、1 未満は 0）、比率 +1804 = R × 行間 / (L − 長さ)。P_btnC_sh_00 / P_btnC_00 / B_btnC_00 の高さ = 長さ、上下の部品 = 中央 ± 長さ/2。
  - `CommonScrollBar_SetPos 0x2987A8`: 位置を [0,R] に収め N_btn_00.y = 基準 + (−位置 × 行間) / 比率。矢印 `CommonScrollBar_SetArrowNg 0x2980F8`（ng, 0 上 / 1 下）: 位置 0 → 上を無効、R → 下を無効、ほか両方有効。有効旗と同じ向きの要求のときだけ動き、無効 = scrl_bar_ng フレーム 0（flt_298204 = 0.0、灰）、有効へ戻す = フレーム 1（flt_298208 = 1.0）。
  - 置き場所 `CommonScrollBar_AttachTo 0x298018`: スクロールのレイアウトのルートペイン（Layout+0x20）を AppendChild。一覧では `BsMenuCatalog_Init 0x21CB28` が枠 ctlg_list（BsMenuCatalog+0x3E4）の `N_scrl_pos_00` を渡す → 枠と一緒に描かれ、一覧の切り抜きの外。
- 照合（`work/evidence/screens/gamelist_20260925/list_id_v1.png`）: 選択バーの範囲 x 70〜249・y 109〜132 と縦のグラデーションが画素で一致。スクロールバーは件数 175（gohan BuildingEditor の一覧 = 建物 ID 0〜0xFB のうち名前表 0x955700 に名前がある物を code.bin で数えた値。先頭 0x4C も画像と一致）で、**輝度で**平均差 3.68・最大 25。件数を 60〜300 で振ると 160〜200 で最小。Chokistream は JPEG なので細い色の線の色差は比べられない（レール幅全体の平均色は差 3 以内）。選択中の文字色は画像では確かめられない（見た目は青）。
- 反証条件: 別の件数・位置の画面でつまみの長さ／位置が合わない、矢印の灰色が逆に出る、選択バーが文字の手前に出る。
- IDB: 上の関数を命名・注記（`CommonScrollBar_*`、`ButtonActionNode_*`、`ButtonActionControl_*`、`nwlyt_Pane_Prepend/Append/RemoveChild`、`UiAnim_SetFrameToEnd`）。

