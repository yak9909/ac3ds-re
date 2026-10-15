---
id: ACNL-F0621
aliases:
- IDA-opus-5.5-F105
title: '模様替え UI のドラッグ・離す・チップと家具の記録の関係（2026-10-07、MEDIUM: 静的のみ。ModuleIndoor.elf / ModuleFtr.elf と主 IDB）'
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。T022（ゴミ箱・家具リスト）の前提。番地は cro_to_elf の便宜上の基準（text 0x00B00000）。名前は work/cache/cro_elf の両 IDB に付けた（キャッシュは再生成で消えるのでここが正）。'
date: '2026-10-07'
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 1376692
- 1376716
- 1376696
- 1377480
- 1798684
- 5818324
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4847-4875
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0623"]
---
## IDA-opus-5.5-F105: 模様替え UI のドラッグ・離す・チップと家具の記録の関係（2026-10-07、MEDIUM: 静的のみ。ModuleIndoor.elf / ModuleFtr.elf と主 IDB）

解析ソフト: IDA / 解析モデル: opus-5.5。T022（ゴミ箱・家具リスト）の前提。番地は cro_to_elf の便宜上の基準（text 0x00B00000）。名前は work/cache/cro_elf の両 IDB に付けた（キャッシュは再生成で消えるのでここが正）。
- **Chip のドラッグ** `Chip_Drag_Calc` 0xB422C4（ModuleIndoor、状態表 0xB62778 の Drag）: 毎フレーム g_FtrMgr（ModuleFtr seg2+0x48 = ELF 0xB47A14）に対し、チップ +1114（まとめて掴んでいる）? `FtrMgr_DragGroup` +0x6E44 : `FtrMgr_DragSingle` +0x8D8C（引数 R1 = チップ +1084）。
  指が離れた（vc_CONTROLLERINPUTCHECK(0x8000) が 0）かつ +1113 なら +1114 ? `FtrMgr_DropGroup` +0x7108 : `FtrMgr_DropSingle` +0x9058 → Drop 状態（0xB42450）+ 音 0x1000524。**ゴミ箱の割り込みはこの分岐（0xB42348〜0xB4239C）の手前**。
- **ModuleFtr の管理（g_FtrMgr）**: +4246 = 掴んでいる数（1 = 単体は +20 に記録、2 以上 = +1996 から 20 B x 最大 112）。`FtrMgr_DropSingle` は置けたら sub_B1CD48 で確定、置けなければ元の位置へ戻し、+20〜+39・+4236〜+4244 を消す。`FtrMgr_DropGroup` は置けなければ `FtrMgr_RestoreGroup` 0xB07FEC（全部元へ）。音 0x1000525 / 0x1000526。
  掴み始め: Select 状態が +0x84E8（まとめ）/ +0x76C4、まとめへの追加 `FtrMgr_AddToGroup` +0x7608（Chip_AddToGroup 0xB43330 から）。回転 `FtrMgr_Rotate` +0x9518。
- **家具の記録**（ModuleFtr .bss、112 x 32 B。+4 = 家具の番号 → g_RoomFtrObjects、+8 = もう 1 つの参照、+24 = 親の記録の番号、+25 = チップ側の番号、+26/+27 = 状態）:
  登録 `FtrRec_RegisterAcFtr` +0x1CF44 は **AcFtr_CreatePrepare が 0x1501B4 経由で呼ぶ**、解除 `FtrRec_UnregisterAcFtr` +0x1D14C は **AcFtr_DestroyBegin が 0x1501CC 経由で呼ぶ**（家の中のみ、Room_HasFlags(8)）。生きているか = `FtrRec_IsAlive` +0x1EDEC。
  → 家具を AcFtr 状態 6 で消すと記録は**自動で外れる**。リストから出した家具も記録は**自動で付く**。
- **チップ**（ModuleIndoor、エディター +1176 から 1,120 B x 112）: 作るのは**エディターの In の入口だけ**（`Editor_CreateChips` 0xB3CC08 = 生きている記録ごとに空きチップ（+1117 == 0）へ `Chip_Setup` 0xB43160(チップ, エディター+76, 記録)、そのあと上に載った物を親チップへ結ぶ）。
  毎フレームの位置合わせ `Chip_SyncPosition` 0xB2EE88 は記録が死んでいれば何もしない（チップは残る）。チップを外す = 状態 Out（`Chip_Out_Enter` 0xB430E4 / `Chip_Out_Calc` 0xB4304C: アニメ 14 を流し終えたら描画から外し +1117 = 0）。状態の切り替えは `StateObj_ChangeByCalc` 0xB2ED80(obj, calc, 0)。
  → **ゴミ箱で消した家具のチップは自前で Out にする必要がある。リストから出した家具のチップは自前で Chip_Setup する必要がある**（ゲームは開いている間に作り直さない）。
