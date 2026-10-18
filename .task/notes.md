# 事前確認

- precheck に従い `kb.py search 参考資料`・`reference`・`refindex` を実行。既存の参考資料利用の記録は見つかったが、索引生成の実装・既存結論はない。ゲームの事実の判定には使用していない。
- `docs/references.md`、`meta/references.toml`、use-references、設計書 STRUCTURE_DRAFT.md §12 を確認。本文・ID 一覧をリポジトリへ写さず、参照先だけをローカル索引に残す。記録の新規登録はしない。
- 作業はワーカーとして実施。git / gh は実行しない。実資料の生成先は指定 evidence/94 のみ。

# 追加修正

- ユーザー指定の番地範囲（0x00100000 以上、0x40000000 未満）を Gateway と0x候補の両方に適用。addr の参考資料は既定20件まで、超過分を件数表示。
- 試験34件通過。実資料を evidence/94/refindex/addresses.tsv に再生成し、集計を同フォルダの stats.json に保存。統計の定義と結果は report.md に追記。
