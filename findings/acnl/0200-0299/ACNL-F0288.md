---
id: ACNL-F0288
aliases:
- F-265
title: 'F-265: ★★★★★UI の投影行列の出所を確定した。**Layout+0x34 の 16 語**であり、記録時ではなく**再生時**に GPU へ流れる — `HIGH`（静的のみ）'
summary: 長年「投影は直前の有効 Layout が Drawer に残した状態へ依存する」（F-233/F-234）
date: '2026-09-01'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5669596
- 4951092
- 5074064
- 5667776
- 4705452
- 1346856
- 1346864
- 5668160
- 5668164
- 8611584
- 8611588
- 8611652
- 8611660
- 8611668
- 8611676
- 8611684
- 8622080
tags:
- layout
supersedes: []
source: v1:RE/FINDINGS.md:15731-15887
by: unknown
original_by: ''
reviewed_by: []
state: superseded
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ACNL-F0696
---
## F-265: ★★★★★UI の投影行列の出所を確定した。**Layout+0x34 の 16 語**であり、記録時ではなく**再生時**に GPU へ流れる — `HIGH`（静的のみ）

長年「投影は直前の有効 Layout が Drawer に残した状態へ依存する」（F-233/F-234）
としていた部分の**実体**が取れた。依存しているのではなく、
**再生するレイアウト自身の `+0x34` が、その場で uniform として送られている。**

### 経路（全て静的・IDA）

```
ssys_ma_lyt_Layout_ReplayRecordedList (0x5682DC)
  if (this+0x108 > 0)
      nwlyt_Drawer_BeginLayoutReplayState(drawer, this+0x30, 0)     ; 0x4B8C34
          cursor = GpuCmd_GetCurrentWritePtr()
          cursor = (*(drawer_vtbl+0x10))(drawer, cursor, 0)
          nwlyt_Drawer_EmitProjectionUniform(drawer, cursor, this+0x34)  ; 0x4D6C90
              Mtx44_Copy16Words(drawer+0x34, this+0x34)   ; 16 語 = 0x40 バイト
              drawer+0x30 = 旧 drawer+0x34 の先頭語
              drawer+0x34 = 0x013F02C1                    ; VSH_FLOATUNIFORM_DATA
              drawer+0x84 = 0
              Mem_Copy(cursor, drawer+0x28, 0x60)         ; 24 語を吐く
      GpuCmd_ReplayRecordedListRange(...)                 ; 記録済みの列を流す
```

吐かれる 24 語の内訳:

| 位置 | 内容 |
|---|---|
| `drawer+0x28` | uniform index の値（`0x80000000` 系。f32 モード・index 0） |
| `drawer+0x2C` | `0x000F02C0` = `VSH_FLOATUNIFORM_CONFIG` |
| `drawer+0x30` | 行列 `m[0]` |
| `drawer+0x34` | `0x013F02C1` = `VSH_FLOATUNIFORM_DATA`, mask `0xF`, extra 19（= 20 語） |
| `drawer+0x38`〜`+0x74` | 行列 `m[1]`〜`m[15]` |
| `drawer+0x78`〜`+0x84` | 残り 4 語（`c4`。`+0x84` は毎回 0） |

### 行列を作る側（`ssys_ma_lyt_Layout_SetupProjectionMatrix` = `0x567BC0`）

Layout vtable `+0x18`。`render.txt` の `m_ProjectionDirty` 経路そのもの。
`sub_73BAC0(&rect, Layout+0x10)` でペインツリーの矩形（`l, t, r, b`）を取り、
row-major の 4x4 直交行列を組む。

```
row0 = [ 2/(r-l),  0,        0,      -(r+l)/(r-l) ]
row1 = [ 0,        2/(t-b),  0,      -(t+b)/(t-b) ]
row2 = [ 0,        0,        0.001,  -0.5         ]
row3 = [ 0,        0,        0,       1.0         ]
```

そのあと `Mtx44_RotateForScreen(m, 1)`（`0x47CCAC`、3DS のフレームバッファ 90 度回転）で

```
row0 <- 旧 row1        row1 <- -旧 row0        row2 / row3 はそのまま
```

最後に `DrawInfo_SetProjectionMatrix(Layout+0x30, m)`（`0x148D28` → `0x148D30`）が
**`Layout+0x34` へ 16 語**を書く。`0x148D28` は `sub_148D30(a1+4, a2)` なので `+0x30+4 = +0x34`。

`0.001f` と `-0.5f` は推定ではなく、`0x567BC0` のリテラルプールの実値
（`0x567D40 = 0x3A83126F`、`0x567D44 = 0xBF000000`）を `find_bytes` で確認した。

### 原点と縮尺

F-208 の実測「原点=画面中央、1 単位 = 1px、下画面 320x240」は、
`l = -W/2, r = W/2, t = H/2, b = -H/2` を意味する。このとき

```
-(r+l)/(r-l) = 0      -(t+b)/(t-b) = 0
```

なので、回転後に非ゼロで残るのは

