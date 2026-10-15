---
id: ACNL-F0129
aliases:
- F-91
title: 'F-91: `1UPキノコ` はfamily 3/type `0xBD`でも同じvptr+8 crash。preview特殊type全域を基底化'
summary: 'confidence: **HIGH**（例外register/stack、ItemParam record、family table、復旧create、実機patch読戻しを照合）'
date: '2026-08-24'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5373888
- 5370220
- 5369072
- 5409960
- 6885372
- 2206740
- 8066096
- 8066392
- 8066416
- 8066712
- 6885368
- 5373872
- 7223824
- 8516280
- 3177736
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5278-5310
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-91: `1UPキノコ` はfamily 3/type `0xBD`でも同じvptr+8 crash。preview特殊type全域を基底化

confidence: **HIGH**（例外register/stack、ItemParam record、family table、復旧create、実機patch読戻しを照合）

第6版で再開後、Item `0x2EA3`「0のランプ」と `0x2E78`「12つぶのぶどう」は順に3D表示された。
両者のItemParam record `+0x11`は1で、preview open時にtype `0xBC -> 0xBB`となった結果である。
続いてItem `0x2C89`「1UPキノコ」を選ぶと、thread 220が再び
`PC/R3=0xE1A04000, LR=0x51FFC0`で停止した。stack returnは
`0x51F16C -> 0x51ECF0 -> 0x528CA8 -> 0x690FFC -> 0x21AC14`で、同じ
`CatalogPreview_UpdateActor -> sub_57ADFC -> UiScreen_RunCreateVirtual`経路だった。

`0x2C89`のItemParam recordは `0x3300FA8E`、`+0x11=3`、
`g_FurnitureActorTypeByFamily[3]=0xBD`。例外actorは `0x30C51C70`、type `0xBD`、primary vptr
`0x7B1430`で、subobject vptrは `0x7B1558 / 0x7B1570 / 0x7B1698`だった。
primary `vptr+8`はtype `0xBC`時と同じ命令語 `0xE1A04000`である。従ってクラッシュは
1UPモデル/resource固有ではなく、late outdoor previewで特殊家具actorをgeneric UiScreen childとして
生成する契約不一致がtype `0xBD`にも共通するためである。

第7版は `0x690FF8` の既存wrapperを拡張し、adapter state 2かつtypeが
`0xBC..0xEB`のときだけ `0xBB`へ置換する。family 0の基底`0xBB`、範囲外type、stock室内Catalog、
field上の通常actor生成には作用しない。これは `g_FurnitureActorTypeByFamily` が返す特殊家具typeを
preview用途では一律に「モデルをItem requestから読む基底AcFtr」として扱い、不要なfield固有挙動だけを省くもの。

停止中のtype `0xBD` actorにも4個の基底vptrを設定し、`PC=0x51FFB0, R3=8`から再実行した。
pre/create/postは `0x6E3A10 / 0x81F2B8 / 0x307D08`、create resultは2で、
`g_CatalogPreview={ actor=0x30C51C70, Item=0x2C89 }`へ正常attachされた。第7版caveとhookは
private `active/status=2`を保持したまま読戻し一致した。

第7版で再開後、1UPキノコを含む家具は一通り3D表示された。これにより、Item requestを維持した
基底`AcFtr`置換が通常の家具モデル読込・描画には有効であることを実機確認した。

---

