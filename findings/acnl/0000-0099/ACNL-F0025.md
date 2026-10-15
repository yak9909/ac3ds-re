---
id: ACNL-F0025
aliases:
- F-382
title: 'F-382: とび森キーボード入口フックと結果返却の契約（2026-09-09）'
summary: MEDIUM。利用者依頼の2点を静的IDBと原本ARMのPC実行で確認。実機アクセスなし。
date: '2026-09-09'
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5409888
- 2810816
- 2811080
- 5385536
- 9797857
- 11338360
- 9797896
- 9797908
- 5380904
- 5747256
- 9741908
- 5754468
- 5754628
- 5371072
- 5765444
- 5386932
- 9797858
- 2420496
- 6087324
- 5520336
tags:
- keyboard
- hook
supersedes: []
source: v1:RE/FINDINGS.md:256-285
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-382: とび森キーボード入口フックと結果返却の契約（2026-09-09）

MEDIUM。利用者依頼の2点を静的IDBと原本ARMのPC実行で確認。実機アクセスなし。
詳細`DOCS/system_keyboard_game_hook.md`、メモ`scratchpad/MEMO_swkbd_game_hook.md`。

- `UiScreen_OpenById` (`0x00528C60`) のID `0x23E`が共通入口。
  返すのは文字列ではなくBsSkb子画面。親の後続書込み・仮想終了呼出しがあり、0/偽ポインタでは代替できない。
- 最小の返却契約を追えたのはBsMenuFriendChat（mode 3）。初期化`0x002AE3C0`、更新`0x002AE4C8`。
  上限32 UTF-16単位、2ボタン、改行なし、空/半角全角空白のみ不可。
- `0x00522D40`は起動ではなく完了通知。R0低byte→`0x009580E1`、
  R0!=0かつR1!=-1の場合だけR1→`0x00AD0278`。R1=-1は結果保持。
  チャットconsumerは1=取消、2=確定を処理し、-2/-1/3では終了状態へ進まない。
- 出力は`[0x00958108]`のUTF-16。`[0x00958114]`はRTTI `sys::TextManager`で、
  +8=長さ、+12=上限、+16=出力先、+20=カーソル、+4=LineManager。
  `0x00521B28`は1コード単位の挿入で文字数/終端/カーソル/行情報も更新する。単なるバッファコピーでは不十分。
- consumerは子のvtable+0x44（`0x0057B238`）へ終了要求後、`[0x0094A654]==0`を待つ。
  `0x0057CE64`→`0x0057CF04`→`0x0051F4C0`、generic lifecycle→`0x0057F944`が後始末。
  破棄時`0x005232B4`がTextManagerを破棄。出力所有フラグ`0x009580E2`が非0なら出力も解放する。
- 既存APT位置はUlcdFramework vtable+0x78（slot30）の`0x0024EF10`内から`0x005CE29C`へ。
  フレームはCalc→Draw→slot30。Calc走査`0x00543BD0`はnode+60が非0なら再帰ロックを保持する。
  入口にAPT待機を直挿入する安全性は未証明。入口で要求を記録し、初期化完了を待って既存APT位置へ渡す方針。
  実行時スレッドID/実際の保持ロック/受渡し同期は実機未確認。
- **PC原本ARM12ケースPASS**: 完了通知・確定/取消/未対応結果・子画面終了待ち・空白判定。
  `SYSTEM_KEYBOARD/verify_game_hook_contract.py`、`evidence/verification_game_hook.json`。
  送信・描画・OS等はモック。実際の通信、実機操作、ビルドはなし。
- 検証初回はROの状態記述子表欠落と未初期化子状態、続いて通知の-1契約の誤解を検出して修正。
  元コードの分岐とcalleeを照合し、成功条件を緩めず再実行した。
- 残件: ゲーム文字列制約を含む置換用TextManager更新、要求/結果の同期、元キー入力の抑止、
  既存APTの失敗回収・常駐配置。フック適用済み/安全な起動済みとはしていない。

