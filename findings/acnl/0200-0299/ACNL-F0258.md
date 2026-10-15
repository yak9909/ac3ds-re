---
id: ACNL-F0258
aliases:
- F-233
title: 'F-233: 描画パス末尾と通常場面の実 replay を再監査 — `HIGH`（静的＋実機。ロード画像の順序は未測定）'
summary: '`HANDOFF_CHEATMENU.md` と F-200 / F-230 の前提を、`code.bin.i64` と'
date: '2026-09-01'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5908424
- 5908628
- 1798596
- 1798884
- 5520492
- 9379668
- 1048576
- 9894968
- 9420548
- 10161408
- 10158096
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:13778-13868
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-233: 描画パス末尾と通常場面の実 replay を再監査 — `HIGH`（静的＋実機。ロード画像の順序は未測定）

`HANDOFF_CHEATMENU.md` と F-200 / F-230 の前提を、`code.bin.i64` と
実機で独立に再確認した。最初の停止時だけロード画像が表示されていたが、
**最初に実機を走らせた時点でロードは終了した**（ユーザー確認）。
従って走行後の breakpoint / replay / capacity 標本はすべて通常場面として扱う。

### 1. `Frame_EndDrawPass1024/1040` は通常の submit 関数ではない

- `Frame_EndDrawPass1024` (`0x5A27C8`) は `dword_94C8A0 == 0` なら即 return
- `Frame_EndDrawPass1040` (`0x5A2894`) は `byte_94C898 == 0` なら即 return
- ロード画像表示中の初期停止（走行前）では両 guard 値が 0
- `0x5A27C8` の breakpoint 到達はロード終了後の通常場面。stock は guard 0 なら早期 return

従って「ここへ積めば stock が直後に必ず `GpuCmd_SplitAndSubmit` する」は誤り。
両関数は**パス末尾の位置にある任意エフェクト処理**であり、通常 submit 点ではない。
フック位置の候補にはなるが、提出まで必要なら自前で明示する必要がある。

### 2. 実際のパス順

software breakpoint を両入口へ置き、ヒットしたものを必ず削除して再開した。

```
Frame_DrawPass1024 (0x1B71C4, 上) → Frame_DrawPass1040 (0x1B72E4, 下)
→ 次の Frame_DrawPass1024
```

両入口の呼出し元は `LR=0x543C6C` (`MethodTree_WalkAndInvoke`)。同じ描画 thread 219。
旧コメントの「1040 → 1024」はフレーム境界の取り方ではなく、実測順として訂正する。

### 3. 通常場面では「最後に Layout へ入る」と「GPU へ実際に再生する」は別

`probe_screen_order.py` では、Layout 関数入口の最後は従来どおり:

| pass | 最後に入口へ来た Layout | list id |
|---|---:|---:|
| 1024 | `0x32C4CBCC` | 8 |
| 1040 | `0x3225AF24` | 15 |

しかしロード終了後に `GpuCmd_ReplayRecordedListRange` を直接記録し、
同時に pass 印も保存すると、通常場面の非ゼロ再生列は両 pass とも次の繰り返しだった。

```
Render_DrawSceneIndexed: list id 4 または 5, length 0x92B0
Layout_ReplayRecordedList: list id 30, length 0x1940..0x2E50
```

list id 8 / 15 は「入口では最後」でも、その通常場面標本では非ゼロ長の replay として現れなかった。
これは「Layout 入口の最後」を「実 replay の最後」と同一視できないことを示す。
従って、その同一視に依存した F-230 の別経路断定は未立証へ戻す必要がある。
ただし list id 30 は**通常場面の標本**であり、ロード画像へ結び付けてはならない。

list id 30 の breakpoint 標本:

```
pass=1 / layout=0x330A494C / vptr=0x008F1F54 (vtbl_Layout)
list id=30 / length=0x2E50 / layout+0x134=0x400
```

### 4. 通常場面の上画面パス末尾では主リストと Drawer が利用可能

`0x5A27C8` 入口の実機標本（計算は IDAPython）:

```
g_GpuCmdPtr = 0x323B59A8
base        = 0x323B2130
g_GpuCmdEnd = 0x324B2130
capacity    = 0x100000
used        = 0x3878
remaining   = 0xFC788
```

`*(0x96FC38)+0x364 = 0x32FF62EC`、vptr `0x008FBF04 = vtbl_nw_lyt_Drawer`。
静的には `Layout_ReplayRecordedList` が非ゼロ長のとき、この同じ Drawer に
`sub_4B8C34(drawer, layout+0x30, 0)` を通してから replay する。

したがって主リストの容量と有効な Drawer の存在は静的・動的で一致する。
ただし現行 `cave_draw_topmost.py` はマテリアル・UV・テクスチャ・頂点を自前設定する一方、
**投影は Drawer に残った直前の有効 Layout 状態へ依存する。**
「投影まで完全に自前確立済み」という引き継ぎ記述は訂正する。

### 5. ロード画像表示中の初期停止状態ではプラグイン描画が無効だった

現行7フックはすべて stock、`0x009B0D00` の LOG と確保スロット `0x009B0010` は全て 0。
この標本だけから「現行メニューがロード画像に隠された」とは判定できない。
次のロード実機A/Bでは、ユーザーがロード画像表示を目視確認して Suspend した状態で、
プラグインを明示的に有効化し、フック語と LOG 非ゼロを確認してから比較する。
ロード画像表示中の低レベル replay 順は今回取得できていない。

---

