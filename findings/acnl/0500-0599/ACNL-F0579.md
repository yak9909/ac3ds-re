---
id: ACNL-F0579
aliases:
- IDA-unknown-F004
- V2-F004
title: gohan-gui-simulator のローカル版と公開版が双方向に食い違っていた（解消済み）
summary: '`src/CTRPF-GUI-Simulator`（ローカル）を削除し `yak9909/gohan-gui-simulator` の clone へ統一した際に判明。'
date: '2026-09-12'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4334-4356
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F004: gohan-gui-simulator のローカル版と公開版が双方向に食い違っていた（解消済み）

`src/CTRPF-GUI-Simulator`（ローカル）を削除し `yak9909/gohan-gui-simulator` の clone へ統一した際に判明。
**ローカルと公開版は一方向に古いのではなく、双方向に食い違っていた。**

- 公開版が新しい部分: `ui-model.js` は 1,178 行（旧ローカル 1,124 行。+78 / -24 行）、`app.js` は 698 行（旧 592 行。+165 / -59 行）。
- **公開版に無い部分**: 2026-09-12 のチャット漢字候補UI。旧ローカルだけが持っていた。
  - 文字列 8 種（`チャット漢字候補` / `チャットの入力から漢字候補を取得し下画面に表示します。` / `変換中です。Bで閉じる` / `漢字候補` / `変換処理中です。` / `チャットに文字を入力してください。` / `普通のチャットを開いてください。` / `入力文字を確認してください。`）
  - 色 2 件（`#79d9a7` = `kColCrumb`、`#4f6c5b` = `kColPanelEdge`）
- 影響: `tools/patches/verify_plugin_port_v2.py` の群5「GuiMenu.cpp が gohan-gui-simulator と一致するか」で
  **総異常 3 件 → NG**。ほかの群と `verify_keyboard_port`（10,943 遷移）・`export_keyboard_layout --check` は PASS。
- **`ui-model.js` 側の差は結果に影響しない**ことを確認済み。新旧どちらから生成しても
  `GuiKeyboardLayout.h` はバイト一致で、キーボードの差分試験も PASS。
- **解消（2026-09-13）**: 利用者の判断で**ローカル版を優先**。解析Git `82adf284` の 29 ファイルを
  `src/gohan-gui-simulator` へ戻し、`4083d70` として push した（**履歴は保持**。公開版の新機能は
  `c0251cd` 以前から参照でき、後日こちらで実装し直す）。
  `verify_plugin_port_v2` の群5 を含め `tools/chat_kanji/verify.py` は **Prebuild PASS**。
- 付随して: `index.html` が `ui-model.js` / `app.js` を直接読む構成に戻ったので `web/` の分割塊は消えた。
  Pages のワークフローは repo 直下をそのまま配信するので `.github/workflows/pages.yml` と `.nojekyll` は残した。
  `core.autocrlf=true` の環境で改行が書き換わらないよう `.gitattributes`（`* -text`）を追加し、
  staged blob が `82adf284` と **29/29 バイト一致**することを確認した。
- 根拠: `work/evidence/rename_sync/rename_20260913.json`、`work/logs/chat_kanji_verify_after_rename.log`。

