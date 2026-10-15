---
id: ACNL-F0152
aliases:
- F-114
title: 'F-114: ★★TODO-71 完了 — 描画コールバックが積むものの全体像（自前描画の手本）'
summary: 'confidence: **HIGH**（静的解析と実機のメモリ直読みの双方。レジスタ名は `registers.h` で照合）'
date: '2026-08-24'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 1240148
- 2680988
- 2681220
- 3128204
- 3113840
- 3113836
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:7168-7311
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-114: ★★TODO-71 完了 — 描画コールバックが積むものの全体像（自前描画の手本）

confidence: **HIGH**（静的解析と実機のメモリ直読みの双方。レジスタ名は `registers.h` で照合）

※ **F-115 で 1 件訂正**: ① の転送関数は `Mem_Copy` ではなく
**`Mem_CopyBytes`(`0x12EC54`)**。意味（memcpy）は同じだが関数が別。

`BsShadowViewMgr_DrawCallback`(`0x28E89C`) = FuncNode の `cb1`（レイヤー 1）。
**実機で観測できた唯一の `FuncNode` コールバック**（1 部屋・1 瞬間の観測。
他にいないとは言えない — F-115）なので、自前描画の直接の手本になる。

### 1. 構造

```c
sub_4EFA00(); sub_4E9E9C();                    // 前処理
GpuCmd_GetProperty(0x208, &p);                 // p = 現在の書き込み位置（基点）

Mem_CopyBytes(p, *(this+0xB4), 4 * *(this+0xB8));  // ★① 既製ブロックを丸ごと memcpy
q = BsShadowViewMgr_BuildShadowCmds(this, p + 4 * *(this+0xB8));  // ★② 可変部を組む
                                               // ★③ 後始末を直接組む（114 dword）
GpuCmd_Advance((q + 114*4) - p);               // 総バイト数を進める
```

**★役割分担がはっきりしている。**

| 段 | 内容 | 実機の量 |
|---|---|---|
| ① 既製ブロック | シェーダとパイプライン設定を丸ごと `memcpy` | **1032 dword = 4128 バイト** |
| ② 可変部 | 影ごとの「色＋アルファ」と「行列」だけ | 可変 |
| ③ 後始末 | 頂点属性の完全リセット | 114 dword = 456 バイト |

### 2. ★① 既製ブロックの中身（実機 `0x308950D4` を PICA ストリームとして解析）

**ヘッダを正しく歩くとストリームとして完全に整合した。**

| 位置 | reg | 名前 | 内容 |
|---|---|---|---|
| `@82` | `0x2CB` | `VSH_CODETRANSFER_CONFIG` | — |
| `@84` `@214` `@344` `@474` | `0x2CC` | `VSH_CODETRANSFER_DATA` | 128+128+128+97 = **481 命令のシェーダ本体** |
| `@572` | `0x2BF` | `VSH_CODETRANSFER_END` | `1` |
| `@576` | `0x2D6` | オペランド記述子 | 82 ワード |
| `@660`-`@672` | `0x2C0` | `VSH_FLOATUNIFORM_CONFIG` | uniform `0x5D`/`0x5E`/`0x5F`（f24, 3 ワード/vec4） |
| `@678` | `0x2B0` | `VSH_BOOLUNIFORM` | `0x7FFF1201` |
| `@690` | `0x2BA` | `VSH_ENTRYPOINT` | `0x7FFF01D8` |
| `@692` | `0x2BD` | `VSH_OUTMAP_MASK` | `0x1F` |
| `@702`-`@720` | `0x04F`-`0x06F` | シェーダ出力マップ | — |
| `@722` | `0x2C0` | `VSH_FLOATUNIFORM_CONFIG` | `0x80000000`（f32 モード, index 0） |

**★教訓: ゲームは「毎フレーム変わらない設定」を事前に作り置きして `memcpy` している。**
自前描画でも同じ形にするのが自然で速い。

`0xEAD0FEAD`（sead の未使用メモリ埋めパターン）が 77 dword（7.5%）現れるが、
**すべて `mask = 0` のバースト**（`@2` reg `0x251` extra 9、`@14`/`@48` reg `0x200` extra 29）
の**パラメータ部**に収まる。`mask = 0` は「どのビットも書かない」なので無害。
**この一致がストリーム解釈の裏付けになった**（ペア前提で読むと崩れる）。

### 3. ★② 可変部 — `BsShadowViewMgr_BuildShadowCmds`(`0x28E984`)

`(this, cursor)` を取り、進んだ cursor を返す。`vc_POINT1` が 0 なら素通り。

