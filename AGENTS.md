# ac3ds-re の規則

『とびだせ どうぶつの森』（日本版、無印＋更新）と『ハッピーホームデザイナー』（日本版 v1.1）の解析の記録です。ゲームの事実だけを書きます（解析の結果を使う製品の設計や実装は書かない）。

## どの作業でも守る約束

- 回答や思考は日本語で行う。数値の変換・アドレスやサイズの計算は道具で行う（暗算しない）。
- 解析を始める前に、スキル `precheck` で既存の知見を引く。
- 確度: HIGH＝静的解析＋実測、MEDIUM＝互いに独立した複数の静的根拠、LOW＝仮説。LOW の段階では名前を付けず、コメントだけ入れる。
- 格付け C と ? の記録だけを根拠にしない（格付けは `python tools/kb.py show` と索引に出る）。
- 既存の記録は書き換えない。訂正は新しい記録で行う（`supersedes:`）。
- 記録は `python tools/kb.py new` で作る。書き方はスキル `record-finding`。
- 名前と型は `docs/naming.md` に従う。

## ワーカーとして呼ばれた場合（依頼文で「ワーカー」と言われたとき）

- 依頼文の作業ツリーと IDB の作業用コピーの中だけで作業する。正本の IDB は開かない。
- コミットしない。
- 報告はスキル `report` の形式で `.task/report.md` に書き、短い完了の知らせだけを返す。ファイルを書けない環境（Claude のサブエージェントなど）では、同じ形式で最終の返答として返す。

## 単独で作業する場合

- Issue と PR で作業し、`python tools/audit.py` と `python tools/kb.py lint` を通してからコミットする。
- 記録のモデル名は `python tools/kb.py stamp --self` で記入する。

## スキル（`skills/`）

`precheck`・`record-finding`・`rename-and-type`・`report`・`consolidate-category`・`reanalyze-record`・`dynamic-analysis`・`use-references`
