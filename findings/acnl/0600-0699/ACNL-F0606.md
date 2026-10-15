---
id: ACNL-F0606
aliases:
- IDA-opus-5.5-F090
title: '目の形を種別 11 で送る実装（T020、2026-10-06、MEDIUM: 静的のみ。gohan e85bac0 未実機）'
summary: '解析モデル opus-5.5。IDB: `sub_581FE0` に注記（プロフィール +21656 の 168 B（Mii まわり、状態 +168）を状態 1 → 2 の送る形にする。戻すのは `sub_582160`）。'
date: '2026-10-06'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9754180
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4697-4703
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F090: 目の形を種別 11 で送る実装（T020、2026-10-06、MEDIUM: 静的のみ。gohan e85bac0 未実機）

解析モデル opus-5.5。IDB: `sub_581FE0` に注記（プロフィール +21656 の 168 B（Mii まわり、状態 +168）を状態 1 → 2 の送る形にする。戻すのは `sub_582160`）。
- 利用者判断（2026-10-06）: sub_51D7E4 の選び直しは「ゲストの村から住人が引っ越してくる」イベント用の選出と思われ、乱数なので途中で選び直しても構わない → ホスト限定を外して実施。
- gohan: けってい で目の形が変わり通信中なら、手順 9 と同じ片と引数（`[0x94D644]`、宛先 4、プロフィール 42,112 B + 管理 +78388 の 50 B、種別 11、0, 1, 0）で送る。送る前に sub_581FE0、送信が受け付けられるか 300 フレームで打ち切ったら必ず sub_6BC270 で戻す。objdump で全引数を確認。通知に pf 0/1/2。
- 反証条件: 相手側で目の形が建物の出入り後も変わらない、相手のセーブ・住人に想定外の変化、送信後に通信が切れる・待ちが残る（未確認送信 Busy）。

