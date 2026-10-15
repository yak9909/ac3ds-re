<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / actor

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| ACNL-F0043 | F-05 アニメ名テーブル基準は `0x0085FFB0` — `HIGH` | 16B × 約1028（終端未検証）。`+0` 未使用 / `+4` 本体名 / `+8` `_e1` / `+12` `_m1`。 | HIGH | ? |
| ACNL-F0044 | F-06 アニメ再生速度は VFP の S1 — `HIGH` | `Actor_PlayAnim` (`0x0068D0EC`) の引数: | HIGH | ? |
| ACNL-F0046 | F-08 アクター状態テーブルは基準 `0x00843634` / エントリ `0x1C` — 基準は `HIGH` / 個々の割り当ては混在 | 状態 N のエントリ関数 = `[0x843634 + N*0x1C]`。 | HIGH | ? |
| ACNL-F0053 | F-15 `Player_StartFieldAction` の呼び出し規約 — `HIGH` | `0x598660`-`0x598688` の assembly から確定。 | HIGH | ? |
| ACNL-F0056 | F-18 `Player_StartFieldAction` の呼び出し元は 16 箇所 — `HIGH` | `0x590000`-`0x5B0000` の BL 全走査で 16 件。 | HIGH | ? |
| ACNL-F0075 | F-37 `FieldObj_InitFallActor` の `kind` が演出を決める — `HIGH` | `FieldObj_SpawnFallActor` は `FieldObj_InitFallActor(obj, item*, X, Y, kind)` を呼ぶ。 | HIGH | ? |
| ACNL-F0104 | F-66: オンライン髪型変更は虫取り網アクションから美容室状態 `0xB9` への迂回 | confidence: **MEDIUM**（独立した複数の静的経路で一致。実機・通信相手を使った動的検証は未実施） | MEDIUM | ? |
| ACNL-F0105 | F-67: 髪型変更状態 `0xB9` が帽子・アクセサリを消し、2 段アニメが反映を遅らせる | confidence: **MEDIUM**（削除先・同期先・アニメ分岐を静的に確認。提案パッチは実機未検証） | MEDIUM | ? |
| ACNL-F0106 | F-68: オフラインなら profile の HairStyle だけを書いて `vc_UPDATE` すれば即時・装備保持にできる | confidence: **HIGH**（静的経路に加え、オフライン実機で即時反映・衣装8枠維持を確認） | HIGH | ? |
| ACNL-F0442 | アニメ機構は ModelInstance_Create の引数で作られる（**a5 ではなく a6。IDA-opus-5-F015 で確定**）（2026-09-21、HIGH、実機A/B） | 解析ソフト: IDA / 解析モデル: opus-5。**同じ資源・同じモデルで第5引数だけ変えた対照実験**を実機で行った。 | HIGH | ? |
| ACNL-F0458 | 模様替えカーソルは大きさを変えていない。V2-F019 の「範囲の形」は誤り（2026-09-21、HIGH、静的） | 解析ソフト: IDA / 解析モデル: opus-5。**既存記録 V2-F019 の訂正**（`work/evidence/unit_cursor/README.md` §5.3〜5.4、 | HIGH | ? |
| ACNL-F0463 | ゆうめいなキノコで大きくなる仕組みと、プレイヤーの大きさは通信に乗らないこと（2026-09-30、MEDIUM: 静的＋Vapecord の送信側の形と受信側の独立一致。実機未観測） | 解析ソフト: IDA（主 IDB）/ 解析モデル: opus-5.5。利用者の問い: 椅子の座る高さはオンラインに反映される（他人にも見える高さ変更チートがある）。 | MEDIUM | S |
| ACNL-F0464 | 住民の AI（第 2 段まで）— 行動の要求・行動表・外の住民のクラス・家の出入り・花植え・傘（2026-09-29、MEDIUM: 静的＋Vapecord の使い方と一致。実機未観測） | 解析ソフト: IDA（主 IDB acnl、CRO の ELF の IDB outdoor）＋ Vapecord の NPC 機能 / 解析モデル: opus-5.5。 | MEDIUM | S |
| ACNL-F0520 | 灯り・プレイヤーの家（テント本体・柵・ポスト）まで全部を薄い青にできた。環境光に関係なく同じ明るさ（2026-09-23、HIGH（静的＋実機で表示確認）） | 解析ソフト: IDA / 解析モデル: opus-5.5。利用者の依頼「街灯の灯り部分も含めて色を変えられるか」「環境光に影響しないが本当か、奥の | HIGH | S |
| ACNL-F0564 | 手紙の ID 種別 3=名前差し込み無しのプレイヤー・4=同住民・6=自分自身（2026-09-18、MEDIUM） | 種別バイト（ID ブロック +0x30、手紙の宛先 +0x30・差出人 +0x64）: 1 プレイヤー、2 住民、3/4 はそれぞれ 1/2 を LetterId_DropNameTag 0x5CB85C が変えた値で、手紙テンプレートの本文展開後に名前差し込み位置（this+212）が負のとき宛先に適用（letter+0x26E=0 と対）。5 は ID なし（テンプレートの差出人はゼロクリア後に同関数で 5）。6 は自分自身＝未来の自分への手紙: 宛先選択 LetterU | MEDIUM | ? |
| ACNL-F0568 | 準備中の日替わり処理に掲示板・雑草・住民の引っ越しがある（2026-09-17、MEDIUM＋実機傍証） | Save_RunDayChange 0x114D18配下を静的に追跡。掲示板: Town_OnDayChange→Bbs_OnDayChangePworks 0x107F80（BBS_Pworks）、Town_OnDayChangeLate 0x103A18→Bbs_OnDayChangeEvents 0x107688（BBS_Event）。記事はBbs_BuildPost 0x302280→Bbs_AddPost 0x302300（TownBase+451128）。雑草:  | MEDIUM | ? |
| ACNL-F0596 | ACNL の見た目の記録と色の表。HHD の番号がそのまま使える（2026-10-05、MEDIUM〜HIGH: 静的 2 経路（命令の復元と HHD のデータ）の一致。実機での反映は未） | 解析ソフト IDA（idalib-mcp）、解析モデル opus-5.5。段階 3（プレイヤーへの反映）。利用者指示: 反映するのは髪型・髪色・目の形・目の色・肌の色、まずオフラインだけ。 | MEDIUM | S |
| ACNL-F0601 | 目の色は頭のキー、目の形は作るときだけ — 複製の目をすぐ反映する方法（2026-10-05、MEDIUM: 静的のみ。gohan は実機未確認） | 解析モデル opus-5.5。IDB: `PlayerFaceSlot_RequestLoad 0x2711AC` / `PlayerFaceSlot_Unload 0x2711A4` を命名・注記。 | MEDIUM | S |
| ACNL-F0604 | 相手側のアクセサリーを残す状態 0xBA、送れなかった件（2026-10-06、MEDIUM: 静的のみ。gohan 未実機） | 解析モデル opus-5.5。IDB: `PlayerState_HeadGoodsExit 0x68A6AC` / `PlayerState_HeadGoodsSyncRemote 0x68C538`（関数を定義）を命名・注記。 | MEDIUM | S |
| ACNL-F0639 | 村を通過する電車は位置状態を持つ `AcStrcTrain` オブジェクトである | **確度: MEDIUM（複数の独立した静的証拠。実機インスタンス未観測）** | MEDIUM | B |
| ACNL-F0640 | パチンコ弾はPlayer内の固定3スロットで管理される | **確度: MEDIUM（複数の独立した静的証拠。実機メモリ観測は未実施）** | MEDIUM | B |
| ACNL-F0647 | 持ち物画面はBsMenuItem UI stateとPlayer state 0x16の二重state machineで成立する | **確度: HIGH（添付Ghidra XML/bytesの独立静的解析＋実機state観測）。state 0x16→0x06のcallerだけ未確定。** | HIGH | B |
| ACNL-F0653 | Ghidra-gpt-sol-5.6-F013 guardは遅すぎた — ActorFactory前にarmする必要がある | **確度: HIGH（Ghidra-gpt-sol-5.6-F013実機不成立＋hook命令順の静的再監査）。** | HIGH | B |
| ACNL-F0657 | menu-open中にstate 0x16から離れる最初のActor_SetStateを記録する診断AR | **確度: HIGH（hook構造/ABI静的検証。実機値取得待ち）。** | HIGH | B |
| ACNL-F0658 | shared page書込み可否とActor_SetState hook到達を分離診断 | **確度: HIGH（既存風船経路＋診断hook静的検証）。** | HIGH | B |
| ACNL-F0660 | AcBalloon terminal dropがPlayer state 0xA4 reactionを明示要求し、desired=0x06へ戻る | **確度: HIGH（実機trace＋ModuleVillage.cro＋main static call chainが一致）。** | HIGH | B |
| ACNL-F0662 | Actor_SetState無条件hit + state 0x16 first-departure trace | Ghidra-gpt-sol-5.6-F023実機結果: |  | B |
