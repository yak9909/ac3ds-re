---
id: ACNL-F0289
aliases:
- F-266
title: 'F-266: ★★★★★`SetupProjectionMatrix` は **`+0x28` / `+0x2C` しか読まない**。だから自前ノードでもそのまま呼べる — `HIGH`（静的のみ）'
summary: F-265 では投影行列を手で組み立てたが、その前提
date: '2026-09-01'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7584448
- 5667776
- 8611868
- 8611872
- 8611876
- 8611880
- 8611884
- 8611888
- 8611892
- 8611896
- 8611900
- 8622080
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:15888-15974
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-266: ★★★★★`SetupProjectionMatrix` は **`+0x28` / `+0x2C` しか読まない**。だから自前ノードでもそのまま呼べる — `HIGH`（静的のみ）

F-265 では投影行列を手で組み立てたが、その前提
「レイアウトの矩形は原点が画面中央（`l = -W/2, r = W/2, t = H/2, b = -H/2`）」は
F-208 の**実測**に頼っていて静的には未証明だった。裏を取ったところ**証明できた**。

### `sub_73BAC0(&rect, Layout+0x10)`（`0x73BAC0`）

```c
float *sub_73BAC0(float *result, int a2)
{
  v2 = *(float *)(a2 + 24);      // a2 = Layout+0x10 なので Layout+0x28 = 幅
  v3 = *(float *)(a2 + 28);      //                       Layout+0x2C = 高さ
  result[0] = v2 * -0.5;         // l = -W/2
  result[1] = v3 *  0.5;         // t = +H/2
  result[2] = v2 *  0.5;         // r = +W/2
  result[3] = v3 * -0.5;         // b = -H/2
  return result;
}
```

**ペインツリーは一切読まない。読むのは `Layout+0x28` と `Layout+0x2C` の 2 つの float だけ。**

これで 3 つのことが同時に決まった。

1. **原点は必ず画面中央**であり、`-(r+l)/(r-l) = 0` / `-(t+b)/(t-b) = 0`。
   F-265 の「非ゼロは `m[1]`, `m[4]`, `m[10]`, `m[11]`, `m[15]` の 5 つだけ」は正しい。
   **F-208 の実測（原点=中央、1 単位=1px）と静的な式が独立に一致した。**
2. **投影と scissor は同じ 2 つの float から作られる。**
   F-264 で `+0x28` / `+0x2C` に画面実寸を入れたことが、投影にもそのまま効く。
3. **自前ノードでも `ssys_ma_lyt_Layout_SetupProjectionMatrix`（`0x567BC0`）を直接呼べる。**
   ペインツリー（`+0x10`）が空でも、`+0x28` / `+0x2C` さえ入っていれば正しく動く。

### 実装を差し替えた

手組みの 27 語（16 語ゼロ埋め＋5 本のリテラル書き込み）をやめ、
**ゲームの関数を呼ぶ 4 語**にした。算術を自分で持たないぶん間違えようがない。

```
MOV  R2,#0
STRB R2,[R1,#0x121]     ; 透視投影フラグ = 0（1 だと透視の枝へ行く）
MOV  R0,R1              ; this = 自前ノード
BL   0x567BC0           ; ssys_ma_lyt_Layout_SetupProjectionMatrix
LDR  R1,=NODE           ; R1 を取り直す
```

`+0x121`（= `a1 + 289`）は `0x567BC0` が唯一見る他のフィールド。
雛形の複製範囲（`+0x28`〜`+0x78`）の外なので、明示的に 0 にする。

**F-265 に書いた行列の中身は破棄しない。** 将来 `+0x34` を実機で読んだときの
期待値（`m[1] = 2/H`, `m[4] = -2/W`, `m[10] = 0.001`, `m[11] = -0.5`, `m[15] = 1.0`、他 0）
として使える。上画面なら `m[1] = 0x3C088889` / `m[4] = 0xBBA3D70A`、
下画面なら `m[1] = 0x3C088889` / `m[4] = 0xBBCCCCCD`。

### 検証（IDA。空き `.text` の `0x83681C` へ一時的に当てて逆アセンブル、直後に復元）

```
0x83681c LDR  R2, loc_83687C
0x836820 STR  R2, [R1,#0x28]
0x836824 LDR  R2, loc_836880
0x836828 STR  R2, [R1,#0x2C]
0x83682c MOV  R2, #0
0x836830 STRB R2, [R1,#0x121]
0x836834 MOV  R0, R1
0x836838 BL   ssys_ma_lyt_Layout_SetupProjectionMatrix
0x83683c LDR  R1, loc_836868
```

BL の飛び先は、生成語 `0xEBF4BC50` / `0xEBF4BBF0` から独立に復号しても
両ケーブとも `0x00567BC0` になった（IDA の表示と一致）。
復元後のバイト列は `NCCH/exefs/code_runtime.bin` の同アドレスと完全一致。

監査（`audit_node_cave.py`、`SETUPPROJ` を既知外部に追加）: 総異常 0 件・重なりなし。

### ケーブ配置（F-266 時点）

```
CAVE_Q=0x838200(382) CAVE_P=0x838800(35)  CAVE_V=0x838890(44)
CAVE_A1=0x838940(98) CAVE_A2=0x838AD0(93) CAVE_N=0x838C50(11)
CAVE_M=0x838C80(7)   CAVE_B=0x838CA0(12)  CAVE_U=0x838CD0(12)
CAVE_F=0x838D00(10)  CAVE_T=0x838D30(2)    末尾 0x838D40 / 上限 0x839000（余り 704 バイト）
```

**未適用。実機へは入れていない。**

---

