# アイテム名・アイコン資源経路 — JPN v1.5

## 要点

通常アイテムでは、Item IDから「名前」と「アイコン」は別々の資源へ分岐する。

```text
Item ID
  |
  +-- Item.bin record +0x00 u16
  |     -> icon basename table
  |     -> icn_NNN.bclim
  |     -> ItemWin layout archive / timg resource
  |
  +-- normal item param index
        -> STR_Item_name[index]
        -> Script/Str/STR_Item_name.umsbt
```

したがって将来のmodでは、アイコン変更はItem.bin + layout archive/BCLIM、名前変更はUMSBTを扱う。

## Item ID index

```text
idx = (itemId & 0x7FFF) - 0x2000
valid when idx < 0x172B
```

`Item.bin` record sizeは0x1E bytes。

## アイコン

`ItemParam_GetIconBaseName @ 0x535110` が `Item.bin[idx]+0x00` のu16を読み、0x872C44の507-entry basename tableへ引く。

戻り値は `icn_000`～`icn_522`系のbasenameで、UI側は `%s.bclim` を付ける。

`ItemIconWidget_SetItem @ 0x2B8EAC`:

- pane `P_itemIcon`
- `%s.bclim`
- fallback `icn_000.bclim`
- layout resource type `timg`

を使用する。

core ItemWinは `Layout/ItemWin/item_icon.arc` を開く。別UIは `Layout/ItemWin/item_icon_tex.arc` も使用する。

## 名前

`ItemName_ResolvePhrase @ 0x56D274` の通常経路は、同じ`idx`を `STR_Item_name` のmessage entry indexとして使う。

資源パスは:

```text
Script/Str/STR_Item_name.umsbt
```

特殊/動的アイテムは別名生成へ分岐するため、全Item IDを単純にUMSBT index対応とみなしてはいけない。

## mod設計

特定Item IDだけを既存アイコンへ差し替えるなら、`Item.bin[idx]+0x00` のiconNameIndex変更が最小。

既存`icn_NNN.bclim`自体を置換すると、そのbasenameを共有する全Itemへ影響する。

完全に新しいbasenameを使うには、507-entry executable tableの既存entryを安全に再利用するか、table/countを拡張するか、`ItemParam_GetIconBaseName`をhookする必要がある。

名前は`.arc`ではなく`STR_Item_name.umsbt`を編集する。

## 未確定

ACNLの実`.arc`ファイルが現在の資料に無いため、NintendoWare `ArcResourceAccessor`で読むことまでは確定しているが、on-disk containerのmagic/packing方式は未確定。

`item_icon.arc`と`item_icon_tex.arc`の実ファイルを取得後に、再パック仕様と両archiveのBCLIM重複関係を解析する。
