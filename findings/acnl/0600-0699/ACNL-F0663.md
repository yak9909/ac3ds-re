---
id: ACNL-F0663
aliases:
- Ghidra-gpt-sol-5.6-F025
- G-F025
title: custom AcBalloon* identityでterminal A4だけ抑止
summary: 'Ghidra-gpt-sol-5.6-F024実機trace:'
date: '2026-09-19'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: Ghidra
addresses:
- 6052400
- 6052404
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:1037-1108
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F025: custom AcBalloon* identityでterminal A4だけ抑止

Ghidra-gpt-sol-5.6-F024実機trace:
- caller LR = 0xBFCCE0
- requested = 0xA4
- current = 0x16
- desired = 0x06
- previous = 0x0D
- Player* = 0x33099E3C
- MENU_FLAGS = 0x081C
- hit counter = 0x06
- last requested/current/LR = 0xA4 / 0x16 / 0xBFCCE0
- Ghidra-gpt-sol-5.6-F022 armed flag (shared+0x0C) = 0

これによりGhidra-gpt-sol-5.6-F022 failure reasonが確定した。
shared+0x0CはAcBalloon state helperの同期実行中だけ1で、helper return後すぐ0になる。
一方、terminal-dropの0xA4 requestはその後にModuleVillage 0xBFCCDC -> import thunk -> main 0x5C5A30として発生するため、+0x0Cでは識別できない。

Ghidra-gpt-sol-5.6-F025はboolean timing guardを廃止し、custom生成したAcBalloon actor identityを使う。

### custom actor pointer保存

AcBalloon state helper 0x838380:
- 旧 0x8383B4: STR r2,[r10,#0] (worldY cleanup)
- 新 0x8383B4: MOV r0,r4

これによりhelperはAcBalloon*をr0で返す。
shared worldYは次回custom dropで必ず上書きされ、armed=0の間はlanding hookで参照されないため、旧cleanupは不要。

spawn cave:
- 旧 0x8382E8: NOP
- 新 0x8382E8: STR r0,[r10,#0x60]

したがってstate helper return直後に custom AcBalloon* を shared+0x60へ永続化する。

### 0x5C5A30 identity guard

ModuleVillage側terminal-dropは:
- 0xBFCCD8: LDRSB r0,[r4,#0x240]
- 0xBFCCDC: BL import thunk
- LR = 0xBFCCE0

import thunkはLDR pc形式なので、main 0x5C5A30入口でも:
- LR = 0xBFCCE0
- incoming r4 = AcBalloon*

が保持される。

Ghidra-gpt-sol-5.6-F025 guardは0x838424で:
1. shared+0x60のcustom AcBalloon*を読む
2. incoming r4と比較
3. LRが0xBFCCE0か比較
4. 両方一致した場合だけshared+0x60をclearしてBX lr
5. 不一致ならstock PUSH {r4,lr}を実行して0x5C5A34へ戻る

従って自然風船や他callerの0x5C5A30はstockのまま。

guard cave:
- 0x838424-0x83845F
- payload 0x3C bytes
- SHA-256 8f2d585a49623abdb1fde21283721f83ce05ba6dfe99c56a4a216a8930b1befd

hook:
- 0x5C5A30 = EA09CA7B -> 0x838424
- stock continuation branch from 0x838450 = EAF63577 -> 0x5C5A34

Actor_SetState diagnostic hookは削除し、0x64C688はstock E92D5FF0へ戻す。

Ghidra-gpt-sol-5.6-F025 scoped Ghidra export:
- acnl_jpn_v15_balloon_identity_delta.xml SHA-256 d9ad99ff21528834e563357b007586074159f933ea7437f334399017a31182c3, size 18991
- companion bytes SHA-256 441d9b800f745565410214f1fb628e8bb3cd06ed7ac760e22892776b951ba418, size 44

