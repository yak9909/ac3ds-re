---
id: ACNL-F0149
aliases:
- F-111
title: 'F-111: ★★TODO-60 解決 — ノードをシーンに載せる仕組み（`Scene_SubmitNode`）'
summary: 'confidence: **HIGH**（当初 MEDIUM。**F-112 の実機観測で昇格**）'
date: '2026-08-24'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5150668
- 10236056
- 10236064
- 10236068
- 4783468
- 5153812
- 10236040
- 5166640
- 4816168
- 4821120
- 5184740
- 4822104
- 2071148
- 2071492
- 5186356
- 5152796
- 5150572
- 5150632
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:6784-6924
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-111: ★★TODO-60 解決 — ノードをシーンに載せる仕組み（`Scene_SubmitNode`）

confidence: **HIGH**（当初 MEDIUM。**F-112 の実機観測で昇格**）

※ 本項には誤りが 2 件あり、いずれも F-112 で訂正済み:
配列 #5 の用途と、`Accept` が呼ぶ visitor スロットがクラスごとに違う点。

「`g3d::FuncNode` をどうやってシーングラフに繋ぐか」の答え。
**結論から言うと「繋がない」。毎フレーム登録する。**

### 1. `Scene_DrawLayers` の `a1` の正体は `nw::gfx::SceneContext`

`Render_InitGlobal`(`0x4E97CC`) が 3 個生成している:

```c
for (k = 0; k < 3; ++k) {
    g_SceneContexts[k]   = sub_48E384(v54, g_GfxAllocator);   // vtbl_nw_gfx_SceneContext を入れる
    g_SceneTraversers[k] = nwgfx_SceneTraverser_Create(...);   // vtbl_nw_gfx_SceneTraverser
}
```

`g_SceneContexts` = `0x9C3098`（`[2]` が `0x9C30A0` = 従来 `dword_9C30A0`）。
`g_SceneTraversers` = `0x9C30A4`。

### 2. `SceneContext` のレイアウト

デストラクタ(`0x48FD6C`)と `Scene_ResetAllContexts`(`0x4EA414`) の
**両方から独立に同じ形が読める**（CLAUDE.md「独立に得た 2 つの結果を突き合わせる」）:

```
+0x00  vtable
+0x04  ?
+0x08 + 0x10*n   配列 n = { allocator, begin, end, flags|capacity }   n = 0..14（15 本）
                 ★4 番目は 上位2bit=フラグ / 下位30bit=capacity（F-115 で訂正）
```

| 配列 | begin / end | 用途 |
|---|---|---|
| #0 | `+0x0C` / `+0x10` | **★描画対象ノード（`Scene_DrawLayers` が回す）** |
| #4 | `+0x4C` / `+0x50` | **カメラ**（F-112 で確定） |
| #5 | `+0x5C` / `+0x60` | 不明（`Render_DrawSceneIndexed` が `sub_4A41EC` を回す）。**F-111 で「カメラ系」と書いたのは誤り → F-112 で訂正** |
| #7 | `+0x7C` / `+0x80` | `g_RenderQueue`(`0x9C3088`) へ配る何か |
| #9 | `+0x9C` / `+0xA0` | 同上（`+16` へ） |
| #10 | `+0xAC` / `+0xB0` | 同上（`+12` へ） |

### 3. ★登録の入口 — `Scene_SubmitNode`(`0x4ED630`)

```c
int Scene_SubmitNode(int pHolder, int sceneIndex)
{
  int node = *(int *)(pHolder + 4);          // g3d_FuncNode_Create が書く位置と同じ
  return (*(vtbl(node)[4]))(node, g_SceneTraversers[sceneIndex]);
}
```

**呼び出し元は 40 件以上ある。ゲーム全体の汎用 API。**

### 4. その先 — ビジター

`vtable[4]` = `nwgfx_SceneNode_Accept`(`0x497D28`):

```c
visitor->vtbl[4](visitor, this);                   // Visit(this)
for (child in [this+0x18, this+0x1C))              // ★子ノード配列
    child->vtbl[4](child, visitor);                // 再帰
```

`nwgfx_SceneTraverser_Visit`(`0x499080`):

