---
id: ACNL-F0491
aliases:
- IDA-opus-5.5-F042
title: '共通ボタン（cmn_btn / btn_pos）・時計とベルの箱（time_bel_win）の組み立てと状態の規則（2026-09-25、HIGH: 静的＋実機画像 2 枚）'
summary: 設計ツール `src/acnl-ui-designer`（ef9b19c）の `cmnbutton.mjs` / `timebel.mjs` の根拠。表は同リポジトリ `docs/verification.md`。
date: '2026-09-25'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 3018936
- 9361768
- 7469580
- 3017236
- 5668344
- 2278300
- 2526720
- 3016952
- 2278716
- 2277756
- 9746020
- 2847016
- 2847300
- 2846516
- 3017124
- 4941284
- 4960364
- 4958304
- 4956148
- 2701768
tags:
- button
supersedes: []
source: IDA:work/FINDINGS.md:2078-2092
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F042: 共通ボタン（cmn_btn / btn_pos）・時計とベルの箱（time_bel_win）の組み立てと状態の規則（2026-09-25、HIGH: 静的＋実機画像 2 枚）

設計ツール `src/acnl-ui-designer`（ef9b19c）の `cmnbutton.mjs` / `timebel.mjs` の根拠。表は同リポジトリ `docs/verification.md`。

- 共通ボタン = RTTI `CommonButtonSingle`（1,304 B、`ButtonActionNode` の派生。dtor `0x2E10B8`、vtbl 0x8ED968。上書きは vt[4] と vt[14] = 決定音 `CommonButtonSingle_PlayDecideSound 0x71FA0C` だけ）。
  - `CommonButtonSingle_Init 0x2E0A14`: cmn_btn.bclyt（+1302 が立つと cmn_btn_back.bclyt）、ノードのペイン B_btn_A・グループ G_btn、N_all の平行移動を 0 に。in をフレーム 0 で当てたあと out を最終フレームで当てる → **作った直後は非表示**（N_all の CLVI 0、縮小 0.8）。`sub_5D3A28`（地域 byte_951234 と言語 byte_951235 から。日本 = 0）が 0 なら T_btn / S_btn を使い G_txt_01 を隠す（`Layout_SetGroupVisible 0x567DF8`）、0 以外なら T_btn_W / S_btn_W。文字は T と影 S の両方（vc_ACMESSAGEBOX_FUNC1）。
  - 置き場所: `ComButton2Lyt_Init 0x22C39C` は btn_pos.bclyt を組み、ボタン 0 → N_cmnbtn_pos_L、1 → _R（`ComButtonCtrl_Attach2 0x268E00` → `CommonButtonSingle_AttachTo 0x2E08F8` = ルートペインを AppendChild）。`ComButton3Lyt_Init 0x22C53C` は L/C/R。`ComButton1Lyt_Init 0x22C17C`（クラスは vtable の隣接から、MEDIUM）は引数で表 0x94B664 = L/C/R の 1 つ。
  - 状態（基底 ButtonActionNode のまま）: 選択 vt+32 `0x2B7128` = select を最終フレーム／フレーム 0、押下 vt+28 `ButtonActionNode_SetTouch 0x2B7244` = touch と select を最終フレーム／0、決定 vt+36 `StartDecide 0x2B6F34` = touch_ok・select_ok を結合して再生（9 フレーム）＋決定音。無効 `CommonButtonSingle_SetNg 0x2E09A4` = cmn_btn_ng をレイアウト全体にフレーム 0（灰、flt_2E0A10 = 0.0）、戻すときは最終フレーム。有効旗 +217 = !ng。状態が変わるときだけ動く。
- TextBox の CLVC（**第 1〜2 段の描画器は読み捨てていた**）: `nwlyt_Pane_SetColorElement 0x4B65E4` = 16 はペインの α（+180）、ほかは vt+32。TextBox `0x4BB06C` = `+216 + 4×(番号>>3) + (番号&3)` → 0〜7 は文字の上の色、8〜15 は下の色。Picture `0x4BA860` / Window `0x4B9FF4` は 番号>>2 = 角（今の実装どおり）。
- 時計 `BsTimeBelWindow_Init 0x2939C8`（日本: sub_5D3A28 = 0、sub_3013F4 = 0）: 左の日付 = T_month、右 = T_day。T_Ger_month / T_Ger_slsh_00 / _01 を隠す。T_slsh = SYS_2D_UI 227。N_time_set / N_ampm_set はレイアウトの位置のまま（他地域は N_time_pos_xx / N_ampm_pos_00 へ移す）。時刻 `BsTimeBelWindow_UpdateClockTexts 0x291D88`: AM/PM = 0x94A734（"AM" / "PM"、時 ≥ 12）を T/S_time_ampm_00、時 = 時 % 12 を 2 桁で T/S_time_00（`0x2932B8` → `0x291ED0`。第 5 引数の S はスタック渡しでデコンパイラが落とす）、分 2 桁を T/S_minute_00。コロンは α 255 / 0 で点滅（`0x2932E8`）。
- ベルの箱 `BellBox_Init 0x1AD804`（BsTimeBelWindow +2916）: in / out / clr_mdl と T_bell_00・G_bell_00。`BellBox_SetKind 0x1AD9A8`: 種類 0・1 → clr_mdl フレーム 0（ベル）、2 → 1、3 → 2、4 → 3。値は種類ごとの出どころから取り、`BellBox_UpdateText 0x1AD8FC` で 9,999,999 までに収めて書く（種類 0・1 は sub_5F5ECC、ほかは sub_5F6238）。種類ごとの意味（財布・貯金など）は未確認。
- 照合: 時計 `scenes/clock_after_cmd2.json`（9/25 金 AM 04:59）と `work/evidence/screens/gamelist_20260925/after_cmd2.png` の上画面。ずらし ±4px で差が最小は (0, 0)、箱の上の 4,330 画素で輝度の平均差 8.05、差 > 24 は 4.8%（JPEG と後ろの 3D）。共通ボタンとベルの箱は `pw_list_buttons_1823.png`（ゲーム本来の公共事業の一覧、利用者のキャプチャ）で照合: 両方ともずれ (0, 0)、「やめる」= 通常・「けってい」= ng フレーム 0 の見た目が一致。**日本版のベルの数はカンマ無し**（「185610」。レイアウトの既定は「8,888,888」）。
- 反証条件: 実機のボタンで灰色・選択色が逆に出る、ボタンが別の位置に出る、日本以外の設定で時計が組み替わらない。
- IDB: 上の関数を命名・注記。

