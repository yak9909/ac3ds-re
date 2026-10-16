# データ構造・テーブル

## アイテム (4バイト)

```
+0 : u16  ID | bit15フラグ     (ID は下位15bit、0x7FFF でマスクして取り出す)
+2 : u16  フラグ              (bit15 = 埋設フラグ)
```

特殊値:

| 値 | 意味 |
|---|---|
| `0x7FFE` (32766) | 空マス。`g_EmptyItem` @ `0x00955FF4` |
| `0x7FFC` (32764) | 別の特殊アイテム @ `0x00955FF8` |
| `158` (`0x9E`) | 穴（推定。掘ると残り、さらに掘ると空に戻る対称性が根拠） |

## 地面オブジェクト定義テーブル

`0x3306FA00 + 16 * ID`（16バイト × 254エントリ、リニアヒープ上）

| オフセット | 内容 |
|---|---|
| `+0x0A` | カテゴリ |
| `+0x0D` | 成長段階数 (signed)。`-1` は非成長 |

実測値:

| ID | cat | 段階 | 備考 |
|---|---|---|---|
| 38 | 4 | 4 | 113-117 と定義がバイト単位で完全一致 |
| 43 | 8 | 4 | 118-122 と完全一致 |
| 139 | 23 | 2 | |
| 153 | 10 | -1 | 構造物 |
| 158 | 0 | -1 | 穴（推定） |
| 201 / 204 | 21 | -1 | 定義が同一 |

## アニメーション名テーブル

`g_AnimNameTable` @ `0x0085FFB0`（16バイト刻み。終端は未検証、約1028エントリ）

```
+0  : 未使用 (常に0)
+4  : 本体アニメ名へのポインタ
+8  : "_e1" 派生
+12 : "_m1" 派生
```

**注意**: `0x85FFC0` を先頭と誤認しやすい。idx 0 は全ゼロエントリで、
名前が非NULLになる最初のエントリは idx 1 (`scoop_wait1`)。実機検証で `0x85FFB0` と確定。

スコップ帯:

| idx | 名前 | 意味 |
|---|---|---|
| 71 | `scoop_swing1` | 振り下ろし |
| 72 | `scoop_swing_wait1` | 振り下ろし後の保持 |
| 73 | `scoop_dig1` | 穴掘り |
| 74 | `scoop_hane1` | 弾かれ |
| 75 | `scoop_suka1` | 空振り |
| 76 | `scoop_stump1` | 切り株 |
| 77 | `scoop_get1` | 採取成功 |
| 78 | `scoop_putaway1` | しまう |
| 79 | `scoop_bury1` | 埋める |
| 102 | `net_swing1` | 虫取り網を振る |
| 237 | `barber_set1` | 美容室・セット開始 |
| 238 | `barber_cut1` | 美容室・カット |
| 239 | `barber_eye1` | 美容室・目の色 |
| 240 | `barber_mii1` | 美容室・Mii 化 |

## プレイヤーオブジェクト

`g_PlayerObjects` @ `0x00AA7994`（ポインタ × 4人分。実機では [0] のみ有効）

| オフセット | 内容 |
|---|---|
| `+0x14` | 座標 X/Y/Z (float × 3) |
| `+0x148` | AR 状態キックの対象選択に使われる sentinel。厳密な意味は未確定 |
| `+0x171` | フラグ。**bit5 = 掘れる対象が前方にあるか** |
| `+0x174` | アクション準備フラグ。bit1 を虫取り網アクションが検査 |
| `+0x1A8`-`+0x1AB` | 状態制御 tuple。`+0x1A9`=現在状態、`+0x1AA`=直前状態。両端は未確定 |
| `+0x22C` | 埋め込みサブオブジェクト |
| `+0x29C` `+0x2B4` `+0x2CC` `+0x2E4` | アニメスロットへのポインタ（ストライド 0x18） |
| `+0x3EC` | スケール X/Y/Z |
| `+0x5A4` `+0x5A8` | 状態決定に使われる値 |
| `+0x8CA` 以降 | **状態別 scratch 領域**。スコップ状態では対象 X/Y、状態 `0xB9` では下記 |
| `+0x8CA` | 状態 `0xB9`: 髪型（0-33） |
| `+0x8CB` | 状態 `0xB9`: 髪色（0-15） |
| `+0x8CC` | 状態 `0xB9`: 目の色（0-5） |
| `+0x8CD` | 状態 `0xB9`: 見た目用 Item（4B） |
| `+0x8D1` | 状態 `0xB9`: 補助フラグ |
| `+0x942` | 適用済み髪型（u8） |
| `+0x944` | 適用済み髪色（u32） |
| `+0x948` | 適用済み目色（u32） |
| `+0xBDC` `+0xBDD` | 対象マス座標 X / Y（状態遷移用） |
| `+0xBDE` | **次に入る状態ID** |
| `+0xBDF` | サブモード |