27 カテゴリ（`v10 = 0..26`）を回し、各カテゴリの連結リスト
（`dword_ABB854[v10]`、next = `*(e+136)`）の要素ごとに:

**アルファ**（カテゴリ 0/2/3/4/26 かつ `*(this+197) & 1` のとき距離フェード）

```
d = sqrtf((px - e.x)^2 + (pz - e.z)^2)      // px,pz は vc_POINT1 の位置
if (!(*(this+197) & 2)) d *= 0.6
t = clamp((d - 100) * 1/150, 0, 1)
alpha = t * *(this+176) * *(float*)(e+124)
```

**書き込む (value, header) は 1 組だけ**

```
value  = (*(u32*)(this+38) & 0xFFFFFF) | (alpha << 24)
header = (*(u16*)(this+42) + 3) | 0x000F0000
```

実機: `*(u16*)(this+42) = 0x00C0` → **reg `0x0C3` = `GPUREG_TEXENV0_COLOR`**
（`0x00C0` は `TEXENV0_SOURCE`。`+3` で `COLOR`）。
`*(u32*)(this+38) = 0x72260000`、`*(this+176) = 114 = 0x72`。
つまり **色は TexEnv0 の定数色に入り、アルファはその最上位バイト。**

**行列**

- 高速経路（`*(e+132) & 1` かつ `!(*(e+132) & 0x20)`）:
  `e+60`..`e+120` の **16 dword を事前計算済みとしてそのままコピー**
- 低速経路: 行列を作り
  `value = uniformIndex | 0x80000000`（f32 モード）,
  `header = 0x000F02C0` = `VSH_FLOATUNIFORM_CONFIG`、
  続けて `0x00BF02C1` = `VSH_FLOATUNIFORM_DATA` extra 11 → **12 ワード = 3×4 行列**

前後には `Mem_Copy` で既製の pre / draw / post ブロックを差し込む。

**★毎フレーム変わるのは「色＋アルファ」と「行列」だけ。**

### 4. ★③ 後始末 — 頂点属性の完全リセット（114 dword）

```
q[0]=0, q[1]=0x000F0201     GPUREG_ATTRIBBUFFERS_FORMAT_LOW  = 0
q[2]=0, q[3]=0x000F0202     GPUREG_ATTRIBBUFFERS_FORMAT_HIGH = 0
Mem_ZeroFill(q+4, 0x98)     152 バイト = 38 dword を 0 埋め
q[5] = 0x823F0203           reg 0x203 mask 0xF extra 35 consec 1
                            → GPUREG_ATTRIBBUFFER0_OFFSET から 36 レジスタ
                              （＝属性バッファ 12 本 × 3 reg）を全部 0 に
12 回ループ（6 dword/回）:
    w0 = i (0..11)
    w1 = 0x803F0232         reg 0x232 mask 0xF extra 3 consec 1
                            → GPUREG_FIXEDATTRIB_INDEX = i、続けて DATA0/1/2 = 0
    w2..w4 = 0, w5 = 0（偶数パディング）
```

内訳: `4 + 38 + 12*6 = 114` dword = 456 バイト = `0x1C8`。
`GpuCmd_Advance` に渡すのは `(q + 456) - p` で、**基点 `p` からの総バイト数**。

**★これは「頂点属性の完全リセット」。自前描画でも同じように後始末しないと
後続の描画を壊す。** F-109 で「頂点属性バッファの設定」と書いたのは
**方向が逆で、実際はリセット**だった（訂正）。

### 5. 判明した補助関数

| address | 名前 | 内容 |
|---|---|---|
| `0x2FBB8C` | `Mem_Copy` | ワード単位 memcpy（LDM/STM 0x20 バイト＋PLD） |
| `0x2F8370` | `Mem_WordFill` | ワード単位 memset |
| `0x2F836C` | `Mem_ZeroFill` | `Mem_WordFill(dst, bytes, 0)` |

### 6. ★自前描画の設計への落とし込み

1. **固定設定（シェーダ、出力マップ、TexEnv 等）は事前に 1 本のブロックとして作り、
   コールバックでは `Mem_Copy` するだけにする**
2. 毎フレーム変わる値だけを `(value, header)` の組で直接書く
3. **最後に頂点属性をリセットする**（③ をそのまま真似る）
4. `GpuCmd_Advance` には**基点からの総バイト数**を渡す。4 バイト境界に丸める

### 7. 進数の扱い

`registers.h` を実際に grep して名前を引いた。数値変換も `int_convert` を使い、
`-2109799933` → `0x823F0203`、`-2143354318` → `0x803F0232` を確認している
（CLAUDE.md「数値・アドレス変換を暗算しない」「16 進なら必ず `0x` を付ける」）。

---

