---
id: ACNL-F0757
aliases: []
title: "メニュー要求状態と登録画面リストの先頭は別で、状態3は作成中を表す"
summary: "0x949D1Eは要求処理のu8状態、0x986500は登録画面ノードの先頭ポインタ。画面登録時に状態3から1へ戻るため、1だけでは画面が無いとは判定できない。"
date: 2026-11-11
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0x949d1e, 0x986500]
tags: ["menu"]
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

0x949D1Eは要求処理のu8状態、0x986500は登録画面ノードの先頭ポインタ。画面登録時に状態3から1へ戻るため、1だけでは画面が無いとは判定できない。

確度MEDIUM。実測なし。各項目について命令列と、独立した呼び元・生成元・消費側またはvtable実データを照合した。

| 番地 | 付けた名前 | 型・プロトタイプ |
|---|---|---|
| `0x00949D1E` | `g_MenuOpenState` | `unsigned __int8` |
| `0x00986500` | `g_MenuScreenListHead` | `AcnlMenuScreenNodeF006 *` |

## 根拠

- ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名はsymbolsを併読。原本code.binのSHA256はbuild台帳と一致。命令列は `tools/codebytes.py` の読取関数とCapstoneで独立照合した（`_local/evidence/146/original_asm.txt`）。型・vtable・表の原本値は同所 `bytes.json` と追加検算。作業用IDBで実測はしていない。
| 対象 | 根拠 |
|---|---|
| 0x949D1E | BsMenuMgr_Init0x6D3144はSTRB 1、Menu_RequestOpen0x6D1330は1/リスト空等を検査してSTRB 2、Menu_PollOpen0x6D10A8は作成前にSTRB 3、失敗時1。Menu_AttachScreenNode0x6D102Cはノードを追加した後3→1へ戻す。 |
| 0x986500 | list base0x9864FCの+4。Menu_IsIdleAndEmpty0x6D1074はopen-state==1とhead==0の両方を見る。0x6D2D40はhead→node+8のnextを巡回しnode+12を画面本体として扱う。AttachScreenNodeは同じlistへノードを追加する。 |

- ポインタの型は既存 `AcnlMenuScreenNodeF006 *`。そのレイアウトは今回の巡回命令でも独立に確認したため、格付け?のF0424だけに依存していない。
- 旧版 `GameList.cpp:24,753` の「state3=開いている」は継続的な表示状態としては誤り。3は作成中で、登録された画面が存在しても状態1になる。`vc_INVMENU`として使われた0x986500は画面そのものへのポインタではなくノードの先頭。0で空を判定する使い方は合う。
- ACNL-F0095の1→2→3という要求処理の記述と整合し、今回は登録後の復帰と型を補足した。既存名の変更は行わない。

- 参考資料は依頼指定の旧版gohan（`_local/legacy-src/gohan-legacy/Sources`、出所は依頼文、台帳の既存キー無し）。未検証の手がかりとして用途を対比し、上記一次証拠を根拠とする。旧版本文を証拠の代わりにしない。

## 反証条件・未確認点

- リスト先頭がNULLでも他の未登録画面や作成途中が無いとは限らない。上位条件・全画面の登録期間は未確認。
- 上記生産/消費の値やvtableが別オブジェクト・別型を指すと判明した場合は再検討する。新しい実機確認やゲーム挙動の保証は含めない。
