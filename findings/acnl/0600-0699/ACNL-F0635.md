---
id: ACNL-F0635
aliases:
- IDA-gpt-6.1-sol-F009
title: '窓が読み込みヒープを食う最大の原因は非表示 TextBox の描画用バッファ（2026-10-09、MEDIUM: 静的。実機未確認）'
summary: '解析: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix6）。照合・commit・採番は親（sonnet-5.5）。根拠 **work/evidence/t022_catalog_fix6/report.md**。gohan f43f757（work/decor-catalog）。'
date: '2026-10-09'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 4960932
- 4960388
- 1292712
tags:
- heap
supersedes: []
source: IDA:work/FINDINGS.md:5027-5038
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F009: 窓が読み込みヒープを食う最大の原因は非表示 TextBox の描画用バッファ（2026-10-09、MEDIUM: 静的。実機未確認）

解析: Codex gpt-6.1-sol xhigh（依頼 t022_catalog_fix6）。照合・commit・採番は親（sonnet-5.5）。根拠 **work/evidence/t022_catalog_fix6/report.md**。gohan f43f757（work/decor-catalog）。
- TextBox は表示状態に関係なく、additionalChars（文字数）に応じた文字／描画の器を読み込みヒープから確保する（TextBox ctor 0x4BB2A4 → 0x4BB084 → vtable +0x70 = 0x13B9A8）。1 文字数 N の器 = totalBytes(N) = 2*(N+1) + drawBytes(N)、drawBytes(N) = ((((((N+7)>>3)+3)&~3)+44*N+55)&~0xF) + 4*((78*N+57)&~3)（Codex。補助語の式は旧プロジェクトの F-342 の BatchCmdWords と同形）。N=127: 45,744 B、N=129: 46,468 B。家具窓の文字 9 個（additionalChars 128）= 413,868 B が窓の 1.22 MB の約 3 割。
- 修正: 窓の文字の additionalChars を名前 16 / 数字 8 へ（原本 STR_Item_name の最大は UTF-16 12 単位。日本語版原本の最大で検証）。家具の旧 9 器 413,868 B → 名前 1 器 5,632 B（−408,236 B）。壁床の文字器 370,296 → 16,108 B。
  さらに、家具窓の不要な上段タブ・リメイク・b00/b01 枝の物理削除、arc を家具用 hhd_catalog.arc（329,256 B）・壁床用 hhd_catalog_wall.arc（184,488 B）に分割、アイコン枠 45 → 24 枠（98,304 B。見える最大 21 セル + 退役待ち 3）、呼ばれないセル loop の削除。
  見積り: 窓の消費 1,221,920 → 617,460 B（残り 639,984 B、目標 628,722 B 以上）。
- 閉じたら窓を毎回返す（SD 読み直し）。家具の生成とチップの追加は窓を返した後。余白の基準 = max(600 KiB, 開始時の空きの半分)、窓完成後・家具決定前・チップ追加前に総空きと 0x80 整列の最大連続空きを確認。毎秒のヒープ記録リング（16 件）と家具／チップごとの消費記録。
- 未確定: 実機の消費・再開時間・家具／チップのピーク、GX 待ちとの因果（LOW）。反証条件: 空きが 600 KiB 以上ある状態で同じ GX 待ちが起きる、または見積りと実測が大きく違う。
- IDB: 主 IDB に容量計算関数の rename 2・コメント 6（ID は親が F009 に置換）。
- 追記（2026-10-09 実機 decor_catalog10）: 窓・再開・位置復元・名前 PASS。繰り返すと「ゲーム用の空きを残せず窓を開けません」→ F010。

