---
id: ACNL-F0741
aliases: []
title: "Controller計算の装置更新直後に必要な値はR4と旧状態R8/R9である"
summary: "0x0053CDE8ではR4=selfとR8/R9の旧保持・旧有効旗が後続で使われる。R0〜R3/R12や呼出し側保存VFPに残る装置更新の値は、その後のedge計算を越えて利用されない。"
date: 2026-10-22
category: input
build: acnl_jpn_v15
confidence: "MEDIUM"
tool: 全関数書き出し / codebytes / IDA型位置検査
addresses: [0x0053CDC4, 0x00542E88, 0x005475D4]
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

`sead_Controller_Calc` の装置更新直後 `0x0053CDE8` で保持すべきローカルの入力は、R4のself、R8の旧held、R9の旧pointer validである。R0〜R3/R12と呼出し側保存VFPに装置更新が残した値を継続利用する依存は無い。
確度 MEDIUM。Calcの全後続命令と、直後のUpdateEdgesおよび旧状態を再利用するWrapper呼出しを独立に照合。実機未確認。

## 根拠

- `0x0053CDC4 PUSH {R4-R10,LR}`、`0x0053CDC8 MOV R4,R0`。旧heldは `0x0053CDD0` でR8へ、旧validは `0x0053CDD4` でR9へ保存し、`0x0053CDE4 BLX R1` で装置更新を行う。
- 後続 `0x0053CDE8 MOV R2,R9; 0x0053CDEC MOV R1,R8; 0x0053CDF0 MOV R0,R4; 0x0053CDF4 BL 0x00542E88` が引数を作り直す。
- UpdateEdges `0x00542E8C..0x00542EA0` はR0/R1/R2を保存してR3をロードし比較する。R12や到来時の条件旗を引数として使わない。
- 同関数が軸計算で使うS0/S1は `0x00542EA8..0x00542EAC`、`0x00542EC8..0x00542ECC` でメモリーからロードしてから渡す。装置更新が残したVFP値への依存は無い。
- CalcのR6は `0x0053CDFC`、R7は `0x0053CE00`、R5は `0x0053CE2C` で使用前に作り直される。R10は本体で入力値として使われず、末尾POPで呼出し元値を戻す。
- `0x0053CE84 MOV R2,R9`、`0x0053CE8C MOV R1,R8` がWrapperへ旧状態を再送する。Wrapperは受け取った旧heldを対応表で再変換し `0x005476F8` でUpdateEdgesへ渡す。
- CalcにVFP演算・VFP値の後続読取りは無い。元末尾 `0x0053CEB4 POP {R4-R10,PC}` とスタック上の復帰状態は維持する必要がある。

## 反証条件・未確認点

これは当該ゲーム関数の生存値であり、割込み先のコードやHookの呼出し規約を緩める許可ではない。SP/LR/復帰先と呼出し元保存状態、VFPのcallee保存部分を壊してよいという結論は含まない。
CTRPFの実際の保存・復元と実機動作は未検証。別の仮想実装が非標準の暗黙引数を要求する場合はその実装を別途調べる必要がある。

一次資料は `_local/evidence/109/exports/` の関数先頭アドレス別ファイル。元の全関数書き出しは symbols commit `65293c69e61e182196200b92414beff86f647a98`。対応と SHA-256 は `_local/evidence/109/manifest.json` に保存した。今回、実機操作はしていない。
