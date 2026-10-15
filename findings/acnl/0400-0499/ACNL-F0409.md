---
id: ACNL-F0409
aliases:
- F-384
title: 'F-384: 通常チャットから内蔵ソフトウェアキーボードを呼ぶケーブを適用（2026-09-09）'
summary: 通常チャットの `0x001938AC` をフックし、元の `UiScreen_OpenById(0x23E)` を必ず呼んで
date: '2026-09-09'
category: text
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1652908
- 6087324
- 6084976
- 11401288
- 10214656
- 10215424
- 10216448
- 10219520
- 10223616
- 4603428
tags:
- chat
- keyboard
supersedes: []
source: v1:RE/FINDINGS.md:24306-24333
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-384: 通常チャットから内蔵ソフトウェアキーボードを呼ぶケーブを適用（2026-09-09）

通常チャットの `0x001938AC` をフックし、元の `UiScreen_OpenById(0x23E)` を必ず呼んで
`BsSkb` の戻りポインタを保ったまま、一回要求を記録する。フレーム側は `0x005CE29C` の
元の `BL 0x005CD970` を先に実行し、要求時だけ `0x00ADF848` の try-lock を取る。
ロック成功後は ACNL 自身の APT 前処理、Prepare(`0x401`)、Start、Wait、APT 後処理、
ロック解放を順に行う。try-lock 失敗時は要求を残して次フレームへ送る。

初回は起動可否だけを安全に分離するため、内蔵キーボードの確定文字をゲーム内チャットへ
注入しない。結果設定と共有ページは実機メモリへ残し、停止後に読み出せる。

- ケーブ: `0x00838D20..0x00838F20`（512 bytes）
- chat hook: `0x001938AC = 0xEB1A951B` -> `0x00838D20`
- frame hook: `0x005CE29C = 0xEB09AAAF` -> `0x00838D60`
- control/config/template/shared: `0x009BDD00` / `0x009BE000` / `0x009BE400` /
  `0x009BF000..0x009C0000`
- config: type NORMAL、2ボタン、最大32 UTF-16単位、空白だけを拒否、predictive input有効
- 結果: config `+0x138`、text offset `+0x144`、length `+0x148`

適用前に、ソース段階のABI/重なり検査、生成後の全24分岐・12個のPC相対LDR・5リテラル、
Unicorn 12経路を検査した。停止中実機でも stock hook、ケーブ736 bytes、予約 `.bss` 8960
bytes が全ゼロであることを確認してから、データ、ケーブ、frame hook、chat hook の順で適用した。
別スクリプトによる全量再読み取りで分岐先とケーブSHA-256
`c3b26373de23645dc2d87e0315c2df089502ca5b91f6397343992bb1be528af3` が一致した。

現在は Suspend 中、PC=`0x00463E24`、breakpoint 0、state 0、run count 0。したがって
**適用の正しさは確認済みだが、内蔵キーボードの実起動はまだ未観測**。適用部分は HIGH、
起動結果は未確認のため LOW。
