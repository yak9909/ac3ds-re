# #169 再開後のメモ

## 確認済み

AGENTS/brief全文とprecheck・record-finding・reportスキルは前半で読了。同じ決まりを継続。git/ghの直接操作、コミット、IDB変更なし。既存知見はtopics/acnl/bottom-screen-widgets.mdと格付け付き記録で確認済み。C/?のコメントだけには依存しない。

最初の再検査（j57）は終了0。_local/evidence/169/verify-resumed-initial.json: lint805件エラーなし（知見索引古い警告のみ）、audit1069ファイル問題0。j61のreview.pyも終了0、原本のタブPMF群とBsMenuMain21状態をreview.jsonへ採録。

## 記録と結論

ACNL-F0785/F0786をkb.py newで作成済み。新しい本文はfinding-general.md/finding-flags.md。analysis.mdに目的0〜5、27登録状態、通常復帰の部分順序、trace全13行、最狭の限定条件。

再開後にcommand-writers.txt（直接xrefの全20生産/初期化関数）、supplement.md（命令入口、キャンセル通知、補助子の静止値）、review.json、resume-calculations.jsonを追加。普通チャットのnativeキャンセル生産枝は0x57B778。keyboard+4424非0かつ2ボタンindex0確定で949D3B=0、+4580=1、結果1を通知。constructorの既定+4424=1も確認。

中心の結論: アニメが終端に来ただけでは、最後のcalcによるbinding解除/S/M/通知処理が終わったとは言えない。さらに入退場が完了して画面が静止しても、13/24等には将来の終了監視と復帰責任が残る。共有値だけで一律にcalcを差し替えても後処理を失わないとは判断できない。0x8080は差し替え前の正常な入場準備値で、11のEと後続経路を外したため残った。flags40/80は全体の切替中フラグではない。

## 範囲の区別

全27行の登録と、その表にある命令契約/入口/待ち/副作用は記録。全画面型×状態の自然な同時到達は登録表だけから証明しない。12は定型PMF群に無く自然な入口未検出。23は命令10の入口があり、enter0x6D5804の原本24byteをcodebytesで確認済み（j65終了0）。M|=0xC0後NOPでBeginEnterへfall-throughする。enter23.jsonに採録。

全地図型/補助子/特殊部屋/持ち物X直接起動の全終了方法の通し実測はない。共有flagsの必要十分式を新設したとの主張はしない。trace n1より前の80生産元、ms3の時刻、キャンセル通知を各actorが読むフレーム順は未確認。

## 最後の検査

j65は終了0、表23を補完済み。verify.py resumed-final は本文2件を正式記録へ同期し、追加抜粋を採録し、kb.py index→lint→auditを実行しverify-resumed-final.jsonへ保存する。最終結果まで取得してからreportスキル形式で返す。報告は.task/report.mdへ自分では書かない。
