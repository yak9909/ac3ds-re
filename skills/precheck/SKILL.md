---
name: precheck
description: 解析を始める前に、対象のアドレス・話題について既存の記録・名前・作業中の Issue を引く手順。重複解析を防ぐ。
---

# 事前確認

1. `python tools/kb.py addr <アドレス>` で、名前・関係する記録・作業中の Issue を引く（対象のアドレスごと）。
2. `python tools/kb.py search <語>` で話題を引く。日本語・英語・コード上の名前の3つで引く（`docs/glossary.md` があれば、表記の揺れを広げる）。
3. 関係するカテゴリの `topics/<スコープ>/<カテゴリ>.md` を先に読み、根拠が要るときだけ findings を `kb.py show` で読む。
4. 分かったことを、作業メモ（`.task/notes.md`）の先頭に書く。既に結論がある物は、解析し直さずに使う（格付け C と ? の記録だけを根拠にしない）。
