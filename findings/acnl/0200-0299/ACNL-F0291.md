---
id: ACNL-F0291
aliases:
- F-268
title: 'F-268: ★★★★★Drawer の既定コマンド列には **TEV 段が 1 つも無い**。色は必ずマテリアル由来 — `HIGH`（静的のみ）'
summary: 「`DrawBegin1` の既定 TEV で LA4 アトラス × 頂点カラーが合成されるか」（F-260 の未検証項目）に
date: '2026-09-01'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4946020
- 9942764
- 9942780
- 9942788
- 9942804
- 9942828
- 9100048
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:16042-16188
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-268: ★★★★★Drawer の既定コマンド列には **TEV 段が 1 つも無い**。色は必ずマテリアル由来 — `HIGH`（静的のみ）

「`DrawBegin1` の既定 TEV で LA4 アトラス × 頂点カラーが合成されるか」（F-260 の未検証項目）に
答えが出た。**合成されない。既定列は TEV 段を一切設定しない。**

### `sub_4D5D1C`（Drawer 既定コマンド列の構築）

`sub_568FDC`（LayoutMgr 初期化）→ `sub_4B77CC` → `sub_4D5D1C` で、
Drawer の 2 本のブロックが作られる。`sub_48A780(a1+4, …)` が begin 側、
`sub_48A780(a1+20, …)` が end 側へ追記する。

> ### ★★★【F-276 による訂正】この節の「記録の先頭で出る」は誤り
>
> 既定ブロックは **記録時ではなく再生時**に出る。
> `sub_4D72C4` は `TST R2,#1 / BNE` で **フラグが立っていたら 1 語も出さない**。
>
> - 記録側 `Layout_RecordPaneTree` は `DrawBegin1(drawer, **1**)` を呼ぶ → **何も出ない**
> - 再生側 `sub_4B8C34(drawer, DrawInfo, **0**)` が `(vtbl+0x10)(drawer, cursor, 0)` を呼ぶ
>   → **ここで既定ブロックが出る**
>
> 詳細は F-276。以下の「begin ブロックの中身」の一覧そのものは正しい。

**begin ブロック（Drawer+0x04 / 長さ +0x08）の中身**

| 順 | 内容 |
|---|---|
| 1 | `unk_8ADC20` 320 バイト（reg `0x251` / `0x200` ×2 / `0x229` / `0x244` の全ゼロ初期化） |
| 2 | 頂点シェーダ本体（reg `0x2CB` CONFIG + `0x2CC` DATA を 128 語ずつバースト） |
| 3 | `unk_8ADA08` = reg `0x2BF` (`VSH_CODETRANSFER_END`) = 1 |
| 4 | オペランド記述子（reg `0x2D5` + `0x2D6`） |
| 5 | 出力マップ（20 バイト/件のテーブルから 24 バイトのコマンドへ） |
| 6 | 属性バッファのアドレス（`sub_143B54()` の戻り値を 16 で丸めたもの。`a1+1664` に控える） |
| 7 | `unk_8ADDF8` 148 バイト |
| 8 | bool uniform / エントリポイント / 属性数などの構成 |
| 9 | reg `0x064` / `0x06F`（attribute permutation） |
| 10 | **`unk_8ADB10` 144 バイト** |

**`unk_8ADB10` の全 18 コマンド**（`scratchpad/pica_decode.py` で解読）

```
reg 0x111 = 00000001     reg 0x110 = 00000001
reg 0x100 = 00E40100     reg 0x101 = 76760000   ← 標準アルファブレンド
reg 0x104 = 00000061     reg 0x0E0 = 00000000
reg 0x08F = 00000000     reg 0x1C6 = 00000001
reg 0x112 = 0000000F     reg 0x084 = 00000000
reg 0x094 = 00000000     reg 0x09C = 00000000
reg 0x08B = 00000001     reg 0x22A = 00000000
reg 0x229 (mask 2) = 0   reg 0x253 (mask 3) = 0
reg 0x25E (mask 2) = 0   reg 0x25F = 00000001
```

**TEV 段（`0x0C0`-`0x0FE`）は `0x0E0` の 1 件だけで、値は 0。
テクスチャの結び付き（`0x082` / `0x085` / `0x08E`）も無い。**

end ブロック（`unk_8ADBA0` 40 バイト）は
reg `0x232` の固定属性バースト（`0`, `0.5f`, `0`, `0`）と reg `0x111` / `0x110` だけ。

### uniform の割り当てが確定した

`sub_4D5D1C` の末尾が Drawer のヘッダ語を直に書いている。

```c
*(_QWORD *)(a1 +   40) = 0xF02C080000000LL;   // +0x28 = 0x80000000, +0x2C = 0x000F02C0
*(_QWORD *)(a1 +  136) = 0xF02C080000006LL;   // +0x88 = 0x80000006
*(_QWORD *)(a1 +  568) = 0xF02C080000020LL;   // +0x238 = 0x80000020
*(_QWORD *)(a1 + 1096) = 0xF02C080000040LL;   // +0x448 = 0x80000040
```

