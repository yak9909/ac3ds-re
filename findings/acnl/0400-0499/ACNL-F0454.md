---
id: ACNL-F0454
aliases:
- IDA-opus-5-F024
title: 場面転換。自前instanceは無傷で残り、ケーブは自分から描画を止める（2026-09-21、HIGH、実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T018。**利用者に建物へ入ってもらって測定した。**'
date: '2026-09-21'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9769786
- 9735792
- 9418824
- 9436920
- 9751624
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:1033-1079
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F024: 場面転換。自前instanceは無傷で残り、ケーブは自分から描画を止める（2026-09-21、HIGH、実機）

解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T018。**利用者に建物へ入ってもらって測定した。**
対象は `Insect/m_ins_tonosama.bcres` の instance 1体（尺10、アニメ無し）、ケーブ 656 B @ `0x838600` で毎フレーム submit。

### 測ったこと

| | 転換前 | 転換後 |
|---|---|---|
| 部屋 `0x0095133A` | 0（村の屋外） | 96 → 0（建物へ入って戻った） |
| シーン所有者 `[0x00948E70]` | `0x33109044` | 読み込み中は **0**、戻ると **`0x3310DAF8`**（別番地） |
| その資源 `manager+0x34` | `0x30C91F00` | `0x30CA9280`（別番地） |
| ケーブの `runs` / `submits` | 増え続ける | **146 で凍結** |
| 自前 node の 576 B | sha `6dbdf415…` | **sha `6dbdf415…`（完全一致）** |
| 自前 node の vtable / activator | `0x8FB848` / `0x30C50214` | 同じ |
| 自前の資源ヒープ・instanceヒープ | 生存 | **どちらも vtable `0x8FFEF8` のまま生存** |
| 自前の資源 / モデル | `CGFX` / `CMDL` | 同じ |
| 親ヒープ `[0x0094CC48]` | `0x301668EC` | 同じ |
| ゲーム | 無事 | **無事**（画像 `t018_after_room_change_top.png`） |

### 3つの結論

1. **自前 instance は場面転換で一切触られない。** 576 バイトがバイト単位で同一だった。
   どのシーンにも登録していないので、ゲームの走査に入らない。**これは以前からの設計どおり**で、
   実測で確かめられた。
2. **ケーブは自分から描画を止める。** 先頭の所有者検査（`[0x948E70]` が生成時の manager と一致し、
   `manager+0x34` が生成時の資源と一致するか）が、読み込み中は manager が 0 なので落ち、
   戻ってきた後も**manager が別番地で作り直される**ので落ち続ける。
   **つまりこの検査は「場面が変わったら描かない」を自動で満たす**。安全側に倒れている。
3. **描画を再開したければ検査の値を作り直す必要がある。** ケーブは manager と資源の番地を
   リテラルに焼いているので、転換後は永久に一致しない。3gx では**場面転換のたびに焼き直す**か、
   別の判定（部屋IDなど）に変える設計が要る。

### 重要な前提: 借りている資源かどうか

今回の instance が参照している資源は**こちらが自分のヒープへ読み込んだ copy**（`res_heap 0x30FA8C40`）で、
ゲームの Season 資源ではない。だから Season が破棄されても無事だった。
**ゲーム側の資源を借りて instance を作っていたら、Season の破棄で足元が消える**
（`fgobj_Proc_Destroy` が Season とそのヒープを解放する。`models3d.md`）。
**自前で読み込むこと自体が、場面転換に対する守りになっている。**

根拠: `events.jsonl` の `t018_*`、`t018_before.json`、
画像 `t018_before_room_change_top.png` / `t018_after_room_change_top.png`、
`build_anim_hook.py` の所有者検査、実機の読み出し。
反証条件: 別の部屋種別（屋内→屋内、夢、島）で違う、セーブ/ロードを挟むと違う、
長時間の滞在でヒープが再利用される。

