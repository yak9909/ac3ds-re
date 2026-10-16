---
id: ACNL-F0702
aliases: []
title: "Fade とロード画像の登録順・状態別の描画元（再解析）"
summary: "Fade と BlackWait の loader は優先度0xFFを共有し、確認した更新経路ではFadeが先に登録される。loaderの登録有無は状態、画像資源は種類欄で変わる。"
date: 2026-10-16
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0x1b6b84, 0x5292dc, 0x52958c, 0x6ce2c0, 0x6a9114, 0x6cd9b0, 0x6cdc54, 0x6cde8c, 0x6cdac0, 0x6ce0b8, 0x6ce404, 0x845fec, 0x4d6c90]
tags: [layout]
supersedes: ["ACNL-F0259"]
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: auto
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

再解析で確認。Fade より後に loader が再生され得るのは、ID の大小によらず、同じ優先度 `0xFF` と登録順で説明できる。確認した更新関数では Fade の上下 Layout を先に登録し、後で BlackWait の状態更新が選択中の loader Layout を上リストへ登録する。両者がそのリストに残る場合、loader は上 Fade より後になる。全場面の最後の Layout・最前面画素の保証ではない。

BlackWait の `Idle` / `DispWait` は loader を登録せず、`Disp` / `CompelDisp` が種類欄に応じた一つを登録する。状態（表示段階）と種類（どの画像を選ぶか）は別の軸である。

確度 MEDIUM：登録側の命令と安定昇順挿入・再生側 [ACNL-F0694]、状態表の実データと遷移・資源生成側が独立に整合する。実機操作はしていない。

## 根拠

一次証拠：`_local/evidence/26/ida-primary.txt`、`ida-followup.txt`、`ida-states.txt`、`ida-phases.txt`、`ida-final-evidence.txt`。既存コメント・関数名を証拠とせず命令・参照先データを読んだ。疑似Cには旧型による引数の省略があるため screen と容量は呼出し命令で確認した。

### Fade と loader の順序

- Fade の二個体は `0x529398` で生成され、`0x52943C/444` は screen=0、`0x5294D4/D8` はscreen=1を初期化へ渡す。Layout は object `+0x24`。`0x529638/63C` がその `+0x0C` に `0xFF` を書く。ID は Build→ID生成から得るので、8/9を即値で固定するコードではない。
- 更新 `0x1B6B84` は `global[0x9483D8]+0xFAE==0` のとき `0x1B6C78/84` で上下の `0x5292DC` を呼ぶ。同関数 `0x529360..394` は状態処理後、Layoutをscreen=0/1へ登録する。アイドルでも登録部分は通る。
- 同じ更新の後方 `0x1B6D14` が BlackWait 更新 `0x6CE404` を呼ぶ（途中に `byte_9563E8` のゲートあり）。`0x6CDC1C` と `0x6CE12C` は loader 登録の screen=0。`0x6A91C0/C4` は全loaderの優先度を `0xFF` にする。
- 同値は後からの登録が後ろになる [ACNL-F0694]。したがって上記経路で両方を登録し、再生までリンクが保たれれば Fade→loader。全更新ゲート・後続登録・リスト変更まで無条件に固定するものではない。

### 状態ごとの登録と遷移

`0x845FEC..0x846038` は名前・enter関数・update関数からなる4行の表。`0x81B208` はupdate関数をキーに行を探し、object `+0x0C/+0x10` を切替えてenterを呼ぶ。`0x6CE404` が現在のupdateを実行する。

| 状態名 | enter / update | この経路の新規画像源・登録 | 遷移の根拠 |
|---|---|---|---|
| Idle | `0x6CDD9C` / `0x6CDC54` | loader登録なし。enterはアニメ結合等を変更 | Fader条件関数`0x565464`が真、`+0xA13/+0xA11==0`、`global[0x9483D8]+0xFB0==0`ならDispWaitへ |
| DispWait | `0x6CDFEC` / `0x6CDE8C` | loader登録なし。enterでtickを保存 | Fader条件偽または`+0xA13/+0xA11!=0`ならIdleへ。経過量の比較後Dispへ。`+0xFB0!=0`中は基準tickを更新 |
| Disp | `0x6CDCB0` / `0x6CDAC0` | `+0xA12<5`なら選択Layoutのloopを進め、`+0xFB0==0`なら計算・上登録 | Fader条件偽または`+0xA13/+0xA11!=0`、かつ`+0xA10!=1`の場合、経過量条件を満たすとIdleへ |
| CompelDisp | `0x6CE13C` / `0x6CE0B8` | Dispと同じ選択・計算・上登録 | `+0xA10!=1`ならIdleへ。`0x6CE404`末尾は`+0xA10==1`でこの状態へ切替 |

- `0x565464` は選択中の上下 Fader の vslot `+0x0C` が共に0（またはnull）のとき真。単に「画面が黒い」を検査する関数ではない。
- DispWait の比較値は種類2/3=`0x342`、4=`0x3E8`、その他=`0x7D0`。Disp離脱側は種類3=`0x7D0`、その他=`0x3E8`。tick差からの換算と比較が存在することを確認したが、旧標本をこの時間軸へ割り当てたものではない。
- 更新末尾は状態を実行した**後**に `0x6CD9B0` で種類を更新する。状態遷移・種類変更・リスト再生・画面表示は同時の出来事とは限らない。

