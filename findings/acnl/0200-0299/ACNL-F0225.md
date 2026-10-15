---
id: ACNL-F0225
aliases:
- F-200
title: 'F-200: ★★★★★UI は「1 本のコマンド列」ではない。記録と再生に分かれている — 静的解析'
summary: '> **2026-09-01 訂正（F-233）:** 記録／再生の構造は維持するが、下の'
date: '2026-09-01'
category: render
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 5670612
- 11412980
- 5669596
- 8063528
- 5908424
- 5908628
- 1212596
- 5075316
- 7589772
- 5075440
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:12215-12336
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0258"]
---
## F-200: ★★★★★UI は「1 本のコマンド列」ではない。記録と再生に分かれている — 静的解析

> **2026-09-01 訂正（F-233）:** 記録／再生の構造は維持するが、下の
> `sub_5A27C8/sub_5A2894 → SplitAndSubmit` という解釈は誤り。
> 両関数は guard 付きで通常は早期 return する。末尾の注入位置候補ではあるが、
> 通常 submit 点でも「安全で確実」な提出点でもない。

**TODO-131 のための静的解析。これまでの「フラッシュの回数で描画順が決まる」という
モデルは根本から誤りだった。**

### 1. レイアウトはそれぞれ専用のリストへ「記録」される

`ssys_ma_lyt_Layout_RecordPaneTree`（`0x5686D4`）:

```c
GpuCmd_GetProperty(519, &save);          // 現在のリスト ID を退避
GpuCmd_SelectList(*(layout + 256));      // ★このレイアウト専用のリストへ切替
nwlyt_DrawPaneTreeToCurrentList(...);    // そこへ記録
GpuCmd_CommitListAndCaptureDelta(layout+260 .. +272);   // 開始/長さを記録
GpuCmd_SelectList(save);                 // 元へ戻す
```

**★F-197 の「`g_GpuCmdPtr` が `0x00AE25F4` と `0x32...` を行き来する」の正体はこれ。**
「別リストのポインタが混ざっていた」のではなく、**リストが切り替わっていた**。

### 2. 記録済みリストは後から「再生」される

`ssys_ma_lyt_Layout_ReplayRecordedList`（`0x5682DC`）→
`GpuCmd_ReplayRecordedListRange`（`0x7B0A28`）。

再生は **GX キューのエントリ（28 バイト）をメインリストに積み、
`g_GpuCmdPtr` を記録長ぶん進める**（＝場所を予約する）。

**したがって描画順は「記録した順」ではなく「再生した順」で決まる。**

### 3. ★フレームの描画順（`Frame_DrawPass1024` / `1040`）

```
Frame_DrawPass1024():             ← 記録＋再生
    BaseObj_RunDrawPhase()
    Render_DrawScene2()           シーン2（無条件）
    Render_DrawScene0(1024)       シーン0
    Render_DrawScene1(1024)       シーン1
    sub_5A27C8()                  ★描画の最後 → SplitAndSubmit

Frame_DrawPass1040():             ← 再生のみ
    Render_DrawScene0(1040)
    Render_DrawScene1(1040)
    sub_5A2894()                  ★描画の最後 → SplitAndSubmit
    Render_FrameEnd()
```

`Render_DrawSceneIndexed` の `if (a1 == 1024)` が記録ブロックを囲っており、
**`GpuCmd_ReplayRecordedListRange` はその外**にある。だから 1040 のパスは再生だけ。

### 4. ★★最良の相乗り点 — `sub_5A27C8` / `sub_5A2894`

| 関数 | xref | 位置 |
|---|---|---|
| `sub_5A27C8`（`0x5A27C8`） | **1 件のみ** | `Frame_DrawPass1024` の描画の最後 |
| `sub_5A2894`（`0x5A2894`） | **1 件のみ** | `Frame_DrawPass1040` の描画の最後 |

**フレームに 1 回ずつ、全シーンの再生が終わったあと、メインリスト上で呼ばれる。**
`GpuCmd_SplitAndSubmit`（28 か所から呼ばれる）より圧倒的に安全で確実。

### 5. ★`sub_5A2894` はコマンド追記の「正規の手順」を見せている

```c
GpuCmd_GetProperty(520, &ptr);      // 現在の書き込み位置（プロパティ 520）
save = ptr;
... ptr へ書く ...
GpuCmd_Advance((ptr - save) & ~3);  // カーソルを進める
GpuCmd_SplitAndSubmit();
```

### 6. ★★仮説の反証 — `GpuCmd_Advance` は特別なことをしていない

「正規 API を通さなかったから GPU が固まった」という仮説を立てたが、
`GpuCmd_Advance`（`0x1280B4`）の実体は

```c
g_GpuCmdPtr += bytes;  return g_GpuCmdPtr;
```

**だけ。私の直接書き込みと等価であり、この仮説は誤り。**
F-197 / 今回のハングの原因は依然として未特定。

### 7. `g_GpuCmdPtr` はレイアウトの境目では有効

`nwlyt_DrawPaneTreeToCurrentList`（`0x4D7174`）:

```c
v8 = GpuCmd_GetCurrentWritePtr();       // g_GpuCmdPtr から読む
v8 = nwlyt_Pane_DrawRecursive(pane, v8, ...);
g_GpuCmdPtr = v8;                       // ★書き戻す
```

**IDB の `TextBox_UpdateDrawState` のコメント「cursor をグローバルに書き戻していない」は
内側の関数の話で、レイアウトの境目では成立していない。** 古いコメントを鵜呑みにしない。

### 8. 動的観測との突き合わせ

| 実測 | 静的解析での説明 |
|---|---|
| 最後のフラッシュの呼び出し元が `0x73CF8C` / `0x4D71F0` の 2 種類 | どちらも**レイアウト描画の内部**。フレーム末尾ではない |
| フラッシュ回数が 1〜42 と振れる | レイアウト数・マテリアル数が場面で変わる |
| `g_GpuCmdPtr` が別領域を指すことがある | `GpuCmd_SelectList` によるリスト切替 |

**3 点とも静的な構造で説明できる。** 逆に「フラッシュの回数で描画順が決まる」は
どの静的証拠とも整合しない。

### 9. まだ確定していないこと（**推測として明示**）

- **1024 / 1040 のパスが上画面 / 下画面のどちらに対応するか。** 未確認
- 両パスが同じ記録済みリストを再生するのに、なぜ別々の画面になるのか
- **GPU ハングの真因。** `GpuCmd_SplitAndSubmit` の入口から
  `DrawCtx_FlushBatch` を呼んだことが原因と**推測**しているが、証拠はない
- `sub_5A27C8` / `sub_5A2894` の時点で、どの画面のフレームバッファが
  束縛されているか

---

