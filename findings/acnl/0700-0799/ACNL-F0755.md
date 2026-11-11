---
id: ACNL-F0755
aliases: []
title: "PWorkList の slot13 は WordFix38 の行を使って候補一覧を構築する"
summary: "PWorkListのslot13は候補を走査して一覧を構築し、行の語に100バイトのWordFix38を使う。カタログの枠種別フレームは別のfloat表で選ぶ。"
date: 2026-11-11
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0x56ce48, 0x6edee0, 0x848b18]
tags: ["layout", "catalog", "message"]
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

PWorkListのslot13は候補を走査して一覧を構築し、行の語に100バイトのWordFix38を使う。カタログの枠種別フレームは別のfloat表で選ぶ。

確度MEDIUM。実測なし。各項目について命令列と、独立した呼び元・生成元・消費側またはvtable実データを照合した。

| 番地 | 付けた名前 | 型・プロトタイプ |
|---|---|---|
| `0x0056CE48` | `script_WordFix38_Ctor` | `ScriptWordFix38 *f(ScriptWordFix38 *word);` |
| `0x006EDEE0` | `PWorkList_BuildEntries` | `bool f(void *list);` |
| `0x00848B18` | `kCatalogListKindFrameTable` | `const float[11]` |

## 根拠

- ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名はsymbolsを併読。原本code.binのSHA256はbuild台帳と一致。命令列は `tools/codebytes.py` の読取関数とCapstoneで独立照合した（`_local/evidence/146/original_asm.txt`）。型・vtable・表の原本値は同所 `bytes.json` と追加検算。作業用IDBで実測はしていない。
| 対象 | 根拠 |
|---|---|
| 0x56CE48 | `MOV R2,#0x26; ADD R1,R0,#0x18; BL vc_SETUPSTACK`、vtbl_script_WordFix_38u格納、0x5F3F84で+0xCのメタデータ初期化、+0x18から0x4Cバイトをクリア。返り値はthis。 |
| 0x6EDEE0 | 原本 `vtbl_PWorkList 0x8F3AA8 +13*4` の値が0x6EDEE0。0x6EDEF8/0x6EDF0Cで候補条件を検査し、0x6EDF20のID取得後、0x6EDF40で0x56CDEC(this+4812+100*count,id)を呼ぶ。0x6EDF54は候補IDをthis+15112+countへ、0x6EDF68は件数をthis+2500へ保存。ループ端は103。 |
| 0x848B18 | `BsMenuCatalog_StartListEnter 0x21B874` の0x21B8B8〜0x21B8CCはthis+15264のu8を4倍して表を引き、VLDR S0→UiAnim_SetFrame。0x21A794は非ゼロの一覧種別に5を足して同じ欄へ保存。原本の11語はfloatで0,0,0,0,0,1,2,2,3,0,0、その次は名前書式のASCII。 |

- `ScriptWordFix38` は先頭vptr/buffer/capacityと+0x18のUTF16[38]を定義。+0xC..+0x17は未解明欄として残す。型サイズ100はctorの書込範囲とPWorkListの独立したstrideで一致する。
- `0x56CDEC` はIDを0x5C97B8でメッセージ番号へ変換し、`STR_Fobj_name`をWordへ設定する。0x6EDEE0そのものは語取得関数ではない。
- 旧版 `GameList.cpp:123,127,160`。WordFix<38>と100byte、枠フレーム用途は一致。「vt[13]の行の語、sub_56CDECと同じ」は正確でなく、slot13は一覧の構築処理でその中から56CDECを使う。
- 表の型は `const float[11]`。表の特定値だけからゲーム内の一覧種別の意味を増やさない。

- 参考資料は依頼指定の旧版gohan（`_local/legacy-src/gohan-legacy/Sources`、出所は依頼文、台帳の既存キー無し）。未検証の手がかりとして用途を対比し、上記一次証拠を根拠とする。旧版本文を証拠の代わりにしない。

## 反証条件・未確認点

- 103候補の全IDの意味や選択条件のゲーム内名称は未確認。11語の領域を超える参照の安全性は保証しない。実機表示未確認。
- 上記生産/消費の値やvtableが別オブジェクト・別型を指すと判明した場合は再検討する。新しい実機確認やゲーム挙動の保証は含めない。
