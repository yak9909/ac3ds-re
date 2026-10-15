---
id: ACNL-F0023
aliases:
- F-391
title: 'F-391: case 0を含むしずえスキップ常設版（2026-09-09、使用禁止）'
summary: '**不採用。** case 0の呼出契約は有効だが、MITMフックの契約違反がある。'
date: '2026-09-09'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 3197332
- 6327788
- 9790001
- 5555236
- 5981772
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:209-234
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-391: case 0を含むしずえスキップ常設版（2026-09-09、使用禁止）

**不採用。** case 0の呼出契約は有効だが、MITMフックの契約違反がある。
F-390復元版の実機復活は利用者が確認済み。

- idalib `acnl_code`で`sub_30C994` (`0x0030C994`)を再解析。引数なしで
  `Save_GetTownBase`→`sub_2FB33C`→`sub_30C9BC(save+0x29224, 0)`へ進む。
  `sub_30C9BC`はThumb本体`sub_30C9C4`へのthunk。
- 独立証拠は、ModulePlSelect.cro case 0の`0x00BE6B34`と本体側`0x00608DEC`。
  どちらも直前にR0-R2を準備せず`sub_30C994`を呼ぶ。本体の別経路3本は
  `sub_30C9BC(save+0x29224, 0)`を直接呼び、内部契約とも一致する。
- `sub_30C9C4`は`0x00956231`が0、または強制引数が非0の時だけ一括処理を行う。
  常設版は番兵が0の場合だけ無引数wrapperを呼び、番兵が1になったことを確かめてから退出する。
- `Sources/ShizueSkip.cpp`は`Framework_ProcOneFrame` (`0x0054C424`, 素
  `0xE92D4070`)へMITMフックを置く。部屋0x63、既定OFF項目の適用値ON、30連続フレーム、
  guard/player index/room manager解決を条件にする。一括処理の前後で出口情報を再取得する。
- リンク後ARMでは`BLX 0x0030C994`→番兵再読→出口情報再取得→
  `BLX 0x005B464C`の順。後者の引数は`mgr, idx, 1, 0, 1, 1`。
- `PATCHES/verify_shizue_skip_integration.py`はソース契約、実機ダンプ入口語、
  メニュー/Simulator/フォント、OFF・待機・再入室を検査。ビルド前後ともPASS。
  既存検査も異常0、Simulator 49/49、キーボード10,943遷移/15場面PASS。
- 成果物846,115 bytes、SHA-256
  `de406a2187a8b7bb93606e65971bc37f1e44eb32dfd5d458a255147dca90f8f7`。
  利用者が実機へ適用し、自前メニューをONにした時点で画面停止・音継続を確認した。
  原因と修正版はF-392。**このSHAの成果物は使用禁止。**

