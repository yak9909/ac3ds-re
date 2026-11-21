# 162 作業メモ

precheck: kb addr 0x957ED4 は vc_DATAPOINTER size=4、型・記録なし。日本語/英語/旧名で検索、ACNL-F0755 (A)・ACNL-F0766 (A)、topics/acnl/ui.md を確認。追加23関数も kb addr の結果を evidence の precheck-added.log に保存。

完了した調査: vc_DATAPOINTER は sub_10A0E8 の 0x10A110–0x10A118 で値を LDR R0,[R0] して j_vc_NPC_2_SETUP に渡す。sub_12DAD4 はオブジェクトの欄を解体してゼロを書き戻す。void *、MEDIUM。ACNL-F0777。
共通UI23関数にprototype、コメント先頭にACNL-F0778を追加。正確な宣言と根拠は _local/evidence/162/changes.json と同記録にある。

生成: 元spec、依頼表34–88行の名前/ワイルドカード、旧ソース3ファイルの番地と一致する既存名を統合。281名（functions176/globals42/types54/vtables9）。全出所 manifest.json。初回は61関数prototypeなし+vc_DATAPOINTER型なし。最終は全spec生成成功（all.hpp）、38関数のprototypeなし警告だけ残存。holes-before.json / holes-after.json / results.md。生成器は元のスクリプトを読み込み、symbols入力だけ作業ツリーへ向けた。ファイル道具で見えない元specとスクリプトはコマンドで読み、参照コピーはevidence内。

記録は kb.py new で ACNL-F0777・ACNL-F0778 を作成。stamp --self はAC3DS_MODEL未設定で失敗、by:autoを維持。kb index は24ファイルを再生成。lintは797件エラーなし。
初回auditは記録中の23ABI宣言を逆コンパイラ出力と検知。記録は通常のC表記へ直し、正確なABIはsymbolsとevidenceに保持。再検査 j50 完了: lint exit0（797件エラーなし）、audit exit0（1060ファイル問題0件）。全コマンドtimeout1200秒。
gitコマンド未実行、commit/pushなし、IDB未使用、作業ファイルはevidence/162内。司令塔の次の確認点: 残存38関数の全ABI、実機、記録のモデル刻印。
