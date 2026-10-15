---
id: ACNL-F0146
aliases:
- F-108
title: 'F-108: FuncNode 解析の精査 — 前提の再検証と 1 件の見落とし'
summary: 'confidence: **MEDIUM**（静的解析のみ）'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9751136
- 9424656
- 7625888
- 9892052
- 9420032
- 7581644
- 9892080
- 9418876
- 7566112
- 5173564
- 5150628
- 5178508
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:6556-6628
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-108: FuncNode 解析の精査 — 前提の再検証と 1 件の見落とし

confidence: **MEDIUM**（静的解析のみ）

F-106 / F-107 の内容と、その前提が上位の解析と噛み合うかを点検した。

### 1. ★型ノードの正体を第 3 の経路で確定

F-107 では「書く側と読む側が同じ型ノードを見ている」で裏を取ったが、
**クラス自身の vtable からも確認できた。**

| 型ノード | クラス | 根拠（vtable slot 2 = 型ゲッタ） |
|---|---|---|
| `0x94CA60` | **`g3d::FuncNode`** | `vtbl_g3d_FuncNode`(`0x8FCF10`) slot2 = `0x745CA0` |
| `0x96F0D4` | **`nw::gfx::Model`** | `vtbl_nw_gfx_Model`(`0x8FBD00`) slot2 = `0x73AFCC` |
| `0x96F0F0` | **`nw::gfx::TransformNode`** | `vtbl_nw_gfx_TransformNode`(`0x8FB87C`) slot2 = `0x737320` |

型ゲッタはいずれも `LDR R0,[PC]; BX LR` の 2 命令（8 バイト）。

**`nw::gfx::Model` と `g3d::FuncNode` の型ノードは
どちらも親が `nw::gfx::TransformNode`。**
nw4c のシーングラフ階層と一致する。

**「`vtable[2]` が型ゲッタ」という前提も、これで逆コンパイルの見た目ではなく
実際の関数の中身で裏が取れた。**

### 2. ★見落とし: `Scene_DrawLayers` の呼び出し元は 2 つある

F-106 / F-107 は `sub_4EEDD8` 一本道であるかのように書いていたが、**誤り**。

| 呼び出し元 | 条件 |
|---|---|
| `sub_4EEDD8`(`0x4EF13C`) | **`if (a1 == 1024)` の内側**。門が掛かる |
| `sub_4E976C`(`0x4E97A4`) | 別シーン `dword_9C30A0` を**無条件で**描画 |

**FuncNode のコールバックは 1024 の経路だけに限られない。**
`sub_4EEDD8` 自身にも呼び出し元が 2 つある（`sub_4EA01C` / `sub_4F2334`、未調査）。

### 3. 内部一貫性のチェック（いずれも合致）

- **オブジェクトサイズ**: 確保 340 = `0x154`、最後のフィールド `[84]` は `0x150`。
  `0x150 + 4 = 0x154` で**過不足なく終わる**
- **ハンドルの扱い**: `Create` は `*(out + 4) = node`（= `out[1]`）に書き、
  `SetCallbacks` は `pNode[1]` を読む。
  `sub_1F9A6C` は両方に同じ `a1 + 28` を渡す
- **コールバック署名**: 呼ぶ側 `cb(g_DrawContext, n[84])`、
  受ける側 `sub_188340(a1, a2)` が `a2+148/+156` をユーザーデータとして使い
  `a1` を描画に渡す
- **レイヤーの門**: `i==0` で `[82]`、`i==1` で `[83]`、`i>=2` は `continue`

### 4. ★別エージェントの解析と噛み合った

`g_TypeNode_nwgfx_TransformNode` を **`ModelInstance_Create`(`0x4F048C`)** が参照している。
これは別エージェントが命名した関数で、F-92 に `ModelInstance_SetRenderLayer` がある。

**`Scene_DrawLayers` の `i`（4 レイヤー）は、その「レンダーレイヤー」と同じ概念**
とみられる。TODO-58 が概念的に解けた。

### 5. 結論

**核心部分に誤りは見つからなかった。**
訂正は §2 の「呼び出し元が 2 つ」の 1 件のみ。
型ノードの同定はむしろ 3 経路で裏が取れて強化された。

### 6. 依然として未確認

- **実機での発火**（`MEDIUM` のまま。CLAUDE.md の `HIGH` には動的観測が要る）
- `sub_4EEDD8` の 2 つの呼び出し元
- `1024` / `1025` / `1040` が何を指すか
- ノードをシーングラフに繋ぐ手順

---

