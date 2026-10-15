---
id: ACNL-F0282
aliases:
- F-259
title: 'F-259: ★★★★★UI 描画経路の完全な静的仕様。render.txt は本作と 1:1 で一致する — `HIGH`（静的のみ）'
summary: '`REFERENCES/TEXTS/render.txt` の `ssys::ma::lyt::Layout::RenderFrame` を、'
date: '2026-09-01'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5670612
- 1212124
- 1185468
- 8061388
- 8062384
- 5075316
- 8062612
- 9894968
- 5670260
- 5669748
- 5669596
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:15239-15355
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-259: ★★★★★UI 描画経路の完全な静的仕様。render.txt は本作と 1:1 で一致する — `HIGH`（静的のみ）

`REFERENCES/TEXTS/render.txt` の `ssys::ma::lyt::Layout::RenderFrame` を、
本作の `ssys_ma_lyt_Layout_RecordPaneTree`（`0x5686D4`）と行単位で対応させた。
**完全に一致する。以後 render.txt は仕様として扱ってよい。**

### 1:1 対応表

| render.txt | ACNL（`0x5686D4`） |
|---|---|
| `if (!m_ProjectionDirty) { SetupProjectionMatrix(this); m_ProjectionDirty = 1; }` | `if (!*(u8*)(L+0x11F)) { (*(vtable+0x18))(L); *(u8*)(L+0x11F) = 1; }` |
| `if (m_CmdBufferDirty)` | `if (*(u8*)(L+0x11D))` |
| `nngxGetCmdlistParameteri(NN_GX_CMDLIST_BINDING, &CmdList)` | `GpuCmd_GetProperty(519, &save)`（`0x127EDC`） |
| `nngxBindCmdlist(m_gl.CmdList)` | `GpuCmd_SelectList(*(u32*)(L+0x100))`（`0x1216BC`） |
| `nngxClearCmdlist()` | `sub_7B01CC`（`0x7B01CC`） |
| `nngxStartCmdlistSave()` | `sub_7B05B0`（`0x7B05B0`） |
| `Drawer->DrawBegin1(&Drawer, 1)` | `(*(*(u32*)(mgr+0x364) + 0x0C))(mgr+0x364, 1)` |
| `nw::lyt::Drawer::Draw(&Drawer, &m_DummyLayout.base, &m_DummyLayout.m_DrawInfo)` | `nwlyt_DrawPaneTreeToCurrentList(mgr+0x364, L+0x10, L+0x30)`（`0x4D7174`） |
| `Drawer->DrawEnd1(&Drawer, 1)` | `(*(*(u32*)(mgr+0x364) + 0x14))(mgr+0x364, 1)` |
| `nngxStopCmdlistSave(&off,&size,&reqId,&reqSize)` | `GpuCmd_CommitListAndCaptureDelta(L+0x104, L+0x108, L+0x10C, L+0x110)`（`0x7B0694`） |
| `nngxBindCmdlist(CmdList)` | `GpuCmd_SelectList(save)` |
| `m_CmdBufferDirty = 0` | `*(u8*)(L+0x11D) = 0` |

`mgr = *(0x0096FC38)`（`LayoutMgr`）、`mgr+0x364` が `nw::lyt::Drawer`。

### Layout の描画関連フィールド（確定）

| オフセット | 意味 | 根拠 |
|---|---|---|
| `+0x10` | Pane ツリーの入れ物（`+0x20` が root） | `nwlyt_DrawPaneTreeToCurrentList` |
| `+0x28` | 幅・高さ（float 2 本。scissor 計算に使う） | `Layout_ReplayRecordedList` |
| `+0x30` | DrawInfo／Drawer へ流し込む描画コンテキスト | 記録・再生の両方で使う |
| `+0x100` | **専用コマンドリストの id** | `GpuCmd_SelectList` の引数 |
| `+0x104` | 記録の開始オフセット | `Commit` の第 1 出力 |
| `+0x108` | **記録の長さ（バイト）**。`<= 0` なら再生しない | `Commit` の第 2 出力／F-240 |
| `+0x10C` | GX キューの開始 index | `Commit` の第 3 出力 |
| `+0x110` | GX キューの件数 | `Commit` の第 4 出力 |
| `+0x114` | 再生時の状態無効化フラグ | `ReplayRecordedListRange` の第 6 引数 |
| `+0x11C` | `allowNoSplit`（byte） | 同 第 7 引数 |
| `+0x11D` | **`m_CmdBufferDirty`（記録要求）** | 上の対応表。F-204 の「記録要求フラグ」の正体 |
| `+0x11F` | **`m_ProjectionDirty`** | 同上 |
| `+0x124` | 立体視オフセット（float） | `0x568574` |
| `+0x134` | display トークン（`0x400`/`0x410`/`0x401`） | `LayoutList_SetDisplay` が書く |
| `+0x138` | scissor 有効（byte） | `Layout_ReplayRecordedList` |
| `+0x13C`〜`+0x148` | scissor の矩形（float 4 本） | 同上 |
| `+0x320` | 立体視オフセットの有効（byte） | `0x568374` |
| `+0x0C` | **描画優先度（byte）**。昇順ソート挿入のキー | `LayoutMgr_AddLayout`（F-253） |
| `+0x04` / `+0x08` | prev / next | 同上 |

