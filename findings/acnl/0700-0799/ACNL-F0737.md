---
id: ACNL-F0737
aliases: []
title: "入力の部分型を解析番号の無い名前に統一しメンバー位置を照合"
summary: "入力の基底・Controller・Wrapper・パッド・座標・旗を番号の無い型名に改名した。ゲーム側の独立した書込み・読取りとIDAのメンバー位置を照合し、既知の部分型の範囲とレイアウトを保った。"
date: 2026-10-22
category: input
build: acnl_jpn_v15
confidence: "MEDIUM"
tool: 全関数書き出し / codebytes / IDA型位置検査
addresses: [0x003533D0, 0x0053CDC4, 0x00540870, 0x00542D78, 0x00542E88, 0x00543050, 0x005475D4, 0x00549AB0]
tags: ["button", "touch", "sead"]
supersedes: ["ACNL-F0721", "ACNL-F0723", "ACNL-F0426"]
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

入力の型を次の番号の無い名前に統一する。既存記録の訂正範囲は**型名と部分型である旨の明記だけ**で、各記録の他の結論を取り消さない。
確度 MEDIUM。初期化・入力の書き手・edge生成・Wrapper読取りの独立した静的根拠を照合し、IDAで改名前後の大きさと全対象欄の位置を検査した。実機照合ではない。

## 根拠

| 旧名 | 新名 |
|---|---|
| AcnlControllerPrefixF005 | SeadControllerBasePrefix |
| AcnlControllerPrefixF103 | SeadControllerPrefix |
| AcnlControllerWrapperPrefixF103 | SeadControllerWrapperPrefix |
| AcnlControllerOffsetListF103 | AcnlControllerOffsetList |
| AcnlPadReaderPrefixF103 | AcnlPadReaderPrefix |
| AcnlPadStateF103 | AcnlPadState |
| AcnlPointerFlagsF005 | AcnlPointerFlags |
| AcnlUiPoint2F005 / AcnlUiPoint2IF005 | AcnlUiPoint2 / AcnlUiPoint2I |

Controller系は実在する `sead::ControllerBase`、`sead::Controller`、`sead::ControllerWrapper` の名前をPascalCaseの部分型名に反映した。vtableと初期化の対応は `0x00543058`、`0x0053CF24..0x0053CF30`、`0x00540B44..0x00540B50`。リストの正確なライブラリ型名は未同定なので断定しない。

メンバーの根拠は ACNL-F0721/0722/0723 の既存解析に加え、今回次を一次資料で照合した。

- `SeadControllerBasePrefix`: Init `0x00543050` の初期値書込み、UpdateEdges `0x00542E88` の読書き、SetPointerState `0x00542D78` と装置入力 `0x00540870` が一致する。
- 同型先頭から `pressed/released/repeat=+4/+8/+0xC`、`pointer_flags=+0x10`、`pixel_int=+0x14/+0x18`、`held_frames=+0x2C`、`button_count=+0xFC`、`axis0_bit/axis1_bit=+0x100/+0x104`、`pointer_bit=+0x108`、`idle_frames=+0x10C`、`held=+0x110`、`pixel_float=+0x114/+0x118`、`axis0=+0x11C/+0x120`。位置はcontroller/Wrapperの`base`が先頭なので共通。
- `SeadControllerPrefix`: `base=+0`、`manager=+0x138`、`addons=+0x13C`、`wrappers=+0x14C`。初期化 `0x0053CF3C..0x0053CF64` と Calc `0x0053CDF8..0x0053CEB0` のリスト参照が一致。既知範囲は `0x15C` バイトで派生型全体のサイズではない。
- `SeadControllerWrapperPrefix`: `source=+0x144`、`enabled=+0x148`、`source_bit_index=+0x174`。登録 `0x00549AB0` と利用 `0x005475E4..0x005476EC` が一致。
- `AcnlPadState`: `held/pressed/released=+0/+4/+8`、符号付き16-bit `circle_x/circle_y=+0xC/+0xE`。ReadPadStateの書込みと装置入力の読取りが一致。
- `AcnlPadReaderPrefix`: `previous_held=+8`、`seed_previous_held=+0x30`。`0x00353450..0x00353490` と `0x003534CC` を照合。全readerの確定サイズではない。
- 旗の列挙子は `AcnlPointerFlags_Valid/Pressed/Released/ClearPosition` として型名から始める。

`_local/evidence/109/layout.json` にIDAで取得した型サイズ・メンバー位置・メンバー幅・改名前後の対応を保存した。関数型・コメント中の型参照も揃え、装置入力の引数は `manager` まで使うため `SeadControllerPrefix *` とした。

## 反証条件・未確認点

部分型の先にある派生メンバー、全readerの大きさ、全場面での実体配置は未測定。`Prefix`型の `sizeof` をゲームの確保サイズと解釈してはいけない。
パッドは装置の処理済みキャッシュであり、読み替え前の生HID全体の型ではない。座標型自体には原点や単位を仮定しない。

一次資料は `_local/evidence/109/exports/` の関数先頭アドレス別ファイル。元の全関数書き出しは symbols commit `65293c69e61e182196200b92414beff86f647a98`。対応と SHA-256 は `_local/evidence/109/manifest.json` に保存した。今回、実機操作はしていない。
