---
id: ACNL-F0743
aliases: []
title: "CtrControllerのオブジェクト先頭仮想表を大域変数と型で登録"
summary: "CtrController本体の先頭に書かれる仮想表は0x008FE6F8で、9項目・36バイト。vtbl_sead_CtrControllerをSeadCtrControllerVtable型のglobalsとして登録し、calcと装置更新の項目を既存関数型で表した。"
date: 2026-10-23
category: input
build: acnl_jpn_v15
confidence: MEDIUM
tool: 全関数書き出し / codebytes / IDA型適用・位置検査
addresses: [0x008FE6F8, 0x00540B3C, 0x005404AC, 0x0053CDC4, 0x00540870]
tags: [button, touch, sead]
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

`vtbl_sead_CtrController` は `0x008FE6F8`、大きさ `0x24`（36）バイト、型は `SeadCtrControllerVtable`。既存の vtables の class/count を保ち、globals にも構造体型を持つ大域変数として登録する。
名前の番地は**オブジェクト先頭のvptrへ書く値**であり、前置きデータを含む元のC++シンボル全体の先頭ではない。
確度 MEDIUM。初期化の書込みと管理体・Controllerの仮想呼出しという独立した静的経路を、原本バイトと照合した。実機測定は行っていない。

## 根拠

### 初期化の書込み

`0x00540B3C` は基底初期化を呼び、`0x00540B44 LDR R3, [PC,...]` でリテラル `0x00540B64` の値 `0x008FE6F8` を読む。`0x00540B50 STR R3,[R0]` が本体先頭へ保存する。リテラルの原本bytesは `F8 E6 8F 00`。
既存 [ACNL-F0737] の初期化同定と一致する。

### 独立した仮想呼出し

- 管理体 `0x005404AC` の `0x005404F8..0x00540504` は controller配列からR0を取得し、`[R0]` の表の `+0x10` を `BLX R1` で呼ぶ。表 `0x008FE708` の原本値は `0x0053CDC4`（`sead_Controller_Calc`）。
- Calcの `0x0053CDD8..0x0053CDE4` は本体先頭の表を読み、`+0x18` を同じthis引数R0で呼ぶ。表 `0x008FE710` の原本値は `0x00540870`（`sead_CtrController_UpdateFromDevice`）。この経路は [ACNL-F0721] とも一致する。

### 表の範囲と型

codebytesで確認した9項目は次のとおり。既存vtablesのcount=9とも一致する。

| offset | 格納値 | 型のメンバー |
|---|---|---|
| +0x00 | 0x00749D88 | void *unk_0 |
| +0x04 | 0x00749D3C | void *unk_4 |
| +0x08 | 0x00540B6C | void *unk_8 |
| +0x0C | 0x00540B68 | void *unk_C |
| +0x10 | 0x0053CDC4 | int (__fastcall *calc)(SeadControllerPrefix *) |
| +0x14 | 0x00748668 | void *unk_14 |
| +0x18 | 0x00540870 | void *(__fastcall *update_from_device)(SeadControllerPrefix *) |
| +0x1C | 0x005429EC | void *unk_1C |
| +0x20 | 0x0053CEB8 | void *unk_20 |

直後の `0x008FE71C` は0であり、関数ポインタ列はここで終わる。9×4=`0x24` バイトを採る。
直前 `0x008FE6F0/0x008FE6F4` は `0/0x008CA914` であり、globalsの範囲には含めない。前置きの意味そのものは今回型にしない。
既知2項目の型はsymbolsにある既存関数プロトタイプと揃えた。未確認項目は [ACNL-F0713] の `SeadExpHeapVtable` と同じ `void *unk_<offset>` の約束とし、署名や役割を推測しない。

IDAの作業用コピーへ型を適用し、読み戻した全9メンバーが4バイト、offsetが `0,4,...,0x20`、全体が36バイトであることを検査した。入力本体の部分型は変更していない。
一次証拠は `_local/evidence/112/` の4関数書き出し、`manifest.json`（元symbols commit・SHA-256・原本word）、`type_verification.json`。書き出し元symbols commitは `65293c69e61e182196200b92414beff86f647a98`。サイズ・番地計算と再現手順は同フォルダーの `prepare.py`、`apply_type.py`。

## 反証条件・未確認点

別ビルドへの適用、実行中オブジェクトの配置・vptr、未確認7項目の署名と意味は未測定。原本の初期化リテラル、呼出しslot、表終端が上記と異なれば番地・型範囲を見直す。
この36バイトは仮想表の大きさであり、CtrControllerオブジェクト全体の大きさではない。既存関数の戻り値型を独立に再確定する解析は今回行っていない。
