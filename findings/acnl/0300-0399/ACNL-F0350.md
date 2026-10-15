---
id: ACNL-F0350
aliases:
- F-324
title: 'F-324（2026-09-07）: リストボックスの背景が後ろの行文字より後ろだった'
summary: '**confidence: MEDIUM**（静的根拠 + 検証器 + プレビュー + ビルド。**実機の目視は未確認**）'
date: '2026-09-07'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 7589704
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:21395-21439
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-324（2026-09-07）: リストボックスの背景が後ろの行文字より後ろだった

**confidence: MEDIUM**（静的根拠 + 検証器 + プレビュー + ビルド。**実機の目視は未確認**）

利用者の報告:「変更ダイアログは問題ないが、リストボックスの背景パネルの
透明度が後ろのチートメニューに反映されず、後ろのテキストの色が背景色の
影響を受けない」。Chokistream の画での指摘（こちらから直接は見られない）。

### 原因

`GuiV2::Commit()` が子リストを **Picture 全部→文字全部** の順に繋いでいた
（`GuiV2.cpp` の「文字（★必ず最後）」）。全 Picture が全 TextBox より
後ろになるので、後から開くリストボックスの背景 Picture が、
先に描いたメニュー行の文字 TextBox より後ろになり、行文字が背景の上に
そのまま乗って突き抜けた。背景の半透明が後ろの文字に効かないのはこのため。

ダイアログ・説明パネルが無事だったのは、表示位置（x=168〜、メニューの右）が
行文字と重ならないため。重なるのはメニュー行域に出るインラインリストだけ。
`preview_menu.py`（Canvas 即時描画＝呼び順通り）は正しく見えていたので、
プレビューと実機の食い違いでもあった。

### 直し

`ScreenState` に表示リスト（`oKind` / `oIdx` / `oCount`）を持ち、
`FillRect` / `DrawText` を呼んだ順に `LinkRing()` へ繋ぐ。
スロット割り当て（best-fit decreasing）は順序と無関係なので先に決め、
繋ぐときだけ順序に従う。安全弁で切り捨てた分は飛ばす。

混在させても前後関係は保たれる。TextBox の `DrawSelf 0x73CF48` は
Picture の溜まりを流してから自分のコマンドを書く設計で、ゲーム自身の
会話 Layout も `P_*` と `T_*` を混在させている（F-147）。
基準仕様 v2 §2.6 の「子リストの最後に置く」を呼び順へ改めた。

### 検証

`verify_plugin_port_v2.py` 8 群 0 件、`verify_spec_v2.py` 8 群 0 件、
`preview_menu.py --sel 3` 出力、`gohan.3gx` 再ビルド済み。
ケーブ不変なので `audit_node_cave.py` の対象外。

### 実機で確かめること

リストボックスを開いたとき、後ろの行文字が背景の下に沈み、
背景色を通した見え方になること。ダイアログ・説明・選択帯・スクロールバーに
退行が無いこと。

