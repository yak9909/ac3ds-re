---
id: ACNL-F0759
aliases: []
title: "0x12D294 は即時 flush ではなく GPU キャッシュ範囲の登録ラッパである"
summary: "0x12D294はGPUへ見せる範囲をマネージャに登録する。実際のGSPGPU_FlushDataCacheは別の後段処理でまとめて呼ばれる。"
date: 2026-11-11
category: system
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0x12d294]
tags: ["heap"]
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

0x12D294はGPUへ見せる範囲をマネージャに登録する。実際のGSPGPU_FlushDataCacheは別の後段処理でまとめて呼ばれる。

確度MEDIUM。実測なし。各項目について命令列と、独立した呼び元・生成元・消費側またはvtable実データを照合した。

| 番地 | 付けた名前 | 型・プロトタイプ |
|---|---|---|
| `0x0012D294` | `GpuCache_QueueFlushRange` | `void f(const void *address, unsigned int bytes);` |

## 根拠

- ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名はsymbolsを併読。原本code.binのSHA256はbuild台帳と一致。命令列は `tools/codebytes.py` の読取関数とCapstoneで独立照合した（`_local/evidence/146/original_asm.txt`）。型・vtable・表の原本値は同所 `bytes.json` と追加検算。作業用IDBで実測はしていない。
- 対象 `0x12D294`: R0をR3へ保存し、`LDR R0,=0x96FC20; LDR R0,[R0]; CMP R0,#0`。非NULL時にR1=元R0、R2=元R1として `0x1338E0` へ末尾分岐。NULLはBX LR。引数は範囲先頭とバイト長。
- `0x1338E0` はlock、要求数増加、0x14067C/0x13E864の範囲と交差を取り、manager+44が真なら0x13887Cへ `[start,end]` を追加/併合。偽ならmanager+16/+20へ最小start/最大endを保存する。この関数はflush APIを呼ばない。
- 別の消費側 `0x565B9C` は同じlock内でqueueまたは+16/+20を取り出し、`0x7B08D4→0x136EDC` から `GSPGPU_FlushDataCache` を呼ぶ。呼び元 `0x1B6B84` の末尾がglobal0x96FC20を渡す。
- 使用元 `0x569EFC` は読み込み完了時に(data,size)を渡す。`ssys_LoadBclimToVram 0x5676C8` も呼ぶため、単なる汎用SVCラッパとは区別する。
- 旧版 `DecorLayout.cpp:42` のFlushRangeは用途を略した呼称。関数名は `GpuCache_QueueFlushRange`、戻り値は意味のある完了値が無いのでvoid、長さu32。F0589の「flush手順」は呼出しそのものと整合するが、即時の書き戻し完了の根拠にはしない。

- 参考資料は依頼指定の旧版gohan（`_local/legacy-src/gohan-legacy/Sources`、出所は依頼文、台帳の既存キー無し）。未検証の手がかりとして用途を対比し、上記一次証拠を根拠とする。旧版本文を証拠の代わりにしない。

## 反証条件・未確認点

- 後段が走る時刻やGPU完了を保証しない。範囲クリップ外のメモリやCPU cache命令単体の保証としては使わない。実測なし。
- 上記生産/消費の値やvtableが別オブジェクト・別型を指すと判明した場合は再検討する。新しい実機確認やゲーム挙動の保証は含めない。
