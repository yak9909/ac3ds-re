---
id: ACNL-F0092
aliases:
- F-54
title: F-54 CTRPF プラグインの地域別アドレス表 — 本ビルドは **JPN 無印** — `HIGH`
summary: '`REFERENCES/CTRPF PROJECTS/Vapecord-ACNL-Plugin-master` の解析。'
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7456272
- 7456232
- 7705288
- 7705248
- 8478348
- 8478308
- 7148336
- 7148296
- 7485524
- 7485484
- 5891508
- 1478152
- 5888636
- 3141176
- 6968284
- 5896948
- 5897468
- 6604424
- 6869228
- 3131512
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:2998-3115
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-54 CTRPF プラグインの地域別アドレス表 — 本ビルドは **JPN 無印** — `HIGH`

`REFERENCES/CTRPF PROJECTS/Vapecord-ACNL-Plugin-master` の解析。
ユーザーの「地域ごとにアドレスが変わるのでは」という見立ては**正しかった。**

### 仕組み

`include/core/infrastructure/Addresses.hpp`:

```cpp
static const u32 ADDRESSES[][8] = {
    { USA, USAWA, EUR, EURWA, JPN, JPNWA, KOR, KORWA },  //NAME
    ...
```

`src/core/infrastructure/Address.cpp`:

```cpp
Address::Address(u32 address) {
    if (regionId == Region::USA) { SetAddressData(address); return; }   // USA はそのまま
    for (const auto& row : ADDRESSES) {
        if (row[0] == address) { SetAddressData(row[regionId]); return; }
    }
    SetAddressData(address);   // 表になければ動的アドレスとみなしてそのまま使う
}
```

**ソースコード中に直接書かれているアドレスはすべて USA 版**であり、
`Region::USA == 0` なので `row[0]` がキーになる。他地域は `row[regionId]` へ差し替える。
地域は `Process::GetTitleID()` から決まる（`Address::LoadRegion`）。

| Region | index | TitleID |
|---|---|---|
| USA | 0 | `0x0004000000086300` |
| USAWA | 1 | `0x0004000000198E00` |
| EUR | 2 | `0x0004000000086400` |
| EURWA | 3 | `0x0004000000198F00` / `0x00040000004C5700` |
| **JPN** | **4** | **`0x0004000000086200`** |
| JPNWA | 5 | `0x0004000000198D00` |
| KOR | 6 | `0x0004000000086500` |
| KORWA | 7 | `0x0004000000199000` |

WA = Welcome amiibo（amiibo+）。表は **465 行**、うち JPN と JPNWA が違う行が 110。

### 本ビルドは JPN 無印（index 4）

`SUB_*` という名前の行（＝関数のはず）で JPN 列と JPNWA 列の両方を
`code.bin.i64` で引き、**関数先頭に当たるか**で判定した:

| 行 | JPN | 結果 | JPNWA | 結果 |
|---|---|---|---|---|
| `SUB_71DE5C` | `0x71C610` | `sub_71C610` 先頭 ✓ | `0x71C5E8` | 関数途中 ✗ |
| `SUB_75AB28` | `0x7592C8` | 先頭 ✓ | `0x7592A0` | 途中 ✗ |
| `SUB_8176E4` | `0x815E8C` | 先頭 ✓ | `0x815E64` | 途中 ✗ |
| `OPEN_MENU` | `0x6D1330` | 先頭 ✓ | `0x6D1308` | 途中 ✗ |
| `GET_ITEM` | `0x723854` | 先頭 ✓ | `0x72382C` | 途中 ✗ |

**JPN 5/5、JPNWA 0/5。** 対象は**日本語版の無印**であり amiibo+ ではない。
長く未確定だった版の問題がこれで決着した。

### 本解析との突き合わせ（11 件が独立に一致）

| JPN | 本解析の名前 | プラグインのラベル |
|---|---|---|
| `0x59E5B4` | `Item_PlaceItem` | `PLACEITEMOFFSET` |
| `0x168E08` | `Field_SetItemAt` | `TRAMPLE1` |
| `0x59DA7C` | `Field_MarkDirty` | `TRAMPLE3` |
| `0x2FEE38` | `Field_GetItemAtXY` | `WORLDITEMCOORDS` |
| `0x6A53DC` | `Field_GetMapManager` | `CURRENTMAP` |
| `0x59FAF4` | `FieldAction_FindActive` | `GETLOCKED` |
| `0x59FCFC` | `FieldAction_RegisterActive` | `CREATELOCKED` |
| `0x64C688` | `Actor_SetState` | `ANIMFUNCTION` |
| `0x68D0EC` | `Actor_PlayAnim` | `SNAKEFUNC` |
| `0x2FC878` | `Item_Copy` | `COPYPASTEFUNC` |
| `0x2FCBB4` | `Item_InitWithId` | `SETSTACK` |

`TRAMPLE1` = `Field_SetItemAt`、`TRAMPLE3` = `Field_MarkDirty` は、
**F-47 の踏みつけ処理がその 2 つを順に呼ぶ**ことと正確に一致する。
JPN 列の対応付けが正しいことの裏付けになっている。

### 一番の収穫 — USA アドレスからの橋渡し

**公開されている ACNL のチート・プラグインはほぼ USA 版アドレスで書かれている。**
この表があれば USA → JPN の変換ができる。逆に、本解析で見つけた JPN アドレスに
対応する USA アドレスが分かれば、他所の資料と突き合わせられる。

`vc_addresses.py` で JPN 列に `vc_<LABEL>` の名前と、
USA / EUR / KOR のアドレスを併記したコメントを入れる。

### 扱い方の注意

- ラベルは**プラグイン作者の主観**であり検証済みの識別ではない。
  `ANTI_ANIM_1` `DONT_DELETE_SEED_ITEMS_PATCH` のような
  「パッチを当てる場所」のラベルも混ざっている
- したがって名前には **`vc_` 接頭辞**を付けて出典を明示し、
  **本解析で名前を付けた箇所は上書きしない**
- 表に無いアドレスは `Address::Address` が「動的アドレス」とみなして
  そのまま使う。**つまり表に無い＝地域非依存とは限らない。**
  プラグイン側で単に未対応なだけの可能性がある

### 付随して片付いた未検証事項

`classes.txt` の「ドロップ関数 `0x59E5B4` は `0x19F86C`（`vtable for BsMenuItem`）から
呼ばれている」を検証した。

- **`0x19F86C` を参照するのは `0x8E522C` の 1 箇所だけで、これは `vtbl_BsMenuItem + 0x0C`。**
  「BsMenuItem の vtable に載っている」という主張は**正しい**
- ただし `Item_PlaceItem` の**直接の**呼び出し元は 16 箇所で、
  すべて `0x595xxx`-`0x598xxx` のフィールドオブジェクトモジュール内。
  **`0x19F86C` は直接の呼び出し元ではない**
- 原文が「lr を辿っていくと」と書いているとおり、これは**コールスタックの祖先**の話。
  静的な xref では確認できない種類の主張だった

`classes.txt` のアドレスは**日本語版無印のもの**で本解析の対象と一致する。
（`0x59E5B4` も `0x8CD000`-`0x8E5000` も本ビルドの値）

---

