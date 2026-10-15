---
id: ACNL-F0004
aliases:
- F-407
title: 'F-407 実機成功: キーボード非起動で候補17/6/143件を取得（2026-09-11、最新・HIGH）'
summary: 利用者がF407を配置・ACNL再起動/再アタッチ。Suspend/bp0、実機headerと全生成コードアンカー、成果物/現行ソースhashを照合した。要求2の展開・辞書配置・315再配置が成功し全解放された後、要求3で「かんじ」「わたしはねこがすきです」「か」を各1回実行。候補17/6/143件が原本PCと全順位一致。前2入力は保存済み実機SWKBD候補列とも直接一致。「か」は初回50件からgetterが143件まで追加検索し、終端0を確認した。
date: '2026-09-11'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5638236
tags:
- keyboard
supersedes: []
source: v1:RE/FINDINGS.md:15-28
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-407 実機成功: キーボード非起動で候補17/6/143件を取得（2026-09-11、最新・HIGH）

利用者がF407を配置・ACNL再起動/再アタッチ。Suspend/bp0、実機headerと全生成コードアンカー、成果物/現行ソースhashを照合した。要求2の展開・辞書配置・315再配置が成功し全解放された後、要求3で「かんじ」「わたしはねこがすきです」「か」を各1回実行。候補17/6/143件が原本PCと全順位一致。前2入力は保存済み実機SWKBD候補列とも直接一致。「か」は初回50件からgetterが143件まで追加検索し、終端0を確認した。

各要求は既存検証用3gxの独立スレッドで実行。キーボード起動/APTなし、辞書・元codeは内蔵タイトルからRAMへRead、SD/3gxへのリソース同梱なし。内蔵FSのOpen/Size/全Read/CRC/Close/Releaseすべて成功、5 MiB arenaのFree完了。変換3要求はstage10/state2/failure0、prepared1/executed1/exhausted1/stack_guard1/freed1。arenaは各回0x061BE000。各5000ms走行後の観測であり、変換時間そのものの測定ではない。

結果はSYSTEM_KEYBOARD/evidence/f407_engine/hardware_prepare.json、hardware_kanji.json、hardware_phrase.json、hardware_ka.jsonへ個別保存。report全34452 bytesを別の実機読取りで保存し143候補を独立に再デコードして一致。hardware_verified.json、hardware_final_report.bin、hardware_final_state.json参照。ソース・3gx/ELF・検証器・実機証拠をBACKUP/plugin_f407_hardware_confirmedへ保存。

最終ACNL Suspend(-1)、PC0x0056085C、bp0、command0。実機はF407版（SHA50ec21a1bde6d52f13fa916ac23aceb2f81dbb833a5ca4db8ca77c3b96368385、exe258048/heap10227712）、report0x07033AE0、command0x07033ADC、input0x0703212C。試験arena/FS handle保持なし。F407はゲームコードをフックしないため、この試験で追加した復元待ちフックなし。F406の一時変更は前bootで復元済み。正常gohan/F404ファイルも不変。

詳細DOCS/system_keyboard_native_loader.mdとPlugin/SwkbdEngineProbe/README.md。今後追加試験するならengine_probe_live_f407.pyの既定inspectから現在値を確認し、要求を1回だけ設定してrun_timed.pyで走らせる。自前メニュー統合を前提にしない。

残る未確認事項: 個人学習/ユーザー辞書、長文上限や全入力、明示的な文節境界指定APIの実機試験、並行呼出し、ロードと変換の処理時間内訳。今回の文章6候補取得を、文節境界編集APIまで確認したものとは扱わない。キーボード非起動・実機内蔵資源の取得・再配置・独立contextの予測候補列挙という今回の経路は成功済み。以下は準備時点と過去の履歴。

