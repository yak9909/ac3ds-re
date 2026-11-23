---
id: ACNL-F0786
aliases: []
title: "キーボードのMenuFlags0x40と0x80は全体の切り替え中を示さない"
summary: "0x40はキーボードの表示を伴う退場段の要否に使われ、0x80は親が準備完了を待つ通知である。0x80はReleaseでも保存され、地図退場後の0x84残留と両立する。"
date: 2026-11-23
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: "exports+codebytes+supplied-trace"
addresses: [0x949D68, 0x57CA00, 0x57CF04, 0x57F944, 0x193850, 0x57D444]
tags: ["menu", "keyboard", "chat"]
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

vc_MENU_FLAGSの0x40はキーボードの表示を伴う退場段の要否に使われ、0x80は準備完了を親が待つ通知である。
両者を下画面全体の切り替え中フラグにはできない。0x80はキーボードReleaseでも保存される。
確度MEDIUM（独立した生産・解除・読み手の静的根拠）。FC→BC→84の変化は今回の実機traceにも一致する。

## 根拠

対象acnl_jpn_v15。以下のflags/maskは0xを省いた表記も16進とする。
直接xref185関数の参照行は_local/evidence/169/flag-uses.txt、
関連疑似Cはflag-functions.txt。詳細と全trace対応はanalysis.md。
原本SHA256、マスクの検算はcheck.py/check.json。関数の過去コメントは根拠に数えない。

|mask|生産/解除|読み手|
|---|---|---|
|40|0x57CA00がButtonsIn完了でC0を立てる。0x57E228が別の再表示側完了で40を立てる。0x57CF04のWindowOut完了と0x57DDD8のOut完了で解除。0x57C97Cの即時終了側、0x5801A8の初期化側でも解除|0x57D444はロード後に+4549=1なら40があればButtonsOut、なければ即破棄へ|
|80|0x57CA00がC0、0x57C768も80を立てる。親0x193890のkeyboard生成、0x57CDC8のWindowIn enterで解除|親0x193850が80を待ち入力待ちへ。0x2DA548も生存keyboard等の条件下で読む|

- WindowIn enter0x57CDC8: (flags & 0xFFFFFF67) | 8。08開始、10/80解除。
- ButtonsIn enter0x57CC9C: flags |= 10。ButtonsIn更新0x57CA00のアニメ完了より早い通知。
- ButtonsIn完了0x57CA00: flags |= C0。
- WindowOut完了0x57CF04: flags &= ~40、破棄要求。
- Release0x57F944: live keyboard=0、flags &= FFFFFFC7。08/10/20を消し、40/80はこのマスクでは消さない。
- 親Release0x193C3Cはmanager+492=0、800解除。80は消さない。
- 全体初期化0x787004はflags全体を0にする。

実機trace:
82=02+80（地図入場完了と既存の準備完了通知）。
84=04+80（地図退場完了と残る準備完了通知）。
n6ではkeyboard生成側が80を消し04となり、08開始で0C、10通知で1C。
n28に外部から終了要求20が追加され3C。
n34でButtonsIn完了C0が加わりFC。
n46でWindowOut完了が40を落としてBC。
n47でReleaseが08/10/20を落として84。親/リスト除去が後であることと矛盾しない。
80は生存actorポインタでもタブの+6580の解除命令でもない。
従って84や82の数値そのものを停止原因とするのではなく、現在calcと未実行の仕事を調べる必要がある。

## 反証条件・未確認点

n1以前に80を立てた具体的な書込みは未採取。後に保存されることは説明できるが過去の生産元は特定しない。
直接xref以外の別名ポインタ経由の全書き手が存在しないとの証明ではない。
40の全キーボードモードでの視覚上の意味・すべての関数間接呼出は実測していない。