### アニメスロット (スロット+0x30 からフレーム制御)

vtable 2本 (`0x008FC930` / `0x008FC964`) を持つ多重継承クラス。

| スロット相対 | 内容 |
|---|---|
| `+0x38` `+0x3C` | 区間値 |
| `+0x40` | **再生レート**（通常 1.0） |
| `+0x44` | 現在フレーム |
| `+0x48` | 総フレーム数 |
| `+0x4C` | 超過時処理。`0x4D3EFC`=clamp(単発) / `0x4D3E70`=wrap(ループ) |

安定したポインタチェーン:

```
[[0x00AA7994] + 0x29C] + 0x40    スロット0の再生レート
[[0x00AA7994] + 0x2B4] + 0x40    スロット1
[[0x00AA7994] + 0x2CC] + 0x40    スロット2
[[0x00AA7994] + 0x2E4] + 0x40    スロット3
```

## プレイヤー状態機械

状態記述子テーブル基準 `0x00843634`、**エントリサイズ `0x1C`**。
状態 N のエントリ関数 = `[0x843634 + N*0x1C]`。

`Actor_SetState(actor, stateID, a3, a4)` が遷移を行い、内部の `BLX R2` (`0x64C7F4`) で
エントリ関数を呼ぶ。

| 状態ID | 記述子 | ハンドラ | 実体 |
|---|---|---|---|
| 6 (`0x06`) | `0x8436DC` | `0x658A68` | neutral / wait。AR 状態キックの遷移先 |
| 13 (`0x0D`) | `0x8437A0` | `0x6584A8` | movement。AR 状態キックでは直前状態として設定 |
| 74 (`0x4A`) | `0x843E4C` | `0x680EBC` | 掘る振り下ろし |
| 75 (`0x4B`) | `0x843E68` | `0x669184` | 空振り |
| 76 (`0x4C`) | `0x843E84` | 未読 | 跳ね返り（`0x67AD6C` 側） |
| 77 (`0x4D`) | `0x843EA0` | `0x67DE00` | 跳ね返り（`0x67DE48` 側） |
| 79 (`0x4F`) | `0x843ED8` | `0x6691E0` | 不明（未検証） |
| 112 (`0x70`) | `0x844274` | `0x668E18` | 虫取り網。`net_swing1`（anim 102） |
| 185 (`0xB9`) | `0x844A70` | `0x687E24` | 美容室／見た目変更。同期コールバックは後述 |

状態選択は `0x663284` 以降で `[player+0xBDE]` を読んで分岐する。
値の設定元: `R11 = 0x4D` (`0x662FE8`)、`R8 = 0x4C` (`0x663034`)、`R9 = 0x4B` (`0x663050`)。

状態記述子は `+00` enter、`+08` update、`+10` ローカル同期、`+18` リモート受信処理。
状態 `0xB9` では順に `0x687E24`, `0x6831B8`, `0x685738`, `0x68B9F8`。

### 状態 `0xB9` の見た目変更パケット／プロフィール

`Player_StartAppearanceChange` は `vc_GETANIMINST(player)` の返す領域へ次を設定する。

| packet off | 内容 |
|---|---|
| `+14` | 髪型 |
| `+15` | 髪色 |
| `+16` | 目の色 |
| `+17` | 見た目用 Item（4B） |
| `+21` | 補助フラグ |

