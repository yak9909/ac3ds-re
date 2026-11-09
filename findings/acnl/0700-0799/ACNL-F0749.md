---
id: ACNL-F0749
aliases: []
title: "住民日次処理・出口遷移・苗の枯死処理の呼出契約と番地"
summary: "住民日次処理ラッパー・プレイヤーセーブ番号・現在部屋の出口遷移、および ID 3/4 に置換する苗の枯死処理を命名した。Room_UseExit の第6引数は整数フラグで、旧記録の float 説を訂正する。"
date: 2026-11-09
category: system
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 0x0030C994
- 0x00309F18
- 0x005B464C
- 0x00956231
- 0x00316344
- 0x003163C4
tags: [player, save-data, map]
supersedes: [ACNL-F0388]
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

日本版更新ビルドの以下の呼出契約と範囲を、関数本体・独立した呼び出し元・転送先の命令列から確認した。確度は MEDIUM（複数の静的根拠。今回の実機測定なし）。既存の格付け ? の記録は手がかりだけに用いた。

| 実番地と範囲（終端を含まない） | symbols 名 | 契約 |
|---|---|---|
| `0x30C994..0x30C9B4` | `Villager_RunDailyUpdateOnce` | 無引数、住民日次処理を非強制で呼ぶ。公開する型は `void(void)` |
| `0x309F18..0x309F70` | `PlayerSave_GetSlotIndex` | `int(const void *player_array, const void *player_save)`。一致したスロット 0〜3、不一致/null は 4 |
| `0x5B464C..0x5B468C` | `Room_UseExit` | `int(void *room_mgr, unsigned int exit_index, int transition_arg0, int transition_arg1, int transition_arg2, int transition_arg3)` |
| `0x956231`、1 byte | `g_VillagerDailyUpdateGuard` | `unsigned __int8`。非強制の住民日次処理を抑止するガード |
| `0x316344..0x3163A8` | `Field_GrowUpWiltSaplingToItem3` | 苗の対象ビットを落として、そのマスをアイテム ID 3 に置換 |
| `0x3163C4..0x316428` | `Field_GrowUpWiltSaplingToItem4` | 同様にアイテム ID 4 に置換 |

最初の3関数の型は ARM の `__fastcall` 表記（r0〜r3、残りは入口 SP のスタック）。後二つは Thumb 関数で symbols の先頭はそれぞれ `0x316345`、`0x3163C5`、サイズは双方 `0x64`。

`supersedes` は ACNL-F0388 の **Room_UseExit の第6引数を `1.0f` とした部分**に限る。CRO や実機成功の説明全体を取り消すものではない。

## 根拠

一次証拠は `_local/builds/acnl_jpn_v15/export/index.txt` とそこから指す全関数の書き出し（`symbols_commit: 4914ab98f271092df116b05c38a6183939b88b16`）。下記の関数名は同索引で検索できる。IDB は指定の作業用コピーで命名・型付けと境界確認にのみ用いた。

### 住民日次処理とガード

- `sub_30C994` は `0x30C998` で `Save_GetTownBase()` を呼び、`sub_2FB33C`（`0x2FB348/34C` の加算で town+`0x29220`）の結果へ 4 を加える。r1=r2=0 にして `0x30C9B0` で `j_Villager_DailyUpdateOnce` へ末尾分岐する。入力レジスタを読む前に置き換えるので無引数。
- 独立した呼び出し元 `sub_608DE0` の `0x608DEC` も引数を準備せず呼び、直後に r0/r1 を上書きする。内部本体の r0 はガードを飛ばす経路と処理を走らせる経路で異なり、安定した返値の契約は確認できないため、ラッパーの型は副作用用の `void` とした。
- `Villager_DailyUpdateOnce` の `0x30C9D0` は `LDRB` で `0x956231` を読み、非ゼロかつ第2引数が 0 なら本体を飛ばす。`0x30C9E2` は本体の**開始前**に `STRB 1`。
- `sub_110CF0` の `0x110CF4` と `sub_10F168` の `0x10F1CC` は同じ byte を 0 にする。従って「起動後永久に一回」「処理完了」のフラグとはしない。ガードが既に立っていても、本体入口では別の byte `0x956232` を 0 にする副作用がある。
- 本体は住民日次リセット・イベント抽選・誕生日郵便・住民配置/外出先等を呼ぶ。村全体の成長や準備処理すべてを実行する関数とは命名しない。

### プレイヤーセーブ番号

- `0x309F18` は r1=0 を拒否し、r0 と r1 の一致、r0+`0xA480`、r0+`0x14900`、r0+`0x1ED80` との一致でそれぞれ 0/1/2/3 を r0 に返す。それ以外は `0x309F68` で 4。データの内容は読まず、ポインタの同一性を判定する。
- 独立した使用例 `Mail_DeliverToMailboxNow` は `vc_D_GARDEN()+0xA0` と宛先プレイヤーセーブを渡し、返った番号を `Mailbox_GetForPlayer` に渡す。`Player_ApplyAbsenceBedHead` の `0x20C710` もセーブ配列とプレイヤーセーブを渡す。

