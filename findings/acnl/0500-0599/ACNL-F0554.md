---
id: ACNL-F0554
aliases:
- IDA-unknown-F028
- V2-F028
title: 実機測定で IDA-unknown-F027 を棄却。頂点バッファの束縛は正しい（2026-09-18、HIGH、実機）
summary: 設計（docs/topics/unit_cursor_hw_plan.md）→ 検証（tools/hw/verify_unitcursor_hw.py、45 件 ok）→ 実装（tools/hw/unitcursor_probe.py）
date: '2026-09-18'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4157-4173
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-unknown-F028: 実機測定で IDA-unknown-F027 を棄却。頂点バッファの束縛は正しい（2026-09-18、HIGH、実機）

設計（docs/topics/unit_cursor_hw_plan.md）→ 検証（tools/hw/verify_unitcursor_hw.py、45 件 ok）→ 実装（tools/hw/unitcursor_probe.py）
→ 検査（tools/hw/inspect_unitcursor_probe.py、0 failed）→ 適用、の順で実施。1 回で通り、クラッシュも中断も無く後片付けまで完了。

**(1) IDA-unknown-F027 は棄却。しかも欄の同定自体が誤りだった**。`mesh+52` は頂点バッファの番地ではなく、**`sub_4A8B44` が書く定数 `983744 = 0x000F02C0`**（レジスタ 0x02C0・マスク 0xF の PICA コマンドヘッダ）で、`mesh+48` から 48 バイトの埋め込みコマンド列（`sub_4957C4` が流す分）の一部。実機の値も `0x000F02C0` だった。`sub_7E5710` の `*(a2+52) = v13` は**資源側のメッシュ**に対する書き込みで、自前インスタンスの mesh とは別の object。IDA-unknown-F027 の「mesh+52 が 0 なら確定」という判定基準そのものが成立していなかった。

**(2) 頂点バッファの束縛は正しい**。属性コマンド列（`mesh+0x60` = 0x30FACC94、64 B）を復号すると、`reg 0x0200 ATTRIBBUFFERS_LOC = 0x03000000`（基底 = `<<3` で 0x18000000）、`reg 0x0203 ATTRIBBUFFER0_OFFSET = 0x08FAA908`。和は **物理 0x20FAA908 = VA 0x30FAA908** で、読み込んだ bcres（0x30FA8C80〜0x30FACC00）の内部に収まる。PICA では属性バッファの物理番地 = `(ATTRIBBUFFERS_LOC << 3) + ATTRIBBUFFERi_OFFSET` なので、**基底は VRAM 先頭を基準点に使っているだけで、実体の番地は正しい**。`sub_7E5710` の `v13` は「番地」ではなく**差分の基準点**だった。

**(3) 同時に 3 件が実機で裏付けられた**。`holder+260 = 3`（＝完了）→ IDA-unknown-F025(1) の「状態は +232 ではなく +260」が正しい。`node+0x1EC = 0x30FE9C80` → IDA-unknown-F025(3) のとおり、インスタンス用ヒープを分ければ活性化子が付く。`mesh+0x60`(0x30FACC94) + 64 = `mesh+0x68`(0x30FACCD4) → IDA-unknown-F026 の「2 本は 1 回の確保の前半・後半」が一致。

**(4) 結果として、これまで確かめた範囲はすべて正常**: 資源の読み込みと Setup、モデル検索、インスタンス生成（活性化子つき）、マテリアル（色・テクスチャ・ブレンド・深度・レイヤー）、メッシュの可視判定、2 本のコマンド列、頂点バッファの束縛、シーンへの登録、`Scene_DrawLayers` のふるい。**それでも画素が出ない**（IDA-unknown-F024 の実機節）。

**残る候補**（未検証）: (a) `desc[usage+76]` の属性番号対応 — `sub_7E5710` は呼び出し元の `sub_4A8B44` と違い `>= 0` の除外判定を持たないので、対応表が噛み合わないと不正な属性番号をそのまま書く。属性コマンド列の先頭語 `0xA000000B` は**シェーダが 12 属性を期待している**ことを示しており、UnitCursor のメッシュが実際に持つ数と噛み合っているかは未確認。(b) 頂点シェーダの束縛（`material+32` → `sub_496298`）。(c) 我々のノード用の変換行列がシェーダの定数として届いているか。

反証条件: mesh+52 が資源側では別の値を持つ、あるいは (ATTRIBBUFFERS_LOC<<3)+OFFSET が bcres の外を指す実例がある。根拠 work/evidence/unit_cursor/probe_result.json、docs/topics/unit_cursor_hw_plan.md §8。

