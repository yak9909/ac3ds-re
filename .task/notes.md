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
