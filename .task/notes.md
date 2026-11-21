# Issue 154

## 結論（変更なし）
- 0x01 地図側入場開始、0x02 入場完了、0x04 退場完了/対象なし。manager+488・地図なしの代替通知を含む。確度MEDIUM。
- 状態7 0x6D6810はTST #2。F0756の「bit2確認」はマスク0x02への訂正を提案する。F0756本体は変更しない。
- 0x04セットは0x01を、0x02セットは0x04を保存するため、全書き手で下位3ビットが排他という断定は不可。
- フラグ行だけ省く場合とFinish全体を呼ばない場合を区別。残留と停止は状態・実体・他の書き手に依存する。
- 上位0x80/0x200の意味、0x84/0x82停止の全因果、部分更新版の実機挙動は未確認。

## 記録の正式化（利用者の続き指示）
- 指定Python: A:/Disassemble/ac3ds-workspace/_local/py/Scripts/python.exe。
- kb.py newを2回使用し、ACNL-F0771とACNL-F0772を作成。本文は元の下書きと一致することを検算済み。
- supersedesは両件とも空。F0756への部分的な指摘だけを本文に維持した。
- この作業の下書き2件を削除し、空になったinboxも削除済み。
- symbols/acnl_jpn_v15/types/local_types.hのコメントを周囲の /// [記録ID] MEDIUM; ... 形式に合わせ、F0771を参照。列挙値は変更なし。
- 手順と本文一致の結果は_local/evidence/154/formalize_records.pyおよびformalized_records.json。

## 検査
- 前回の書き出し検算: state7 TST #2、state6 ORR #0x20、enum 1/2/4、マスク表PASS、候補30関数。xrefは185行・185関数。
- 今回のlint: `A:/Disassemble/ac3ds-workspace/_local/py/Scripts/python.exe -B tools/kb.py lint`。終了コード0、791件の記録、エラーなし。findings/INDEX.md・findings/acnl/INDEX.md・findings/acnl/by-category/ui.mdの索引更新待ち警告3件。生成索引は変更していない。
- 今回のaudit: `A:/Disassemble/ac3ds-workspace/_local/py/Scripts/python.exe -B tools/audit.py`。上限1200秒で1回実行。終了コード0、1054ファイル、問題0件。
- 正式化コマンド・lint・auditはすべて終了状態を回収済み。
- git/ghの直接実行・gitへの書き込み・IDA/IDB操作は行っていない。作業ツリー外への書き込みを指定する操作は行っていない。

## 深い検証後の修正
- 依頼された各点をall_functions.txtで再確認した。
- F0771の0x01解除欄から0x22556Cを削除。0x225690のTST #1と0x225694のBNEにより、0x01が既に0の時だけ0x02を補う。0x225698のBIC #1は立っている0x01を落とす経路ではない。
- manager+488は部屋メニューBsMenuRoomMgr（命令byte_949D29）と明記。地図manager+484（byte_949D25）と完了通知を共有することをF0771・MenuFlagsコメントに追記。
- 0x6D4CB4の地図退場命令／地図なし完了と部屋メニュー退場命令の分岐、0x22556Cの状態名、0x225778の+488クリア、0x6D1E14の生成・命令処理を確認。
- 地図なし分岐で0x04を立てる0x1A0C64・0x1A0F80・0x6D6440の3例を追加。F0772、列挙名と値、F0756は変更していない。
- 今回の書き出し抜粋: _local/evidence/154/review_followup_exports.txt。
- 検査: A:/Disassemble/ac3ds-workspace/_local/py/Scripts/python.exe -B tools/kb.py lint。終了コード0、791件の記録、エラー・警告なし。
- 今回はauditを実行していない。gitへの書き込み・IDA/IDB操作なし。
