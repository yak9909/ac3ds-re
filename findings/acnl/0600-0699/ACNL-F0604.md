---
id: ACNL-F0604
aliases:
- IDA-opus-5.5-F088
title: '相手側のアクセサリーを残す状態 0xBA、送れなかった件（2026-10-06、MEDIUM: 静的のみ。gohan 未実機）'
summary: '解析モデル opus-5.5。IDB: `PlayerState_HeadGoodsExit 0x68A6AC` / `PlayerState_HeadGoodsSyncRemote 0x68C538`（関数を定義）を命名・注記。'
date: '2026-10-06'
category: actor
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6858412
- 6866232
- 6861368
- 8662048
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4672-4683
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F088: 相手側のアクセサリーを残す状態 0xBA、送れなかった件（2026-10-06、MEDIUM: 静的のみ。gohan 未実機）

解析モデル opus-5.5。IDB: `PlayerState_HeadGoodsExit 0x68A6AC` / `PlayerState_HeadGoodsSyncRemote 0x68C538`（関数を定義）を命名・注記。
- 実機（hhd_t017a）: 相手の見た目は変わらず、通知「通信相手へは送れませんでした」= 送信前の検査で止まり何も送っていない。2・6 PASS。
  **利用者の訂正: 相手側でアクセサリーが消えるのは許容していない**（許容したのは目の形を相手の建物の出入りで更新すること）。
- 状態 0xBA（美容室の小物の付け外し）: 引数 +14 帽子 / +18 アクセサリー（各 4 B）。入る = `Player_SetHeadGoodsWithSound 0x68B238`（控えへ写し、髪型の控えを写しの記録から、
  美容室の音 GROUP_SHOP）、抜ける = `PlayerState_HeadGoodsExit`（写しの +10 帽子 / +14 アクセサリーを書き戻す）、+0x18 = 同じく写しへ。
  → 0xB9 → 0xBA → 0 → 今の状態 の順なら、0xB9 の抜けが消したアクセサリーを 0xBA の抜けが戻してから状態 0 の抜けが vc_UPDATE する見込み。
- 止まった検査は未特定（理由番号を通知に出す版で確かめる）。けってい の時点はキャラクリを閉じ始めたところで、今の状態がまだ同期しない状態だった可能性が高い
  → gohan はけっていで予約し、ゲームと同じ条件がそろうまで最大 300 フレーム待って送る。
- F088 追記（2026-10-06）: hhd_t017b 実機 = 相手側のアクセサリー・帽子は残る（0xBA が効いた）。即時反映は不安定、通知は「送ります」のまま／理由 4 / 5。状態の属性表 `sub_64E960` = `0x842C20 + 10×状態`（同期 = +7 bit3、全 235 中 41）。**立ち止まり 6・移動 13 は同期しない**ので、今の状態が同期する状態になるのを待つとほぼ毎回打ち切られていた（送られていなかった）。着替えの状態 0x36（同期する）は受信側で写しの服を書き（`sub_68B054`）、旗 0x40 なら控えへ写して抜けで作り直す→ 着替えで反映されたのは、たまたま送られて写しの髪が更新されていた回と整合。対策: 待たずに送る（gohan 0c3036c、hhd_t017c_test）。

