---
id: ACNL-F0301
aliases:
- F-277
title: 'F-277: 記録 → Commit → 再生の連鎖を端から端まで静的に証明した — `HIGH`（静的のみ）'
summary: 「実装したものがどう影響するか」を、関数ごとに全部読んで繋いだ。
date: '2026-09-01'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8062612
- 8063528
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:16957-17042
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-277: 記録 → Commit → 再生の連鎖を端から端まで静的に証明した — `HIGH`（静的のみ）

「実装したものがどう影響するか」を、関数ごとに全部読んで繋いだ。

### 1. `sub_7B01CC`（Clear）— リストを空に戻す

```c
if (mgr && (mgr[1] /*base*/ || mgr[6] /*キュー配列*/)) {
    Mem_ZeroFill(mgr[6], 28 * mgr[8]);
    mgr[3] = 0;  mgr[4] = 0;  mgr[5] = 0;
    mgr[8] = 0;                      // ★GX キュー件数を 0 に
    mgr[9] = mgr[10] = mgr[12] = mgr[13] = 0;
    g_GpuCmdPtr = mgr[1];            // ★base
    g_GpuCmdEnd = mgr[1] + mgr[2];   // ★base + size
}
```

- **`base` も キュー配列も 0 なら何もしない。** F-259 が警告した「未知 id を渡すと
  ヘッダだけできて base が 0」の状態では Clear が空回りする。
  自前リストは `GenCmdlists` + `CmdlistStorage` で作るので base ≠ 0。**問題なし**
- Clear 後は `g_GpuCmdPtr` が自前リストの先頭、`g_GpuCmdEnd` が先頭 + 0x4000。
  **記録中の残量検査（`g_GpuCmdPtr + 0x2000 <= g_GpuCmdEnd`）は自前リストを見ている**

### 2. `GpuCmd_CommitListAndCaptureDelta`（`0x7B0694`）— 長さの出所

```c
v5 = g_GpuCmdPtr - g_GpuCmdListMgr[1];          // base からのオフセット
g_GpuCmdListMgr[3] = v5;
if ((v5 & 8) != 0 && g_GpuCmdEnd > g_GpuCmdPtr) // 16 バイト境界へ詰め物 2 語
    { *p = 0; p[1] = 0x0008025E; g_GpuCmdPtr += 8; }
*a1 = dword_AD9A28;                              // start
*a2 = g_GpuCmdPtr - g_GpuCmdListMgr[1] - start;  // ★len ＝ +0x108
*a3 = dword_AD9A2C;                              // qStart
*a4 = g_GpuCmdListMgr[8] - qStart;               // qCount
```

**長さは `mgr[3]` ではなく `g_GpuCmdPtr` から計算される。**
したがって自前ケーブは Commit の前に **必ず `g_GpuCmdPtr` を書き戻さなければならない**。

### 3. `g_GpuCmdPtr` の受け渡し（自前ケーブの中）

```
（3）で g_GpuCmdPtr を R6 へ読む → R5 = R6
   ... STR R1,[R5],#4 でコマンドを積む（g_GpuCmdPtr は触らない）...
   DrawCtx_FlushBatch(drawctx, R5) -> R5   （この関数も g_GpuCmdPtr を触らない）
   ★ STR R5,[=g_GpuCmdPtr]      ← 書き戻し。build_q の描画終了直後にある
endrec:
   DrawEnd1(drawer, 1)
       = g_GpuCmdPtr = (*(drawer_vtbl+0x18))(drawer, g_GpuCmdPtr, 1)   （sub_4D723C）
         → sub_4D71D4: 溜まったバッチがあれば流して進める
         → sub_4D7204(…, 1): フラグが立っているので end ブロックは出さない
   Commit(node+0x104..)          ← ここで g_GpuCmdPtr から長さが決まる
   SelectList(退避した id)
```

**書き戻しが 1 行でも欠けると `+0x108` が 0 になり、一切描画されない。**
（F-273 で見つけた `R4` のバグと同じ症状を、別の原因で起こしうる箇所である。）

### 4. `GpuCmd_ReplayRecordedListRange`（`0x7B0A28`）— 実体のコピー

- `a7`（= `+0x11C`）が偽だと**キューのエントリに印を付けるだけで 1 バイトも積まない**。
  `sub_5685A4` と同じく `+0x11C = 1` を入れてあるので通る
- `a6`（= `+0x114`）は状態無効化のビット列。0 なら何もしない。ゲームの Layout と同じ 0
- 本体のコピーは `Mem_CopyBytes3(g_GpuCmdPtr, srcBase + off + copied, len - copied)`（F-274）

### 5. 早期離脱の経路がリストを戻すか

`build_q` の分岐を全部並べた。

| 位置 | 条件 | 飛び先 | 安全か |
|---|---|---|---|
| 表が無い | `LOG_CUR_TAB == 0` | `skip` | ✓ SelectList の**前**なので戻す必要が無い |
| チャンク 0 | `LOG_CUR_CHUNK == 0` | `skip` | ✓ 同上 |
| drawctx 未捕獲 | `LOG+4 == 0` | `endrec` | ✓ 記録開始後なのでリストを戻す |
| カーソル 0 | `g_GpuCmdPtr == 0` | `endrec` | ✓ 同上 |
| 残量不足 | `ptr + 0x2000 > end` | `endrec` | ✓ 同上 |

**記録を開始したあとの離脱は必ず `endrec` を通り、`SelectList(退避した id)` に到達する。**
戻し忘れるとゲームが自前のリストへ書き込んでしまうので、ここは設計上の要である。

なお `endrec` 経由で離脱すると `len = 0` になり、そのフレームは描かれない
（前フレームの記録も Clear 済みなので残らない）。
残量検査は自前の 16KB を見ており、記録は約 2.3KB（F-276）なので実際には起きない。

---

