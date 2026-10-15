<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / network

| ID | 題 | summary | 確度 | 格付け | 訂正 |
|---|---|---|---|---|---|
| ACNL-F0093 | F-55 Vapecord のコードを手がかりにした関数解析（時刻・部屋・通信） — `HIGH` | F-54 の対応表を使い、プラグインが実際に呼んでいる関数を本ビルドで解析した。 | HIGH | ? |  |
| ACNL-F0439 | 下位送信のBusyは未確認フレーム数、F008待機中拒否の再検証（2026-10-04、静的＋利用者実測） | F008試作で待機中にも`Net=1 Busy=1`が持続し、旧版では同じ接続内で複数回送信できたと利用者が確認。送信バッチ`0x62710C`は管理`+156+peer`のbyteを+1、受信下位ヘッダ低2bitの処理`0x62A0B4`は負deltaで減らす。これは未確認フレーム数であり、F008の「転送枠使用中」だけの解釈を訂正。`SendSegments`も同じゲートを呼ぶため、同じ瞬間の値1なら旧通常送信も失敗する。新事前呼出しが値1を作った証拠はなく、版差/タイミ |  | ? |  |
| ACNL-F0440 | 送信者の動作中に下位種別12が拒否される送信ゲート（2026-10-04、静的MEDIUM／回避未検証） | 利用者の2台では座標同期がホスト・ゲストの両方向で成立し、拒否は送信者本人の歩行・アクション中に起きる。受信相手の動作状態には依存しないとの訂正を優先する。個別宛先の`NetTransfer_SendSegments 0x616E10`は`NetTransfer_CanQueueForPeer 0x61849C`の拒否で0を返す。同関数は`enforcePeerMasks=1`なら相手別4マスクを検査し、0ならその4条件だけ省く。接続可能性とpeer転送枠のbusy検査は両モ |  | ? |  |
| ACNL-F0441 | 下位種別12の送信APIと2台同時接続時の座標宛先（2026-10-04、静的＋実測） | NEW 3DS LLとOLD 3DSを同じ村に同時接続した屋外で、両機とも `Town=0x31F49A80`、`XYZ=0x33099E50` と実測。Python計算で下位種別12の累積オフセットは `0x11514BA`、16B本文は `[u32 streamOffset, X, Y, Z]`。汎用 `NetTransfer_SendSegments 0x616E10` は町サイズで制限しないが、通常町送信 `0x61FE5C` は制限する。送信の9引数ABI、2Bヘッ |  | ? |  |
| ACNL-F0565 | 郵便ポストの手紙は「通信相手から」を判定できる／sub_6070CC・sub_606964 はデバッグ判定（2026-09-18、MEDIUM） | sub_6070CC/sub_606964（SaveIo_DbgIsWholeIo89A60/89B00）はセーブ入出力中のオフセット0・サイズ0x89A60/0x89B00を返すだけで、Save_GetTownBase等27/15か所で戻り値は使われない（アサート残骸、影響なし）。手紙640Bは Mailbox_WriteLetter 0x6F4454 のコピー区切りから +0x00 宛先PersonalID(0x2E)+種別+0x30、+0x34 差出人PersonalI | MEDIUM | ? |  |
| ACNL-F0582 | 通信パケット種別番号 `0x00`～`0x84` の受信表（2026-10-03、MEDIUM/一部LOW） | 対象は日本語版更新 `artifacts/update/exefs/code.bin`（SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`）。解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。`Net_DispatchPackets 0x627718` は6バイトヘッダの種別を `0x85` と比較し、`off_875B4C[種別]` から受信ハンドラを | MEDIUM | ? |  |
| ACNL-F0583 | 通信中の村データ転送と屋外再読み込みは別経路（2026-10-03、MEDIUM） | 解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。日本語版更新 `artifacts/update/exefs/code.bin`、SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。`sub_61F3DC` の状態6で参加者が遷移部屋96に揃うと、唯一の呼出し元から `sub_61FE5C` がホスト `TownBase` の `0x71880`（46 | MEDIUM | ? |  |
| ACNL-F0584 | 下位種別12の受信に町サイズ上限がない（2026-10-04、MEDIUM） | 解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。日本語版更新 `artifacts/update/exefs/code.bin`、SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。通常送信 `sub_61FE5C` は町全量 `0x71880` Bで止まるが、非ホスト受信 `sub_187030` は先頭4Bオフセットが `>=0x10EA` なら  | MEDIUM | ? |  |
| ACNL-F0585 | Pretendoの公表したACNL RCE対策は `0x81` 掲示板パケット（2026-10-04、MEDIUM） | 解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。対象は日本語版更新 `artifacts/update/exefs/code.bin`、SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。Pretendo Nimbusの[公開ソース](https://github.com/PretendoNetwork/nimbus/blob/fc2d813412a6 | MEDIUM | ? |  |
| ACNL-F0587 | 屋外XYZを下位 `0x0C` で書くための条件と副作用（2026-10-04、静的MEDIUM／実用性LOW） | 解析ソフト IDA（idalib-mcp）、解析モデル gpt-6-sol。対象は日本語版無印＋更新、原本SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。利用者指定の屋外XYZ `0x33099E50` は2026-09-18のgohan実機記録と、別日のプレイヤー実体 `0x33099E3C` に対する静的 `+0x14` が一致する。前回答の「実体の位置が不明」はこの屋外 |  | ? |  |
| ACNL-F0603 | オンラインで見た目を伝える経路 — 美容室状態 0xB9 と状態 0 の抜け、プロフィール丸ごとの転送（2026-10-06、MEDIUM: 静的のみ。実機・通信未検証） | 解析モデル opus-5.5。旧 F-66 / F-67（reference/old_project/RE/FINDINGS.md）と docs/topics/network_packets.md を前提に、受信側の処理を読み直した。 | MEDIUM | S |  |
| ACNL-F0605 | 目の形を通信相手へ伝える経路の調査（T020、2026-10-06、MEDIUM: 静的のみ。実装・実機なし） | 解析モデル opus-5.5。IDB: `sub_61F3DC`（参加時の転送の段階）/ `sub_51C720` / `vc_PLOAD` に注記（意味が LOW のものは改名しない）。 | MEDIUM | S |  |
| ACNL-F0607 | 0xAA7994 はホストの枠 — 自分のプレイヤーは [自分の通信番号]（2026-10-06、HIGH: 静的（vc_PLAYERINSTANCE の索引）＋実機の症状が一致） | 解析モデル opus-5.5。 | HIGH | S |  |
| ACNL-F0608 | 訪問者のプロフィールは固定領域にある（2026-10-06、HIGH: 静的 + 実機の症状が一致） | 解析モデル opus-5.5。 | HIGH | S |  |
