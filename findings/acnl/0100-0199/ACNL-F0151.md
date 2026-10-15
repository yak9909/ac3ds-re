---
id: ACNL-F0151
aliases:
- F-113
title: 'F-113: ★★TODO-68 完了 — `BsShadowViewMgr` が実例。フレーム描画の全体像と `1024`/`1040` の正体'
summary: 'confidence: **HIGH**（静的解析と実機観測の双方。実機の `LR` とスタックで連鎖を確認）'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5520456
- 2680988
- 9349680
- 9196244
- 9200960
- 2686500
- 2686476
- 9741756
- 5373836
- 5373968
- 5374016
- 5374080
- 5376600
- 5369424
- 5369408
- 1798596
- 1798884
- 5373928
- 5376640
- 5369632
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:7012-7167
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-113: ★★TODO-68 完了 — `BsShadowViewMgr` が実例。フレーム描画の全体像と `1024`/`1040` の正体

confidence: **HIGH**（静的解析と実機観測の双方。実機の `LR` とスタックで連鎖を確認）

※ F-115 で追検証: 2 パスの**実行順は当時は推測**だったが実機で確定した。
呼び出し元は `MethodTree_WalkAndInvoke`(`0x543C48`)。

F-112 で見た `FuncNode`（`cb1 = 0x28E89C`, `ud = 0x3309C334`）の持ち主を特定した。

### 1. 持ち主は `BsShadowViewMgr`

`sub_28FE24` が sead ヒープ `"BsShadowViewMgr"` を作っており、そこから特定できた
（CLAUDE.md「一次情報（ゲーム内の文字列）が取れるものは常にそちらが上」）。

RTTI: `vtbl_BsShadowViewMgr`(`0x8EAA30`) / `ti_BsShadowViewMgr`(`0x8C52D4`)。
**基底は `ti_Base`**(`0x8C6540`)。

### 2. 生成側 — `BsShadowViewMgr_Create`(`0x28FE24`) = vtable[3]

```c
sead ヒープ "BsShadowViewMgr" 102400 バイトを this+188 に作る
部屋の種類を見て *(this+197) を 0..4 に決める
g3d_FuncNode_Create(this + 168, this + 188);          // holder, allocator
g3d_FuncNode_SetCallbacks(this + 168, 0, sub_28E89C, this);
*(this + 200) = (*(this+197) == 4) ? 0 : 2;           // ★sceneIndex
```

**`cb0 = 0` / `cb1 = 0x28E89C` は実機観測（F-109 / F-112）と完全一致。**

### 3. 登録側 — `BsShadowViewMgr_SubmitToScene`(`0x28FE0C`) = vtable[12]

```c
Scene_SubmitNode(this + 168, *(this + 200));
```

**`sceneIndex` がオブジェクトのフィールドから来ているのが要点。**
部屋カテゴリが `4`（既定＝屋外系と思われる）なら `0`、それ以外は `2`。

実機（Suspend 中のメモリ直読み）:

| 読んだもの | 値 | 判定 |
|---|---|---|
| `g_BsShadowViewMgr`(`0x94A5BC`) | `0x3309C334` | `ud` と一致 ✔ |
| `*(this + 168 + 4)` | `0x30896104` | **`ctx[2]` の配列 #0 にいた FuncNode と同一** ✔ |
| `*(this + 197)` | `3` | 部屋カテゴリ |
| `*(this + 200)` | `2` | sceneIndex ✔（`ctx[2]` にいたことと整合） |

### 4. ★`Base` のライフサイクル — 4 フェーズ × (pre, main, post)

`Obj_InvokePmfTriple`(`0x51FF8C`, **旧名 `UiScreen_RunCreateVirtual`**) は
`UiScreen` 専用ではなく、**Itanium ABI のメンバ関数ポインタを呼ぶ汎用トランポリン**だった。
奇数ビット = virtual フラグ、`>>1` = vtable オフセット。
`pre()` が非 0 を返したときだけ `main()` を呼び、最後に必ず `post(result)`。

| フェーズ | vtable slot (pre/main/post) | 起動関数 |
|---|---|---|
| A（生成） | 2 / 3 / 4 | `BaseObj_InvokeCreateTriple`(`0x520010`) |
| B | 5 / 6 / 7 | `BaseObj_InvokePhaseBTriple`(`0x520040`) |
| C | 8 / 9 / 10 | `BaseObj_InvokePhaseCTriple`(`0x520080`) |
| **D（描画）** | **11 / 12 / 13** | `BaseObj_InvokeDrawTriple`(`0x520A58`) |

### 5. ★`Base` オブジェクトの連結リストを毎フレーム走査する

`BaseObj_RunDrawPhase`(`0x51EE50`):

