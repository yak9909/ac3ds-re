# #164 修正メモ（2026-11-22）

AGENTS.md、precheck/report読了。レビュー164.mdは共有範囲から読めず、依頼文の要点を採用。
対象5文書を直接修正する明示指示に従う。F0770本文・symbols・製品コードは変更しない。
meta/models.tomlではF0770のsonnet-5.5、F0779〜F0782のgpt-6.1-solはいずれもA。
既存topicsとF0770/779〜782を読み、export all_functions.txtとxrefs.tsvのrg、symbolsのrg、旧版GameList.cppで再照合。
precheckのkb検索/addr/showは_local/evidence/164/revision_precheck.pyで実行、結果はrevision-precheck.txt。
作業根拠は_local/evidence/164/revision-evidence.json。

修正内容:
- §3とF0780: 命令11/2/2、タブcalc/adjustorとmask、地図/部屋参照0、manager+56→tab+6416更新ゲート、判定対象外を明記。
- §6: 旧版が部屋命令消費/+488消滅/再出現を待たない差(A)、byte_949D34の一時保留と書き手、sub_565794/+57ゲート。
- §6問題3: 旧版ShutdownのOffかつShown待ち（最大90回）とRestoringでもDrainedの対比。
- 対象本文の省略名をsymbolsの正式名へ統一。57CC9Cにはfunctionsの正式名を見つけられず番地とenterの記述を維持。
- F0782は08/10の説明だけの部分訂正、72294C ButtonActionControl_GetDecidedIndexの戻り値解析は訂正しないと明記。
未確認: 現行ソース/深いレビュー報告を今回再読できないため現行側3条件は依頼文、Drained等は前ワーカー結果による。実機未試験、確度MEDIUM。
通常pythonにyaml/pipなし。依頼に沿ってpip導入コマンドを試みたがpip自体がなく失敗。既存_local/evidence/164/venvにはPyYAML/filelockがあり、同venvで指定3検査を実行した。
検査結果:
- precheck検索/addr/show: 全件正常終了、格付けAを確認（revision-precheck.txt）。
- python tools/kb.py lint: 801件エラーなし、exit0。UI索引の古さの警告は次のindexで更新。
- python tools/kb.py index: 24ファイル生成、exit0。
- python tools/audit.py: 1066ファイル、問題0件、exit0。
- index後のlint再実行と修正5文書のaudit.scan_file: exit0、問題0件。
ログ: _local/evidence/164/revision-checks.json、revision-finalcheck.jsonと各txt。
git/ghの直接実行なし。audit.py等が内部で使う分はAGENTS.mdの例外に従う。新たに.taskへ置いたファイルはnotes.mdだけ。既存report.mdは変更していない。
