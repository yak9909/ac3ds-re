---
id: ACNL-F0112
aliases:
- F-74
title: 'F-74: field持ち物の開始点はplayer state `0x16`。同位置で公式catalog要求へ置換可能'
summary: 'confidence: **HIGH**（制御フロー・命令・戻り値と第1版の停止状態を `code.bin.i64`・実機で照合）、'
date: '2026-08-24'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 6037356
- 10113372
- 8718588
- 9484439
- 7168824
tags:
- catalog
- player
supersedes: []
source: v1:RE/FINDINGS.md:4804-4848
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-74: field持ち物の開始点はplayer state `0x16`。同位置で公式catalog要求へ置換可能

confidence: **HIGH**（制御フロー・命令・戻り値と第1版の停止状態を `code.bin.i64`・実機で照合）、
**LOW**（controller state 5も抑止する第2版の画面結果は実機確認待ち）

通常屋外Xの `sub_5C1F08` は各種gateを通した後、playerを取得して次を行う。

```asm
005C1F64  BL   sub_679A48
005C1F68  MOV  R0,R4              ; player
005C1F6C  BL   sub_65945C          ; Actor_SetState(player,0x16,...)
005C1F70  CMP  R0,#0
005C1F74  MOVNE R0,#1
```

`sub_65945C` はplayer animation instanceを取得し、最終的に
`Actor_SetState(player, 0x16, anim, 0)` へtail-callする。一方、公式catalog入口
`vc_CFUNCTION(0)` は `Menu_RequestOpen(0x7C,0)` の戻り値をそのまま返し、成功時だけ
catalog mode/globalとUI音を設定する。第1版は `0x5C1F6C` のcall先を
`MOV R0,#0; B vc_CFUNCTION` へ置換し、player state `0x16` だけを抑止した。

実機ではplayerは状態 `0x06` のままで移動可能だったが、カタログは表示されず、持ち物ボタンが
押された状態で下画面操作だけが停止した。Suspend時は `g_MenuOpenState/Id/Arg = 2/0x7C/0`、
catalog globals `byte_949D3B=2`, `byte_949D23=0` で、公式要求は成功してキュー済みだった。
同時にfield controller `0x9A515C+0x1A=5`、player `+0x1A9=0x06`。
従ってstate `0x16` はplayer motionだけでなく、下画面managerがopen requestを消費する遷移の
トリガーでもある。また `sub_165B40` のcontroller state 5だけを残すと、ボタン層が待機状態になる。

第1版を完全撤去後、stock `sub_6D27E8()` one-shotで復旧し、地図と通常X開閉を確認した。
第2版は `vc_CFUNCTION(0)` を呼んだ後にR0を0へ固定して返す。これによりplayer state `0x16` に加え、
`sub_165B40` の成功分岐とcontroller state 5も抑止し、catalog requestだけをglobal queueへ残す。

第2版の実機ではボタン音と一瞬の押下表示だけが出て、下画面・playerはidleのまま、何も開かなかった。
操作不能にはならないが通常持ち物も開けない。Suspend時はcontroller `+0x1A=0` のまま、
`g_MenuOpenState/Id/Arg = 2/0x7C/0`。従ってglobal requestはfield側state遷移なしでは消費されない。
第2版も完全撤去し、stock `sub_6D27E8()` one-shotで要求を破棄した。

`0x8508FC` からのlower-menu状態記述子は20バイトで、`[name, enter, 0, update, 0]`。
`sub_6D62AC/sub_6D6060` のrecordはname `0x90B897` =「メニュー切り替え」。
したがって旧 `0x6D6338` hookは正しい状態の中ではあるが、enterの後半まで進んだ遅い位置だった。
次候補は `sub_6D62AC` の関数入口でcatalogへ分岐し、同関数内の持ち物用animation/button/
`sub_693EE8` 初期化を一切実行させないもの。

---

