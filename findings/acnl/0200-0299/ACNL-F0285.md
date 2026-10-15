---
id: ACNL-F0285
aliases:
- F-262
title: 'F-262: 再生の複製経路を逆アセンブルで裏取りし、実装の誤り 2 件を追加で直した — `HIGH`（静的のみ）'
summary: '`GpuCmd_ReplayRecordedListRange` の `if (a7)` 側（`0x7B0E08`〜）を逆アセンブルした。'
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 8064520
- 5069980
- 2097280
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:15512-15599
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-262: 再生の複製経路を逆アセンブルで裏取りし、実装の誤り 2 件を追加で直した — `HIGH`（静的のみ）

### 裏取り 1: `Layout+0x11C = 1` が必須であることの独立確認

`GpuCmd_ReplayRecordedListRange` の `if (a7)` 側（`0x7B0E08`〜）を逆アセンブルした。

```
LDR R0,[SP,#var_C]   ; a2 = 記録の開始オフセット
LDR R1,[R7,#4]       ; R7 = 送り元マネージャ → R1 = 送り元 base
ADD R2,R0,R10        ; R10 = 既にコピー済みのバイト数
ADD R1,R1,R2         ; ★src = 送り元base + start + copied
LDR R0,[SP,#var_8]   ; a3 = 長さ
SUB R5,R0,R10        ; 残りバイト数
LDR R0,[R4]          ; R4 = &g_GpuCmdPtr → dst
MOV R2,R5
BL  sub_2F858C       ; memcpy(dst, src, size)
LDR R0,[R4]; BIC R1,R5,#3; ADD R0,R0,R1; STR R0,[R4]   ; g_GpuCmdPtr += size & ~3
```

**この複製は `a7`（= `Layout+0x11C`）が真のときにしか実行されない。**
`else` 側はキューのエントリに印を付けるだけで、1 バイトも積まない。
`sub_5685A4` が `+0x11C = 1` を書いていることと合わせ、**独立した 2 経路で確定**した。

同時に、マネージャの `+0x04` が base、`Layout+0x104` が開始オフセット、
`+0x108` が長さであることも、この 1 箇所で全部裏が取れた。

### 裏取り 2: `drawctx` は `Drawer`（`mgr+0x364`）そのもの

`nwlyt_GetDrawCtxForList`（`0x4D5C9C`）は名前に反して**取得関数ではない**。
`a1+116` へ float 3 つと 0 を書いて `a1+116` を返す **setter** で、
別の drawctx オブジェクトを返してはいない。
`sub_4D7274`（DrawBegin の実体）が `a1+1684..1698` を触ることと合わせ、
**Drawer と drawctx は同一オブジェクト**で確定（IDB の名前は誤解を招くのでコメントを追加）。

### 裏取り 3: 記録経路に `GpuCmd_SplitAndSubmit` は無い

- `sub_4D72C4`（DrawBegin 後半）は生のコマンド語をカーソルへ直接書き、
  `sub_2F858C` で Drawer が持つ既定ブロックを複製するだけ
- `sub_4D7204`（DrawEnd 後半）も `sub_2F858C(cursor, *(drawer+0x14), *(drawer+0x18))` だけ
- `sub_4D71D4`（DrawEnd 前半）は `drawctx+36 != 0` のとき `DrawCtx_FlushBatch` を呼ぶ

したがって**記録中に GX キューのエントリは作られない**。
再生時は `a5 = 0` になり、上記の「本体まるごと複製」経路だけが走る。

### 定数の展開（暗算せずスクリプトで計算）

| 出所 | 値 | 意味 |
|---|---|---|
| 再生の scissor | `0x802F0065` | reg `0x065` から 3 語連続（scissor mode / pos / dim） |
| 同 | `((w-1)<<16) \| (h-1)` | **`Layout+0x28` の幅と `+0x2C` の高さがここに出る** |
| 8 バイトパディング | `0x0008025E` / `0x0008021E` | reg `0x25E` / `0x21E` |
| SplitAndSubmit 末尾 | `0x000F0111` / `0x000F0110` / `0x000F0010` | FRAMEBUFFER_FLUSH / INVALIDATE / FINALIZE |
| DrawBegin | `0x0002006F`、`0x00200080`、`0x000B0080` | reg `0x06F` と **reg `0x080`（テクスチャユニット構成）** |
| `sub_4D6C90` | `0x013F02C1` | reg `0x2C1`（行列） |

**DrawBegin が reg `0x080` を設定している。** 以前 `ONLY_TEXUNIT0` として
手で入れた `reg 0x080 = 1` は、この既定設定と重複していた。

### ★実装の誤り 3: 記録時の画面選択に `display` を使っていた

`Layout+0x134`（display）は `LayoutList_SetDisplay` が**再生の直前**に書く。
記録は `RecordChildren`（`SetDisplay` より前）で走るので、
記録の時点では**前フレームの最後の値**が入っている。初回は 0 で、
上画面ノードが下画面のスプライト表を選んでしまう。

→ 登録時にノードへ**画面番号**（`+0xFC`。0=上 / 1=下）を書き、それで選ぶよう変更。

### ★実装の誤り 4: マテリアルの控えが無いと描画ごと諦めていた

自前記録では `DrawBegin1` が既定の GPU 状態（reg `0x06F` / `0x080` と Drawer の既定ブロック）を
積むので、借りたマテリアルが無くても描ける見込みがある。
控えが無い場合は**マテリアルの部分だけ飛ばして描画は続行**するよう変更した。

### 検証

いずれも生成語を静的 IDB へ一時的に書き込み、IDA に逆アセンブルさせて確認し、
元のバイト列へ戻した（`idb_save` は呼んでいない）。

```
LDR R1,[R4,#0xFC] / CMP R1,#0 / BEQ 上画面ブロック（+0x88/+0x8C/+0x9C）
                                 落ちた先は下画面ブロック（+0x80/+0x84/+0x98）
CMP R2,#0 / BEQ matdone          （マテリアルだけ省いて続行）
```

**実機には一切適用していない。**

---

