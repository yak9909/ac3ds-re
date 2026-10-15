---
id: ACNL-F0460
aliases:
- IDA-opus-5.5-F036
title: 'ゲーム共通の 8 行リスト InstSelect<8> を下画面だけ借りる部品の作り（2026-09-25、MEDIUM: 静的＋実機の欄の読み取り。描画は未試験）'
summary: '公共事業のリストは `PWorkList : InstSelect<8> : SelectBase : CatalogBase`（RTTI）。`InstSelect<8>`（vtbl `0x8E54B4`、ctor `sub_7C6EB0`、4,812 B）は派生 10 種が共有する**ゲーム共通の 8 行リスト**で、純粋仮想は vt[13]（一覧を作る・件数 +2500）と vt[25]（i 行目の語）だけ。'
date: '2026-09-25'
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9327796
- 9455900
- 8864520
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:1336-1346
by: opus-5.5
original_by: ''
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F036: ゲーム共通の 8 行リスト InstSelect<8> を下画面だけ借りる部品の作り（2026-09-25、MEDIUM: 静的＋実機の欄の読み取り。描画は未試験）

公共事業のリストは `PWorkList : InstSelect<8> : SelectBase : CatalogBase`（RTTI）。`InstSelect<8>`（vtbl `0x8E54B4`、ctor `sub_7C6EB0`、4,812 B）は派生 10 種が共有する**ゲーム共通の 8 行リスト**で、純粋仮想は vt[13]（一覧を作る・件数 +2500）と vt[25]（i 行目の語）だけ。
行の文字は `vc_ACMESSAGEBOX_FUNC2` が `word->vt[3]()` の UTF-16 を流すだけなので、`script::WordPtr {0x0090491C, 文字列, 容量}` で任意の文字列を出せる。
枠 `ctlg_list` と「やめる/けってい」（`common/btn_pos.arc`）・上画面 `ctlg_T` は `BsMenuCatalog` 側の持ち物で、**枠と一覧だけ自前で組めばボタンと上画面は出ない**。
アニメは UiAnim（40 B）: 結合 `sub_4B8ECC` / フレーム `sub_568C00`（VFP s0、任意位置）/ 進める `UiAnim_Step`＋`vc_ACSYSTEM_DATA2` / 終了 `UiAnim_IsFinished` / 解除 `sub_568840`。
状態機械は `sub_8163C0`（表 `0x874308`: 何もしない・入場処理・退場処理・待機処理・リストフェードアウト）。入力は `ButtonActionControl`（+2560）で、+212 bit0＋(+180) が「決定」、bit3 が入力止め。十字はメニュー管理 `BsMenuMgr`（`off_949D4C`）と手カーソルを使う（メニュー外は未検証）。
実機（カタログ表示中）: nw::lyt ヒープの空き 1,456,124 B、Layout のコマンドリスト用 FCRAM ヒープの空き 865,080 B。PWorkList の欄（件数 95・in アニメ 総 11 など）と BsMenuCatalog +15264=6（kind フレーム 2.0）を読んで静的な欄の意味と照合した。
反証条件: 枠・一覧をメニュー外で組むと落ちる／描画フェーズ後の AddLayout が下画面に出ない／+2500 以外に件数を読む経路がある。
詳細・関数表・設計: docs/topics/game_list.md。