同期先の `vc_PSOFFSET(playerNo)` プロフィールレコードでは
`+4`=髪型、`+5`=髪色、`+7`=目色、`+10`=見た目用 Item、`+14`=付随領域。
ローカル同期 (`0x685738`) とリモート受信 (`0x68B9F8`) の双方が同じフィールドを更新する。

`profile+10` は実際には `0x21` byte の衣装ブロック先頭で、アクター側 `player+0x920` に対応する。
`PlayerOutfit_Copy` (`0x10AC4C`) が 4B Item × 8 と末尾 1B をコピーする。

| index | actor off | profile off | 内容 |
|---:|---:|---:|---|
| 0 | `+0x920` | `+10` | Hat |
| 1 | `+0x924` | `+14` | Accessory / Glasses |
| 2 | `+0x928` | `+18` | TopWear |
| 3 | `+0x92C` | `+22` | UnderTopWear |
| 4 | `+0x930` | `+26` | BottomWear |
| 5 | `+0x934` | `+30` | Socks |
| 6 | `+0x938` | `+34` | Shoes |
| 7 | `+0x93C` | `+38` | HeldItem |
| — | `+0x940` | `+42` | 付随 byte |

状態 `0xB9` は anim 237 のマーカーで actor index 0/1 を空にし、退出同期でも
profile index 0/1 を空にする。通常髪型変更で帽子とアクセサリが消える直接原因（F-67）。

## `nw::font::ResFont` / glyph atlas (F-133, static; F-135 cross-checked; F-139 live)

`ResFont+0x04` は CFNU/CFNT resource base、`+0x08` は FINF payload、
`+0x0C` は sheet descriptor table、`+0x10` は filter flags。

### TGLP payload

| offset | 型 | 内容 |
|---:|---|---|
| `+0x00/+0x01` | u8 | cell width / cell height |
| `+0x02/+0x03` | u8 | baseline 系 / max character width（名称未確定） |
| `+0x04` | u32 | sheet byte stride/size |
| `+0x08` | u16 | sheet count |
| `+0x0A` | u16 | texture format |
| `+0x0C/+0x0E` | u16 | columns / rows per sheet |
| `+0x10/+0x12` | u16 | sheet width / height |
| `+0x14` | ptr | raw glyph-sheet atlas |

### glyph-sheet descriptor (1 sheet = 0x14 bytes)

| offset | 内容 |
|---:|---|
| `+0x00` | texture handle 初期値 0 |
| `+0x04` | owner `ResFont*` |
| `+0x08` | `sub_143B54(raw) >> 3`。アドレス変換後の GPU 用表現（raw pointer の単純な `>>3` ではない） |
| `+0x0C/+0x0E` | height / width |
| `+0x10` | texture format |

raw sheet は `TGLP+0x14 + index * LE32(TGLP+0x04)`。`0x143718`→`0x144C44` の
IPC header `0x001F0082` へ全 sheet 範囲を渡す。
`0xFFFF8001` は `dword_8AD218` の process handle 値であり command ID ではない。
既知の `GSPGPU_FlushDataCache` (`0x13B6A4`, header `0x00080082`) とは header が異なるため、
この request の正確な cache semantics は未確定である。glyph 描画の静的経路は
`0x7438B4` → `0x4D4EAC` → `0x4D8484` → `0x7A7FAC`。`0x4D8484` は
decompiler の表示上より多く、width/height/format/raw sheet を format-dependent に
`0x7ABDBC` へ渡した後に wrap/filter state を設定する（F-137）。

F-135 の独立照合で、上記6関数（parser、EmitGlyphQuad、descriptor loop/init、sheet-table
size、texture parameters）の raw bytes は `code.bin.i64` と実機コードダンプ由来の
`code_runtime.elf.i64` で同一 VA・差分 0 bytes だった。これは静的な offset/layout の
ビルド一致を裏付けるが、ライブ実機の descriptor 値・lazy handle の生成時点までは示さない。

### F-139 実機値（読み取り専用）

