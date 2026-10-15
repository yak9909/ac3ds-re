---
id: ACNL-F0147
aliases:
- F-109
title: 'F-109: ★★実機で `g3d::FuncNode` の実在とコールバックを確認（HIGH 達成）'
summary: 'confidence: **HIGH**（CLAUDE.md の定義どおり**静的解析と動的観測の双方**で確認）'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5158976
- 5150632
- 5150628
- 9424656
- 2680988
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:6629-6711
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-109: ★★実機で `g3d::FuncNode` の実在とコールバックを確認（HIGH 達成）

confidence: **HIGH**（CLAUDE.md の定義どおり**静的解析と動的観測の双方**で確認）

TODO-59。

### 手順（CLAUDE.md 準拠）

`Scene_DrawLayers`(`0x4EB840`) の入口に `BPT_SOFT` を設置 → 即ヒット →
観測 → **bp を削除してから再開**。F-104 で確立したサイクル。

### 1. ★F-108 の「呼び出し元は 2 つ」が実機で裏付けられた

ヒット時 **`LR = 0x004E97A8`** = `sub_4E976C`(`0x4E97A4` の次)。

**`if (a1 == 1024)` の門が掛かる `sub_4EEDD8` ではなく、
無条件経路の `sub_4E976C` が動いていた。**
F-106 / F-107 を一本道と書いていた誤りが実機でも確認された。

```
R0(scene) = 0x329BA8F0   R1(a2) = 0x30F99EF4   LR = 0x004E97A8
```

### 2. ★★FuncNode インスタンスが実在した

シーンのノード配列（`scene[3]`..`scene[4]`）を走査:

```
scene=329BA8F0  node配列=329B3520..329B3524  ノード数=1
  [0] node=30896220  vptr=008FCF10  ★g3d::FuncNode
       cb0  = 00000000    （レイヤー 0 は未設定）
       cb1  = 0028E89C    ★レイヤー 1 に実関数
       user = 3309C334
```

- **`vptr` が静的 IDB の `vtbl_g3d_FuncNode`(`0x8FCF10`) と完全一致**
- **`+0x148` / `+0x14C` / `+0x150` のオフセットが予測どおり**
- **このシーンは FuncNode 1 個だけで構成されている**

### 3. ★★登録されているコールバックが「定石」そのものだった

`cb1 = sub_28E89C`(`0x28E89C`) の中身:

```c
sub_4EFA00(); sub_4E9E9C(...);               // 前処理
GpuCmd_GetProperty(520, &p);                 // ★現在の書き込み位置を取得
sub_12EC54(p, *(a2+180), 4 * *(a2+184));     // ★ブロック転送でコマンドを積む
... ヘッダを直接書く ...
GpuCmd_Advance((... + 440) & ~3);            // ★書き込み位置を進める
```

**F-97 で「自前でコマンドを積む定石」として書いた手順と完全に同じ。**
ゲーム自身が FuncNode のコールバック内でそれをやっている。

### 4. 積んでいるコマンド（`registers.h` で照合）

| 十進 | 16 進 | reg | 名前 |
|---|---|---|---|
| 983553 | `0x000F0201` | `0x201` | `GPUREG_ATTRIBBUFFERS_FORMAT_LOW` |
| 983554 | `0x000F0202` | `0x202` | `GPUREG_ATTRIBBUFFERS_FORMAT_HIGH` |
| -2109799933 | `0x823F0203` | `0x203` | `GPUREG_ATTRIBBUFFER0_OFFSET`（extra=35, consec=1） |
| -2143354318 | `0x803F0232` | `0x232` | `GPUREG_FIXEDATTRIB_INDEX`（extra=3, consec=1） |

**頂点属性バッファの設定。`do..while` の 12 回ループは
PICA200 の属性バッファ 12 本と一致する。**

### 5. これで確定したこと（`HIGH`）

- `g3d::FuncNode` は実機に**実在し、シーンに繋がっている**
- コールバックのオフセット `+0x148` / `+0x14C` / `+0x150`
- **コールバック内で `g_GpuCmdPtr` に直接コマンドを積むのが正規の使い方**
- `Scene_DrawLayers` の呼び出し元が 2 つあること（F-108 の訂正）

### 6. 未確認

- 観測できたのは **`cb1`（レイヤー 1）のみ**。`cb0` は 0 だった。
  レイヤー 0 を使う FuncNode は別のシーンにあるはず
- ノードをシーングラフに繋ぐ手順（TODO-60）
- `g3d_FuncNode_SetCallbacks` の呼び出しの瞬間は観測していない
- 別シーン（`sub_4EEDD8` / `a1 == 1024` 経路）のノード構成

---