```c
*(mgr + 70700) = 5;                              // フェーズ番号
for (n = *(mgr + 53268); n; n = *(n + 4)) {      // ★連結リスト
    obj = *(n + 8);
    if (!*(obj + 15) && 可視ビットチェック)
        BaseObj_InvokeDrawTriple(obj);            // slot 11 → 12 → 13
}
*(mgr + 70700) = 0;
```

`mgr` は `vc_GETDATA1`(`0x51EE40`) が返す。
**CTRPF のラベル `vc_GETDATA1` は作者の用途名で、実体は「`Base` オブジェクト
マネージャのシングルトン取得」**（CLAUDE.md の注意どおり、ラベルを正体と取らない）。

| offset | 内容 |
|---|---|
| `+0xD014` (53268) | `Base` オブジェクトの連結リスト先頭（node: `+4` next, `+8` obj） |
| `+0x1102C` (69676) | 可視ビットマップ |
| `+0x1142C` (70700) | 現在のフェーズ番号（描画中は 5） |

### 6. ★★1 フレームの描画（`Frame_DrawPass1024` → `Frame_DrawPass1040`）

```c
Frame_DrawPass1024()  0x1B71C4
    mgr = vc_GETDATA1();
    BaseObj_RunDrawPhase(mgr);   // ★全 Base オブジェクトの slot 12 → Scene_SubmitNode
    Render_DrawScene2();         // g_SceneContexts[2]（無条件）
    ...
    Render_DrawScene0(1024);     // g_SceneContexts[0]
    ...
    Render_DrawScene1(1024);     // g_SceneContexts[1]

Frame_DrawPass1040()  0x1B72E4
    （登録なし。Render_DrawScene2 も呼ばない）
    Render_DrawScene0(1040);
    ...
    Render_DrawScene1(1040);
    Render_FrameEnd();           // ★全配列クリア + ダブルバッファ切替
```

**登録は 3 つのシーン描画の前に 1 回だけ走る。**

### 7. ★TODO-61 解決 — `1024` / `1040` の正体

`Render_DrawSceneIndexed` の `if (a1 == 1024)` は、**この 2 つのパスを区別する門**だった。

- **`1024` のパスだけが `Scene_DrawLayers` とコマンド提出を行う**
- `1040` のパスは末尾処理のみ

`1024` / `1040` は**呼び出し元がリテラルで渡すタグ**で、
`Render_DrawScene0` / `Render_DrawScene1` の呼び出し元はこの 2 関数だけ。
F-104 で挙げた `1025` はこの 2 関数には現れない。

**2 つのパスが上画面 / 下画面に対応するかは未確認**（仮説、TODO-70）。

### 8. 自前描画を入れるときの結論

**`BsShadowViewMgr` の形をそのまま真似るのが最短。**

```
生成フェーズ（slot 3 相当）で:
    g3d_FuncNode_Create(&this->holder, allocator);
    g3d_FuncNode_SetCallbacks(&this->holder, cb0, cb1, this);
描画フェーズ（slot 12 相当）で:
    Scene_SubmitNode(&this->holder, sceneIndex);
```

既存の `Base` オブジェクトの slot 12 をフックすれば、
**新しいオブジェクトを作らずに 1 ノード足せる**（`BsShadowViewMgr` の
`Scene_SubmitNode` の直後に自前 holder をもう 1 回 submit するだけ）。

### 9. 検証手順（CLAUDE.md の bp サイクル準拠）

1. 静的に `cb1 = sub_28E89C` の登録元 `sub_28FE24` を特定
2. Suspend 中のメモリ直読みで `g_BsShadowViewMgr` / holder / `+200` を確認
3. `add_bpt(0x28FE0C)` → continue → ヒット → `LR = 0x51FFE8`、`R0 = 0x3309C334`
4. bp を削除 → `continue` + `suspend` を 1 呼び出しに束ねて後片付け
5. スタックにあった `0x00520A80` / `0x0051EF20` が
   `sub_520A58` / `sub_51EE50` 内の戻り先と一致することを静的に照合
   （**xref から辿った連鎖と独立に一致**）

### 10. 途中で 1 度、逆コンパイラの破綻に当たった

`xrefs_to` をまとめて投げた結果が壊れており、`0x51E91C` を逆コンパイルしたら
無関係な関数（`sub_51E884`）が出た。CLAUDE.md の
「逆コンパイラが破綻している箇所は関数境界の誤りを疑い、その経路の結論を採用しない」
に従い結論を採らず、`xrefs_to` を単独で投げ直したところ正しい
`sub_51EE50`(`0x51EE50`) が得られた。**まとめ投げの結果を鵜呑みにしない。**

---

