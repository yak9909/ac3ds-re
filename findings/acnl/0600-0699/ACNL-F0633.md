---
id: ACNL-F0633
aliases:
- IDA-gpt-6.1-sol-F007
title: '改造テントの壁紙/床・自由スクロール・すぐ開く・すぐチップ・位置保持（2026-10-08、MEDIUM: 静的。実機未確認）'
summary: '解析: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix4）。照合・commit・採番は親（sonnet-5.5）。根拠 **work/evidence/t022_catalog_fix4/report.md**。gohan 0db52e0（work/decor-catalog）。'
date: '2026-10-08'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5978548
- 2970324
- 2971432
- 3131512
- 7672352
- 9754184
- 9754180
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:5003-5016
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0438"]
---
## IDA-gpt-6.1-sol-F007: 改造テントの壁紙/床・自由スクロール・すぐ開く・すぐチップ・位置保持（2026-10-08、MEDIUM: 静的。実機未確認）

解析: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix4）。照合・commit・採番は親（sonnet-5.5）。根拠 **work/evidence/t022_catalog_fix4/report.md**。gohan 0db52e0（work/decor-catalog）。
- 壁紙・床（改造テント）: 家の外観 +0x4 = 0 だと 0x5B39B4 が拒否（F005）。メニューに「改造テントのかべ・ゆか」（既定 OFF）を追加。ON のとき、通常許可が偽で、自分の家（室フラグ 0x80・室所有者が本人）・外観 0・通信相手なしを確かめてから下位 setter RoomData_SetWallpaper 0x2D52D4 / RoomData_SetFlooring 0x2D5728 を呼ぶ。
  下位 setter は保存部屋データ +0x2F2 / +0x2F6 に Item_Copy（親が命令で照合: ADD R0,#0x200; ADD R0,#0xF2/#0xF6; B 0x2FC878。F106 の +754 / +758 と一致）。壁の variant +0x20 / 床 +0x21 を 0、音 0x100094E / 0x100094F。通信片 0x78 / 0x79 は送らない。
  **ゲーム本来との差**: 通常のテントの家でも貼り替えられる（改造と通常を保存値から区別できない）。利用者の依頼に基づく明示的な例外で、既定は OFF（本来の判定）。
- 自由スクロール: DecorSlider に SetupFree / RestorePosition（ページに吸着せず任意の位置で止まる、慣性、端でクランプ、L/R 残す）。アイコンの 45 枠は据え置き。HHD のページ吸着は Setup として残し、HHD の写しの検査（600 シナリオ）は不変。自由送りは別の検査（180 シナリオ）。
- すぐ開く: 上段タブの決定から s_pend による拒否を除去、Closing からも操作可、同じ main の窓は保持して再利用。家具決定時は窓を即非表示にして入力を返す。
- すぐチップ: 資源旗 +0x66 bit1（Finalize 済み）・破棄要求なし・対応する生きた記録・層 0 / 親なし・未使用枠で追加（状態 2 / 2 フレームの待ちは除去）。初回座標は AcFtr_BuildAnchorWorldMatrix 0x751220(actor, actor+0x548, 0, &u16 0, 0) で確定してから Chip_Setup → Chip_RestoreOwnRoot 0xB2F77C。親が 0x751220 の入口語 0xE92D43F0 を照合。配置演出中のドラッグはゲーム側の操作状態 +0x7FD が 0 / 2 なら通る（静的、実動作は未測定）。
- 位置保持: main ごとに tab / kind / 位置を BeginClose で保存し、開き直しで復元。模様替えを閉じると初期化。
- 周辺訂正: [0x94D648] は NetGameMgr 本体でなく SingletonDisposer へのポインタ（本体は [0x94D644]）。HhdScreen.cpp の既存の判定は未変更（別件）。
- IDB: 本体にコメント・命名、ModuleIndoor にコメント（ID は親が F007 に置換: 本体 6+1、Indoor 4+1）。
- 追記（2026-10-08 実機 decor_catalog8）: 5 項目 PASS。しばらく使うとフリーズ／クラッシュ → F008。

