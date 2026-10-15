---
id: ACNL-F0464
aliases:
- IDA-opus-5.5-F069
title: '住民の AI（第 2 段まで）— 行動の要求・行動表・外の住民のクラス・家の出入り・花植え・傘（2026-09-29、MEDIUM: 静的＋Vapecord の使い方と一致。実機未観測）'
summary: '解析ソフト: IDA（主 IDB acnl、CRO の ELF の IDB outdoor）＋ Vapecord の NPC 機能 / 解析モデル: opus-5.5。'
date: '2026-09-29'
category: actor
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 9381904
- 9201448
- 9378600
- 9790444
- 7234848
- 7233760
- 7234644
- 8890872
- 7245640
- 7245728
- 7245812
- 7244132
- 7245464
- 7245572
- 7253280
- 7251072
- 7261556
- 7261348
- 7259716
- 7253164
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:1410-1469
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F069: 住民の AI（第 2 段まで）— 行動の要求・行動表・外の住民のクラス・家の出入り・花植え・傘（2026-09-29、MEDIUM: 静的＋Vapecord の使い方と一致。実機未観測）

解析ソフト: IDA（主 IDB acnl、CRO の ELF の IDB outdoor）＋ Vapecord の NPC 機能 / 解析モデル: opus-5.5。
利用者の依頼: 住民の AI（家に入る・出る・花を植える・傘を差す等）を完全解明し自由に操る。**この記録は第 1 段（地図づくり）**。
- **クラス**: 外の住民 = ModuleOutdoor.cro の **AcNpcOut**（RTTI、vtable 0x00B98138 は cro_to_elf の便宜番地）→ 基底 AcNpcNml（main vtbl 0x8F2810、TypeInfo 0x8C6728）→ AcNpc（0x8F1B28）。
  家の中 = ModuleIndoor の AcNpcIn、商店街 = ModuleNpcDt の AcNpcDt。ModuleOutdoor に A*（NpcOutAStarForeachCB ほか）・道の探索（NpcOutMacroRoadSearchCB）・
  徘徊先の候補（WanderSearchMaxMinCandCB）・家の表札の会話（NpcHousePlateTalkRecept）。名前付き状態表（cro_state_tables.py の形）は ModuleOutdoor に無い。
- **住民の実体の取り方**（Vapecord NPC::GetData。USA→JPN は Addresses.hpp の 5 列目）: *(0x9563EC) + 0xD00C から連結。+0x14 位置、+0x2E 向き、**+0x78 = NpcAction**。
- **行動の要求** 0x6E6520（Vapecord NPCCODES_FUNC1）: NpcAction+1140 に行動番号（u8、29 = 無し）、+1141 に優先度。まだ要求が無いか、優先度が今の要求以上のときだけ受ける。
  引数 +1144..（目標の xyz・float・u16×2・u8・u64）。**NpcAction_ConsumeRequest 0x6E60E0** が、優先度 ≥ 実行中の優先度（+1245）なら 17/18 = 持ち物の差し替え、
  19 = 体の +640 bit5 を sub_205218 / sub_204A9C で切り替え（傘の開閉の見込み・LOW）、21 = sub_6ABC18 / sub_6ABD08 を行い、引数を +1196.. へ写して
  **NpcAction_ChangeAction 0x6E6454**（+48 = 今の行動、+52 = 行動表の項目、前の項目の終わり +24 → 新しい項目の始め +0）。要求は毎回消す。
- **行動表 0x87A9F8**: 29 項目 × 32 B（メンバ関数ポインタ 4 つ: 始め・?・?・終わり）。要求する小関数（main）: 0 = 0x6E8F48、1 = 0x6E8FA0（Vapecord が
  この中の BL 0x6E8FF4 をフックして住民の移動を止める = 1 は移動）、2 = 0x6E8964、3 = 0x6E8E98、4 = 0x6E8F04、5 = 0x6EAD20、6 = 0x6EA480、8 = 0x6ECD74、9 = 0x6ECCA4、
  11 = 0x6EC644、12 = 0x6EACAC（Vapecord「感情」）、13 = 0x6E9B50（Vapecord「歩き・走りのアニメ」0xE/0xF）、14 = 0x6ECE58、16 = 0x6E9698、17 = 0x6E9AC8、
  18 = 0x6ECF44（Vapecord「持ち物」）、19 = 0x6ECFCC、21 = 0x6EABB4、22 = 0x6EC6A4、23 = 0x6ECD10、24 = 0x6EC5E0、25 = 0x6EC398、26 = 0x6EAC2C。
  USA→JPN の差はどれも 0x1834（NPCCODES_FUNC1〜4 の 4 本で同じ）→ Vapecord の止めるフック USA 0x6EA828 = JPN 0x6E8FF4（行動 1 の要求の BL）と一致。
- **上の層**: ModuleOutdoor は上の小関数を 29 本取り込み（imports）、呼ぶのは主に 0xB65000〜0xB78000 と 0xB30000〜0xB41000 の関数（例: 行動 19 を sub_B74504 が 2 回）。
  「家に入る・出る・花を植える・傘」はこの層が行動を組み合わせて作っていると見込む（未確認）。
