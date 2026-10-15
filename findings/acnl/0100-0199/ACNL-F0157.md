---
id: ACNL-F0157
aliases:
- F-119
title: 'F-119: ★★TODO-80 完了 — 自前の `g3d::FuncNode` を生成し、毎フレーム呼ばせることに成功'
summary: 'confidence: **HIGH**（実機。生成物の型・コールバック回数を直接確認）'
date: '2026-08-24'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 2686476
- 9424656
- 9751088
- 5150668
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:7698-7794
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-119: ★★TODO-80 完了 — 自前の `g3d::FuncNode` を生成し、毎フレーム呼ばせることに成功

confidence: **HIGH**（実機。生成物の型・コールバック回数を直接確認）

`PATCHES/cave_own_funcnode.py` を作成。**ゲームのオブジェクトを借りずに、
自分で作ったノードを自分のコールバックで毎フレーム呼ばせる**ところまで到達した。

### 1. 構成

フック: `BsShadowViewMgr_SubmitToScene`(`0x28FE0C`) の先頭 1 ワードを `B ケーブ`。
ここは `Frame_DrawPass1024` の登録フェーズで毎フレーム 1 回だけ通る (F-113)。

```asm
PUSH {R4,R5,LR}
MOV  R4, R0                 ; this (BsShadowViewMgr)
LDR  R1, [R4,#0xC8]         ; 本来の sceneIndex
ADD  R0, R4, #0xA8
BL   Scene_SubmitNode       ; ★本来の影（挙動を変えない）
LDR  R5, =HOLDER
LDR  R0, [R5,#4]
CMP  R0, #0
BNE  submit                 ; 生成済みなら飛ばす
  MOV  R0, R5
  LDR  R1, =&g_GfxAllocator
  LDR  R1, [R1]
  BL   g3d_FuncNode_Create      ; ★初回だけ生成
  MOV  R0, R5
  MOV  R1, #0                   ; cb0 = なし
  LDR  R2, =STUB                ; cb1 = 自前
  MOV  R3, #0                   ; userdata
  BL   g3d_FuncNode_SetCallbacks
submit:
MOV  R0, R5
LDR  R1, [R4,#0xC8]
BL   Scene_SubmitNode       ; ★自前ノードを毎フレーム登録
MOV  R0, #2
POP  {R4,R5,PC}
```

STUB（`0x01E81680`）は `COUNTER` を 1 増やして `BX LR` するだけ。**GPU に触らない。**

メモリ配置（CTRPF の空ページ、既存ケーブと非衝突）:

| 用途 | アドレス |
|---|---|
| ケーブ本体 | `0x01E81500`-`0x01E81567` |
| STUB | `0x01E81680`-`0x01E81697` |
| HOLDER（`+4` にノード） | `0x01E816C0` |
| COUNTER | `0x01E816D0` |

### 2. ★実機の結果

2000ms 走らせて（`run_timed.py`）読んだ値:

| 項目 | 値 | 判定 |
|---|---|---|
| `HOLDER[1]` | `0x329D8500` | **生成された** |
| ノードの `vptr` | `0x008FCF10` | **`vtbl_g3d_FuncNode`** ✔ |
| `cb1`(`+0x14C`) | `0x01E81680` | 自前 STUB ✔ |
| `userdata`(`+0x150`) | `0` | 指定どおり |
| `allocator`(`+4`) | `0x329A4820` | `g_GfxAllocator` ✔ |
| 子(`+0x18`/`+0x1C`) | `0` / `0` | 木に繋がっていない ✔ |
| **`COUNTER`** | **62** | **2 秒で 62 回 ≒ 31fps = 毎フレーム呼ばれている** |

**F-111 で導いた手順が、ゲームのオブジェクトを一切借りずに成立した。**

### 3. アロケータの選定

`g_GfxAllocator`(`0x94CA30`) を採用。根拠:

- `Render_InitGlobal`(`0x4E97CC`) が `(*(vtbl+8))(alloc, size, align)` の形で使っており、
  `g3d_FuncNode_Create` が要求する形と**同一**
- グローバルで寿命が長い（`BsShadowViewMgr` の sead ヒープは部屋遷移で作り直される恐れ）

実機で `node+4` が `0x329A4820` になっており、確かにこのアロケータが記録されている。

### 4. 副産物 — フレームレートは約 31fps

`COUNTER = 62 / 2 秒`。**デバッガを繋いでいても 30fps 前後で動いている。**
F-117 前後で「フレームが遅い」と疑った観測は、やはり bp の当たり方の問題だった。

### 5. 注意点

- **生成したノードは解放していない。** `uninstall` してもグラフィクスヒープに残る。
  ゲーム再起動で消える。何度も install/uninstall を繰り返すとその分だけ漏れる
  （1 個 340 バイト）
- ノードは `HOLDER[1]` で管理しているので、**`uninstall` で HOLDER がゼロ埋めされると
  次の install で新しいノードが作られる**（前のものは孤児になる）

### 6. 次

**TODO-81: STUB を実際の描画に置き換える。** F-114 の 3 段構成を踏襲する。
**F-118 の制約に注意** — 同じ深度に同じ形を描くと深度テストで落ちるので、
深度を変えるか深度テストを切る必要がある。

---

