---
id: ACNL-F0012
aliases:
- F-402@v1:RE/FINDINGS.md:72
title: 'F-402進行中: ACNL自身の内蔵タイトルFS経路（MEDIUM）'
summary: 'idalib code.bin.i64: sub_1304C8はIPC0x08030204、TLS+0x80へarchive/fileのbinary pathを詰めSVC32。sub_346AB8はarchive0x2345678A/16byte archive/20byte file/READ1で同関数を呼び、sessionはdword_96EF28。独立caller sub_1290C4も同sessionを使用。libctru fs.cのOpenFileDirectly定'
date: '2026-09-11'
category: system
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1933354
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:72-77
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-402進行中: ACNL自身の内蔵タイトルFS経路（MEDIUM）

idalib code.bin.i64: sub_1304C8はIPC0x08030204、TLS+0x80へarchive/fileのbinary pathを詰めSVC32。sub_346AB8はarchive0x2345678A/16byte archive/20byte file/READ1で同関数を呼び、sessionはdword_96EF28。独立caller sub_1290C4も同sessionを使用。libctru fs.cのOpenFileDirectly定義と一致。実機session値0x001D802A、3入口のbytesを読取り保存（f402_before.json）。内蔵辞書のOpen成功はまだ未観測。

追加frame wrapperは212bytes、全分岐/literal・16経路PC試験PASS。レジスタ/flags/TLS256bytesを保存復元。実機へ適用・読戻し済み、要求state0でResume未実行。詳細RE/STATE.md先頭。ゲームがキーボード終了待ちのため、キャンセル後の通常frameで試験する。

