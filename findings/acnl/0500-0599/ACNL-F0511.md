---
id: ACNL-F0511
aliases:
- IDA-opus-5.5-F020
title: 建物の衝突判定 = 花を植えられない属性（byte_957A35 == 0）。利用者の正解と一致／プレビューが作れないのは親ヒープの断片化（2026-09-24、HIGH（利用者の正解と静的な表の一致）／HIGH（実機の読み取り））
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。利用者の正解: ベンチ 2x1、街灯 1x1、噴水 3x3、交番 [[1,1,1],[1,1,1],[1,1,1],[0,1,0]]（3x3 と下段中央の突起）。'
date: '2026-09-24'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 6083932
tags:
- heap
supersedes: []
source: IDA:work/FINDINGS.md:2424-2439
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F020: 建物の衝突判定 = 花を植えられない属性（byte_957A35 == 0）。利用者の正解と一致／プレビューが作れないのは親ヒープの断片化（2026-09-24、HIGH（利用者の正解と静的な表の一致）／HIGH（実機の読み取り））

解析ソフト: IDA / 解析モデル: opus-5.5。利用者の正解: ベンチ 2x1、街灯 1x1、噴水 3x3、交番 [[1,1,1],[1,1,1],[1,1,1],[0,1,0]]（3x3 と下段中央の突起）。

- 足元の属性コードごとの 7 表を並べると、正解と一致するのは **FieldAttr_CanPlantFlower 0x5CD55C = byte_957A35[code] が 0** のマスだけ
  - 塞ぐ: 0x02/0x03/0x04（本体）、0x11（交番の入口）、0xA2〜0xA5（噴水の四隅）、0x17（橋板）、0xA0（橋の角）
  - 塞がない: 0x05（ベンチ・街灯・噴水の外周）、0x31/0x32/0x33
- 物を置ける表 byte_957D32 & 2（FieldAttr_CanPlaceItem）は 0x05 を「置けない」とするので、混ぜるとベンチが 4x3 になる（F019 の誤り）。F017 の byte_957B34 も 0x05 を 2 とする
  - **訂正（F021）**: 0x05 は StampFootprint が属性を書き換えないコードなので、表で引くこと自体が誤り
- 塞ぐマスが無い 6 種（dobj_dummy / dobj_livehouse / fobj_flower_bed / fobj_sandbox / sobj_buoy / sobj_crossing）は、利用者の定義どおり範囲を一回り削る
- 反証条件: ほかの建物で利用者の見立てと食い違う

プレビュー（実機、読み取りのみ）: 役場 03 で `Failed / 2`（資源ヒープが作れない）。頼んだ 179,168 B（ファイル合計 79,392 B x2 + 16 KB）に対し、
親ヒープの空きは合計 306,824 B・**最大の塊 150,880 B**（4 塊）。ヒープは連続した塊にしか作れない → 見積もりを x1.5 + 16 KB に（gohan `95b817a`）。
Setup 後の資源ヒープの残りを Status::resourceSpare に記録し、x1.5 で足りるかを次の実機で確かめる。

