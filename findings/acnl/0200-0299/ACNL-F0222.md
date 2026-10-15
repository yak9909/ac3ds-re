---
id: ACNL-F0222
aliases:
- F-197
title: 'F-197: ★★★コマンドバッファは 1 つではない。`g_GpuCmdPtr` と `g_GpuCmdEnd` は別リストのことがある — `HIGH`（GPU ハングで判明）'
summary: 「そのフレームの最後のフラッシュ」を予測する方式が破綻したので
date: '2026-08-30'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7589772
- 5075440
- 1212620
- 11412980
- 1247120
- 11412948
- 11376988
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:12026-12088
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-197: ★★★コマンドバッファは 1 つではない。`g_GpuCmdPtr` と `g_GpuCmdEnd` は別リストのことがある — `HIGH`（GPU ハングで判明）

### 1. 何をしようとしたか

「そのフレームの最後のフラッシュ」を予測する方式が破綻したので
（フラッシュ回数が場面で **1〜42** と振れ、最後の呼び出し元も
`0x73CF8C` / `0x4D71F0` の 2 種類に割れる）、
**`GpuCmd_SplitAndSubmit`（`0x1280CC`）の直前に積む**方式へ切り替えた。

これは構造的に必ず最後になる正しい発想で、
**IDB の自分のコメントにも「自前のコマンドを割り込むならこれより前に積むこと」と書いてあった。**

### 2. ★何が起きたか

```
g_GpuCmdPtr = 0x00AE25F4    ← ゲームのデータ領域にある小さなリスト
g_GpuCmdEnd = 0x3239D0C0    ← 別のリスト（FCRAM）
```

**この 2 つが別のリストのものだった。**
「残量 = `end - ptr`」で安全確認したつもりが巨大な正の値になり、検査が無意味に。
小さなリストに 1776 バイトを書き込んではみ出し、**GPU が停止**した
（PC が `0x130790` 付近の `LDREX`/`CMP`/`BLE` セマフォ待ちで停滞、
`g_GpuCmdPtr` も動かなくなる）。**再起動が必要。**

### 3. 書き込み先はデータ破壊ではなかった

`0x00AE25D4` 以降には標準の終端列が並んでいた。

```
0008025E  reg 0x25E PRIMITIVE_CONFIG
000F0111  FRAMEBUFFER_FLUSH
000F0110  FRAMEBUFFER_INVALIDATE
000F0010  FINALIZE
```

**ゲームのデータ領域に置かれた正規の小さなコマンドリスト。**
壊したのはリストの内容だけで、他のデータは無事だった。

### 4. ★教訓 — 独立に得た 2 つの結果を突き合わせる

**アドレス帯が `0x00AE` と `0x3239` で明らかに違う時点で気付けたはず。**
「チェックを入れたから安全」ではなく、
**チェックに使う 2 つの値が同じ対象のものかを先に確かめる。**

この項目はユーザーの指示で運用ルールに追加した
（`CLAUDE.md` / `AGENTS.md` / `HANDOFF_RENDERING.md` / `RE/STATE.md`）。

### 5. 次にやるなら

`g_GpuCmdListMgr`（`0xAD995C`）からリストの base / size を取り、
**`ptr` がそのリストの範囲内にあることを検証**してから書く。

```c
mgr[1] = リストの base
mgr[3] = 現在のオフセット
```

`GpuCmd_SplitAndSubmit` は `v2 = g_GpuCmdPtr - mgr[1]` を使うので、
`mgr[1] <= ptr < mgr[1] + サイズ` を確かめられる。

---

