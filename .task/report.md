（ワーカーの最終の返答を司令塔が保存した）
DONE_WITH_CONCERNS

（codex-bridge taiyo、gpt-6.1-sol / medium。t20261121-184239-7）

CommonScrollBar +0x6FB に unsigned __int8 drag_blocked_this_frame（ACNL-F0776、MEDIUM）。0x2990E0 で 1、UpdateDrag 0x298674..84 で +0x6FA==0 か +0x6FB==1 ならドラッグを進めない、0x299C54..5C で次の Update の頭で消す。実機未検証。どの入力で 0x2990E0 の関数が呼ばれるかは未確定。lint 795 件エラーなし、audit 問題 0。
