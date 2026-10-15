---
id: ACNL-F0530
aliases:
- IDA-opus-5-F038
title: 更新タイトルの RomFS は開けなかった（2026-09-22、HIGH（事実）、原因は未解明）
summary: '解析ソフト: IDA / 解析モデル: opus-5。利用者の実機報告：'
date: '2026-09-22'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:3118-3162
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F038: 更新タイトルの RomFS は開けなかった（2026-09-22、HIGH（事実）、原因は未解明）

解析ソフト: IDA / 解析モデル: opus-5。利用者の実機報告：
「8629件でした。**本体8629+更新0**」。

### 1. 確かなこと

`ARCHIVE_SAVEDATA_AND_CONTENT`（0x2345678A）へ **SD(1) / カード(2) / NAND(0) の 3 通りを試して
すべて失敗**した（成功していれば 741 件以上増えるはず）。
base 側は 8,629 件で F037 の通り動いているので、**歩き方や表の読み方の問題ではなく、
開けていない**。

### 2. こちらの設計ミス: 理由を見る手段が無い

`RomfsIndex::UpdateOpenResult()` に Result を残してはあるが、**どのメニュー項目もそれを出していない**。
だから今回は「開けなかった」としか分からない。
F031 で「失敗ではない停止は通知が出ない」と同じ罠を、**別の場所で踏み直している**。
次にやるのは直すことではなく、**まず Result を見せること**（T025）。

### 3. 候補（いずれも未検証。前提にしないこと）

1. **FS のアクセス権**が足りない。他タイトルの content を読むには exheader の
   ARM11 FS アクセス情報にそのビットが要る。**`artifacts/update/exheader.bin` を読めば静的に分かる**。
   ただし漢字変換は同じアーカイブで**システムタイトル**（0x0004009B00011902）を開けているので、
   アーカイブ自体が禁じられているわけではない。**対象タイトルによって違う**可能性が高い。
2. **タイトル ID の導き方**が違う。`Process::GetTitleID()` の低位 32 bit に
   高位 `0x0004000E` を載せているが、走っているタイトル ID が既に更新側だったとしても
   低位は同じなので値は合うはず。**実際の値を見ていない**ので話半分。
3. **更新が別の入れ方をしている**。そもそもこの端末に更新タイトルが
   インストールされていない可能性。ただしこのビルドは更新版なので、
   何らかの形で入っているはず。
4. `FS_OPEN_READ` 以外の引数が違う。libctru の `romfsMountFromTitle` と
   同じ形にしてあるが、**検証器はそこまで見ていない**（見ているのは
   `romfsMountFromCurrentProcess` 側だけ）。

### 4. 影響

**機能としては困らない。** base だけで 8,629 本、`Item/Model` 2,956 本を含む主要なフォルダは全部ある。
見えないのは amiibo+ で追加された 741 本（アイテム 540、住民 128）だけ。

根拠: 利用者の実機報告（2026-09-22）、
`src/gohan/Sources/Cheats/RomfsIndex.cpp` の `Build()`、
`libctru/source/romfs_dev.c` の `romfsMountFromTitle`、IDA-opus-5-F037。
反証条件: Result を見たら全く別の原因だった、別の端末では開ける。

