<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / network

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| ACNL-F0565 | 郵便ポストの手紙は「通信相手から」を判定できる／sub_6070CC・sub_606964 はデバッグ判定（2026-09-18、MEDIUM） | sub_6070CC/sub_606964（SaveIo_DbgIsWholeIo89A60/89B00）はセーブ入出力中のオフセット0・サイズ0x89A60/0x89B00を返すだけで、Save_GetTownBase等27/15か所で戻り値は使われない（アサート残骸、影響なし）。手紙640Bは Mailbox_WriteLetter 0x6F4454 のコピー区切りから +0x00 宛先PersonalID(0x2E)+種別+0x30、+0x34 差出人PersonalI | MEDIUM | ? |
| ACNL-F0582 | 通信パケット種別番号 `0x00`～`0x84` の受信表（2026-10-03、MEDIUM/一部LOW） | 対象は日本語版更新 `artifacts/update/exefs/code.bin`（SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`）。解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。`Net_DispatchPackets 0x627718` は6バイトヘッダの種別を `0x85` と比較し、`off_875B4C[種別]` から受信ハンドラを | MEDIUM | ? |
| ACNL-F0583 | 通信中の村データ転送と屋外再読み込みは別経路（2026-10-03、MEDIUM） | 解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。日本語版更新 `artifacts/update/exefs/code.bin`、SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。`sub_61F3DC` の状態6で参加者が遷移部屋96に揃うと、唯一の呼出し元から `sub_61FE5C` がホスト `TownBase` の `0x71880`（46 | MEDIUM | ? |
| ACNL-F0603 | オンラインで見た目を伝える経路 — 美容室状態 0xB9 と状態 0 の抜け、プロフィール丸ごとの転送（2026-10-06、MEDIUM: 静的のみ。実機・通信未検証） | 解析モデル opus-5.5。旧 F-66 / F-67（reference/old_project/RE/FINDINGS.md）と docs/topics/network_packets.md を前提に、受信側の処理を読み直した。 | MEDIUM | S |
