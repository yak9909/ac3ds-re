---
id: ACNL-F0543
aliases:
- IDA-opus-5-F005
title: SkeletalModelも描けた。node+0x228/+0x22C は不可視の原因ではない（2026-09-21、HIGH、実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。**`UnitCursor`（`0x40000092` = `nw::gfx::SkeletalModel`）を'
date: '2026-09-21'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:3944-3972
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F005: SkeletalModelも描けた。node+0x228/+0x22C は不可視の原因ではない（2026-09-21、HIGH、実機）

解析ソフト: IDA / 解析モデル: opus-5。**`UnitCursor`（`0x40000092` = `nw::gfx::SkeletalModel`）を
曲面変換した姿勢で置いたら、そのまま画面に出た。** 生成引数は木と同じ `(0, 0, 1)`。
同じフレームに `book`（`0x40000012` = `nw::gfx::Model`）を並べ、枠を片方ずつ切って帰属を確定させた。

| 画像 | 枠A(book) | 枠B(UnitCursor) | 見えたもの | 計器 |
|---|---|---|---|---|
| `run3_01_both_slots_top.png` | on | on | 本＋明るい縞 | runs 45 / submits **90**（1回に2体） |
| `run3_02_slotA_book_only_top.png` | on | off | **本のみ** | 46 / 46 |
| `run3_03_slotB_cursor_only_top.png` | off | on | **縞のみ** | 46 / 46 |
| `run3_04_all_off_top.png` | off | off | **どちらも無し** | 0 / 0 |

画素でも整合する（`run3_pixel_diff.json`）: 本だけで 3,445 px、カーソルだけで 27,399 px、
両方で 29,879 px（＝和 30,844 − 重なり 965）。カーソルが大きいのは加算合成の光だから。

**IDA-unknown-F029 の残る容疑を棄却する。** 描画に成功したこの `UnitCursor` の
`node+0x228 = 0` / `+0x22C = -1` は、**`a7=3` で観測した値と同一**（今回は `a7=1`）。
描く `book` 側は `+0x228 = 0x30FE8F44` / `+0x22C = 0xBCD` だが、これはクラスの違いであって
可視性の条件ではない。**`a7` も原因ではなかった。** 旧 `UnitCursor` が見えなかったのは
IDA-opus-5-F003 のとおり生のゲーム座標に置いていたからで、これで説明が閉じた。

曲面角はこの boot でも実機 `0x5C63`=23651 ＝ 事前予測 23651（**3 回目の独立一致**、別の座標で）。

根拠: `work/evidence/models3d/arbitrary_20260920/` の `run3_*.png`（4枚）、`run3_pixel_diff.json`、
`run3_result.json`、`arb_state_b.json`、`events.jsonl`。
反証条件: 枠Bを空にしても縞が出る、別の部屋・尺で再現しない、他の SkeletalModel で出ない。
未確認: SkeletalModel はこの 1 種類のみ。骨・アニメは一切与えていない（静止姿勢）。

