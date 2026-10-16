# サウンド（`GardenSound.bcsar` / BGM ストリーム）

対象: `NCCH/romfs v1.5/Sound/`。ツールと出力は `SOUND/` にある。
根拠は F-242 / F-243 / F-244（`RE/FINDINGS.md`）。**confidence: HIGH**
（BCSAR の構造解釈と、CSEQ 側の独立したラベル表・ゲームコードの音 ID の 3 系統が一致。
CSEQ 命令表はラベル境界一致 100.00%）。**ただし合成音の包絡の時定数だけは近似**（第 9 節）。

## 1. 何がどこにあるか

| パス | 中身 |
|---|---|
| `Sound/GardenSound.bcsar` | 33.2 MB。**音の名前・ID・カテゴリの一次情報はすべてここ**。効果音の波形も内包 |
| `Sound/stream/*.bcstm` | BGM 268 本（CSTM / DSP-ADPCM / 2ch）。**romfs 上で既に個別の名前付きファイル** |
| `Sound/asr/JPN/*.bin` | 音声認識（マイク）用の音響モデル 6 本。**音声データではない** |
| `SeData/field/field.bin` | 2,203 B。音そのものではない |

## 2. ★ゲームコードの音 ID = BCSAR の Sound itemId

**`itemId = (type << 24) | index`。type 1 が Sound なので、
`Game::PlaySound(id)` が `Game_PlaySound(0x1000000 + id)` に渡す値は
`0x01000000 | soundIndex` そのもの**（F-242）。

既に `RE/FINDINGS.md` にあった値がそのまま名前に解決し、意味も一致した:

| コード中の値 | = | 名前 | 使われている場面 |
|---|---|---|---|
| 16778777 | `0x1000619` | `SE_ACT_SCOOP_DIG_IN` | スコップで掘る |
| 16778582 | `0x1000556` | `SE_ACT_ITEM_CMN_THROW_OUT` | アイテムのドロップ |
| 16778798 | `0x100062E` | `SE_OBJ_PLANT_CMN_GROW` | 花を植える |
| 16779596 | `0x100094C` | `SE_ACT_MYDESIGN_S_CHANGE` | マイデザイン |

**つまり `SOUND/index/sounds.csv` は「コードで見かけた音 ID → 名前」の逆引き表として使える。**
新しい `Game_PlaySound` の即値を見つけたら、まずここを引くこと。

## 3. 数

| 種別 | 数 | 備考 |
|---|---|---|
| Sound | 4,266 | `seq` 3,960 / `stream` 267 / `wave` 39 |
| SoundSet | 96 | `WSDSET_` 26（→CWSD）/ `SQSET_`・`SEQSET_` 67（→CSEQ）/ その他 3 |
| Bank | 840 | File テーブル上 530。残り 310 は null だが **CGRP 内に実体あり** |
| WaveArchive | 603 | File テーブル上 556、残り 47 は CGRP 内。**唯一 BCSAR 内で無名** |
| Group | 47 | `GROUP_*`。場面ごとのロード単位 |
| Player | 18 | `PLAYER_*`。再生バス（同時発音数・優先度の系統） |
| File | 3,110 | internal 2,484 / external 267 / null 359（null も CGRP から解決可） |
| 波形 (CWAV) | 3,801 | 全部 DSP-ADPCM。合計 35.2 分 |
| CSEQ 内ラベル | 33,344 | シーケンスの名前と開始オフセット |

## 4. カテゴリ

**3 つの軸がある。どれもゲーム自身が持っているもので、こちらの推測ではない。**

### 4.1 名前の階層（`cat1_cat2_cat3`）

| cat2 | 件数 | | cat2 | 件数 |
|---|---|---|---|---|
| `SE_DOU` | 700 | どうぶつ語 | `SE_TV` | 124 |
| `SEQ_BGM` | 595 | | `SE_INSECT` | 79 |
| `SE_FUR` | 549 | 家具 | `SE_MR` | 58 |
| `SE_MELODY` | 506 | | `SE_ENV` | 51 |
| `SE_SYS` | 422 | **UI・システム** | `SE_PNP` | 36 |
| `SE_ACT` | 306 | プレイヤー動作 | `SE_IND` | 35 |
| `STRM_BGM` | 257 | | `SE_RESULT2` | 11 |
| `SE_OBJ` | 215 | | `SE_CUR` | 10 |
| `SE_ESCAPE` | 151 | | `STRM_SE` | 7 |
| `SE_HNW` | 131 | ハニワ | 他 | 各 4 以下 |

