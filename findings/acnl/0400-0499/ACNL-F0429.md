---
id: ACNL-F0429
aliases:
- IDA-gpt-6-F002
title: gohanへのidle/気絶/消失抑制・チャット移植（2026-10-11）
summary: '2026-10-12修正T003: 利用者のMapEditor入力不能報告を旧実Start/HoldField/Present/Wantedで再現。Presentはfield非Shownも含み、actionの退場gateが自身のHoldFieldで継続Tickを止めていた。Running前だけ待つことで新実Tickの移動/touch/game入力遮断が全true。ChatCommandsはcheckbox適用値で有効化し、hotkeyでnative Wait前に原文captu'
date: '2026-10-11'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 9959068
- 7317672
- 3131728
tags:
- chat
supersedes: []
source: IDA:work/FINDINGS.md:99-109
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-F002: gohanへのidle/気絶/消失抑制・チャット移植（2026-10-11）

- 2026-10-12修正T003: 利用者のMapEditor入力不能報告を旧実Start/HoldField/Present/Wantedで再現。Presentはfield非Shownも含み、actionの退場gateが自身のHoldFieldで継続Tickを止めていた。Running前だけ待つことで新実Tickの移動/touch/game入力遮断が全true。ChatCommandsはcheckbox適用値で有効化し、hotkeyでnative Wait前に原文capture、chord全releaseまで取消抑止。保持/再束縛/OFF/元送信経路PASS、修正実機未確認/native概念DB変更なし。設計gohan_chat_ports_design.md、根拠gohan_editor_chat_fix evidence。
- 担当GPT-6、IDA/idalib。更新原入力SHA c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb、ARM32LE/imagebase0。原FOXXY/Vapecordの地域表・callerと更新命令の独立照合でMEDIUM。PC ARM1176の部分実行を実機HIGHと扱わない。
- 状態6/0x9D: native共有38B packetの編集コピーはactor+0x8BC→0x97F69C、引数+0xE以降を消す。XZ×4のs16を+2へ詰め、気絶は+0xFにも復帰XZ、+0x13へ向き。SetStateが自分のネット送信を行う。入力の気絶entry0x676284に対し旧IDB状態表は0x672684へpatch済み、無断復元せず原入力を採用する。idle entry0x658A68は旧IDB関数0x658A20内に合併されており、境界の全面検査までrename保留、commentで記録。
- 消失抑制: 0x6FA8A8/0x52734Cの可逆2語と0x2FC950 MITM。5つのThumb BLX callerだけ今の植物ID+1を局所コピーにして渡す。第5引数はnative stack floatの生bits、hardfloat S0へ渡す宣言は不適合。OFF/別callerは元item/5引数を維持し、保存mapへ事前書込みしない。
- チャット結果通知0x522D40は普通チャット以外にも使われるためTextInput_PublishResultへ改名。先頭PC相対LDRはSDK MITMで移設されないので、原値R2ロード→原+4の専用trampolineが必要。認識コマンドだけ送信を捕捉、通常/OFFの原通知経路は維持する。数字filterはReturnWait内で認識コマンドのみ一時解除し復元。native GameListを普通チャットの上へ重ね、既存IME hookを共有する。
- 日時は12B GohanNativeDate、2000epochのnative変換と実入力をPCで照合し日曜0。Time_SetFromDate→Time_StoreToSaveを使い、通信中/特殊時計部屋は拒否。Time_DateFromSystemNsの64bit引数はR2/R3（IDA fastcallのR1/R2自動割当をusercallへ訂正）。数字単独は利用者の最新指示で分。月差分は暦で月末丸め。入力範囲2012..2050。
- DBへ5rename、型/7prototype・current-date global型、根拠commentをsave/readback、close/所有者0。公式XML/全入力bytes/hash検査PASS。未確定の0x521084の細部は今回nativeテキストfixtureの既存caller確認だけであり、全helperの役割/構造検証不足のため旧名を維持。
- 製品操作: 両エディターはaction/B/再実行/排他。公共事業設定folder/7項目と登録callbackを削除、MapCursor90/120/60固定、ドロップID共有、R+A、室内メニュー、catalog-trash統合、自前GUI自動open解除。parser4330条件/22anchor/13CPP/linked/nativeABI/両editor遷移/しずえ検査PASS。新文字は既存生成器でフォント再生成し欠字0。詳細docs/topics/gohan_chat_ports_design.md、work/evidence/gohan_chat_ports。実機・GPU/FS/ネット・フレームタイミングは未確認。

