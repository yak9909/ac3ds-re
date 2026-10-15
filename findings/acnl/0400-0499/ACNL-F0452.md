---
id: ACNL-F0452
aliases:
- IDA-opus-5-F022
title: 自前で作ったものを全部解放できた。ヒープは1バイト単位で元に戻る（2026-09-21、HIGH、実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T005。**このプロジェクトで初めての解放。**'
date: '2026-09-21'
category: system
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5178684
- 5161364
- 3109876
- 3243260
- 5177732
- 5166696
- 5161500
- 5184740
tags:
- heap
supersedes: []
source: IDA:work/FINDINGS.md:889-948
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F022: 自前で作ったものを全部解放できた。ヒープは1バイト単位で元に戻る（2026-09-21、HIGH、実機）

解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T005。**このプロジェクトで初めての解放。**
対象はカブトムシ1体（`m_ins_tonosama` + 骨アニメ `wait` + 専用ヒープ2本 + 資源）。
12体の `UnitCursor` には触れていない。設計は [instance_teardown_plan](../docs/topics/instance_teardown_plan.md)。

### 手順と結果（6段。全段が正常に戻り、ゲームは無傷）

| 段 | 呼んだもの | 結果 |
|---|---|---|
| T0 | ケーブの表から外す | 12/12/24 per frame へ復帰 |
| T1 | 46フレーム走らせて静止確認 | node 576 B と骨配列4本が **0 バイト変化** |
| T3 | `ModelInstance_Destroy 0x004F053C(holder)` | `holder+4 = 0`。**5,484 B** 返却 |
| T4 | `g3d::SkeletalAnim` vtable **スロット5** `0x004EC194(anim)` | `anim+8`(AnimObject) と `anim+0x10`(専用ヒープ) が 0。**652 B** 返却 |
| T5a | `sub_2F73F4 0x002F73F4(instance allocator)` | instance ヒープ `0x6000` を親へ返却 |
| T5b | `G3dResHolder_Dtor 0x00317CFC(holder)` | vtable が `ResourceSet` へ戻り、ファイル要求欄がクリア |
| T5c | `sub_2F73F4(resource allocator)` | 資源ヒープ `0xC000` を返却 |

### ヒープは元の値へ正確に戻る

| ヒープ | 作る前 | 解放直前 | 解放後 |
|---|---:|---:|---:|
| 親ヒープ `0x301668EC` | **36,168** | 11,576 | **36,168** |
| A の instance ヒープ `0x30FE8C50` | **68,592** | 19,424 | **68,592** |

**どちらも作る前に測った値とバイト単位で一致した。** 漏れも断片化も出ていない。
子ヒープの返却量は `0x6000 + 16` と `0xC000 + 16` で、16 B は確保ヘッダ。

instance ヒープ内訳: 24,576 B 中 6,304 B 使用 → T3 で 5,484 B、T4 で 652 B 返り、
残り 168 B は ExpHeap 自身の管理領域（ヒープごと破棄して回収）。

### 解放に使う関数（全部ゲーム自身の経路）

- `ModelInstance_Destroy 0x4F053C` → `0x4F0184`（mesh ポインタを昇順に戻す）→
  `SceneNodeHolder_Destroy 0x4ED668`（node vtable[0] → **`node+4` のアロケータ**の vtable slot3 で free → `holder+4=0`）。
  **前処理は instance が自前の mesh 配列を持つとき（`node+0x170 != +0x174`）は資源に触れない。**
  等しいときは `resModel+184` 経由で**資源側へ書く**ので、共有資源では危険。今回は自前配列があった。
- `g3d::SkeletalAnim` の後始末は **vtable スロット5**（`0x4EC194`）。デストラクタ（スロット1 `0x4EC21C`）は
  vtable と HeapAllocator を戻すだけで、**AnimObject も専用ヒープも解放しない**。
  スロット5 はビルド失敗時にゲーム自身が呼ぶ経路で、`*(anim+20)=0` → AnimObject の dtor と free →
  `sub_2F73F4(anim+12)` で専用ヒープ破棄、まで一気にやる。
- `sub_2F73F4(allocator)` は `allocator+4` のヒープに対し **heap vtable[4]（`+0x10`）= destroy** を呼び、`allocator+4` を 0 にする。

### GPU の引き取りについて（設計時の想定を1点訂正）

設計では「`mgr[9] >= mgr[8]` かつ `byte_AD98D8 == 0` を確認してから解放する」としていたが、
**park（描画パスの中）では `submitted=2 / dispatched=0` が常態で、この条件は満たせない。**
実際に成り立っているのは「**その instance を submit しなくなってから数百フレーム経っている**」の方で、
`Render_FrameEnd 0x4F1CE4` が毎フレーム全トラバーサを捨て、コマンドリストが2面で回ることから、
2フレーム以上あけば在庫は入れ替わる。今回はそれを大きく上回っていた。
**GX キューの欄は「今このフレームの積み具合」を見るものであって、解放の門にはならない。**

根拠: `events.jsonl` の `destroy_*`、`skel_state.json`（`inst_heap_free_*` / `A_free_*` / `parent_free_*`）、
`destroy_predestroy_record.json`、`skel_snap_g_predestroy` / `h_predestroy2`、
画像 `after_destroy_top.png` / `after_full_teardown_top.png`、
`0x4F053C` `0x4F0184` `0x4ED668` `0x4EC194` `0x4EC21C` `0x2F73F4` `0x317CFC` の逆アセンブル。
反証条件: 共有資源（ゲーム自身が読んだ bcres）では `0x4F0184` の分岐が資源側へ書く、
mesh が多いモデルでは局所配列65要素を超える、場面転換中の解放は別、
**描画中（submit をやめずに）解放したらどうなるかは試していない**。

