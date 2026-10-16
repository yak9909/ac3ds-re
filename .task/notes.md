# 事前確認

対象は F0253/F0259/F0261（いずれも ?）。前提は F0693〜F0701（A）。日本語「フェード」、英語 loader、コード/資源名 save_wait を kb search。対象アドレスは kb addr で既存記録・symbols・Issue を確認（作業中 Issue なし）。三パス二リスト、安定昇順挿入、保存長による再生、IDの再利用、manager容量は前提として使う。git/gh と実機操作は行わない。

# 確かめる主張

- F0253: Fade の上8/下9、通常0/フェード0x180、通常UIより後で最後、終了後の記録保持、再記録条件。
- F0259: 上8→10、loaderの save_wait 資源、Drawer変換、bucket計算、容量と主リスト値、提出保証の限界。
- F0261: 各停止標本とフェーズの意味、10/0x10の同一視、manager保持、IDと所有Layout、ゼロ長guardと画像源の二択。

旧実測の再現は静的IDBではできない。一次証拠が支持する構造と、再実測を要する標本値を分けて判定する。

# 完了時の経過

- 対象本文のアドレス46件（今回の主要関数を含む）のkb addr出力は `_local/evidence/26/precheck-addresses.txt`。
- 一次証拠は同フォルダの `ida-primary.txt` / `ida-followup.txt` / `ida-states.txt` / `ida-phases.txt` / `ida-final-evidence.txt`。採取スクリプトも同所。
- 状態表0x845FECのIdle/DispWait/Disp/CompelDispと資源表0x845FD8を確認。Fade/loaderとも0xFFで更新内のFade先行を確認。
- ID0x0Aのbucket=0xAD9904、0x10のbucket=0xAD991C。旧同ID照合は撤回し、旧current nodeの実値は未確認とした。
- F0702/F0703/F0704に全主張の判定を記載。supersedesはそれぞれF0259/F0261/F0253。topicsの対象節・優先度表・ゼロ長に関する関連行を更新。旧記録は無変更。
- 確認できた9関数を命名、guard/bucket/終了処理へコメント追加。export_symbols.pyで書き出し、事前コピーとのCSV比較で対象外の差分がないことを確認（symbols-diff.txt）。型の変更なし。
- 指定IDBはsave=Trueで保存後閉じ、export時の再オープンも閉鎖済み。作業フォルダにIDB一個だけでlock/workファイルなし。
- kb.py index更新後、kb.py lintは724件エラーなし。変更内容7ファイルをaudit.scan_fileで検査し問題0件。全体audit.pyは814ファイル・問題0件で完了。初回はnotes.mdのCRLFのみ指摘され、LFへ修正後に再実行した。
- git/ghを直接実行せず、実機操作なし。byは依頼どおりautoのまま。
