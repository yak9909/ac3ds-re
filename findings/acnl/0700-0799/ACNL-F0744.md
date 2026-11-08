---
id: ACNL-F0744
aliases: []
title: "パッチ位置を含む関数と木の作業領域、および text ページ末尾の詰め物を識別した"
summary: "未命名のパッチ位置2か所の包含関数、木の打撃カウンタと4枠キュー、textページ末尾の詰め物を一次証拠で識別し、symbolsから引ける名前と型を付けた。"
date: 2026-11-09
category: system
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 0x00658EEC
- 0x0062E60C
- 0x00838018
- 0x009AE504
- 0x009AE15C
tags: []
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6.1-sol
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

日本版更新コードの下表の5領域を名前で識別できる。確度は MEDIUM（複数の独立した静的根拠。今回は実機を操作していない）。旧 vc_ ラベルは命令位置の別名として残す。

| 名前 | 半開区間・型 | 役割 |
|---|---|---|
| Player_TryDispatchFrameActions | [0x658EEC,0x6591C8), int(void *playerActor) | 毎フレームの入力・状態・フィールド動作の条件判定と呼び分け |
| Weather_GetCurrentType | [0x62E60C,0x62E730), int(void) | 部屋・日時・天気表に基づく現在天気の選択 |
| g_TextPagePadding | [0x838018,0x839000), u8[4072] | text実体の後から次のページ境界までのゼロ詰め物 |
| g_TreeHitCounts | [0x9AE504,0x9AEA04), u32[320] | 1マス2 bitの木の打撃数 |
| g_DropDataTable | [0x9AE15C,0x9AE1A4), DropData[4] | 18バイト×4枠のフィールドアクション要求・完了状態 |

## 根拠

### パッチ位置の包含関数

全関数書き出しの索引（symbols_commit `4914ab98f271092df116b05c38a6183939b88b16`）を使い、以下を命令列と呼び出し側で照合した。

- `sub_658EEC` は PUSH から各 POP PC まで、IDBの範囲も `[0x658EEC,0x6591C8)`。後ろの4語はリテラルで、次関数は `0x6591D8`。
  `PlayerState_UpdateFrame (0x653038)` の `0x653068` から呼び、内部で入力を調べ、`Actor_SetState`、`PlayerAction_DispatchTop`、フィールドオブジェクトの検索・動作開始を呼ぶ。戻り値は処理成立の1か、不成立の0。
  `vc_NOTRAPS1 (0x659160)` は関数先頭から `+0x274`、元語 `0x1A000014`。直前の `sub_682AF0(actor,1)` が返った後の条件分岐で、行き先 `0x6591B8` は return 1。単独で「落下判定関数」とは呼ばない。
- `sub_62E60C` は `[0x62E60C,0x62E730)`。`Date_GetRaw` と部屋IDを用い、`0x957FB0` の指定値または時間別の天気表を選び、通常経路では3→5・4→6の変換後に返す。
  独立した呼び出し側 `Weather_GetRainAmount (0x22A14C)` は、この関数の結果3と4をそれぞれ雨量32と128に変換する。
  `vc_WEATHER (0x62E728)` は `+0x11C` の `MOV R0,R4`（元語 `0xE1A00004`）で、直後の `POP {R4-R6,PC}` が通常経路の終わり。特殊部屋の早期returnはここを通らない。

### textページの詰め物

- `meta/builds.toml` とIDBの双方で `.text=[0x100000,0x838018)`、`.rodata` の開始は `0x839000`。したがって依頼で「.text末尾」と呼ばれた候補は、厳密にはtextセグメント実体の後のページ詰め物である。
- `tools/codebytes.py` の `read_bytes` に、ファイル配置上のこの隙間だけを明示的に含めて読み、`[0x838018,0x839000)` の4072バイトがすべてゼロであることを確認した（通常CLIはセグメント間の隙間を拒否する）。
- 全4072番地に対するIDBのコード・データxrefは0件。全初期化セグメントを1バイト刻みで32 bit絶対番地検索し、ARM B/BLの符号付き分岐先も全語で検査した。分岐候補は0件、内部へ向かう4バイト整列ポインタも0件。
- 例外は `.data` の `0x97803C` にある境界値 `0x838018`。直前 `0x978038` は `0x100000` で、textの開始・排他的終端の組と一致する。詰め物内部のデータを指す根拠にはならないが、「範囲を値に持つデータが一切ない」とは言わない。
- 非整列の値一致は7件。6件はARM命令の末尾1バイトと次命令の先頭3バイトをまたぐ。残る `0x2880FB` は `0x2880F8` のリテラル `0x008EA4C0` と次の `0x00008388` をまたぐ偶然一致で、詰め物のポインタではない。
- IDBの未配置部分へ `.text_padding` セグメントを追加し、元ファイルと同じゼロを読み込み、全域を1配列にした。textの元の実体終端やゲームファイルは変更していない。

### 木の2リテラル

- `FieldObj_ResolveAxeAction (0x597CE0)` の `0x597D50–0x597D7C` は `t=X+80*Y-0x510`、`word=t>>4`、`shift=(t&15)*2` で `0x9AE504` の32 bit語から2 bitを読む。必要打撃数との比較結果と現在打撃数を `Item_PlaceItem` に渡す。
- 独立した `FieldAction_CanApply (0x59F830)` は要求内の打撃数と同じ2 bitを照合し、`FieldObj_RevertRecord (0x5A037C)` のcase 0xE/0xFは同じ位置を更新する。
- `sub_30808C` の `0x3080E0–0x3080E8` と `sub_5A19EC` の `0x5A19EC–0x5A19F8` は、別経路から共に先頭 `0x9AE504` と長さ `0x500` を `Mem_ZeroFill` に渡す。この長さと32 bitアクセスから `u32[320]` を適用した。
- `Item_PlaceItem (0x59E5B4)` は `0x9AE15C+i*18+15` が0の枠を4枠から探し、3個の4バイトItemID、座標、種別、状態、flagsを格納する。満杯なら -1、成功時は枠番号。
- 独立した `sub_596C84` は同じstrideで状態 `+15` を読み、完了・エラーの後に枠を戻す。既存型 `DropData` は実際に18バイトでこの配置に一致するため、既存定義を変えず `DropData[4]` を適用した。直後 `0x9AE1A4` の32枠テーブルとは別物。

### 再現用証拠

- `_local/evidence/121/static_scan.py`: codebytesでの詰め物読取りと関連書き出しの抽出。
- `_local/evidence/121/idb_probe.json`: 名前を付ける前の関数範囲・セグメント・xref。
- `_local/evidence/121/raw_scan.py` / `raw_scan.json`: 生ファイル上の絶対番地・ARM分岐検査と値一致の分類。
- `_local/evidence/121/select_symbols_delta.py`: 全体exportから依頼5番地の差分だけを採用。作業用コピーに元からある無関係の型・自動thunk名は持ち込まない。
- `_local/evidence/121/apply_names.py`: 作業用IDBへの名前・型・根拠コメントの適用。記録IDをコメント先頭に付けた。

## 反証条件・未確認点

- 実機での動的参照・書込みや、実行時に整数演算で生成される番地の不存在までは証明していない。初期コード・静的参照の範囲で詰め物と判定した。
- text終端の境界値は存在する。内部への到達経路や実行時割当てが見つかれば、ケーブの置き場としての判断は再検討する。今回の命名は実行時の安全性を保証しない。
- 木の実際の打撃回数・部屋ごとの天気の実測は追加していない。過去の ? 記録だけを根拠とせず、上記の命令と別の呼び出し側・初期化側を使用した。
