# symbols の形式

`symbols/<ビルド>/` に置く、IDA・Ghidra で共有する名前と型の正本です。道具（`tools/sync/`）が書き出し・取り込みをします。手で編集しません。

- 文字コードは UTF-8（BOM なし）、改行は LF。CSV は RFC 4180（項目に `,` `"` 改行があれば `"` で囲む）。
- アドレスは `0x` 付きの大文字16進で8桁（`0x00193764`）。各表の行は番地の昇順（同じ番地の comments は func・line・repeatable 順、lvars は location 順）。
- `confidence` は `HIGH`・`MEDIUM`・`LOW`・空欄（未評価）。`source` は `analysis`（記録に基づく）・`legacy-idb`（旧 IDB から）・`sdk`（公開名）・`rtti`。
- `refs` は根拠の記録 ID を `;` でつないだ物（無ければ空欄）。

## 書き方の決まり

- **Thumb の関数**: `functions/<範囲>.csv` の `address` は、Thumb の関数なら下位ビットを 1 にする（`0x00300E05`。ARM の関数は `0x00300E04`）。`lvars/<範囲>.csv` の `function` も同じ。`comments/<範囲>.csv` と `globals/<範囲>.csv` のアドレスは実際の番地のまま。
- **名前もプロトタイプも無い関数の行**: 関数のコメント（`comments/<範囲>.csv` の `func`）だけがある関数も `functions/<範囲>.csv` に入れる（`name`・`prototype` は空）。取り込みのときに、その関数を作る手がかりになる。
- **`clone_of`**: `tools/clones.py --build <ビルド> --update-symbols` が、同じ形の関数の代表の番地を `0x` 付きの大文字16進8桁で書く。Thumb の代表は下位ビットを 1 にする。代表自身は空欄。代表は名前の付いた関数のうち最小番地、無ければ全体の最小番地。IDA の自動名とローダー名 `start` は名前付きに数えない。既存の名前付き行だけを更新し、名前の無い行は追加しない。現在のまとまりの代表に残っていた `clone_of` は空に戻す。まとまりの外の行は変更しない。
- **`lvars/<範囲>.csv` の `location`**: `stk:<スタックのオフセット（10進、負もある）>@<定義の番地>` または `reg:<レジスタ番号>@<定義の番地>`（例 `stk:-20@0x00123456`）。
- **名前の無い構造体メンバー**: IDA は `unsigned int;` と出力するが、C として解釈できないので `types/` では `unsigned int __unnamed_1;` のように補う。
- **コメント**: IDA が自動で入れる物（型名だけ、switch の説明、RTTI の説明、呼び出し先の引数名）は書かない。
- **`meta.toml`**: `build`・`source`（書き出しの元の種別）・`idb_input_sha256`（IDB に記録された入力の SHA256）・`code_sha256`（`meta/builds.toml` の値）・`idb_input_is_code_bin`（前者と後者が同じか。旧 HHD の IDB は CXI から作られていて false）・`ida_version`・`tool_version`・`exported_at`（UTC）と、`[counts]`（表ごとの行数）。

## 番地範囲ごとの分割

CSV は `symbols/<ビルド>/<表>/<範囲の先頭の16進8桁>.csv` に置きます。
表は `functions`・`globals`・`comments`・`vtables`・`lvars` です。
範囲の幅は `0x100000`（1 MiB）で、先頭は大文字の16進8桁（`0x` なし）。
例えば `functions/00100000.csv` は `0x00100000` 以上 `0x00200000` 未満の行です。
`lvars` は `function`、他の表は `address` の番地で分けます。Thumb の下位ビットも保存します。
各ファイルの先頭には、下表のヘッダーを必ず書きます。主キーは表の全体で重複させません。

`symlib.read_table` / `read_all` は範囲ファイルを結合して読み、`write_table` は分割して書きます。
読み込み時にはヘッダー・列数・範囲・キーの重複を検査します。旧形式の `<表>.csv` が残っていたらエラーにします。
書き出し時は古い行を置き換え、行のなくなった範囲にもヘッダーを残します。
これにより Git のファイル削除対変更ではなく、行の削除対変更として統合できます。
最初から空の表は `00000000.csv` をヘッダーだけで作ります。
`types/` と `meta.toml` の形式・置き場所は変わりません。`[counts]` は表全体の行数です。

