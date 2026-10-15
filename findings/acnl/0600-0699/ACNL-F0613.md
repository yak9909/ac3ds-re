---
id: ACNL-F0613
aliases:
- IDA-opus-5.5-F097
title: '建物プレビューのファイル読み込みは既にゲームの読み込み係のスレッドで非同期（2026-10-06、MEDIUM: 静的）'
summary: '解析ソフト: IDA / 解析モデル: opus-5.5。'
date: '2026-10-06'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 3242272
- 5676436
- 5675936
- 11401184
- 11401172
- 9894996
- 3242328
- 5676204
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:4757-4765
by: opus-5.5
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5.5-F097: 建物プレビューのファイル読み込みは既にゲームの読み込み係のスレッドで非同期（2026-10-06、MEDIUM: 静的）

解析ソフト: IDA / 解析モデル: opus-5.5。
- gohan の BuildingPreview は `G3dResHolder_RequestLoad` 0x317920 → `FileRes_RequestLoadAligned` 0x569D94 → `FileRes_RequestLoadAsync` 0x569BA0（a5 = 1 = 非同期）で読む。
  初回の呼び出しは、錠 0xADF7E0 の下で FileRes をリスト 0xADF7D4 へ積み、読み込み係 [0x96FC54] へ 'load'（0x6C6F6164）を vtable +0x0C で通知するだけ。呼んだスレッドはファイルを読まず、毎フレーム状態（FileRes+232 = 3/4/5 で完了）を問い合わせる。a5 = 0 のときだけ呼んだスレッドで同期に読む（sub_569EFC）。
- したがって「入力と読み込みを別スレッドに分ける」の読み込み（I/O）部分は既に別スレッド。ゲームのスレッドに残るのは 資源の準備（ResHolderSetup 0x317958 x5）・インスタンス生成・ヒープの作成/破棄で、これらはゲームのヒープとシーンを触るので別スレッドへは移せない（錠の有無を確かめていない）。
- 切り替えが遅い要因（gohan のコードから）: 読み込み中の 1 本は中断できない（切れ目まで待つ）、3 本（LUT・テクスチャ・モデル）を 1 本ずつ順に、片付けで 4 フレーム待つ、毎回ヒープを作り直す、LUT は種類（fobj/sobj）ごとに同じなのに毎回読む。どれがどれだけ効いているかは未測定。
- IDB: 0x569CAC にコメント。

