事前確認: kb.py search を「書き出し」「export」「export_all」で実行。関連する既存ツール・記録なし。設計変更書 §2・§3、docs/symbols.md、symlib、idacommon を確認。ゲームの事実の追加解析なし。

実装: tools/sync/export_all.py、tools/codebytes.py、tools/tests/test_export_all.py。
試験: tools の Python にて pytest 185 passed（32.13秒）。audit 975ファイル・問題0、kb lint 724記録・エラーなし。
実行中: export-full.log に全44330関数の進捗。環境 AC3DS_WORKSPACE=共有workspace、TMP/TEMP=evidence/79。
symbols-commit=d87bcfa（state/tasks.json の #77 accepted/idb_import=取り込み済み/merge_commit。Gitは直接実行していない）。
作業用IDBの書き出し中SHA256: B01E0D90107E6C8F40D72CA4A813CFB8C4E724A4CA220BCD8CDFC2193AD28DFE。
残り: 全関数の完了を待つ、verify_export.py を実行、実IDBで --only sub_100024 を試す、報告。

完了。計測・部分更新・整合性検査の結果は report.md と evidence/79/ に記載。