### コマンドリストのマネージャ構造（確定）

`GpuCmd_SelectList` / `sub_7B01CC` / `GpuCmd_SplitAndSubmit` の 3 つから確定した。
バケット表は `dword_AD98C0`、`id & 0x1F` で引き、`+7` 語目が鎖の先頭。

| オフセット | 意味 |
|---|---|
| `+0x00` | list id |
| `+0x04` | **base**（バッファ先頭） |
| `+0x08` | **size**（容量。`g_GpuCmdEnd = base + size`） |
| `+0x0C` | 現在のオフセット |
| `+0x14` | 提出済みオフセット |
| `+0x18` | GX キューのエントリ配列（28 バイト/件） |
| `+0x20` | GX キューの件数 |
| `+0x2C` | 生成時に 768 |
| `+0x40` | 次のマネージャ（id 昇順の鎖） |

**★未知の id を `GpuCmd_SelectList` に渡すと、68 バイトのヘッダを作って
ゼロ埋めするだけで base も size も 0 のまま。** その状態では
`g_GpuCmdPtr = g_GpuCmdEnd = 0` になり、`sub_7B01CC` も何もしない。
**したがって自前のリストを持つなら base と size を自分で入れる必要がある**
（F-236 で id 0x10 に対して実験済み）。

### 記録の内側

- `sub_7B05B0`（StartSave）: 8 バイト境界へパディングし、
  `dword_AD9A28 = 現在オフセット`、`dword_AD9A2C = GX キュー件数` を控える
- `GpuCmd_CommitListAndCaptureDelta`: 同じくパディングしてから
  `start = dword_AD9A28` / `len = 現在オフセット - start` /
  `qStart = dword_AD9A2C` / `qCount = 件数 - qStart` を書き出す
- `nwlyt_DrawPaneTreeToCurrentList`: カーソルは `g_GpuCmdPtr` から読み、
  `g_GpuCmdPtr` へ書き戻す。**レイアウトの境目ではカーソルはグローバルで受け渡される**

### ★これが意味すること — これまでの失敗の説明

我々は **replay の列に直接コマンドを積んで**いた。しかし GPU 状態
（テクスチャ結び付き・頂点属性の構成・TEV・投影）は
**`DrawBegin1` が記録の先頭で確立し、`DrawEnd1` が締める**ものである。

- 記録が走ったフレームでは、直前のレイアウトの記録内容が replay されて状態が残るので描けた
- 記録が走らないフレームでは状態が無く、GPU が止まった（F-256 / F-257）
- 作業配列を自前に差し替えても、`DrawBegin1` を通っていないので直らない（F-258）

**正しいやり方は「replay に積む」ではなく「自分で記録する」である。**

### 設計（次に実装する）

自前ノードを**本物の Layout と同じ契約**にする。

1. **自前のコマンドリストを持つ。** 未使用の id（例 100）で `GpuCmd_SelectList` を
   一度呼んでヘッダを作らせ、`+0x04`（base）と `+0x08`（size）に
   `g_GfxAllocator` で確保したバッファを入れる。
2. **記録スロット（vtable `+0x14`）** で `Layout_RecordPaneTree` と同じ手順を踏む。
   `GetProperty(519) → SelectList(自前 id) → Clear → StartSave →
   DrawBegin1 → 自前スプライトを積む → DrawEnd1 → Commit(node+0x104..) → SelectList(save)`
   内容が変わったときだけ記録し直せばよい（`node+0x11D` を自分で管理する）。
3. **再生スロット（vtable `+0x08`）はゲームの `Layout_ReplayRecordedList`（`0x5682DC`）を
   そのまま使う。** `node+0x100`〜`+0x11C` は Commit が埋めるので、
   記録さえすれば毎フレーム再生される。scissor・寸法・display も本物と同じ意味になる。
4. 順序は `LayoutMgr_AddLayout` の優先度 `0xFF` で末尾＝最前面（F-253 / F-254）。

これで gokiro 氏の 3 要素がそのまま揃う。
**描画コマンドを追加するフック**＝記録スロット、
**順番を変えるフック**＝優先度 `0xFF` での登録、
**コマンドバッファ拡張**＝自前 id への base/size 設定。

---

