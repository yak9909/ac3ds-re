---
id: ACNL-F0393
aliases:
- F-366
title: 'F-366（2026-09-08）: しずえスキップをトグル式チートとして取込'
summary: '`DOCS/skip_isabelle.md`（F-361。実機で成功済み）を常設化。'
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5555236
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:23908-23943
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-366（2026-09-08）: しずえスキップをトグル式チートとして取込

`DOCS/skip_isabelle.md`（F-361。実機で成功済み）を常設化。
関連: `HANDOFF_MESSAGE.md` §5（飛ばすものの実害評価）。

### 実装

- 木： ルートにチェック `しずえスキップ`（セーブ実行の次）。
  説明文に一括処理スキップと成長未検証を明記。
  Simulator の木にも同文で追加（検証器の文字列照合のため）。
  使う字 14 字（会備処影成未村検準理証話長響）は美咲表になかったので
  BDF（7x7 を確認）から `extract_misaki_gothic_2nd_8.py` で追加し、
  `make_font_ui.py` でアトラス再生成。美咲 362→377、総字形 390→405。
- 発火： `Sources/ShizueSkip.cpp`（新規）。`Framework_ProcOneFrame`
  `0x0054C424` の入口に CTRPF の `Hook` を 1 本（F-361 §6 の処方どおり。
  先頭は `PUSH {R4-R6,LR}` を `code_runtime.bin` で確認済み。
  素（`0xE92D4070`）でなければ掛けない）。
  毎フレーム： 部屋 `!= 0x63` → fired 解除。未アーム・発火済みは帰る。
  それ以外はケーブと同手順（ガード→番号→遷移）＋通知
  （題「しずえスキップ」／「村へ移動しました」）。
- 引数はケーブの実測ビットそのまま（R0=mgr, R1=idx, R2=1, R3=0,
  スタック 1, 1）。資料の「1.0f」表記とビットが違うが、動いたのは
  ケーブ側なので原型は int 6 個で宣言し、コンパイラの float ABI に
  左右されないようにした。
- ライフサイクル： チートON（`OwnGuiToggle`）で `GuiMenu::Initialize()`
  のあとに設置（失敗しても GUI は続ける）。OFF（`Disable()`）で
  `RemoveHooks()` と同じ場所で外し、後続の 100ms 待ちに含める。
- case 0（一括処理）は飛ばす。`sub_30C994` の呼出規約が未確定なので
  盲目的には呼ばない。日付またぎの成長比較は HANDOFF_MESSAGE.md §7-3
  の実機作業として残る。

confidence: MEDIUM（検証器 2 種 0 件 + ビルド + プレビュー。
フック点・手順は F-361 の実機成功と同一。**本構成の実機は未確認**）。
実機で見ること： チートON→タイトルで選択→しずえ画面で放置→村へ出るか。
通知が出るか。部屋 0x63 以外・チートOFF で何も起きないこと。

