# symbols の形式

`symbols/<ビルド>/` に置く、IDA・Ghidra で共有する名前と型の正本です。道具（`tools/sync/`）が書き出し・取り込みをします。手で編集しません。

- 文字コードは UTF-8（BOM なし）、改行は LF。CSV は RFC 4180（項目に `,` `"` 改行があれば `"` で囲む）。
- アドレスは `0x` 付きの大文字16進で8桁（`0x00193764`）。行はアドレスの昇順。
- `confidence` は `HIGH`・`MEDIUM`・`LOW`・空欄（未評価）。`source` は `analysis`（記録に基づく）・`legacy-idb`（旧 IDB から）・`sdk`（公開名）・`rtti`。
- `refs` は根拠の記録 ID を `;` でつないだ物（無ければ空欄）。

## 書き方の決まり

- **Thumb の関数**: `functions.csv` の `address` は、Thumb の関数なら下位ビットを 1 にする（`0x00300E05`。ARM の関数は `0x00300E04`）。`lvars.csv` の `function` も同じ。`comments.csv` と `globals.csv` のアドレスは実際の番地のまま。
- **名前もプロトタイプも無い関数の行**: 関数のコメント（`comments.csv` の `func`）だけがある関数も `functions.csv` に入れる（`name`・`prototype` は空）。取り込みのときに、その関数を作る手がかりになる。
- **`lvars.csv` の `location`**: `stk:<スタックのオフセット（10進、負もある）>@<定義の番地>` または `reg:<レジスタ番号>@<定義の番地>`（例 `stk:-20@0x00123456`）。
- **名前の無い構造体メンバー**: IDA は `unsigned int;` と出力するが、C として解釈できないので `types/` では `unsigned int __unnamed_1;` のように補う。
- **コメント**: IDA が自動で入れる物（型名だけ、switch の説明、RTTI の説明、呼び出し先の引数名）は書かない。
- **`meta.toml`**: `build`・`source`（書き出しの元の種別）・`idb_input_sha256`（IDB に記録された入力の SHA256）・`code_sha256`（`meta/builds.toml` の値）・`idb_input_is_code_bin`（前者と後者が同じか。旧 HHD の IDB は CXI から作られていて false）・`ida_version`・`tool_version`・`exported_at`（UTC）と、`[counts]`（表ごとの行数）。

## ファイル

| ファイル | 列 |
|---|---|
| `functions.csv` | `address,size,name,prototype,confidence,source,refs,clone_of` |
| `globals.csv` | `address,size,name,type,confidence,source,refs` |
| `comments.csv` | `address,kind,text`（`kind` は `func`（関数のコメント）・`line`（行のコメント）・`repeatable`） |
| `vtables.csv` | `address,class,count` |
| `lvars.csv` | `function,name,type,location` |
| `types/<サブシステム>.h` | 構造体・Enum・typedef の C 宣言 |
| `meta.toml` | 書き出しの元（IDB の入力の SHA256、道具の版、日時） |
