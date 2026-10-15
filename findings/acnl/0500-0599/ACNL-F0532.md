---
id: ACNL-F0532
aliases:
- IDA-opus-5-F036
title: RomFS の開き方を 3 箱所間違えていた（2026-09-22、HIGH、実機＋libctru ソース）
summary: '解析ソフト: IDA / 解析モデル: opus-5。利用者報告:「一覧を作るを押すと'
date: '2026-09-22'
category: system
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:3216-3273
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F036: RomFS の開き方を 3 箱所間違えていた（2026-09-22、HIGH、実機＋libctru ソース）

解析ソフト: IDA / 解析モデル: opus-5。利用者報告:「一覧を作るを押すと
『RomFS が開けません 0xE0E046BE』」。

### 1. Result コードがそのまま答えだった

| 欄 | 値 |
|---|---|
| description | 702 |
| **module** | **17 = FS** |
| **summary** | **7 = invalid argument** |
| level | 28 |

「権限が無い」でも「見つからない」でもなく、**渡した引数が不正**。

### 2. libctru の実物と照らして 3 箱所

`C:/devkitPro/libctru/source/romfs_dev.c` の `romfsMountFromCurrentProcess`:

```c
u8 zeros[0xC] = {0};
FS_Path archPath = { PATH_EMPTY, 1, "" };
FS_Path filePath = { PATH_BINARY, sizeof(zeros), zeros };
FSUSER_OpenFileDirectly(&fd, ARCHIVE_ROMFS, archPath, filePath, FS_OPEN_READ, 0);
```

| こちらが書いていたもの | 正しいもの |
|---|---|
| archPath = `{PATH_EMPTY, 0, nullptr}` | `{PATH_EMPTY, **1**, **""**}` |
| filePath = `{PATH_EMPTY, 0, nullptr}` | **`{PATH_BINARY, 12, ゼロ 12 バイト}`** |
| 先頭に IVFC を要求 | **IVFC は付いてこない** |

3 つ目が一番大事。`romfsMountFromFile` は `_romfs_read(mount, 0, &mount->header, ...)` で
**オフセット 0 から 40 バイトヘッダを読んでいる**。つまり
**`ARCHIVE_ROMFS` で開くと FS が既に IVFC を剥いて level 3 を渡してくる**。
`artifacts/*/romfs.bin`（生のパーティション）とは形が違うので、オフライン検証だけでは気付けない。
両方受ける形にした（先頭が IVFC なら level 3 へ飛ぶ、そうでなければ 0）。

ヘッダの形は libctru の `romfs.h` とも照合済み: **`u32` 10 個**、
ディレクトリ項 24 B、ファイル項 32 B、名前は UTF-16。こちらの読み方と一致。

### 3. 検証器を libctru のソースへ繋いだ

`tools/models3d/verify_romfs_index.py` は `romfs_dev.c` と `romfs.h` をその場で読み、
**プラグインの引数の形が libctru と同じかを比べる**（全 20 検査）。
記憶で書いた値を検査にも写すと両方同じだけ間違うので、**権威の側を読む**。

なお、この回の検証器に一つ `or True` を混ぜてしまい、**常に真になる検査**を
書いていた。見つけて直したが、検査を書くときは**落ちることを一度確かめる**こと。

根拠: 利用者の実機報告の Result コード、
`C:/devkitPro/libctru/source/romfs_dev.c` と `include/3ds/romfs.h`、
`tools/models3d/verify_romfs_index.py`（20 検査 PASS）。
反証条件: このビルドの libctru と実機の FS の振る舞いが違う、
プラグインのプロセスでは `ARCHIVE_ROMFS` に別の制約がある。
**未確認: 直したものはまだ実機で走らせていない。**

