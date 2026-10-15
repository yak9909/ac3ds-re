<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / actor

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| ACNL-F0075 | F-37 `FieldObj_InitFallActor` の `kind` が演出を決める — `HIGH` | `FieldObj_SpawnFallActor` は `FieldObj_InitFallActor(obj, item*, X, Y, kind)` を呼ぶ。 | HIGH | ? |
| ACNL-F0464 | 住民の AI（第 2 段まで）— 行動の要求・行動表・外の住民のクラス・家の出入り・花植え・傘（2026-09-29、MEDIUM: 静的＋Vapecord の使い方と一致。実機未観測） | 解析ソフト: IDA（主 IDB acnl、CRO の ELF の IDB outdoor）＋ Vapecord の NPC 機能 / 解析モデル: opus-5.5。 | MEDIUM | S |
| ACNL-F0520 | 灯り・プレイヤーの家（テント本体・柵・ポスト）まで全部を薄い青にできた。環境光に関係なく同じ明るさ（2026-09-23、HIGH（静的＋実機で表示確認）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「街灯の灯り部分も含めて色を変えられるか」「環境光に影響しないが本当か、奥の | HIGH | S |
| ACNL-F0564 | 手紙の ID 種別 3=名前差し込み無しのプレイヤー・4=同住民・6=自分自身（2026-09-18、MEDIUM） | 種別バイト（ID ブロック +0x30、手紙の宛先 +0x30・差出人 +0x64）: 1 プレイヤー、2 住民、3/4 はそれぞれ 1/2 を LetterId_DropNameTag 0x5CB85C が変えた値で、手紙テンプレートの本文展開後に名前差し込み位置（this+212）が負のとき宛先に適用（letter+0x26E=0 と対）。5 は ID なし（テンプレートの差出人はゼロクリア後に同関数で 5）。6 は自分自身＝未来の自分への手紙: 宛先選択 LetterU | MEDIUM | ? |
| ACNL-F0568 | 準備中の日替わり処理に掲示板・雑草・住民の引っ越しがある（2026-09-17、MEDIUM＋実機傍証） | Save_RunDayChange 0x114D18配下を静的に追跡。掲示板: Town_OnDayChange→Bbs_OnDayChangePworks 0x107F80（BBS_Pworks）、Town_OnDayChangeLate 0x103A18→Bbs_OnDayChangeEvents 0x107688（BBS_Event）。記事はBbs_BuildPost 0x302280→Bbs_AddPost 0x302300（TownBase+451128）。雑草:  | MEDIUM | ? |
| ACNL-F0639 | 村を通過する電車は位置状態を持つ `AcStrcTrain` オブジェクトである | **確度: MEDIUM（複数の独立した静的証拠。実機インスタンス未観測）** | MEDIUM | B |
| ACNL-F0653 | Ghidra-gpt-sol-5.6-F013 guardは遅すぎた — ActorFactory前にarmする必要がある | **確度: HIGH（Ghidra-gpt-sol-5.6-F013実機不成立＋hook命令順の静的再監査）。** | HIGH | B |
| ACNL-F0657 | menu-open中にstate 0x16から離れる最初のActor_SetStateを記録する診断AR | **確度: HIGH（hook構造/ABI静的検証。実機値取得待ち）。** | HIGH | B |
| ACNL-F0658 | shared page書込み可否とActor_SetState hook到達を分離診断 | **確度: HIGH（既存風船経路＋診断hook静的検証）。** | HIGH | B |
| ACNL-F0662 | Actor_SetState無条件hit + state 0x16 first-departure trace | Ghidra-gpt-sol-5.6-F023実機結果: |  | B |
