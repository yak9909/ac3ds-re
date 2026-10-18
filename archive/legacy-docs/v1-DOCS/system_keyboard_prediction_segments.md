# 未確定予測候補の順位と内部文節（F-397）

入力「わたしはねこがすきです」を保持した実機から、候補6件と先頭候補の内部文節3件を取得した。
全文を確定・候補選択する操作は行っていない。ACNLは停止保持、SWKBDは取得後detach済み。
confidence HIGHはこの入力の実機状態と原本解析の照合に限定する。他の入力・学習状態への一般化はしない。

## 実機状態

- 今回のプロセス一覧: GARDEN PID 47、swkbd PID 50、SWKBDポート4001。
- app=`[0x001B7780]=0x08292880`、editor=`[0x001B777C]=0x080EA7F4`。今回読み直した値。
- app+`0x69588`のeditorポインタはglobalと一致。
- editorの`+0x14/+0x24/+0x28`は11/0/11。対象区間`[0,11)`、入力全文と一致。
- mode=0、ready=1、予測件数6、従来のmode1文節件数app+`0x37B7A`は0。
- 先頭候補index=0、展開済み表示cacheは2件。

## 候補順位

| index | 候補 | 根拠 |
|---|---|---|
| 0 | 私は猫が好きです | 実機表示cache。独立した原本PC予測でも同一 |
| 1 | わたしはねこがすきです | 実機recordを原本ARM decoderで復号、表示cacheとも一致 |
| 2 | ワタシハネコガスキです | 実機recordを原本ARM decoderで復号 |
| 3 | ﾜﾀｼﾊﾈｺｶﾞｽｷです | 同上 |
| 4 | ワタシハネコガスキデス | 同上 |
| 5 | ﾜﾀｼﾊﾈｺｶﾞｽｷﾃﾞｽ | 同上 |

F-398訂正: 旧PC構築では関数型辞書slot7..9が未登録だったため1件だった。
初期化を補うと同じwrapper直後に実機と同じ6件を再現する。
段階差という解釈は撤回。詳細system_keyboard_full_candidates.md。

## 従来の文節領域とは別の内部リスト

先頭recordの種別は`0x1012`。`0x13A0D4`は下位byteが`0x12`の場合に
engine+`0x2D1C4`、u16件数engine+`0x2E4AC`を使い、88 bytesずつ候補を復号して連結する。
逆アセンブルでADD/LDRHとstrideを確認した。読み取得`0x1368D4`も同じ領域を独立に参照する。

engine=app+`0x1518`のため、**record列はapp+`0x2E6DC`、件数はapp+`0x2F9C4`**。
今回の件数は3。mode1用app+`0x36890`が空でも、予測候補内の文節はこの別領域に残る。
古い領域の件数0だけから「文節情報が存在しない」とは判断できない。

| UTF-16範囲（終端を含まない） | 実機recordの読み | 対応する変換結果 |
|---|---|---|
| `[0,4)` | わたしは | 私は |
| `[4,7)` | ねこが | 猫が |
| `[7,11)` | すきです | 好きです |

読みは実機の各recordを原本`0x150898`で実行して取得。`0x1368D4`による連結読みも全文と一致。
変換片は実機recordとPC生成recordの全88 bytesを比較し、読みポインタと辞書handleの8 bytes以外が
完全一致した後、PCの対応recordを`0x139404`で復号した。3片の連結は実機表示cacheと一致する。
実機辞書の全状態をdumpして直接復号した、という意味ではない。実機recordをそのまま候補復号へ
渡す最初の試行は未取得の辞書領域参照でPC側が停止した。実機への影響はない。

この内部区切りと、UIで現在選択している変換範囲は別。今回のUI範囲は全文のままである。
他の候補種別・mode・入力ではこのリストが古い値になりうる。種別とreadyを必ず確認する。

## 検証と再現

`SYSTEM_KEYBOARD/evidence/phrase_prediction/`に生データ・取得ログ・各検証JSONを保存。
SWKBDコード655,360 bytesが提供イメージと完全一致。取得前は124命令語の照合、
取得後はglobal/editor/UI領域の再読取り一致も確認した。ブレークポイントや実機メモリ書換えなし。
IDA Pro MCPから別GDBクライアントを起動し、ACNLの接続を保ってSWKBDを取得した。
初回の状態照会タイムアウト、PID列挙後のGDB接続でinferiorが未attachだった失敗もログに残す。
PID50への明示attach後は正常取得・detach、exit0。ACNLはstate=-1、PC=`0x00137064`、bp0。

再現コマンド（すべて保存済みデータのみ）:

```
python -X utf8 SYSTEM_KEYBOARD/verify_phrase_reader.py
python -X utf8 SYSTEM_KEYBOARD/parse_phrase_dump.py
python -X utf8 SYSTEM_KEYBOARD/decode_phrase_candidates.py
python -X utf8 SYSTEM_KEYBOARD/verify_prediction_segments.py
```

`prepare_phrase_gdb.py`はこの取得時のPID/ポート用の記録。次のbootでは必ず再確認・更新する。
`read_phrase_snapshot.py`はIDAをSWKBDへ接続した場合の読取り器。ACNL接続のまま実行しない。

次は別入力での再現、境界変更時の内部リスト更新、表記候補の追加箇所を追う。
今回の指定入力については、追加の変換操作なしで候補と内部文節の取得を完了した。
