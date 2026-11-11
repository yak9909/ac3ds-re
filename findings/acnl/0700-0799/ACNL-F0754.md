---
id: ACNL-F0754
aliases: []
title: "CLYT の組み立てとペイン・TextBox・Bounding・Group の名前検索の ABI"
summary: "Layoutの名前検索は、無条件Pane検索と実行時型で絞る検索に分かれる。Group検索は第3引数を使わず、CLYT Buildはリソースアクセサを第3引数で受け取る。"
date: 2026-11-11
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0x567bac, 0x567ea0, 0x567efc, 0x4b4328, 0x4b9474]
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

Layoutの名前検索は、無条件Pane検索と実行時型で絞る検索に分かれる。Group検索は第3引数を使わず、CLYT Buildはリソースアクセサを第3引数で受け取る。

確度MEDIUM。実測なし。各項目について命令列と、独立した呼び元・生成元・消費側またはvtable実データを照合した。

| 番地 | 付けた名前 | 型・プロトタイプ |
|---|---|---|
| `0x00567BAC` | `SsysMaLayoutNode_FindPane` | `NwLytPane *f(SsysMaLayoutNode *node, const char *name);` |
| `0x00567EA0` | `SsysMaLayoutNode_FindTextBox` | `NwLytTextBox *f(SsysMaLayoutNode *node, const char *name);` |
| `0x00567EFC` | `SsysMaLayoutNode_FindBounding` | `void *f(SsysMaLayoutNode *node, const char *name);` |
| `0x004B4328` | `SsysMaLayoutNode_FindGroup` | `void *f(SsysMaLayoutNode *node, const char *name);` |
| `0x004B9474` | `nwlyt_Layout_Build` | `bool f(void *nw_layout, const void *clyt_data, void *resource_accessor);` |

## 根拠

- ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名はsymbolsを併読。原本code.binのSHA256はbuild台帳と一致。命令列は `tools/codebytes.py` の読取関数とCapstoneで独立照合した（`_local/evidence/146/original_asm.txt`）。型・vtable・表の原本値は同所 `bytes.json` と追加検算。作業用IDBで実測はしていない。
| 対象 | 命令列と独立した呼び元・生成元 |
|---|---|
| 0x567BAC | `LDR R0,[R0,#0x20]`、rootのvt+0x2Cへname(R1),1(R2)で末尾呼び出し。`BsTimeBelWindow_Init 0x2939C8` がN_timeを探して+1760へ保存する。型フィルタは無い。 |
| 0x567EA0 | 同検索の後、vt+8で得た型の親鎖を0x96F164と比較。原本vtable `0x8FC07C+8` は0x73CF24で、そのgetterが0x96F164を返す。vtableの実名はnw::lyt::TextBox。0x2939C8がT_month等に使い、文字列設定へ渡す。 |
| 0x567EFC | 同じ親鎖を0x96F14Cと比較。原本vtable `0x8FC104+8` は0x73CFECで、getterが0x96F14Cを返す。vtable実名nw::lyt::Boundingと対応。型定義は無いので戻り値void*。 |
| 0x4B4328 | `LDR R0,[R0,#0x24]; NOP` 後0x4B4330へ連続。後者はgroupリストを巡り、group+24の名前を0x4BDB00→0x150F7Cで16byte比較し一致時groupを返す。0x4B7230のctorがvtbl_nw_lyt_Groupと同じ+24の名前を構築。0x2939C8のG_clock検索にも合う。R2は読まない。 |
| 0x4B9474 | CLYTヘッダ検査(0x4B9498)、section巡回、vt+0x40によるPane生成、AppendChild(0x4B9610)、Group ctor(0x4B96C0)、lyt1の寸法コピー(0x4B95C0/5C4)。R2を0x4B947CでR4へ、0x4B94B0でbuild resource setへ保存。呼び元ssys_ma_lyt_Layout_Build 0x5685A4はthis=node+0x10、resource accessorをR2へ渡す。 |

- 既存 `ACNL-F0751`（格付けA）の兄弟検索という記述を使用し、今回vtableの実データでTextBox/Boundingの対応を追加確認。推測された隣接getterだけに依存しない。
- 旧版 `DecorLayout.cpp:53`・`GameLabel.cpp:48,49` の用途は一致。ただし旧版のFindGroup第3引数recursiveは当該実体に効果が無い。GameList.cpp:220のBuildの3引数は正しく、古い疑似Cの2引数が欠落している。
- SsysMaLayoutNodeは既存symbolsの部分型名で、クラスの実名と主張しない。TextBoxも既存NwLytTextBoxを使用。Group/Bounding/nw::lyt::Layoutの構造体は今回新設しない。

- 参考資料は依頼指定の旧版gohan（`_local/legacy-src/gohan-legacy/Sources`、出所は依頼文、台帳の既存キー無し）。未検証の手がかりとして用途を対比し、上記一次証拠を根拠とする。旧版本文を証拠の代わりにしない。

## 反証条件・未確認点

- 型の一致はライブラリ独自の実行時型鎖。見つからない・型違いはNULL。実測なし。全種類の資源や失敗復旧は未追跡。
- 上記生産/消費の値やvtableが別オブジェクト・別型を指すと判明した場合は再検討する。新しい実機確認やゲーム挙動の保証は含めない。
