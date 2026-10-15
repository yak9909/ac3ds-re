# 事前確認（Issue 22）
- 対象6記録とF0693〜F0695を kb.py show で読んだ。対象は全て ?、F0693〜F0695 は A。描画の三パス・二リスト・寸法は後者を前提にする。
- kb.py search: 投影 / projection / SetupProjectionMatrix。番地は kb.cmd_addr（CLI と同じ処理、load_records をキャッシュ）で本文の番地と補助関数を照会した。出力: `_local/evidence/22/precheck.txt`、`precheck-addresses.txt`。即値も広めに照会している。
- 既存の名前は SetupProjectionMatrix、EmitProjectionUniform、Pane_CalculateMtx 等。旧記録だけを根拠にせず命令を採取する。
- F0288 のペインツリー矩形説と F0321 の Layout寸法説、F0288/F0303 の c4 範囲の違いを重点確認する。
- 主張一覧と判定は新記録本文へ記載。外部のケーブ実装、旧実機標本は静的IDBでは追試できないため未確認として分ける。

# 完了時の補足
- F0611はS。既存実機によるシザー向きは採用し、今回は静的命令だけ再確認。
- 新記録F0696〜F0698とtopics更新済み。IDBの訂正コメントをexport_symbolsで全書出し。改名・型付けなし。IDBは保存・閉鎖した。
- symbolsの前後比較はevidence/22/symbols-diff.txt（初回書出し）。差分はコメントとmetaのみ。書出しはIDB外の行を保持し手で絞っていない。
- 更新実体のaudit.scan_fileは7ファイル問題0。全体auditとkb lintの結果は報告末尾へ追記。

- 最終検査：kb.py index実行後のlint --strictは718記録エラーなし。tools/audit.pyは808ファイル問題0。初回のnotes改行警告はLF化して解消。旧9記録本文の不変も照合済み。
