---
id: ACNL-F0763
aliases: []
title: "TextWriter のデストラクタ 0x4D5BCC は何も解放しない"
summary: "0x4D5BCCはTextWriterの使用終了時に呼ばれる空のデストラクタであり、フォントや文字バッチを解放しない。"
date: 2026-11-11
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0x4d5bcc]
tags: ["font", "layout"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6.1-sol
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

0x4D5BCCはTextWriterの使用終了時に呼ばれる空のデストラクタであり、フォントや文字バッチを解放しない。

確度MEDIUM。実測なし。各項目について命令列と、独立した呼び元・生成元・消費側またはvtable実データを照合した。

| 番地 | 付けた名前 | 型・プロトタイプ |
|---|---|---|
| `0x004D5BCC` | `nwfont_TextWriter_Dtor` | `void f(void *writer);` |

## 根拠

- ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名はsymbolsを併読。原本code.binのSHA256はbuild台帳と一致。命令列は `tools/codebytes.py` の読取関数とCapstoneで独立照合した（`_local/evidence/146/original_asm.txt`）。型・vtable・表の原本値は同所 `bytes.json` と追加検算。作業用IDBで実測はしていない。
- 対象 `0x4D5BCC` の原本は `NOP; BX LR` の2命令。thisを読まず、メモリ書き込みも解放呼び出しも無い。
- 呼び元 `ChoiceStandardItem_MeasureText 0x5E9430` はSP上にTextWriterを構築、文字箱からfont/size/spacingを移し、CalcStringWidth後に0x5E94C4でこの関数を呼ぶ。
- 独立した `TextBox_RebuildBatchWriter 0x4BAFB0` と `nwlyt_TextBox_DrawText 0x4BB1E8` も同じTextWriter_Ctor0x7E8488と対にし、末尾でローカルwriterをR0へ渡して呼ぶ。したがって一般的な関数名不明のnoopではなくTextWriter寿命終了点と識別できる。
- 旧版 `DecorLayout.cpp:69` と既存ACNL-F0480（S）のdtor注記は正しい。ただし空のデストラクタなので、所有フォント/描画器の後始末まで含むと解釈してはならない。
- writerの完全構造体はsymbolsに無いため引数はvoid*。空関数の自動推定で引数無しとなる疑似Cを採用せず、ARM呼び元からthisを補った。

- 参考資料は依頼指定の旧版gohan（`_local/legacy-src/gohan-legacy/Sources`、出所は依頼文、台帳の既存キー無し）。未検証の手がかりとして用途を対比し、上記一次証拠を根拠とする。旧版本文を証拠の代わりにしない。

## 反証条件・未確認点

- SDK公開ヘッダとの照合や実機の寿命監視はしていない。空の処理から他の所有物の寿命を導かない。
- 上記生産/消費の値やvtableが別オブジェクト・別型を指すと判明した場合は再検討する。新しい実機確認やゲーム挙動の保証は含めない。
