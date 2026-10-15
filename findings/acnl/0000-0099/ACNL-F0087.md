---
id: ACNL-F0087
aliases:
- F-49
title: F-49 メッセージ表示の仕組みと「メニューアニメーションをカット」の副作用 — `HIGH`
summary: '`REFERENCES/CHEATS/ui.txt` の「メニューアニメーションをカット」で'
date: '2026-09-08'
category: ui
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 9452652
- 9456052
- 6271144
- 6270396
- 6270824
- 6259256
- 6294484
- 2004024
- 2004520
- 4663772
- 6193092
- 6193176
- 6268416
- 6268992
- 6270284
- 6271272
tags:
- menu
- message
supersedes: []
source: v1:RE/FINDINGS.md:2583-2673
by: unknown
original_by: ''
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ''
---
## F-49 メッセージ表示の仕組みと「メニューアニメーションをカット」の副作用 — `HIGH`

`REFERENCES/CHEATS/ui.txt` の「メニューアニメーションをカット」で
**漢字とルビが消える**原因の解明。**静的 IDB (idalib) のみで解析した。**

### 関係するクラス（RTTI 実測、F-43 の手法）

| vtable | クラス |
|---|---|
| `0x903C6C` | **`script::TalkSeq`** → `script::SeqEngine` → `script::MsgEngine` |
| `0x9049B4` | **`script::TalkRuby`** |

`TalkSeq_Create` (`0x5FB0A8`) が `script::TalkSeq` を作り、
その中に **`script::TalkRuby` を 2 つ**持たせる（`this+212` と `this+352`）。

初期値:

```c
*(float*)(this + 176) = flt_5FB298;   // 1.0f  文字送り倍率
*(byte *)(this + 202) = 0;            // 一気に表示フラグ
```

### 呼び出し構造

```
vtable script::TalkSeq +0x10
  -> TalkSeq_Update   (0x5FADBC)
       0x5FAF68  BL TalkSeq_StepText   ★呼び出し元はここ 1 箇所だけ
  -> TalkSeq_StepText (0x5F8238)
       this+202 / +501 / +502 のいずれかが立つと「一気に表示」経路へ
       while (!rubyA.done || !rubyB.done) { MsgStream_Emit(rubyA); MsgStream_Emit(rubyB); }
  -> MsgStream_Emit   (0x600BD4)
       MsgStream_DecodeCode で制御コードを判別
         14 -> MsgStream_ReadRubyCode + vtable+24   ★ルビ（漢字＋ふりがな）
         15 -> vtable+28
         他 -> vtable+20                            通常の文字
```

### チートの 3 行が何をしているか

```
005FAF68 E1A00000   BL TalkSeq_StepText -> NOP
005FB298 43B00000   文字送り倍率 1.0 -> 352.0
00568BF8 43B00000   UI アニメ再生レート 1.0 -> 352.0
```

**1 行目が不具合の原因。** `BL` を NOP にすると、直前の `MOV R0, R4` で入った
`R0`（非ゼロ）がそのまま `CMP R0,#0` / `MOVNE R6,#1` を通るので、
`TalkSeq_Update` は**即座に「表示完了」を返す**。文字が一瞬で出るのはこのため。

同時に **`MsgStream_Emit` が一度も回らない**ので制御コード 14 が処理されず、
**漢字とふりがなが両方消える。**

**2 行目は効いていない。** `TalkSeq_StepText` の呼び出し元は `0x5FAF68` の
1 箇所だけ（`xrefs_to` で確認）なので、1 行目で潰した時点で倍率は参照されない。
**3 行のうち 1 行が死に、1 行が不具合の原因だった。**

3 行目だけがウィンドウアニメに効いている（`UiAnim_Init` が `this+16` に入れる再生レート）。

### 修正版

**`this+202` の読み出しを 1 に固定する。**

```
005F8278 E3A00001    ; LDRB R0,[R4,#0xCA] -> MOV R0,#1
```

- `LDRB [Rx,#0xCA]` は**バイナリ全域でこの 1 箇所だけ**（実測）。
  影響範囲がこの読み出しに限定される
- 書き込み側は `0x1E9438` / `0x1E9628` / `0x4729DC` / `0x5E7FC4` / `0x5E8018` /
  `0x5FA600` / `0x5FA840` / `0x5FAD4C` / `0x5FB128` の 9 箇所。
  UI モジュール内にあり、正規の「一気に表示」フラグだと分かる
- 1 に固定すると**ゲーム自身の一括表示経路**に入り、`MsgStream_Emit` が全文字分回るので
  漢字もルビも欠けない
- `R0` はこの `CMP` にしか使われない（直後に別経路で上書きされる）ので安全

生成した AR コードは `DOCS/ar_codes.md`。

### 教訓

**チートの行を「全部必要」と思って丸ごと採用しない。** 3 行のうち

- 1 行は他の行に潰されて**効いていない**
- 1 行が**副作用の原因**
- 実際に望んだ効果を出していたのは残り 1 行と、副作用込みの 1 行だった

`xrefs_to` で「その関数の呼び出し元は 1 箇所だけ」と分かったことが、
2 行目が死んでいる判断の決め手になった。

---