Remote GDB の会話表示で `nwfont_ResFont_MapCharToGlyph` (`0x743768`) に停止した際、
`ResFont*=0x3302ABE0`、入力 UTF-16 `0x904A`、戻り glyph index `0x0A01` を確認した。
cache フィールド `ResFont+0x14/+0x16` は `0x904A/0x0A01` に更新された。
`nwfont_CharWriter_EmitGlyphQuad` (`0x4D4EAC`) では glyph record がスタック上に生成され、
raw sheet `0x318B2A80`、glyphWidth 4、cellHeight 24、sheet 128×128、format `0x0B`、
descriptor `0x319BEB70`、`writer+0x44=0x32D3A6F0`（非零）だった。従って実機は
texture bind を行わない batch 分岐を選び、終端で44-byte instance（`0x32D3A770`）へ
descriptor を格納した。17×24/7×7/40×29/26×21 フォントの descriptor table（154/3/3/1
sheets）を停止中に走査したが、`descriptor+0` handle は全て0であり、lazy materialize の
時点は後段 submit または immediate 経路の未解決事項である。

## `DropData` — `g_DropDataTable` (`0x9AE15C`, 18B x 4)

実名 `ACNL_Item::s_DropDataTable`（`REFERENCES/TEXTS/drop_method.txt`、実機で確認 F-44）。
従来「フィールドアクション要求キュー」と呼んでいたもの。

| off | 型 | 名前 | 内容 |
|---|---|---|---|
| +0 | ItemID | `ItemToReplace` | 置き換え元（伐採なら木そのもの） |
| +4 | ItemID | `ItemToPlace` | **置き換え先（切り株・切断竹）** |
| +8 | ItemID | `ItemToShow` | 表示用。伐採経路では `g_EmptyItem` |
| +12 | u8 | `wX` | |
| +13 | u8 | `wY` | |
| +14 | u8 | `DropType` | アクションID |
| +15 | u8 | `State` | 0=空き。`Item_PlaceItem` が 1 を書く |
| +16 | u8 | — | スロット番号 |
| +17 | u8 | `Flags` | 下記 |

### `Flags`

```
bit0    IsInside     屋内か
bit1    PlayerSide   AcPlayer+0x2E (s16) > 0。FieldObj_FinalizeRecord が
                     これで kind 4/5 を選ぶ = 倒れる向き
bit2-4  FruitTree
bit5    CrashTree    倒すか。flags & 0x20 が成立すると a2 = ItemToPlace
bit6-7  HitCount     打撃数
```

**空きスロットが無いと `Item_PlaceItem` は -1 を返す。**
使い終わったら `+14`/`+15` を 0 に戻すこと。戻さないと 4 スロットが埋まり、
斧を含む他のアクションが一切効かなくなる（F-42）。

## RTTI とクラス名 (F-43)

| 領域 | 内容 |
|---|---|
| `0x8CD000` - `0x8E5000` | シンボルテーブル（マングル名） |
| `0x8C0000` 台 | `TypeInfo` |
| `0x900000` 付近 | vtable |

```
vtable-8  int        offset_to_top
vtable-4  TypeInfo*  ti          -> +4 が名前、+8 が基底
vtable+0  void*      vmethods[N]      ★ポインタはここを指す
```

マングル名は `_Z` が落ちているだけ。`rtti.py` で引ける。

| アドレス | クラス |
|---|---|
| `0x901EEC` | `fgobj::ObjectSwing`（倒木アクター） |
| `0x901F4C` | `fgobj::ObjectTimer`（結果アイテムのアクター） |
| `0x8F29BC` | `AcPlayer` |
| `0x8F3DD0` | `__cxxabiv1::__si_class_type_info` |

`fgobj::Object*` の継承:
`ObjectExe` → `ObjectBase` → `ssys::st::ListNodePriorityBase` → `ssys::st::ListNode`

## 掘削適用レコード配列

`0x009AE244`（22バイト × 32スロット）。`sub_5A16B0` が空きスロットを探して登録・実行する。

```
sub_5A16B0(char actionID, char playerIdx, int *item0, int *item1, int *item2,
           int X, int Y, int a8, char a9, BYTE *a10)
```

## 木の打撃カウンタ (`0x9AE504`, 2 bit / マス)

