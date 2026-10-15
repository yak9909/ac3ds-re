---
id: ACNL-F0081
aliases:
- F-43
title: F-43 RTTI からクラス名を引ける — `HIGH`
summary: '出典: `REFERENCES/TEXTS/classes.txt` / `2.txt` / `1.txt`。**実機メモリで裏取り済み。**'
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9228288
- 9326592
- 9175040
- 9437184
- 9387472
- 9445100
- 9445196
- 9382332
- 5891508
- 1701996
tags:
- rtti
supersedes: []
source: v1:RE/FINDINGS.md:2086-2158
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-43 RTTI からクラス名を引ける — `HIGH`

出典: `REFERENCES/TEXTS/classes.txt` / `2.txt` / `1.txt`。**実機メモリで裏取り済み。**

### レイアウト

| 領域 | 内容 |
|---|---|
| `0x8CD000` - `0x8E5000` | シンボルテーブル（マングル名の文字列） |
| `0x8C0000` 台 | `TypeInfo`（RTTI） |
| `0x900000` 付近 | vtable が大量 |

vtable は次の並びで、**ポインタは `vmethods[0]` を指す**:

```
vtable-8   int        offset_to_top
vtable-4   TypeInfo*  ti
vtable+0   void*      vmethods[N]
```

`TypeInfo`（単一継承 `__si_class_type_info` の場合）:

```
+0  void*      vptr    -> vtbl___si_class_type_info (0x8F3DD0)
+4  char*      name    -> シンボルテーブル内のマングル名
+8  TypeInfo*  base    -> 基底クラス（継承なしのときは無い）
```

`0x8F3DD0` の TypeInfo を辿ると `N10__cxxabiv120__si_class_type_infoE` が読めた。
**資料の記述どおり。**

マングル名は `_Z` が落ちているだけなので、頭に付ければ `c++filt` でデマングルできる。

```
N5fgobj11ObjectSwingE  ->  _ZN5fgobj11ObjectSwingE  ->  fgobj::ObjectSwing
```

### 実測で確定したクラス

| アドレス | 種別 | クラス |
|---|---|---|
| `0x901EEC` | vtable | **`fgobj::ObjectSwing`** — 倒木アクター |
| `0x901F4C` | vtable | **`fgobj::ObjectTimer`** — 結果アイテムのアクター（赤いバラが出ていたもの） |
| `0x8F29BC` | vtable | **`AcPlayer`** — `g_PlayerObjects[0]` の実体 |
| `0x8F3DD0` | vtable | `__cxxabiv1::__si_class_type_info` |

`fgobj` の 2 つは共通の継承チェーンを持つ:

```
fgobj::ObjectSwing / fgobj::ObjectTimer
  -> fgobj::ObjectExe
  -> fgobj::ObjectBase
  -> ssys::st::ListNodePriorityBase
  -> ssys::st::ListNode
```

`ssys` は sead 系のライブラリ名前空間。フィールドオブジェクトが
優先度つき連結リストのノードとして管理されていることが分かる。

**再現手順は `rtti.py` に落とした。** `TARGETS` にアドレスと種別
（`vtable` / `object` / `ptr`）を並べて実行する。

### メンバ関数の探し方（資料由来、未検証）

vtable は必ず `offset_to_top / TypeInfo* / vmethods[]` の並びなので、
**TypeInfo のアドレスを数値としてサーチすれば vtable が見つかる。**
`this` から型情報を取るときは vtable ポインタから 4 を引く。

資料は「ドロップ関数 `0x59E5B4` の LR を辿ると `0x19F86C` から呼ばれており、
`0x19F86C` は `vtable for BsMenuItem` に載っている」としている。**未検証。**

---

