# #167 作業メモ

## 既存知見の事前確認
brief.md 全文、AGENTS.md、precheck / record-finding / rename-and-type / report、docs/naming.md、topics/acnl/bottom-screen-widgets.md と gohan の blocked.md を読んだ。
既定Pythonのyaml/pip不在を解決し、PyYAMLとfilelockを _local/evidence/167/deps に導入した。
kb.py addr 4件、search 日本語/英語/コード名、show F0772/F0780/F0766 はすべて終了0。結果は _local/evidence/167/precheck.json。3記録はいずれも格付けA。対象関数の既存定義なし。

## 結論と反映
- ACNL-F0783: 0x006D5110 BsMenuTab_UpdateSingleExit（型はsymbols参照）。対象なし/後片付け完了1、進行中0。stock はindex10。地図再生成・遷移は含まない。
- ACNL-F0784: 0x00565794 Fader_IsFadeOutComplete（型はsymbols参照）。上下activeフェーダーがnullまたは状態1（fade-out完了）の時のみ1。単なる非遷移判定ではない。
- 0x006D1E14 BsMenuMgr_ProcessRoomCommand（型はsymbols参照）。返値に受付/完了の契約なし。
- 0x0074F2A0 ssys_co_FaderBase_GetState（型はsymbols参照）。全4vtableの+12から参照し、LDRB R0,[R0,#5]; BX LR。
- g_ActiveTopFader 0x96F3F8 / g_ActiveBottomFader 0x96F3FC、型struct FaderBase *。
- IDBコピーは共有がread-onlyなのでsymbolsに直接反映。既存名の変更なし。関数コメント先頭に根拠IDを付けた。
- 部屋ゲート通過だけで命令受付/退場完了を保証しない。外部更新は初期化済み・生存中・対応アニメ準備済み、ゲームの直列UI更新文脈で重複せず進める条件。スレッドID・実機追試なし。確度MEDIUM。
- byはnewのautoのまま。stamp --selfはAC3DS_MODEL未設定で終了2（ワーカーの仕上げで司令塔がモデル名を記入する）。

## 検査
完了。index は24ファイル生成、最終lintは803記録で警告・エラーなし。symbols/refs/vtable/precheck の整合性PASS。初回auditは支給brief2件とprototype誤検出2件で失敗。誤検出は記述整理で修正。actual_audit.pyで支給briefだけを除く1067実ファイルを同じaudit規則で検査し問題0、終了0。最終lintも終了0。結果は checks.json・final-lint.json・actual-audit.json。
作業過程のスクリプト名inspect.pyは標準ライブラリと衝突したためgather_evidence.pyへ改名済み。

## 制約
git / gh のコマンドは実行していない。kb.py / audit.py の内部処理のみ。既存記録・topicsは未変更。作業ファイルは _local/evidence/167/。.task/report.md は作らない。
