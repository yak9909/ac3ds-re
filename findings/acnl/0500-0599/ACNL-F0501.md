---
id: ACNL-F0501
aliases:
- IDA-opus-5.5-F030
title: '複製を出したまま建物に入ると無限ロード＝管理役が枠の返却を待つ。枠は BankTable_Release で下ろしてから返す（2026-09-24、HIGH（静的＋実機 2 回）。直した gohan 0107a5b は利用者が実機で確認: 出したまま建物に出入りしても止まらない、入ったあと複製は消える、OFF→ON で問題なく再出現）'
summary: '**利用者の実機確認（gohan fa33556）**: 右隣に完全な複製（装備も同じ）、髪型・髪色は複製だけに適用、OFF で消える。**出したまま建物に入ると無限ロード。**'
date: '2026-09-24'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9741172
- 1853304
- 1853276
- 2756212
- 2760084
- 8160896
- 8160984
- 2563156
- 5675848
- 8530840
- 2177276
- 1753576
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2258-2278
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F030: 複製を出したまま建物に入ると無限ロード＝管理役が枠の返却を待つ。枠は BankTable_Release で下ろしてから返す（2026-09-24、HIGH（静的＋実機 2 回）。直した gohan 0107a5b は利用者が実機で確認: 出したまま建物に出入りしても止まらない、入ったあと複製は消える、OFF→ON で問題なく再出現）

- **利用者の実機確認（gohan fa33556）**: 右隣に完全な複製（装備も同じ）、髪型・髪色は複製だけに適用、OFF で消える。**出したまま建物に入ると無限ロード。**
- **原因（2 経路）**:
  - 実機（Suspend 中）: 大域 `0x94A374` = 0、古い `BsPlayerMgr 0x3308714C` は生きていて、各バンクの使用数 +8 が複製の分だけ残る
    （7 枠型は枠 3、顔は枠 7、テクスチャアニメは枠 0 と 7）。`work/evidence/models3d/clone_state_loading.json`（`tools/models3d/probe_clone_state.py`）。
  - 静的: `BsPlayerMgr` vtbl[19] `BsPlayerMgr_ClearGlobal 0x1C4778` が大域を 0 にし、vtbl[20] `BsPlayerMgr_DestroyWaitBanks 0x1C475C` が
    `BsPlayerMgr_DestroyBanks 0x2A0E74` を呼ぶ。後者は各バンクの使用数が 0 でないとその場で 0 を返し、前者が 3（やり直し）を返し続ける。
  - gohan は場面の変化を見て**枠を返さずに手放していた**。
- **復旧の試み（実機、書き込み）**: 使用中ビット 12 か所と使用数 12 か所を 0 にした（`tools/models3d/release_stuck_clone_slots.py`、元値 `release_stuck_state.json`）。
  読み込みは進んだが、管理役の片付けの頭の段（0x2A1D94）→ `PlayerHeadBank_UnloadBuffer 0x7C8680`（0x7C86D8）→ 0x271C54 → … →
  `Allocator::Free 0x569B48` がアロケータ 0 で **SIGSEGV**（R6 = テクスチャアニメのバンクの枠 7 の中）。`work/evidence/models3d/bp_stack.json`、
  `work/evidence/models3d/alpha_screen_20260920/ida_warning.png`（inspect_ida_dialog.ps1 の保存先）。**利用者の再起動が必要。**
- **なぜ落ちたか（静的）**: `BankTable_Release` は vt[0]（頭は `BankTable_PlayerHeadBank_UnloadSlot 0x822B98` = 読み込み先 2 つを
  `PlayerHeadBank_UnloadBuffer` で下ろし、済むと真）が真のときだけ空きにする。ビットと数だけを消したので頭が読み込まれたまま残り、
  `DestroyBanks` はテクスチャアニメを先に消す順なので、その後で頭を下ろすときに消えたアロケータを使った。
- **直し（gohan 0107a5b、実機未確認）**: 場面の変化で積むのをやめ 4 フレーム待ち、**作ったときの管理役**のバンクへ `PlayerModel_DestroyStep` と同じ順で
  `BankTable_Release 0x2138FC` を返し終えるまで毎フレーム（顔は `sub_2711A4`、体は `HumanModel_DestroyBody 0x1AC1E8` を先に）。諦めない。
  検査 `tools/models3d/verify_player_clone.py`（片付けの順 = DestroyStep の BL 0x2138FC の順、取る組 = Setup の Acquire の組、vtbl の番地、手放さない）0 failed。
- 反証条件: 直した版でも出したまま建物に入ると止まる／落ちる（フレームフックが読み込み中に回らない、管理役が先に消える等）。

