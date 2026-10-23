# 事前確認

- 対象 0x008FE6F8 は vtables に sead_CtrController/count=9 として存在するが globals には無い。
- kb.py addr、search（コントローラー・Controller・sead_CtrController）を実行。入力の topics は無く、既存 topics/acnl/ui.md を確認した。
- ACNL-F0721、F0737、F0713 は kb.py show で格付け A。F0376 等の ? 記録だけを根拠にしない。
- F0737 の初期化と F0721 の管理体 calc/装置更新の結論を利用し、原本書き出し・codebytes と照合する。
- 命名は docs/naming.md、未確認項目は既存 SeadExpHeapVtable と同じ void *unk_<offset>。
- 資料は workspace 共通の _local/orchestrator/precheck/re-ctrcontroller-vtable.md に存在。

# 完了内容

- ACNL-F0743 を作成。原本bytesで0x008FE6F8から9項目、終端0x008FE71C=0、36バイトを確認。
- 作業用IDBへ SeadCtrControllerVtable を適用し保存。全9メンバーの位置・サイズを読み戻して検証した。
- export_symbols.py を実行。既存の無関係な3関数と旧型9個が書き出されたため、narrow_export.py で新規型と今回のglobals/commentsだけを残し、metaの件数を合わせた。
- kb.py stamp --self の最初の実行は AC3DS_MODEL 未設定で失敗。AC3DS_MODEL=gpt-6 を明示して対象記録だけ再実行した。
- kb.py index 更新済み。lint=762件エラーなし。変更実ファイルへのaudit.scan_file=問題0件。
- 証拠・スクリプトはすべて _local/evidence/112/。git/ghは直接実行していない。
- python tools/audit.py 終了コード0、1024ファイル・問題0件（2回とも同結果）。
