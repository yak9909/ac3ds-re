---
id: ACNL-F0593
aliases:
- IDA-opus-5.5-F077
title: 'カタログを開くときの遷移は BsMenuBg の切り替え（クロスフェード）と画面自身の in アニメ。Fade / Wipe / Fader は使わない（2026-10-05、HIGH: 静的 + 実機の否定観測）'
summary: '解析ソフト IDA（idalib-mcp / ida-pro-mcp）、解析モデル opus-5.5。段階 2（上画面と遷移）の下調べ。**既存資料**: 旧 RE/FINDINGS.md F-50（Wipe、UiAnim のレート）/ F-51（Fade・Fader 9 個と Fader_SetKind の種類）、'
date: '2026-10-05'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 6900104
- 6897504
- 9738008
- 6898908
- 2210380
- 5410392
- 5410724
- 5416252
- 5416584
- 5658756
- 5658808
- 6967600
- 6899692
- 6897384
- 6898092
- 5412072
tags:
- catalog
supersedes: []
source: IDA:work/FINDINGS.md:4501-4517
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F077: カタログを開くときの遷移は BsMenuBg の切り替え（クロスフェード）と画面自身の in アニメ。Fade / Wipe / Fader は使わない（2026-10-05、HIGH: 静的 + 実機の否定観測）

解析ソフト IDA（idalib-mcp / ida-pro-mcp）、解析モデル opus-5.5。段階 2（上画面と遷移）の下調べ。**既存資料**: 旧 RE/FINDINGS.md F-50（Wipe、UiAnim のレート）/ F-51（Fade・Fader 9 個と Fader_SetKind の種類）、
旧 DOCS/menu_system.md（BsMenuCatalog の開始・終了、`BsMenuBg_RequestKind(manager+476, 1, 0)` / `(bg, 0, 6)`）、旧 DOCS/catalog_outdoor.md（`Menu_RequestOpen(124, 0)`、ctlg_book / ctlg_list / ctlg_T）。
**最初にこれらを確かめずに実機の BP を張った（利用者の指摘）。**

- `BsMenuBg_RequestKind 0x694988`(bg, 種類, アニメ): +1553 = 種類、+1560 = アニメ番号、状態を `BsMenuBg_ChangeCalc 0x693F60`（命名）へ。ChangeCalc は change アニメ（+1504）を
  終わるまで進め、+1554 = 種類で確定して待機へ。bg = `g_BsMenuBg 0x949718`（命名。`BsMenuBg_InitStep 0x6944DC` が入れる）= BsMenuMgr+476。
- 見た目: `Layout/Menu/mvmnt_undscrn.arc` の `mvmnt_undscrn_change.bclan` = P_base_00 / P_base_01 の不透明度（CLVC 16）を **0→255 の 5 フレーム**で上げる
  = 新しい種類の背景が重なって現れる**クロスフェード**。`mvmnt_undscrn_kind.bclan` が種類ごとの背景の絵（11 枚: my_mvm_check / design / dic / dream / friend / island / key / manp / pspo / ruck / tool）。
  loop はテクスチャ SRT を 125 フレームで流す。（designer の extract で bclan を読んだ。）
- カタログは開くとき `(1, 0)`（sub_21A794）、閉じるとき `(0, 6)`（sub_21C1B0、BsMenuCatalog_ListLeaveCalc 0x21BA4C）。ほかに ctlg_book / ctlg_list / ctlg_T の in / out アニメ（sub_21AC6C が読む）。
- **上画面**: ctlg_T（400x240）は品名・値段の札だけで、全面の背景を持たない。上画面を覆っているのは 3D のプレビュー（Catalog カメラ、旧 catalog_outdoor.md）。
- 実機の否定観測（2026-10-05）: Fade IN/OUT の enter（0x528E58 / 0x528FA4）、Wipe IN/OUT（0x52A53C / 0x52A688）、FaderBase_StartFadeOut/In（0x565884 / 0x5658B8）、
  Fader_StartFade（0x6A5130）に BP を張って利用者がカタログを開いた → どれも止まらない。静的の結論（Fade / Wipe / Fader はカタログの遷移ではない）と整合。
- IDB: BsMenuBg_ChangeCalc / BsMenuBg_InitStep / BsMenuBg_ResetPanels（0x6947EC）/ BsMenuBg_StartLeave（0x693EE8）/ BsMenuBg_LeaveCalc（0x6941AC）/ Fade_Reset（0x5294E8）/ g_BsMenuBg を命名。

