# 事前確認

brief.md・precheck.md、AGENTS.md、skills/precheck・rename-and-type・report、docs/naming.md・symbols.md を全文読了。kb.py addr を両アドレス、search を「コマンドバッファ」「command buffer」「g_GpuCmdPtr」で実行済み。F0140・F0198 を kb.py show で照合（双方格付け ?）。C/? の記録だけに頼らず、下記の書き出し命令列を一次根拠とした。関連 topics/acnl/ui.md 先頭のカテゴリ方針を確認。render の topic は存在しない。

# 結論と反映

0x0096EA94 g_GpuCmdPtr と 0x0096EA98 g_GpuCmdEnd に unsigned int * を設定済み。名前・サイズ・既存コメント・その他の列は維持。型判断の確度 MEDIUM（複数の静的根拠）。既存 F0140 の実機観測は役割の補助根拠であり、新規実測なし。

- GpuCmd_SelectList 0x001216BC: 0x001217E8〜0x001217FC で base+offset / base+size をそれぞれ大域に保存。
- GpuCmd_SplitAndSubmit 0x001280CC: 0x00128108〜0x00128190 で unsigned 境界比較、STR/STM による32ビット語の書き込み、8バイトのカーソル更新（道具で 32/8=4 バイト、8/4=2語と計算）。指す先は管理構造体やGXキュー要素ではなくコマンド語。
- GpuCmd_Advance 0x001280B4: 引数はバイト数。ポインタ型にしてもこの API の引数単位を語数と読み替えない。
- GpuCmd_GetCurrentWritePtr 0x004D7164: 大域に保持した番地を返す。

書き出しの索引 symbols_commit は依頼指定のもの、該当関数ごとの書き出し元は index に記載の既存版。正本IDBは開かず、作業ツリー内 _local/evidence/172/gpucmd-types.i64 に複製して型だけ設定・保存した。指定Pythonに idapro がなかったため既設 IDA の idalib/python を import パスに追加。設定・一時ファイルの出力先も作業ツリー内。

tools/sync/export_symbols.py の export_globals が生成した対象2行の型を tools/sync/symlib.py の write_table で取り込み。全 symbols の前後バイト比較で globals/00900000.csv のみ変更された。最終アサーションは Windows のパス区切りだけで失敗したが、型反映は完了。別検証で対象2行を全列照合済み。apply_result.json と各ログは _local/evidence/172/。

# 検査

- tools/kb.py lint: 成功。803件、エラーなし。
- tools/audit.py 通常実行: 失敗。依頼資料 .task/brief.md / precheck.md の許可外ファイル2件と brief.md の Windows ユーザーパス1件、計3件のみ。資料を勝手に変更・削除せず維持。
- tools/audit.py --ci: 成功（j77, exit 0）。1066ファイル、問題0件。追跡対象の symbols を含めた検査。
- 初回の短い timeout_sec 指定は誤り。j70 は idapro import 前に失敗、symbols 未変更。その後の j73 で型反映完了。
- 重複した確認ジョブ j69 / j76 は結果取得待ち。必要な事前確認と lint / audit の結果は j74 および保存ログで取得済み。

依頼の範囲外の変更なし。新しい記録の作成や既存記録の訂正は行っていない。git・gh のコマンド直接実行なし（tools 内部での使用を除く）。
