---
id: ACNL-F0437
aliases:
- IDA-gpt-6.1-sol-F014
title: HHD通常室内カメラの連続操作をACNLの家へ移植（2026-10-09、静的MEDIUM、2026-10-10利用者実機PASS）
summary: '2026-10-10追記: 利用者は提示hhd_room_camera1を実機で確認し問題なしと報告。配布版SHA/sourceに対する確認として扱い、端末上のSHAや各個別ケースは再測定していない。F013同梱の確認待ちも解消。新F015追加の確認ではない。'
date: '2026-10-09'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 1718380
- 6873436
- 1403916
- 1389080
tags:
- camera
supersedes: []
source: IDA:work/FINDINGS.md:200-213
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F014: HHD通常室内カメラの連続操作をACNLの家へ移植（2026-10-09、静的MEDIUM、2026-10-10利用者実機PASS）

2026-10-10追記: 利用者は提示hhd_room_camera1を実機で確認し問題なしと報告。配布版SHA/sourceに対する確認として扱い、端末上のSHAや各個別ケースは再測定していない。F013同梱の確認待ちも解消。新F015追加の確認ではない。

解析ソフトIDA（idalib-mcp）/解析モデルgpt-6.1-sol。両原SHA/ARM32 LE/imagebase0/ロード範囲、独立6地点の原命令、保存XMLのT=0を照合。調査→設計保存→実装の順で実施。HHD v1.1 JPN Rev1の通常室内操作を対象とし、撮影専用操作は別経路。

- ACNL `CameraGame_ControlRoomSteps 0x1A386C`はpressedの左右12段階/上下3段階。`CurrentCamera_ControlRoomSteps 0x68E15C`とプレイヤー更新0x64C4A0により状態/入力ゲートを通る。mode0/9/25、room flag0x100、inputBlocked+442、遷移後半がnativeの条件。
- HHD `HhdCameraGame_ControlRoomContinuous 0x156C0C`はheld左右の線形加減速とu16 yaw、held上下の加減速/予測制動とzoom位置[0,3]。4点profile IDs[3,4,5,37]を0x153218→0x5F942Cで自然3次スプラインへ変換し、各乗算のs32 polar切捨てを含むHorner補間を使う。`param.bin`20B×167、`interpolation.bin`16B×63。原float値は表示の丸めと区別した。
- gohan `HhdRoomCamera.cpp`はACNL入力とApplyTargetのMITM。house room flags0x108と0x40/0x80、mode0/25で有効。外観番号なし。player側の入力ゲート、nativeの基準位置/範囲/eye/壁透過を保持。特殊mode/入力UI停止、room/scene変更初期化、OFFで元indexのprofileを再構成。既存屋外FieldCameraの2語目POPとS0も共存検査済み。
- 原HHD ARM1176の493 frame対移植C++/リンクARMは制御stateとY/距離/角が全bytes一致（native回転後のX/Z ±0だけ正規化）。20経路/ライフサイクル条件とR4–R11/D8–D15/SP/S0/native基準追従、158関連関数/9411命令/1742分岐/801PC相対/境界/領域/hash、必須しずえ、新文言の欠字0を確認。
- ACNL17/HHD20関数とglobal等12件のrename、Profile/PMF/補間/CameraPrefix/spline/ModeEntry/入力Enum・型・根拠コメント・stroffを各DBへ反映/保存。所有終了し最新XML/bytes/manifestを出力・hash検証。未確定のHHD UI owner0x4D89D0等は推測renameせず、理由と次の照合をDBコメント/報告へ記録。

作業枝 `work/hhd-room-camera`、配布 `artifacts/plugins/hhd_room_camera1`。F013の壁家具/壁紙床修正を同梱し、利用者の指示により実機確認はカメラ版と一緒に行う。実機未確認なのでmainへ入れない。詳しい根拠/反証/棄却した経路は [設計](../docs/topics/hhd_room_camera_design.md) と [報告](evidence/hhd_room_camera/report.md)。

