---
id: ACNL-F0751
aliases: []
title: "SsysMaLayoutNode_FindPicture 0x567E44: レイアウトからペイン名で Picture を探す"
summary: "0x567E44 は (layout ノード, ペイン名) を取り、ルート pane（+0x20）の vt+0x2C で再帰検索したあと、型情報の親鎖が nw::lyt::Picture の実行時型 0x96F160 と一致する時だけ pane を返す（違えば NULL）。lyt_Object_FindPane 0x7461D0 は型を絞らない別の関数。"
date: 2026-11-11
category: ui
build: acnl_jpn_v15
confidence: MEDIUM         # LOW / MEDIUM / HIGH
tool: IDA
addresses: [0x567E44, 0x96F160, 0x2B8EAC, 0x7461D0]
tags: [layout]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: sonnet-5.5
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

`0x567E44`（`SsysMaLayoutNode_FindPicture`）は `NwLytPicture *(SsysMaLayoutNode *node, const char *name)`。`node+0x20` のルート pane に対し vt+0x2C（FindPaneByName）を `(name, recursive=1)` で呼び、見つかった pane の型情報（vt+8）の親鎖に `0x96F160`（`nw_lyt_Picture_runtimeTypeInfo`）があれば pane を、なければ 0 を返す。つまり `dynamic_cast<Picture*>(FindPane(name))`。型 ID が Picture である根拠は隣接関数と RTTI 名の 2 本の静的根拠、実測なし（MEDIUM）。

gohan の「(layout, name) -> pane」は妥当。ただし名前が見つかっても Picture でなければ NULL になる点を足す。

## 根拠

## 根拠

- 0x567E44（0x58 バイト、先頭 `PUSH {R4-R6,LR}` = 0xE92D4070）の疑似C:
  `r = (*(*(a1+32) + 44))(*(a1+32), a2, 1); if (r) { t = (*(*r + 8))(r); while (t != &dword_96F160) { t = *t; if (!t) return 0; } return r; } return 0;`
- 0x96F160 が Picture の型情報である根拠:
  - 0x73CB34（8 バイトの getter）が 0x96F160 を返す。0x73CB04 `nw_lyt_Picture_GetMaterial`（F0705）・0x73CB40・0x73CB58 の Picture 系メソッド群に隣接する。
  - 0x7917B0（静的初期化、4 命令）が `*0x96F160 = 0x96F15C`（親＝Pane の型情報）を書く。BSS 上の実行時型情報の節。
  - `0x8C9B9C ti_nw_lyt_Picture`（cxxabi 型情報、名前文字列 `N2nw3lyt7PictureE`）が別にあるが、これはコンパイラの RTTI で、0x96F160 は nw ライブラリ自前の実行時型情報。両者の対応は番地の直接の参照では未確認。
  - 呼び元 `ItemIconWidget_SetItem` 0x2B8EAC は戻り値に vt+0x28(0) を呼んで Material を取り、+52 の TexMap を書き換える。Picture の GetMaterial と整合する。
- 呼び元 0x2B9014: `ADR R1,"P_itemIcon"; ADD R0,R4,#0x134 (= widget+308); BL 0x567E44`。ACNL-F0484（アイコンの決まり方）の `P_itemIcon` 探しがこの関数。他に約 40 か所（`sub_197D34` の 7 か所、`sub_216998` の 5 か所など）から呼ばれる。
- 兄弟（同形、型 ID だけ違う）: 0x567EA0 は `0x96F164`（getter 0x73CF24、`nwlyt_TextBox_GetVtxColorElement` 0x73CF30 の隣で TextBox の疑い）、0x567EFC は `0x96F14C`（getter 0x73CFEC、クラス未確定）。いずれも名前は付けていない。
- `lyt_Object_FindPane` 0x7461D0 との違い:
  - 0x7461D0 は `lyt::Object` の `+0x48` のルート pane に vt+0x2C(name, 1) を呼ぶだけで、型の絞り込みがない。呼び元は BsSkb 系の 4 件。
  - 0x567E44 は `+0x20`（別クラスのレイアウトノード）で同じ vt+0x2C を呼び、さらに Picture 型で絞る。
  - 同じ「ルート pane の vt+0x2C(name, 1)」を使うので、ルート pane の探し方は同じ。クラスが違うので同一視はしない。

## 反証条件・未確認点

- Picture の vtable（`vtbl_nw_lyt_Picture` 0x8FBFFC）の slot 2（+8）が 0x73CB34 を指していなければ、0x96F160 = Picture は誤り（隣接関数からの推定のため。vtable の中身は読めず未確認）。
- ルート pane の vt+0x2C がペイン名の検索（FindPaneByName）であることは、引数 `(name, 1)` と使われ方からの推定で、実体の関数は追っていない。
- `node` の実クラス名（`SsysMaLayoutNode` は既存の前方宣言を借りた）は確定していない。
- 動的に実測していない。
