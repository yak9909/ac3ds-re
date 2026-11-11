# 事前確認と作業状況（Issue 146）

- `precheck` 実施。全38番地（関数18、列挙された変数は20）を `kb.py addr`、下画面/font/BsMenuTab/WordFix/touch/TextWriter を `kb.py search`。結果 `_local/evidence/146/precheck.txt`。`topics/acnl/ui.md` と依頼の19記録は `kb.py show` で確認（格付けを含む `_local/evidence/146/records.txt`）。C/?だけを根拠にせず、元の書き出しとcodebytesで独立確認する。
- 原本書き出し: 4914ab98f271092df116b05c38a6183939b88b16。現在名/型は symbols を優先。正本 IDB は開いていない。
- 適用スキル: precheck / use-references / rename-and-type / record-finding / idapython / report。
- 旧版ソースは依頼指定の外部 `_local/legacy-src/gohan-legacy` を読むだけ。ゲーム事実の記録に製品の設計は含めない。
- 根拠の重要な差: 6EDEE0 はPWorkListの候補一覧を構築（語取得だけではない）。316E7C/52B678/52B644 はメニューフローのcurrent request kind判定と+26=1による完了通知で、音再開という根拠なし。12D294 はフレーム末565B9Cへ向けたflush範囲登録で即時flushではない。4B4328はR2を読まないgroup検索。567EFCはvtable8FC104のgetter73CFEC→96F14CなのでBounding。
- 許可範囲はこの作業ツリーと work/146/acnl_jpn_v15.i64 のみ。実機操作なし。Git/ghコマンドは一切実行しない。依頼の git diff origin/main --stat は司令塔へ委ね、ここではbaselineハッシュとsymbolsの行比較で関係外差分を防ぐ。
- 変更前ファイルのハッシュ: `_local/evidence/146/baseline.json`。一時スクリプト/ダンプは同evidence内。

## 完了状況

- 全38番地を作業用IDBに命名・型付けし保存済み。関数18件すべてにprototype、変数20件すべてに型。命令u8・ポインタ型・インライン実体を区別。
- 記録はACNL-F0752〜F0763（12件）。各対象に同記録IDのコメントを付けた。旧記録・旧名付きの対象外番地は変更しない。新記録の管理項目はkb.py生成時のまま（ワーカーでは単独作業用stampを実行しない）。
- `apply_idb.py`で適用、公式`tools/sync/export_symbols.py`で同作業コピーからevidence内symbols_exportへ書き出した。`merge_symbols.py`は対象番地の行と新規4型だけを元symbolsへ組み込み、古いIDB由来の無関係な差分を除外する。
- `scope_check.json`: 関数18・変数20、既存の対象番地のコメント込み44行を採用。対象外の関数/変数/comment/vtable/lvars行の差分ゼロ。既存型の本文差分ゼロ。新型はAcnlTouchState / CameraViewPrefix / ScriptWordFix38 / SeadControllerMgrPrefixだけ。metaのcountsも実数へ更新。
- `saved_idb_check.json`: 保存後のIDBを開き直し38件の名前/型と4型のoffset/sizeを確認。正本IDBは開いていない。
- 原本code.binのSHA256一致、`codebytes.py`で読んだ72関数のARM命令とvtable/表を確認（`original_asm.txt`、`bytes.json`）。実機操作は行っていない。
- `python tools/audit.py`: 1045ファイル、問題0件（初回は著者が書いた型宣言表を疑似Cと検出したため、記録中のABI修飾子を省いて解消。symbolsのABIは維持）。`kb.py lint --strict --quiet`:成功。
- `check_worktree.py`による実際の作業内容監査は40変更ファイル、問題0件。変更はsymbols/acnl_jpn_v15と今回記録/関連する生成索引だけ。`.task/notes.md`以外の作業用ファイルはevidence内。`file_stat.json`はGitを使わない変更量の確認。
- `git diff origin/main --stat` はワーカー禁止規則により未実行。司令塔で実行すること。Git/ghコマンドは直接一度も実行していない。

## 未確認点と判断

- 全件MEDIUM（独立した複数の静的根拠）。新しい実測なし。+488の画面の実クラス、kind7/13のゲーム内名称、CloseSelectionFlagの全用途、prefixの全体サイズ・シーン越し寿命は未確認。
- 訂正: 0x949D1Eの3は作成中。Menu_AttachScreenNodeで3→1へ戻り、画面の有無は0x986500のノードheadと別に見る。0x986500は画面への直接ポインタではない。
- タブflag0x949D88のset条件はindex10、またはindex0かつ以前index!=-1と明記。「同じタブなら全て」ではない。
- 公開symbolsの型が無いmanager/Group/Bounding等にはvoid*を使用。ScriptWordFix38は100byte、ControllerMgrとCameraは観測範囲のprefixと注記。
- by管理項目とGit上の最終差分検査は司令塔へ。報告はこのnotesとは別に最終返答で返し、`.task/report.md`は書かない。