```
m[1] = 2/H     m[4] = -2/W     m[10] = 0.001     m[11] = -0.5     m[15] = 1.0
```

の 5 つだけ。**実測（F-208）と静的な式が独立に一致した。**
`x = 160` → `-2/320 * 160 = -1.0`（画面端）、`y = 120` → `2/240 * 120 = 1.0`（画面端）。

### ★これが説明すること

「下画面のテキストだけ横幅が 0.8 倍」（利用者報告）は、
**下画面の再生時に投影幅 400 の行列が使われた**場合そのものである
（`320/400 = 0.8`。高さは上下とも 240 なので縦は変わらない）。
F-252 の取り下げた説明とは別物で、今回は
「どの Layout が再生されたかで `+0x34` が変わる」という**特定の機序**が根拠になっている。

### 実装（`cave_node_record.py`、未適用）

登録ケーブで毎フレーム、自前ノードの `+0x34` に 16 語を組み立てる。

```
MOV R2,#0 / STR R2,[R1,#0x34..0x70]     ; 16 語をゼロ埋め
LDR R2,=2/240   ; STR R2,[R1,#0x38]   m[1]
LDR R2,=-2/W    ; STR R2,[R1,#0x44]   m[4]   W = 400（上） / 320（下）
LDR R2,=0.001f  ; STR R2,[R1,#0x5C]   m[10]
LDR R2,=-0.5f   ; STR R2,[R1,#0x60]   m[11]
LDR R2,=1.0f    ; STR R2,[R1,#0x70]   m[15]
```

リテラル: `2/240 = 0x3C088889`、`-2/400 = 0xBBA3D70A`、`-2/320 = 0xBBCCCCCD`、
`0.001f = 0x3A83126F`、`-0.5f = 0xBF000000`、`1.0f = 0x3F800000`。

雛形の 0x50 バイト複製（`+0x28`〜`+0x78`）は行列も上書きするので、
**この書き込みは複製より後**に置いてある。

### 検証（IDA。空き `.text` `0x836700` へ一時的に当てて逆アセンブル、直後に復元）

```
0x836700 MOV R2, #0
0x836704 STR R2, [R1,#0x34]      … +0x38 +0x3C … +0x70 まで 16 本
0x836744 LDR R2, loc_8367B0      -> STR R2, [R1,#0x38]
0x83674c LDR R2, loc_8367B4      -> STR R2, [R1,#0x44]
0x836754 LDR R2, loc_8367B8      -> STR R2, [R1,#0x5C]
0x83675c LDR R2, loc_8367BC      -> STR R2, [R1,#0x60]
0x836764 LDR R2, loc_8367C0      -> STR R2, [R1,#0x70]
```

リテラル 5 本が 4 バイト間隔で連続していることまで一致。
復元後のバイト列は `NCCH/exefs/code_runtime.bin` の同アドレスと**完全一致**した
（これは code.bin.i64 と code_runtime.bin が同一ビルドであることの追加の裏付けでもある）。

### ★監査スクリプトの欠陥を 1 つ潰した

`audit_node_cave.py` はリテラル境界を「末尾から最初に見つかる分岐の次」で**推定**していた。
今回入れた float リテラル `0xBBA3D70A`（`-2/400`）と `0x3A83126F`（`0.001`）は
**B / BL として復号できてしまう**ため、境界が後ろへずれて 40 件の誤検出を出した。

- `Asm.assemble()` が `LIT_BOUNDARY[(base, 語列)]` に**実際の境界**を残すようにした
- 監査はまずこの正解表を引き、無ければ推定に落ちて「[注意]」を出す
- 監査ループはリテラル領域の語を**命令として復号しない**

**推定でごまかしていた安全網は、いつか本物の異常を見逃す。**
生成器が知っている事実は生成器から受け取ること。

### ケーブ配置（F-265 時点）

```
CAVE_Q=0x838200(382) CAVE_P=0x838800(35)  CAVE_V=0x838890(44)
CAVE_A1=0x838940(125) CAVE_A2=0x838B40(120) CAVE_N=0x838D20(11)
CAVE_M=0x838D50(7)   CAVE_B=0x838D70(12)  CAVE_U=0x838DA0(12)
CAVE_F=0x838DD0(10)  CAVE_T=0x838E00(2)    末尾 0x838E10 / 上限 0x839000（余り 496 バイト）
```

監査: 総異常 0 件・重なりなし。**未適用。実機へは入れていない。**

### IDA へ入れた名前

| address | 名前 |
|---|---|
| `0x567BC0` | `ssys_ma_lyt_Layout_SetupProjectionMatrix` |
| `0x4D6C90` | `nwlyt_Drawer_EmitProjectionUniform` |
| `0x4B8C34` | `nwlyt_Drawer_BeginLayoutReplayState` |
| `0x148D28` | `DrawInfo_SetProjectionMatrix` |
| `0x148D30` | `Mtx44_Copy16Words` |
| `0x47CCAC` | `Mtx44_RotateForScreen` |

---

