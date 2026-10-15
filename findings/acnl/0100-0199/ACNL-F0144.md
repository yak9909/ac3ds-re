---
id: ACNL-F0144
aliases:
- F-106
title: 'F-106: ★`g3d::FuncNode` — 描画中に任意の関数を呼べるシーンノード'
summary: 'confidence: **MEDIUM**（静的解析のみ。CLAUDE.md の定義に従い実機未観測なので HIGH にしない）'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5158976
- 9892080
- 5177268
- 4772460
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:6408-6475
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-106: ★`g3d::FuncNode` — 描画中に任意の関数を呼べるシーンノード

confidence: **MEDIUM**（静的解析のみ。CLAUDE.md の定義に従い実機未観測なので HIGH にしない）

TODO-51。`sub_4EEDD8`(F-104) の描画本体 `sub_4EB840` を掘った結果。

### 1. `Scene_DrawLayers`(`0x4EB840`)

シーンをレイヤー別に 4 周して描画する。

```c
vtable[24] で前処理
for (i = 0; i <= 3; ++i)                      // ★4 レイヤー
  for (n = scene[3]; n != scene[4]; ++n)      // シーンノードのリスト
    型 = vtable[2](n);                        // オフセット 8
    while (型 != X) 型 = *型;                  // 親を辿って型判定
```

- 型が `&dword_96F0D4` … メッシュを回し、material のレイヤー番号が `i` と
  一致するものだけ `sub_48D26C(dword_94CA48, mesh, model)` で提出
- 型が `&dword_94CA60` … **コールバックを呼ぶ**（下記）

型ノードは `+0` が親へのポインタ。`dword_96F0D4` と `dword_94CA60` は
どちらも親が `0x96F0F0`。**sead 風の簡易 RTTI**（Itanium ABI の RTTI とは別物）。

### 2. ★`g3d::FuncNode`（RTTI 実名）

`g3d_FuncNode_Create`(`0x4EFFB4`) が生成する。**サイズ 340 = `0x154` バイト。**

| offset | 内容 |
|---|---|
| `+0x148`（`[82]`） | **コールバック（レイヤー 0 で呼ばれる）** |
| `+0x14C`（`[83]`） | **コールバック（レイヤー 1 で呼ばれる）** |
| `+0x150`（`[84]`） | **ユーザーデータ** |

`Scene_DrawLayers` 側の呼び出し形:

```c
if (i == 0 && n[82]) n[82](dword_94CA48, n[84]);
if (i == 1 && n[83]) n[83](dword_94CA48, n[84]);
```

**生成時は 3 つとも 0 に初期化される**ので、
**あとから関数ポインタを入れる設計**だと分かる。

### 3. ★これが自前描画の正規の注入点になりうる

**ゲーム自身が「描画中に任意の関数を呼ぶためのシーンノード」を持っている。**

- 第 1 引数に **描画コンテキスト**（`dword_94CA48`）が渡る
- 第 2 引数に **自分で入れたユーザーデータ**が渡る
- 呼ばれるのは **レイヤー 0 と 1**（4 レイヤー中）

コマンド列を手で `g_GpuCmdPtr` に積む（F-97）より、
**この仕組みに乗るほうがゲームの状態管理と喧嘩しない可能性が高い。**

### 4. 未解明・要検証

- **`g3d::FuncNode` が実際に使われているか未確認。**
  `g3d_FuncNode_Create` の呼び出し元を辿っていない
- `dword_94CA48`（描画コンテキスト）の実体
- `sub_48D26C`(`0x48D26C`) — メッシュ提出。`nw::gfx` 領域内
- 4 レイヤーの意味。別エージェントの家具解析（F-84）に
  「layer 2 登録」という記述があり、突き合わせる価値がある
- **実機で `FuncNode` が生成されているか、コールバックが実際に発火するか**

---

