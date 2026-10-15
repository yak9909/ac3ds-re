---
id: ACNL-F0472
aliases:
- IDA-opus-5.5-F061
title: 'UnitCursor を村の物体の下に描く — 地面に張り付く物の材質と、深度書き込みの出どころ（2026-09-28、MEDIUM: 静的のみ。gohan f47f5af、実機未確認）'
summary: '解析ソフト: IDA（主 IDB を idalib-mcp で静的）/ 解析モデル: opus-5.5。利用者指示: マイデザイン等の極薄・地面に吸着したモデルに UnitCursor が被さる → 常に対象マスのモデルより下／背面。公共事業エディターも共通。'
date: '2026-09-28'
category: render
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5875968
- 5881836
- 5885396
- 5885400
- 5885472
- 5885468
- 5177252
- 9424656
- 4833420
- 4835876
- 4836088
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:1656-1672
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F061: UnitCursor を村の物体の下に描く — 地面に張り付く物の材質と、深度書き込みの出どころ（2026-09-28、MEDIUM: 静的のみ。gohan f47f5af、実機未確認）

解析ソフト: IDA（主 IDB を idalib-mcp で静的）/ 解析モデル: opus-5.5。利用者指示: マイデザイン等の極薄・地面に吸着したモデルに UnitCursor が被さる → 常に対象マスのモデルより下／背面。公共事業エディターも共通。
- **地面のマイデザイン** = アイテム 0x9D（Pattern。ID 一覧）→ romfs Fg/Param/Fg.bin[0x9D] +12 = 形 76。季節資源（base romfs Fg/Bcres/Season00.bcres ほか）の **fg_mydesign**。
  材質 mat_fg_mydesign（`tools/models3d/dump_material_state.py`）: **層 0・不透明（BLEND ONE/ZERO）・0x107 = 0x41（深度テスト LESS、深度書き込みは材質のブロックでは触らない）**。
  m_UnitCursor: 層 1・加算（SRC_A/ONE）・0x107 = 0x41。どちらも深度のずらし（0x4D/0x4E）無し。→ カーソルは層 1 で後から描かれ、平らな物と高さが近いと LESS で勝って被さる。
- **村の物体の描画**: `fgobj_Proc_Setup` が proc + 0x45B0 に FuncNode を作り cb0（層 0）= **0x59A900**、cb1（層 1）= 0x59BFEC（0x59CDD4 / 0x59CDD8、リテラル 0x59CE20 / 0x59CE1C）。
  cb0 → `fgobj_DrawList`(proc, ctx, proc+13740)。物体は `sub_59C778` が obj+104 & 0x20000 なら +13752（層 1）、それ以外は +13740（層 0）へ。描画ノードは `sub_59C8FC`（Proc の slot 12）がシーン 0 へ。
  `g3d_FuncNode_SetCallbacks` は node + 0x148 に cb0 / cb1 / userdata（0x4EFFA4 `ADD R4,R4,#0x148` / `STM`）。FuncNode の vtable 0x8FCF10。
  （★主 IDB で 0x59A900 / 0x59BFEC の名前を逆に付けていたので、fgobj_DrawCallbackLayer0 / Layer1 に直した）
- **深度書き込みの出どころ**: 汎用の書き出し 0x49C08C の 0x49CA24〜0x49CAF8: フラグメント部分 a3[20]（M+0x50）の鍵 +720 が前回と違えば、+280 の bit1 を深度書き込みとして
  0x107 の上位バイト（ヘッダ 0x20107。色マスク << 8 | 深度書き込み << 12）で積む。→ 体ごとの写しの +280 bit1 を落とし +720 = 0 にすれば、その体は深度を書かない。
- **gohan f47f5af**: InstancedDraw::SubmitUnder = 村の物体の描画ノードの cb0 を包み、先頭で登録された束を（層を問わず）描いてから 0x59A900 を呼ぶ = 地面の後・村の物体の前。
  GridCursor（全エディター共通）はこれで描き、深度を書かない（DisableDepthWrite）。村の物体の描画ノードが無い場面は従来の自前ノード。`fgobj_DrawList` は先頭でキャッシュを捨てるので、後の物体に状態は漏れない。
- **未確定**: 地面が村の物体の描画ノードより先に描かれること（描画段の登録順 = Base 物体の連結リスト、旧 F-113。地面の登録元は未特定）。外れた場合はカーソルが地面に消されて見えない（落ちない）。
- 反証条件: 実機でカーソルが見えない（地面が後）、物体の上にカーソルが残る、ほかの物体の深度が崩れる。