### 各種類の資源の出どころ

`0x6CE2D0/D8` は `Layout/common/save_wait.arc` を BlackWait `+0x34` の資源保持体へ読み込む。実データ `0x845FD8..0x845FE8` とループ `0x6CE30C..348` は以下の順で5個体を生成する。`0x6A9114` は `%s.bclyt` / `%s_loop.bclan` を組み、同じ保持体でBuild・アニメLoadを行い、`G_loop` を取得する。

| 種類 `BlackWait+0xA12` | Layout先頭（BlackWaitから） | bclyt / loopの基底名 | 記録容量 |
|---|---|---|---|
| 0 | `+0x27C` | `load_wait` | `0x1000` |
| 1 | `+0x3F4` | `load_wait_b` | `0x1000` |
| 2 | `+0x56C` | `load_wait_w` | `0x1000` |
| 3 | `+0x6E4` | `load_wait_p` | `0x1500` |
| 4 | `+0x85C` | `load_wait_h` | `0x1000` |

- `0x6CE350..35C` は別途 `load_wait_kind.bclan` を読み込む。各enterは条件付きで種類0にこのアニメのframe 0を適用してからloopを結合する。
- 種類更新 `0x6CD9B0`：次room=`0xA5`なら維持。現在/次roomのflags `0x20000|0x200000` がどれか真なら1。そうでなく現在roomが`0x9D/0x9E`なら4、次room=`0x9D`なら2、`0x9E`なら3、それ以外0。この優先順位は命令 `0x6CD9BC..0x6CDA98` による。各roomの実画面上の名称はここでは付けない。
- 別の `WaitIcon` (`0x6C8138`) や `ComDialogA` (`0x1A9884`) も `save_wait.bclyt` を使う。資源名の一部が同じことだけで BlackWait の loader と同一視しない。
- Fade の画像源は `0x529598..614` の **`Layout/Wipe/fade.arc` / `fade.bclyt` / fade系5アニメ**。loaderとは別資源である。

### F0259 の残る静的主張

- Drawer変換：`0x4B8C34`→`0x4D6C90` は Layout `+0x34` から16語をコピーし、最初の語をDrawer `+0x30`へ移し、`+0x34`をheader `0x013F02C1`にする。旧記録の変換後fingerprint式は確認。ただし旧実測で一致した事実は再採取していない。
- 容量は生成時の引数にあり、全loader一律`0x1000`ではない。旧記録の特定managerの値・主リストの残量は静的IDBからは確かめられない。容量の一般契約は[ACNL-F0701]、提出条件は[ACNL-F0695]。

## 主張ごとの判定・訂正

| 元記録の主張 | 判定 | 再解析の結果 |
|---|---|---|
| F0259 上Fadeの後にloaderが再生される | 確認 | 上記更新経路・同値優先度・安定挿入が支持。実測の特定passを追試した意味ではない |
| F0259 8→10がロード時に常に続く／Fadeが最後という解釈 | 一部訂正 | ID固定を撤回。条件付きの登録順と状態表で説明する |
| F0259 `save_wait.arc` / `load_wait_kind` / `G_loop` がloaderの資源 | 確認 | 資源名の参照・生成・選択・登録まで接続 |
| F0259 `tc_load_01..03.bclim`、P_bg/N_All、停止Layout・Drawerの実物同定 | 一部訂正 | 埋込み資源・旧実機メモリを今回取得していないので、この個別同定は未確認。コードの資源経路のみ再確認 |
| F0259 十進10のbucketとmanager検索式 | 確認 | [ACNL-F0703]。F0261の0x10表記とは分ける |
| F0259 Drawerのrawコピー比較は誤り・変換後fingerprint式 | 確認 | コピーとheader挿入の命令が一致 |
| F0259 manager容量/offset/remaining・主リスト残量の旧値 | 一部訂正 | 旧停止標本として保留。一般の有限容量と生成時の値のみ確認 |
| F0259 特定の末尾追記が自然に提出・表示される可能性 | 一部訂正 | 提出は[ACNL-F0695]の条件付き。旧実装案・安全量はゲームの結論として採用しない |
| F0261 ロード表示に複数のフェーズがある | 一部訂正 | 状態ごとの登録差を静的確認。ただし旧二標本がどの状態だったかは未確認 |

本記録・[ACNL-F0703]・[ACNL-F0704] でF0253/F0259/F0261のゲーム側結論を置き換える。F0259は本記録のsupersedesとする。外部製品の設計・フックの提案は引き継がない。

## 反証条件・未確認点

- 各状態の実行時時刻、更新ゲート、種類変更、他の登録・解除、実際の画素の重なりは未測定。上記経路外でリストを書き換えれば順序の前提が崩れる。
- Idle/DispWaitにロード画像を目視したとしても、その状態関数は新しいloaderを登録しない。前回提出画像の保持か、別処理による描画か、途中で止めた標本かは、旧停止メモリだけでは確定しない。[ACNL-F0704]。
- 旧標本のID8/9/10・Layoutポインタ・0x180/0x2C0・pass順・容量・画像のtexture名は未追試。資源アーカイブ内の画像データとbclytの材質対応は今回のIDB証拠には含まれない。
