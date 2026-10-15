---
id: ACNL-F0294
aliases:
- F-271
title: 'F-271: ★★★★★`TextBox_UpdateDrawState`(`0x4B7DEC`) が「テクスチャ付き描画へ切り替える」全手順。実測列の全項目がこれで説明できた — `HIGH`（静的 + F-124 の実測列）'
summary: F-270 で reg `0x080` の穴を見つけたので、**同じ穴が他にもないか**を
date: '2026-09-01'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4947436
- 2097280
- 4194368
- 8612256
- 8613128
- 8613180
- 8622080
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:16363-16459
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-271: ★★★★★`TextBox_UpdateDrawState`(`0x4B7DEC`) が「テクスチャ付き描画へ切り替える」全手順。実測列の全項目がこれで説明できた — `HIGH`（静的 + F-124 の実測列）

F-270 で reg `0x080` の穴を見つけたので、**同じ穴が他にもないか**を
「ゲームがペイン 1 枚を描くときのコマンド列」と突き合わせて確認した。
基準表は F-124 で実機から捕獲したグリフ 1 枚ぶんの 86 ワード。

### `TextBox_UpdateDrawState` が出す並び（静的）

`v10 = *(mat+0x30) & 3` = 使うテクスチャユニット数、
`v7` = 使うユニットのビットマスク（1 個なら `1`）。

```c
if (フラッシュが要る) {
    *v17 = 0;  v17[1] = 2097280;    // 0x00200080  reg 0x080 mask 2 = 0
    v17[2] = 0; v17[3] = 0;         // ヘッダ 0 = 詰め物
}
if (バッチが空) {
    *a2 = v7 << 8;  *v19 = 131183;  // 0x0002006F  reg 0x06F mask 2 = 0x00000100
    次の 2 語 = (v7 | 0x11000, 721024);  // 0x000B0080  reg 0x080 mask 0xB = 0x00011001
}
if (…) 次の 2 語 = (v7 | 0x11000, 262272);  // 0x00040080  reg 0x080 mask 0x4 = 0x00011001
if (テクスチャが変わった) Mem_Copy(a2, unk_97B74C, 32 * v10);  // ユニットごと 32 バイト
```

`unk_97B74C` はユニットごと 32 バイトのテクスチャ状態キャッシュで、
中身は `0x082` / `0x083` / `0x085` / `0x08E` の 4 対（F-1xx で確認済み）。

### F-124 の実測列との突き合わせ（全項目）

| 実測列の項目 | 我々の側での出所 | 状態 |
|---|---|---|
| `reg 0x2B1 = 1` | `DrawCtx_FlushBatch` が `drawctx+1692` から出す。ケーブが 1 を入れる | OK |
| `reg 0x111` / `0x100` / `0x101` / `0x104` | Drawer の既定ブロック（F-268） | OK |
| `reg 0x0F8` TexEnv5 ほか TEV | **自前 36 語**（F-269） | OK |
| **`reg 0x06F` mask 2 = `0x00000100`** | **どこからも出していなかった** | **★F-271 で追加** |
| **`reg 0x080` mask B / mask 4 = `0x00011001`** | **どこからも出していなかった** | **★F-270 で追加** |
| `reg 0x08E` / `0x085` / `0x082` / `0x083` | 自前 4 対（F-191） | OK |
| `reg 0x2C0` / `0x2C1`（uniform 6 / 0x40） | `DrawCtx_FlushBatch`（F-268） | OK |
| `reg 0x227` / `0x228` / `0x253` / `0x245` | `DrawCtx_FlushBatch`（F-268） | OK |

**これで実測列の全項目に出所がついた。未説明のコマンドは残っていない。**

### `reg 0x06F` を落としてはいけない理由

`sub_4D72C4`（DrawBegin1 の中）は `reg 0x06F` を **mask 2 = 0** で書く。
`0x06F` = `SH_OUTATTR_MODE` で、bit8 以降が「どのユニットへテクスチャ座標を出すか」。
0 にされると**シェーダがテクスチャ座標を出力しなくなる**。

自前記録は `DrawBegin1` の直後から始まるので、立て直さないと
自前アトラスが正しい UV でサンプルされない。

### マスクをゲームと揃えた

- `reg 0x06F` は **mask 2**（バイト 1 だけ）。`mask 0xF` で書くと
  Drawer の既定ブロックが入れた他のバイトを 0 で潰してしまう。
- `reg 0x080` は **mask 0xB と mask 0x4 の 2 回**。合わせて 4 バイト全部になるが、
  ゲームがこの形で出しているので合わせる。

### 実装と検証

`build_q` のテクスチャ列は (値, レジスタ, マスク) の三つ組 7 件 = 14 語になった。

**独立その 1**（生成語から LDR のリテラルを復号）

```
reg 0x06F mask 0x2 = 0x00000100   SH_OUTATTR_MODE
reg 0x080 mask 0xB = 0x00011001   TEXUNIT_CONFIG
reg 0x080 mask 0x4 = 0x00011001   TEXUNIT_CONFIG
reg 0x082 mask 0xF = 0x00400040   TEXUNIT0_DIM     64x64
reg 0x083 mask 0xF = 0x00000000   TEXUNIT0_PARAM   ニアレスト
reg 0x085 mask 0xF = 0x0453B0A0   TEXUNIT0_ADDR1   (0x329D8500-0x10000000)>>3
reg 0x08E mask 0xF = 0x00000009   TEXUNIT0_TYPE    LA4
```

**独立その 2**（IDA。相対位置を保ったまま `0x8369A0` と `0x836D08` へ当てて逆アセンブル）

```
0x8369a0 LDR R1, loc_836D08 / STR R1, [R5],#4
…（全 14 対、リテラルは 0x836D08〜0x836D3C に 4 バイト間隔で連続）
```

直後に元バイトへ復元し `NCCH/exefs/code_runtime.bin` と一致を確認。
監査: 総異常 0 件・重なりなし。`CAVE_Q` は 388 → 400 語。

### ケーブ配置（F-271 時点。現行）

```
CAVE_Q=0x838200(400) CAVE_P=0x838840(35)  CAVE_V=0x8388D0(44)
CAVE_A1=0x838980(87) CAVE_A2=0x838AE0(82) CAVE_N=0x838C30(11)
CAVE_M=0x838C60(7)   CAVE_B=0x838C80(12)  CAVE_U=0x838CB0(12)
CAVE_F=0x838CE0(10)  CAVE_T=0x838D10(2)    末尾 0x838D20 / 上限 0x839000（余り 736 バイト）
```

**未適用。実機へは入れていない。**

---

