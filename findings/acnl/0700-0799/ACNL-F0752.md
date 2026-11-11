---
id: ACNL-F0752
aliases: []
title: "フォントの登録は名前付き非所有エントリを作り、名前取得は SafeString を返す"
summary: "フォントの名前・登録・所有者を識別できる。名前取得の返り値は文字列本体ではなく SafeString、登録の返り値は登録エントリである。"
date: 2026-11-11
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0x4b3fd4, 0x747528, 0x94c9c8]
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

フォントの名前・登録・所有者を識別できる。名前取得の返り値は文字列本体ではなく SafeString、登録の返り値は登録エントリである。

確度MEDIUM。実測なし。各項目について命令列と、独立した呼び元・生成元・消費側またはvtable実データを照合した。

| 番地 | 付けた名前 | 型・プロトタイプ |
|---|---|---|
| `0x004B3FD4` | `nwlyt_ArcResourceAccessor_RegisterFont` | `void *f(void *accessor, const char *name, NwFontResFont *font);` |
| `0x00747528` | `Font_GetNameString` | `const void *f(void *manager, int slot);` |
| `0x0094C9C8` | `g_FontMgr` | `void *` |

## 根拠

- ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名はsymbolsを併読。原本code.binのSHA256はbuild台帳と一致。命令列は `tools/codebytes.py` の読取関数とCapstoneで独立照合した（`_local/evidence/146/original_asm.txt`）。型・vtable・表の原本値は同所 `bytes.json` と追加検算。作業用IDBで実測はしていない。
- `0x4B3FD4`: `MOV R3,#0; ADD R0,R0,#0x24; NOP` のあと `0x4B3FE0` へ連続する。後者は `0x90` バイトを確保し、+8 に最大127文字の名前、+0x88 に font、+0x8C に R3=0 を置いてリストへ追加し、そのエントリを返す。
- 解放側 `0x4B4070` はエントリ+0x8Cが非ゼロの時だけ+0x88のフォントとglyph texture descriptorsを解放し、エントリ本体は常に解放する。登録時0の非所有という意味を、確保側の値だけでなくこの消費側でも確認した。
- 独立した呼び元 `BsMenuCatalog_Init 0x21C76C` の `0x21C7E8→0x21C81C` と `BsTimeBelWindow_Init 0x2939C8` の `0x293B48→0x293B7C` は、名前取得→SafeString vt+8→+4 の char*→Font_GetLoadedFont→登録の順。
- `0x747528`: slot0/1/2/4 に manager+0x15C/+0x2F4/+0x48C/+0x7BC、それ以外に+0x624を返す。`0x52D8EC` の固定長文字列構築と対応する。slot境界検査はなく、不正値もslot3へ行く。
- `0x94C9C8`: `0x52D418` が生成・公開し、Garden_msg_size16/ruby/no/no_f16の読み込みを進める。上記二つの呼び元が同じ大域値を名前取得とFont_GetLoadedFontへ渡す。構造体が未定義なので型は `void *`。
- 旧版 `DecorLayout.cpp:50,52,74`、`GameLabel.cpp:19,61`。書体の登録という用途は一致。旧版RegisterFontのvoid戻り値より正確には登録エントリ。FontNameは生のchar*ではない。

- 参考資料は依頼指定の旧版gohan（`_local/legacy-src/gohan-legacy/Sources`、出所は依頼文、台帳の既存キー無し）。未検証の手がかりとして用途を対比し、上記一次証拠を根拠とする。旧版本文を証拠の代わりにしない。

## 反証条件・未確認点

- 登録エントリの自動解放とフォント本体の寿命は別。全スロットの読み込み時点・実画面は未実測。
- 上記生産/消費の値やvtableが別オブジェクト・別型を指すと判明した場合は再検討する。新しい実機確認やゲーム挙動の保証は含めない。
