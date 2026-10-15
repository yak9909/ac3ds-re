---
id: ACNL-F0436
aliases:
- IDA-gpt-6.1-sol-F015
title: リスト背景のフェードと模様替えカメラpan（2026-10-10、MEDIUM、本体非表示はF016で訂正）
summary: 解析ソフトIDA（idalib-mcp）/解析モデルgpt-6.1-sol。原SHA/ARM32 LE/imagebase/ロード範囲・独立した入口命令を確認し、実装前に[設計](../docs/topics/catalog_camera_controls_design.md)を保存。利用者が前版hhd_room_camera1を実機PASSと報告した後の追加要望。
date: '2026-10-10'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:190-199
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F015: リスト背景のフェードと模様替えカメラpan（2026-10-10、MEDIUM、本体非表示はF016で訂正）

解析ソフトIDA（idalib-mcp）/解析モデルgpt-6.1-sol。原SHA/ARM32 LE/imagebase/ロード範囲・独立した入口命令を確認し、実装前に[設計](../docs/topics/catalog_camera_controls_design.md)を保存。利用者が前版hhd_room_camera1を実機PASSと報告した後の追加要望。

- CameraGame_UpdateEyeの原ARMとsin/cos表から水平forward=(-sin(yaw),-cos(yaw))、right=(cos(yaw),-sin(yaw))を確定。R0角/S0 floatのABIをDBへ修正。cameraのtarget+36/eye+48も型へ反映。
- ModuleIndoorのSubmit＋本体のmatrix/draw経路より、editor+664、chip+1176+i*1120+36（112枠）、range+128200+36のLayoutと子リングを照合。全paneの描画用globalAlpha+181を入口MITMで一時乗算/復元し、localAlpha/親/flags/アニメを維持。容量4096/深さ64超過は全復元してnative描画。Scene/owner不一致は適用除外。
- Xは最後に成功したリストを押下edgeで開く。既存Bを保持。カテゴリ行の音はSE_SYS_BOOK_ICON_SELECTED、上段は現行のまま。panは利用者指定どおりHHDカメラON＋実模様替えUI＋mode25だけ、X/Zのみ、list/menu/禁止で停止。通常mode0のnative追従を保つ。
- 原ARM Eye対実C++とlinked pan63条件、HHD493frame/20条件、fade24条件で全pane184Bの復元、X/B/音7条件、170関数の全分岐/リテラル/ABI/領域/hash・必須しずえ・新字形を確認。根拠は[report](evidence/catalog_camera_controls/report.md)。OS/GPUを模擬する部分は実機確認に昇格しない。
- 2関数/1表rename、Pane/Layout/trigの部分型、cameraメンバーとVFP型、音ID Enum/PlaySound引数型、周辺コメントを保存し所有終了。音IDは現行GardenSoundのSTRGと旧参照CSVへ照合（旧script未実行）。mainとModuleIndoorの最新XML/bytesを出力し保存読戻しPASS。owner不明のUI wrapper/PMF dispatcherは既存名を維持し、次のRTTI/constructor照合をDBに記録。

