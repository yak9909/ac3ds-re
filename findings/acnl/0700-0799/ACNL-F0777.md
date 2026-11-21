---
id: ACNL-F0777
aliases: []
title: "メッセージ管理体ポインタ vc_DATAPOINTER の型"
summary: "vc_DATAPOINTER はメッセージ管理体の先頭を保持する4バイトのポインタであり、公開する型は void * とする。vc_NPC_2_SETUP の message_data へ値を読み出して渡す。"
date: 2026-11-21
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: export ARM
addresses: [0x00957ED4]
tags: []
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: auto
original_by: ""
reviewed_by: []
state: active
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

0x00957ED4 の既存名 vc_DATAPOINTER に `void *` を付ける。
格納先そのものを指す `void **` ではなく、格納されている値の型である。
呼出側の値の受渡しと、独立した破棄側の内部欄へのアクセスが一致するため MEDIUM。
実機検証は行っていない。

## 根拠

- `sub_10A0E8` の 0x0010A110 は `LDR R0, =vc_DATAPOINTER`、
  0x0010A116 は `LDR R0, [R0]`、0x0010A118 は `BLX j_vc_NPC_2_SETUP`。
  R1 は WordFix のスタック先頭、R2 は STR_Fobj_name、R3 は行番号。
  [ACNL-F0766]（事前照会時の格付け A）の第1引数 `void *message_data` と一致する。
- `sub_12DAD4` の 0x0012DBD4 は大域の値を R4 へロードし、
  0x0012DBE0–0x0012DBF4 で R4+0x14/R4+0x30 由来の内部オブジェクトを破棄する。
  0x0012DC18 で同じ値を R0 に読み、0x0012DC24 で +0x14 を解体し、
  0x0012DC34 で先頭を解放する。0x0012DC38 は大域へゼロを書き戻す。
- `xrefs.tsv` の同番地の参照群と全関数書き出しを照合した。
  全文検索の保存先は `_local/evidence/162/datapointer-rg.txt`。
  旧名の外部作者の注記だけを根拠にはしていない。

## 反証条件・未確認点

管理体の実名と全メンバーは未定義。MSBT本体のバイト列を直接指す型や
WordFix38専用の型にはしていない。ランタイムの寿命・排他・全ロード経路は未実測。
