---
id: ACNL-F0455
aliases:
- IDA-opus-5-F025
title: 描画中に instance を解放しても何も起きない。ただし理由は2つある（2026-09-21、HIGH、実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T017a。**意図的に安全手順を破った試験。**'
date: '2026-09-21'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5178684
- 1798712
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:1080-1118
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F025: 描画中に instance を解放しても何も起きない。ただし理由は2つある（2026-09-21、HIGH、実機）

解析ソフト: IDA / 解析モデル: opus-5。IDA-opus-5-T017a。**意図的に安全手順を破った試験。**

### やったこと

カブトムシ1体をケーブで**毎フレーム submit している最中に**、`ModelInstance_Destroy 0x4F053C` を呼んだ。
park（`0x1B7238`）は**ケーブが submit を終えた直後**の位置なので、
「このフレームで提出したばかりの instance を、同じフレームの中で解放する」という最悪の並びになる。

| | 解放前 | 解放直後 | 1.5秒走らせた後 |
|---|---:|---:|---:|
| `runs` | 45 | 46 | **92**（増え続ける） |
| `submits` | 45 | 46 | **46（凍結）** |
| `applies` | 90 | 92 | **92（凍結）** |
| `holder+4` | node | **0** | 0 |

**ゲームは無傷**（画像 `t017a_after_free_while_drawing_top.png`）。GPU も固まらず、絵も壊れなかった。
消えたのはカブトムシだけ。

### なぜ無事だったのか。理由は2つあり、片方は「たまたま」ではない

1. **ケーブが自分で守っている。** 各段が `holder != 0` → `[holder+4] != 0` → vtable 一致 を確かめてから
   進むので、`holder+4` が 0 になった次のフレームからそのエントリを飛ばす。
   `submits` と `applies` が解放の瞬間で止まり `runs` だけ増え続けたのがその証拠。
   **この守りが無いケーブなら、宙に浮いた node ポインタを submit して落ちていたはず。**
2. **instance の記憶は GPU から見えていない**（IDA-opus-5-F022 の分解）。
   コマンドリストを組む側（CPU）が読むだけなので、組み終わったあとに解放しても
   在庫のコマンドが壊れた番地を指すことはない。

**したがって「submit をやめてから解放する」規則は、instance に関しては**
**必須ではなく作法**である。ただし上の 1. を満たすケーブであることが前提。

**まだ試していないのは資源側**（頂点・テクスチャ。GPU が番地で直接読む）。そちらは別物。

根拠: `events.jsonl` の `t017a_*`、`t017a_before.json`、
画像 `t017_drawing_before_free_top.png` / `t017a_after_free_while_drawing_top.png`。
反証条件: 守りの無いケーブ、mesh の多いモデル、apply 中の解放（今回は apply の外で呼んでいる）。

