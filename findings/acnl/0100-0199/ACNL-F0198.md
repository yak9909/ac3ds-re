---
id: ACNL-F0198
aliases:
- F-172
title: 'F-172: ★★★TextBox に依らない発行点を特定。答えは自分の記録の中にあった — `HIGH`（静的＋実機で前提を確認）'
summary: 「UI が何も出ていない状態では、CTRPF を含めどんな方法でも自前 GUI は不可能か」
date: '2026-08-28'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1212596
- 9890452
- 9890456
- 1212620
- 11376988
- 4947404
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:10390-10474
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-172: ★★★TextBox に依らない発行点を特定。答えは自分の記録の中にあった — `HIGH`（静的＋実機で前提を確認）

### 1. 問い

「UI が何も出ていない状態では、CTRPF を含めどんな方法でも自前 GUI は不可能か」

**否。** F-171 が示したのは「TextBox に相乗りする方式に穴がある」ことだけで、
「描画できない」ではない。

同じ計測から重要な事実が出ている:
**`Render_FrameEnd` は 25 秒で 748 回、つまり毎フレーム呼ばれている。**
UI が無くてもゲームは毎フレーム描画しており、**コマンドストリームは常に組まれている。**
足りなかったのは「その瞬間の書き込み位置」という解析上の 1 点だけだった。

### 2. ★答えは F-95 / F-96 / F-99 に既にあった

```c
GpuCmd_Advance(bytes) { g_GpuCmdPtr += bytes; return g_GpuCmdPtr; }   // 0x1280B4
```

**`g_GpuCmdPtr`(`0x0096EA94`) はグローバルの書き込み位置。**
`g_GpuCmdEnd`(`0x0096EA98`) が上限。

`GpuCmd_SplitAndSubmit`(`0x1280CC`) の IDB コメント（F-96/F-99）には
**「自前のコマンドを割り込むならこれより前に積むこと」**と既に書いてあった。

**教訓: 別の課題を追う前に、自分の過去の記録を索引として引くこと。**
TODO-115 は「未解決」として何セッションも残っていたが、
必要な事実は F-95 の時点で手元にあった。

### 3. 実機で確認した前提（この boot）

| | 値 |
|---|---|
| `g_GpuCmdPtr` | `0x322B5180`（物理 `0x222B5180`。linear の窓の中） |
| `g_GpuCmdEnd` | `0x3239D0C0` |
| **空き** | **950,080 バイト** |
| `g_GpuCmdListMgr`(`0xAD995C`) | `0x3229D06C` |
| リスト先頭 `mgr[1]` | `0x3229D0C0` |
| 現在長 `mgr[3]` / 提出済み `mgr[5]` | `0x180C0` / `0x180C0` |
| GX キュー件数 `mgr[8]` | 12 |

**TextBox と一切関係がない。** 空きも 1MB 近くある。

### 4. 発行の手順（設計）

`GpuCmd_SplitAndSubmit`(`0x1280CC`) の**入口**にフックを置き:

```
p = g_GpuCmdPtr
（p から自前のコマンドを書く）
g_GpuCmdPtr = p + n
（元の PUSH を実行して SplitAndSubmit へ戻る）
```

`GpuCmd_SplitAndSubmit` は毎フレーム 8 回程度呼ばれる（CLAUDE.md の既知情報）ので、
**UI の有無に関わらず必ず通る。**

境界検査（`g_GpuCmdPtr < g_GpuCmdEnd`）は本体側にあるので、
自前で積むときも同じ検査を入れること。

### 5. 残っている作業

**何を積むか。** 完結した 1 枚の描画に必要なコマンド列が要る。
既知のものを流用するのが早い:

```
[R9-64, R0)  = 16 ワードの状態プリフィックス
             + 0x60 バイトの TextBatch ヘッダ
             + batch 本体
```

これは `0x4B7DCC` の時点で読める（F-158 / F-168）。
**一度捕獲して自前バッファへ保存し、SplitAndSubmit のフックから毎回書き出す**のが
最小の検証になる。

注意点:

- batch は状態（ブレンド・TexEnv・テクスチャ）を自分で持っているので比較的自己完結だが、
  **ビューポートやシェーダ選択など「フレームに 1 回だけ設定される状態」は
  直前の描画のものを引き継ぐ。** そこが崩れると出ないか化ける
- 積む位置によっては、直後の `SplitAndSubmit` の終端列との順序に注意

---

