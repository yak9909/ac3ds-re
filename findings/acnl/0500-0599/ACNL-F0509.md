---
id: ACNL-F0509
aliases:
- IDA-opus-5.5-F022
title: 更新データの RomFS は ARCHIVE_ROMFS をファイルパス {5,0,0} で開く（ゲーム自身の開き方）（2026-09-24、MEDIUM（静的＋実機で失敗の側を確認））
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。利用者の報告「0xFA・0xFB はプレビューが無いと通知されるが、置くとモデルがある」。'
date: '2026-09-24'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1217552
- 1167748
- 1270688
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:2399-2410
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F022: 更新データの RomFS は ARCHIVE_ROMFS をファイルパス {5,0,0} で開く（ゲーム自身の開き方）（2026-09-24、MEDIUM（静的＋実機で失敗の側を確認））

解析ソフト: IDA / 解析モデル: opus-5.5。利用者の報告「0xFA・0xFB はプレビューが無いと通知されるが、置くとモデルがある」。

- 0xFA/0xFB = `fobj_barricade_L/R`。モデル・テクスチャ・足元（`Strc/data/fobj_barricade_L.bin`）は**更新データの RomFS にだけある**（生の RomFS で確認）
- 実機（Suspend 中、読み取りのみ）: gohan の RomfsIndex の更新側ハンドルが 0（ARCHIVE_SAVEDATA_AND_CONTENT で更新タイトルを開く方法が失敗）→ base だけを見て「プレビューなし」
- ゲームの開き方: `nnfs_OpenSelfNcchFile 0x129410` が archive 3（ARCHIVE_ROMFS）・空のアーカイブパス・12 B のファイルパスで OpenFileDirectly（ゲームの FS セッション dword_96EF28）。
  **`nnfs_MountUpdateRomfs 0x11D184` がファイルパス {5,0,0}**、`nnfs_MountBaseRomfs 0x1363A0` が {0,0,0}
- → gohan RomfsIndex（ReadFile と索引の Build）もまず {5,0,0} で開く（gohan `0315dc6`）。IDA-opus-5-T024／T025 の答えの候補。実機での成否は未確認
- 同時の修正: 光らせる処理が、動かした直後（実体・モデルの組み立て中）で失敗のままになっていた → 90 フレームやり直す。
  部屋の読み直し後の再開でカーソル・モード・種類を保つ。移動・削除の近さはマンハッタン距離（利用者指示）

