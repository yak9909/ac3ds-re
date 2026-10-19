# 事前確認

- 依頼で kb addr 済み: 0x0053CDC4 / 0x0053CDF4 / 0x003534E0 / 0x009B7010 / 0x32C85A2D。追加で 0x003533D0 は該当名・記録なし。
- kb search: 入力 / input / sead_Controller_Calc。topics/acnl は ui.md のみ、input カテゴリの統合はない。
- 旧 ACNL-F0376・0377・0381 は全て格付け ?。根拠にせず書き出しの命令で再検証する。関連の F0378–0380、F0426–0427 も ? のため手がかりのみ。
- 書き出しは依頼指定の symbols_commit 65293c69e61e182196200b92414beff86f647a98。現 symbols に ControllerPrefixF005 と入力関数既存名あり。

# 確かめる主張

1. F0376: Controller/Wrapper の関係、ボタンとタッチの欄、53CDF4 の順序、旧holdを消さずに release が出ないか、ButtonActionNode の旗の範囲。
2. F0377: ゲーム側の遮断範囲、タッチとボタンは独立に塞げるか。旧製品の実装・過去の実機成功は今回の一次証拠ではない。
3. F0381: 3533D0→483020 の条件、SELECT/START の hold と edge 統合、読み替え前の三語からSELECTを消した際の挙動。

# 作業制約

- ワーカー。git/gh 不使用、実機操作の許可はないので静的のみ。
- 関数は指定 export から読む。IDB は指定 work/103 のコピーに名前・型を付ける時だけ開く。
- スクリプト・証拠はこのツリーの _local/evidence/103/ に置く。

# 最終状態

- 新3件 ACNL-F0721/0722/0723 はF0376/F0377/F0381をそれぞれsupersedes。旧記録は不変更。
- IDBコピーへ保存後、公式export_symbolsでsymbolsへ反映。名前・型のみで命令の変更はない。
- 元ARM replay: SELECT/STARTの16遷移、本体/Wrapperの旧状態処理3条件、二重pointer、28bitの保持カウンター消去PASS。人工producerを使うCPU検証であり実機ではない。
- サイズ/offset検証: PrefixF005=0x134、Controller部分=0x15C、Wrapper部分=0x194、Pad=0x10、Reader部分=0x32。保存後のexportとも一致。
- byte0x009778D8、旧プラグイン作業領域、旧実機objectの実アドレスは新規命名しない。
- 実行モデルの詳細名は環境に無い。問い合わせ未回答のため、明示された系列gpt-6で新3件にstamp。台帳上は?のままなので、正確な実行名の確認後にオーケストラで再stampする。
- 最終検証: `python tools/kb.py lint --strict` は743件・エラーなし。`python tools/audit.py` は1005ファイル・問題0件。さらに更新したsymbols/新記録/報告の実ファイル15件をaudit.scan_fileで検査し問題0件（audit通常実行は追跡済みファイルのindex内容を読むため補完した）。
- symbolsの事前snapshotとの比較で、変更は入力関連のコメント/関数、部分型、exportメタデータだけであり、globals/vtables/lvarsは一致した。