```c
ctx = *(traverser + 8);                 // BindContext で入れた SceneContext
nwut_Array_PushBack(ctx + 8, &node);    // ★配列 #0 へ push
```

**`ctx + 8` は配列 #0。`Scene_DrawLayers` が回すのはまさにこれ。輪が閉じた。**

### 5. ★毎フレーム必要な理由

`Render_FrameEnd`(`0x4F1CE4`) がフレーム末に
`Scene_ResetAllContexts`(`0x4EA414`) を呼び、
`nwgfx_SceneTraverser_BindContext`(`0x499458`) 経由で
**15 本の配列を全部空にする**（`end = begin`）。

だから **`Scene_SubmitNode` は毎フレーム呼び直さないと描かれない。**
`SceneNode` には子配列（`+0x18`/`+0x1C`）があり本物のシーングラフは存在するが、
**ゲーム側はそれに繋がず、毎フレーム直接 `Accept` を呼ぶ使い方をしている。**

### 6. ★自前描画の完全な手順（TODO-60 の成果物）

```
一度だけ:
  1. g3d_FuncNode_Create(&holder, allocator)        → holder[1] にノード
  2. g3d_FuncNode_SetCallbacks(&holder, cb0, cb1, userdata)

毎フレーム:
  3. Scene_SubmitNode(&holder, sceneIndex)

すると Scene_DrawLayers が:
  レイヤー 0 で cb0(g_DrawContext, userdata)
  レイヤー 1 で cb1(g_DrawContext, userdata)
を呼ぶ。コールバックの中で F-97 の定石どおり g_GpuCmdPtr へ積む。
```

**最小の実例がゲーム内にある**（生成と登録が別関数なのが要点）:

| 役割 | 関数 |
|---|---|
| 生成 | `sub_1F9A6C`(`0x1F9A6C`) — `g3d_FuncNode_Create(a1+28, a1+20)` + `SetCallbacks` |
| 登録 | `sub_1F9BC4`(`0x1F9BC4`) — `Scene_SubmitNode(a1+28, 0)` |

### 7. sceneIndex の意味（`MEDIUM`。要実機確認 = TODO-65）

| index | 描画する関数 | 条件 |
|---|---|---|
| 0 | `Render_DrawScene0`(`0x4F2334`) → `Render_DrawSceneIndexed(a1, 0)` | `byte_94CA2C == 0` |
| 1 | `Render_DrawScene1`(`0x4EA01C`) → `Render_DrawSceneIndexed(a1, 1)` | `byte_94CA2C == 1` |
| 2 | `Render_DrawScene2`(`0x4E976C`) → `Scene_DrawLayers(g_SceneContexts[2], …)` | **無条件** |

`byte_94CA2C` は `Render_InitGlobal` の末尾で `0` に初期化される。
**0 と 1 は排他のモード切り替えに見えるが、意味は未確定。**
F-109 で実機の `LR` が `0x4E97A8` だったのは **index 2 の経路**。

### 8. 旧記述の訂正

F-104 のコメントに「`sub_4EEDD8` の `1024 / 1025 / 1040` は
sead のバッファ / ターゲット ID と同じ値」と書いたが、
**`sceneIndex` を決めているのは第 2 引数 `a2` であって `a1` ではない。**
`a1`（1024 等）は `if (a1 == 1024)` の門にしか使われていない。両者は別物。

### 9. IDB へ反映済み

`Scene_SubmitNode` / `nwgfx_SceneNode_Accept` / `nwgfx_SceneTraverser_Visit` /
`nwut_Array_PushBack` / `nwgfx_SceneTraverser_BindContext` /
`Scene_ResetAllContexts` / `Render_FrameEnd` / `Render_InitGlobal` /
`Render_DrawScene0` / `Render_DrawScene1` / `Render_DrawScene2` /
`Render_DrawSceneIndexed` / `nwgfx_SceneContext_Finalize` /
`nwgfx_SceneTraverser_Create` / `SortMeshGroup_InitAll` /
`g_SceneContexts` / `g_SceneContext_2` / `g_SceneTraversers` / `g_GfxAllocator`

---

