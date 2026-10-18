# 事前確認

- precheck に従い kb search の「Ghidra」「同期」「sync」を実行。既存のゲーム解析と旧 XML exporter の記録はあるが、今回の raw code.bin から独立解析する同期道具の完成済み記録はない。
- docs/symbols.md、meta/builds.toml、作業場 scripts/third_party.toml と既存 sync を確認。IDB は開かない。git/gh は実行しない。
- PyGhidra 3.1.0 を tools venv に導入。未適用 independent と symbols 適用用を分離して検証の独立性を保つ。

## 実装と実測の経過

- tools/sync/ghidra/run.py の create/import/dump/compare を実装。common.py は Ghidra 非依存、backend.py は起動後の API 処理。
- 両方の raw 独立解析を作成済み。ACNL: 27,592 関数・自動解析 998.61 秒、HHD: 21,864 関数・819.218 秒。
- symbols コピーを取り込み済み。HHD 最終: 関数 414/6、名前 407/3、プロトタイプ 12/2、大域名 62/0、大域型 23/0、コメント 381/0、型 50/1（成功/失敗）。
- ACNL は enum の明示幅の保存を実読みで検出し、EnumDB の copy からサイズを変更して addDataType(REPLACE_HANDLER) で保存するよう修正、最終取り込み・読み戻し検証とも完了。
- 初回コピーは symbols_initial、幅修正前の ACNL コピーは symbols_enum_attempt に保管。independent は変更しない。
- 開始位置の食い違い（IDA 開始が別 Ghidra 関数の中）は ACNL 1,131、HHD 613。未検出と集合差は starts.json に別集計。
- 合成 ARM/Thumb、型・プロトタイプ・大域型・3種類のコメント・両ビューの dump は smoke3.log で成功。pytest 最終 200 passed。
- evidence は作業場 _local/evidence/82。verify.py はメモリ・権限・全 initialized bytes・開始番地保持・明示 enum 幅・名前の読み戻し・dump を検査する。

## 完了

- ACNL の最終型宣言は 225 成功 / 1 失敗。大域型 2,920 件成功。明示 enum 幅 1 バイトの読み戻し PASS。
- verification.json で両ビルドの全バイト・メモリ権限・independent の開始番地保持・名前とコメントの読み戻し・番地と名前の dump が PASS。
- pytest: 200 passed。audit.py: 980 ファイル、問題 0 件。詳細と再開・使用手順は report.md と同期道具の README.md。

## オーケストラからの修正依頼

- precheck の addr 0x00193764 で既存名 ChatWindow_ConsumeInputResult と ACNL-F0423 を確認。ゲームの知見は再解析せず、道具の再現試験だけ行った。
- --create、一時プロジェクトの分離・破棄、--mode と symbols の下位ビット、自動 workspace/Ghidra 検出、requirements-ghidra.txt、README を追加・更新。
- 指定の dump --build acnl_jpn_v15 --target 0x00193764 --create は指定パスなしで成功。先頭20行を report.md に貼付。
- tools/tests は 212 passed。check-revision.log で ACNL independent の不変、Thumb の一時解析・元の不変・削除が PASS。コピー失敗時の削除も pytest で PASS。
