# #169 作業メモ

## 事前確認

AGENTS/brief全文、precheck・record-finding・reportスキルを読んだ。依頼文の格付け付き索引、topics/acnl/bottom-screen-widgets.md、F0756/F0757/F0771/F0772/F0781/F0783/F0784を確認。C/?だけを根拠にしない。git/ghの直接実行、IDB変更なし。

## 結果と根拠

_local/evidence/169/analysis.mdに目的0〜5の詳細、全27登録状態の責任表、通常復帰列、trace全13行の説明。
states.tsv/check.jsonはcodebytes.read_bytesで得た原本状態表（全adjustor0）、SHA256一致、before/停止ダンプの値とマスク検算。
selected.txt/more-tabs.txt/flag-functions.txt/flag-uses.txtは書き出し抜粋（既存コメントは削除し一次命令・疑似Cを根拠とする）。map-out.mdは村地図全体Outと地図内リストの区別。
finding-general.md/finding-flags.mdは新規記録の本文。

結論: アニメ静止はcalc差替え時に後処理を失わない十分条件でない。13/24/25/26など静止した画面の終了監視にも復帰責任が残る。0x8080はチャット入場11が0x10待ちで保持した値で、正常完了ならEが0にする。n28で0へ、n49で3へ外部からcalcを差し替えたため、入場処理と後続復帰が失われた。停止ダンプ+6419=1/+6420=0も一致。
flags40は表示を伴う退場段の要否、80は準備完了通知。80はReleaseで消されず84残留を説明する。

## 未確認範囲

全画面型×全27状態の自然到達と全命令発行元、全補助子/地図型/特殊部屋は未確定。12/23の全入口、持ち物X直接起動の全閉じ方、正常チャットのM=0とキャンセル通しの新規実測はない。trace開始前の80生産元、ms3時刻、949D3Bが落ちる時刻は未確認。

## 検査の再開点

既定pythonはyaml/pip無し。Python310のpipから依存を_local/evidence/169/depsへ導入した（j48成功）。初期j41はimport失敗、j45はtimeout。
kb_work.pyは依存パスを加えkb.mainでprecheck各検索・addr/showとkb.py new相当を実行する。j49はtimeout_sec600で実行中。実行結果はget_command_resultで確認する。precheck.json/kb-create.txtと新規findings2件の存在を確認し、finish_records.pyで本文を入れkb lintを実行する。最後にtools/audit.pyを実行する。既存記録は変更しない。新規IDは固定しない。最終報告はreportスキル形式で、未確定範囲を残す。
