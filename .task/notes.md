事前確認: precheck で対象4番地と復元/restore/import_symbolsを検索。関数3件に関連記録なし。ItemID の既存知見はあるが、今回はゲームの再解析はせず同期処理だけを修正する。docs/symbols.md の関数サイズ・Thumb下位ビット規約を採用。正本IDBは開かない。
最終検証: 両restore一致（不一致0・失敗0）。ACNLのみ未ロード関数5/コメント5を保持。pytest114件成功。大域の根因は型適用ではなくexportのNames限定走査。詳細はreport.mdとevidence/20/*_final.log/json。全IDB閉鎖済み。
