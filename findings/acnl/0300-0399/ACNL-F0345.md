---
id: ACNL-F0345
aliases:
- F-318
title: 'F-318: F-317 の削除を実装。実機で **132,192 B が丸ごと戻った** — HIGH'
summary: '```'
date: '2026-09-06'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8388608
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:21078-21147
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0346"]
---
## F-318: F-317 の削除を実装。実機で **132,192 B が丸ごと戻った** — HIGH

### 削除ケーブ（43 語。`PATCHES/free_cmdlists.py`）

```
PUSH {R0-R3,R12,LR}
LDR R0,=519 / LDR R1,=SCRATCH / BL GpuCmd_GetProperty   ; いま束縛されている id
上ノード:
  LDR R12,=&node+0x100 / LDR R0,[R12] / CMP R0,#0 / BEQ 次
  LDR R1,=SCRATCH / LDR R1,[R1] / CMP R0,R1 / BEQ 次     ; ★束縛中なら消さない
  MOV R0,#1 / MOV R1,R12 / BL sub_127D98                 ; nngxDeleteCmdlists(1,&id)
  LDR R12,=&node+0x100 / MOV R0,#0 / STR R0,[R12]        ; 二重削除を防ぐ
下ノード: 同じ
LDR R12,=DONE / MOV R0,#1 / STR R0,[R12]                 ; 完了印
POP / 元命令 / B Render_FrameEnd+4
```

`0x00838100`〜`0x008381AC`（`CAVE_LIMIT 0x838200` 内）。

### 実機の結果

```
組み込み後: list id 上=46 下=47   nngx 空き 823,608
A1/A2 のフックを外す
削除ケーブを 3 秒:
  完了印 = 1 / list id 上=0 下=0
  nngx 空き 823,608 -> 955,800   ★+132,192 B（空きブロックは 1 個のまま）
  g_GpuCmdPtr = 0x323BAC40 / g_GpuCmdEnd = 0x324B2130 / g_GpuCmdListMgr = 0x323B20D0
    → 全部非 0。**束縛中を避ける守りが効いている**
```

### ★仕様書 §5.3 の順序を訂正した

F-317 で書いた順序は**誤り**だった。フックが生きたまま削除すると、
次のフレームで A1/A2 が `node+0x100 == 0` を見て**また作り直す**。

```
1. detach → 記録長が 0 になるのを待つ
2. ★A1/A2 のフックを素へ戻す      ← 先に外す
3. 100ms 待つ
4. ★コマンドリストを削除          ← .bss を消す前
5. nw::lyt の借用を Free
6. .bss とケーブをゼロ埋め
```

### ★監査そのものが壊れていた（見つけて直した）

削除ケーブの事前監査が **LDR を 1 件も検査せずに「異常 0 件」と出していた。**

```
マスク 0x0F7F0000 は U ビット(0x00800000)を落とすので
期待値は 0x051F0000。0x059F0000 と書いていた。
```

**「異常 0 件」は「検査した結果 0 件」とは限らない。**
検査した件数を必ず出すようにした（いまは `LDR 9 件 / 分岐 8 件 を検査した` と出る）。
直した後の監査と objdump の逆アセンブルは一致している。

### プラグインへの実装

| | |
|---|---|
| `PATCHES/export_gui_v2.py` | 削除ケーブ 43 語を `GuiCavesV2.h` へ（`kDelCave` / `kDelDoneFlag`） |
| `Sources/OwnGui.cpp` | `DeleteCmdLists()` を追加し、`Disable()` の順序を上記へ |
| `verify_plugin_port_v2.py` | 群 1 に `kDelCave` の照合、群 8 に **`Disable()` の順序検査**を追加 |

`gohan.3gx` 再ビルド済み。照合 3 本とも 0 件。**プラグイン側は実機未検証。**

---

