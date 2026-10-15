---
id: ACNL-F0473
aliases:
- IDA-opus-5.5-F060
title: '持ち物の選択窓（ItemSelectWindow）のキー操作 — 十字・A・B の実装（2026-09-28、MEDIUM: 静的のみ。gohan d6b8470 で使用、実機未確認）'
summary: '解析ソフト: IDA（主 IDB を idalib-mcp で静的）/ 解析モデル: opus-5.5。利用者指示: 一覧が出ている間、ゲームと同じく十字で選択・A で決定・B でやめる（推測で自前実装しない）。'
date: '2026-09-28'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9739596
- 7156036
- 8697084
- 7156340
- 7156400
- 3400868
- 9375588
- 3107612
- 3399392
- 3105480
- 3107880
- 2858096
- 2857612
- 2859200
- 2862536
tags:
- inventory
supersedes: []
source: IDA:work/FINDINGS.md:1673-1692
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F060: 持ち物の選択窓（ItemSelectWindow）のキー操作 — 十字・A・B の実装（2026-09-28、MEDIUM: 静的のみ。gohan d6b8470 で使用、実機未確認）

解析ソフト: IDA（主 IDB を idalib-mcp で静的）/ 解析モデル: opus-5.5。利用者指示: 一覧が出ている間、ゲームと同じく十字で選択・A で決定・B でやめる（推測で自前実装しない）。
- **入力の出どころ**: BsMenuMgr（*0x949D4C）+68 = sead::ControllerWrapper（+72 押した瞬間 / +80 リピート / +0xFC ボタン数 / +0x110 hold / +372 対応表）。
  `BsMenuMgr_Init 0x6D3144` が `sub_54752C(+68, 19, 表 0x84B4FC)`（0x6D3274）: メニュー側ビット i ← 元（CtrController）のビット 表[i]。
  0x1 / 0x4 = A、0x2 / 0x8 = B、0x400 / 0x800 / 0x1000 / 0x2000 = 十字 上 / 下 / 左 / 右（元のビット 0, 1, 16..19。旧 input_block の対応表）。
  同じ関数が `sub_542B58(+68, 0x77F00, 20, 5)`（0x6D32B0）= リピートの遅れ 20・間隔 5（A・B は対象外）。`sub_542E88`: ボタンごとの押し続け c（最初 = 0）が
  c == 遅れ か c > 遅れ かつ (c − 遅れ) % 間隔 == 0 でリピートのビット。`sub_6D33F0(mgr, mask)` = +72 & mask（`sub_5CDAE4` が真なら 0）。
- **窓の部品**（窓 +1256、ctor 0x33E4A4、vtable **0x8F0F64**: +24 = 0x2F6B1C、+28 = **0x33DEE0**、+32 = 0x2F62C8、+44 = 0x2F6C28）。窓の更新 → `sub_2F7744` → `sub_2F7768`:
  vt+40 → **vt+24 ショートカット 0x2F6B1C**（部品 +208 & 8 かつ BsMenuMgr +508 == 部品 +204 (11) か −1）: 各ノードの **+196** を `sub_6D33F0` で照合し、当たったノードにフォーカス → ノード vt[+28](node, 1, 0) → 部品 vt[+44]（決定）。
  → **`ItemSelectWindow_LayoutRows` 0x2B9C70 が取消の行（窓 +1224）のノード +196 に 8（= B）を書く**（ほかの行は 0x2B9A8C で 0）。**B は「やめる」のショートカット**。
  その後 (+208 & 4 かつ +508 == +204) で **vt+28 キー方式 0x33DEE0**: フォーカスが無ければ +215 == 1 の最初のノード、`sub_722A6C`（次へ）/ `sub_722B40`（前へ）で隣のノード＋音 `sub_71C0F8`、
  `sub_6D33F0(mgr, 4)` = A でフォーカス中のノード vt[+52](node, node+32, 1) → 部品 vt[+44]。
  部品 +196 = 3076（`sub_2F6EF0`）| 81920（`sub_2F6D94`、0x1000 が無いとき）= 0x14C04 → 次へ = 0x800（下）/ 0x10000、前へ = 0x400（上）/ 0x4000。**左右は外れていて効かない**。
  窓を開くと（SelectIn_Enter 0x2BA0C0）BsMenuMgr +508 = 11。部品 +208 = 13（0x2BADC8、LayoutRows が取消の行の有無で 0x10 を上げ下げ）。
- **訂正**: 途中で「B の処理は窓・部品・ChoiceStandardItem のどこにも無い」と結論し、gohan 3afec9d で B を「窓の外タッチの取消の手順」で作っていた。**誤り**（探したのが `sub_6D33F0` の即値 2 / 8 だけで、ノードの +196 経由を見落とした。利用者の指摘）。
  また「キー方式 = sub_2F5C68」と書いたのは基底クラスの物で、この窓は派生の 0x33DEE0。
- **gohan d6b8470**: ゲームの入力は止めたまま、自前で呼ぶ ItemSelectWindow_Update の間だけ +72 / +80 に実機のボタンと同じビット（A 0x5、B 0xA、十字）を入れて戻す。判断・音・決定は窓の部品。
- 反証条件: 実機で十字・A・B が効かない（BsMenuMgr +508 が 11 でない、`sub_5CDAE4` が真）、B で「やめる」以外が決まる。

