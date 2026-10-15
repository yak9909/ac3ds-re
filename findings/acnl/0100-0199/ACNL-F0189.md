---
id: ACNL-F0189
aliases:
- F-163
title: 'F-163: ★CTRPF プラグインは GPU 可視メモリを確保できない — `HIGH`（実機で検証、結果コードまで確認）'
summary: '`Plugin/CTRPluginFramework-BlankTemplate-0.8.0` に検証エントリを追加して実機で実行。'
date: '2026-08-28'
category: system
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9751088
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:9729-9796
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-163: ★CTRPF プラグインは GPU 可視メモリを確保できない — `HIGH`（実機で検証、結果コードまで確認）

### 1. 検証内容

`Plugin/CTRPluginFramework-BlankTemplate-0.8.0` に検証エントリを追加して実機で実行。
ログ: `Plugin/.../CTRPF_LinearTest.txt`

### 2. 結果 — 全て否定的

| 呼び出し | 結果 |
|---|---|
| `linearSpaceFree()` / `vramSpaceFree()` | **0 / 0** |
| `linearAlloc()` 4KiB〜2MiB | 全て確保できず |
| `linearMemAlign(0x10000, 0x80)` | 確保できず |
| **`svcControlMemory(MEMOP_ALLOC_LINEAR)` 4KiB〜2MiB** | **全て `0xD86007F3`** |
| `vramAlloc(0x10000)` | 確保できず |
| `new u8[0x10000]`（対照） | VA `0x061FE170`、**PA = 0** |
| `GSPGPU_FlushDataCache` | `0xD8E007F7` |

### 3. 結果コードの分解

```
0xD86007F3 = Kernel / OutOfResource / OutOfMemory / Permanent
0xD8E007F7 = Kernel / InvalidArgument / InvalidHandle / Permanent
```

### 4. 解釈

**`OutOfMemory` は「プロセスに空き linear メモリが無い」という意味。**
ACNL は起動時にメモリ予算を使い切る設計で、プラグインが後から取る余地が無い。
**これは libctru のヒープ初期化とは無関係**で、`svcControlMemory` 直呼びでも同じ。
`linearSpaceFree = 0` は「プラグインは libctru の起動処理を通らない」ことの確認に過ぎず、
**本質的な障害はカーネルが返す `OutOfMemory` のほう。**

プラグインヒープの `PA = 0` は対照として期待どおり
（プラグインのメモリは linear ではないので GPU に見せられない）。

**`GSPGPU_FlushDataCache` の失敗は別問題で、こちらは回避できる。**
module が GSP でなく **Kernel / InvalidHandle** なので、
GSP サービスセッションがプラグイン文脈で作られていない（`gspInit()` が走っていない）だけ。
代替として **`svcFlushProcessDataCache(CUR_PROCESS_HANDLE, addr, size)`** がある
（`3ds/svc.h` に存在。サービスセッション不要）。

### 5. 結論 — 設計を変える必要がある

**「プラグインが自前でバッファを確保して GPU に見せる」構成は取れない。**
**代わりにゲーム自身の linear メモリを間借りする。**

これは実現可能であることが既に分かっている。
F-123 / F-124 で **ゲームの影テクスチャ（VA `0x33076480` / PA `0x23076480`）を
書き換えて実際に表示させた**実績がある。
GPU が読むメモリに我々が書けること自体は実証済みで、
足りないのは「そこを正当に確保する手段」だけ。

`VA - PA = 0x10000000` は new linear heap のマッピング（VA `0x30000000+` / PA `0x20000000+`）
と整合するので、**`osConvertVirtToPhys` はこの範囲のアドレスに対しては使える**はず。
アドレスが GPU 可視かどうかの判定に利用できる。

### 6. 取りうる 2 つの経路 → TODO-117

- **(a) 既存バッファの間借り** — 使われていない、または上書きしても安全な
  テクスチャ・頂点バッファを特定して流用する。F-123/124 と同じ手法
- **(b) ゲームのアロケータを呼ぶ** — `g_GfxAllocator`(`0x94CA30`) は既に同定済み。
  これが linear メモリを配るなら、フック内（ゲームのスレッド上）から呼べば
  正当に所有権のあるバッファが得られる。**こちらが本命**

---

