---
id: ACNL-F0564
aliases:
- IDA-unknown-F018
- V2-F018
title: 手紙の ID 種別 3=名前差し込み無しのプレイヤー・4=同住民・6=自分自身（2026-09-18、MEDIUM）
summary: '種別バイト（ID ブロック +0x30、手紙の宛先 +0x30・差出人 +0x64）: 1 プレイヤー、2 住民、3/4 はそれぞれ 1/2 を LetterId_DropNameTag 0x5CB85C が変えた値で、手紙テンプレートの本文展開後に名前差し込み位置（this+212）が負のとき宛先に適用（letter+0x26E=0 と対）。5 は ID なし（テンプレートの差出人はゼロクリア後に同関数で 5）。6 は自分自身＝未来の自分への手紙: 宛先選択 LetterU'
date: '2026-09-18'
category: actor
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6076508
- 1700956
tags:
- player
supersedes: []
source: IDA:work/FINDINGS.md:4260-4263
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F018: 手紙の ID 種別 3=名前差し込み無しのプレイヤー・4=同住民・6=自分自身（2026-09-18、MEDIUM）

種別バイト（ID ブロック +0x30、手紙の宛先 +0x30・差出人 +0x64）: 1 プレイヤー、2 住民、3/4 はそれぞれ 1/2 を LetterId_DropNameTag 0x5CB85C が変えた値で、手紙テンプレートの本文展開後に名前差し込み位置（this+212）が負のとき宛先に適用（letter+0x26E=0 と対）。5 は ID なし（テンプレートの差出人はゼロクリア後に同関数で 5）。6 は自分自身＝未来の自分への手紙: 宛先選択 LetterUi_ApplyAddressee 0x19F45C の 0 番が Letter_SetRecipientSelf で 6 にし、ヘッダを player+35146（Vapecord FutureLetterHeader と同じ並び）から取る。7 は自由な名前（24 文字）で特殊差出人番号 27 のときだけ表示、書く箇所未発見（LOW）。ゲーム自身の見出し（romfs SYS_2D_Mail、tools/msbt_dump.py）で独立に確認: 1/3→「〜さんへ」「〜より」（プレイヤー名）、2/4→住民名、6→「みらいのじぶんへ」「むかしの〜より」。読む側は 1≡3、2≡4 で扱う。プレイヤーが書く手紙の差出人は常に 1 で、差出人が 3 になる経路は見つからない。letter+0x271 は特殊差出人番号（はは・HHA・しずえ等、dword_888AAC）。IDA-unknown-F017 の判定条件は「差出人種別 1（安全側に 1/3/6）かつ差出人の町≠自分の町」で変わらず、+0x271≠0 を除外に足せる。反証条件: 実機でプレイヤーの手紙の差出人が 3 になる。根拠 work/evidence/mail_sender/README.md 追記・SYS_2D_Mail.txt・sender_kind_table.txt。

