## 結果

完了。完了条件 (1)〜(5) を実装・実測した。Ghidra に未対応の宣言・境界衝突・メモリ範囲外は失敗件数と例を集計し、成功扱いにしない。

## 結論と根拠の要約

ゲームの事実についての新規 finding はない。PyGhidra 3.1.0 / JPype1 1.5.2 / Ghidra 12.1.4 / Java 26 を採用。実際に headless 起動、ProgramDB の raw 読み込み、自動解析、C 宣言、ARM/Thumb、プロトタイプ、大域、コメント、複製、逆コンパイルを試して選択した。既存 symlib を再利用でき、Java 側に CSV 検査の重複実装が要らない。Java スクリプト版の比較実装は作っていない。

`tools/sync/ghidra/run.py` の create / import / dump / compare。使用例・依存関係・制限は同ディレクトリの README.md。成果物は作業場の `_local/builds/<ビルド>/ghidra/ac3ds.gpr`。`independent` は code.bin のみから作成し、`symbols` はその複製。dump の既定は independent、symbols は番地と（--create 時）ARM/Thumb の解決だけに用いる。IDA 索引は自動解析の終了後の比較だけで読む。名前を付けたコピーは独立の根拠として使わない。

| 項目（成功 / 失敗） | acnl_jpn_v15 | hhd_jpn_v11 |
|---|---:|---:|
| 関数の作成・境界・TMode | 1,710 / 45 | 414 / 6 |
| 関数名 | 1,586 / 29 | 407 / 3 |
| プロトタイプ | 210 / 7 | 12 / 2 |
| 大域名 | 8,645 / 0 | 62 / 0 |
| 大域型 | 2,920 / 0 | 23 / 0 |
| コメント | 2,602 / 5 | 381 / 0 |
| 型宣言 | 225 / 1 | 50 / 1 |
| 型の前方宣言のまとまり | 1 / 0 | 1 / 0 |

名前・プロトタイプ・大域型は CSV の非空欄だけを計数。型宣言は `// type:` ごと、前方宣言は別集計。関数境界の失敗後でも同番地に既存関数があれば名前・プロトタイプを個別に試みるため、項目ごとの成功は別々。

| 時間・関数数 | acnl_jpn_v15 | hhd_jpn_v11 |
|---|---:|---:|
| 独立解析で認識した関数 | 27,592 | 21,864 |
| 作成・保存（秒、JVM 起動除く） | 1025.1 | 836.8 |
| うち自動解析（秒） | 998.6 | 819.2 |
| 最終の取り込み（秒、JVM 起動含む） | 82.3 | 41.0 |

初回の両ビルドの作成は並行して実行した。上表の作成時間は今回実行中だった初版の計測範囲（JVM 起動後から保存まで）。最終版の CLI の seconds は JVM 起動も含む。再試行前のコピーは `symbols_initial`（両ビルド）、`symbols_enum_attempt`（ACNL）として手元に保存してある。

| 開始番地の比較（symbols 適用前） | acnl_jpn_v15 | hhd_jpn_v11 |
|---|---:|---:|
| IDA 索引の全関数 | 44,330 | 37,057 |
| Ghidra の全関数 | 27,592 | 21,864 |
| 開始番地が一致 | 27,159 | 21,447 |
| IDA 開始を含む Ghidra 関数の開始が異なる | 1,131 | 613 |
| IDA 開始で Ghidra 関数未検出 | 16,040 | 14,997 |
| 開始番地の集合: IDA のみ | 17,171 | 15,610 |
| 開始番地の集合: Ghidra のみ | 433 | 417 |

集合差は一対一の対応を仮定しない。IDA 開始を含む関数の開始が異なる件数も、どちらが正しいかの判定ではない。比較元は両ビルドの全関数書き出し（symbols_commit `65293c69e61e182196200b92414beff86f647a98`）。索引の入力 SHA256 と code.bin の一致も検査する。

検証: `python -m pytest -q tools/tests` は **212 passed**。`python tools/audit.py` は **980 ファイル、問題 0 件**。Ghidra の生成物・逆コンパイルはすべて作業場の `_local` にある。git/gh は直接実行せず、IDB は一切開いていない。

実読みの検証では両ビルドについて、全メモリブロックの番地・権限・bss の未初期化状態、初期化した全バイトの code.bin との一致、取り込み後も independent の全開始番地が create.json と一致することを確認した。関数名・大域名・コメントも読み戻した。番地指定で両ビュー、名前指定で独立ビューの逆アセンブル・逆コンパイルを出力した。ACNL の基底幅指定 enum は 1 バイトで保存された。

- acnl_jpn_v15: 関数名 1,586、大域名 8,645、コメント 2,602 の読み戻し一致。独立ビューの Thumb 関数 709、symbols ビュー 731。
- hhd_jpn_v11: 関数名 407、大域名 62、コメント 381 の読み戻し一致。独立ビューの Thumb 関数 169、symbols ビュー 169。

