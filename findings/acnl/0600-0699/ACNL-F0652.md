---
id: ACNL-F0652
aliases:
- Ghidra-gpt-sol-5.6-F014
- G-F014
title: 0x838080 dead-cave再利用は実機runtimeと衝突する
summary: '**確度: HIGH（crash_dump_00000009＋enable直後再現）。**'
date: '2026-09-19'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 5664260
- 6604424
- 6604428
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:403-454
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F014: 0x838080 dead-cave再利用は実機runtimeと衝突する

**確度: HIGH（crash_dump_00000009＋enable直後再現）。**

Ghidra-gpt-sol-5.6-F013初版は添付XMLの旧allocation noteを根拠に、`0x838080-0x838137` を「dead cave / NOP化済み / 参照なし」としてguard wrapperに再利用した。

しかし実機ではAR enable直後、drop操作なしでクラッシュ。

crash_dump_00000009:
- exception type = data abort
- PC = `0x566E04`
- LR = `0x8380AC`
- r0 = `0`
- r10 = `0`
- FAR = `0`

`0x8380AC` はGhidra-gpt-sol-5.6-F013 wrapperのhelper-call復帰点。正規custom balloon経路ならspawn caveがshared baseを `r10=0x01E81000` に保持した状態でwrapperへ入るが、dumpは `r10=0`。しかもユーザーはdropしていない。

従って `0x838080` wrapperはcustom drop以外の既存runtime経路から実行されている。旧XMLの「参照なし」は静的export時点の情報であり、実機runtime patch/別経路まで保証していなかった。

Ghidra-gpt-sol-5.6-F013 guardロジック自体は維持し、caveだけを既存allocation間の未使用gapへ移設:

- `0x838424-0x83845B`: guard-arm wrapper
- `0x838464-0x8384BB`: Actor_SetState guard
- `0x838400-0x838423`: 既存textbox cave
- `0x838500-`: 既存replacement string storage

`0x838424-0x8384BB` に対する静的再確認:
- main initialized imageのARM B/BL target: 0件
- initialized image内のaligned direct pointer: 0件
- XML allocation map上の既存割当: 0件

更新branch:
- `0x64C688 -> 0x838464`: `EA07AF75`
- `0x8384B0 -> 0x64C68C`: `EAF85075`
- `0x8382E4 -> 0x838424`: `EB00004E`
- `0x83844C -> 0x838380`: `EBFFFFCB`

relocated guard cave SHA-256:
`e3c9f2dd07c3cc4fd6a5c4961e2c691a832fd1a21a90bde44dc6afb44d3e1077`

modified main cave SHA-256:
`4e59739939afcaedd53612a348f8b8707e163b238061899b1b8071c89f4dd00f`

concatenated SHA-256:
`eb815cc9f2ba683285c507022c60bdba1873a78783cdba08f0fccabca2038bcb`

**重要:** `0x838080-0x838137` は今後custom caveとして使用禁止。

根拠: `work/evidence/balloon_drop_ar_20260915.md`、`docs/balloon_drop_action_replay.md`。


