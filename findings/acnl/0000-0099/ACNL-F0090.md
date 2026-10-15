---
id: ACNL-F0090
aliases:
- F-52
title: F-52 静的解析の本体を `code.bin.i64` に移した — `HIGH`
summary: ユーザーが持ち込んだ `code.bin.idb`（IDA が `code.bin.i64` へ自動アップグレード）を
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1048576
- 5671928
- 5859472
- 5864796
- 5873844
- 5880516
- 5902508
- 6259320
- 6270824
- 6967992
- 5859388
- 6967988
- 6680400
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:2855-2923
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-52 静的解析の本体を `code.bin.i64` に移した — `HIGH`

ユーザーが持ち込んだ `code.bin.idb`（IDA が `code.bin.i64` へ自動アップグレード）を
idalib-mcp の**セッション `acnl_code`** として常用することにした。

| 項目 | 値 |
|---|---|
| IDB | `A:\Disassemble\acnl\code.bin.i64` |
| セッションID | `acnl_code` |
| 元の入力 | `<USER>\Downloads\ac\exefs\code.bin`（別の人のダンプ） |
| `imagebase` の表示 | `0x0` |
| **実際のアドレス** | **我々の実行時 VA と同一**（`0x100000` 起点） |

### 【重要】`NCCH/exefs/code.bin` とは別物

F-45 で「`NCCH/exefs/code.bin` は別ビルドで使えない」と結論したが、
**今回の `code.bin` はそれとは違うファイルで、実機と同一ビルドだった。**
同じ `code.bin` という名前なので混同しないこと。

### 検証（F-45 の手順どおり）

`imagebase` が `0x0` と報告されるので、まず「ファイルオフセット = VA - 0x100000」で
読んだところ **14 件すべて不一致**。次に**我々の VA でそのまま**読むと:

| アドレス | 値 | 内容 |
|---|---|---|
| `0x568BF8` | `3F800000` | `g_UiAnimRate` |
| `0x596890` | `EBF5990F` | `BL Item_GetCategory` |
| `0x597D5C` | `E2400E51` | 打撃カウンタ index |
| `0x59A0B4` | `E92D4FFF` | `FieldObj_FellObject` |
| `0x59BAC4` | `E92D43F0` | `FieldObj_BumpFellCaller` |
| `0x5A10AC` | `E92D40F0` | `FieldObj_FinalizeRecord` |
| `0x5F8278` | `E5D400CA` | 一気に表示フラグ |
| `0x5FAF68` | `EBFFF4B2` | `BL TalkSeq_StepText` |
| `0x6A52B8` | `E1A05000` | `Fader_SetKind` |

**10/10 一致。** さらに自動解析後の関数サイズも
`0x59683C`=`0x19C` / `0x59A0B4`=`0x3D8` / `0x6A52B4`=`0xC4` と
`code_runtime.elf.i64` 側と完全に一致した。**同一ビルド確定。**

**`imagebase` の表示を信じず、実際のアドレスで照合すること。**

### 移行した内容

| 種別 | 件数 |
|---|---|
| 関数のリネーム | 103 |
| グローバルの名前＋型 | 45 |
| 関数プロトタイプ | 12 |
| コメント | 67（`0x65EF50` の decompiler コメントのみ失敗。データ領域のため） |
| struct | 7（`ItemID` `DropData` `DigRecord` `FieldActionActive` `FieldObjDef` `UiAnim` `FaderBase`） |
| enum | 5（`DropFlags` `FieldObjCategory` `MsgStreamCode` `FallActorKind` `FaderKind`） |

集約データは `scratchpad/symbols.json` / `comments.json` / `protos.json`。
`ida_restore.py` から機械的に吸い出す手順は `scratchpad/extract_comments.py`
（IDA モジュールをスタブに差し替えて exec する）。

### idalib の落とし穴

- **`rename` の `data` はアドレスを受け付けない。** `old` は「現在の名前」
  （`dword_9AE15C` など）でなければならず、新規 IDB では予測できない。
  **代わりに `type_apply_batch` で `addr` + `name` + `ty` を同時に指定する。**
  `ty` は必須（省略すると "Type text is required"）。
- `idb_open` に `run_auto_analysis=false` を渡すと関数が定義されず
  `lookup_funcs` が "Not a function" を返す。**必ず `true` で開く**（9MB で約 5 分）。
- 解析はバックグラウンドに落ちるので、完了通知を待ってから作業する。

---