証拠: 作業場 `_local/evidence/82/verification.json`、`verify.log`、`pytest-final.log`、`audit-final.log`、`smoke3.log`。実ビルドのテキスト出力は `<ビルド>-independent-start.txt`・`<ビルド>-symbols-start.txt`・`<ビルド>-named-independent.txt`。各プロジェクトの `create.json` / `import.json` / `starts.json` に件数・時間・入力ハッシュ・失敗例・番地集合を保存。

主な失敗例:

- 関数境界: ACNL `0x0013149C` は別の Ghidra 関数 `0x0012AAD0` と衝突、HHD `0x001C879C` は `0x0058D3D4` と衝突。衝突する関数を削除しない。
- プロトタイプ: HHD `0x00552160`・`0x0061AC1C` などの明示レジスタ付き `__usercall` は未対応。通常の ARM 既定呼出規約への推測変換はしない。
- 型: 両ビルドの `svfloat16_t` は `short float` を Ghidra の CParser が解釈できず失敗。
- コメント: ACNL の `0x00B19CEC` など 5 件は code.bin のセグメント外（追加の領域を推測して作らない）。

オーケストラからの追加修正 3 点を完了。

- `dump --create` は independent を一時プロジェクトへコピーして指定開始に関数を作成。Ghidra の CreateFunctionCmd で境界を求め、名前・プロトタイプ・symbols のサイズは適用しない。`--mode arm|thumb`、指定番地の下位ビット、symbols の下位ビット、既定 ARM の順でモードを解決する。元の解析を保存し直さず、一時コピーは終了・失敗時とも削除する。先頭に指定開始であることを明記。
- 作業場は workspace.toml まで親をたどって自動検出（入れ子の作業ツリーにも対応）。Ghidra は scripts/third_party.toml の版の `_local/tools/ghidra/<版>/` 以下から自動検出。明示オプション、既存環境変数、自動検出の優先順。`--out` 省略時は `_local/builds/<ビルド>/ghidra/dump.txt`。
- `tools/requirements-ghidra.txt` に `pyghidra==3.1.0` を追加し、README の導入・起動例も更新。

追加試験を含む tools/tests は 212 件成功（pytest-revision.log）。実測で ACNL の全開始番地が create.json と一致し、元の independent には 0x00193764 の関数が依然存在しないことを確認した。Thumb の合成プログラムでも作成・逆コンパイル・元の不変・一時コピー削除が成功。失敗時のコピー削除も pytest で確認（check-revision.log）。git/gh は直接実行していない。

環境変数 AC3DS_WORKSPACE / GHIDRA_INSTALL_DIR を除き、作業ツリーから次をそのまま実行し成功した。

```powershell
python tools/sync/ghidra/run.py dump --build acnl_jpn_v15 --target 0x00193764 --create
```

出力 `_local/builds/acnl_jpn_v15/ghidra/dump.txt` の先頭 20 行（複製は evidence/82/dump-create-first20.txt）:

```text
開始の番地は指定から与えた。境界と中身は Ghidra の解析
temporary_copy: independent
mode: arm
build: acnl_jpn_v15
code_sha256: c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb
view: independent
language: ARM:LE:32:v6
requested: 0x00193764
requested_address: 0x00193764
entry: 0x00193764
name: FUN_00193764
body: [[00193764, 00193833]]
prototype: undefined FUN_00193764(void)

[disassembly]
0x00193764  c8 10 9f e5                      ldr r1,[0x193834]
0x00193768  c8 c0 9f e5                      ldr r12,[0x193838]
0x0019376C  10 40 2d e9                      stmdb sp!,{r4,lr}
0x00193770  c4 30 9f e5                      ldr r3,[0x19383c]
0x00193774  00 20 91 e5                      ldr r2,[r1,#0x0]
```

## 訂正の提案

なし。開始位置の差は検証対象であり、今回 IDA/symbols の既存名やゲームの記録は訂正していない。

## 統合・重複の提案

なし。

## 新しいタグの提案

なし。

## 未確認点

- lvars / vtables の専用復元は今回の完了条件外。未対応行数として ACNL は 9 / 2,586、HHD は 0 / 0 を記録。vtable の既存の大域名・型は globals から適用される。
- 上記の失敗宣言と境界の衝突は未解決。関数を独立ビューで認識していない場合、通常の dump はエラーとする。追加の --create なら独立解析の一時コピー上で、指定開始から Ghidra に境界を決めさせる。IDA の境界は適用しない。
- Ghidra の自動解析が全関数を認識するとは限らず、開始位置の一致だけで正しさは確定しない。ゲームの実機検証は本作業では行っていない。

## 次の1手

オーケストラで差分をレビューして取り込む。深い検証では `dump --build <ビルド> --target <番地または名前> --out <作業場の_local内のパス>` を使い、既定の independent と IDA の全関数書き出しを見比べる。
