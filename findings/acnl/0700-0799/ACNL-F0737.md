---
id: ACNL-F0737
aliases: []
title: "入力の部分型を解析番号の無い名前に統一しメンバー位置を照合"
summary: "入力の型名と欄の型を整理し、pointer_flagsを4バイトのunsigned intにした。現在の宣言を派生側のARMコンパイラで検証し、enumサイズの設定によらず8構造体の全メンバー位置・大きさがIDAと一致した。"
date: 2026-10-22
category: input
build: acnl_jpn_v15
confidence: "MEDIUM"
tool: 全関数書き出し / codebytes / IDA型位置検査 / arm-none-eabi-g++
addresses: [0x003533D0, 0x0053CDC4, 0x00540870, 0x00542D78, 0x00542E88, 0x00543050, 0x005475D4, 0x00549AB0]
tags: ["button", "touch", "sead"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6.1-sol
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

入力の型を次の番号の無い名前に統一する。既存記録の更新範囲は**型名・欄の型と部分型である旨の明記**で、入力の計算・旧状態の扱いなどの結論を取り消さない。
型名の更新の対象: F0721・F0723・F0426（結論は有効）。
確度 MEDIUM。初期化・入力の書き手・edge生成・Wrapper読取りの独立した静的根拠を照合し、IDAと派生側のARMコンパイラで全対象欄の位置・大きさを検査した。実機照合ではない。

## 根拠

| 旧名 | 新名 |
|---|---|
| AcnlControllerPrefixF005 | SeadControllerBasePrefix |
| AcnlControllerPrefixF103 | SeadControllerPrefix |
| AcnlControllerWrapperPrefixF103 | SeadControllerWrapperPrefix |
| AcnlControllerOffsetListF103 | SeadOffsetList |
| AcnlPadReaderPrefixF103 | AcnlPadReaderPrefix |
| AcnlPadStateF103 | AcnlPadState |
| AcnlPointerFlagsF005 | AcnlPointerFlags |
| AcnlUiPoint2F005 / AcnlUiPoint2IF005 | AcnlUiPoint2 / AcnlUiPoint2I |

Controller系は実在する `sead::ControllerBase`、`sead::Controller`、`sead::ControllerWrapper` の名前をPascalCaseの部分型名に反映した。vtableと初期化の対応は `0x00543058`、`0x0053CF24..0x0053CF30`、`0x00540B44..0x00540B50`。リストは `sead::OffsetList` の形に合わせて `SeadOffsetList` とし、要素からノードまでの位置を表すメンバー名を `offset` とした。

メンバーの根拠は ACNL-F0721/0722/0723 の既存解析に加え、今回次を一次資料で照合した。

- `SeadControllerBasePrefix`: Init `0x00543050` の初期値書込み、UpdateEdges `0x00542E88` の読書き、SetPointerState `0x00542D78` と装置入力 `0x00540870` が一致する。
- 同型先頭から `pressed/released/repeat=+4/+8/+0xC`、`pointer_flags=+0x10`、`pixel_int=+0x14/+0x18`、`held_frames=+0x2C`、`button_count=+0xFC`、`axis0_bit/axis1_bit=+0x100/+0x104`、`pointer_bit=+0x108`、`idle_frames=+0x10C`、`held=+0x110`、`pixel_float=+0x114/+0x118`、`axis0=+0x11C/+0x120`。位置はcontroller/Wrapperの`base`が先頭なので共通。
- `SeadControllerPrefix`: `base=+0`、`manager=+0x138`、`addons=+0x13C`、`wrappers=+0x14C`。初期化 `0x0053CF3C..0x0053CF64` と Calc `0x0053CDF8..0x0053CEB0` のリスト参照が一致。既知範囲は `0x15C` バイトで派生型全体のサイズではない。
- `SeadControllerWrapperPrefix`: `source=+0x144`、`enabled=+0x148`、`source_bit_index=+0x174`。登録 `0x00549AB0` と利用 `0x005475E4..0x005476EC` が一致。
- `AcnlPadState`: `held/pressed/released=+0/+4/+8`、符号付き16-bit `circle_x/circle_y=+0xC/+0xE`。ReadPadStateの書込みと装置入力の読取りが一致。
- `SeadOffsetList`: `prev/next/count/offset=+0/+4/+8/+0xC`、大きさ `0x10`。初期化時の `addons.offset=4`、`wrappers.offset=0x14C` と、Calcの要素アドレスへの復元で使う位置が一致する。
- `AcnlPadReaderPrefix`: `previous_held=+8`、`bool resync_previous_held_pending=+0x30`。後者が真なら現在heldを前回heldへ同期してから旗を消す（`0x00353450..0x0035346C`）。続くedge計算と `0x003534CC` の保存を照合。全readerの確定サイズではない。
- 旗の列挙子は `AcnlPointerFlags_Valid/Pressed/Released/ClearPosition` として型名から始める。

関数型・コメント中の型参照も揃え、装置入力の引数は `manager` まで使うため `SeadControllerPrefix *` とした。

### 欄の型と派生側コンパイラでの検証

- `pointer_flags` は `unsigned int`。`AcnlPointerFlags` は旗の列挙として残すが、欄の型には使わない。大きさを固定しないenumはコンパイラの設定で1バイトになるため、IDAの4バイトenumをそのまま欄の型として使うと後続の位置が変わる。
- `unk_12C` は意味未確定の `float[2]` とした。座標型とする根拠は無い。`resync_previous_held_pending` は `bool` とし、全構造体の `#pragma pack(push, 2)` を維持した。
- 修正後のIDAの全欄は `_local/evidence/109/layout_after.json`。`local_types.h` の対象ブロックから `_local/evidence/109/layout_test_after.cpp` を生成した。変換はIDA固有の整数型の綴りと `__bitmask` 注記だけで、メンバー宣言・packはそのまま使った。
- devkitARM release 61 の `arm-none-eabi-g++` 13.1.0、ARMv6Kで、`-fno-short-enums` 無し・有りの両方が成功。8構造体のsizeof・alignofと、55メンバー全てのoffsetof・sizeof（各設定110メンバー検査）がIDAと一致した。オブジェクトの定数配列も読み戻して同じ値であることを確認した。
- 列挙単体の `sizeof(AcnlPointerFlags)` は既定で1、`-fno-short-enums` 有りで4。IDAでは4だが、これは構造体の格納欄ではない。`pointer_flags` の4バイトと後続の位置は両設定で同じ。
- 試験ログは `_local/evidence/109/layout_test_after.log`、設定別の測定値・入力ファイルのSHA-256は `layout_test_after_results.json`、再生成・照合手順は `verify_arm_layout.py` に保存した（後二者も同じ証拠フォルダー）。

## 反証条件・未確認点

部分型の先にある派生メンバー、全readerの大きさ、全場面での実体配置は未測定。`Prefix`型の `sizeof` をゲームの確保サイズと解釈してはいけない。
パッドは装置の処理済みキャッシュであり、読み替え前の生HID全体の型ではない。座標型自体には原点や単位を仮定しない。

一次資料は `_local/evidence/109/exports/` の関数先頭アドレス別ファイル。元の全関数書き出しは symbols commit `65293c69e61e182196200b92414beff86f647a98`。対応と SHA-256 は `_local/evidence/109/manifest.json` に保存した。今回、実機操作はしていない。
