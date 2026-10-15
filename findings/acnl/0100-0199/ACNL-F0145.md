---
id: ACNL-F0145
aliases:
- F-107
title: 'F-107: ★`g3d::FuncNode` の実在を確認。コールバック登録 API まで判明'
summary: 'confidence: **MEDIUM**（静的解析のみ。ただし独立した 2 経路から裏付け）'
date: '2026-08-24'
category: _triage
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5177268
- 1874256
- 2071148
- 2266280
- 2271108
- 2509832
- 2515560
- 2686500
- 2711168
- 3336504
- 5104308
- 5168992
- 5884276
- 5177176
- 5158976
- 9751112
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:6476-6555
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-107: ★`g3d::FuncNode` の実在を確認。コールバック登録 API まで判明

confidence: **MEDIUM**（静的解析のみ。ただし独立した 2 経路から裏付け）

TODO-55。CLAUDE.md「広域走査は静的 IDB かローカルのダンプでやる」に従い、
実機メモリを舐めず静的 IDB の `xrefs_to` から入った。

### 1. ★実在する。しかも常用されている

`g3d_FuncNode_Create`(`0x4EFFB4`) の**呼び出し元は 12 箇所**:

`0x1C9950` / `0x1F9A6C` / `0x2294A8` / `0x22A784` / `0x264C08` / `0x266268` /
`0x28FE24` / `0x295E80` / `0x32E938` / `0x4DE2B4` / `0x4EDF60` / `0x59C974`

**多様な subsystem に分布しており、汎用の拡張機構として使われている。**

### 2. ★コールバック登録 API

**`g3d_FuncNode_SetCallbacks(pNode, cb0, cb1, userdata)`(`0x4EFF58`)**

```c
型 = vtable[2](pNode[1]);
while (型 != &g_TypeNode_g3d_FuncNode) 型 = *型;   // 型チェック
v8 = node + 82;
*v8   = cb0;       // +0x148  レイヤー 0
v8[1] = cb1;       // +0x14C  レイヤー 1
v8[2] = userdata;  // +0x150
```

### 3. ★型ノードが 2 経路で一致 = 確定

- `Scene_DrawLayers`(`0x4EB840`) … 型が `&g_TypeNode_g3d_FuncNode` と一致する
  ノードで `n[82]` / `n[83]` を呼ぶ
- `g3d_FuncNode_SetCallbacks`(`0x4EFF58`) … 同じ型ノードと一致を確かめてから書く

**書く側と読む側が同じ型ノードを見ている。**
これで `dword_94CA60` = `g3d::FuncNode` の型、という推定が確定に変わった。

### 4. ★使い方の最小実例

`sub_1F9A6C`(`0x1F9A6C`, 全 4 行):

```c
sub_5A2A2C(a1 + 36, 2);
g3d_FuncNode_Create(a1 + 28, a1 + 20);                          // 生成
g3d_FuncNode_SetCallbacks(a1 + 28, sub_188340, sub_1883C8, a1); // 登録
dword_949360 = a1;
```

### 5. ★コールバックの中で実際に描ける

レイヤー 0 側の実体 `sub_188340`:

```c
sub_4EFA00(); sub_4EDEEC(...);          // 前処理
// userdata+148 = 件数、userdata+156 = 配列
// キューから取り出して (*(obj[0] + 8))(obj, g_DrawContext) を呼ぶ
```

**描画コンテキスト（`g_DrawContext` = `0x94CA48`）を使って
オブジェクトの描画メソッドを呼んでいる。**
`g_DrawContext` は `Scene_DrawLayers` がメッシュ提出
`sub_48D26C(g_DrawContext, mesh, model)` でも第 1 引数に渡すもの。

### 6. 手段 A の評価が上がった

`DOCS/rendering.md` の「手段 A: `g3d::FuncNode` のコールバックに乗る」は
**「使われているか未確認」という欠点が解消された。**
残る課題は「ノードをシーンに登録する手順」と「実機での発火確認」。

### 7. 未確認

- **実機で FuncNode インスタンスの存在・コールバック発火を見ていない**
  （見れば CLAUDE.md の `HIGH` 基準を満たす）
- ノードをシーングラフに繋ぐ手順（`Create` の第 1 引数 `out` の扱い）
- `g_DrawContext` の型・中身
- レイヤー 2 / 3 にはコールバックが無い理由

---

