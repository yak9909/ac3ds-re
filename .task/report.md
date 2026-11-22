（ワーカーの最終の返答を司令塔が保存した）
# #167 の報告（mycodex、gpt-6.1-sol / high）

記録 ACNL-F0783・F0784、symbols に反映（IDB の作業用コピーは共有が読み取り専用のため symbols に直接）。

- 0x006D5110 BsMenuTab_UpdateSingleExit: 引数はタブと index、戻りは整数。対象なし・後片付け完了で 1、更新中は 0。呼出元 0x6D4E5C は index 10 を渡す。地図の再生成はしない。
- 0x00565794 Fader_IsFadeOutComplete: 引数なし。上下の active なフェーダーがそれぞれ無いか状態 1 の時だけ 1。部屋命令の受付・退場完了は保証しない。
- 0x006D1E14 BsMenuMgr_ProcessRoomCommand: 引数は manager、戻りなし（R0 は経路ごとの残値）。
- 0x0074F2A0 ssys_co_FaderBase_GetState: 引数は FaderBase、戻りは状態。
- グローバル g_ActiveTopFader 0x0096F3F8・g_ActiveBottomFader 0x0096F3FC。
- 外から呼ぶ前提: タブの更新は対応するアニメを準備し、ゲームの直列の UI 更新の文脈で重複せずに呼ぶ。

未確認点: 実機、OS スレッド ID、index 10 以外の外部利用。
検査: lint 803 件エラーなし、index 成功、シンボル整合性 PASS、audit 問題 0。
