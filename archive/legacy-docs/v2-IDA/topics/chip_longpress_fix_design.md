# チップ長押し窓と選択アニメの修正

IDA / gpt-6.1-sol / 2026-10-10、IDA-gpt-6.1-sol-F017/T004。日本語無印ACNL＋更新、F016の利用者実機不具合を受けた設計補正。

## 根拠と変更方針（実装前）

- ModuleFtrのFtrRec_Get（0xB1D244）は112件のstatic `.bss` 表 g_FurnitureRecords（0xB480D4）を32B刻みで返す。登録側0xB1CF44も同じ表の+4へactor参照を格納する。F016のHeap(rec)は正規recordを拒否する。handleを[0,112)で検査したうえで、返値の非null/整列/参照先read permissionを検査する。actorには従来のheap/完成検査を維持する。範囲外handleはnativeがrecord0へ丸めるため呼出し前に拒否する。
- Chip_Select_Calc（0xB429BC）はselectFrames(+1092)=0時にアニメ5/6を開始し、終了時にunbindする。押下を維持するとcounterを増やし、6以上または24以上の移動でdragへ進む。F016の毎frameゼロ書込みはアニメを再bind/resetし続ける。ゼロには戻さず、5を超えたcounterだけ5へ制限する。最初のアニメが進み、長押し18frameまでdragへ進まず、24移動と短いreleaseのnative経路は維持される。
- CancelSingleSelection→UpdateChipParentsAfterDrop→選択pointerゼロ→EditorのPMF待機→既存ItemSelectWindowを開く、という経路は維持する。ゲームの描画frame callbackで監視する。既存native状態表/Select/取消/親整理を実コードで検査し、必要なworld/resourceサービスだけ明示模擬する。

## 検証と配布

旧ELFでstatic record拒否とアニメ反復を再現、新ELFで窓/A複製/B取消/PMF復帰・短tap/24移動・範囲外record拒否を検査する。原CROから独立照合したARMとリンク済みC++を使い、ABI/SP/VFP/全分岐・リテラル/領域/hash/しずえも確認する。DBへ型/コメント/確定名を反映・保存し最新XMLを出力する。新変更はsrc/gohanのwork/chip-longpress-fixへpush、実機未確認/main未反映。実機書込み/Resumeは行わない。
