---
id: ACNL-F0724
aliases: []
title: "更新 RomFS は ARCHIVE_ROMFS とファイルパス {5,0,0} で実機から開け、背景の画像 2 枚を読めた（2026-10-20、HIGH（実機の表示＋呼び出しの静的な確認））"
summary: "2026-10-20 の実機で、プラグインから ARCHIVE_ROMFS・ファイルパス {5,0,0} により更新データの RomFS を開き、Layout/Title/opng_titl.arc の背景 2 枚（BCLIM 各 168 バイト）を読めた。ARCHIVE_SAVEDATA_AND_CONTENT は使っていない。"
date: 2026-10-20
category: system
build: acnl_jpn_v15
confidence: HIGH
tool: gohan の実機の状態表示（プラグイン）
addresses: [0x0011D184]
tags: []
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: haiku-5.5
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

- 実機（gohan の開発版、2026-10-20）で、ARCHIVE_ROMFS（ID 3）・空のアーカイブパス `{PATH_EMPTY, 1, ""}`・12 バイトのファイルパス `{5,0,0}` により、更新データの RomFS を開けた。`Layout/Title/opng_titl.arc` の `timg/my_opn_bg_00.bclim`（A4）と `timg/my_opn_bg_01.bclim`（L4）、各 168 バイトを読んで復号できた。背景の出どころは「更新」。
- ゲーム自身が更新データを開く `nnfs_MountUpdateRomfs`（0x0011D184）の引数 `{5,0,0}` と同じ（ACNL-F0509）。F0509 の確度（MEDIUM）を上げる実機の裏付けになる。**F0509 の確度を HIGH に上げる提案**。F0509 自体は書き換えず、判定はオーケストラが行う。
- 確度 HIGH の理由: 実機の表示（利用者の観測）と、gohan の呼び出し引数の静的な確認。「ゲームの開き方と同じ」という同一視だけは F0509（MEDIUM）の静的読みに依る。

## 根拠

- 実機の表示（写しの証拠: `_local/evidence/105/status-and-source.txt` の 1）: 「背景: 更新から取得」「更新: 成功」「本体: 未試行」。
- 呼び出し（gohan main 028adbc の依頼文の版。作業ツリーの各ファイルの SHA256 は証拠ファイルの 2）: `src/game/title_background_self.cpp` の `Try(5)` が上の引数で `FSUSER_OpenFileDirectly` を呼ぶ。更新を先に試し、失敗したときだけ本体（`{0,0,0}`）を試す。`{0,0,0}` は ACNL-F0509 の `nnfs_MountBaseRomfs`（0x001363A0）と同じ形。
- 成功の根拠: 表示の「成功」は `failure == None`。`Try` が真を返すのは、Open・`FSFILE_GetSize`・索引（先頭が IVFC なら level を読み、無ければ 0 から読む）・`timg` の 2 枚の復号（各 168 バイト、CLIM ヘッダの照合）まで通ったとき。「背景: 更新から取得」は `Try(5)` が真のときだけ立つ。
- **表示の `Result=00000000` は、Open の戻り値ではない。** gohan は `attempt.result` を失敗時にだけ書き、既定値は 0。よって「`FSUSER_OpenFileDirectly` が 0 を返した」とは観測していない。戻り値を見るには、表示を変えた実機試験が要る（未実施）。
- ACNL-F0530 との関係: F0530 は `ARCHIVE_SAVEDATA_AND_CONTENT`（0x2345678A）で更新タイトルを開く試みが SD・カード・NAND の 3 通りとも失敗した記録。今回の成功は別の経路（ARCHIVE_ROMFS＋`{5,0,0}`）で、SAVEDATA_AND_CONTENT を使っていない。よって、更新 RomFS を開くのに SAVEDATA_AND_CONTENT が要るという前提は、この結果で要らなくなる。**ただし F0530 の失敗の原因は説明していない**（候補 1〜4 は未確認）。
- ACNL-F0531 との関係: F0531 は「ARCHIVE_ROMFS が返すのは base だけ（8,629 本）」。今回は `{5,0,0}` で更新側が返った。F0531 の本文はファイルパスを書いていない。零のファイルパスで開いた観測なら食い違わない。範囲を絞る訂正が要るかは報告で提案する。

## 反証条件・未確認点

- 反証条件: 表示の「更新: 成功」「更新から取得」が、実は本体の読みだった場合（`Try(5)` が偽で `Try(0)` が真なら、表示は「本体から取得」になるはず）。別の端末・別の入れ方（カード版など）で `{5,0,0}` が失敗する場合。更新の RomFS に `opng_titl.arc` が無く、本体の物だけが読まれていた場合。
- 証拠は利用者の状態表示の写し（上の証拠ファイル）。画面の撮影・IDA・ログは無い。
- `FSUSER_OpenFileDirectly` の戻り値は見ていない（上記）。
- 背景の確保の結果（成功か失敗か）は、依頼文の表示に無い。
- gohan の作業ツリーの版が依頼文の 028adbc と一致するかは未確認（Git を使っていない）。
- 「ゲームの開き方と同じ」は F0509 の静的読みに依る。ゲームの FS セッション（`dword_96EF28`）側での実機確認は無い。
- 本体の読み（`{0,0,0}`）は、今回の表示では「未試行」。
