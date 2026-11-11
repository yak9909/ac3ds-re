---
id: ACNL-F0761
aliases: []
title: "タッチ状態の実体と ControllerMgr のポインタは別で、座標系も異なる"
summary: "0xACF6E0は40バイトのタッチ状態そのもの、0x96F2ECはsead::ControllerMgrへのポインタ。Controllerの画素座標からタッチ状態の中央基準座標を作る。"
date: 2026-11-11
category: input
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0xacf6e0, 0x96f2ec]
tags: ["touch", "button", "sead"]
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

0xACF6E0は40バイトのタッチ状態そのもの、0x96F2ECはsead::ControllerMgrへのポインタ。Controllerの画素座標からタッチ状態の中央基準座標を作る。

確度MEDIUM。実測なし。各項目について命令列と、独立した呼び元・生成元・消費側またはvtable実データを照合した。

| 番地 | 付けた名前 | 型・プロトタイプ |
|---|---|---|
| `0x00ACF6E0` | `g_TouchState` | `AcnlTouchState` |
| `0x0096F2EC` | `g_SeadControllerMgr` | `SeadControllerMgrPrefix *` |

## 根拠

- ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名はsymbolsを併読。原本code.binのSHA256はbuild台帳と一致。命令列は `tools/codebytes.py` の読取関数とCapstoneで独立照合した（`_local/evidence/146/original_asm.txt`）。型・vtable・表の原本値は同所 `bytes.json` と追加検算。作業用IDBで実測はしていない。
| 対象 | 根拠 |
|---|---|
| 0xACF6E0 | 0x1B6B84はアドレスをTouch_UpdateState0x1B7874へ渡す。0x1B7874は+0/+1をu8、+2..+12を16bit、+14/+15をu8、履歴を+16..+29、floatを+32/+36へ保存。独立した0x1B7A48はprevious held/changed(+26/+27)を読む。構造体型AcnlTouchState、ポインタではない。 |
| 0x96F2EC | 0x540488がsingletonへthisを公開し+188を設定、0x540748/0x540788がvtbl_sead_ControllerMgrへ戻し大域値をクリア。GameInput_IsMaskPressed0x520D4CとGetTouchPixelPosition0x520DECはmanager+208のcountと+216のtableから先頭SeadControllerPrefix*を引く。BsMenuMgr_Init0x6D3144も同じtableをControllerWrapperへ結ぶ。 |

- `0x1B7990〜0x1B79BC` はfloat `(position_x-160,120-position_y)` を+32/+36へ保存。Controller+276/+280の画素座標と同じ値ではない。
- `AcnlTouchState`は+30/+31を未解明のまま残す。+16以降は単純な前40byteコピーではなく、前のstart/position/counters/held/changed/raw_yを上記順に詰める。
- `SeadControllerMgrPrefix`は+208のu32 count、+212は未解明4byte、+216の `SeadControllerPrefix **controllers` までを型付けした220byteの部分型。Controller本体は既存型のため新しく重複定義しない。
- 旧版 `GameList.cpp:367,420,423` の構造体/ポインタ用途は一致。名前の「システムの何か」はControllerMgrまで特定。履歴の配置と中央基準の座標を明示する。

- 参考資料は依頼指定の旧版gohan（`_local/legacy-src/gohan-legacy/Sources`、出所は依頼文、台帳の既存キー無し）。未検証の手がかりとして用途を対比し、上記一次証拠を根拠とする。旧版本文を証拠の代わりにしない。

## 反証条件・未確認点

- ControllerMgrの全体サイズと+212の意味は未確認。入力の置換・復元や割込みとの競合は今回の解析対象でない。実測なし。
- 上記生産/消費の値やvtableが別オブジェクト・別型を指すと判明した場合は再検討する。新しい実機確認やゲーム挙動の保証は含めない。
