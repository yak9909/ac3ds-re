---
id: ACNL-F0784
aliases: []
title: "部屋命令の入口0x565794は上下activeフェーダーのフェードアウト完了を要求する"
summary: "0x565794 は引数なしの32bit 0/1判定で、上下activeフェーダーの各参照がnullかvirtual GetState()==1の時だけ1。部屋命令処理0x6D1E14はこれに加えmanager+57と部屋別条件を使い、命令0の退場には+488とready byteを要求する。"
date: 2026-11-22
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: exports+codebytes
addresses: [0x00565794, 0x006D1E14, 0x0096F3F8, 0x0096F3FC, 0x0074F2A0]
tags: ["menu", "layout"]
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

0x00565794 に `Fader_IsFadeOutComplete`、prototype `int __cdecl(void)` を付ける。引数はなく、32bit R0 に0/1を返す。1の条件は上下それぞれの active フェーダーが null または vt+12 の状態値1であること。状態0も停止状態だが本判定は0を返す。

0x006D1E14 は `BsMenuMgr_ProcessRoomCommand`、prototype `void __fastcall(void *manager)`。完了や受付を表す戻り値はなく、逆コンパイルの int は経路ごとのR0残値。部屋命令の消費とactorの最終退場も別である。

確度 MEDIUM。判定本体、active参照設定、フェーダー生成・状態遷移、部屋/地図側callerの複数の静的根拠が一致。実機追試なし。

## 根拠

一次資料は export/all_functions.txt と xrefs.tsv の rg 結果。_local/evidence/167/selected_functions.txt、xrefs.txt、vtables.json、calculations.json に採録。vtableの値は tools/codebytes.py の read_bytes で確認する。書き出しの過去コメントは根拠に数えない。

- 0x56579C〜0x5657B8 は *0x96F3F8 があればその vt+12 を this のみで呼び、戻りが厳密に1でなければ0。通過後だけ *0x96F3FC へ同じ検査を行う。両nullでも1。本体に書込みもアニメ進行も無い。
- Fader_SetActive 0x5655B8 は第1引数を0x96F3F8、第2引数を0x96F3FCへ設定する。Fader_SetKind 0x6A52B4 の第1/第2引数は上/下のフェーダー選択で、Fader_CreateAll 0x6A4ED0 が screen=0/1 の FaderColor / FaderMoment と上側 FaderWipe を生成する。
- 両参照の基底型は既存の FaderBase（RTTI は ssys::co::FaderBase）。先頭vptr、+4 screen、+5 state、+6 doneFlags、+8 duration、+12 counter。動的型は選択中の FaderColor / FaderWipe / FaderMoment。
- vt+12 は state getter（thisだけ、状態値をR0に返す）。実体は全4表で 0x0074F2A0（LDRB R0,[R0,#5]; BX LR）。名前は ssys_co_FaderBase_GetState、型は this に既存 FaderBase のポインタを1個取り、状態値を int で返す（完全な宣言は symbols に保存）。表は FaderColor 0x8E5458、FaderMoment 0x8E5E34、FaderWipe 0x8F3964、基底 0x90044C。対応は vtables.json と getter-functions.txt。
- FaderBase_StartFadeOut 0x565884 は state0から2へ、FaderBase_Update 0x5657F0 は2の終了で1へ書く。StartFadeIn 0x5658B8 は1から3へ、Update は3の終了で0へ戻す。従って値1はfade-out終了側。FaderMoment_Update 0x1C86E8 の即時遷移も同じ状態値を使う。「ready全般」「フェードが動いていない」とは呼ばない。

### 部屋命令側の入口と戻り値

- 0x6D1E1C の判定が0なら0x6D1F40へ即return。次にmanager+57が厳密に1でなければreturn。先頭2条件は命令の消費より前にある。
- ゲート通過後にも部屋フラグ・既存actor・他画面の条件によって byte_949D29 が上書きされ得る（0x6D1FA8等）。
- 命令0の分岐0x6D1FE8ではmanager+488が非null、かつ byte_949D34 非0の時に限り0x2257E8へ退場要求する。要求時だけ0x6D20ECで命令を2へ戻す。対象なし/readyなしならこの分岐では命令0を保留する。ただし、それ以前の部屋別分岐が2へ変える経路は別にある。
- 0x6D3688 のcallerはR0を使わず直後に上書きする。早期returnではゲート値・+57、後段ではRoom_HasFlags・actor・別関数の値等がR0に残り、一貫した返値が無い。従ってこの関数を bool として受付判定に使えない。

### 外部からの呼出条件・副作用

Fader_IsFadeOutComplete は、ゲームのフェーダー初期化後、その参照の生存が保証される同じ直列のゲーム/UI更新文脈で照会できる。確認したgetterは状態読取りのみで、進行・命令消費・actorの生成/破棄を行わない。null は成功扱いなので「フェーダー初期化済み」までこの返値で確認することはできない。終了・参照切替と競合する他スレッドからの照会は保証しない。OSスレッドIDは未測定。

部屋処理はゲーム自身が manager 更新0x6D34ACから実行する。外部で入口ゲートだけを調べても、manager+57、部屋別分岐、+488、ready、以降の通常actor更新とReleaseを代替しない。処理本体を追加で呼ぶと命令上書き、画面生成、退場要求、manager/global更新が起こり得る。通常更新中の重複呼出や、非生存manager・初期化前・破棄中の呼出は契約外とする。具体的スレッド名を静的解析だけで断定しない。

## 反証条件・未確認点

全特殊部屋の命令再発行・通信切替・終了処理の実測なし。active参照に調査対象外の派生型を差した場合、virtual getterの副作用と状態値契約は別途確認が必要。単一フレームのゲート通過は退場完了を意味しない。
