# Issue 125 作業メモ

事前確認: 司令塔が 2026-11-09 に実施した #125 の確認結果を依頼文から引き継いだ。ゲームの解析は行わず、道具だけを変更。

- WebChat 手順書6節を読み、下書きの鍵と並びを確認した。
- lint の型検査・台帳検査・参照先検査を共通関数に抽出。下書きは build の scope を利用。
- intake は全下書きを検査してから reserve_number で採番する。
- .gitignore は inbox を追跡するため追加変更。
- pytest は既定 temp と mode=0o700 のディレクトリで WinError 5。実行時のみ os.mkdir の mode を 0o777 にするラッパーを使い、evidence/125 配下で試験中。製品コードには環境回避を含めない。

検証の経過:
- python tools/audit.py: 1029 ファイル、問題 0 件。audit は追跡済みファイルをインデックスから読むため、変更した全ファイルも scan_file で直接検査し問題 0 件。
- python tools/kb.py lint: 767 件、エラーなし。
- 共通 fixture に AC3DS_WORKSPACE の隔離を追加。_local 配下の一時 repo が実作業場の参考資料索引を見つける既存試験の干渉を防ぐ。

最終結果:
- 全 288 試験成功（39.94 秒）。実行: python <作業場>/_local/evidence/125/run-tests.py。
- ラッパーは os.mkdir の mode を実行時だけ 0o777 にし、pytest -q tools/tests と同じ全試験を呼ぶ（cache 無効、basetemp を evidence/125 に固定）。通常の python -m pytest -q tools/tests は sandbox の WinError 5 で実行できなかった。
- audit 再実行: 1029 ファイル、問題 0 件。変更した全ファイルの直接監査も問題 0 件。
- lint: 767 記録、エラーなし。
- Git/gh のコマンドは直接実行していない。ゲームの事実は使っていない。