- IDB: NpcAction_ConsumeRequest / NpcAction_ChangeAction / NpcAction_Ctor を命名、0x6E6520・0x87A9F8 に注記。ModuleOutdoor の ELF は work/cache/cro_elf/ModuleOutdoor.elf（.i64）。
- 次: 各行動の中身（使うアニメ）と上の層の関数の意味を静的に割り当て、実機で「行動番号の変化」を記録して見た目と突き合わせる。
- 反証条件: 実機で要求しても行動番号（+48）が変わらない、Vapecord の止めるフックが別の行動番号の要求に掛かっている。
- **追記（2026-09-29、第 2 段: 静的のみ。利用者指示「静的に解析してください」— 家の出入り・花植え・傘は稀で操作もできないので実機記録は取らない）**
  確度: 下の各項目は **MEDIUM**（逆コンパイル＋逆アセンブル＋アニメ名・効果音名・アイテム名の表という独立した一次データの一致）。実機未観測。
  番地のうち 0x00B… は ModuleOutdoor.cro を cro_to_elf で ELF にしたときの便宜番地（.text 先頭 = 0x00B00000）。実機ではロード先 + (番地 − 0xB00000)。
  道具: tools/patches/npcout_selectors.py（行動を切り替える箇所と呼び出し元・表の全列挙 → work/evidence/npc_ai/npcout_selectors.txt）、
  npcout_steps.py（手順の表の抽出。表の範囲の誤りを直した → npcout_steps.txt）、outdoor_dis.py（取り込みとデータ取り込みの番地を名前つきで注記する逆アセンブル）。
  - **二層構造**: 下 = main の NpcAction（29 の「動作」: 歩く・アニメ・持ち物…）。上 = ModuleOutdoor の **ふるまい表 0x00B8DFF4（51 項目 × 24 B = {始め, 毎フレーム, 手順の進め役}）**。
    制御の構造体 = 住民の実体 + 0x1334（4916）。+0x1960 = 実体、+0x1964 = 目標（xyz）、+0x1975 = 今のふるまい番号、+0x1978 = 待ち、+0x197C = 待ち、+0x19A0 = 花の区分、+0x19A4 = 手順番号。
    ふるまいを変えるのは **sub_B4109C(制御, 番号)**（前の項目の後始末 → 新しい項目の [0] を呼ぶ）。手順の進め役は「+0x19A4 < n なら表[+0x19A4] を呼ぶ」形が多い。
  - **ふるまい 0 = ふだん（うろうろ）** の手順 sub_B69C64 が毎フレーム順に見る: ①sub_B3F434（優先の割り込み: 部屋 0x5E の特別処理 → 32、町の条件で 6 択表 0x00B8E504、
    単独プレイなら 7 択表 0x00B8E534 → sub_B3F928）②sub_B6B45C ③**sub_B67670（目的地に着いたか）** ④実体 +0x868 の bit → 1 ⑤持ち物の見直し（下の傘）⑥どれも無ければ徘徊（動作 1 歩く / 2 走る、次まで 60〜179 フレーム）。
  - **次の目的（実体 +0x4651 = 18001）を決める sub_B66148**: 「家へ帰る時間か」sub_B405D4 が真なら **1 = 家へ帰る**（+0x4650 = 1）。そうでなければ乱数で
    0 = ただ歩く / 2 / 5 = **特別なことをする**（sub_B403D4 の 9 択）。+0x4652/+0x4653 = 目的のマス。着いたら sub_B67670 が目的ごとに:
    1 → **sub_B69398 → ふるまい 3（家に入る）**、3 → プレイヤーのいるマスなら会話の予約（sub_B40E48(…,19)）、4 → 12/31 23:59 ならふるまい 43（年越し）。
  - **家に入る = ふるまい 3**（手順: sub_B75764 → sub_B734FC/sub_B73500 = 持ち物があれば動作 18 で片付け、無ければ**動作 25 アニメ 0x30 door_in1** → sub_B76310 → sub_B729E4）。
    入る条件 sub_B69398: 実体 +0xB06 bit0、sub_B405D4、家の入口のマス（sub_7519C4 の結果と一致・y + 1）、g_BsStrcMgrCreateStep == 0xFF かつ g_BsStrcMgr がある、sub_6DD6B4 / sub_577E90 が真。
  - **家から出る = ふるまい 5**（手順 sub_B6C174 = **動作 26 アニメ 0x32 door_out1** → sub_B6AE24）。5 へ切り替える箇所は定数で渡していない（npcout_selectors の「?」の 24 箇所のどれか）→ **LOW**、未特定。
  - **特別なことの 9 択 sub_B403D4**（候補表 0x00B8E4BC、残りの候補を制御 +0x30 のビット集合で持ち、済んだ物を消す。済んだ数（9 − 残り、+0x38）が 5 以上なら選ばない（集合を戻す時期は未確認）。多人数プレイでは選ばない）:
    0 sub_B6F7D4 → 45 / 1 sub_B69528 → 22 / 2 sub_B69AA0 → 28（水やり jyoro_raise1）/ 3 sub_B6F668 → 29（草むしり pickup_weeds1）/
    **4 sub_B6E4F4 → 30（花を植える）** / 5 sub_B6B1D4 → 23（木を揺する tree_shake_wait1 → tree_shake1、sub_5961B0 = 揺すった木の処理）/ 6 sub_B6B110 → 31 /
    7 sub_B6F4A8（道具を片付ける → 21）/ 8 sub_B6AEE4（あみ 0x3351・つりざお 0x3355・スコップ 0x3359・じょうろ 0x335D を 1/4 ずつ乱択して持たせる → 21）。
  - **花を植える = ふるまい 30**。選ぶ条件 sub_B6E4F4: 部屋 0x5E でない・手ぶら・**周り 8 マス（半径 1.25 → 1）に花がある**（判定 sub_B02F50 = sub_768364 が真で区分が 16/17/18/20 以外、
    sub_B3F728 が乱択して目標を制御 +0x1964 へ）→ その花の区分を制御 +0x19A0 へ → 住民の向き（vc_ADDR2）から隣の 2 マス（表 0x00B8DFD4 / 0x00B8DF44）のうち
    空き・Field_CanPlantFlowerAt・sub_613688 が真のマスを乱択。手順: 動作 4（近づく）→ 動作 13 アニメ 0x1A（表の名前は menu_think1）→ **sub_B70788: sub_114B84(品物, 区分) で花を作り
    sub_596F10(品物, x, y) で置く**（FieldObj_ApplyDigRecord 0x23 → sub_599FBC）。**植える花 = 隣の花と同じ種類の基本 3 色から乱択**（表 0x008888D6、u16 × 3 × 6）:
    区分 11 チューリップ 0x9F/0xA0/0xA1、12 パンジー 0xA6/0xA7/0xA8、13 コスモス 0xAC/0xAD/0xAE、14 バラ 0xB2/0xB3/0xB4、27 ユリ 0xBE/0xBF/0xC0、28 スミレ 0xC4/0xC6/0xC7（ほかの区分は植えない）。
  - **傘**: main の **sub_10E388(町 + 4, 住民番号)** が「住民が今持つべき物」を決めて住民データ（1 人 0x2518 B）の **+0x8E6（持ち物）** を書く（0 = 対象外、1 = 同じ、2 = 変えた）。
    行事（sub_308EC0 の番号 12 = あみ 0x3351、0 = つりざお 0x3355、16 = 0x338E）、それ以外で sub_30B9FC == 3（特別な枠に入っていない）かつ **sub_22A14C() > 0（天気 sub_62E60C が 3 → 32、4 → 128 = 降っている）**
    なら **住民データ +0x24AA（その住民の傘）**、降っていなければ空（持っている傘を外す）。ModuleOutdoor は ふるまい 0 の⑤で sub_10E389 を呼び、
    **sub_B3FA38 が「手の物（実体 vtable +0x164）≠ 住民データ +0x8E6」ならふるまい 21**（始め sub_B6C830 = 実体 +0x46AC へ写して **動作 18（持ち物、0x6ECF44）**）。
    動作 18 の中 sub_6EB3D0: 品物の区分が **25（傘）なら アニメ 67 umb_open1 と SE_ACT_UMBRELLA_OPEN（0x10005D9）**、片付けは 0x6EAF64 の SE_ACT_UMBRELLA_CLOSE。
  - **落とし穴 = ふるまい 7**（sub_B78674: sub_597FB4 が真 → 7。手順 = 動作 16 アニメ 0xD5 pitfall_fall1＋SE_ACT_HOLE_TRAPPED、0xD6/0xD8 pitfall_fall2＋SE_ACT_HOLE_FALL_IN）。第 1 段の「1 = 落とし穴」は誤り。
  - **ふるまい 46** = 節分: 0x338F（good-luck roll）を持たせて動作 18（sub_B741F8）。
  - **自由に操る入口（静的な見込み。どれも実機未確認）**: (a) 傘・道具 = 住民データ +0x8E6 に品物を書けば sub_B3FA38 が 21 → 動作 18 で持ち替える（傘なら開く）。
    ただし sub_10E388 が毎フレーム天気で上書きするので、雨でない日に傘を持たせ続けるには sub_10E388 の結果か sub_22A14C を変える必要がある。
    main だけで済ませるなら vc_NPCCODES_FUNC4 0x6ECF44(実体 + 0x78, 優先度, &品物)。(b) ふるまいを直接 = sub_B4109C(実体 + 0x1334, 番号)（ModuleOutdoor のロード先が要る）。
    (c) 家へ帰す = 実体 +0x4651 = 1 と目的のマス（+0x4652/+0x4653）。(d) 花を植えさせるだけなら sub_596F10(品物, x, y) を main から呼べる（動作は伴わない）。
  - 反証条件: 雨の日に住民データ +0x8E6 が傘にならない、ふるまい 30 の後に植わる花が隣と違う種類、家に入るとき +0x1975 が 3 にならない。

