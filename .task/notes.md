# 事前確認と進行

- 対象は依頼の49関数とUiAnim/ArcResAccReader/InstSelect8。名前変更なし。git/ghは実行しない。
- precheck: 全49番地のkb.py addr結果は `_local/evidence/149/precheck.txt`。UiAnim/アニメーション/prototype/型/ArcResourceAccessor/InstSelectを検索、topics/acnl/ui.mdを読了。
- ACNL-F0754/F0755は格付けA。既存Layout/WordFix38の型とABIを使用。旧型UiAnimは28Bの途中まで、先頭resは実際にはvptr。
- 旧版資料は指定3ファイルのみ、未検証の手がかり。根拠は全関数export(4914ab98...)とcodebytes.py+Capstoneで読む原本命令列。実機操作なし。
- `_local/evidence/149/targets.json` は対象49件、symbols-beforeは変更前の全symbolsスナップショット。original-asm.txt/caller-asm.txtは原本code.bin由来、SHA256台帳一致。
- IDBは指定work/149/acnl_jpn_v15.i64のみを型適用のとき開く。functions/types/commentsの対象外差分を取り除き、既存コメントは後ろに追記する。

## 完了

- 対象49/49のprototypeを指定IDBへ適用・保存して閉じた。UiAnim=40B、ArcResAccReader=584B、InstSelect8=4812B。名前変更0、旧関数注記は全件前方一致で保持し根拠を末尾追記。
- symbolsの差分は49関数のprototype/confidence/refs、同49関数のfunc注記（既存20件に追記、新規29件）、上記3型のみ。globals/vtables/lvarsは全行一致、その他の関数・注記・型blockも一致。metaは件数の追随のみ。
- 記録はACNL-F0766（49関数ABI）、F0767（UiAnim）、F0768（ArcResAccReader）、F0769（InstSelect8）。kb.py newで作成し、AC3DS_MODEL=gpt-6を明示してstamp --self。台帳上の格付けは?なので司令塔のレビュー対象。
- `_local/evidence/149/verification.json` は保存後IDBとsymbolsの49prototype・名前・旧注記保持、型のサイズとoffsetの一致、変更21ファイルのaudit.scan_file成功を記録。`scope-result.json` は対象外差分0の検査結果。
- 最終検査: `python tools/kb.py index` 成功、`python tools/kb.py lint --quiet` exit 0、`python tools/audit.py` は1049ファイル・問題0件。作業ファイルを直接読むaudit.scan_fileも成功しており、インデックス内容のみの監査に依存していない。
- 新規補助スクリプトとスナップショットは全て `_local/evidence/149/`。旧資料、書き出し、正本IDBは変更なし。git/gh直接実行なし、実機操作なし。
- 独立した更新系戻り値の利用者が見つかればvoid戻りを再検討。opaque型・unk欄・TextWriter全構造・content_work要素の全構造は未確定。旧版予約0x74Bに対しnative TextWriterのローカル領域/コピーは0x64B。
