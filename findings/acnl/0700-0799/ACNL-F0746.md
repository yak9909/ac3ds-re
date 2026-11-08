---
id: ACNL-F0746
aliases: []
title: "通信枠からプレイヤーセーブを得る関数と resident 配列"
summary: "0x2FEB60 は通信枠 0..3 を選び、4 以上は自分のプレイヤーセーブを返す。resident セーブは全体先頭 +0xA0 の 4 要素、要素間隔は 0xA480。"
date: 2026-11-09
category: save
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA (export), IDAPython, codebytes, Unicorn
addresses: [0x002FEB60, 0x002FB900, 0x002FB920, 0x002FB8AC, 0x002FAF48, 0x00955F8C]
tags: [save-data, player]
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

`0x2FEB60` は `AcnlPlayerSave *Save_GetPlayerByOnlineSlot(unsigned int online_slot)`。
0..3 は通信枠、4 以上は自分を選ぶ。通信枠を resident の配列添字に直接使う関数ではない。
自分の時は `[0xAA914C]`、他の枠では対応する save ID を引き、必要な検査後に `0x2FB920` へ渡す。
分岐・独立した自分用 getter・save ID getter・stride の補助関数を照合したため MEDIUM。実機未確認。

## 根拠

- 書き出し `_local/builds/acnl_jpn_v15/export/functions/00200000/002FEB60_vc_PSOFFSET.txt`。
- `0x2FEB68..0x2FEB70`: `SaveIo_DbgIsWholeIo89A60()` が非 0 なら null。
- `0x2FEB74..0x2FEB84`: 引数が unsigned 4 以上なら `0x305F6C` の返り値へ置換。`0x305F6C` は `Net_GetLocalPlayerIndex` (`0x75D7A4`) へ尾呼出しする。
- `0x2FEB8C..0x2FEBA4`: 自分の枠と等しければ `dword_AA914C` の格納値をそのまま返す。
- 他の枠では `g_PlayerSaveCacheById4To7 + 0x29200 + (slot & 3)` のバイトを save ID として読む。`0x2FDE6C` の `id < 8` 検査を通過した時のみ `0x2FB920` へ進む。不成立なら null。
- `0x2FB900` は I/O 状態を確認して同じ `[0xAA914C]` を返す、独立した `Save_GetCurrentPlayer`。自分を指すことの別根拠。
- `0x2FB920` の `0x2FB938..0x2FB954`: resident ID は `Save_GetTownBase()+0x20` を `0x2FB8AC` に渡す。`Save_GetTownBase` (`0x2FAF48`) は `[0x955F8C]+0x80`。
- `0x2FB8AC` の `0x2FB8B8..0x2FB8C0`: `0x149 * index << 7`、すなわち `0xA480 * index` を足す。index>=4 は null。従って resident 4 人の先頭は全体 +0xA0、末端は +0x292A0。
- cached ID の場合も `0x2FB980..0x2FB98C` は同じ stride で `g_PlayerSaveCacheById4To7` を参照する。resident と cache の二つの保存先でサイズを照合した。
- `AcnlPlayerSave` はこの stride 全体を詰め物を含めて表し、`AcnlGardenSavePrefix.players[4]` を +0xA0 に置く。
- `g_GardenSaveBasePtr` の型を `AcnlGardenSavePrefix *` へ絞る。`AcnlGardenSavePrefix` は +0x6AE40 までの部分型であり、セーブ全体の大きさを意味しない。
- 旧 `vc_PSOFFSET` は未検証ラベルであった。ACNL-F0106 / ACNL-F0592 の「4 で自分を得る」使用とは両立するため訂正ではなく、`supersedes: []`。当該旧記録の格付け ? には依存せず上の命令列を使用した。

## 反証条件・未確認点

実機で I/O 中・他プレイヤー参加中の null 条件は未実測。
自分のポインタが常に resident 配列内とは限らないため、自分の選択には getter の返り値を使う。
セーブ全体の完全なサイズ、型の詰め物の内部構造は未確認。
