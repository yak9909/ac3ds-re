---
id: ACNL-F0064
aliases:
- F-26
title: F-26 【成功】直接書き込み方式で隣マスに穴が空いた — `HIGH`
summary: 状態機械・レコードを一切通さず、隣マスのアイテムを直接書き換える。
date: '2026-09-08'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5892556
- 6697836
- 6697936
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:1376-1418
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-26 【成功】直接書き込み方式で隣マスに穴が空いた — `HIGH`

状態機械・レコードを一切通さず、隣マスのアイテムを直接書き換える。

```
フック 0x59E9CC (BL FieldObj_ApplyDigRecord)
  PUSH {R0-R6,LR}
  CMP  R0, #19               掘る以外は素通し
  BNE  skip
  LDR  R5, [SP,#36]          X      (元a6)
  LDR  R6, [SP,#40]          Y      (元a7)
  ADD  R5, R5, #1            X+1
  MOV  R4, R3                item1* = 掘削結果(158=穴) を退避
  BL   Field_GetMapManager
  MOV  R1,R5 / MOV R2,R6 / MOV R3,#0
  BL   Field_GetItemAtXY     R0 = 隣マスの item*
  CMP  R0, #0
  BEQ  skip                  範囲外なら何もしない
  MOV  R1, R4
  BL   Item_Copy             隣マスへ 158 を書く
  MOV  R0,R5 / MOV R1,R6 / MOV R2,#0
  BL   sub_59DA7C            地面更新のダーティビットを立てる
skip:
  POP  {R0-R6,LR}
  B    FieldObj_ApplyDigRecord   中心マスは完全に元通り
```

22 命令 / 88B。ケーブ領域A (`0x66336C`-`0x6633D0`, 100B) に収まる。

**実機結果**: 隣に実体のある穴が出現。何度でも掘れる（レコードを消費しないため
キューもレコードも枯渇しない）。

**要点**: フック時点で `R3` に掘削結果アイテム（158）へのポインタが渡ってきている。
自前で ID を作る必要はなく `Item_Copy` でコピーするだけでよい。

**未解決**: 隣マスでは掘るエフェクト（土煙パーティクル）が再生されない。
`sub_5A0C2C` の case 0xA/0xB/0xC/0xD はエフェクトを
`unk_5BFAD4(playerIdx)` → `unk_2504FC(handle, effectID)` で出しているが、
**actionID 19 は switch の default に落ちるためここを通らない**。
座標を取るエフェクト生成 API は未特定。

---

