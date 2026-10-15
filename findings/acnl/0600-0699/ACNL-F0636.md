---
id: ACNL-F0636
aliases:
- IDA-gpt-6.1-sol-F010
title: 窓を開けなくなる原因 — 余白の基準（連続空き）が現実の割れ方と合っていなかった（2026-10-09、実測 HIGH + 静的 MEDIUM）
summary: '測定: 親（sonnet-5.5、拒否された後の停止状態）。修正: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix7）。根拠 **work/evidence/t022_heap_20261009/README.md**、**work/evidence/t022_catalog_fix7/report.md**。gohan 1bfb8ca。'
date: '2026-10-09'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5625880
- 5626088
- 5624540
- 7658520
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:5039-5048
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F010: 窓を開けなくなる原因 — 余白の基準（連続空き）が現実の割れ方と合っていなかった（2026-10-09、実測 HIGH + 静的 MEDIUM）

測定: 親（sonnet-5.5、拒否された後の停止状態）。修正: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix7）。根拠 **work/evidence/t022_heap_20261009/README.md**、**work/evidence/t022_catalog_fix7/report.md**。gohan 1bfb8ca。
- 実測: 読み込みのヒープの総空き 1,251,204 B は 2 ブロック（828,856 / 422,348 B）に割れている。リークなし（窓を閉じると総空きは元に戻る）。拒否された窓の構築: 完成後の総空き 658,136 B（基準 629,026 B 以上）、最大連続空き 499,448 B（基準未満）。基準 = max(600 KiB, 開始時の空きの半分) は、空きが割れている以上、連続空きでは構造的に満たせなかった。
  ゲーム側の消費は小さい: チップ 1 個の Setup が 5,616 B、同期家具の生成ではほぼ変化なし。
- 修正: 総空き 384 KiB（0x60000）・最大連続空き 128 KiB（0x20000）を別々の基準に（開始時の半分の基準は廃止）。窓の大きな塊（arc の写し、アイコン枠）をヒープの末尾側から確保（ExpHeap の確保 0x55D818 は 0x55D8E8 で ldrsb [heap+0x50]（方向 +1）× 整列を掛け、負なら末尾側 0x55D2DC → 0x74DC18。親が命令と実機の方向の値で照合）→ 窓を返したとき元の大きな連続空きに戻りやすい。拒否の通知に不足の種類と 残り/必要 の数値を表示。
- 未確定: 全品目での 384 / 128 KiB の十分性、末尾確保による断片化の改善（実機未確認）。反証条件: 384 / 128 KiB 以上の空きで窓を開いた状態の家具追加が止まる。
- IDB: 主 IDB に rename 3・型 3・コメント、ModuleIndoor にコメント（ID は親が F010 に置換）。
- 追記（2026-10-09 実機 decor_catalog11）: 全項目 PASS。ただし家具を約 48 個出すと「合計不足」→ F011。

