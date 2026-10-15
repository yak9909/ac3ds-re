---
id: ACNL-F0154
aliases:
- F-116
title: 'F-116: ★★TODO-75 第1段達成 — シーンへノードを追加できた。あわせて Suspend の条件を確定'
summary: 'confidence: **HIGH**（実機。対照実験つき）'
date: '2026-08-24'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 2686476
- 1798884
- 5166640
- 5520492
- 1273956
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:7439-7558
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-116: ★★TODO-75 第1段達成 — シーンへノードを追加できた。あわせて Suspend の条件を確定

confidence: **HIGH**（実機。対照実験つき）

### 1. ★成果 — 任意のシーンへノードを 1 個追加できた

`PATCHES/cave_scene_node_dup.py` を作成。`BsShadowViewMgr_SubmitToScene`(`0x28FE0C`)
の先頭 1 ワードを `B ケーブ` に差し替え、ケーブで `Scene_SubmitNode` を 2 回呼ぶ。

```asm
PUSH {R4,LR}
MOV  R4, R0
LDR  R1, [R4,#0xC8]      ; 本来の sceneIndex
ADD  R0, R4, #0xA8       ; holder
BL   Scene_SubmitNode    ; 1 回目（本来の動作）
MOV  R1, #1              ; ★sceneIndex 1（描画されないシーン）
ADD  R0, R4, #0xA8
BL   Scene_SubmitNode    ; 2 回目（追加分）
MOV  R0, #2
POP  {R4,PC}
```

**実機での観測:**

| 観測点 | 結果 |
|---|---|
| ケーブ内 2 回目直前 (`0x01E81514`) | `R4 = 0x3309C334` 保持、`ctx[2] n=1` |
| ケーブ内 2 回目直後 (`0x01E81520`) | **`ctx[1] n=1`、中身 `0x30896104`** |
| パッチ適用後のフル 1 フレーム (`0x1B72E4` 入口) | `ctx[0] n=24` / **`ctx[1] n=1`** / `ctx[2] n=1` |

**F-111 / F-112 の「`Scene_SubmitNode` を毎フレーム呼べば描画対象を増やせる」が
実際のコード注入で成立した。** `sceneIndex` はこちらで自由に選べる。

`ctx[1]` は `byte_94CA2C = 0` のため描画されないので、
**GPU に一切触れずにノード追加だけを検証できた**（段階を分ける設計が効いた）。

### 2. ケーブ領域 `0x01E81500` は実行可能だった

「CTRPF の空ページが今回の起動で実行可能か未確認」と疑ったが、
**対照実験（submit 1 回だけのケーブ）が正常動作したので実行可能**と確定。
最初のフリーズをケーブのせいにしたのは誤りだった。

### 3. ★★Suspend の条件が確定した（CLAUDE.md 全面改訂）

ユーザーの指摘を受けて資料を読み直し、実機で 4 通り試した。

| 試したこと | 結果 |
|---|---|
| `suspend_process()` 単独（対象は**正常走行中**） | タイムアウト |
| `request_suspend_process()` + `run_requests()` 単独 | タイムアウト |
| 直後の `get_process_state()` プローブ | タイムアウト |
| **`server_health`**（デバッガに触らない疎通確認のみ） | **タイムアウト** |

**最後の行が決定的。** デバッガと無関係な疎通確認すら通らないので、
「suspend の呼び方の問題」ではなく **プラグインのハンドラごと待たされている**。

**正しい理解:**

- 要求は**キューに積まれ、対象が停止した時点で処理される**
- 対象が 30 秒以内に停止しなければ MCP プロキシのタイムアウトに当たる
- したがって **走り出したあとに外から止める手段は無い**

F-105 の「py_eval から Suspend できる」は**正しい**。ただし成功例はすべて
**停止中に始まった呼び出しの中で `continue` → `suspend` と束ねた**ものだった。
F-105 の運用欄に書いた「手動 Suspend 依頼が不要になった」がこの区別を潰していた。

### 4. ★解決策 — `run_timed.py`（走らせる前に止まる予約を入れる）

`ida_kernwin.register_timer` のコールバックは **IDA のイベントループ上**で走るので、
こちらのハンドラの外側で `suspend_process()` を呼べる。

```python
register_timer(RUN_MS, cb)   # 予約（cb は suspend して -1 を返す）
continue_process()           # 走り出す
```

**実機で検証:**

| 検証 | 結果 |
|---|---|
| 1500ms 走らせる（bp なし） | `state=-1` で戻る。`g_GpuCmdPtr` が `0x322B95C0` → `0x322B8D60` と変化 = **実際に走った** |
| bp `0x4ED630`（毎フレーム 40 回超）＋ 1500ms | **bp がヒット**して停止（`PC=0x4ED630`） |
| bp `0x1B72E4`（毎フレーム 1 回）＋ 1500ms | **未ヒットのまま時間切れ停止** = 待ちぼうけにならない |
| bp `0x1B72E4` ＋ 5000ms | **ヒット**（`PC=0x1B72E4`, `LR=0x543C6C`） |

**bp が先にヒットすればそこで、しなければ時間切れで必ず停止する。**
これで手動 Suspend 依頼は原則不要になった。

**注意: `RUN_MS` は MCP プロキシの 30 秒タイムアウトより十分短くする。**
次の呼び出しは「対象が止まるまで待ってから」処理されるため。

### 5. ★踏んだ誤り（同じ種類を 2 回）

**タイムアウトを「フリーズ」と読んだ誤りを 2 回**やった。

1. `DUP=True` のとき → 手動 Suspend 後の `PC` は `0x137064`(GSP 待ち)、bp 未ヒット。
   **これは本物のハングの可能性が高い**（未確定）
2. `DUP="scene1"` のとき → 手動 Suspend 後の `PC` は **`0x001B72E4` = bp の位置**。
   **ゲームは正常に bp で止まっていただけ**。パッチのせいにしたのは完全な誤り

さらに `ctx[1] n=0` を「2 回目の submit が効いていない」と読んだが、
**パッチ投入時にプロセスがフレーム途中（`BaseObj_RunDrawPhase` 実行中）で止まっており、
影の submit がパッチ適用前に済んでいた移行フレーム**を見ていただけだった。

**教訓: タイムアウトからは何も分からない。`PC` を見るまで断定しない。**
`PC` が bp の位置なら正常停止、まったく別の場所なら本当のフリーズ。

### 6. 未解決

**`DUP = True`（同じシーンへ 2 回 submit＝描画コールバックが 2 回走る）は
ハングの疑いが濃厚だが 1 回の観測しかない。**
`run_timed.py` を使えば安全に再検証できる（TODO-79）。

### 7. 現在の状態

パッチは **uninstall 済み**（フック `0xE92D4010` 復元、ケーブ全ゼロ、bp 0 件）。
`PATCHES/cave_scene_node_dup.py` の `MODE` と `DUP` を変えれば再現できる。

---

