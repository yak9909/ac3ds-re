---
id: ACNL-F0734
aliases: []
title: "GX 完了カウンタと Framework の前回リスト待ち"
summary: "実行中GXリスト+0x28は要求の完了割り込みで進み、+0x24の提出数と別。Frameworkは前回リストの実行終了を待ってからクリアする。VBlankや経過フレーム数だけでは画像の最終参照完了にならない。"
date: 2026-10-21
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: "全関数export・実RomFS・提供停止ログ・公開ソース"
addresses: [0x00121E2C, 0x00128264, 0x0012E6B4, 0x0012E7D8, 0x007B1138, 0x0054C5D8, 0x0054C424, 0x007B0A28, 0x0011F384, 0x0011F348]
tags: ["layout", "sead"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6.1-sol
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

ゲームにはGPU要求の完了を知る経路がある。実行中GXリストの完了カーソルと、Frameworkの前回リスト待ちを使えば、VBlankや任意の待ちフレーム数より直接的にGPUの進捗を判定できる。ただし資源の安全な返却には、その後の記録列からの再参照が無いことも要る。
確度MEDIUM：GSP callback登録、生産側、完了側、Frameworkの待ち/クリア順序という独立した命令列を照合。実機での世代追跡は未実施。

## 根拠

一次証拠 `_local/evidence/107/0x<8桁アドレス>.txt`、出所 `exports.json`。旧exportコメントの「522の役割未確定」は今回の根拠に使わない。

| 実行中mgrからのoffset | 意味 |
|---|---|
| +0 | list ID |
| +0x18 / +0x1C | 28 B GX配列 / 容量 |
| +0x20 | 積んだ要求数 |
| +0x24 | GSPへ提出済みの要求数 |
| +0x28 | 完了した要求数（次の未完了index） |
| +0x38 / +0x3C | callback / 最終要求でもcallbackするflag |

- `0x121E2C` がGSPイベント0/1/4/5/6へ完了経路を登録。P3D=5へ `0x128264`、PPF=4へ `0x128330`、PSC0/1へ `0x128334/0x128338`。PDC0/1=2/3は別のVBlank handler。
- `0x12E7D8` はmgr+0x24を進めてGX要求を提出。`0x128264` は対応するコマンドの完了byte数を更新して `0x12E6B4` へ入る。後者は **running mgr `[0xAD9960]` の+0x28を1増やす**。全要求の末尾なら `[0xAD98D1]` を0へする。途中停止flagでも0になり得るため、0だけでは全完了を意味しない。
- 最終callbackを設定する `0x11F384` と `0x11F348(-1)` の使用例は `0x11CE64`。ただし既存callbackの上書きは本作の通知を失う。個別Layoutの記録列と実行中の親GX列は別物である。
- `0x54C424` はCalc→Draw→vslot+0x78 (`0x54C5D8`)→提示待ち→現在list提出 `0x7B04E0`→2本を交替。
- `0x54C5D8` はframework+0x148が現在index、反対側のlist IDは `framework+0x128+4*(1-index)`。`0x54C608` でproperty513の実行中判定、`0x54C614` で `0x7B1138` を条件呼出し、`0x54C61C` でその列をclearする。
- `0x7B1138` は実行中flagを待つが、`[0xAD9A38]` のtimeout超過では `[0xAD9A30]` のcallbackまたはreturnへ進む。**待ちから戻ったという事実だけでは完了でない**。全完了をいうなら同じ実行世代の `completed==submitted==queued`、途中停止無しを別に確かめる。
- `0x7B0A28` のreplayはflagにより記録GPU列をコピーするか外部列への参照をGXへ積む。元Layoutのlist IDへ完了callbackを付けるだけでは、親GX列の実行完了通知にはならない。

公開資料 `STUDY107_PUBLICS`: [3dbrew GSP Shared Memory](https://www.3dbrew.org/wiki/GSP_Shared_Memory) のIRQ番号、[libctru gxqueue.c](https://github.com/devkitPro/libctru/blob/master/libctru/source/gpu/gxqueue.c) のgxCmdQueueInterrupt、[gspgpu.c](https://github.com/devkitPro/libctru/blob/master/libctru/source/services/gspgpu.c) のGSPイベントdispatchと照合。libctruのポインタ/関数を本作の管理者へそのまま当てる結論ではない。

## 反証条件・未確認点

timeout/途中停止/HOME復帰/再提出時にカーソルは再使用される。同じpointerやカウント値だけを永続fenceとせず、list ID・提出世代・最終参照要求indexを対応させる必要がある。
複数画面/立体視の最後の参照を含め、記録済みの未提出列と将来のreplayを全て排除したことは未実測。安全な画像の面数を、この関数の存在だけから断定しない。