| uniform index | 用途 | 誰が流すか |
|---|---|---|
| `0`〜`4` | **投影行列 16 語 + c4** | `nwlyt_Drawer_EmitProjectionUniform`（F-265） |
| `6`〜 | 行列・色・幾何（1 スプライト 6 語） | `DrawCtx_FlushBatch`（`a1+136` の staging） |
| `0x20` | テキスト用 | `sub_4D6CE0`（`a1+632`） |
| `0x40` | 第 3 の配列 | `a1+1096` |

**F-265 で「`drawer+0x28` は `0x80000000` 系、`+0x2C` は `0x000F02C0`」と推定した部分が、
まったく独立に、初期化側の即値として確認できた。** F-260 の未検証項目 1 も解消。

### マテリアルが出す TEV（`Material_EmitState` = `0x4B7864`）

`*(mat+0x30) & 3` でモードが決まり、**そのモードのテンプレート列を丸ごとコピーする**。
テンプレートはグローバルにあり、色の入る「穴」だけを直前に書き換える。

**モード 0**（`0x97B6EC` から 6 語、色の穴は `0x97B6FC` ← `*(mat+0x14)`）

```
reg 0x0F8 バースト(consecutive, 5 語) = TexEnv5
  SOURCE  = 0x0EE00EE0   rgb/alpha とも src0=PRIMARY(0), src1=CONSTANT(E), src2=CONSTANT(E)
  OPERAND = 0x00000000
  COMBINE = 0x00010001   rgb=MODULATE, alpha=MODULATE
  COLOR   = ★穴（定数色）
  SCALE   = 0x00000000
→ 頂点カラー × 定数色
```

**モード 1**（`0x97B704` から 18 語、穴は `0x97B714` ← `*(mat+0x10)` と `0x97B72C` ← `*(mat+0x14)`）

```
reg 0x0D8 バースト = TexEnv3
  SOURCE  = 0x0E3E0E3E   src0=CONSTANT, src1=TEXTURE0, src2=CONSTANT
  OPERAND = 0x00010010   op1 = ONE_MINUS_SRC（rgb・alpha とも）
  COMBINE = 0x00010001   MODULATE
  COLOR   = ★穴1        SCALE = 0
reg 0x0F0 バースト = TexEnv4
  SOURCE  = 0x0F3E0F3E   src0=PREVIOUS, src1=TEXTURE0, src2=CONSTANT
  OPERAND = 0x00000000
  COMBINE = 0x00080008   MULTIPLY_ADD（src0*src1 + src2）
  COLOR   = ★穴2        SCALE = 0
reg 0x0F8 バースト = TexEnv5
  SOURCE  = 0x0FF00FF0   src0=PRIMARY, src1=PREVIOUS, src2=PREVIOUS
  COMBINE = 0x00010001   MODULATE
  COLOR   = 0            SCALE = 0
→ 2 色グラデーションのテキスト。最後に必ず **頂点カラーを掛ける**
```

**★両モードとも最終段（TexEnv5）が `PRIMARY_COLOR`（頂点カラー）を掛ける。**
これが「自前スプライトの色を頂点カラーで決められた」理由（F-187〜F-190）。

`Material_EmitState` が出す他のレジスタも、既定ブロックと**同じ値**だった。

```
reg 0x111 = 1          (983313 = 0x000F0111)
reg 0x100 = 0x00E40100 (983296 = 0x000F0100)
reg 0x101 = 0x76760000 (983297 = 0x000F0101)
reg 0x104 = 0x61       (983300 = 0x000F0104)
```

**独立した 2 つの経路（`sub_4D5D1C` の `unk_8ADB10` と `Material_EmitState` の即値）が
同じ値に一致した。** ブレンドと色演算の解釈はこれで裏が取れた。

### 結論 — マテリアルは今も必要で、**設計に残る最後の借り物**

- 既定列は TEV 段を作らないので、我々が何も出さなければ
  **直前の描画が残した TEV がそのまま効く**。投影と同じ不定性である。
- 現行実装はテクスチャユニット 0 の結び付き（reg `0x082`/`0x083`/`0x085`/`0x08E`）だけを
  自前で出し、TEV は借りたマテリアルのコマンド列（`MATCMD`）を再生している。
- **`MATCMD` を「捕獲した列」ではなく「自前で組んだ列」に替えれば、
  借り物はゼロになる。** レジスタの並びと符号化はこの節でゲーム自身から取れている。

### 使ったもの

`scratchpad/pica_decode.py` — PICA コマンド列の解読器（値 + ヘッダ、`extra` と 8 バイト丸め対応）。
`NCCH/exefs/code_runtime.bin` から読むので **IDA を起動しなくても再現できる**。
`0x8ADB10` の先頭 16 バイトが IDA の `get_bytes` と一致することを確認済み。

---

