---
id: ACNL-F0503
aliases:
- IDA-opus-5.5-F028
title: PlayerModel と部品バンク。複製はゲーム自身の作成・片付け関数と「プロフィールの写し」で作れる（2026-09-24、HIGH（静的＋実機 BP・実機の読み取り）。複製の作成は未実施）
summary: '**構造**: AcPlayer+436 = PlayerModel（RTTI 11PlayerModel、vtbl 0x8E5F74、624 B）。pm+548 髪型 / +552 髪色 / +556 目の色 / +512 服 8 枠。'
date: '2026-09-24'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9330548
- 9741172
- 1853596
- 1914964
- 1896592
- 3066672
- 1897588
- 2176972
- 8530984
- 2177168
- 1897988
- 1896764
- 6630716
- 1913040
- 2177276
- 1915264
- 1895440
- 2564852
- 11003792
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2288-2302
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F028: PlayerModel と部品バンク。複製はゲーム自身の作成・片付け関数と「プロフィールの写し」で作れる（2026-09-24、HIGH（静的＋実機 BP・実機の読み取り）。複製の作成は未実施）

- **構造**: AcPlayer+436 = PlayerModel（RTTI 11PlayerModel、vtbl 0x8E5F74、624 B）。pm+548 髪型 / +552 髪色 / +556 目の色 / +512 服 8 枠。
  pm+324..+444 = {BankTable*, 枠} x15。管理役 = *(0x94A374)+24（HumanBankMgr_Get 0x1C489C）。部品バンクは BankTable<X,7>（枠 4 確保済み）。
- **作成**: PlayerModel_ctor 0x1D3854 → PlayerModel_CreateFromProfile 0x1CF090（人形 AcNpcDemoDollPlayer 0x2ECB30 と同じ呼び方）を 1 まで毎フレーム。
  初回の PlayerModel_Setup 0x1CF474 が BankTable_Acquire 0x2137CC で全バンクの空き枠を取る。
  **実機 BP**: BankTable<PlayerHeadBank>::MarkUsed 0x822C28 で停止（家に入ったとき、R1=枠 1）。戻り先の連鎖 0x213890（Acquire 内 BLX）→ 0x1CF604（Setup）→
  0x1CF13C（CreateStep）→ … → 0x652D3C（プレイヤー生成 → Actor_SpawnByProfile）。`work/evidence/models3d/bp_stack.json`（`tools/models3d/probe_bp_stack.py`）。BP は削除済み。
- **片付け**: PlayerModel_DestroyStep 0x1D30D0（BankTable_Release 0x2138FC、済むまで 0）。dtor 0x1D3980 は枠を返さない。
- **姿勢**: PlayerModel_SetMatrix 0x1CEC10（vtbl[9]）＝体と服 4 部品のノードに同じ行列。回転はここで。
- **髪型だけ変える**: Setup は見た目のレコード（profile+4）のポインタを pm+452 と頭の枠（PlayerHeadBank_SetSources 0x2722F4）へ渡し、髪は読み込み時にそこから読む。
  → プロフィール（42,112 B、vc_PLAYER_1_PPOFFSET = 0xA7E790 + 42112*n）を写して髪型 +4・髪色 +5 だけ変えて渡す。本物は書かない。
- **実機の空き枠**（村・家の中）: 自分は全バンク枠 1（使用中ビット 0x02）。枠 0/2/3 は空き。`work/evidence/models3d/player_model.json`。
- 設計・未確定点: [player_clone_preview](../docs/topics/player_clone_preview.md)。反証条件: 人形・オンラインの他人が同じバンクの別枠を使っていない場面で Acquire が失敗する等。

