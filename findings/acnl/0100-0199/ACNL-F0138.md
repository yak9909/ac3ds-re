---
id: ACNL-F0138
aliases:
- F-100
title: 'F-100: 再々精査 — GX 5 本の type バイト確定、「実装位置」表記の誤りを訂正'
summary: 'confidence: **MEDIUM**（**静的解析のみ**、F-101 で訂正。表題の「HIGH 化」も撤回）'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1268044
- 1273224
- 1273612
- 1268096
- 1273448
- 1268064
- 1274264
- 1268128
- 1273820
- 4809012
- 5525076
- 4771840
- 5079040
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5870-5938
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-100: 再々精査 — GX 5 本の type バイト確定、「実装位置」表記の誤りを訂正

confidence: **MEDIUM**（**静的解析のみ**、F-101 で訂正。表題の「HIGH 化」も撤回）

### 1. ★GX 関数 5 本すべてを type バイトで確定（MEDIUM-HIGH → HIGH）

F-96 で「switch の位置からの同定」に留めていた 4 本を、
**impl 側で type バイトを書く命令を直接確認**した。

| type | 公開関数 | impl | 確認した命令 |
|---|---|---|---|
| 0 `RequestDma` | `0x13594C` | `0x136D88` | `MOV R12,#0` → `STRB R12,[SP,#0]` |
| 1 `SetCommandList` | `0x136F0C` | — | `LOBYTE(hdr)=1`（flush 時 5） |
| 2 `MemoryFill` | `0x135980` | `0x136E68` | `LOBYTE(v10[0])=2` |
| 3 `DisplayTransfer` | `0x135960` | `0x137198` | `LOBYTE(v10)=3` |
| 4 `TextureCopy` | `0x1359A0` | `0x136FDC` | `MOV R12,#4` → `STRB R12,[SP,#0]` |

`0x13594C` の `MOV R12,#1` は**スタック引数のフラグ**であって type ではなかった。
危うく「type 1」と誤読するところだった。

GX コマンドが **0x20 バイト = `u32 x 8`** であることも
ctrulib `gspgpu.h` の `gspSubmitGxCommand(u32*, u32 gxCommand[0x8])` で裏付けた。

### 2. ★「実装位置」と書いたものは全部デストラクタだった

F-94 で

> `nw::gfx::RenderContext` の実装 … `0x496134` 付近

のように書いたが、**これらは vtable の `[0]` = デストラクタ**。
クラスの実体メソッドは非仮想のものが多く、別の場所にある。

同じ誤りが `sead::PrimitiveDrawer` の「実装 `0x544E54` 付近」にもあった。
**`PrimitiveDrawer` の描画メソッドは未特定のまま。**

派生して、「nw4c 本体は `0x48D000`-`0x4D8000`」も
**dtor の分布からの推定**でしかない。区間として断定しない。

### 3. GSP スタブの検証を補強

F-94 の 6 本について、リテラル一致に加えて
**IPC ヘッダを形式で分解し引数個数と突き合わせた**:

`header = cmd<<16 | normal<<6 | translate`

- `0x00010082` → normal 2 / translate 2
  = `tls[1]`(addr), `tls[2]`(size) + 静的バッファ記述子 `tls[3]`, ポインタ `tls[4]` ✓
- `0x00080082` → normal 2 / translate 2
  = addr, size + ハンドル記述子 `tls[3]=0`, handle ✓

**記憶に依存しない構造的な裏付けになった。**
API 名と署名は同梱 ctrulib `services/gspgpu.h` で照合済み。

### 4. 名前からの推測として明示したもの

- 「`sead::MethodTreeMgr` / `MethodTreeNode` が毎フレームの呼び出し木」
  … **クラス名からの推測。未検証。**
- 「`sead::UlcdDoubleCmdGameFrameworkCtrNw4c` がアプリのフレームワーク本体」
  … RTTI で**クラスの存在と継承**は実測したが、
  **実際に生成・使用されているかは未確認。**

### 5. 今回の精査で新たな誤りが出なかったもの

`g_GpuCmdPtr` / `g_GpuCmdEnd` / `GpuCmd_Advance` / `GpuCmd_GetProperty` /
`GpuCmd_SplitAndSubmit` の構成 / `Copy24Bytes`（6 dword = 24B を確認）/
RTTI による継承関係。

---

