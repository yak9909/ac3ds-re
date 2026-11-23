# 事前確認
司令塔のprecheck.mdとF0785/F0786、topics/acnl/bottom-screen-widgets.mdを参照。F0785の格付けAをkb showで確認。
既存の結論は再定義せず採用。共通命令はなく型別の後処理責任がある。

# #171 経過
依頼資料の全文と全13行traceを読み、関数書き出しを_local/evidence/171/functions.txtへ抽出。
解析本文は_local/evidence/171/analysis.md。核は、静止した通常チャットで949D3B byte0 + MENU_FLAGS word OR20が親/タブ双方を進める（MEDIUM、未実測）、通常メニューback静止はタブ命令3。
入場途中は一律安全ではなく、退場途中の再enterも避ける。キーボードcloseの実体57B238を追跡済み。
採番prepare.pyはジョブj101で実行中。完了後に新規記録本文を埋め、audit/lintを実行する。git/gh/IDBは未使用。
