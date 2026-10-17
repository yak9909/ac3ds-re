## 結果

完了（実装・形式移行・全行照合）。完了条件 (1)〜(4) を実施。(5) の通常 pytest はサンドボックスのアクセス拒否で完走できず、代替確認を実施した。IDA の試験は依頼どおり未実施。

## 結論と根拠の要約

- 2ビルド・5表を 1 MiB の番地範囲で分割。lvars は function 列を使用し、全ファイルにヘッダーを付けた。16,466 行を53ファイルへ移行し、移行前後の全行・全列・行順が完全一致。types/ と meta.toml もバイト一致。最大 CSV は568,409バイト。
- 移行の根拠: `_local/evidence/77/symbols-before/`（元 CSV）、`symbols-migration.json`（表ごとの件数・照合結果・元 SHA256）、`migrate_symbols.py`（照合手順）。この作業ツリーの symbols を移行元とし、main の取得・更新は行っていない。
- 同期処理と kb addr は分割表を結合して読む。書き出しと復元試験の準備も分割形式を使用する。import は既存の read_all 経由で対応。byte_diff は symbols を参照せず独自の差分 CSV を出すため、形式変更は不要。
- merge driver は functions/globals/vtables=address、comments=address+kind、lvars=function+location で3方向統合する。同じ鍵の双方の異なる行だけ衝突。異なる列への変更も行単位で衝突させる。共通祖先付きの Git マーカーを出力し、終了値0/1/2で成功・衝突・入力エラーを区別する。空になった既存範囲はヘッダーを残し、ファイル削除対変更の衝突を避ける。
- 既存ツールを実装前に評価した。[daff の公式説明](https://github.com/paulfitz/daff) は3方向 merge と複合キーに対応するが、セル単位の統合を行う。[csvdiff3 の公式説明](https://github.com/sctweedie/csvdiff3) も同じ行の異なる列の変更を統合し、主キー・衝突印にも追加対応が必要。今回の行単位衝突と既存の出力規則に合わせるラッパーが必要になるため、どちらも不採用。pip での導入・実行比較はせず、公式仕様を評価し、標準ライブラリと symlib で実装した。
- 試験: `python -m pytest -q tools/tests --basetemp .pytest-tmp` は一時フォルダーへの WinError 5 で完走不可。追加した試験をパラメータごとに直接実行し、62ケース成功（全表の分割・結合、3方向の変更・同一変更・衝突・追加・削除、複合キー、lvar rename、改行入り CSV、CLI 終了値、不正入力の保持）。両ビルドの実データに対する kb addr 4検索と、境界をまたぐ検索3ケースも成功。代替実行は `manual_tests.py` と `kb_boundary.py`。
- 監査: `audit_worktree.py` で tools/audit.py の検査本体を現在の作業ツリー973ファイル（報告書を含む）へ適用し、問題0件。通常の audit.py は追跡済みファイルをインデックスから読むため、この未ステージ移行では旧形式と新形式が混在する。最終のステージ後の通常監査はオーケストラで実行する。既存コメント引用の監査許可はハッシュを変えず、新パスへ付け替えた。
- ゲームの新しい事実・findings の追加はない。

## 訂正の提案

なし

## 統合・重複の提案

なし

## 新しいタグの提案

なし

## 未確認点

- サンドボックス外での全 pytest 完走、Git からの merge driver 呼び出し。driver 自体の CLI は試験済み。Git の登録操作はしていない。
- IDA の export/import/restore_test はオーケストラが実施する。
- `.pytest-tmp` と、追加診断で作成した `.pytest-tmp-check` が作業ツリー直下に残っている。絶対パスを確認して削除を試みたが、自動承認レビューが `blocked by policy` と拒否した。追加の理由は返されなかった。

## 次の1手

bootstrap で以下を登録する（Python は作業場のものを指定）。これは設定例で、ワーカーは実行していない。

```powershell
git config merge.ac3ds-symbols.driver '"A:/Disassemble/ac3ds-workspace/_local/venv/tools/Scripts/python.exe" tools/sync/merge_symbols.py "%O" "%A" "%B" "%P" --marker-size %L'
```

サンドボックス外で残った一時フォルダーを削除し、全 pytest を指定の basetemp で実行する。差分をステージした状態で tools/audit.py を再実行し、Git 経由の統合確認と IDA の同期・復元試験を行う。
