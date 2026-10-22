# 事前確認
- オーケストラの確認に従い、F0737/F0742のsupersedesを外す。型名更新とbitの名前づけの一部訂正を、report.mdにbefore/after/kind=partialのTSVで提案する。旧記録の結論・実測は有効。今回は記録の関係づけだけを直し、ゲームの再解析やIDB変更はしない。
- 依頼文の転載を事前確認資料として使用。指定 `_local/orchestrator/precheck/re-input-types.md` はこの作業ツリーには無い。
- ACNL-F0721/0722/0723 は格付け A、MEDIUM。入力経路・履歴・Wrapper・SELECT の条件付き統合は既存結論を使い、追加指定の点のみ一次書き出しと照合する。
- ACNL-F0379 は格付け ?。SELECT=0x800 の結論は根拠に採用せず、反証対象。ACNL-F0426 も ? のため単独根拠にしない。
- kb.py addr の対象は依頼文の9番地。日本語「入力」、英語 input、コード名 AcnlControllerPrefixF103 を検索。topics/acnl/input.md は無く、topics/acnl/ui.md に対象の統合は無い。
- 読み取り元: 全関数書き出し（commit 65293c69e61e182196200b92414beff86f647a98）。以後の名前は symbols を優先。
- 作業コピーのみ使用。git/gh は実行しない。実機操作をしない。

# 照合中
- 0x003534C8 は全体ゼロ化分岐（0x003534B4..C4）の合流後。SELECT読み替えの後ではなく前。失敗経路はこの点を通らない。
- 0x00540870 は pad 成功 bit0 が偽ならボタン/軸更新を飛ばす。一方 touch 成功 bit1 が真なら SetPointerState は保持の pointer bit を更新し得る。
- START pad0x8 -> held0x800、SELECT pad0x4 -> held0x1000。旧実測の0x8は統合後の装置キャッシュの観測と整合。

# 完了時の検証
- 入力9型を作業コピーで改名。旧型名0件、関数型13件、コメント14件、宣言レイアウト不変を確認。
- 記録は ACNL-F0737〜F0742。by:autoはオーケストラがstampする。
- 作業コピーの無関係な既存差分をsymbolsに混ぜないよう、全書出しをevidenceへ保持した上で対象変更だけ採用。
- tools/audit.pyとkb.py lintの結果はreport.mdに追記する。

- 最終検査: audit 開始時の1023ファイルでは旧notes.mdのCRLFを1件検出。LF修正後、同じscan_fileで現在の全1024ファイルを再監査し問題0件、kb lint761件エラーなし。

# 深い検証の指摘の修正（fix109b）: 中断時点の状態（利用枠 90% で区切った）
完了:
- 証拠を作業場 A:\Disassemble\ac3ds-workspace\_local\evidence\109\ へ移し、作業ツリー内の _local\ を削除。記録の参照パス（_local/evidence/109/...）は作業場基準で正しい。
- 作業用 IDB: pointer_flags を unsigned int（コメントに AcnlPointerFlags_* の旗と明記）、unk_12C を float[2]、AcnlControllerOffsetList を SeadOffsetList（node_offset を offset）、seed_previous_held を bool resync_previous_held_pending に変更。大きさは全て不変（Base 0x134, Prefix 0x15C, Wrapper 0x194, OffsetList 0x10, PadReader 0x32）。set_udm_type で pragma pack(2) が落ちたため C 宣言から作り直した（fix_pack.py）。layout_after.json に全メンバー位置を保存。
- symbols: types/local_types.h を作業用 IDB の書き出し（evidence/109/symbols_export2）の該当ブロックで差し替え（apply_header.py）。comments/00500000.csv 行 311 の wrappers.node_offset を wrappers.offset に。旧名の残存 0 件。
- enum を欄の型に使う型は他に無い（9 型と依存型は AcnlPointerFlags だけ）。
未了（次の担当）:
1. arm-none-eabi-g++（C:\devkitPro\devkitARM\bin）で、local_types.h の該当ブロックから作ったテストを -fno-short-enums 無し・有りの両方で通し、layout_after.json の全メンバーの offsetof・sizeof が一致する事を evidence/109 に残す（evidence/109-review/layout_test.cpp と同じ方法）。
2. ACNL-F0737 本文に、上の直しと派生コンパイラでの確認を書き足す（根拠表の AcnlControllerOffsetListF103 -> SeadOffsetList、メンバー名の更新含む）。F0737 と報告の AcnlControllerOffsetList・seed_previous_held・node_offset の表記も直す。
3. python tools/kb.py lint と python tools/audit.py（_local/venv/tools/Scripts/python.exe を使う）、.task/report.md の更新。
