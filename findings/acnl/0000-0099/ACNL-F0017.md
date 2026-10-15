---
id: ACNL-F0017
aliases:
- F-397
title: 'F-397: 予測モードにも複合候補の文節リストがある'
summary: HIGH（今回の未確定入力について）。実機「わたしはねこがすきです」はmode0/予測6件。
date: '2026-09-10'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1286356
- 1272020
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:118-135
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-397: 予測モードにも複合候補の文節リストがある

HIGH（今回の未確定入力について）。実機「わたしはねこがすきです」はmode0/予測6件。
表示先頭「私は猫が好きです」、UI対象全文11文字。従来mode1領域の文節数は0。
type0x1012に対する0x13A0D4（候補連結）と0x1368D4（読み連結）は独立に
engine+0x2D1C4/count+0x2E4ACを参照し、88-byte stride。engine=app+0x1518。
実機app+0x2E6DCに3record、app+0x2F9C4=3。原本0x150898で読み境界0,4,7,11。
PC独立予測の各recordとpointer/handle8 bytes以外一致。「私は/猫が/好きです」の
PC変換片を連結すると実機cacheと一致。mode1件数0を「文節情報なし」と一般化しない。
表記候補5件も実機recordを復号。本文DOCS/system_keyboard_prediction_segments.md。
実機辞書全状態の直接復号・他入力・UI編集操作への一般化は未完。

### F-396追記: 移設後の起動を利用者が確認

利用者は指定した未確定入力「わたしはねこがすきです」を保持していると報告。
移設版で内蔵キーボードが開いたことは確認済み。候補順・mode・文節状態の実機取得は未完了。
IDA状態照会のタイムアウトからクラッシュや停止状態は推定しない。

