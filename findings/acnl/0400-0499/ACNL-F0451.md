---
id: ACNL-F0451
aliases:
- IDA-opus-5-F018
title: 骨アニメが結線できる条件と、実機に触れずに選んだ資源の組（2026-09-21、HIGH、静的＋実機読み出し）
summary: '解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T009 の前段。**実機へは一切書いていない**（読み出しのみ）。'
date: '2026-09-21'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5164316
- 5178112
- 4811068
- 5161444
- 9424028
- 9438524
- 5160956
- 5159956
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:818-888
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F018: 骨アニメが結線できる条件と、実機に触れずに選んだ資源の組（2026-09-21、HIGH、静的＋実機読み出し）

解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T009 の前段。**実機へは一切書いていない**（読み出しのみ）。

### 結線できるかどうかは「モデル資源が群を宣言しているか」で決まる

`ModelInstance_BindSkeletalAnim 0x004ECD1C` はマテリアル版 `0x4F0300` と**同じ式**で書く。

```
slots = *(binding + 0x1C)          binding = *(node + 0x28)
per    = *(binding + 0x28)         index   = *(node + 0x22C)   <- ここだけ違う（材質は +0x14C）
slots[index * per] = *(anim + 8)
```

前提が2つあり、**どちらも外すと危険**:

1. `node` が `SkeletalModel` でないと TypeNode 走査が null になり、**そのまま `v3[138]` で番地 `0x228` を読んで SIGSEGV**する。
   関数は自分で守ってくれない。
2. `node+0x228`（`m_SkeletalAnimGroup`）が 0 なら**何も書かずに戻る**。

そして **`node+0x228` はモデル資源が `CMDL+0x2C` の群 DICT で `"SkeletalAnimation"` を宣言しているときだけ埋まる**。
アニメ群は `ModelInstance_Create` の引数ではなく**資源が決める**。

### 独立2経路で一致（UnitCursor がなぜ 0 だったか）

| 経路 | 結果 |
|---|---|
| 資源（`Ftr/Chip/UnitCursor.bcres` の `CMDL+0x2C`） | `['VisibilityAnimation', 'MaterialAnimation']` の**2つだけ** |
| 実機（このセッションの instance の `node+0x28`） | 群は**2行**（行0=1メンバ、行1=4メンバ）、`+0x14C`=1、**`+0x228`=0 / `+0x22C`=-1** |

行数・索引・`+0x228` が 0 であることが資源の宣言とそのまま対応する。
IDA-opus-5-T009 に書いていた「`UnitCursor` は資源に骨アニメが無いので 0」は結論としては合っていたが、
**正しい理由は「骨アニメの有無」ではなく「モデルが群を宣言していない」こと**。
`UnitCursor` は骨を1本持っており（`type 0x40000092` ＝ SkeletalModel）、骨が無いわけではない。

### CMDL / CANM の読み方（`nwgfx_SkeletalModel_Create 0x0049693C` の実コードから）

| 欄 | 意味 |
|---|---|
| `CMDL+0x2C` | アニメ群 DICT（宣言する群の名前） |
| `CMDL+0xE0` | 骨格への相対ポインタ |
| 骨格`+0x18` | 骨数 |
| 骨格`+0x1C` | 骨 DICT（エントリは `DICT+0x1C` から16バイト刻み） |
| `CANM+0x00` | `'CANM'` |
| `CANM+0x0C` | **対象アニメ群の名前**（`"SkeletalAnimation"` / `"MaterialAnimation"`） |
| `CANM+0x14` | フレーム数（float） |
| `CANM+0x18` / `+0x1C` | メンバ数 / メンバ DICT。骨アニメのメンバ名は骨名 |

`g3d::SkeletalAnim` の生成は `0x004EC1E4`（32バイト。`+0=0x8FCC9C`、`+4=2`、`+8=0`、`+0xC=0x90053C`、`+0x10=heap`、`+0x14=0`）。
`g3d_SkeletalAnim_BuildFromRes 0x004EBFFC(anim, holder, canm, allocatorHolder, maxAnimObjects)` は
**`maxAnimObjects` が 0 なら 64 を使う**。**holder は `anim+0x14`**（MaterialAnim は `+0x18`。ここが違う）。

### 実機に触れずに選んだ候補（`tools/models3d/survey_skeletal.py`）

romfs 2本・**8,818 ファイル**を走査し、骨付きモデル **2,059**（うち `SkeletalAnimation` を宣言 **2,030**）、
骨アニメ **2,596** を得た。読めなかったのは6件で、いずれも `artifacts/base/romfs/Bg/Outdoor/Models/grd_Dtn_*`
（base 展開が PARTIAL なので原本側の問題。update 側には影響しない）。

**第一候補: `MiniGame0/character/esc_spider.bcres`（155,776 B）**

- モデル `esc_spider_bq`、`type 0x40000092`（SkeletalModel）、骨21本、群は3つ全部を宣言。
- 同じファイルに骨アニメ8本。`esc_spider_wait1_bq` は `SkeletalAnimation` 群・**21/21 骨・30フレーム**。
- **モデルとアニメが同一ファイル**＝ゲーム自身の組み合わせなので、互換性を仮定しなくてよい。
- 次点は `esc_scorpion.bcres`（324,352 B、骨54本、49/49）。資源ヒープを倍にする必要がある。

根拠: `tools/models3d/survey_skeletal.py`、`work/evidence/models3d/arbitrary_20260920/skeletal_survey.json`、
`0x4ECD1C` `0x4EBFFC` `0x4EC1E4` `0x49693C` `0x4EBC14` の逆アセンブル、実機の node `0x30FE94B8` の読み出し。
反証条件: 群を宣言していても `+0x228` が 0 のままの場合がある、`esc_spider` が MiniGame 専用の別経路を要求する、
骨アニメのメンバ名が骨名でない資源がある。