- 主 IDB: 0x1501B4 / 0x1501CC を命名・注記。
- 未確定: ゴミ箱で離したときに ModuleFtr の掴み状態をどう片付けるか（Drop を呼ばずに消すと +4246 等が残る。戻す経路を通してから消すか）。gohan のフレームの相乗りと ModuleIndoor の更新の順序。CRO の実行時のロード先（gohan からチップの関数を呼ぶため）。
- 追記（F105、2026-10-07、静的）:
  - エディター本体 = `g_InteriorEditor`（ModuleIndoor seg2+0x4BC、ELF 0xB8E18C）。`Editor_Setup` 0xB3DD6C（chip.arc を読み N_Room_00 の原点を取った後）で書き、`Editor_Teardown` 0xB3E048（全チップ Chip_Release の後）で 0。ModuleFtr もこれを読む（seg2+0x4BC の取り込み 9 か所）。チップは g_InteriorEditor + 1176 + 1120 × i。
  - チップの指: +1068/+1072 = 押し始めた点、+1084/+1088 = いまの点（float、画面座標）、+1076/+1080 = 前の点（`Chip_Select_Calc` 0xB429BC）。6 フレーム未満かつ 24.0 未満の移動ならまだ掴まない。+1114 = まとめて掴む（Chip_AddToGroup）。
  - **CRO の実行時の先頭の求め方**（静的、未実機）: 本体の取り込み口（`LDR PC,[PC,#-4]` + 語）の語はロード時に CRO の実番地へ書き換わる（static.crs の匿名取り込み、tools/patches/crs_import_slots.py）。
    ModuleFtr の先頭 = [0x1501B8] − 0x1CF44（FtrRec_RegisterAcFtr）、ModuleIndoor の先頭 = 一覧の任意の口（例 [0x1504C8] − 0x52A4）。モジュールが無いときの値は未確認なので、先頭の命令語を照合してから使う。
- 追記（F105、2026-10-07、静的）: **チップの指の欄は触れている間だけ書かれる**。`Chip_Update` 0xB2F7C0（エディター Neutral 0xB3D1E4 が毎フレーム全チップに呼ぶ）: vc_CONTROLLERINPUTCHECK(0x8000) が真のときだけ sub_74F3FC で指の点を +1084/+1088 に書き、そのあと状態の calc を呼ぶ。
  ModuleFtr 側の読み手 sub_B147EC / sub_B140D4 は +1084 を読むだけ（部屋の原点 エディター+129568 と 1 マス +129560 で世界座標へ）。掴み始めの世界座標は g_FtrMgr +40 に押し始めの点 +1068 から作られる（FtrMgr +0x84E8 / sub_B140D4）。
  → 離したフレームの Drop は**最後に書かれた +1084** を使う。gohan の相乗り（0x1B721C、描画フェーズ = その フレームの計算の後）で +1084 を押し始めの点 +1068 にしておけば、触れている間は次の Chip_Update が上書きし、離したときだけ「押し始めの点で離した」= 元の位置へ戻る（静的。未実機）。
  - 音: ModuleIndoor / ModuleFtr の Game_PlaySound は本体 0x58C7D4 を通る（取り込み表）。離す 0x1000524（Chip_Drag_Calc）、戻す/置く 0x1000525・0x1000526（FtrMgr_Drop*）。
- 訂正（F105、2026-10-07）: 模様替えの音の番号を暗算で 0x1000424〜26 と書いていた。Python で換算し直すと 16778532 = **0x1000524 SE_SYS_FUR_OFF**（Chip_Drag_Calc の離す）、16778533 = **0x1000525 SE_SYS_FUR_PUT**（同じ位置に置いた）、16778534 = **0x1000526 SE_SYS_FUR_BACK**（元へ戻した）、16778535/36 = SE_SYS_FUR_POLY_MOVE / _OUT（reference/old_project/SOUND/index/sounds.csv）。上の記述は直した。
- 追記（F105、2026-10-07、静的）: エディターの状態は In(0xB3D678) → CommonButtonIn(0xB3DC48)（sub_B315E0 が偽のとき）→ Neutral → CommonButtonOut(0xB3DCA0) → Out。
  チップのレイアウトの優先度（Layout+12 = チップ +48）は普段 6、掴んでいる間 7（`sub_B2EBB0`(チップ, 掴む?) が一緒に動くチップ +1036/+1044 にも同じ値を書く。Drag の入口 0xB42500 が 1 で呼ぶ）。
  HHD の開いた缶の絵 my_min_Trash_01/02 は BFLIM の swizzle 8（保存が転置）、閉じた絵 00 は 0。絵の差し替え（CLTP）では UV で直せないので、画素を転置して書き直す（tools/hhd/make_decorate_arc.py upright）。

