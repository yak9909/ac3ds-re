---
id: ACNL-F0083
aliases:
- F-45
title: F-45 `NCCH/exefs/code.bin` は実機とは別ビルド — アドレスが対応しない — `HIGH`
summary: ExeFS の `.code` は `0x00100000` にロードされ、`.text` / `.rodata` / `.data` が
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1048576
- 9355264
- 5880516
- 5188728
- 5902508
- 5208808
- 5864784
- 5873844
- 5856024
- 5864832
- 9228288
- 9326592
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:2234-2314
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-45 `NCCH/exefs/code.bin` は実機とは別ビルド — アドレスが対応しない — `HIGH`

### 原則

ExeFS の `.code` は `0x00100000` にロードされ、`.text` / `.rodata` / `.data` が
その順で連続して入っている。したがって**ビルドが一致していれば**:

```
仮想アドレス = ファイルオフセット + 0x100000
```

### この `code.bin` では成立しない

`NCCH/exefs/code.bin` は 9,355,264 バイト (`0x8EC000`)。
実機の既知の命令列 6 件をファイル全域から検索したところ、**存在したのは 2 件だけ**で、
しかも含意される base が食い違った。

| 実機 VA | 関数 | ファイル内オフセット | 含意される base |
|---|---|---|---|
| `0x59BAC4` | `FieldObj_BumpFellCaller` | `0x4F2C78` | `0xA8E4C` |
| `0x5A10AC` | `FieldObj_FinalizeRecord` | `0x4F7AE8` | `0xA95C4` |

**2 関数の間隔が違う**:

```
実機 : 0x5A10AC - 0x59BAC4 = 0x55E8
file : 0x4F7AE8 - 0x4F2C78 = 0x4E70
差   : 0x778 バイト（実機側にこの区間だけで 1912 バイト多い）
```

単純なベース差ならこの差は 0 になる。**コードそのものが違う。**

見つからなかった 4 件:
`0x597D50` / `0x59A0B4` / `0x595B18` / `0x597D80` の命令列はファイル全域に存在しない。

### RTTI シンボルテーブルが無い

実機には `0x8CD000`-`0x8E5000` にマングル名が並ぶ (F-43) が、
`code.bin` の同じ位置はポインタ配列で、**マングル名らしき文字列は全域で 0 件**
（正規表現 `N\d{1,2}[A-Za-z_]{2,}...E` で 0 ヒット。
`__cxxabiv1` / `ssys` / `oml` / `typeinfo` も 0 件）。

**F-43 の手法はこのファイルには使えない。**

### ACNL であること自体は確か

Shift-JIS の日本語デバッグ文字列が入っている:

```
AcPlayer::doDeleteFirst() イス専有情報削除しました。MachineID<%d> Frame<%d>
BankTable::~BankKey() closeBank 呼ばれ
```

`sead` が 25 件。マリオカート 7 の文字列 (`Kart` / `Course` / `MarioKart`) は 0 件。
**`romfs/` が別ゲームなのに対し、`exefs/code.bin` は ACNL 日本語版。**
ただし**版かバージョンが実機と違う**（無印 / amiibo+ の別、あるいはアップデート差分）。

### 対処

**実機と同じビルドのイメージを GDB 経由で吸い出す。** `dump_code.py` を用意した。
`0x100000` から未マップに当たるまで読み、`VA = オフセット + 0x100000` になるよう
`NCCH/exefs/code_runtime.bin` へ詰める。

MCP の 30 秒タイムアウトがあるので **1 回の実行で 1.5MB だけ進めて中断する。**
完了するまで繰り返し実行する。途中で止めてもファイルサイズから再開位置を決めるので続きから進む。

**パッチ・コードケーブを当てたまま吸うとその状態が焼き付く。**
素のイメージが欲しいなら先に `PATCHES/cave_tree.py` を uninstall し、`PATCHES/apply_patches.py` を revert する。

### 候補イメージの照合手順

新しい `code.bin` を入手したら、採用する前に必ず次を確認する:

1. 実機の命令列を 5-6 箇所ファイル全域から検索する
2. **全部見つかること**、かつ**含意される base が全部同じ `0x100000` になること**
3. 2 関数の間隔が実機と一致すること

1 箇所だけ一致しても意味がない。**間隔まで見ること。**

---

