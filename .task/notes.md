# 事前確認

- Issue #98 のワーカー。git/gh は実行しない。実機操作は許可されていないため行わない。
- precheck: 指定19番地を kb.py addr、Layout / 描画 / GpuCmd / TextBox を kb.py search で検索。topics/acnl/ui.md を先読した。
- ACNL-F0693/F0694/F0699/F0700/F0701/F0705/F0706/F0707/F0708 は格付けAの既存静的再解析。上下リスト、record/replay、Picture/Material/Pane配置を再利用。F0326/F0318/F0333など旧記録は格付け?のため単独の根拠にしない。
- 書き出しは指定 commit 65293c69e61e182196200b92414beff86f647a98。現在の名称は symbols 優先。

# 作業メモ

- IDBは指定の ida/work/98/acnl_jpn_v15.i64 のみ使用。型適用時に idalib で開く。
- 一次証拠は全関数export、vtableのバイトは tools/codebytes.py のread_bytes経由。
- GpuCmd_SelectList は入力ID一つ（疑似Cの余分な引数に注意）。Genは件数と出力配列。FreeはR1を末尾呼出しへ引き継ぐ。
- Pane=0xD4、Picture=0x158、TextBox=0x108、Material=0x50。DrawInfoは0x8CでLayout+0x30内包。LayoutMgr文字作業体=+0x1C、Drawer=+0x364。
- 作業スクリプトと採取物は _local/evidence/98/ に置く。

# 反映・検証

- ACNL-F0709～F0713を作成。34型、24関数の型、4大域、8vtable型を指定IDBへ適用しsymbolsへ書き出した。
- ResFontは依頼の0x20ではなく0x18。通常確保0x18と、別クラスの埋込み+0x178～次欄+0x190が一致。
- vtable構造体の適用型は従来exportで落ちるため、既存globals形式でも保存し、import時にdword分解しない修正を加えた。型ヘッダの関数ポインタ宣言を監査が疑似Cと誤検出する点も、宣言だけを狭く区別した。
- 型/全命名offsetをIDAで検証、関連99テスト通過。kb.py lint全733件エラーなし。最終audit.pyは996ファイル問題0、変更後実ファイル48件も問題0。
- code.binからの新規検証IDB自動解析は待機が長いため停止。作業IDBを複製し8vtable型を消した後、全symbolsをimport/exportする往復確認は一致。8表の構造体型がsymbolsから復元され、5種類の表と261型も一致した。
- 完了。項目別の付与範囲・保留理由はreport.mdの表。正本IDB・実機には触れず、直接のgit/gh・コミット・pushはしていない。