`FieldObj_ResolveAxeAction` の `0x597D50`-`0x597D7C` から（asm 由来）:

```
t      = X + 80*Y - 0x510
word   = dword_9AE504[t >> 4]     ; 算術シフト
shift  = (t & 0xF) * 2
打撃数 = (word >> shift) & 3
```

`0x597D80`-`0x597D98` で `必要打撃数 <= 打撃数 + 1` なら `R6 = 1`（倒す）。
必要打撃数は `Item_GetFieldObjDef(item)[13]`。

そのマスだけ一撃で倒したいときは、この 2 bit を 3 にする。

## Catalog家具3Dの主要構造

詳細な生成・resource読込・描画・破棄は `DOCS/furniture_rendering.md`。

### `g_CatalogPreview` (`0x949338`)

| offset | type | 内容 |
|---:|---|---|
| `+0x00` | `AcFtr*` | 現在のpreview actor。未生成・破棄後はnull |
| `+0x04` | `Item` | cached selection。actor生成成否より先に更新される |

### `ItemParam` record

`Item/Param/Item.bin` を `ItemParam_GetRecord` (`0x535188`) が30 bytes刻みで引く。

| offset | type | 内容 |
|---:|---|---|
| `+0x11` | `u8` | 家具actor family。`g_FurnitureActorTypeByFamily` のindex |

model名は別の固定tableから `ItemParam_GetModelName` (`0x535040`) が返す。

### `BsFtrMgr`

RTTI `BsFtrMgr`、vtable `0x8F2BE8`、UiScreen type `0xEE`、size 2240 bytes。

| offset | type | 内容 |
|---:|---|---|
| `+0x13` | `u8` | create flags。下位bit 0=phase 1済み、bit 1=phase 2/3済み |
| `+0x14` | `BankTable` | 最大50 actorのCPU/VRAM bank table |

完全生成済み判定は `(manager[0x13] & 3) == 3`。global `g_BsFtrMgr` (`0x949320`) は
phase 1中に公開されるため、nonnullだけをready判定に使えない。

1 bankはCPU 96000 bytes、VRAM 20500 bytes、VRAM 5500 bytesを持つ。

### `UiScreen` child生成gate

`UiScreen_OpenChild` (`0x51EC58`) はparentに対して次を要求する。

- parentがnonnull
- `parent+0x0F == 0`
- `parent+0x0E != 2`

2026-08-25の精密再読ではactive `ScStage` とsaved `BsMenuTab` は共に
`+0x0E=1 / +0x0F=0` で、このgateを通過する。以前の `ScStage +0x0F=1` という記録は誤り。
両parentでtype `0xEE`が即時失敗した原因はchild gateより後のcreate phaseにある。

### `AcFtr` のCatalog関連field

| offset | type | 内容 |
|---:|---|---|
| `+0x1B4` (`+436`) | model wrapper | phase 3でg3d model instanceを保持 |
| `+0x310` (`+784`) | scene handle | 現在sceneへの登録handle |
| `+0x318` (`+792`) | bank handle | `BsFtrMgr+20` のowner/index |
| `+0x5E4` (`+1508`) | `Item` | preview対象Item |
| `+0x5EC` (`+1516`) | `u8`/mode field | Catalog previewでは2 |
| `+0x5F0` (`+1520`) | `ItemParam*` | 対応parameter record |
| `+0x5F4` (`+1524`) | preview record* | y-offset、scale等 |

Catalog mode 2は生成完了時に全model entryのrender layerを2へ設定する。

## 主要関数

