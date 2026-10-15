---
id: ACNL-F0013
aliases:
- F-401
title: 'F-401: 静的再配置315語・50比較一致・内蔵FS読取り条件'
summary: 2026-09-10。DOCS/system_keyboard_relocation_audit.md参照。idalibの完全な命令列とxref/原本値から315語（旧52語を包含）を生成。直接参照243アドレスの未取得queue/エラー0、15 switch table、未解決literal/未処理switch 0。出力省略7件は完全版で回収し命令数を照合。静的根拠はMEDIUM、PC試験成功を実機HIGHへ昇格させない。
date: '2026-09-10'
category: _triage
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:78-85
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-401: 静的再配置315語・50比較一致・内蔵FS読取り条件

2026-09-10。DOCS/system_keyboard_relocation_audit.md参照。idalibの完全な命令列とxref/原本値から315語（旧52語を包含）を生成。直接参照243アドレスの未取得queue/エラー0、15 switch table、未解決literal/未処理switch 0。出力省略7件は完全版で回収し命令数を照合。静的根拠はMEDIUM、PC試験成功を実機HIGHへ昇格させない。

25入力×2配置先で候補列と順位が原本に一致。旧52語も同じ25入力で成功したため、追加分すべてが現行日本語予測で必要とは未証明。22 BLX箇所に検査を設けた7入力では5箇所が実行され、宛先は再配置した登録callback3個の範囲内。常駐辞書flag=7でファイルI/Oの6 BLX経路を回避することはassembly/decompileで照合。任意の辞書構成・全間接経路・学習・並行利用は未検証。

Luma commit aef31308a7ea33601d9d21cdede1dfd8471c07b0のPM/SM/ARM9ソースを固定URLのbytes/hashで検証。PMはFSREG_Register前にfs_access_info=0xFFFFFFFFを設定。内蔵タイトル読取りにはソース上の根拠があるが現在の実機Resultは未取得。libctru/Azaharの定義からarchive 0x2345678A用16-byte/20-byte pathを生成し往復検査。辞書TitleID/NANDはSWKBD原本でも照合。証拠はSYSTEM_KEYBOARD/evidence/f401_*.json。実機アクセス・ビルド・3gx変更なし。

