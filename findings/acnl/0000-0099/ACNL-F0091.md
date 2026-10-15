---
id: ACNL-F0091
aliases:
- F-53
title: F-53 RTTI から全クラス名をデマングルして命名した — `HIGH`
summary: '`code.bin.i64`（セッション `acnl_code`）に **クラス 2,895 件・名前 5,481 件**を入れた。'
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9228288
- 9326592
tags:
- rtti
supersedes: []
source: v1:RE/FINDINGS.md:2924-2997
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-53 RTTI から全クラス名をデマングルして命名した — `HIGH`

`code.bin.i64`（セッション `acnl_code`）に **クラス 2,895 件・名前 5,481 件**を入れた。

| 項目 | 件数 |
|---|---|
| TypeInfo | **2,895** |
| vtable | **2,586** |
| 継承なし (`__class_type_info`) | 440 |
| 単一継承 (`__si_class_type_info`) | 2,192 |
| 多重継承 (`__vmi_class_type_info`) | 263 |
| vtable が複数あるクラス | 194（最大 4 本） |
| vtable を持たない TypeInfo | 533（テンプレート実体など） |
| 識別子の衝突 | **0** |

### 手順

1. **`rtti_dump.py`** — `code_runtime.bin` を走査して `scratchpad/rtti.json` を作る
   - `__cxxabiv1` の 3 種の type_info vtable を名前から逆引きし、
     `TypeInfo[0]` がそれらのいずれかで `TypeInfo[4]` がシンボルテーブル
     (`0x8CD000`-`0x8E5000`) を指すものを TypeInfo とみなす
   - vtable は「`TypeInfo` のアドレスを値として持つワードの次」= `vmethods[0]`
2. **デマングル** — マングル名は `_Z` が落ちているだけなので `_ZTS` を付けて
   `c++filt` に渡す（MSYS2 に入っている）。一括で流せば順序は保たれる
   ```
   N5fgobj11ObjectSwingE -> _ZTSN5fgobj11ObjectSwingE -> typeinfo name for fgobj::ObjectSwing
   ```
3. **`rtti_apply.py`** — `rtti.json` を読んで IDB へ一括適用（べき等）

### 命名規則

```
ti_<Class>        TypeInfo。型は継承の種類に応じた構造体
vtbl_<Class>      vtable。多重継承で複数あるときは 2 本目以降に _1 _2 _3
```

`::` は `_`、テンプレートの `<>` `,` も `_` に落とす。
`state::Mode<Wipe>` → `state_Mode_Wipe`。

### 何が変わったか

**継承関係が `xrefs_to` で辿れるようになった。**
`ti_X` への xref = `X` を基底に持つクラスの TypeInfo。

例: `xrefs_to ti_ssys_co_FaderBase` → `ti_FaderColor` / `ti_FaderMoment` / `ti_FaderWipe`。
F-51 で「派生は 3 つだけ」と結論するのに専用スクリプトを書いたが、いまは 1 クエリで済む。

vtable もデコンパイル結果に名前で出る:

```c
FieldObj_SpawnFallActor:
    *v12 = &vtbl_fgobj_ObjectSwing;
```

### 教訓 — 大量の機械的作業を MCP のバッチで押し込まない

最初 idalib の `type_apply_batch` に 300 件ずつ 19 バッチで流そうとした。
**1 バッチを自分で書き写す必要があり、実際に 1 バッチ目で 11 クラス分を落とした。**

**生成できる作業はスクリプトにして 1 回で流す。**
`rtti_apply.py` なら 5,481 件が一度に入り、取りこぼしも起きない。
「MCP のツールで殴れるか」ではなく「スクリプトにできるか」を先に考える。

### 運用上の注意

**idalib でセッションを開いたまま IDA GUI で同じ IDB を開いてはいけない。**
idalib は `.id0` / `.id1` / `.nam` / `.til` を掴んだままで、`idb_save` はそれを消さない。
GUI 側に「IDA did not close properly」が出て、そのまま進めると 2 プロセスが
同じ DB を書いて壊れる。**GUI で作業する前に必ず `idb_close` すること。**
それでもルースファイルは残るので、パック済みの `.i64` が最新なら
GUI 側では「Restore packed base」を選ぶのが安全。

---

