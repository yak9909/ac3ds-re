# 事前確認

- 対象はIssue 100、作業用IDBのみ。git/ghは実行しない。実機操作なし。
- `precheck` で 0x5682DC/0x5686D4/0x567BC0/0x97C0B4、Layout/レイアウト/SsysMaLayoutNodeを検索。topics/acnl/ui.mdとACNL-F0709〜F0713を読了（全て格付けA）。ACNL-F0705もA。
- F0709: storageはcommand bytesとGX capacity。F0710: Material容量と件数、Pane番兵。F0711: font/batch部分型。F0712: Layout寸法とdraw_info。これらを使い、既存記録は変更しない。
- 追加対象のaddr/search出力は作業用IDBフォルダprecheck.txt。最初の子processは別Pythonでyaml不足、sys.executableへ直して再実行し完了。

# 進行

- 原本exportの生成commitは依頼どおり。Layout vtable 0x900608は7slot、+0x10はBuildで単一this型にしない。
- +F8はeye Z float、+FCはanimation flags。有効/画面指定説は反証。+114は再生state mask、+118はcommand bytes。
- default processor初期化は0x79B70C、相対初期化表0x93ECC8の値0xFFE5CA44から到達。start→0x1019D8が同表を全巡回する。TextWriter ctorは初期化しない。
- storageはnullチェックをせずbase+bytesへGXゼロ書込み。bool戻り値にしない。

# 完了時の状態

- ACNL-F0714〜F0720を新規作成。全てMEDIUM。型/関数/大域を作業用IDBへ反映し指定exporterで書出し済。柔軟配列3種も固定sizeofを変えずに検証。
- 原本56範囲と表データ、数値計算、型検証は作業用IDBフォルダのprimary.txt、primary-index.json、calculations.json、type-verification.json。
- audit.py初回はCRLF8件のみ、修正後の変更現物24ファイルでaudit.scan_file問題0。kb lintエラーなし。
- stamp --selfはAC3DS_MODEL無しで失敗。by:autoの仕上げをオーケストラへ依頼。
