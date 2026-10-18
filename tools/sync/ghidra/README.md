# Ghidra 同期と独立検証

Python 3.11 以上、PyGhidra 3.1.0（`python -m pip install -r tools/requirements-ghidra.txt`）、Ghidra 12.1.4、Java 21 以上を使います。
Java 26 でも実測しました。`JAVA_HOME` は `bin` でなく JDK のルートです。
PyGhidra での headless 起動・プロジェクト作成・CParser・逆コンパイルを試して採用しました。
CSV を既存の symlib で直接検査できるため、Java スクリプトへ CSV を二重実装しません。

PowerShell の例（`$ws` は作業場、`$py` は tools venv の Python）:

```powershell
$env:TMP = "$ws/_local/evidence/82"
$env:TEMP = $env:TMP
& $py tools/sync/ghidra/run.py create --build acnl_jpn_v15
& $py tools/sync/ghidra/run.py import --build acnl_jpn_v15
& $py tools/sync/ghidra/run.py dump --build acnl_jpn_v15 --target 0x00100000 --out "$env:TMP/start.txt"
& $py tools/sync/ghidra/run.py dump --build hhd_jpn_v11 --target HhdCameraGame_CreateRoomSpline --out "$env:TMP/camera.txt"
```

作業場はリポジトリの親をたどり、workspace.toml のある場所を自動検出します（作業ツリーにも対応）。
Ghidra は作業場の scripts/third_party.toml の版を読み、_local/tools/ghidra/<版>/ 以下から検出します。
`--workspace` / `--ghidra` の明示指定、AC3DS_WORKSPACE / GHIDRA_INSTALL_DIR 環境変数、自動検出の順に優先します。`--build hhd_jpn_v11` で同じ手順を行えます。
Ghidra は利用者の設定フォルダへ設定・ログを作ります。生成物のプロジェクト・集計は
`_local/builds/<ビルド>/ghidra/` に置きます。逆コンパイルの出力も `_local` に置いてください。

`create` は builds.toml のサイズ・SHA256 を照合してから JVM を起動します。
ARM:LE:32:v6 / default、.text=R-X、.rodata=R--、.data/.bss=RW-。
ファイルオフセットは仮想番地と text 先頭の差、bss は未初期化です。エントリは text の先頭のみで、
symbols・IDA の索引は解析の入力に使いません。自動解析後にだけ、比較用に全関数の IDA 索引を読みます。

プロジェクト `ac3ds.gpr` の `independent` は code.bin だけから解析したプログラムです。
`import` はそれを `symbols` に複製し、複製にだけ関数境界・TMode・名前・プロトタイプ・大域の型・コメント・C 宣言を適用します。
`dump` は既定で `independent` を使います。名前は symbols の関数名と Ghidra の関数名で解決し、symbols は要求番地と（--create 時）ARM/Thumb の解決にだけ使います。
要求番地と Ghidra が認識した開始番地を両方出し、要求番地を含む関数の逆アセンブル・逆コンパイルを出します。
通常は関数未検出ならエラーです。`dump --build acnl_jpn_v15 --target 0x00193764 --create` は
independent を一時プロジェクトにコピーし、指定番地で関数を作成して出力します。
開始番地だけを与え、境界は Ghidra に決めさせます。symbols の名前・サイズ・型は適用しません。
`--mode arm` / `--mode thumb` で明示でき、省略時は指定番地の Thumb ビット、symbols の下位ビット、ARM の順に決めます。
先頭に「開始の番地は指定から与えた。境界と中身は Ghidra の解析」と明記します。
元の independent は変更せず、一時コピーは終了・失敗時とも閉じて削除します。
`--out` 省略時は作業場の `_local/builds/<ビルド>/ghidra/dump.txt` に出力します。
`--view symbols` は同期結果の点検用で、独立した根拠にはできません。

既存の independent や symbols は上書きしません。作り直すときは Ghidra で既存プロジェクトを閉じ、
生成済みの ghidra フォルダを別名で保管してから実行します。create の途中で失敗し、プログラムがまだ保存されていない場合は再実行できます。

- `create.json`: バイトの由来、セグメント、Ghidra の版、自動解析の時間、全開始番地。
- `starts.json`: IDA の全関数索引との開始番地集合の差。IDA のみ / Ghidra のみは一対一の対応を仮定しません。
- `import.json`: 項目別の成功・失敗件数、失敗例、経過秒、型ファイルの SHA256。

`compare --build <ビルド>` は独立解析を変更せず、現在の IDA 全関数索引との比較だけを更新します。
開始番地の集合差に加え、IDA の開始が別の Ghidra 関数の中に入る件数と、関数未検出の件数を分けます。

IDA の整数型と呼出規約の表記は C に正規化します。大域型の const/volatile は Ghidra の DataType が表現しないため除き、基底型・ポインタ・配列を適用します。未知の構文は失敗として報告します。
他の関数と境界が重なる場合はその関数の境界適用を失敗にし、別の関数を削除しません。
関数境界の適用が失敗しても、元の同番地の関数があれば名前・プロトタイプは個別に試みます。
`types` は export の `// type:` ごと（印がなければヘッダー全体）で計数し、前方宣言は別集計です。
`lvars` と `vtables` の専用の復元は対象外で、行数を `unsupported_tables` に明示します。

Ghidra を使わない入力検証・比較の試験: `python -m pytest -q tools/tests`。
