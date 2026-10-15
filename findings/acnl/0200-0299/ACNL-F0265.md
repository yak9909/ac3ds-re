---
id: ACNL-F0265
aliases:
- F-242
title: 'F-242: `GardenSound.bcsar` を解読し、全 4,266 音の名前・ID・カテゴリを確定 — `HIGH`（独立 3 系統の一致）'
summary: '`NCCH/romfs v1.5/Sound/GardenSound.bcsar`（33.2 MB, `CSAR`）を静的に解読した。'
date: '2026-09-01'
category: sound
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:14182-14269
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-242: `GardenSound.bcsar` を解読し、全 4,266 音の名前・ID・カテゴリを確定 — `HIGH`（独立 3 系統の一致）

`NCCH/romfs v1.5/Sound/GardenSound.bcsar`（33.2 MB, `CSAR`）を静的に解読した。
ツールは `SOUND/`（`bcsar.py` / `bcwav.py` / `bcstm.py` / `extract.py` / `verify.py`）。
確定内容の全文は **`DOCS/sound.md`**、全オフセットは `SOUND/NOTES_bcsar.md`。

### 最重要: ゲームコードの音 ID がそのまま引ける

BCSAR の itemId は `(type << 24) | index` で、type 1 が Sound。
したがって `Game::PlaySound(id)` → `Game_PlaySound(0x1000000 + id)` に渡る値は
**`0x01000000 | soundIndex` そのもの**。

既に本解析で記録済みだった 4 つの即値が、名前でも意味でも一致した:

| 記録済みの値 | 名前 | 記録済みの場面 |
|---|---|---|
| 16778777 = `0x1000619` | `SE_ACT_SCOOP_DIG_IN` | スコップで掘る |
| 16778582 = `0x1000556` | `SE_ACT_ITEM_CMN_THROW_OUT` | ドロップ |
| 16778798 = `0x100062E` | `SE_OBJ_PLANT_CMN_GROW` | 花植える |
| 16779596 = `0x100094C` | `SE_ACT_MYDESIGN_S_CHANGE` | マイデザ |

**これは BCSAR の構造解釈が正しいことの独立証拠**（アーカイブ側だけでは検証できない）。
以後、`Game_PlaySound` の即値は `SOUND/index/sounds.csv` で逆引きすること。

### 独立検証その 2: CSEQ の `LABL` セクション

CSEQ（`0x5001 LABL`）はシーケンス名と DATA 内オフセットを自前で持つ。
BCSAR 側の値と全件突き合わせた結果:

- 完全一致 1,481
- **+3 ずれ 449 — 449 件すべてでラベル位置の 1 バイト目が `0xFE`**
- 別シーケンスを指す 5
- 同名ラベル無し 2,025（専用 CSEQ で名前が `start` 等）

`0xFE` + u16 は AllocateTrack（3 バイト）。すなわち
**BCSAR の dataOffset は AllocateTrack を読み飛ばした位置を指す**。
delta=0 側には `0xFE` が 1 件も無く、例外なく二分される。
残り 5 件は自分と同名のラベルとは別のシーケンスを鳴らすもの（別名参照・残骸）で、
オフセット自体は正当なシーケンス命令を指しており解釈誤りではない。

### 構造で誤りやすい点

- **INFO の 8 本の ref は「並び順」が役割順**（sound, soundset, bank, warc, group, player, file）。
  type code は `0x2100, 0x2104, 0x2101, 0x2103, 0x2105, 0x2102, 0x2106` の順で並んでおり、
  **数値順に対応付けると bank と soundset を取り違える**。件数と名前（`BANK_*` / `WSDSET_*`）で裏を取った。
- **WaveArchive の item type は 5**。603 本あるが **BCSAR 内で唯一名前を持たない**。
  bank（`+0x14` の `{count, warcItemId[]}`）と CBNK の波形表、および
  WSDSET の `0x2205` ブロックから参照元を辿ると 603 本すべてに名前が付く
  （bank 経由 577 + WSDSET 直参照 26）。
- external ファイル参照（`0x220D`）は**長さ接頭辞を持たないヌル終端文字列**。
  長さ付きと誤読すると巨大スライスで固まる。
- File テーブルの 359 件は `offset/size = 0xFFFFFFFF` の null エントリ。

### 数と抽出物

Sound 4,266（seq 3,960 / stream 267 / wave 39）、SoundSet 96、Bank 840、
WaveArchive 603、Group 47、Player 18、File 3,110。
内部ファイル 2,484 を magic 別に抽出（CSEQ 1,325 / CBNK 530 / CWAR 556 / CGRP 47 / CWSD 26）、
CWAR 内の CWAV 1,601 本を DSP-ADPCM から復号して WAV 化（合計 14.9 分、全部モノラル or 2ch の 3DS 標準 ADPCM）。
`SOUND/verify.py` の 16 項目がすべて通る。

### カテゴリは 3 軸あり、いずれもゲーム自身が持っている

1. 名前の階層（`SE_SYS_*` 422 = UI、`SE_ACT_*` 306 = 動作、`SE_FUR_*` 549 = 家具 など 27 分類）
2. **Player**（`PLAYER_*` 18 本の再生バス。sound エントリが直接持つ）
3. **Group**（`GROUP_*` 47。場面ごとのロード単位。4,266 中 3,398 音が所属）

**名前の接頭辞と Player は一致しない。** 例: `SE_CUR_*` は `PLAYER_SE_FUR_TRG`。

### ★略語から意味を推測しない

`SE_CUR_*` は **cursor ではなく curtain**（カーテン等の開閉家具）。
`WSDSET_SE_FUR_CURTAIN` が `SE_CUR_CLOSE`/`SE_CUR_OPEN` を担当していることで判明した。
SoundSet エントリの `+0x00/+0x04` が担当 Sound itemId の範囲なので、この対応は機械的に取れる。

### まだ確定していないこと

- **1 効果音 ↔ 1 波形の対応**。bank → 波形スロット → `(warc, waveIndex)` までは取れるが、
  シーケンスのどのプログラム番号がどのスロットを選ぶかは CSEQ バイトコードを読む必要がある。
  `index/waves.csv` の `sounds` 列は「その warc を使うバンクを使う音の一覧」であり、
  **「この波形がその音である」という意味ではない**。
- **シーケンスの合成（曲としての書き出し）**は未実施（TODO-135）。
- BGM の `.bcstm` 268 本は変換していない（利用者指定）。`SOUND/bcstm.py` で
  いつでも WAV 化できる（部分デコードで波形の妥当性は確認済み）。
  `STRM_BGM_PROLOGUE_12.bcstm` は romfs にあるが BCSAR から参照されていない。

---