**★`SE_CUR_*` は「カーソル」ではなく「カーテン等の開閉家具」**。
`WSDSET_SE_FUR_CURTAIN` が `SE_CUR_CLOSE` / `SE_CUR_OPEN` を担当していることで確定した。
名前の略語から意味を推測しないこと。

UI の音を探すなら `SE_SYS_*`（422 件）を見る。
`SE_SYS_DECIDE` / `SE_SYS_CANCEL` / `SE_SYS_SCROLL_*` / `SE_SYS_WIN_*` などが揃っている。

### 4.2 Player（再生バス）— sound エントリが直接持つ

`PLAYER_DOUBUTSUGO` 702 / `PLAYER_BGM` 637 / `PLAYER_SE_FUR_TRG` 511 /
`PLAYER_SE_MELODY` 505 / `PLAYER_SE_SYSTEM` 504 / `PLAYER_SE_ACT` 321 /
`PLAYER_SE_OBJ` 301 / `PLAYER_SE_HANIWA` 131 / `PLAYER_SE_FUR_LV` 128 /
`PLAYER_SE_TV` 124 / `PLAYER_BGM_MU` 91 / `PLAYER_BGM_RM` 91 / 他 6 種。

**名前の接頭辞と完全には一致しない**（例: `SE_CUR_*` は `PLAYER_SE_FUR_TRG`）。
「どの系統として鳴るか」を知りたいならこちらが正。

### 4.3 Group（場面ごとのロード単位）

`GROUP_STATIC`（常駐）1,346 / `GROUP_HOUSE` 714 / `GROUP_MUSEUM` 495 /
`GROUP_SHOP` 483 / `GROUP_STATION` 397 / `GROUP_VILLAGE` 318 /
`GROUP_AUTOCAMP` 238 / `GROUP_ISLAND` 234 ほか、全 47。
`GROUP_TV_00`〜`GROUP_TV_21` と `GROUP_TV_255` のようにデータ寄りの区分もある。

sound 4,266 件のうち 3,398 件がいずれかの group に属する（残り 868 件は
group 経由でロードされない = 別経路）。

## 5. BCSAR の構造

`SOUND/NOTES_bcsar.md` に全オフセットを書いた。要点だけ:

- セクション `0x2000 STRG` / `0x2001 INFO` / `0x2002 FILE`
- 名前は STRG の patricia trie の葉が `(stringIndex, itemId)` を持つ
- INFO は **ref の並び順**が役割順（sound, soundset, bank, warc, group, player, file）。
  **type code（0x2100/0x2104/0x2101/…）の数値順ではない**ので、code で引くと取り違える
- Sound エントリ: `+0x00 fileIndex` / `+0x04 playerItemId` / `+0x08 volume` /
  `+0x0C Reference{subtype, off}` / `+0x14 flags`。エントリ長は可変（84〜192 B）
- subtype `0x2201 stream` / `0x2202 wave` / `0x2203 seq`
- seq の場合、`a+0x54` = CSEQ DATA 内オフセット、`a+0x60` = bank itemId
- Bank: `+0x14` に `{u32 count, u32 warcItemId[]}`。**WaveArchive の item type は 5**
- CBNK INFO の波形表 = `{u32 count, {u32 warcItemId, u32 waveIndexInWarc}[count]}`
- SoundSet: `+0x00/+0x04` に担当する Sound itemId の範囲、`+0x20` にファイル表

## 6. ★シーケンス名の独立検証（重要）

CSEQ には `LABL`（`0x5001`）セクションがあり、**シーケンス名と DATA 内オフセットを
ゲーム自身が持っている**。BCSAR 側の値と突き合わせた結果（`SOUND/verify.py`）:

| | 件数 |
|---|---|
| 完全一致 | 1,481 |
| **+3 のずれ** | 449 |
| 別シーケンスを指す | 5 |
| 同名ラベルが無い | 2,025 |

