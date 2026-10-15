---
name: rename-and-type
description: IDB の作業用コピーで関数・変数に名前・プロトタイプ・型（構造体・Enum）・コメントを付け、symbols の差分として書き出す手順。
---

# 名前と型

- 規則は `docs/naming.md`。確度 LOW の段階では名前を付けず、コメントだけ入れる。
- 作業は依頼された IDB の作業用コピーで行う（単独で作業するときは、正本から作ったコピー）。
- 名前・型を付けたら、その根拠の記録 ID を関数のコメントの先頭に `[ACNL-F0412]` の形で入れる。
- 既存の名前を変えるときは、変える理由の記録（`supersedes` 付き）を作る。
- 終わったら `python tools/sync/export_symbols.py --idb <コピー> --build <ビルド>` で symbols に書き出す（作業ツリーの `symbols/<ビルド>/` が更新される）。書き出した差分を `git diff --stat symbols/` で確かめる。
