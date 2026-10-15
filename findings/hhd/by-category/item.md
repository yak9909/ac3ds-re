<!-- 生成物。編集しない（kb.py index が作り直す） -->

# hhd / item

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| HHD-F0016 | 置ける場所の計算・家具の削除・状態名の表（2026-10-06、MEDIUM: 静的のみ） | 入口（**訂正 2026-10-07、IDA-gpt-6.1-sol-HHD-F001 を親 opus-5.5 が逆コンパイルと xref で照合**: `Room_PutItemAuto` は既存の部屋の物（`sub_583DF4(a2)`）から品を取る**コピー側**。カタログから新しく出す入口は `HHD_Room_RequestFurnitureAutoPlacement` 0x4D00A0（呼び手 `HHD_CatalogWindow_WaitExec` 0x36B | MEDIUM | S |
| HHD-F0019 | カタログのタブ・種類の表と、種類ごとの品の並び（2026-10-07、HIGH 相当: 静的 + ROM の実データで全件検算） | 解析ソフト: IDA / 解析モデル: opus-5.5。T022。再現 `tools/hhd/catalog_kinds.py` → work/evidence/hhd_decorate/catalog_kinds.json。 | HIGH | S |
| HHD-F0020 | カタログの格子 Tum15・上段タブ・小分類・名前の吹き出し・NEW の動き（2026-10-07、MEDIUM: 静的のみ） | 解析ソフト: IDA（idalib）/ 解析モデル: **gpt-6.1-sol（推論 max）**、Codex CLI のサブエージェントとして（依頼 work/codex/tasks/t022_tum15.md）。記録・採番・照合は親（opus-5.5）。対象 HHD v1.1（code.bin SHA-256 42a4e486…）。 | MEDIUM | A |
