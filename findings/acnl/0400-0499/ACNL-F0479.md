---
id: ACNL-F0479
aliases:
- IDA-opus-5.5-F054
title: '模様替えの音は屋外では鳴らない（GROUP_HOUSE）と、選択窓の決定音が音程を上げる仕組み（2026-09-27、HIGH: 静的＋利用者の実機確認）'
summary: '解析ソフト: IDA（主 IDB）＋ BCSAR 索引（reference/old_project/SOUND）/ 解析モデル: opus-5.5。'
date: '2026-09-27'
category: sound
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9354556
- 2074536
- 2074732
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:1796-1810
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F054: 模様替えの音は屋外では鳴らない（GROUP_HOUSE）と、選択窓の決定音が音程を上げる仕組み（2026-09-27、HIGH: 静的＋利用者の実機確認）

解析ソフト: IDA（主 IDB）＋ BCSAR 索引（reference/old_project/SOUND）/ 解析モデル: opus-5.5。
- **SE_SYS_FUR_*（0x100051D〜0x1000528）は全部 GROUP_HOUSE**（BANK_SE_SYS_HOUSE_PLUS file 1460・SEQSET file 600・波形 WARC005 file 2245 = 668,792 B）。
  GROUP_STATIC / GROUP_VILLAGE のどちらにも入っていない（bcsar.group_members）→ 屋外で Game_PlaySound / sub_583068 / sub_5827D0 に渡しても鳴らない。
  実機: マップエディター（屋外）で範囲選択・解除・移動の音が鳴らず、GROUP_STATIC の一覧の音（0x10003C4 など）は鳴った（利用者 2026-09-27）。
- **SE_SYS_WIN_SELECT_ITEM_DECIDE 0x10003C5** の CSEQ（file 596 @2633）: `F0 81 1F 0001`（変数 31 に +1）→ `F0 90 1F 0000/0001`（比較）で 3 通りの呼び先
  （キー 0x4A/0x51 → 0x4C/0x53 → 0x4F/0x56）。鳴らすたびに音程が上がり 3 段目で止まる（利用者: 「埋める」を選ぶたびに上がる）。SE_SYS_DECIDE は変数を足さない。
- 屋外の同じ役割の音（GROUP_STATIC）: スクロールのつまみ SE_SYS_SCROLL_BAR_DRAG 0x10003A6 は sub_2993E4 が 1 行動くたびに sub_5827D0 で、
  持ち物のドラッグの SE_SYS_ITEM_SLOT_ACTIVE 0x1000405 は sub_1FFA80（ButtonActionNode 系 vtable 0x8EBD3C）が sub_5827D0 で鳴らす。
  ButtonActionNode の決定音 +204 は sub_71C338 が Game_PlaySound、フォーカス音 +208 は sub_71C1AC（+220 が真なら sub_5827D0）。
- 手カーソル: BsHandCursor_Show 0x1FA7A8 / Hide 0x1FA86C は BsMenuMgr +64 を 1 / 0 にする。ItemSelectWindow の閉じ終わり（sub_2BA2A0）は
  +1251（= +0x400 の +0xE3）が真かつ開く前の +64（+1249）が 1 なら Show、偽なら Hide。+1251 は ctor で 1、閉じ終わりで 1 に戻る。
- 反証条件: 屋外で SE_SYS_FUR_* が鳴る場面がある（GROUP_HOUSE が読まれている）。

