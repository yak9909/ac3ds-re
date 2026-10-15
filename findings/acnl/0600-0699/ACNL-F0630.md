---
id: ACNL-F0630
aliases:
- IDA-gpt-6.1-sol-F004
title: 'T022 カタログの実機不具合 8 件の原因と修正（2026-10-08、MEDIUM: 静的。実機未確認）'
summary: '解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（xhigh）**、Codex（依頼 work/codex/tasks/t022_catalog_fix1.md、--allow-gohan）。採番・照合・commit は親（opus-5.5）。根拠 **work/evidence/t022_catalog_fix1/report.md**。gohan b68e21f（work/decor-catalog）。'
date: '2026-10-08'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6889676
- 3299628
- 3299664
- 3299924
- 3299968
- 3299668
- 9740332
- 3304696
- 3305312
- 9368488
- 4959608
- 3912852
tags:
- catalog
supersedes: []
source: IDA:work/FINDINGS.md:4968-4980
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F004: T022 カタログの実機不具合 8 件の原因と修正（2026-10-08、MEDIUM: 静的。実機未確認）

解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（xhigh）**、Codex（依頼 work/codex/tasks/t022_catalog_fix1.md、--allow-gohan）。採番・照合・commit は親（opus-5.5）。根拠 **work/evidence/t022_catalog_fix1/report.md**。gohan b68e21f（work/decor-catalog）。
- 小分類の色: OnDecide(Kind) が s_kind = -1 にしてから ShowKindSelection → 前の小分類を戻していなかった。
- 置けない: 模様替え中のプレイヤー不在は LOW（未測定）。エディターに入る前に観測した位置を起点に保持し、実体が無いときは 0x6920CC の占有引数だけ負値にする（負なら占有チェックを省く）。離したときの当たり判定が離した後の座標（CTRPF Touch::GetPosition = hidTouchRead）で外れていた疑い（壁紙・床が替わらない件と共通の候補）→ 最後に触れていた点で判定。
- 手前に出るゲーム UI: BsMenuRoomLightSwitch_BuildLayouts 0x32592C が rom_lgt / rom_chip / rom_strg の優先度を 0x87 にする（0x325950 / 0x325A54・0x325A80）。窓は 0x80 → 0x88。親の照合（opus-5.5）: 0x325950 MOV R0,#0x87 → 0x325954 STRB [R4,#0x44]（R4+0x38 = Layout、+0xC = 優先度）。
- 十字キー案内: g_BsMenuRoomLightSwitch 0x94A02C（Setup 0x326CF8 が登録・Teardown 0x326F60 が 0、vtable 0x8EF3A8）の +0x474 = N_angl_00。ゴミ箱オンかつエディター中は非表示、オフで元の可視ビット。
- 名前: 文字ペインの幅が固定で左寄せ・折り返し（TextBox +0x48 が折り返し幅、0x4BAD78）。HHD 0x3BB494 は文字ペインの幅も更新する → 文字幅で更新、寄せを中央へ（make_catalog_arc）。
- タブ長押し: 範囲選択器 = エディター +128200（Neutral 0xB3D1E4 が更新）。0xB0AAF0 は開始点 +0x1A8/+0x1AC が非 0 なら離したときに確定。タブで始まった指は離すまで遮断し、漏れた開始点を 0 に戻す。親の照合: ModuleIndoor.elf の 0xB0AB10〜0xB0AB3C の命令列が一致。
- 壁紙・床: F106 の経路は再確認、誤りとは断定せず。実機到達は未確認。
- IDB: 主 IDB に命名 7・型・コメント 12、ModuleIndoor にコメント 7 ほか（ID は親が F??? → F004 に置換、件数一致）。
- 追記（2026-10-08 実機 decor_catalog5）: 1・3〜7 は PASS。家具・壁紙・床は「不可」の音 → F005。

