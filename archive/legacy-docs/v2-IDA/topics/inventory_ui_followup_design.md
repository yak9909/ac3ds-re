# 持ち物UIの実機訂正 / IDA-gpt-6-F013・T016

担当: GPT-6。対象: JPN無印＋更新、原code.bin SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb。実機報告はT015で再現した症状の証拠であり、今回の修正版は実機未確認。

## 原因と設計

- pocket取得: 旧Actorはscreen list先頭だけを読んだ。native LoadStep 0x19F86Cは現行actorを0x9499ECへ登録し、Dispose 0x19FF4Cで解除する（原STR命令とも照合）。このsingletonを優先し、完全なscreen list走査をfallbackとする。vtableとdispose flagを検査する。旧単一head fixtureでは再入場の不具合を捕捉できなかった。
- 消去音: native DragIconControl cleanup 0x29B364はsource有効又はtarget groupのdrag許可を音の条件とする。icon更新がsourceを無効にし、trash自身のdragも禁止した場合は鳴らない。削除成功時に一度明示再生し、native cleanupには音0を渡す。無効sourceのdropを追加検証する。
- A決定: node StartDecide 0x2B6F34のみではBACのanimation待ちPMFが設定されない。0x2F6C28→0x2F6694→native wait cleanupを使い、完了後に青いdecide終端を復元する。取得は従来通り即要求し、同じA決定の完了で二重取得しない。別行選択・再A・解放時はpendingを処理する。旧fixtureはdecided flagを直書きし、本物のA入口を通さなかった。
- 選択肢: ROM SYS_2D_UI index43=たべる、index15=じめんにおく、index12=にがす。native builderのactionは順に16、0、15。dispatchの原ARMがtable 0x9499FCをaction*8で引き、action16→0x199AFC、action0→0x19AD30、action15→0x19C8A0。独立したROMラベルと索引コードを照合し、食べるをaction15とする仮説は却下。新2項目はnative dispatchへ渡し、既存行とcancelと6行容量を保つ。既存4項目のmask位置を保つ。
- メニュー: チャットコマンドとアイテム検索の表示をゲーム/キーボードへ移す。ラベルとhotkeyを維持する。保存は階層パスをキーにするため、同じ形式で保存した以前のrootパス2件も新配置へ復元する。以後は新パスで保存する。保存形式は変えない。
- フォント: 全58source検査で旧656codesには10literalの欠字。生成器から667codesへ更新、画素/CMAP/余白/範囲検証成功、欠字0。headerは手編集しない。今後はprebuildにもglyph検査を含める。

静的結論の確度はMEDIUM。GPU描画・資源負荷・実機の音/見た目は今回のPC検証でHIGHへ昇格させない。根拠はwork/evidence/gohan_inventory_ui_followup、成果物はartifacts/plugins/gohan_inventory_ui_followup1。正常版・旧配布版は保持する。実機/SD/main/中断整理は変更せず、Gitは完了後に一括保存。

PC検証中の訂正: 重複を削るためCommit内でSetOptionCountを再呼出しすると、既存row descriptorまで初期化される（F010原知見/DB注記とnative実行が一致）。descriptorコピー後の調整はheader count+8/cancel+192のみ更新する。native手のカーソル経路ではcleanupがfocusを保持するため、source=nullを無条件の正解とせず決定bit解除を検証する。

## 検証結果

最新build3/prebuild3（4334parser・71anchor・21CPP・glyph欠字0）/linked3/halfscroll2/runtime6終了0。runtimeは旧53＋新7case、native A入口→animation待ち→完了→青/即取得一度/再A/移動、複数screen actor・singleton寿命、disabledsource音一度、実フォルダ/hotkey/6checkbox、全64maskと4種既存row/実Word65/重複/6行/cancel、JPN PMF dispatch eat16/place0、旧root/新keyboard path復元を含む。過去fixtureの4項目期待と保持mask期待を6項目へ更新し、native Aアニメ完了後に次の独立touchを試す。最新公式XMLは121名・67func注記・13構造体・actionEnum・global名・T・全bytes/input/DB SHAを読戻し成功。成果物/source SHAと旧14版/正常版保持はmanifestを正とする。実機は未確認。
