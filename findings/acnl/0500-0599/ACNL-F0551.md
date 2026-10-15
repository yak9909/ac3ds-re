---
id: ACNL-F0551
aliases:
- IDA-gpt-6-astra-F003
title: 専用view/projectionで画面固定、pixel配置・倍率・alpha併用（2026-09-20、HIGH）
summary: '解析ソフト: IDA / 解析モデル: gpt-6-astra。replay直後NOP0x4EF1B0へ最小late passを設置。CameraBind0x494D3C(lowCtx,privateSource,1)→DrawMesh0x48D26C(**[0x94CA48]**,mesh,node)→CameraBind(lowCtx,元camera,1)。world登録OFF、global cameraへの書込みなし。sourceのview+328/projection'
date: '2026-09-20'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 4803900
- 4772460
- 9751112
- 9751104
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4118-4125
by: gpt-6
original_by: ''
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-astra-F003: 専用view/projectionで画面固定、pixel配置・倍率・alpha併用（2026-09-20、HIGH）

解析ソフト: IDA / 解析モデル: gpt-6-astra。replay直後NOP0x4EF1B0へ最小late passを設置。CameraBind0x494D3C(lowCtx,privateSource,1)→DrawMesh0x48D26C(**[0x94CA48]**,mesh,node)→CameraBind(lowCtx,元camera,1)。world登録OFF、global cameraへの書込みなし。sourceのview+328/projection+424を初回捕獲して固定し、各eyeの元行列を復元する。core/PSR/VFP/SP、全分岐/LDR/領域、10条件のARM監査を通した。

利用者の20秒移動でgame viewが変わっても私有行列bytesは不変、1200 drawsと前後画像で木の画面位置不変を確認。原点pixel(320,180)/倍率0.6へ変更し右側へ縮小、同位置でalpha128を表示、OFFで消去。counter1480で停止し入口・材質・vtableの原状を読戻し確認。LCD回転はscreen x=200*(1-clip.y/w)、y=120*(1-clip.x/w)。書込み前float32検算を行う。

根拠: `work/evidence/models3d/alpha_screen_20260920/reboot1/` の `screen_audit.json`、`movement_comparison.json`、`screen_placed.png`、`screen_alpha128.png`、`screen_off.png`、`final_restored_state.json`。初版は誤って[0x94CA40]を渡してSIGSEGV、実機caller/chainで訂正し利用者再起動後に成功した。詳細 [alpha_screen_plan](../docs/topics/alpha_screen_plan.md)。反証/制限: 上画面の屋外1種のみ、overlay深度OFF、GPU寿命/場面切替/他材質/下画面/左右目個別画像は未検証。gohan.3gx未統合。

