---
id: ACNL-F0638
aliases:
- IDA-gpt-6.1-sol-F012
title: HHD の「壁にかける家具」リストの移植（2026-10-09、静的 MEDIUM、実機未確認）
summary: '調査・実装: Codex gpt-6.1-sol xhigh（依頼 t022_wall_catalog）。照合・commit・採番は親（sonnet-5.5）。根拠 **work/evidence/t022_wall_catalog/report.md**。gohan 3e9654f。'
date: '2026-10-09'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 6796388
- 6889676
- 7051592
- 7048408
- 5055460
- 5036844
- 5036936
- 5036988
- 6773716
- 6773748
- 5191760
- 7755296
- 9742464
- 6879876
- 5978820
- 6888148
- 6888244
- 6888284
- 5692964
- 5693128
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:5061-5071
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F012: HHD の「壁にかける家具」リストの移植（2026-10-09、静的 MEDIUM、実機未確認）

調査・実装: Codex gpt-6.1-sol xhigh（依頼 t022_wall_catalog）。照合・commit・採番は親（sonnet-5.5）。根拠 **work/evidence/t022_wall_catalog/report.md**。gohan 3e9654f。
- HHD main 2 のタブ 0（my_pct_AWall）の種類 6 個を、原 ItemSort の順のまま ACNL 対応 665 品・48 ページで追加（壁 71 / 時計 32 / 曲 91 / 絵 25 / 服 346 / ワンピース 100）。HHD 専用の服 3 品（0x36CC / 0x36C6 / 0x36C5）と天井タブ（品 0）は出さない。表は HHD の表 0x67B464 と ItemSort の再読込みで全件照合。
- 品番: 壁表は服 147・ワンピース 148・曲 49 のカテゴリ側を選ぶ（床表は従来の 6 / 7 / 47）。0x6920CC は入力品番をそのまま記録し変換しない（F003: 通常の「カベにかける」は 0x6B9948 → 0x6B8CD8 で変換）。
- 置き場所: HHD の壁探索 0x4D23E4 を別関数 DecorPlace::SearchWall に移植（HHD Room_PutFurnitureAuto 0x4CDB2C の壁判定 0x4CDB88 → 0x4CDBBC。8 候補、向き表 0x675BD4 = [3,3,1,1,0,0,2,2]、角度表 0x675BF4）。カメラの向きによる壁の優先（HHD 0x4F3850 と ACNL 0x765620 が同じ角度分岐。ACNL の vc_CAMERA1 0x94A880 のオブジェクト +0x68 / +0x60 / +0x58 / +0x50 の壁 alpha）。ACNL の 0x6920CC へ壁用の品番・向き・層 0 を渡し、本来の配置制約を維持。成功戻り 0 のときだけ 0x68FA84。
- テント: ACNL のゲーム自身が壁の品に対して 0x5B3AC4（自宅で House+4 == 0 なら 1）で壁掛けを不可にする（Room_SearchPutSpot 0x691AD4 の 0x691B34〜0x691B5C）。gohan も同じ判定を呼んで本来の不可を維持。**利用者の改造テントの家では壁掛けが不可になる**（壁紙・床は利用者の依頼で例外にしたが、壁掛けは未対応。実機で確認してから判断）。
- 壁の家具の層は 0、親なし（CreatePrepare 0x56DE24 の 0x56DEC8 / 0x56DED8 / 0x56DFA8）。Editor_CreateChips 0xB3CC08 は壁も除外しない。既存の ChipStep（Finalize bit1 → anchor → Setup → root 復元）をそのまま使う。
- UI: 上段の 3 つ目のタブは MainTop の L_Top_02（x −27、黄色）、窓は ctl_Base_02 系。arc は別ファイル hhd_catalog_hang.arc（204,200 B）、常駐 hhd_catalog_top.arc は 27,688 B（+8,448 B）、hhd_icons.bin は 18,008,448 B。窓の同時保持は従来どおり 1 つ。
- 未確定: 実機の壁の位置・向き・チップ、窓のヒープ消費（壁窓が家具窓より多いか）。反証条件: 壁 side と rot が実マップで合わない、壁の家具が層 0 / 親なしにならない、チップがずれる。
- IDB: 主 IDB 6+1、Indoor 3、HHD 2+2 のコメント／命名（ID は親が F012 に置換）。
