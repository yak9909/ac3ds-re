---
id: ACNL-F0142
aliases:
- F-104
title: 'F-104: ★single-step 無効なら breakpoint が使える。`GpuCmd_SplitAndSubmit` の呼び出し元を捕捉'
summary: 'confidence: **HIGH**（実機で breakpoint ヒットを観測）'
date: '2026-08-24'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1273820
- 1273224
- 1212620
- 5173588
- 5173584
- 7625888
- 5172696
- 1185468
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:6253-6336
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-104: ★single-step 無効なら breakpoint が使える。`GpuCmd_SplitAndSubmit` の呼び出し元を捕捉

confidence: **HIGH**（実機で breakpoint ヒットを観測）

### 1. ★CLAUDE.md の breakpoint 記述を実測に合わせて訂正した

旧記述「高頻度実行箇所に breakpoint を置くとゲームがフリーズする」は**誤り**。

**★本項の当初の解釈も誤っていた。**
「single-step 無効だから高頻度でもフリーズしなかった」と書いたが、
ユーザーの実機検証によれば **フリーズの原因は頻度ではなく
「ヒットした bp を削除せずに再開すること」**。
今回フリーズしなかったのは、毎回 CLAUDE.md 通り
**削除してから再開していたから**であって、single-step の設定は関係ない。

ユーザーが実機で確認した正しいモデル（CLAUDE.md に反映済み）:

- ヒットした bp を**削除せずに再開するとフリーズする**。これが唯一の条件
- **頻度は関係ない**
- **フリーズしても復帰できる**。Suspend して bp を削除し再開すれば普通に動く
- **削除して即座に置き直すだけでは恐らく意味がない。**
  効くのは「削除 → 再開 → Suspend → 再設置」の順
- `Use stepping support` を切れば削除不要になる可能性がある（**未検証**）

実測:

| 対象 | 頻度 | 結果 |
|---|---|---|
| `GX_SetTextureCopyImpl`(`0x136FDC`) / `GX_RequestDmaImpl`(`0x136D88`) | 低（1 フレームのキューに出ない） | 設置して継続しても**フリーズせず**、未ヒットのまま正常動作 |
| `GpuCmd_SplitAndSubmit`(`0x1280CC`) | 高（毎フレーム 8 回 ≈ 秒 480 回） | **設置してすぐヒット。フリーズなし** |

**`BPT_SOFT`（`type=4`）で設置。`BPT_EXEC` は CLAUDE.md 通り使わない。**
「設置 → 停止 → 観測 → 削除 → 再開」のサイクルは引き続き守った。

**★注意**: 走行中は MCP がブロックしてタイムアウトするので、
「タイムアウト＝フリーズ」ではない。手動 Suspend で切り分ける。

### 2. ★捕捉した呼び出し元

```
PC = 0x001280CC（GpuCmd_SplitAndSubmit 入口）
LR = 0x004EF154  -> BL は 0x4EF150
R0=0 R1=0x00745CA0 R2=0xFFFFFFFF R3=0x303814C8
```

**呼び出し元は `sub_4EEDD8`(`0x4EEDD8`, size `0x48C`)。**
`xrefs_to` では `limit` で打ち切られて見えていなかった呼び出し元。

### 3. ★別コマンドリストへ切り替えて描画するパス

`sub_4EEDD8` は `a1 == 1024` のときだけ以下をやる:

```c
GpuCmd_GetProperty(519, &saved);                 // 現在のリスト id を退避（519 = mgr[0]）
GpuCmd_SelectList(dword_94CA74[dword_94CA54]);   // 別のリストへ切り替え
... シーンのオブジェクトを sub_4A41EC で集める ...
sub_4EB840(v4, dword_94CA58);                    // 描画本体
GpuCmd_SplitAndSubmit();                         // ★0x4EF150
sub_7B0694(...);
GpuCmd_SelectList(saved);                        // 元の id へ復帰
```

**この「退避 → 切り替え → 構築 → 提出 → 復帰」が
自前描画を割り込ませるときの手本になる。**

### 4. 新規に特定した API

**`GpuCmd_SelectList(id)`(`0x1216BC`)** — アクティブなコマンドリストを id で選ぶ。
id は `mgr[0]`（実機実測で 1 か 2、F-102）。
`GpuCmd_GetProperty(519, &id)` で現在値が取れる。
sead 初期化（`sead_GfxMemoryMgr_InitBuffers`）でもバッファ毎に呼ばれる。

`1024` / `1025` / `1040` は sead 初期化 `sub_11EAFC` で使われる
バッファ / ターゲット ID と同じ値。

### 5. 手法上の教訓

**メモリ読みでは「誰が呼んだか」は取れない。**
GX キューの直接読み（F-103）は「何が積まれたか」には最適だったが、
呼び出し元の特定には breakpoint が必要だった。
**両者は補完関係にある。**

---

