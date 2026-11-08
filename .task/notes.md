# 事前確認と作業状況
- 依頼 #122。作業用 IDB のみ使用し、git/gh は実行しない。
- precheck: 0x303530/0x303404 は記録なし。0x2FEB60 は ACNL-F0106/F0592 (?)。0x955F8C 関連も ? のため一次証拠で追う。
- 貯金/checksum/vc_MONEYGET、メダル/tickets/AcnlPlayerInventoryFinanceF010 を検索。save topic は存在しない。ui topic の BellBox は種類の意味が未確認。
- 既存型 AcnlEncryptedValueF010、AcnlPlayerInventoryFinanceF010 がある。旧記録 ACNL-F0420 (?) の結論だけは採用せず書き出しを照合する。
- 書き出しは共有 _local/builds/acnl_jpn_v15/export (commit 4914ab98f271092df116b05c38a6183939b88b16)。ワークツリー内には未配置。
- 0x2FEB60: 引数 >=4 でローカル通信枠を選択。0..3 は指定枠。セーブ I/O 状態と不正枠で null。

## 完了
- ACNL-F0745..F0748 を作成。確度 MEDIUM、実機は操作していない。
- 3 関数: Save_DecryptValue / Save_EncryptValue / Save_GetPlayerByOnlineSlot。型 AcnlEncryptedValueF010 を再利用し、AcnlPlayerSave (0xA480) と AcnlGardenSavePrefix (0x6AE40 まで) を作成。全体の完全サイズは未確定。
- g_GardenSaveBasePtr の型も prefix ポインタにした。旧部分型の既存メンバーは変更なし。
- 暗号化 ARM 728 条件・加算 cap 境界4条件、型と prototype の compile-time 検証に成功。
- 作業用 IDB 保存後、export_symbols.py を evidence/122/idb-export へ出力し、対象行/型だけ symbols に反映。IDB が古いので他の新しい symbols を消さないための限定取込み。証拠は _local/evidence/122/ 以下。
- kb.py index 更新、kb.py lint --strict 成功。作業ファイル直接 audit は問題 0 件。通常 audit は最初の実行が修正前の notes の CRLF を読んだため再実行中。
- メダル・チケットの加算 cap は 99999。旧資料の 9999 とは異なる。UI 他経路の限界は未確認。
- stamp はワーカーのため by:auto のまま。司令塔の仕上げに委ねる。

- カブ配列の曜日名/AM-PM 対応は確認不足として明記し、確定とするのを取り下げた。配置・要素数・添字式は MEDIUM。

- 公開対象の作業ファイル全体を audit.scan_file で直接検査: 1028 ファイル、問題 0 件（audit_all_working_files.json）。通常 audit.py の再実行の完了待ち。

## 最終状態
- python tools/audit.py: 1028 ファイル、問題 0 件、終了 0。
- python tools/kb.py lint --strict: 766 件の記録、エラーなし、終了 0。
- 依頼の完了条件を満たす。実機未確認点は各記録の末尾に明記。
