---
id: ACNL-F0756
aliases: []
title: "下画面のタブ・地図・補助画面は別々の命令と状態遷移で制御される"
summary: "BsMenuTab、地図、manager+488の画面は別のu8命令を使う。タブ状態の切替はcalcのPMFペアを検索し、一致したenterをその場で呼ぶ。"
date: 2026-11-11
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0x6d4444, 0x6d4ee8, 0x6d67f0, 0x81b41c, 0x949d24, 0x949d25, 0x949d29, 0x949d4c, 0x949d88, 0x949718]
tags: ["menu", "layout", "map"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: auto
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

BsMenuTab、地図、manager+488の画面は別のu8命令を使う。タブ状態の切替はcalcのPMFペアを検索し、一致したenterをその場で呼ぶ。

確度MEDIUM。実測なし。各項目について命令列と、独立した呼び元・生成元・消費側またはvtable実データを照合した。

| 番地 | 付けた名前 | 型・プロトタイプ |
|---|---|---|
| `0x006D4444` | `BsMenuTab_WaitUpdate` | `void f(void *tab);` |
| `0x006D4EE8` | `BsMenuTab_MenuOutEnter` | `void f(void *tab);` |
| `0x006D67F0` | `BsMenuTab_TabsInFinishUpdate` | `void f(void *tab);` |
| `0x0081B41C` | `BsMenuTab_ChangeState` | `void f(void *state_machine, unsigned int calc_function, int calc_adjustor);` |
| `0x00949D24` | `g_BsMenuTabCommand` | `unsigned __int8` |
| `0x00949D25` | `g_BsMenuMapCommand` | `unsigned __int8` |
| `0x00949D29` | `g_BsMenuSubscreenCommand` | `unsigned __int8` |
| `0x00949D4C` | `g_BsMenuMgr` | `void *` |
| `0x00949D88` | `g_BsMenuTabCloseSelectionFlag` | `unsigned __int8` |
| `0x00949718` | `g_BsMenuBg` | `void *` |

## 根拠

- ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名はsymbolsを併読。原本code.binのSHA256はbuild台帳と一致。命令列は `tools/codebytes.py` の読取関数とCapstoneで独立照合した（`_local/evidence/146/original_asm.txt`）。型・vtable・表の原本値は同所 `bytes.json` と追加検算。作業用IDBで実測はしていない。
| 対象 | 命令列・呼び元の根拠 |
|---|---|
| 0x949D24 | BsMenuTab_ConsumeCommand 0x6D3F04がLDRBで保存→STRBで11へ戻す。7はAllTabsOut、3はMenuOut。2は通常MapSyncTabsInだが部屋フラグにより別経路もある。 |
| 0x949D25 | BsMenuMgr_ProcessMapCommand 0x6D1428がLDRBで読み、0→退場、1→profile0x219作成/入場、2→待機。処理成立時にSTRB 2。0を毎フレーム必ず消費するとは限らない。 |
| 0x949D29 | 0x6D1E14が同じ0/1/2を読み、1はUiScreen_OpenById(0x261,this,0)を+488へ、0は+488の実体へ0x2257E8を呼ぶ。0x6D6440が地図とは別に退場0を書き込む。 |
| 0x949D4C | BsMenuMgr_Init 0x6D3144がthisを公開。+480にprofile0x218、+484/+488を0、+500にprofile0x216を保存し、状態名BsMenuMgrを設定。getter0x6D1198もこの大域値を返す。完全型は無いためvoid*。 |
| 0x949D88 | TabSelectUpdateの0x6D48F4〜0x6D4928は選択indexが10、またはindexが0で以前のindexが-1以外なら1を書く。MenuOutUpdateの0x6D4E80/88と0x6D4D8C/0x6D7B9Cが0へ戻す。型u8。汎用メニュー表示フラグとは断定しない。 |
| 0x949718 | BsMenuBg_InitStep 0x6944DCはmvmnt_undscrnの二枚のLayoutと状態名BsMenuBgを作ってthisを保存。0x6947A8でクリア。MenuOutUpdate0x6D4E94/98は値をBsMenuBg_StartLeaveへ渡す。型void*。 |
| 0x6D4444 | 原本命令はBX LRのみ。下記状態表のstate0 calcにも一致。型void(tab*)。 |
| 0x6D4EE8 | state6 enter。選択ボタン解除要求、+6427=10、手カーソルHide、MENU_FLAGS ORR #0x20、+6576 bit0、+6422=0。相方MenuOutUpdate0x6D4E5Cが退出/メニュー空を待つ。 |
| 0x6D67F0 | state7 calc。0x6D67F8でUpdateEnter、MENU_FLAGS bit2確認、+4493/+4881=1、メニューフロー完了通知、0x20解除、+6422=1/+6427=-1、0x6D688CでTabSelectへ遷移。 |
| 0x81B41C | 引数はsm=tab+20,calc関数,PMF調整語。sm+28の表をsm+32件、20byteずつ走査。entry+12/+16と引数ペアを比較。0x81B4C4/CCで現在calcを保存、entry+4/+8のenterを0x81B51Cで即時BLX。調整語のbit0で仮想PMFも分岐。 |

- 原本の状態表baseは0x8508FC。20byte行 `{name,enter,adjustor,calc,adjustor}`。state0のcalc欄0x850908=0x6D4444、state6のenter欄0x850978=0x6D4EE8/calc=0x6D4E5C、state7のcalc欄0x850994=0x6D67F0。アドレス計算と値はevidenceのスクリプトで検算。
- `ACNL-F0466`（S）、F0473（S）、F0593（S）を既存の手がかりとして使用し、上の生産/消費双方を再確認。新しい命名の確度は実測を増やしていないのでMEDIUM。
- 旧版 `GameList.cpp:27〜43,738〜755`。大筋は一致。ただしcommand2の地図同期は全室共通ではない。+488の実クラスは未確定なので名前はSubscreenに限定。CloseSelectionFlagは観測したset/clear用途に限定。0x81B41Cは無条件の関数ポインタ差替えではなく、登録表のPMFペア一致が必要。

- 参考資料は依頼指定の旧版gohan（`_local/legacy-src/gohan-legacy/Sources`、出所は依頼文、台帳の既存キー無し）。未検証の手がかりとして用途を対比し、上記一次証拠を根拠とする。旧版本文を証拠の代わりにしない。

## 反証条件・未確認点

- 実機での状態遷移は追試していない。全タブが閉じる場合の入力条件、+488の実クラス、CloseSelectionFlagの全ての用途は未確認。
- 上記生産/消費の値やvtableが別オブジェクト・別型を指すと判明した場合は再検討する。新しい実機確認やゲーム挙動の保証は含めない。
