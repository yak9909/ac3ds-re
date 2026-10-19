---
id: ACNL-F0720
aliases: []
title: "GPUリスト領域確保は失敗を戻り値で通知しない"
summary: "GpuCmd_AllocateListStorageは成功/失敗を返すAPIではなく、確保結果nullも検査せずGX領域を初期化する。void型を維持し、選択中managerの既知先頭へ型を付けた。"
date: 2026-10-19
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # 静的な生産側と独立した消費側。実機なし
tool: IDA
addresses: [0x00121988, 0x00AD995C, 0x005685A4]
tags: ["layout"]
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

`GpuCmd_AllocateListStorage(unsigned int command_bytes,int gx_capacity)` のvoid型を維持した。boolや成功コードへ変更する根拠はない。`GpuCmdListStoragePrefix` と現在の `g_GpuCmdListMgr` の型を付け、+4が確保結果、+8がバイト容量、+18がGX列、+1CがGX容量、+20が件数と明記した。部分型のsizeof0x24はmanager全体0x44のサイズではない。

確度 MEDIUM：本体の全分岐と独立したBuild呼出し・再生側のmanager消費が一致 [ACNL-F0709][ACNL-F0701]。実機なし。

## 根拠

- `_local/builds/acnl_jpn_v15/ida/work/100/primary.txt` の0x121998..9A0は現在managerがnullなら何も確保せず戻る。この戻りR0はstatusではない。
- 既存baseがありfree callbackがあれば先に解放する（0x1219A4..CC）。確保callbackが無ければR0=0、あれば `command_bytes+28*gx_capacity` を要求（0x1219D0..F4）。結果へのCMPは無い。
- 0x1219FCは要求command容量を+8へ、0x121A18は確保結果そのままを+4へ保存。0x121A1C..2Cで+18=base+command_bytes、+1C=gx_capacityを保存。
- 直後0x121A30..38で `Mem_ZeroFill(base+command_bytes,28*gx_capacity)`。base=nullでも実行される。GX容量が正なら低位の無効メモリへ書き、復帰前に障害となる可能性がある。復帰後のnull検査を無条件に可能な失敗契約とは呼ばない。
- 正常末尾0x121A40..54はcursor=base、end=base+command_bytesを保存し、R0はendが残る。非nullや非zeroの戻りを成功とみなす型ではない。
- Layout Build 0x568638の呼出し後はその結果を検査せず、元IDへ切り替え、Layout資源の構築結果を最終戻り値とする。Buildのboolをstorage成功専用の結果として使う説明も成立しない。

## 反証条件・未確認点

- 復帰できた標本のmanager+4は割当結果の事後観測点になる。しかしnullでも安全に戻るとは限らず、callback自身が失敗時に停止/例外を出す可能性も未測定。一般的な失敗検出用の関数/プロパティは今回確認できなかった。
- 実際のOOM、gx_capacity=0/負値、サイズoverflow、callbackごとの挙動は未測定。再確保失敗で旧領域が保持される保証もない。
