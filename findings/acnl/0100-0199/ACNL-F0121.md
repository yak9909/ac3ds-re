---
id: ACNL-F0121
aliases:
- F-83
title: 'F-83: `BsFtrMgr` のglobal公開は生成完了より早く、完全readyはobject `+19` の下位2bit'
summary: 'confidence: **MEDIUM**（`code.bin.i64` のvtable、create wrapper、3 phaseを静的照合）'
date: '2026-08-24'
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9382888
- 8515068
- 6880324
- 6880060
- 6877632
- 6881508
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5077-5097
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-83: `BsFtrMgr` のglobal公開は生成完了より早く、完全readyはobject `+19` の下位2bit

confidence: **MEDIUM**（`code.bin.i64` のvtable、create wrapper、3 phaseを静的照合）

`BsFtrMgr` はtype `0xEE`、vtable `0x8F2BE8`、size 2240。
`UiScreen_CreatePhases` (`0x81EDFC`) はslot 16 `BsFtrMgr_CreateResources` (`0x68FC44`)、
slot 17 `BsFtrMgr_WaitCommonResource` (`0x68FB3C`)、slot 18 `BsFtrMgr_PopulateRoom`
(`0x68F1C0`) を順に呼ぶ。

phase 1は35KBの共通heap、room容量ぶんのactor record、最大50 bankを作り、各bankへ
CPU 96000 bytes、VRAM 20500/5500 bytesを確保する。その末尾 `0x6900E4` で
`g_BsFtrMgr=this` を公開する。phase 2の `Ftr/Common/FtrCommon.bcres` 非同期完了待ちと
phase 3のroom家具初期化はこの後である。

wrapperはobject byte `+19` のbit 0をphase 1後、bit 1をphase 2完了・phase 3呼出し後に立てる。
従って完全生成済み判定は `(manager[19] & 3) == 3`。global nonnullだけを待った初版adapterは早過ぎる。

room scene builder `sub_5B3F38` はroom flags bit `0x8` の時だけ室内共通groupを開く。
同groupはtype `0xEE`, `0x26F`, `0x5B`, `0xA3` の4件。room 0の固有type列に `0xEE`は無く、
stock屋外はmanagerを生成しない。room 0の38という容量は、外部生成されたmanagerが利用できる枠数である。

