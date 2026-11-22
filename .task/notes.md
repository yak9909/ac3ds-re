# #167 作業メモ

## 訂正作業（2026-11-23）
precheck / report と docs/naming.md、topics/acnl/ui.md を読了。既存 precheck.json の A 格付けの知見を参照し、追加 precheck を recheck-precheck.json へ採録済み（全12件終了0、F0783/F0784/F0772は格付けA）。
F0783: enter 相当の準備後の毎フレーム更新と明記。bit10不在の無処理成功、別アニメの完了判定、group[10] の入場側利用、フラグ復帰とbit10設定元の未確認点、literal poolを除くサイズを追記。
F0784: ctor mode=1 と sub_5658E8 による状態1の直接設定を追記し、実際のfade-out履歴を保証しないと明記。getterを既存クラス命名に合わせ FaderBase_GetState に訂正。symbolsコメントも同期。
根拠: 指定 export の命令列・xref。追加採録先は _local/evidence/167/recheck-*。git / gh コマンドは使わない。
既存 .task/report.md は指定に合わせ _local/evidence/167/previous-report.md に移動。

訂正後の検査: kb.py index 終了0（24ファイル生成）。最終 kb.py lint 終了0（803記録、警告・エラーなし）。tools/audit.py 終了0（1068ファイル、問題0）。実作業ファイルへの同規則の補助auditも終了0（1067ファイル、問題0）。結果: recheck-checks.json / recheck-finish.json / recheck-actual-audit.json。最初の一括ジョブは300秒で打ち切られたが、残りのauditと最終lintを別ジョブで完了した。指定rgの検索・追加採録・検算も終了0。

以下は前回作業の履歴。

## 既存知見の事前確認
brief.md 全文、AGENTS.md、precheck / record-finding / rename-and-type / report、docs/naming.md、topics/acnl/bottom-screen-widgets.md と gohan の blocked.md を読んだ。
既定Pythonのyaml/pip不在を解決し、PyYAMLとfilelockを _local/evidence/167/deps に導入した。
kb.py addr 4件、search 日本語/英語/コード名、show F0772/F0780/F0766 はすべて終了0。結果は _local/evidence/167/precheck.json。3記録はいずれも格付けA。対象関数の既存定義なし。

## 結論と反映
- ACNL-F0783: 0x006D5110 BsMenuTab_UpdateSingleExit（型はsymbols参照）。対象なし/後片付け完了1、進行中0。stock はindex10。地図再生成・遷移は含まない。
- ACNL-F0784: 0x00565794 Fader_IsFadeOutComplete（型はsymbols参照）。上下activeフェーダーがnullまたは状態1（fade-out完了）の時のみ1。単なる非遷移判定ではない。
- 0x006D1E14 BsMenuMgr_ProcessRoomCommand（型はsymbols参照）。返値に受付/完了の契約なし。
- 0x0074F2A0 FaderBase_GetState（型はsymbols参照）。全4vtableの+12から参照し、LDRB R0,[R0,#5]; BX LR。
- g_ActiveTopFader 0x96F3F8 / g_ActiveBottomFader 0x96F3FC、型struct FaderBase *。
- IDBコピーは共有がread-onlyなのでsymbolsに直接反映。既存名の変更なし。関数コメント先頭に根拠IDを付けた。
- 部屋ゲート通過だけで命令受付/退場完了を保証しない。外部更新は初期化済み・生存中・対応アニメ準備済み、ゲームの直列UI更新文脈で重複せず進める条件。スレッドID・実機追試なし。確度MEDIUM。
- byはnewのautoのまま。stamp --selfはAC3DS_MODEL未設定で終了2（ワーカーの仕上げで司令塔がモデル名を記入する）。

## 検査
完了。index は24ファイル生成、最終lintは803記録で警告・エラーなし。symbols/refs/vtable/precheck の整合性PASS。初回auditは支給brief2件とprototype誤検出2件で失敗。誤検出は記述整理で修正。actual_audit.pyで支給briefだけを除く1067実ファイルを同じaudit規則で検査し問題0、終了0。最終lintも終了0。結果は checks.json・final-lint.json・actual-audit.json。
作業過程のスクリプト名inspect.pyは標準ライブラリと衝突したためgather_evidence.pyへ改名済み。

## 制約
git / gh のコマンドは実行していない。kb.py / audit.py の内部処理のみ。既存記録・topicsは未変更。作業ファイルは _local/evidence/167/。.task/report.md は作らない。
