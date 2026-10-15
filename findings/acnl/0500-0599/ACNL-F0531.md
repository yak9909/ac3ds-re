---
id: ACNL-F0531
aliases:
- IDA-opus-5-F037
title: '`ARCHIVE_ROMFS` が返すのは **base だけ**。8,629 本（2026-09-22、HIGH、実機計測）'
summary: '解析ソフト: IDA / 解析モデル: opus-5。利用者が実機で「一覧を作る」を押した結果。'
date: '2026-09-22'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:3163-3215
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F037: `ARCHIVE_ROMFS` が返すのは **base だけ**。8,629 本（2026-09-22、HIGH、実機計測）

解析ソフト: IDA / 解析モデル: opus-5。利用者が実機で「一覧を作る」を押した結果。

### 1. 数値がそのまま答え

F035 で立てた 3 つの候補のうち、**8,629 = base のみ**だった。

| 見えた本数 | 意味 |
|---|---|
| 1,907 | update のみ |
| **8,629** | **base のみ ← これ** |
| 10,430 | FS が重ねている |

つまり **3DS の FS は更新タイトルの RomFS を重ねて見せない**し、
プロセスの中から `ARCHIVE_ROMFS` を開いても base が返る。
（ゲーム自身が update 側のファイルをどう読んでいるかは**未解明**。T024）

### 2. 見えていなかったもの

update にしか無いパスは **1,801 本**、そのうち**描画できるモデルを持つのが 741 本**:

| 本数 | フォルダ |
|---|---|
| 540 | `Item/Model` |
| 67 | `Npc/Normal/Model` |
| 61 | `Npc/Special/Model` |
| 32 | `MiniGame0/Bg` |

amiibo+ で追加されたアイテムと住民。捨てるには惜しいので、**更新タイトルの RomFS も続けて読む**ようにした。
libctru の `romfsMountFromTitle` と同じ形で、`ARCHIVE_SAVEDATA_AND_CONTENT`（0x2345678A）へ
`{低位 ID, 高位 ID, メディア種別, 0}` を渡す。

- **タイトル ID は走っているプロセスから取る**（`Process::GetTitleID()` の低位＋高位 `0x0004000E`）ので、
  地域を焦き込まない。
- メディア種別は事前には分からないので **SD(1) -> カード(2) -> NAND(0)** の順に試す。
- **失敗しても致命ではない**。base だけで 8,629 本使える。
- **重複は取り除かない。** 両方にあるのは 106 本だけで、一覧に 2 行出る以上の害がない。
  どちらの行を選んでも、実際に読むのはゲームのローダなので同じ結果になる。

通知は `.bcres N 件 (本体A+更新B)` の形で出すので、更新側が開けたかどうかがその場で分かる。

### 3. オフラインの数字との対応

`artifacts/base/romfs.bin` を歩いた結果が **8,629**。実機の報告と**完全に一致**した。
これで `verify_romfs_index.py` の歩き方が実機と同じものを数えていることが裏付けられた
（展開済みツリーの 6,911 ではなく、生イメージの 8,629 が正しい。F035 の 3）。

根拠: 利用者の実機報告（8,629 件）、`tools/models3d/verify_romfs_index.py`、
`work/evidence/models3d/model_catalog.json`、`libctru/source/romfs_dev.c` の `romfsMountFromTitle`。
反証条件: 別の端末・別の入れ方（カード版など）では `ARCHIVE_ROMFS` が別のものを返す。
**未確認: 更新タイトルを開けるかはまだ見ていない。**

