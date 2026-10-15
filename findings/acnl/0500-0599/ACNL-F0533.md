---
id: ACNL-F0533
aliases:
- IDA-opus-5-F035
title: モデルの一覧は ROM から読める。8,818 本の .bcres とその検算（2026-09-22、HIGH、静的）
summary: '解析ソフト: IDA / 解析モデル: opus-5。利用者の問い「ROMに名前群が存在する可能性はないですか？」への答え。'
date: '2026-09-22'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags:
- model
supersedes: []
source: IDA:work/FINDINGS.md:3274-3350
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F035: モデルの一覧は ROM から読める。8,818 本の .bcres とその検算（2026-09-22、HIGH、静的）

解析ソフト: IDA / 解析モデル: opus-5。利用者の問い「ROMに名前群が存在する可能性はないですか？」への答え。

### 1. 結論: 読める。しかも gohan に実績のある経路

ゲームは `Item/Model/%s.bcres` のような**書式文字列＋名前表**でパスを組んでいる
（`code.bin` に `%s.bcres` が 24 箱所、`.bcres` を含む文字列が 462 箱所）。
名前表はカテゴリごとに別形式で散在しており、全部を特定するのは新規解析が相当量になる。

しかし **RomFS のディレクトリ表そのもの**を読めば、全ファイルが網羅的に出る。
gohan は漢字変換で既に `FSUSER_OpenFileDirectly` と romfs のディレクトリ表を扱っており
（`Includes/ChatKanji/NativeFsApi.hpp` / `Sources/ChatKanji/Engine.cpp` の `RomFs`）、
**利用者確認済みの仕組み**。自分自身の RomFS なら `ARCHIVE_ROMFS`（ID 3）を
`PATH_EMPTY` で開けばよく、タイトル ID もメディア種別も要らない。

埋め込む場合との比較:

| 方式 | 3gx に載る量 |
|---|---|
| パス＋モデル名を素で | 253,284 B |
| フォルダを括り出し、モデル名は実行時に CGFX から | 104,624 B |
| **RomFS を実行時に列挙** | **0 B** |

実際のビルドの増分は **19 KB**（936,246 -> 955,468 B）。これはコードの分だけ。

### 2. RomFS の実寸（`artifacts/*/romfs.bin` をその場で歩いて計測）

| | update | base |
|---|---|---|
| .bcres | 1,907 | **8,629** |
| ディレクトリ表 | 4,408 B | 42,648 B |
| ファイル表 | 301,956 B | 940,716 B |
| パスの置き場 | 74,709 B | 336,906 B |
| 歩行中のピーク | 388,701 B | **1,354,786 B** |
| 最長パス / 木の深さ | 56 / 4 | 75 / 6 |

update にしか無いパスが **1,801 本**、両方の和集合は **10,430 本**。
実機で `ARCHIVE_ROMFS` がどれを見せるかは**数えるまで分からない**ので、
プラグインは見つけた本数をそのまま通知へ出す。1,907 / 8,629 / 10,430 のどれかになる。

### 3. 抽出済みのツリーは不完全だった

`artifacts/base/romfs/` に展開されている .bcres は **6,911 本**だが、
生イメージを歩くと **8,629 本**ある。**1,718 本が展開されていない**
（`Strc/Shadows/*`、`Strc/dobj/*` など）。
**romfs 全体の調査は `romfs.bin` を直接歩くこと。** 展開済みのツリーだけを見て
「存在しない」と言わない。

### 4. 歩き方で踏んだ罠（検証器が捕まえた）

子ディレクトリを**兵弟まとめてスタックへ積む**書き方にすると、スタックの深さが
木の深さではなく**フロンティアの幅**になる。ルート直下が 40 個あるので 32 で溢れ、
`Shader` / `Shadow` / `Sound` などが**フォルダごと黙って落ちていた**（update で 57 本、base で 77 本）。
子と兵弟の鎖をそのまま辿り、スタックには**先祖だけ**を積む形へ直した。
実機へ行く前に `tools/models3d/verify_romfs_index.py` が見つけた。

### 5. モデルの中身

`tools/models3d/catalog_models.py` で展開済みツリーを解いた結果（参考値。上記 3 の取りこぼしを含む）:

- 描画できるモデルを持つファイル **4,413**、モデル **8,788**（うち SkeletalModel **1,970**）
- 骨アニメを持つファイル 896、マテリアルアニメ 238
- 1 つのファイルにモデルが 2 つ以上入っているのは 140 ファイルだけ
- ファイルの大きさは中央値 16,768 B、p99 219,776 B、**最大 5,535,872 B**

**親ヒープの空きは 500 KB ほどしかない**（V2-F023 / T020）ので、資源ヒープは固定値にできない。
romfs のファイル表にバイト数が入っているので、**それから `size*2 + 16 KiB` で決める**。
入らない大きいモデルは `kResourceHeap` で理由付きに断る。

根拠: `tools/models3d/verify_romfs_index.py`（12 検査 PASS、`work/evidence/models3d/romfs_index_check.json`）、
`tools/models3d/catalog_models.py`（`model_catalog.json`）、`artifacts/{update,base}/romfs.bin`、
`src/gohan/Sources/ChatKanji/Engine.cpp` の `RomFs`。
反証条件: 実機の `ARCHIVE_ROMFS` が開けない、見えるのが上記どの本数でもない、
プラグインのヒープに 1.4 MB のピークが取れない。
**未確認: 実機ではまだ 1 回も走らせていない。**