| アドレス | 名前 | 内容 |
|---|---|---|
| `0x002FC878` | `Item_Copy` | 4バイト(u16×2)コピー |
| `0x002FCB24` | `Item_IsEmpty` | ID == 0x7FFE |
| `0x002FCB88` | `Item_IsId` | `(*(u16*)a1 & 0x7FFF) == a2` |
| `0x002FCBA0` | `Item_IsBuriedFlag` | `*(u16*)(item+2) >> 15` |
| `0x002FCBB4` | `Item_InitWithId` | ID指定でアイテム構築 |
| `0x002FCCBC` | `Item_IsFieldObj` | ID <= 0xFD |
| `0x002FCCD4` | `Item_GetCategory` | ID>0xFD なら29、他は 定義[+0x0A] |
| `0x002FD064` | `Item_GetFieldObjDef` | 定義テーブル引き |
| `0x002FE9A8` | `Item_IsGrowableCategory` | カテゴリ ∈ {4,6,8,25} |
| `0x002FE9E4` | `StaticGuardAcquire` | `__cxa_guard_acquire` 相当 (Thumb) |
| `0x002FEE38` | `Field_GetItemAtXY` | `(mapmgr, x, y, 0)` → アイテムへのポインタ |
| `0x00592890` | `FieldObj_InitFallActor` | `(obj, item*, X, Y, kind)` `kind` が演出種別（F-37） |
| `0x00592F8C` | `FieldObj_SpawnFallActor` | `(item*, X, Y, kind, fx)` 倒木アクター生成 |
| `0x00595A8C` | `Player_BeginFieldObjAction` | `(X, Y, mode)` mode2=スコップ |
| `0x00597148` | `FieldObj_ResolveResultItem` | バリエーションIDを基準IDへ正規化 |
| `0x00597CE0` | `FieldObj_ResolveAxeAction` | 斧/木のアクション決定 |
| `0x00598244` | `FieldObj_ResolveDigAction` | 掘るアクション決定 |
| `0x0059A0B4` | `FieldObj_FellObject` | `(a1, a2=残す item*, X, Y, a5, kind, fx)` 伐採本体。**`a2` が空だと `Item_GetFieldObjDef(a1)` の先頭 2 バイトを ID に流用**（F-40） |
| `0x0059BAC4` | `FieldObj_BumpFellCaller` | **ぶつかった／揺すった両方**から呼ばれる。`a2` は `g_EmptyItem` 固定。区別は `kind`（ぶつかる=0 / 揺する=2）（F-40, F-42） |
| `0x005A10AC` | `FieldObj_FinalizeRecord` | レコード完了時に `FieldObj_FellObject` を呼ぶ。`a2` = `item1`、`kind` = `flags` bit1（F-41） |
| `0x0059E5B4` | `Item_PlaceItem` | `ACNL_Item::PlaceItem`。`(DropType, ItemToReplace, ItemToPlace, ItemToShow, wX, wY, IsInside, PlayerSide, FruitTree, CrashTree, HitCount)`（F-44） |
| `0x005A16B0` | `FieldObj_ApplyDigRecord` | 22バイトレコードを登録して実行 |
| `0x005C27D4` | `GetPlayerObject` | `g_PlayerObjects[idx]` |
| `0x0064C688` | `Actor_SetState` | `(actor, stateID, a3, a4)`。記述子を引き BLX で呼ぶ |
| `0x00682994` | `PlayerAction_TryBugNetSwing` | 虫取り網アクション。通常状態 `0x70`、髪型チートは `0xB9` へ差し替え |
| `0x00682F78` | `Player_StartAppearanceChange` | 正規の見た目変更パケットを作り状態 `0xB9` を開始 |
| `0x00687E24` | `PlayerState_AppearanceChangeEnter` | 状態 `0xB9` enter |
| `0x006831B8` | `PlayerState_AppearanceChangeUpdate` | 髪型等の範囲検査と見た目適用 |
| `0x00685738` | `PlayerState_AppearanceChangeSyncLocal` | ローカルプロフィール同期 |
| `0x0068B9F8` | `PlayerState_AppearanceChangeSyncRemote` | リモート受信パケット反映 |
| `0x0068D0EC` | `Actor_PlayAnim` | アニメ再生。S1=速度、S2=ブレンド |
| `0x006A53DC` | `Field_GetMapManager` | 引数なし。`Field_GetItemAtXY` の第1引数 |

## 3DS SVC メモ

| 番号 | 名前 |
|---|---|
| `0x19` | `svcClearEvent` |
| `0x22` | `svcArbitrateAddress` |
| `0x24` | `svcWaitSynchronization1` |
| `0x25` | `svcWaitSynchronizationN` |
