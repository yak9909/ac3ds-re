---
id: ACNL-F0653
aliases:
- Ghidra-gpt-sol-5.6-F015
- G-F015
title: Ghidra-gpt-sol-5.6-F013 guardは遅すぎた — ActorFactory前にarmする必要がある
summary: '**確度: HIGH（Ghidra-gpt-sol-5.6-F013実機不成立＋hook命令順の静的再監査）。**'
date: '2026-09-19'
category: actor
build: acnl_jpn_v15
confidence: HIGH
tool: Ghidra
addresses:
- 6039512
- 5746172
- 6604424
- 6604428
tags: []
supersedes: []
source: Ghidra:work/FINDINGS.md:455-519
by: gpt-sol-5.6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## Ghidra-gpt-sol-5.6-F015: Ghidra-gpt-sol-5.6-F013 guardは遅すぎた — ActorFactory前にarmする必要がある

**確度: HIGH（Ghidra-gpt-sol-5.6-F013実機不成立＋hook命令順の静的再監査）。**

Ghidra-gpt-sol-5.6-F014移設版はenable時crashを解消したが、実機ではcustom drop後の `0x16 -> 0x06` が残った。

Ghidra-gpt-sol-5.6-F013/Ghidra-gpt-sol-5.6-F014のguard-arm wrapperは `0x8382E4`、すなわち:
- target座標計算
- `GET_PLAYER @ 0x5C27D8`
- `ActorFactory_CreateByTypeId @ 0x57ADFC`
- AcBalloon生成成功
- shared Item/Vec3保存

の**後**に呼ばれていた。

従ってPlayer state resetがActorFactory内部またはその生成副作用中に発生すると、shared+0x1C guardはまだ0であり、`Actor_SetState` hookはstock遷移を通してしまう。

静的確認:
- `GET_PLAYER @ 0x5C27D8` 自身は `player+0x1A9` を読むが書かない。
- spawn hookでGET_PLAYER以前に呼ぶ外部関数はない。
- よってPlayer取得直後にguardをarmすれば、ActorFactory以降の全custom処理を覆える。

Ghidra-gpt-sol-5.6-F015では `0x838270` のGET_PLAYER callを `0x838424` wrapperへ置換。

wrapper:
1. stock GET_PLAYERをcall
2. shared+0x1Cを0へ初期化
3. returned Player != 0
4. `player+0x1A9 == 0x16`
5. `MENU_FLAGS & 0x08 != 0`
6. 条件成立時だけ shared+0x1C=1
7. Player*をそのままspawn hookへ返す

その後ActorFactoryを実行するため、生成中の `Actor_SetState(player,6,...)` もguard対象。

遅いwrapper callは削除し、AcBalloon state helperは従来通り直接call。

現行配置:
- `0x838424-0x83847B`: GET_PLAYER + early guard-arm wrapper
- `0x838484-0x8384DF`: Actor_SetState guard
- `0x8384E0-0x8384FF`: unused
- `0x838500-`: existing replacement strings

branch:
- `0x838270 -> 0x838424`: `EB00006B`
- `0x8382E4 -> 0x838380`: `EB000025`
- `0x64C688 -> 0x838484`: `EA07AF7D`

Actor_SetState stock continuationはPC literalで `0x64C68C` へ復帰する。

extended cave `0x838424-0x8384E3` 再検証:
- main initialized image ARM B/BL target 0件
- aligned direct pointer 0件
- known allocationなし

hash:
- early guard cave 0xC0 bytes: `888c90a30e2d121b9794d4c44fb51334f532cb864a53b724382a16d3e8b84e67`
- main balloon cave 0x1D8 bytes: `5fcbadb1449c4d7a316df1a8dd46fd47fb9e2685f1d9a7654d037ba61f6cf368`
- combined: `ead098d3dc8144ce4fc4a0a5e69bfc357b2764369b2ad52da240bcb92b10a7e2`

**実機未確認:** early-arm版でstate 0x16が維持されるか。

根拠: `docs/balloon_drop_action_replay.md`、`work/evidence/balloon_drop_ar_20260915.md`。


