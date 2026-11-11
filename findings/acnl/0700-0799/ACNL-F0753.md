---
id: ACNL-F0753
aliases: []
title: "時計の大域変数は BsTimeBelWindow 本体を指し、時計ペインはその +1760 にある"
summary: "0x94A720 は BsTimeBelWindow 本体へのポインタであり、時計ペインを直接指す変数ではない。"
date: 2026-11-11
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0x94a720]
tags: ["layout"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: auto
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

0x94A720 は BsTimeBelWindow 本体へのポインタであり、時計ペインを直接指す変数ではない。

確度MEDIUM。実測なし。各項目について命令列と、独立した呼び元・生成元・消費側またはvtable実データを照合した。

| 番地 | 付けた名前 | 型・プロトタイプ |
|---|---|---|
| `0x0094A720` | `g_BsTimeBelWindow` | `void *` |

## 根拠

- ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名はsymbolsを併読。原本code.binのSHA256はbuild台帳と一致。命令列は `tools/codebytes.py` の読取関数とCapstoneで独立照合した（`_local/evidence/146/original_asm.txt`）。型・vtable・表の原本値は同所 `bytes.json` と追加検算。作業用IDBで実測はしていない。
- `BsTimeBelWindow_Init 0x2939C8` はtime_bel_win.bclytを組み、`FindPane(layout+108,"N_time")` の結果を this+1760 に保存する。そのペインの+183 bit0を落とす。
- 同関数の末尾は `off_94A720=this`。画面の状態名も `"BsTimeBelWindow"` に設定するため、レイアウトの名前だけに依存しない識別である。
- 生産側（thisの公開）と利用側（N_timeの保存）を独立に確認。完全構造体はsymbolsに無いため大域変数の型は `void *`。
- 旧版 `GameLabel.cpp:115` の説明と一致。+1760はペインポインタの格納欄であり、インラインPaneではない。

- 参考資料は依頼指定の旧版gohan（`_local/legacy-src/gohan-legacy/Sources`、出所は依頼文、台帳の既存キー無し）。未検証の手がかりとして用途を対比し、上記一次証拠を根拠とする。旧版本文を証拠の代わりにしない。

## 反証条件・未確認点

- ウィンドウとペインの寿命、画面切替中の非NULL保証は未確認。
- 上記生産/消費の値やvtableが別オブジェクト・別型を指すと判明した場合は再検討する。新しい実機確認やゲーム挙動の保証は含めない。
