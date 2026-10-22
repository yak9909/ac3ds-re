# 事前確認
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
