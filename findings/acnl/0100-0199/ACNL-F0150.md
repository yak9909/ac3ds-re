---
id: ACNL-F0150
aliases:
- F-112
title: 'F-112: ★★実機で F-111 を検証（TODO-64 完了）— 確度 `HIGH` へ。配列 #5 の記述を訂正'
summary: 'confidence: **HIGH**（静的解析と実機観測の双方で一致。CLAUDE.md の `HIGH` 定義を満たす）'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 10236056
- 9418496
- 10236068
- 9418928
- 5150632
- 6875784
- 9424656
- 7625888
- 4816168
- 2680988
- 9420084
- 9214704
- 4902436
- 4819040
- 4821120
- 4821148
- 4818944
- 4820768
- 4822296
- 5158976
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:6925-7011
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0153"]
---
## F-112: ★★実機で F-111 を検証（TODO-64 完了）— 確度 `HIGH` へ。配列 #5 の記述を訂正

confidence: **HIGH**（静的解析と実機観測の双方で一致。CLAUDE.md の `HIGH` 定義を満たす）

※ 本項には後日 F-115 で訂正した点がある: 配列 #5 の扱いと、
「どの Visit も配列 #0 に入れる」を 2 本しか読まずに一般化していた点。

### 1. 静的な主張と実機の突き合わせ

| 主張（F-111, 静的） | 実機で観測した値 | 判定 |
|---|---|---|
| `g_SceneContexts`(`0x9C3098`) は `SceneContext` × 3 | 3 つとも `vptr = 0x008FB700` = `vtbl_nw_gfx_SceneContext` | ✔ |
| `g_SceneTraversers`(`0x9C30A4`) は `SceneTraverser` × 3 | 3 つとも `vptr = 0x008FB8B0` = `vtbl_nw_gfx_SceneTraverser` | ✔ |
| `traverser+8` が対応する `SceneContext` | `trv[i]+8 == ctx[i]` が **3 組とも厳密に一致** | ✔ |
| 配列 #0 は `alloc=+0x08 / begin=+0x0C / end=+0x10 / cap=+0x14` | `alloc = g_GfxAllocator`(`0x329A4820`)、`cap = 1024`（3 つとも） | ✔ |
| `Render_DrawScene2` は `g_SceneContexts[2]` を描く | `Scene_DrawLayers` 到達時 `R0 = 0x329BA8F0` = `ctx[2]`、`LR = 0x4E97A8` | ✔ |
| `Scene_SubmitNode` の `R0` は holder、`R1` は sceneIndex | `R0 = 0x3309BE28`、`R1 = 0`、`*(R0+4) = 0x329D7B0C` | ✔ |
| その node が配列 #0 へ push される | 呼び出し前 `n = 0` → 復帰時（`LR = 0x68EA88`）`n = 1`、要素 = `0x329D7B0C` | ✔ |

**`n: 0 → 1` と要素の一致が決定的。** F-111 の経路はこれで実証された。

### 2. 実機で見た `FuncNode` の実体

`Scene_DrawLayers` 到達時、`ctx[2]` の配列 #0 は **1 件だけ**だった。

```
node   = 0x30896104
vptr   = 0x008FCF10   = vtbl_g3d_FuncNode
vt[2]  = 0x00745CA0   = g3d_FuncNode_GetTypeNode
vt[4]  = 0x00497D28   = nwgfx_SceneNode_Accept   ★F-111 の主張どおり
+0x18/+0x1C = 0 / 0   ← 子ノードなし
cb0    = 0x00000000
cb1    = 0x0028E89C   ← F-109 で見たものと同一インスタンス
ud     = 0x3309C334
```

**子ノードが 0 件**であることは、「シーングラフの木に繋がず毎フレーム `Accept` を呼ぶ」
という F-111 の解釈を支持する。

### 3. ★訂正 — カメラが入るのは配列 #5 ではなく **#4**

F-111 の表で配列 #5 を「カメラ系」と書いたが**誤り**。
根拠は `Render_DrawSceneIndexed` が `v4+92/96` を回していたことだけで、裏を取っていなかった。

実機で `Scene_SubmitNode` に引っ掛かったノードが `nw::gfx::Camera`
（`vptr = 0x008FBD34` = `vtbl_nw_gfx_Camera`、TypeInfo `0x8C9AF0` = `ti_nw_gfx_Camera`）
だったので、その `Accept` を辿って確定させた。

`nw::gfx::Camera::Accept`(`0x4ACE24`) → visitor の `vtbl[8]`(`0x498860`):

```c
nwut_Array_PushBack(ctx + 8,   &node);   // 配列 #0（描画対象）
...      ctx + 72..84 へ手書き push      // ★配列 #4（begin=+0x4C end=+0x50）
if (*(node + 40))
    nwut_Array_PushBack(ctx + 232, &node); // 配列 #14（begin=+0xEC end=+0xF0）
```

**配列 #5（`+0x5C`/`+0x60`）が何かは未確定。** TODO-66 に残す。

### 4. ★もう 1 つの訂正 — `Accept` はクラスごとに**違う visitor スロット**を呼ぶ

F-111 では「`visitor->vtbl[4]`」と書いたが、それは**汎用の `SceneNode::Accept` の場合だけ**。

| ノードのクラス | `Accept` | 呼ぶ visitor スロット |
|---|---|---|
| `SceneNode` / `g3d::FuncNode` | `0x497D28` | `vtbl[4]`（`+16`）= `0x499080` |
| `nw::gfx::Camera` | `0x4ACE24` | `vtbl[8]`（`+32`）= `0x498860` |

`SceneTraverser` の vtable にはこの種の Visit が **6 本**ある
（`vtbl[4..9]` = `0x499080` / `0x49909C` / `0x498800` / `0x498F20` / `0x498860` / `0x499518`）。
ノード種別ごとに「どの配列へ入れるか」が違う。

**どのクラスも配列 #0 には入る**ので、`Scene_DrawLayers` は
そこで型チェックして `Model` と `FuncNode` だけを処理している（Camera は素通り）。

### 5. 手順（実機、CLAUDE.md の bp サイクル準拠）

1. Suspend 中にメモリ直読みで vptr / `trv+8` / 配列 #0 を確認（bp 不要）
2. `add_bpt(0x4EB840)` → continue → ヒット → `R0`・配列 #0 を読む
3. **bp を削除**してから `add_bpt(0x4ED630)` → continue → ヒット → 引数を読む
4. **bp を削除**してから `add_bpt(LR = 0x68EA88)` → continue → 復帰時の `n` を読む
5. bp を削除 → `continue` + `suspend` を 1 呼び出しに束ねて後片付け

F-110 の制約（走行中は外から止められない）に従い、5 では continue と suspend を束ねた。

---

