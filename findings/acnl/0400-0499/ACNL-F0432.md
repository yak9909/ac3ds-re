---
id: ACNL-F0432
aliases:
- TreeSitter-gpt-6-F002
title: 整理済みチートの挙動保持リファクタリング（2026-10-11）
summary: '解析/検証: Tree-sitter・GNU C++ / gpt-6。元IDA-gpt-6.1-sol-F018と追加TreeSitter-gpt-6-F001の帰属を保持。対象は2700既存関数のみ、新規JOKER/他CTRPF整理は中断。共有設定familyの1関数化は利用者の訂正で撤回。'
date: '2026-10-11'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:128-135
by: gpt-6
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## TreeSitter-gpt-6-F002: 整理済みチートの挙動保持リファクタリング（2026-10-11）

- 解析/検証: Tree-sitter・GNU C++ / gpt-6。元IDA-gpt-6.1-sol-F018と追加TreeSitter-gpt-6-F001の帰属を保持。対象は2700既存関数のみ、新規JOKER/他CTRPF整理は中断。共有設定familyの1関数化は利用者の訂正で撤回。
- ARの不変register選択を定数化し、未使用scratch/data、不要label/step scopeを除く。12loop callbackは関数内structの直接再帰へ変更し、register共有・各再帰のread scratch・終了伝搬を保つ。28immutable payload bufferを関数内static constへ移す。選択肢tableの36private helperをconst参照にし、計44callbackでreserveする。関数名/引数/元の取消・復元・書込幅/順序を維持し、短い関数内の処理メモを追加する。
- 独立経路: 原bodyの逆差分完全復元→既存原資料/局所化contractの再構成、変換前後を別namespaceで実compileしてhost mock上のordered read/write/key/copy traceとbytesを比較。AR2367/table48/synthetic25・466548条件PASS（変換前2373の残りは6XX雛形でコメント変更のみ）。全20cppの既存SDK・ARM C++11/C++17構文PASS。最終公開source/hash/旧stage復元hash・原資料・全partition/ヘッダ・関数外状態を12406/53450で再検証終了0、status_refactor/refactor_final_gate=VERIFIED_SOURCE_REFACTOR。全2700関数にメモ2970を反映済み、source REFACTOR.mdとvalidationへ結果を保存。
- ARM -Osの最適化対象40関数でtext15228B減/rodata319B増、入口stack最大72B減。命令byte数はobject単位で、最終link/再帰深さ/callee stack/実機時間は含めない。根拠work/evidence/cheat_collection/{refactor_staged_manifest,refactor_ARM_gate,refactor_host_gate,refactor_measurement}.jsonとwork/logs/cheat_collection_refactor_*。
- 確度: source変換の静的・host照合はMEDIUM、ゲーム上の意味と現build一致はLOW/未検証。実ARのpayload先はhostでは拒否経路のみ、syntheticだけself-owned pageでbytes一致を確認。原資料の未定義取消/異常choiceは保ったままで試験から除外。動作や番地の実機適合が違えばゲーム上の仮説は反証される。実機/解析DB/正常3gxへは適用しない。

