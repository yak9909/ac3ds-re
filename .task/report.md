（ワーカーの最終の返答を司令塔が保存した）
DONE_WITH_CONCERNS

（codex-bridge taiyo、gpt-6.1-sol / high。t20261121-190852-9。全文は codex-bridge の get_result）

- vc_DATAPOINTER（0x957ED4）を void *（MEDIUM、ACNL-F0777）。0x10A110〜118 で読んで vc_NPC_2_SETUP の message_data に渡す、0x12DBD4〜C38 の破棄が先頭として使い最後に 0 にする。
- 生成に 281 名（関数 176・大域 42・型 54・仮想表 9）を通した。初回の穴は関数 61・大域 1。23 関数の prototype と大域の型を足し、再生成は成功（ACNL-F0778）。ButtonActionControl_Ctor・SelectBase_Ctor・ButtonActionControl の 8 つ・SelectBase の 7 つ・UiAnim_Set・UiAnim_SetFrameToEnd・GpuCmd_Advance・GpuCmd_GetCurrentWritePtr・GpuCmd_CommitListAndCaptureDelta・script_WordRes_Ctor。
- 残り 38 関数は prototype が確かめられず残した（_local/evidence/162/results.md。26 は gohan の spec に前からある物）。
- lint 797 件エラーなし、audit 1060 ファイル問題 0。実機未検証。
