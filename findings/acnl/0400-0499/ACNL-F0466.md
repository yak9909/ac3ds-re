---
id: ACNL-F0466
aliases:
- IDA-opus-5.5-F067
title: 'メッセージのあと下画面にエディターが出ない — GameList が「隠した」と思い込んだまま、ゲームが戻した下画面をもう一度戻して止まる（2026-09-28、HIGH: 実機の値＋静的＋書き込みでの確認。経緯の一部は未確認）'
summary: '解析ソフト: IDA（主 IDB を idalib-mcp で静的、実機を ida-pro-mcp で動的）/ 解析モデル: opus-5.5。利用者報告: 蚊に刺される等のあと、マップエディターの下画面が出なくなった（実機 Suspend 済み）。'
date: '2026-09-28'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7171936
- 7159556
- 7172124
- 7148584
- 2828064
- 2828500
- 7159932
- 7172208
- 7163128
- 7161676
- 7170756
- 7165980
- 7166796
- 9739556
tags:
- message
supersedes: []
source: IDA:work/FINDINGS.md:1513-1533
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F067: メッセージのあと下画面にエディターが出ない — GameList が「隠した」と思い込んだまま、ゲームが戻した下画面をもう一度戻して止まる（2026-09-28、HIGH: 実機の値＋静的＋書き込みでの確認。経緯の一部は未確認）

解析ソフト: IDA（主 IDB を idalib-mcp で静的、実機を ida-pro-mcp で動的）/ 解析モデル: opus-5.5。利用者報告: 蚊に刺される等のあと、マップエディターの下画面が出なくなった（実機 Suspend 済み）。
- **実機の値**（走っている 3gx = ローカルの gohan.elf と FieldHidden のバイト一致）: GameList s_field = Restoring が 5163 フレーム、s_holdField = 1（エディターは s_want 0・Off）。
  ゲームのタブ = 状態 18「地図同期タブ入場」（calc 0x6D6F60 = MENU_FLAGS & 1 を待つ）、MENU_FLAGS = 0x2、地図の画面 +484 あり（状態 Proc）、+6578 = 0x81DF。
- **止まる仕組み（静的）**: 命令 2（GameList の kCmdRestoreField）→ BsMenuTab_ConsumeCommand 0x6D3F04 → 状態 18 enter 0x6D701C（屋外）= 地図命令 1。
  BsMenuMgr_ProcessMapCommand 0x6D1428 は地図 +484 が**既にある**と（+488 == 0）何もせず命令を 2 に戻すだけ。bit0 を立てるのは地図の In enter 0x2B2720（0x2B28D4）・
  0x6D407C・0x6D7070・0x6D4CF8 だけ（code.bin の走査）→ **地図が既にあるときに命令 2 を出すと状態 18 が永遠に待つ**。
- **確認（書き込み）**: MENU_FLAGS に bit0 だけ立てて 3 秒 → 状態 18 → 7 → タブ選択（0x6D474C）へ進んだ。続いて +6580（出入り中）= 0x1DF が残り FieldIdle が偽のまま。
  状態 7 enter 0x6D6AC4 は +6580 |= 0x3FF → BsMenuTab_BeginEnter 0x6D581C。タブが既に出ている（+6418 == 0）と sub_6D41B0 の道で 0x8000 を立てず、
  BsMenuTab_UpdateEnter 0x6D5B4C は 0x8000 が無ければ何もせず 1 を返すので出入り中のビットが残る。2026-09-25 の正常な復帰では Restoring が終わっていた
  → **命令 2 を出した時点でタブと地図はゲームが既に出していた**（二重に戻した）。
- **経緯（推定・未確認）**: メッセージのイベントの前後でゲームが自分で下画面（タブ・地図）を戻したが、GameList は Hidden のまま（Hidden では実物を見ていない）→ エディターを切って hide が偽 →
  Hidden → Restoring で命令 2 → 上の停止。★どの処理が戻したかは未特定（0x949D24 を書く所は 20 か所超）。FrameTrace の輪は FrameMark で上書き済みで経緯は取れなかった。
- **別の不具合**: MapEditor::Stop を盤面を組む前（Off / Loading）に呼ぶと DestroyAll が走らず s_holdField = 1 が残る → エディターを切っても下画面を隠し続けようとする。
- **その場の復旧（実機、利用者の確認待ち）**: タブ +6580 = 0（UpdateEnter の終わりと同じ。+6578 は既に含む）、s_holdField = 0、MENU_FLAGS を 2026-09-25 の正常値 0x2 に戻した
  → GameList = Shown、タブ = タブ選択。Chokistream が繋がっておらず画面は未確認。
- **直し方の案（未実装）**: (1) StepField の Hidden で実物を見る（タブ +6578 か地図 +484 が出ていれば Shown に戻し、まだ隠したいならもう一度隠す）。Restoring へは本当に隠れているときだけ。
  (2) FieldIdle の出入り中は 0x8000（アニメ中）が立っているときだけ忙しいとみなす（+6580 の他の使い手の確認が要る）。(3) Stop で組む前なら HoldField(false)。
- 反証条件: 直したあとも同じ手順で Restoring / 状態 18 に止まる。

