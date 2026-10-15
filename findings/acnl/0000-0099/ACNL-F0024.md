---
id: ACNL-F0024
aliases:
- F-383
title: 'F-383: 通常チャットのキーボード生成入口（2026-09-09）'
summary: MEDIUM。利用者指定でフレンドチャットを除外、通常チャットを対象にする。
date: '2026-09-09'
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9192100
- 9326880
- 1653312
- 1652880
- 1652908
- 1652912
tags:
- chat
- keyboard
supersedes: []
source: v1:RE/FINDINGS.md:235-255
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-383: 通常チャットのキーボード生成入口（2026-09-09）

MEDIUM。利用者指定でフレンドチャットを除外、通常チャットを対象にする。
詳細`DOCS/system_keyboard_normal_chat.md`。静的idalib/code.bin.i64と原本ARM入口6ケースで照合。実機/ビルドなし。

- RTTI `0x8C42A4`/名前`10BsMenuChat`/vtable `0x8E5120`からinit=`0x193A40`を特定。
  mode0/max32/output親+80を設定し、状態表848BC8のwindow In enter=`0x193890`を呼ぶ。
- **フック候補`0x001938AC: BL UiScreen_OpenById`**。R0=0x23E/R1=親/R2=0/R3=0。
  次の`0x1938B0`は`STR R0,[R4,#0xDC]`。親が子BsSkbを保持する契約を維持する。
- factory登録1D3A84とCreate51FD2Cから基準94FDBC/幅8を確認。entry950FB4→ctor7EA97C→193C90。
  screenId0x23F。メニュー表初期化787004でmenuId5に対応。BsMenuTab選択値6→byte85080C[6]=5も照合。
- 親のWait193764はresult2でsend、result1でwindow Out。send1938EC→218044で文字列を渡す。
  send Wait1939F4は入力とreadyを戻してWaitへ戻る。**確定後も同じキーボードで入力を継続**。
  F-382の「確定で子を閉じる」はフレンドチャット限定。通常チャットへ流用しない。
- 取消は状態表からenter193988→子virtual+0x44、calc1938D0→global94A654解除待ち。
  193988は未定義関数でdecompile失敗、原本assemblyで確認。
- `SYSTEM_KEYBOARD/verify_normal_chat_entry.py`はRTTI/factory/BL/LDRと原本入口を検査、6ケースPASS。
  証拠`evidence/normal_chat_static.json`/結果`verification_normal_chat_entry.json`。APIはモック、通信なし。
  全通常チャット状態遷移・物理操作の発火・APT起動/復帰は未検証。
- 初回入口は確定後の再入力では呼ばれないため、連続起動を実装する際は別途再入力状態との同期が必要。