## ファイル

| ファイル | 列 |
|---|---|
| `functions/<範囲>.csv` | `address,size,name,prototype,confidence,source,refs,clone_of` |
| `globals/<範囲>.csv` | `address,size,name,type,confidence,source,refs` |
| `comments/<範囲>.csv` | `address,kind,text`（`kind` は `func`（関数のコメント）・`line`（行のコメント）・`repeatable`） |
| `vtables/<範囲>.csv` | `address,class,count` |
| `lvars/<範囲>.csv` | `function,name,type,location` |
| `types/<サブシステム>.h` | 構造体・Enum・typedef の C 宣言 |
| `meta.toml` | 書き出しの元（IDB の入力の SHA256、道具の版、日時） |

## 3方向の自動統合

`.gitattributes` の `symbols/*/*/*.csv merge=ac3ds-symbols` により、登録済みの
Git merge driver `tools/sync/merge_symbols.py` を使います。登録は作業場の bootstrap が行います。
リポジトリ単独で使う場合も同じ driver の登録が必要です。次の設定の `python` は実行環境の Python に合わせます。

```sh
git config merge.ac3ds-symbols.driver 'python tools/sync/merge_symbols.py "%O" "%A" "%B" "%P" --marker-size %L'
```

| 表 | 行の主キー |
|---|---|
| functions・globals・vtables | address |
| comments | address と kind |
| lvars | function と location（name は鍵に含めない） |

共通祖先・自分・相手の各 CSV を読み、鍵ごとに次のように統合します。

- 双方が同じ行にしたらその行を採用します（同じ追加・同じ削除も含む）。
- 一方が祖先のままなら、もう一方の変更・追加・削除を採用します。
- 双方が祖先と異なり、互いにも異なれば、その行だけを衝突として残します。
  同じ行の別の列を変えた場合や、削除と変更の場合も衝突です。

結果は番地順で `%A` に書き、衝突行には `<<<<<<< ours`・`||||||| base`・`=======`・
`>>>>>>> theirs` の Git の印を付けます。改行入りの CSV 行も行の全体を印の内側へ書きます。
印の長さは `%L` に従います。終了値は成功が 0、衝突が 1、入力や入出力のエラーが 2 です。
入力エラーのときは `%A` を変更しません。衝突を解消するまでは CSV として取り込めません。
Git が driver を呼ばないファイル単位の削除対変更は Git 側で解消します。

export・import・restore_test は全範囲を1つの表として扱います。
`kb.py addr` は functions・globals の全範囲を読むため、範囲の境界をまたぐ関数や大域も検索できます。
`byte_diff.py` は symbols の CSV を読まず、IDB と code.bin のバイトを比較して独自の差分 CSV を出すため、
その出力形式にはこの分割や merge driver を適用しません。

## 同じ形の関数の検出

`python tools/clones.py --build <ビルド>` は全関数の書き出しの `index.txt` に載った
`functions/` を読み、`export/clones.txt` に同じハッシュのまとまりを出す。IDA は不要。
`--export DIR` で入力、`--out FILE` で出力先を変えられる。
`--min-instructions N` は最小命令数（既定は 5、4 命令以下を除外）。
`--symbols DIR` はビルド単位の symbols ディレクトリを指定する。

逆アセンブル節の命令だけを対象にし、データ・コメント・疑似コードは使わない。
命令の番地・ラベル・名前・直接分岐先・ADR の参照先・`=値` 全体・PC 相対参照の
即値変位を伏せ、命令の種類、レジスタ、通常の即値を残して SHA-256 を取る。
ARM／Thumb は各命令の区分をハッシュに含め、途中で区分が変わる関数も区別する。
名前は現在の symbols の行を優先し、行が無ければ索引の名前を使う。
これは正規化した命令列の一致であり、動作の等価性を保証しない。
数値だけの通常の `#即値` は、番地か整数かをテキストから判別できないため残す。
分岐先・リテラル値の違いは意図して区別しない。既定の実行は symbols を変更しない。
