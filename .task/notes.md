# 事前確認
- 対象は ACNL-F0313/F0315/F0316/F0317/F0319/F0321（すべて格付け ?）。F0315 は F0316、F0321 の投影は F0696 の訂正を先に採用する。
- topics/acnl/ui.md を先読。日本語「材質」「マテリアル」、英語 TexMap、コード名 Picture を kb search で検索した。
- F0693〜F0704 の上下面別リスト、投影、記録要求・保存再生、ID再利用、容量の結論は前提として利用する。
- 全対象の addresses と本文の番地を kb addr で照会し、_local/evidence/28/precheck-addresses.txt に保存。作業中 Issue の照合はローカル索引にある範囲。
- IDB の既存名・コメントは証拠と数えず、命令・データ・xref を採取する。旧実機の画素・枚数・同番地再確保・連写結果は今回再実測しない。

# 確かめる主張
- F0313: Pictureサイズ/埋込Material、位置寸法/行列、状態送出とcursor、TexMap各欄/書式、色、外部依存なし/世代/ロード寿命、UVキャッシュ、優先度FFの最前面保証、旧実験の回数と画素。
- F0315: RTTI/継承、Picture/Materialサイズ別確保、Pane行列と一次値、過剰コピー、色7個、TexMapビットと派生、可変長ブロック/個数、アンカー、旧IDB注釈。
- F0316: accessor/vtableスロット、子リスト/可視、基底Layout記録/必要欄、DrawInfo使用範囲、Paneサイズ/派生投影、Materialの隣接確保、実データ標本。
- F0317: 木からの記録/画素/頂点色とTEV/UV省略、bit1早期return、容量と記録長、ロード後の寿命、外部実装のコード量。
- F0319: 共通allocatorとサイズ上限、材質共有、74枚/容量、解放、旧外部実装の手順。
- F0321: 独立した上下木とリンク、投影（F0696採用）、共有材質が読むだけ、detach/free/再確保、184枚/容量/同番地、alpha/キャプチャ/連写。

# 最終結果
- 全72番地の precheck を完了。旧動的番地や定数も含めて照会し、作業中Issueの競合はローカル索引で検出なし。
- IDB一次証拠を ida-primary/followup/lifetime/final/data/rtti/extra の各ファイルへ保存。主要11関数のoriginal byte照合ではパッチ差分なし。
- F0705: 別確保、Paneサイズ0xD4、容量による可変領域区切り、Alpha/Blend/TEVの順を確認・訂正。
- F0706: TexMap派生値、UV再計算、GPU側差分比較がアドレス/paramsのみであることを確認。
- F0707: 可視木とcursor、TEV分岐、bit1が状態発行だけを省く点、texMap数0のregが0x0FBである点を訂正。
- F0708: 共有UVフラグ更新、所有bit付き破棄、座標配列の独立解放、共有寿命の限定。旧184枚は算術上0xFE00で64KB内。
- F0315/F0316はゲーム側結論を全置換としてsupersedes。他4件は実機/外部実装の旧経過を再認定していないため主張ごとの部分訂正。
- 名前15件と注釈を作業用IDBへ反映して保存・閉鎖。新しい構造体/型は付けていない。symbolsはexport_symbolsで書出し、CSVの差分を証拠フォルダで比較（gitコマンド不使用）。
- byはautoのまま。実機操作・git/gh直接実行・コミットは行っていない。

# 検査
- tools/kb.py lint: 728件、エラーなし。索引再生成後は警告なし。
- tools/audit.py: 818ファイル、問題0件。
- 変更対象10ファイルの現物をaudit.scan_fileで直接検査: 問題0件（CLIがtrackedファイルをインデックスから読むため別途検査）。
- symbols差分: comments.csv/functions.csv/meta.tomlだけ。型定義・その他symbolsは変更なし。
- 作業用IDBフォルダはi64のみで、開いたままのDBファイルは残っていない。
