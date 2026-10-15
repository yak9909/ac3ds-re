---
id: ACNL-F0389
aliases:
- F-362
title: 'F-362: 内蔵日本語辞書6本の取得・主要辞書75,770件の読み/候補を抽出（2026-09-08）'
summary: '**confidence: MEDIUM**。複数静的証拠とPC内での元ARM命令実行で検証。'
date: '2026-09-08'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1622412
- 1720664
- 1625564
- 1285788
- 1472264
- 1352852
- 1369392
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:23621-23663
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-362: 内蔵日本語辞書6本の取得・主要辞書75,770件の読み/候補を抽出（2026-09-08）

**confidence: MEDIUM**。複数静的証拠とPC内での元ARM命令実行で検証。
実機上の動的観測はしていない。以下のコード番地は**SWKBD専用でACNLの番地ではない**。

利用者提供のSWKBD CIA `0x000400300000C002` と日本語辞書CIA `0x0004009B00011902`を
ctrtool v1.3.0で`FILES/extracted_system_keyboard/`へ展開。
内容ハッシュ/IVFCはGOOD、Ticket/TMD/NCCHヘッダ署名はFAILを区別してログ保存。
sysnandは今回未使用。ビルド・実機書き込み・実機再開なし。

### 対応を示す独立証拠

1. SWKBD `0x0018C18C`のARMは`0x001A4158`の表をindex×16で参照し、entry+8からTitleIDを読む。
   日本語エントリは内部言語1 / `0x0004009B00011902`。`dict:`にマウントする。
2. `0x0018CDDC`の日本語分岐が`JA_small/njcon.a`、`JA_small/32/`以下の
   `njubase1.a`、`njubase2.a`、`njfzk.a`、`njtan.a`、`njexyomi.a`を指定。
   提供CIAのRomFSから抽出された6ファイルと一致する。

### 主要辞書の抽出と全件照合

主要2辞書はNJDC type`0x00050000`で、確認したOpenWnn公開版の対応種別にない。
提供されたSWKBD自身の`0x00139E9C`（読み）/`0x00167708`（候補）から、
レコード位置=`BE32(header+0x20)+10*(ID-1)`、文字列基準=`BE32(header+0x24)`を確認した。
`0x0014A494`が明示候補/読みそのまま/カタカナ化を分岐し、`0x0014E530`がかな→カナを行う。

- `njubase1.a`: 5,992件、`njubase2.a`: 69,778件、合計75,770件。
- 読み/候補ペアの重複除外65,729組。
- `SYSTEM_KEYBOARD/extract_dictionary.py`で全件のサイズ/境界/UTF-16BEを検証してCSV化。
- `SYSTEM_KEYBOARD/verify_dictionary_arm.py --all`で無変更の元ARM getterをUnicorn上で実行。
  **全75,770件の読み・候補がPython抽出と一致、不一致0件。** 実機の起動・表示確認ではない。
- 成果物:`FILES/extracted_system_keyboard/word_tables/japanese_main.csv`。
  `manifest.json`と`verification_arm_all.json`も同ディレクトリ。
- 例:`かんじ`→感じ/漢字/幹事/監事/寛治/完治/寛二。順位は実機表示順を意味しない。

他の4辞書の原本も取得済み。単漢字・付属語・追加読み系の単語一覧化、接続規則、
頻度/文脈/学習を含む候補生成と順位、実機での未確定候補配列は未検証。
自前メニューやgohan.3gxへ組み込む作業ではない。

詳細:`DOCS/system_keyboard_dictionary.md`。
SWKBD専用IDB:`FILES/extracted_system_keyboard/swkbd_jpn/swkbd.elf.i64`（`swkbd_jpn`）。
静的根拠:`SYSTEM_KEYBOARD/evidence/swkbd_dictionary_static.json`。
一時メモ:`scratchpad/MEMO_20260908_swkbd_dictionary.md`。

