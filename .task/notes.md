# 事前確認

precheck: kb.py search 衝突 / symbols / merge_symbols を実施。ゲームの衝突判定や旧 symbols の記録はあるが、CSV 分割・統合の既存実装は見当たらない。対象は道具の変更であり、ゲームの番地に対する解析はない。
資料: docs/symbols.md と作業場直下 STRUCTURE_DRAFT.md §10。

既存ツール評価（実装前）:
- daff: https://github.com/paulfitz/daff 。3方向 merge と複合 --id があるが、セル単位の統合が基本で、同じ行への異なる変更を必ず衝突にする要件とは違う。
- csvdiff3: https://github.com/sctweedie/csvdiff3 。README に同一行の異なる列の変更を統合すると明記。主キーは単列で、Git と異なる衝突マーカー。複合キー・行単位衝突の追加ラッパーが必要。
- 不採用。標準ライブラリと symlib の CSV 処理・キー定義で実装する。pip 導入や実行評価はしていない（公式仕様の評価）。

Git/gh は一切実行しない。IDA の試験と bootstrap の設定はオーケストラが担当。

# 経過と検証

- symbols の元 CSV は evidence/77/symbols-before/ に保存。migrate_symbols.py で移行前後の全行・全列・順序を比較。一致後に旧 CSV を削除。全 16,466 行、53 範囲ファイル、最大 568,409 バイト。types/ と meta.toml は移行時にバイト一致を確認。
- meta/audit-allow.toml の既存コメント引用の許可は、対象パスだけ comments/00100000.csv へ移した。ハッシュ・許可内容は不変。
- 通常の pytest は .pytest-tmp の読み出しで WinError 5。追加ファイルの診断時の .pytest-tmp-check でも同様。後片付けの Remove-Item は自動承認レビューが blocked by policy と拒否した。両フォルダーの削除はオーケストラへ引き継ぐ。
- evidence/77/manual_tests.py は pytest のパラメータを展開し、新規の試験関数を直接実行。全 62 ケース成功。通常権限で作った evidence 内のフォルダーを使用。両ビルドの実データ kb addr 4 検索、kb_boundary.py の範囲境界 3 ケースも成功。
- tools/audit.py の通常実行は追跡済みファイルをインデックスから読むため、未ステージの形式移行を評価するには混在する。通常実行は修正前の notes の CRLF と新パスの許可未反映を検出。最終確認は evidence/77/audit_worktree.py で同じ audit.main / scan_file を作業ツリーの 972 ファイルへ適用し、問題 0 件。実行時の列挙のみ差し替え、検査本体・許可内容は変更しない。
- Git/gh コマンドは直接実行していない（audit.py 内部の利用のみ）。IDA は使用していない。
