（ワーカーの最終の返答を司令塔が保存した）
## 未確認点

実際の IDB を使った復元試験は再実行していません。追加した同期関連の試験は **91 件すべて通過**し、`python tools/audit.py` と `python tools/kb.py lint` も通過しました。

全 `tools/tests` では、対象外の `test_refindex.py::test_addr_with_and_without_index` が 1 件失敗しました。参考資料の表示に関する期待値の差です。

## 迷った判断

参考扱いは、復元側にだけある関数のうち、`source` が `restore-test`、prototype が空、名前が `j_` で始まり、接頭辞と任意の連番を除いた名前が元の symbols に存在する場合に限りました。件数と全行を報告に残し、ほかの差は不一致のままです。

## 依頼の範囲外の変更

なし

## 使ったゲームの事実

なし
