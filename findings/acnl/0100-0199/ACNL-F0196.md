---
id: ACNL-F0196
aliases:
- F-170
title: 'F-170: CTRPF は発行点の問題を解決しない。cursor は値渡しでグローバルに無い — `HIGH`（静的解析、assembly で確認）'
summary: 「発行点の問題は CTRPF で実行すれば解決するのでは」という指摘を受けて確かめた。
date: '2026-08-28'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4947436
- 4948832
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:10265-10329
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-170: CTRPF は発行点の問題を解決しない。cursor は値渡しでグローバルに無い — `HIGH`（静的解析、assembly で確認）

### 1. 問い

「発行点の問題は CTRPF で実行すれば解決するのでは」という指摘を受けて確かめた。

### 2. CTRPF の `Hook` が与えるもの

**我々のコードケーブと同じ能力**である。
ゲームのスレッド上で任意のアドレスに自前コードを置ける。
C++ で書けるぶん楽になるが、**能力としては増えていない。**
プラグインスレッド側は cursor を持たないので、そちらからは触れない。

必要なのは 2 つ:

- **(a) 毎フレーム通るフック地点** — CTRPF `Hook` で簡単に置ける
- **(b) その地点で有効な cursor** — **解析でしか埋まらない**

### 3. cursor はグローバルに無い（確認済み）

**`TextBox_UpdateDrawState`(`0x4B7DEC`)**
テクスチャ状態の差分を積んで **進んだ cursor を返すだけ**。
**グローバルへ書き戻していない。**

**`sub_4B8360`(`0x4B8360`)**
`sub_73CF48` では `a2 = sub_4B8360(a4)` と 1 引数に見えるが、
assembly では

```
MOV R0, R3        ; drawctx
BL  sub_4B8360    ; R1 は触られず cursor がそのまま渡る
```

**実際は `sub_4B8360(drawctx, cursor)` の 2 引数。**
渡された cursor を消費して進めた結果を返すだけで、
**cursor を作り出す関数ではない。**

（decompiler が引数を落とす罠はこれで 3 度目。
F-164 の `Alloc`/`Free` と同じ。**assembly を見ること。**）

### 4. 結論

**cursor は描画ウォークの上流から値渡しで流れてくる。**
任意の地点で入手する手段は現時点で無い。
したがって **CTRPF に移しても発行点の問題は残る。** TODO-115 は未解決のまま。

### 5. 解決の候補

- **上流を辿る** — レイアウト描画ウォークの起点で誰が最初の cursor を持つかを特定する
- **★自前のコマンドリストを再生させる** — F-145 で
  「会話 TextBox は専用 list 32 に構築され、`GpuCmd_ReplayRecordedListRange` で
  メイン list へ再生される」ことが分かっている。
  **F-166 で GPU 可視メモリを確保できるようになったので、
  自前のリストを組んで再生させる道が開けた。** こちらのほうが筋が良い。
  → TODO-110 / TODO-112 と合流する

### 6. 現状の実務的な制約

対象の TextBox が描かれる場面でしか出せない。
**どの程度の場面で描かれているかは未確認。**
ユーザーの指摘によれば、上画面の時計 UI は一定時間操作しないときだけ出るので、
「常にどれかの TextBox が描かれている」とは限らない（F-166 の教訓）。

---

