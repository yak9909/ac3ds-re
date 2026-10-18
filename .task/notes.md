# 事前確認

- `precheck` に従い `kb.py search UI` / `画面` / `Layout`、カテゴリ索引と既存 topics を確認した。
- 未消化は `category: ui`、`state: active`、`consolidated_into` が空の17件。本文で未参照という意味ではない。ACNL-F0693/F0694/F0696〜F0708の15件は既に本文に参照がある（格付けA、MEDIUM）。残る旧記録はACNL-F0262/F0312（sourceあり、格付け?）。
- 既存のPicture・Material・TexMap節は#28の再解析（F0705〜F0708）を採用済み。構造を解析し直さず、記録本文との整合を確認して不足する条件だけを追記する。
- F0262は外部計測コードによるメモリ破損と復旧作業、F0312はChokistream/PowerShellの画面取得手順が中心。ゲームの事実として採用する旧主張はないため、topicsには入れない方向。旧観測を再認定せず、再解析したとの記録も作らない。
- 管理欄は変更しない。git/gh、IDB、実機は使用しない。

# 予算

- 利用枠の残量を示す道具はなく、`get_goal` はgoalなし・残量なし。数値で3割を保証できないため、既存再解析済み15件の照合と旧2件の採否判定に範囲を限定する。

# 経過

- 対象17件を全て `kb.py show` で確認。旧2件を採用せず、格付けAの15件のtopics対応を確認した。
- topicsに正常な未所属node・二重登録検査の限界、種類別loader容量と状態/種類更新の時差、UV出力数、自身の描画省略と子走査、子Pane/共有材質の所有条件を補足。
- F0262関連で `kb.py addr 0x566E30` を実行。書き出しとsymbolsを照合し、更新版code.binの当該関数56バイトをcodebytesで確認した。既定パスは作業ツリーから解決できず、`--code` に更新版の実ファイルを指定した。旧注入コードの停止PC付近は配置済みセグメント外で、再認定していない。
- 報告には17件の表、15件の統合提案、旧2件の非採用理由と未確認範囲を記入。新規記録やsupersedesは作成していない。
- `_local/evidence/91/ui-consolidation-check.json` に17件の抽出・報告行・topics参照の照合結果を保存。17行、参照15件、非採用2件が一致。
- `python tools/kb.py lint` は728件、エラーなし。auditの結果は報告を参照。
- `python tools/audit.py` は987ファイル・問題0件。通常実行の追跡済みファイルはインデックス内容なので、topics・notes・reportの実ファイルにもaudit.scan_fileを適用し3ファイル・問題0件を確認した。
