# 事前確認（2026-11-09、Issue 127）

- precheck を実施。対象 6 番地の `kb.py addr` で既存 symbols の名前なし・作業中 Issue なしを確認。しずえ／growth／KeepItems を検索した。
- topics は acnl/ui.md を確認。他カテゴリの topic は未作成。
- ACNL-F0023・F0388・F0567 は格付け ?。一次証拠として全関数書き出し（symbols_commit 4914ab98f271092df116b05c38a6183939b88b16）の命令と独立した呼び出し元を読む。
- 0x30C994 は無引数の住民日次処理ラッパー。Save_GetTownBase → sub_2FB33C (+0x29220) → +4 → Villager_DailyUpdateOnce(...,0,0)。0x956231 は本体の u8 ガード。入口で検査し、処理開始前に 1 にする（完了の保証ではない）。
- 0x309F18 はプレイヤーセーブ配列のポインタ一致で 0〜3、不一致または null で 4。
- 0x316392/0x316412 は Thumb BLX の先頭。真の次命令は 0x316396/0x316416。戻り番地という旧説明に注意。
- 指定 IDB コピー以外は開かない。git/gh は実行しない。

# 完了した解析と反映

- ACNL-F0749 に全対象を集約。ACNL-F0388 の第6引数 float 説だけを supersedes で訂正。
- Room_UseExit の第6引数は整数。5B5798第7引数→vc_RELOADFUNC第9引数→Room_RequestChange第6引数→Room_SetTransitionKind第5引数となり、0x605F38 の STRB で 0x94A3CE へ保存される。途中の VLDR/VSTR はビット転送。
- IDB コピーに5関数名・最初の3関数の型・u8大域名と型・根拠コメントを保存。
- 全 symbols を IDB 作業フォルダの symbols-export へ書き出し、対象6番地の行だけを作業ツリーへ反映。元からあったコード中の vc_NEVER_WILT_CALLER_4/3 ラベルを維持。
- 新規名: Villager_RunDailyUpdateOnce / PlayerSave_GetSlotIndex / Room_UseExit / Field_GrowUpWiltSaplingToItem3 / Field_GrowUpWiltSaplingToItem4 / g_VillagerDailyUpdateGuard。
- 2つの成長関数の範囲は各0x64、対象BLXの実先頭からの差は+0x4E、Thumb付きsymbols番地との差は+0x4D。4 byte全体の包含確認は双方PASS。
- 作業スクリプトと機械出力は指定 IDB コピーのフォルダに置いた。実機操作なし。
- 最終検査: python tools/audit.py は1031ファイル・問題0件、python tools/kb.py lint は768記録・エラーなし。作業ツリー実ファイルの追加監査も32ファイル・問題0件。
- 索引生成済み。symbols の行数メタデータも実数へ更新。5新規関数名の一意性、既存ラベル保持、2呼出命令全体の関数内包含を確認。
