---
id: ACNL-F0414
aliases:
- F-389
title: 'F-389: 実機SWKBDから「かんじ」の全17候補と順位を回収（2026-09-09）'
summary: '**confidence: HIGH（実機の表示cache・全候補record、原本ARMのローカル実行、F-363の独立PC実行を照合）。**'
date: '2026-09-09'
category: text
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1073764
- 1800064
- 1048576
- 1703936
- 1287204
tags:
- keyboard
supersedes: []
source: v1:RE/FINDINGS.md:24405-24435
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-389: 実機SWKBDから「かんじ」の全17候補と順位を回収（2026-09-09）

**confidence: HIGH（実機の表示cache・全候補record、原本ARMのローカル実行、F-363の独立PC実行を照合）。**

RosalinaでSWKBDをGDB port 4001へ割り当て、PID 60へ読み取り専用で接続した。
停止PCは`0x00106264`、`[0x001B7780]=0x08292880`。実行コード
`0x00100000..0x001A0000`の655,360 bytesは供給済み日本語SWKBDの同範囲と完全一致した。
app全域`0x69BC0` bytesと候補状態領域を別々に取得し、重複範囲も全バイト一致した。

入力長3、入力cache/変換入力ともに`かんじ`、全候補数17、選択index 0、表示件数6。
表示cacheから直接得た先頭6件は、`感じ / 頑丈 / 感情 / 元日 / 幹事 / 感じる`だった。

全候補recordは`app+0x30170`から88 bytes単位で17件存在した。index 0..13は、
実行時ポインタ/資源位置フィールドを除く全バイトがF-363のPC実行recordと同順で一致した。
index 14..16の種類`0x5832` recordは、取得appをローカルUnicornへ配置し、供給済み原本の
復号関数`0x13A424`を実行して`かんじ / カンジ / ｶﾝｼﾞ`を得た。全順位は次のとおり。

`感じ, 頑丈, 感情, 元日, 幹事, 感じる, 肝心, 勘定, 患者, 漢字, 監事, 寛治, 完治, 寛二, かんじ, カンジ, ｶﾝｼﾞ`

先頭6件は「実機表示cache」と「全候補record」の二経路で一致する。index 0..13はさらに
独立したPC実行と一致し、index 14..16は原本ARMによる復号で確定した。辞書handleは
index 0..13がデータソースslot 2/3（`njubase1.a`/`njubase2.a`）だけを指し、個人学習slot 0と
ユーザー辞書slot 1は含まれない。このためPC側14件との差は学習ではなく、実機表示列が
ひらがな・全角カタカナ・半角カタカナを追加することによる。

一次取得物は`SYSTEM_KEYBOARD/evidence/live_candidates_kanji*.bin`、機械検証済み結果は
`SYSTEM_KEYBOARD/evidence/live_candidates_kanji.json`。再現器
`SYSTEM_KEYBOARD/parse_live_candidate_dump.py`はサイズ、SHA-256、コード一致、app pointer、
UTF-16、件数、表示cache、候補record、原本ARM復号を検査してPASSした。対象への書込み、
breakpoint設置は行っておらず、各取得後にdetachしてSWKBDを再開した。文節境界は別状態である。

