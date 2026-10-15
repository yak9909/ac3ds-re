---
id: ACNL-F0632
aliases:
- IDA-gpt-6.1-sol-F006
title: '足したチップが動かない・2 回目の窓のヒープ不足・テントでの壁紙/床タブ（2026-10-08、MEDIUM: 静的。実機未確認）'
summary: '解析: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix3。5 時間枠のため停止指示で途中終了、ビルド可の状態）。照合・仕上げ・採番は親（opus-5.5、Codex の枠切れ後）。根拠 **work/evidence/t022_catalog_fix3/report.md**。gohan d059843。'
date: '2026-10-08'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5625880
- 5623888
- 7658312
- 7657648
- 9436920
- 5978548
tags:
- heap
supersedes: []
source: IDA:work/FINDINGS.md:4992-5002
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F006: 足したチップが動かない・2 回目の窓のヒープ不足・テントでの壁紙/床タブ（2026-10-08、MEDIUM: 静的。実機未確認）

解析: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix3。5 時間枠のため停止指示で途中終了、ビルド可の状態）。照合・仕上げ・採番は親（opus-5.5、Codex の枠切れ後）。根拠 **work/evidence/t022_catalog_fix3/report.md**。gohan d059843。
- **F002 の訂正**: ModuleIndoor の状態表 0xB62434 = {"Neutral", enter 0xB3D49C, calc 0xB3D1E4}、0xB62448 = {"Out", enter 0xB3D7B0, calc 0xB3D708}。F002 の「0xB3D7B0 = Editor_Neutral_Enter」は誤りで Out の入口（IDB の名前を訂正済み）。親が ELF のバイトで照合。
- チップ: Neutral の入口 0xB3D49C は使用中の各チップに Chip_RestoreOwnRoot 0xB2F77C を呼ぶ（0xB3D4F8 の BL、間隔 1120 = r4×7×5×32）。0xB2F77C = root *(chip+0x44)、N_All *(chip+0x3F0)、親 *(N_All+0xC) が root でなければ RemoveChild → AppendChild(root) → LayoutCalc（親が ELF で照合）。
  gohan の旧 ChipStep が呼んでいた Editor_AttachActiveChipPanes 0xB2F6E4 は全チップを In/Out 用の共有ペインへ付け直す処理 → 既存のチップも更新の木から外れた、という見立て（症状と一致、ペインの親は未実測）。→ 足したチップにだけ 0xB2F77C。窓を返してから・選択/まとめ（+129100 / 件数 +128640）/共通ボタン（+126796 / +129288）が空のときだけ足す。
- ヒープ: ExpHeap の確保は 1 個の自由ブロックから取る（0x55D818 → 0x55D050 → FindFreeBlockHeadAligned 0x74DB48）。合計空きは足りても連続枠が無いと失敗 → アイコン枠 184,320 B を最初に取る、判定は sead_ExpHeap_getMaxAllocatableSize 0x74D8B0（vtable 0x8FFEF8 の +64、+60 が getFreeSize。親が照合）、組み上がり後に 24 KiB（0x6000、暫定）残らなければ開かない。s_heapMaxLog / s_heapWindowReady を記録。
- テント: 模様替えの開始時に Room_CanChangeWallOrFloorForCurrentPlayer 0x5B39B4 を呼んで保存し、不可なら壁紙・床タブは不可音で窓を開かない（判定は飛ばさない）。
- 反証条件: 足したチップと既存チップの N_All の親が自身の root なのに症状が残る。旧方式の失敗直前に 0x80 整列で 184,320 B 以上の連続空きがあった。
- 追記（2026-10-08 実機 decor_catalog7）: チップ（既存・追加とも）と 2 回目の窓は PASS。テントのタブは不可音のまま（利用者の家は「改造で見た目だけテント」で、内装は張り替えられる状態）。