**+3 のずれは 449 件すべてで、ラベル位置の 1 バイト目が `0xFE` だった。**
`0xFE` + u16 = AllocateTrack（3 バイト）なので、
**BCSAR の dataOffset は AllocateTrack を読み飛ばした位置を指す**と確定。
delta=0 の側には `0xFE` が 1 件も無く、例外なく分かれる。

残り 5 件（`SE_SYS_WIN_SELECT_ITEM_CLOSE`, `SE_OBJ_FISH_STRUGGLE_HAND`,
`SE_IND_SICK_CLOSE`, `SE_FUR_DARU_MATORYOSIKA_OPEN/CLOSE`）は、
**自分と同名のラベルとは別のシーケンスを鳴らしている**（別名参照・使われないラベルの残骸）。
いずれも BCSAR 側のオフセットは正当なシーケンス命令を指しており、解釈誤りではない。

「同名ラベルが無い」2,025 件は、専用 CSEQ（BGM 1 曲 = 1 ファイル）で
ラベルが `start` 等になっているもの。

## 7. 抽出物（`SOUND/out/`, 約 850 MB）

```
out/files/cseq/  1325 本  .bcseq   シーケンス（UI 音・効果音・内蔵 BGM）
out/files/cbnk/   840 本  .bcbnk   バンク
out/files/cwar/   603 本  .bcwar   波形アーカイブ
out/files/cgrp/    47 本  .bcgrp   ロードグループ
out/files/cwsd/    28 本  .bcwsd   波形サウンドセット
out/se_wav/<cat2>/WARC<NNN>_<BANK名>/NN.wav   3801 本（素材の波形）
out/seq_wav/<cat2>/<名前>.wav                 2839 本（★シーケンスから合成した「その音」）
```

内部ファイルは**参照元から名前を付けている**（bank / group / soundset / warc の名前）。
BCSAR の File テーブル自体はファイル名を持たない。

**★File テーブルが null の 359 件は `CGRP` の中に実体がある。**
`BANK_SE_SYS_COMMON` もこれに該当するので、File テーブルだけ見ると
**UI 音のバンクが「存在しない」ように見える**。`bcsar.file_data()` が両方を吸収する。

## 8. seq 型サウンドの合成（F-243 / F-244）

`SE_SYS_*` `SE_ACT_*` などは seq 型で、**素材の波形だけでは「その音」にならない**。
CSEQ を実行して合成する。出力は `SOUND/out/seq_wav/<分類>/<名前>.wav`
（**2,839 本 / 100.2 分**）。

    python render.py --no-bgm     # BGM を除く seq 型を全部
    python render.py SE_SYS       # 名前が SE_SYS で始まるものだけ
    python dis.py SE_SYS_DECIDE   # 1 つのシーケンスを逆アセンブル

### 命令表はラベル境界で検定して 100.00%

CSEQ の `LABL` が持つ 33,344 個のオフセットは必ず命令境界。
「各ラベルから復号して次のラベルにぴったり着くか」で引数長を決めた。
**ラベル区間 33,319 中 33,318 (100.00%)、復号失敗ゼロ。**

**★「未知の命令」を追う前に、既知の命令の引数長を疑う。**
最初は 99.43% で未知 opcode が 171 件残っていたが、それらは実在しなかった。
`0xF0` の sub `0xE0` だけ引数が 1 バイト短いのに一律で読んでいたための
見かけの誤りで、1 箇所直したら全部消えた。音にも出ていた（`SE_MU_CTRL_GRID_*` が雑音）。

### 素朴に鳴らすと実機と別の音になる

| 命令 | 何が起きるか | 使用率 |
|---|---|---|
| `tie` (0xC8) | ON の間、続く note を**鳴らし直さない**。音程だけ変わる | 12.5% |
| `porta_key` (0xC9) | ポルタメント。**`porta_time`=0 なら音符の長さ全体で滑る** | 14.6% |
| ADSR (0xD0-0xD3) | 音量包絡。既定値は**楽器側**（CBNK の葉 +0x28..+0x2C） | 最大 28.5% |
| variable 接頭辞 (0xA1) | 最後の引数は**値ではなく変数番号** | — |

