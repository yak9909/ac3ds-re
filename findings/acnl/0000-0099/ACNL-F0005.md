---
id: ACNL-F0005
aliases:
- F-407@v1:RE/FINDINGS.md:29
title: F-407 PC準備時点の履歴（配置待ちは解消済み）
summary: 独立Plugin/SwkbdEngineProbe/swkbd_engine_probe.3gxを作成。289,985 bytes、SHA50ec21a1bde6d52f13fa916ac23aceb2f81dbb833a5ca4db8ca77c3b96368385。ソース/ホスト/ARM構文を検証してからビルド。生成1301命令/213直接分岐/48PCリテラルの検査、生成ARMから原本エンジンへの一連のPC試験、mailbox誤適用防止10条件までPASS。展開はctrt
date: '2026-09-11'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 4603428
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:29-38
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-407 PC準備時点の履歴（配置待ちは解消済み）

独立Plugin/SwkbdEngineProbe/swkbd_engine_probe.3gxを作成。289,985 bytes、SHA50ec21a1bde6d52f13fa916ac23aceb2f81dbb833a5ca4db8ca77c3b96368385。ソース/ホスト/ARM構文を検証してからビルド。生成1301命令/213直接分岐/48PCリテラルの検査、生成ARMから原本エンジンへの一連のPC試験、mailbox誤適用防止10条件までPASS。展開はctrtool出力と全bytes一致、6辞書と315再配置も照合。PCで「かんじ」17件、文章6件、「か」143件が原本実行と順序一致。保存対象レジスタ/FPSCR/SPとstack guard、辞書本体不変も確認。

F407は実機未配置・未実行。最後の実機読取りはACNL Suspend/PC0x00463E24/bp0、F404 header exe217088/heap10268672、slot0x07029DD8=0x070012B8。F406の一時変更は全復元済み。F407の予期headerはexe258048/heap10227712なので、旧版へ新mailboxを書かない。PCからSDのタイトルフォルダは見えていない。利用者による検証版の入替え→ACNL再起動→IDAアタッチ/Suspendが必要。実機側のF407変換成功はまだ主張しない。

次はSYSTEM_KEYBOARD/engine_probe_live_f407.py（既定inspect）でheader/全アンカー照合。action prepareで要求2を一度だけ設定→run_timed.py→inspect、prepared1/executed0/freed1と全FS成功を保存。それからaction convert/text「かんじ」の要求3を一度だけ設定して最小候補照合。driverは成功した準備結果が現bootにないとconvertを拒否。Resumeは別操作、要求の再送をしない。state1ならstageを記録して進捗を確認。辞書/元codeをSDや3gxに同梱しない。gohan/F404ファイルは不変。BACKUP/plugin_f407_pc_verifiedへソース/ELF/3gx/検証結果を保存した。

詳細DOCS/system_keyboard_native_loader.md、Plugin/SwkbdEngineProbe/README.md、証拠SYSTEM_KEYBOARD/evidence/f407_engine/。以下はF406以前の完了記録。学習/ユーザー辞書/並行利用/全入力の保証は残る。

