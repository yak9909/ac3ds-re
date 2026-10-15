---
id: ACNL-F0450
aliases:
- IDA-opus-5-F019
title: 骨アニメを実機で結線し、骨が動いた（2026-09-21、HIGH、実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T009。資源は IDA-opus-5-F018 が選んだ'
date: '2026-09-21'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5161444
- 5160956
- 5164316
- 1844944
- 2069032
- 5168280
- 5062256
- 4761668
- 4811068
- 7657284
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:734-817
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F019: 骨アニメを実機で結線し、骨が動いた（2026-09-21、HIGH、実機）

解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T009。資源は IDA-opus-5-F018 が選んだ
`Insect/m_ins_tonosama.bcres`（24,448 B）、アニメは同ファイルの `wait`（`resource + 0x2F5C`）。
道具は `tools/models3d/skeletal_anim.py`、状態は `work/evidence/models3d/live_20260919/skel_state.json`。

### F018 の予測が実機でそのまま当たった

| 予測（資源から） | 実機（node `0x31017808`） |
|---|---|
| `SkeletalAnimation` だけを宣言 → `+0x228` が埋まる | `+0x228` = `0x31018130`（**非0**） |
| 群が1つだけ → binding は1行、索引0 | 行数 **1**、`+0x22C` = **0**、その1行が `0x31018130` 自身 |
| 材質・可視群は宣言なし | `+0x148` = 0、`+0x150` = 0 |
| CANM は30フレーム | フレーム制御器の `end` = **30.0** |

`UnitCursor` のとき（2行・`+0x14C`=1・`+0x228`=0）と鏡像になっている。

### 手順（1体につきゲーム呼び出し3回）

```
g3d_SkeletalAnim_Ctor      0x004EC1E4 (anim)
g3d_SkeletalAnim_BuildFromRes 0x004EBFFC (anim, holder, CANM, allocatorHolder, 0)
ModelInstance_BindSkeletalAnim 0x004ECD1C (holder, anim)
```

第5引数はスタックの `[sp]` に置く。ゲーム自身も `str r7,[sp]` で **0** を渡している
（`0x1C26D0` / `0x1F9228` の2箇所で確認）ので、既定の 64 が使われる。
instance の生成引数は **`(0x834, 1, 3)`**。`arbitrary_model` の既定 `(0, 0, 1)` は
`isAnimationEnabled=0` なので AnimBinding ができず、**結線先が無い**。

### 骨が動いたことの測り方（画像を使わない証明）

フレーム制御器は `0x4EDC98` の実コードから確定した:
**`+0x38`=現在フレーム / `+0x3C`=直前 / `+0x40`=速度 / `+0x44`,`+0x48`=範囲 /
`+0x4C`=折り返し関数（`AnimFrame_WrapLoop 0x4D3E70`） / `+0x58`=更新印**。
`+0x38` へ直接 float を書いて `AnimBinding_EvaluateAndApply 0x48A844(binding, 1)` を呼べば、
**描画せずに**適用だけを起こせる。骨の配列は骨格オブジェクトの
`{allocator, begin, end, capacity}` 4 つ組から形で特定する（**`0x49693C` が書く 2049 は
ビルダが上書きするので目印に使えない**）。10骨 × 64 B が2本、10骨 × 48 B が2本。

| 測定 | 結果 |
|---|---|
| phase 0 だけ | 何も書かない |
| phase 1（フレーム0で初回） | 骨配列 `skel+0x1C`（10×64）の **640 B 中 171 B** が変化 |
| フレーム 0 → 15 | 同配列の **53 B** が変化 |
| 動いた骨 | `root` `footL` `footR` `legL` `legR` の**5本だけ**。最大 float 差 0.416 |
| 動かなかった骨 | `m_ins_tonosama`、`foot` — **どちらもアニメの駆動対象ではない** |

**駆動対象でない骨が1バイトも動いていない**ことが、偶然や別要因ではないことの根拠になる。
`wait` で羽（`wing`/`wingL`/`wingR`）がフレーム0と15で同じなのは資源の内容と整合する。

### ヒープ

この boot の時点で親ヒープ `0x301668EC` の空きは **36,168 B**、12体のときに使った
instance ヒープ `0x30FE8C50` は **68,592 B**（どちらも `getFreeSize 0x74D744` で実測）。
そこで資源ヒープ `0xC000` は後者から、instance ヒープ `0x6000` は前者から取った。
`arbitrary_model.py` に `PARENT_RES` / `PARENT_INST` / `CREATE_ARGS` を足してある。

根拠: `events.jsonl` の `skel_*`、`skel_state.json`、
`skel_snap_a_after_phase0/b_after_phase1/c_frame15.json`、
`0x4EC1E4` `0x4EBFFC` `0x4ECD1C` `0x4EDC98` `0x49693C` の逆アセンブル。
### 描画まで通した（同じ日のうちに追記）

ケーブ（656 B @ `0x838600`）の13行目に入れ、12体の `UnitCursor` と**同時に**描いた。

| 項目 | 実測 |
|---|---|
| 1500ms あたりの hook 実行 | **46**（＝30.67fps。12体のときと同じ） |
| submit / advance / apply（1フレーム） | **13 / 13 / 26** |
| 2回の走行（計3秒・92フレーム） | 落ちず、ゲームは無傷 |
| フレーム制御器 | 共有時間 176.0 → 26.0、222.0 → 12.0。**どちらも `time mod 30` と一致**（`AnimFrame_WrapLoop` が折り返している） |
| 2回の走行の間の骨配列 | **126 B** 変化 |

つまり **1体あたり毎フレーム4呼び出し（advance → apply0 → apply1 → submit）という契約は、
マテリアルアニメでも骨アニメでもそのまま同じ**で、ケーブは種別を区別しない。
骨アニメ入りを1体足しても実効 fps は変わらなかった。

根拠: `events.jsonl` の `skel_*`、`skel_state.json`、
`skel_snap_a_after_phase0/b_after_phase1/c_frame15/d_cave_run1/e_cave_run2.json`、
`0x4EC1E4` `0x4EBFFC` `0x4ECD1C` `0x4EDC98` `0x49693C` の逆アセンブル。
反証条件: 別の資源で `+0x228` が埋まらない、phase 0 が要る資源がある、
**画像で見た確認はまだ取れていない**（IDA-opus-5-T014。Chokistream の映像が止まっている）。


