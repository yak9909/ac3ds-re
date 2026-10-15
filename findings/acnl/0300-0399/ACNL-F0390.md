---
id: ACNL-F0390
aliases:
- F-363
title: 'F-363: 内蔵キーボードの候補順位・文節変換・学習を原本ARMで再現（2026-09-08）'
summary: '**confidence: MEDIUM。** SWKBD専用idalib IDBの静的解析＋PC上のUnicorn実行。'
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1253708
- 1366624
- 1473440
- 1474296
- 1472696
- 1691652
- 1234264
- 1131948
- 1233692
- 1268104
- 1272308
- 1366024
- 1352468
- 1352028
- 1473744
- 1122260
- 1381960
tags:
- keyboard
supersedes: []
source: v1:RE/FINDINGS.md:23664-23713
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-363: 内蔵キーボードの候補順位・文節変換・学習を原本ARMで再現（2026-09-08）

**confidence: MEDIUM。** SWKBD専用idalib IDBの静的解析＋PC上のUnicorn実行。
実機のUI・学習状態を観測したものではない。ビルド・実機書込み・再開なし。
対象原本・辞書はF-362と同じ。自前メニュー/gohan.3gxへの組み込みを前提としない。

### 結論と根拠

- **順位は段階別。** `0x13214C`が候補を列挙、`0x14DA60`が予測から追加検索へ遷移、
  `0x167BA0`が表示文字列の重複を除く。
  PC再現で「かんじ」は「感じ」261など予測9件の後、「漢字」419などを返した。
  単一のスコア降順ではない。曖昧一致を外すと「頑丈」「元日」が消える。
- **頻度・品詞の位置を解明。** `0x167EF8`は単語ごとの別表2バイトから下位6ビットを読み、
  10バイト単語レコード末尾2バイトは前後品詞表の索引として使う。
  主要辞書75,770件×2モードの151,540回を原本ARMと照合し、不一致0件。
  `word_tables/japanese_main_ranking.csv`へ頻度・品詞・基礎スコア付きで出力。
  最終順位のCSVではない。
- **スコア算術。** `0x1678B8`の算術分岐はlower+trunc((upper-lower)*weight/100)、上下限制限付き。
  別分岐は計算済みスコアを使う。SMULL/ASR/SUBとPC捕捉値1,441件の独立計算が一致。
- **学習。** 原本`0x19D004`で空の学習/ユーザー辞書を作り、`0x12D558`で「漢字」を1回選択。
  再検索で10位/419→1位/1000（学習辞書由来）、文字列重複なし。
  同関数は辞書と直前選択状態を更新する。個人の実機の学習データは未使用。
- **文節。** `0x1145AC`→`0x12D31C`→`0x135988`→`0x1369F4`。
  「わたしはねこがすきです」→「私は／猫が／好きです」。
  「ここではきものをぬいでください」は先頭を3文字固定すると「ここで／履き物を／脱いでください」、
  4文字固定すると「ここでは／着物を／脱いでください」。8ケースで読みの全被覆も確認。
- **接続表。** `njcon.a`は前側251・後側294品詞の両方向ビット表。
  全73,794組で転置一致（接続8,405組）、`0x14D808`で全545行のアドレスも一致。
  付属語辞書だけを外すと上記の「私は…」の例は「私／羽／古賀／好き／です」となり、
  付属語/接続が分割に寄与することを確認。
- **探索。** 192バイト仮説に最大2件の88バイト文節。
  `0x14A314`のARMで2件上限と累積score += s16(result+0x0C)-1000を確認。
  `0x14A15C`は同一読み被覆長・末尾品詞を併合、`0x167CD0`は被覆長→スコアで比較。
  刈込みと先頭文節確定によって進む。無制限の大域最適化とはしない。

外側`0x111FD4`はUTF-16LE、直接エンジン`0x1145AC`はUTF-16BE。
`0x151648`が交換することを確認し、入力のバイト順を分けた。

成果物:`DOCS/system_keyboard_conversion.md`、`SYSTEM_KEYBOARD/probe_conversion.py`、
`verify_conversion.py`、`export_ranking_metadata.py`、`evidence/ranking/`。
全結果:`FILES/extracted_system_keyboard/ranking/verification_conversion.json`。
主要辞書メタデータの照合:`word_tables/verification_ranking_metadata.json`。
SWKBD専用IDBへ関数7件命名・コメント5件を追加、保存済み。

callback辞書・個人学習・実UIを含む完全な実機順位、各モード/同点/未知語の全条件は未検証。
ACNL/CTRPFからの安全な内蔵キーボード起動・復帰と、実機の未確定候補配列取得も未検証のまま。
一時メモ:`scratchpad/MEMO_20260908_swkbd_ranking.md`。

---

