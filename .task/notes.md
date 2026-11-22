# #164 完了メモ（静的解析、実機未試験）

依頼文 .task/brief.md 全文→AGENTS.md読了。precheck/record-finding/report読了。
F0110/112–119、F0770–772、F0423とtopics/acnl/ui.mdを確認。旧記録unknown/gpt-6の格付け?に単独依存せず、元ARM/表で照合。
git/gh直接実行なし、IDB/実機/製品コードへの変更なし。

## 成果物
- topics/acnl/bottom-screen-widgets.md: 問1〜6、所有欄全体、11タブ、地図6種/部屋3種、命令と完了、チャット、部屋変化、旧版/現行0596153比較、未確認点。
- topics/acnl/ui.md: 新topicリンクと訂正。
- inbox/webchat/164/1.md〜4.md: record-finding受け箱形式。kb.py newはyaml不在で採番前に失敗。正式IDを捏造せずintake待ち。
- _local/evidence/164/: selected_functions.txt/additional_functions.txt/widget_functions.txt、xrefs.tsv、tables.json、widget_profiles.tsv、calculations.json、document-checks.json、tool-results.json、verify.py。

## 結論
通常静止フィールド: map0/other0/tab7→実退場待ち→tab2→18の0x01→7の0x02/TabSelect。
全actorを一命令で退場/完全復元する汎用APIは確認できない。chatはkeyboard/親Releaseとリストの寿命が別。
F0770の08/10排他を訂正。通常持ち物完了では0x18。keyboard button-in enter57CC9Cも10を立てるので「チャットで10は来ない」という旧F008コメントは不採用。
+496はReaction、+504はRandomHeadsUp。隠す対象の3欄だけを全表示物と同一視しない。

## 検証
codebytes.read_bytesによる元code.bin表を照合、SHA256=c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb。
profile534〜617の84件を出力。keyboard state851430のenter57CC9C/update57CA00を元bytesで確認。
bridge readbackでtopic問1〜6、4下書きのkeys順/見出し、PC絶対パス不在を確認しPASS。
kb addr j106/new j109/lint j112: ModuleNotFoundError yaml。py -3.12 j108: runtimeなし。
verify j110(1秒)/j111(60秒)はtables出力後のsubprocess列でtimeout、checks.jsonは未生成。表の出力は成立。
audit j113: 30秒timeout、stdout/stderrなし。audit合格とは報告しない。

## 未確認・再開する場合
topicの「未確認点」を起点にする。全map/部屋子の内部解放・+496別名経由全型・全特殊部屋・連打・チャット内容までの完全復帰は未確認。
必要なら依存環境でkb.py intake --issue 164、lint/auditを再実行。今回は製品修正/実機試験をしていない。
