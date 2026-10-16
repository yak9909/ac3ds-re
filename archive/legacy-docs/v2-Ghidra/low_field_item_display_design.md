# 低ID Field Object Item 表示拡張設計 — JPN v1.5

## 結論

0x0000～0x00FAを表示上だけ独自化し、Item.binの通常Item体系には入れない設計を推奨する。

```text
low field-object Item
  |
  +-- icon: low-ID display resolver -> fgo_XXX.bclim
  |
  +-- name: low-ID name resolver -> custom UMSBT entry
```

`Item_ToParamIndex`自体は変更しない。

## stock fallback

0x0000～0x00FAは通常Item範囲外なのでItem.bin recordを持たない。

アイコン:
`ItemParam_GetIconBaseName` がNULL record時にtable[0] = `icn_000`を返す。

名前:
`ItemName_ResolvePhrase`で通常名を設定できず、empty-name fallbackへ落ちる。実機表示は`???`。

## custom icon

推奨basename:

```text
fgo_000
fgo_001
...
fgo_0fa
```

各文字列は7 bytes + NUL = 8 bytesなので、`base + (id << 3)`で直接参照できる。

arc内のファイル順はruntime mappingではない。ArcResourceAccessorはfilenameをキーに検索する。

## custom name

初期実装では既存 `STR_Item_name.umsbt` の末尾に0xFB entriesを追加し、

```text
customIndex = originalEntryCount + lowId
```

とするのが最小変更。

新規 `STR_FgObj_name.umsbt` は設計として綺麗だが、Script/Str resource table拡張が追加で必要。

## なぜItem.binへ追加しないか

`Item_ToParamIndex`は17 direct callers、`ItemParam_GetRecord`は324 direct callersが存在する。

低IDをItem.binへ通すと、表示だけでなくcategory/behavior/predicateへ波及するため危険。

## resource pack

まずはstock `item_icon.arc`を保持したままcustom BCLIMを追加する。

別UIで `item_icon_tex.arc` も使用されるため、実archive比較後に両方へ同じcustom BCLIMを入れるか決める。

archive orderではなく、1つのmanifestからicon filenameとname entryを生成する。
