---
id: ACNL-F0261
aliases:
- F-238
title: 'F-238: ロード表示中でも top LayoutList の構成はフェーズで変わる — `MEDIUM`（独立した stopped snapshot＋no-draw 実行標本）'
summary: F-234 の replay ring は、ロード中の一つの上画面 pass で id `0x08 -> 0x0A` を記録した。
date: '2026-09-01'
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5664304
- 10170112
- 1273956
- 11376900
- 1185468
- 1185476
- 1185488
- 1185728
- 1185740
- 1185768
- 1185788
- 5669596
- 5669724
- 5670280
- 5669764
- 5669828
- 5669860
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:13992-14067
by: unknown
original_by: ''
reviewed_by: []
state: consolidated
consolidated_into: topics/acnl/ui.md
duplicate_of: ''
superseded_by: ''
---
## F-238: ロード表示中でも top LayoutList の構成はフェーズで変わる — `MEDIUM`（独立した stopped snapshot＋no-draw 実行標本）

F-234 の replay ring は、ロード中の一つの上画面 pass で id `0x08 -> 0x0A` を記録した。
しかし「ロード画像が見えている」ことだけから、その node 構成が継続しているとは仮定できない。
F-237 の再生順制御を統合する前に、現在の list を自動で選ぶ必要があるかを追加確認した。

ユーザーがロード画像を目視して Suspend した直後、read-only `inspect` は top list
`0x32FF5F8C` に id `0x10` の tail 1 node、bottom list に 0 node を記録した。これは既存の
F-234 trace とは独立した stopped memory walk（vtable / prev / next / tail を検査）である。

次に新規 `PATCHES/probe_layout_reorder_auto.py` を使用した。この no-draw hook は上画面ごとに
current list を先に走査し、`Layout+0x100 == 0x08` が**ちょうど一つ、かつ non-tail**の時だけ
再生を保留して末尾へ移す。それ以外は stock loop を再現する。静的 `code.bin.i64` の zero cave
`0x838C00..0x838E00` と、停止中実機の zero cave / zero LOG / stock hook / BP=0 を二経路で
監査してから設置した。

300 ms reservation ではクラッシュせず停止した。LOG は `calls=0x5D`、last top match count `1`、
累積 reorder `0`、target `0` を記録した。コード上 target は unique non-tail の時だけ LOG に書く
ため、この短い標本では id `0x08` が現れても tail だったことを示す。実行前の id `0x10` snapshot と
合わせ、少なくともこのロード遷移には list 組成が異なる複数フェーズがある。これは F-234 の
一回限りの `0x08 -> 0x0A` pass を否定しないが、固定 id / 固定 heap pointer を常時の順序制御に
使えないことを強める。

hook は直後に uninstall し、`state=-1`、BP 0、`0x566E30=0xE92D4070`、
`0x838C00=0`、`0x9B2F00=0` を独立に読み戻した。F-238 は UI画像（スプライト）の前面化をまだ
示さない。次は **transition 前** にこの自動プローブを置き、F-234 型の unique non-tail id `0x08`
を捕獲した時だけ replay ring と表示の両方を確認する。

その後、hook なし・BP 0 の状態で、ユーザーがロード画像を実際に目視して Suspend した第 2 標本を
read-only で採取した。`state=-1`、`PC=0x00137064`、top List `0x32FF5F8C` は再び
`0x3225B070` の id `0x10` tail 1 node、`start=length=capacity=0`、bottom List は空だった。
この時、`GpuCmd_SelectList` の既知の id `0x10` bucket `0x00AD9904` も read-only で辿った。
manager は `0x327AE21C`、`base=0x327AE270`、`size=0x1000`、`offset=0x2C0`、next 0 だった。
すなわち current Layout node 側はゼロ長でも、同 id の GPU record manager には F-234 と整合する
非ゼロ記録が残っている。静的に `GpuCmd_SelectList` が id からこの manager bucket を選ぶこと、
動的に current Layout と manager の値が食い違うことを突き合わせた。

これは「画像が見えているなら id `0x08 -> 0x0A` の非ゼロ記録列が現在の List に必ずある」という
解釈を否定する一方、current top の `0x3225B070` を F-234 でリソースまで同定した loader Layout
`0x3225A2B4` と同一視できないことも示す。F-234 と矛盾するのではなく、描画済み画像を見ている
時点、record manager の保持状態、次の List を組む時点を区別すべきという根拠である。ただし、
この二標本だけでは各 phase の遷移条件・画像保持機構・current id `0x10` node の個別責務は未確定である。

### F-239: Layout の list id は描画対象 Layout の一意な同定子ではない — `HIGH`（静的＋動的）

`GpuCmd_SelectList` の static assembly は id を bucket key にして manager を選ぶ。一方、現在の
user-visible loader stopped 標本では、top List の `Layout=0x3225B070` は id `0x10` で
`start=length=capacity=0`、display `0x410` だったが、同 id bucket の manager は上記の非ゼロ
`offset=0x2C0` を保持した。F-234 でロード専用 resource と結び付けた Layout は
`0x3225A2B4`（id `0x10`、recorded length `0x2C0`、display `0x400`）である。

この static 根拠は `code.bin.i64` の `GpuCmd_SelectList(0x1216BC)` を今回あらためて assembly で
確認したものでもある。`0x1216C4..0x1216D0` は `id & 0x1F` と bucket を使って exact id manager を
連結リストから選び、`0x1217C0..0x1217CC` は旧 manager の `g_GpuCmdPtr-base` を `+0x0C` に保存する。
`0x1217E8..0x1217FC` は選択 manager の `base + offset` から `g_GpuCmdPtr` / `g_GpuCmdEnd` を再確立する。
この二箇所には F-239 の IDB コメントを保存した。

従って **id だけ、または固定 heap pointer だけで「ロード画像の Layout」と判定してはいけない。**
以後の trace は (1) Layout pointer、(2) id、(3) manager base/size/offset、(4) replay caller/pass を
同じ標本に残す。これが揃わない限り、順序制御・command-add・buffer 拡張の対象を選ばない。

### F-240: current Layout の記録長 0 は replay を完全に止める — `HIGH`（静的＋user-visible stopped 実機）

`code.bin.i64` の `Layout_ReplayRecordedList(0x5682DC)` は、`0x56835C` で `Layout+0x108` を読み、
`<=0` なら `0x568588` へ分岐して return する。この return は Drawer の準備
(`0x568384..0x5683C4`) と `GpuCmd_ReplayRecordedListRange(0x5683E4)` の**前**である。IDB にこの
guard の F-240 コメントを保存した。

現在の user-visible loader stopped 標本の top node `0x3225B070` は `+0x108=0` だった。従ってこの
node は、その停止時に `Layout_ReplayRecordedList` を通じて GPU command を再生している直接の画像源
ではない。画面上のロード画像は、既に提出済みフレームの表示保持、またはこの top node 以外の描画
経路のどちらかである。この二択をまだ確定せず、次の transition では final submit / framebuffer
switch と record/replay を別々に記録する。

---

