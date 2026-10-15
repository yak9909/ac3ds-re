---
id: ACNL-F0128
aliases:
- F-90
title: 'F-90: 3回目は選択Item `0x2EA3` のtype `0xBC`。基底`AcFtr`置換でgeneric create完了'
summary: 'confidence: **HIGH**（例外register/stack、ItemParam record、3 virtual targetとreturnを命令stepで照合し、'
date: '2026-08-24'
category: item
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 6885372
- 8066096
- 8066372
- 8066396
- 8066692
- 8330744
- 8330824
- 8066088
- 9377940
- 9378216
- 9378240
- 9378536
- 5373872
- 7223824
- 8516280
- 3177736
- 6885368
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5245-5277
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-90: 3回目は選択Item `0x2EA3` のtype `0xBC`。基底`AcFtr`置換でgeneric create完了

confidence: **HIGH**（例外register/stack、ItemParam record、3 virtual targetとreturnを命令stepで照合し、
基底actorによる「0のランプ」と「12つぶのぶどう」の3D表示をユーザーが目視確認）

第5版でmanager phase 3を完了後に再開すると、thread 220が3回目の
`PC=0xE1A04000` SIGSEGVで停止した。今回はstack returnが `0x690FFC`、request pointer
`R11=0x0FFFFD24` のItemが `0x2EA3`であり、`CatalogPreview_UpdateActor`自身の選択品生成である。
生成objectは同heap `0x30C51C70`、識別値 `0x17DA`、type `0xBC`、primary vptr
`0x7B1430`。4 vptrは `0x7B1430 / 0x7B1544 / 0x7B155C / 0x7B1684`だった。

`ItemParam_GetRecord`の実機baseは `0x32FF8280`、index `0xEA3` のrecordは
`0x3301399A`。record `+0x11=1`で、`g_FurnitureActorTypeByFamily[1]=0xBC`だったため、
これはfallbackの誤選択ではなく正規のfamily 1 (`AcFtrLoop`) 選択である。
`UiScreenFactory_TypeBC` (`0x7F1DF8`) は基底`AcFtr` constructor後に派生vptrを上書きするが、
このobjectのgeneric UiScreen create slot `vptr+8`は関数pointerではなくARM命令語
`0xE1A04000`だった。`code.bin.i64`のliteral `0x7F1E48`は `0x7B1428`、実機と
`code_runtime.bin`ではruntime解決後の `0x7B1430`である。

例外objectの4 vptrだけをconstructor直後の基底値
`0x8F1894 / 0x8F19A8 / 0x8F19C0 / 0x8F1AE8`へ戻し、`PC=0x51FFB0`、`R3=8`から
generic createを再実行した。pre/create/postのvirtual targetは順に
`0x6E3A10 / 0x81F2B8 / 0x307D08`で全て有効、createはresult `2`（完了）を返した。
stock attachを通して `g_CatalogPreview={ actor=0x30C51C70, Item=0x2EA3 }`になった。

第6版は `0x690FF8` のpreview actor open callを `0x01E815F0` のguard付きwrapperへ接続する。
adapter state 2かつ選択type `0xBC`の場合だけtypeを完全な基底`0xBB` (`AcFtr`)へ変え、
manager、Item request、その他のactor type、通常の室内Catalogには作用しない。hookは
`0x690FF8=0xEB5FC17C`、private stateは `active/status=2`、preview actorは上記pointerのまま
読戻し一致し、processを再開した。

---

