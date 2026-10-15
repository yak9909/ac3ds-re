---
id: ACNL-F0260
aliases:
- F-235
title: 'F-235: `Frame_EndDrawPass1024` 主リスト末尾の手製 Drawer-state 版は安全な提出経路ではない — `MEDIUM`（静的＋実機失敗）'
summary: '`PATCHES/cave_tail_sprite.py` は `0x5A27C8` で、捕獲済み material と inline Drawer を用いて'
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5908424
- 1798844
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:13971-13991
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-235: `Frame_EndDrawPass1024` 主リスト末尾の手製 Drawer-state 版は安全な提出経路ではない — `MEDIUM`（静的＋実機失敗）

`PATCHES/cave_tail_sprite.py` は `0x5A27C8` で、捕獲済み material と inline Drawer を用いて
UI画像（スプライト）1枚を主リストに書く最小実験だった。branch / PC-relative literal / cave / BSS /
list base-ptr-end を停止中に機械監査し、stock `0x5A27C8` への別 software breakpoint では
同 boot で `PC=0x5A27C8, LR=0x1B72BC` を観測して入口到達も確認した。

しかし実機では画像は出ず、通常 Resume 後も画面更新だけが停止して音声は継続した。
直後に停止して uninstall し、hook 2語・LOG・cave 2範囲（各320 words）の stock/zero を
読み戻した。従ってこのケーブは**再適用禁止**とする。

静的にも `Frame_EndDrawPass1024` は guard 0 で即 return し、そこに有効な UI state が
自然に残ることを保証しない。`GpuCmd_SplitAndSubmit` の直接追加は F-201 の cursor
キャッシュ問題を再導入し得るため、この失敗版へ重ねて試してはいけない。

ただし、後から読んだ主リストにケーブ固有の `-120.0f` が見つからなかった事実だけでは、
list 切替後に読んだ可能性を除外できない。どの命令が表示停止を起こしたか、ケーブが描画
まで到達したかは未確定である。次は同一フレーム内の読み取り専用 trace を先に行う。

---