### 現在部屋の出口と整数 ABI

- `0x5B4654/65C` は出口番号 r1 と第3引数 r2 を保存。`0x5B4660` は入口 SP+0/+4 の第5/第6引数を読み、`0x5B4670/74` で第4〜第6引数を新しいスタックに保存する。
- `0x5B466C` は `g_CurrentRoomId` を読む。`0x5B4680` は `sub_5B5798(mgr,current_room,exit_index,arg0,arg1,arg2,arg3)` を呼ぶ。
- 転送先は `0x5B57FC..5828` で現在部屋の出口表と出口件数を調べ、出口番号から 36 byte のエントリを選ぶ。その出口に対応する部屋/特殊遷移と位置へ進む。
- `sub_608D90` の `0x608DA4..DB4`、`sub_609534` の `0x609550..55C`、`sub_18E030` の `0x18E04C..58` は第5/第6引数のスタックに **整数 1 (`0x00000001`)** を格納する。
- 転送経路は `sub_5B5798` の第7引数 → `vc_RELOADFUNC` 第9引数 → `Room_RequestChange` 第6引数 → `Room_SetTransitionKind` 第5引数。最終的に **`0x605F38 STRB R4,[...0x94A3CE]`** で下位 byte を保存する。途中の `VLDR/VSTR` はビット列を運ぶだけで、float への数値変換はない。
- `Room_RequestChange` の `0x5B4248` は別の次引数を 0 にし、`Room_SetTransitionKind` の**第6引数（こちらは float、保存先 `0x94A3DC`）**へ渡す。これと出口ラッパーの第6引数を混同しない。
- 従って旧記録の `1.0f`（ビット列 `0x3F800000`、下位 byte は 0）と整数 1 は同じ契約ではない。名前付き型では第6引数を int とした。下位 byte の意味が未確認のため、4引数は `transition_arg0..3` とした。返値は下位関数の r0 をそのまま返し、全分岐の成功 bool とは保証しない。

### ID 3/4 への苗の置換と呼出命令

- `sub_316344` の `0x31635E` は `Item_InitWithId(...,3)`、`sub_3163C4` の `0x3163DE` は `Item_InitWithId(...,4)`。両者は r0=成長用コンテキスト、r1=マス記述子を保存する。
- 記述子の `+0` を半語配列の索引、`+0x10` をビットマスクとして、それぞれコンテキスト+`0xA54` / +`0xCD8` をクリアする。`+8/+0xC` の座標へ `Field_SetItemAtWorldXY(...,item,x,y,0)` を呼び、コンテキスト+`0x1464` の対象ビットも落とす。
- 呼び出し側 `Field_GrowUpWiltSapling` は `0x315A92` / `0x315AA6` で対応するビット配列を検査し、`0x315A9A` / `0x315AAE` から各関数へ進む。独立した配置検査コールバック `sub_116564` / `sub_116870` も外周や設置条件の不成立からそれぞれを呼ぶ。書込 ID と両経路が枯死処理の判断を支える。樹種名は未確定なので ID を名前に残した。
- `python tools/codebytes.py` で `0x316384..39C` と `0x316404..41C` を読み、書き出しと一致する Thumb `BLX` を確認。`0x316392` の命令は `E6 F7 DE EA`、`0x316412` は `E6 F7 9E EA`。

| 関数 | BLX 先頭 | 実先頭から | symbols の Thumb 番地からの差 | 次命令 / Thumb の LR |
|---|---|---|---|---|
| `Field_GrowUpWiltSaplingToItem3` | `0x316392` | `+0x4E` | `+0x4D` | `0x316396` / `0x316397` |
| `Field_GrowUpWiltSaplingToItem4` | `0x316412` | `+0x4E` | `+0x4D` | `0x316416` / `0x316417` |

旧 `vc_NEVER_WILT_CALLER_4/3` は呼出命令先頭のラベルとして残した。いずれも4 byte の命令全体が新しい関数範囲内にある。

## 反証条件・未確認点

- 実機の新しい測定は行っていない。上記 ABI と ID 3/4 への置換が異なる実機命令・引数・書込先なら再検証が必要。
- 4個の遷移引数の個別の意味、出口遷移の全経路の返値、ID 3/4 の樹種、成長コンテキストと記述子の完全な構造体型は未確定。後二関数には今回プロトタイプを追加しない。
- 住民日次処理ラッパーの `void` は安定した返値を公開しない型付けであり、機械語が r0 をゼロにするという意味ではない。
- 過去の実機成功・CRO イベントとの同一性は今回の MEDIUM の根拠に数えていない。動的なモジュール呼出しの引数を今回は取り直していない。