- `SE_ACT_ITEM_CMN_PICK_UP` = `porta_key 33` → `note 83` の上昇スイープ
- `SE_ACT_SCOOP_DIG_OUT_ITEM` = `tie 1` で 9 個の note が 1 つの音に繋がる
- **note の長さ 0 = ノートオフ無し**（サンプル終わりまで鳴る）

### 合成しなかった 526 件は正当

`note` を 1 つも持たない制御用シーケンスが 521 件。`SE_MELODY_*` 489（村メロ =
実際の音符はセーブデータ側）、`SE_MU_CTRL_*` / `SE_DJ_CTRL_*`（音楽プレイヤーの制御）など。

## 9. できていないこと

- **包絡の時定数は近似。** 0..127 → 速度の変換は任天堂系で共通の形を使ったが、
  実機の変換表そのものではない。耳で確かめて調整する余地がある。
- `ex`（0xF0）の sub の**意味**は未確定（引数長は確定済みなので復号は正しい）。
  条件分岐の判定だけが近似で、変数分岐に依存する音は経路が実機と異なりうる。
- 合成結果のうち 46 本 (1.6%) が無音同然。未調査。
- **1 つの効果音 ↔ 1 つの波形の対応**は `index/waves.csv` では付けていない。
  同 CSV の `sounds` 列は「その warc を使うバンクを使う音の一覧」であって、
  「この波形がその音である」という意味ではない。
  ただし合成側（`render.py`）は program → スロット → 波形を実際に引いている。
- BGM の `.bcstm` は変換していない（利用者の指定）。`SOUND/bcstm.py` で
  いつでも WAV 化できる（検証済み）。`STRM_BGM_PROLOGUE_12.bcstm` だけは
  romfs にあるが BCSAR から参照されていない。
- `SEQ_BGM_*` 595 曲は同じ仕組みで出せるが未実施。

## 10. 使い方

```
cd SOUND
python extract.py            # 抽出 + 索引（約 40 秒）
python extract.py --index    # 索引だけ
python verify.py             # 20 項目の整合チェック
python bcstm.py info  <f.bcstm>
python bcstm.py wav   <f.bcstm> <out.wav>
```

索引: `SOUND/index/` に `sounds.csv`（4,266 行・音 ID 逆引きの本体）、
`waves.csv` `banks.csv` `warcs.csv` `groups.csv` `players.csv` `soundsets.csv`
`streams.csv` `sequences.csv`（33,344 行）、`sounds.json`。

## シーケンスの合成（`out/seq_wav/`）

全 3,434 件（BGM 595 + 効果音 2,839）。`SOUND/index/rendered.csv` が索引。

```
cd SOUND
python render.py                      # 全件（約 7 時間）
python render.py SE_SYS               # 接頭辞で絞る
python render.py --names=list.txt     # 名前の一覧で絞る（処理を直したときの差分用）
python render.py --no-bgm             # BGM を除く
python dis.py SE_SYS_DECIDE           # 1 件を逆アセンブル
```

### 音量の換算（F-249）

`volume` / `expression` / `velocity` は **振幅の 2 乗側**。dB では `40*log10(v/127)`。
`synth.VOL_POW = 2.0`。音量ランプは**生の 0-127 の上で補間してから**振幅へ直す
（`synth.RAMP_SQUARE_FIRST = False`）。
tie で繋がった音の途中ではベロシティを効き直さない（`render.VEL_PER_NOTE = False`）。
**2 乗を入れる前の状態は `SOUND/backup/linear_vol/` にある**（音まで md5 一致で再現可）。

### 音符 0 で書き出されない 526 件（F-250）

| 内訳 | 件数 | 理由 |
|---|---|---|
| `SE_MELODY_*` | 489 | 村メロ。旋律が外部データで、シーケンスに音符が無い |
| `SE_SYS_SILENT` ほか制御用 | 37 | `SE_MU_CTRL_*` `SE_DJ_CTRL_*` など。音符を持たない |

`0xBC`-`0xBF` の比較は、シーケンスが設定していない変数に対しては判定を変えない
（`synth.UNSET_CMP_NEUTRAL`）。これを入れないと K.K. の曲 186 件が丸ごと無音になる。
