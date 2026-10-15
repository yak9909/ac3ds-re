---
id: ACNL-F0427
aliases:
- IDA-gpt-6-F004
title: native scrollの別入力経路とstyle arc一時pool（2026-10-12）
summary: '訂正F005: 7word差込みのうち+0はvtableであり除外、+276/+280は中心座標でなく画素。T005 identity geometry fixtureは二重変換を隠したため、scroll実機成立の証拠としない。最新sourceは6word限定で元変換/hit-testを実行する。'
date: '2026-10-12'
category: input
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 2727804
- 1800728
- 2724836
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:83-90
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6-F004: native scrollの別入力経路とstyle arc一時pool（2026-10-12）

- 訂正F005: 7word差込みのうち+0はvtableであり除外、+276/+280は中心座標でなく画素。T005 identity geometry fixtureは二重変換を隠したため、scroll実機成立の証拠としない。最新sourceは6word限定で元変換/hit-testを実行する。
- GPT-6 / IDA（idalib）、MEDIUM。更新SHA/ARM/imagebase/Tとnative命令はstatic.json、F041/F054・旧input_blockとsourceを照合。修正版実機未確認、旧版のscroll不動/arc大領域new失敗/fgobj末尾は元native ARM fixtureで再現。
- CommonScrollBarのmodeはController+272 hold、開始/終了は+4/+8 edge、継続dragは+16 validと+276/+280 float pointerを読む。TouchState40Bだけでは足りない。管理体+208 count/+216 table経由でcurrent controllerを得る。list更新内にtouch関連7wordだけ差込み、40Bとも全値復元して背景遮断を保つ。
- ApplyDragPoint（0x299F7C）のpointはR1、次virtualのdeltaはVFP s0。Touch_IsDragHoldReady（0x1B7A18）はheldかつ40B+14>=3であり座標変化ではない。CommonScrollBar_UpdatePositionFromKnob（0x2993E4）はtop/端数とcallbackを更新する。10rename/3prototype/16概念commentをDB保存/読戻し、公式XMLでT=0・名前/全comment/hash確認。full arrow/binding型とtrack-click point ABIは未確定理由を注記し旧名保持。
- arc失敗はFile Open後newlibの連続領域確保。CTRPF予約poolへ一時退避しcopy/取消/失敗で返す。poolとnewlibは同じ物理plugin heap内の別allocator、追加heap要求なし。検索は通常/補完名の全候補をsort/unique後ページ分割。根拠/回帰試験はgohan_chat_scroll_fix、設計chat_scroll_style_fix_design.md。

