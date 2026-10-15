---
id: ACNL-F0394
aliases:
- F-367
title: 'F-367（2026-09-08）: しずえスキップ取込後のクラッシュ切り分け（静的監査まで）'
summary: 利用者の報告： 新しい 3gx（F-366 取込版）でクラッシュした。
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 5555236
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:23944-23978
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-367（2026-09-08）: しずえスキップ取込後のクラッシュ切り分け（静的監査まで）

利用者の報告： 新しい 3gx（F-366 取込版）でクラッシュした。
IDA の PC は未受領（デバッガに触れる手段が当セッションに無いため、
PC・LR・発生場面の申告待ち）。以下は実機なしの静的監査の結果。

### 潰した候補（安全を確認）

- CTRPF `Hook` のレジスタ保存： `libctrpf.a` の `HookManager.o` を
  逆アセンブルし、生成ラッパが `PUSH {R0-R3,R12,LR}`／`POP` で
  呼び出し側保存分を復元することを確認。R4-R11 は C++ の ABI 契約で
  コールバック側が保存する。VFP はコールバックが触らない
 （整数処理のみ。`snprintf` も `%s` だけ）。
- フック点 `0x0054C424` の先頭は `PUSH {R4-R6,LR}`（`code_runtime.bin`
  で確認）。OI_BEFORE_CB の再配置に適合。素でなければ掛けない検査付き。
- 呼出規約： ケーブ（実機成功済み）と語単位で一致。
  R0=mgr, R1=idx, R2=1, R3=0, スタック 1, 1。原型は int 6 個。
- 発火条件： 部屋 `!= 0x63` 即帰り／未アーム即帰り／発火済み即帰り。
  ガード NULL・番号範囲外も帰る（ケーブと同一）。
- フォント： CMAP 対はソート済み（`make_font_ui.py` が整列＋自己検査）。
  アトラス同寸・CWDH/CMAP は検証器群 2・3 で一致。
- メニュー判定： `g_fxMenuJudge` は全 false のまま（誰も送らない）なので
  `ApplyItem()` の経路は従来と同一。`FireHotkeyItem()` は束縛一致時のみ。

### 残る仮説（PC が要る）

- H1: 既知クラッシュの再発。PC `0x070058A0` 付近＝F-320（ready 直後 ON）、
  PC `0551C928`＝TODO-133。PC 照合で即切り分け。
- H2: 発火先の状態が想定外（部屋 0x63 に別経路で入った等）。
  PC が `sub_309F18`/`Room_UseExit` 内ならこちら。
- H3: 取込と無関係（フォント・木・他作業）。切り分け手順：
  (a) チートON＋しずえ項目OFF で遊ぶ→落ちれば発火は無罪、
  (b) メニューを開くだけ→落ちれば描画・フォント側、
  (c) しずえ画面＋項目ON で放置→落ち方を見る。

