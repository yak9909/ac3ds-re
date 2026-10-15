---
id: ACNL-F0631
aliases:
- IDA-gpt-6.1-sol-F005
title: '家具が置けない・壁紙が張り替わらない原因（2026-10-08、HIGH: 実機 BP＋静的）'
summary: '解析: 親（opus-5.5）が ida-pro-mcp の BP で測定、Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix2、--allow-gohan）が静的解析と修正。根拠 **work/evidence/t022_catalog_fix2/report.md**。gohan 1746df8。'
date: '2026-10-08'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 2642856
- 6889676
- 10230260
- 5049380
- 5049420
- 2908072
- 5978548
- 9789324
- 1096200
- 1775260
- 1688956
- 1695608
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4981-4991
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F005: 家具が置けない・壁紙が張り替わらない原因（2026-10-08、HIGH: 実機 BP＋静的）

解析: 親（opus-5.5）が ida-pro-mcp の BP で測定、Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix2、--allow-gohan）が静的解析と修正。根拠 **work/evidence/t022_catalog_fix2/report.md**。gohan 1746df8。
- 家具（実測）: 起点 s_origin = 部屋 3 の (8,14)、Room_GetInteriorCellBounds 0x2853A8 = x[4,11] z[5,12]（両端を含む）→ z が範囲外で PlaceFurniture が拒否、TryPut 0x6920CC 未到達。FtrTable 0x9C19F4・空き 25。
  修正: HHD Room_GetPutStartCell は起点を範囲の端へ収めてから探す（0x4D0C24〜0x4D0C4C の CMP/STRLT 4 組。親が HHD v1.1 code.bin を capstone で照合）→ DecorPlace::Search で同じく収める。占有チェックの引数は実位置のまま。
- 壁紙（実測）: HouseRoom_SetWallpaper 0x2C5FA8 に Item {0x2385, 0}（カテゴリ 3）で到達、入口の Room_CanChangeWallOrFloorForCurrentPlayer 0x5B39B4 が 0。途中: 部屋 3、プレイヤー 0、家 0、家の記録（[0x955F8C] + 0x5D900 + 0x1228 × 家）+0x4 = 0。4 軒の +0x4 = [0, 3, 0, 0]。
  +0x4 = 家の今の外観の種類（Codex、MEDIUM: 書く側 0x10BA08 が予定 +0xD から日替わりで写す、読む側 HouseExterior_GetObjectDataForPlayer 0x1B169C が 0 なら Strc/data/hobj/tent/hobj_tent_%02d.bin、1〜6 なら my_house）。→ 0 = テント。判定 0x5B39B4 は 0 / 8 なら不可。ポケットの壁紙・床（PocketMenu_UseWallpaper 0x19C57C / UseFlooring 0x19DF78）も同じ判定を通る。
  → テントでは壁紙・床を替えられないのはゲーム本来の決まり。判定は飛ばさない（Codex・親とも）。対象のセーブで普段から 0 か（家がテントか）は利用者に確認する。
- IDB: 主 IDB に命名 9 ほか・部分型 T022_HouseSaveExteriorPrefix、HHD に命名 2・コメント（ID は親が F005 に置換: 主 18、HHD 6）。
- 追記（2026-10-08 実機 decor_catalog6）: 家具の配置 PASS。利用者: 家の見た目はテント（壁紙・床の不可はゲーム本来）。

