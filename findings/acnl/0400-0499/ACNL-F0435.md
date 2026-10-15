---
id: ACNL-F0435
aliases:
- IDA-gpt-6.1-sol-F016
title: Editorキャッシュの再記録・チップ複製・内装保存/交換（2026-10-10、MEDIUM、実機未確認）
summary: '追補F017: 長押し窓と縞アニメは利用者実機で不具合。F016のnative Select/取消/親整理stub検査はstatic記録とアニメgateを覆えていなかった。上記F017の原ARM再現/修正で補正。他F016項目の実機結果は未報告。'
date: '2026-10-10'
category: _product
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: []
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:174-189
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F016: Editorキャッシュの再記録・チップ複製・内装保存/交換（2026-10-10、MEDIUM、実機未確認）

追補F017: 長押し窓と縞アニメは利用者実機で不具合。F016のnative Select/取消/親整理stub検査はstatic記録とアニメgateを覆えていなかった。上記F017の原ARM再現/修正で補正。他F016項目の実機結果は未報告。

解析ソフトIDA（idalib-mcp）/解析モデルgpt-6.1-sol。F015版は利用者実機で「チップだけ非表示、本体UIは残る」と確認されたため、本体も非表示になるというF015合成試験の結論を訂正。新変更の実機適用/Resumeは行っていない。

- 原mainのLayout_RecordPaneTree 0x5686D4はouterLayout+285のdirtyが0ならDrawPaneTreeへの到達を省き、保存GPU列を再利用する。0x568704の読取/0x5687B0のclearとCRO Editor_SubmitLayoutsのmain+664を独立照合。F015 alphaだけ＋cleanで本体描画を省く経路を原ARMで再現し、不透明度変更時のdirty再記録とResetでcache更新/復帰を確認（OS/GPUサービスは明示stub）。原因はMEDIUM、実機dirty実測はまだない。
- リスト中は生十字入力をnative方向bitへ変換し、mode25＋実Editor中のパッドも有効にする。速度2→6の3倍、yaw基底/斜め正規化/Y不変を保持。原Eye/linked pan63条件、list/menu/通常室内ゲート13条件と旧HHD493frame/20経路を照合。
- 長押しはnative Chip_Selectの開始点/counter/24移動閾値とcaller/state表を照合。安定押下18frameで単体選択取消→MapEditorと同じItemSelectWindow「複製/やめる」、短tap/dragはnative経路。EditorのPMF+52/+56を所有者固定の待機calcへ退避し、別Submitを維持して窓だけ更新。向き/リメイクを保つ共有TryPut/Spawnと新品chip rootを使用する。家具リストOFF/素材なしでも複製pendingを常設frameから進める。
- FieldMap2層anchorのItem flagsとactor全数を、native PopulateRoomのrecord組立/AcFtr CreatePrepareのmap書込で照合。12B記録とnative Footprint Init/Count/Offsetを定義。保存624B/8枠は壁紙・床variantを含め、版/長さ/checksum/全配置を検証する。native footprint20種は原ARMとraw descriptorに一致、実C++plan2000条件・file4992bit破損検査PASS。
- サイズ違いは共有16×16絶対anchorを保って全footprint/壁向き/上載せ親を検査し、範囲外の削除数を確認してから配置。actor state7の通常破棄→table空＋描画待ち→床/壁/上載せ生成→chip112枠再初期化/背景setterで、部屋の出入りを要求せず反映。変更前SD退避成功が破棄の前提。交換は反映成功後に旧部屋を枠へ戻し、枠の書戻し失敗は部屋も復元する。
- 新しい名前7main/3CRO、record/footprint/layout dirty/actor lifecycle/chip/editor PMFの部分型とenum・operand stroff・周辺コメントを保存。既存Item_GetCategory 0x2FCCD4とは概念が違うため0x2FCB64はItem_GetParamCategoryとして衝突を避けた。最新XML/bytes構文・参照・hashと保存DB再openの名前/型読戻しPASS、所有者0。実名・旧来歴は保持した。
- 関連225関数の全分岐/PC相対/境界/領域/hash/ABI、必須しずえ・字形欠字0、内装linked11条件（開/閉Editor、サイズ取消、生成/交換失敗復元、scene変更、長押し/窓/B/PMF復帰、catalog OFFでも実複製/チップ追加/解放保持）・SD21段階失敗・GUI確認3条件はPASS。リンク済み制御を実行するがworld/資源/FS/GPUの模擬を実機成功へ昇格しない。

根拠/反証条件は[設計](../docs/topics/interior_presets_design.md)と[report](evidence/interior_presets/report.md)、原命令native_assembly.json、調査survey_native.json、検査JSON/ログ。実機では本体fade/閉窓復帰、listカメラ、短tap/drag/長押し、家具flags/壁家具、内装save/load/swapとサイズ取消/clipを確認する。復元自体の資源生成失敗ではSD退避を保持して通知し、成功とは報告しない。

