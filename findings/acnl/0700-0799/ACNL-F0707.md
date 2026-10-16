---
id: ACNL-F0707
aliases: []
title: "Pane 木の可視走査と Layout 記録・Picture 描画（再解析）"
summary: "基底 Layout は可視 root の Pane 木を子リンク順に記録し、Picture は材質状態と幾何・色・UVをバッチへ追加する。頂点色の入力と TEV 構成、バッチ残量の検査とコマンド領域容量は別である。"
date: 2026-10-16
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: IDA
addresses: [0x5686d4, 0x4d7174, 0x73b524, 0x73b5bc, 0x73cb58, 0x4b8090, 0x4b7864, 0x4b7dec, 0x4b8790]
tags: [layout]
supersedes: ["ACNL-F0316"]
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: auto
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

再解析で確認。基底 Layout の記録メソッドは自身の root Pane を取り、可視なら Pane 自身→子をリスト順に巡回する。DrawSelf が返すローカル cursor を次の子へ渡し、木の最後に global cursorへ書き戻す。空の子リストでも root 自身の DrawSelf は別に実行され、素の Pane の DrawSelf はcursorを素通しする。

Picture の DrawSelf は Material/texture状態を発行し、行列・寸法/アンカー・UV・頂点色を描画作業体へ追加する。複数Pictureが同じMaterialポインタを持っても、幾何と色の入力元はPictureごとである。ただし最終色は材質のTEV構成にも依存する。

確度 MEDIUM：Layoutの記録呼出し、Paneの再帰命令、vtable実データ、Pictureの各入力と状態送出側を独立に照合。実機操作なし。

## 根拠

一次証拠：`_local/evidence/28/ida-primary.txt`、`ida-data.txt`、`ida-final.txt`、`ida-followup.txt`、`ida-vtable-check.json`。数値の検算は `calculation.json`。要求・保存再生・投影・上下別managerリストは既に再解析された [ACNL-F0693] [ACNL-F0696] [ACNL-F0699] を前提とする。

- Layout vtable `0x900608` は+0x08=`0x5682DC`、+0x14=`0x5686D4`、+0x18=`0x567BC0`。`0x568758/0x568788` のDrawer begin/endの間で、`0x568760..0x56876C` は `(drawer,layout+0x10,layout+0x30)` を `0x4D7174` へ渡す。
- `0x4D7190` は内部Layout+0x10、すなわち外側Layout+0x20のrootを取る。`0x4D71A4..AC` はroot+0xB7 bit0を検査する。最終cursorを `0x4D71C8` がglobalへ保存する。
- `0x73B530..48` はbasePosition+0xB6 bit4が立ち、計算後alpha+0xB5が0ならそのPane自身の描画を飛ばす。子走査は続く。`0x73B550` はvslot+0x68を呼び、`0x73B55C` は戻りcursorをR1へ。
- `0x73B560..9C` は番兵pane+0x14のnextを取り、各link+0xB3 bit0（実体pane+0xB7）を検査。実体はlink−4、次linkは `LDR R4,[R4]`。可視の子の再帰戻りを次のcursorにする。+4のnext/+8のprevと番兵はPane ctorの初期化、破棄時unlinkとも整合する。
- Picture vtable `0x8FBFFC+0x68` は `0x73CB58`、Pane `0x8FBE7C+0x68` は `0x73B5BC`（`MOV R0,R1; BX LR`）。F0316のslot番号26は確認。
- `0x73CB64..80` は+0x13CのMaterialを両状態関数へ渡す。Picture自身は第3引数のDrawInfoを読む前にR2を上書きするが、計算側の `0x4B6154` や他のPane派生にまで「DrawInfo不要」とは拡張しない。
- `0x73CC80..88` はPicture+0x80の行列をコピー、`0x73CCAC` はアンカー計算、`0x73CCD8..E4` は+0x48/+0x4Cを読む。`0x73CCF0..F8` はPicture固有の四頂点色+0x140と計算後alpha+0xB5を `0x4B8090` へ。`0x4B80E4..0x4B813C` は色をRGBA floatへ分解、`0x4B8170..74` はalpha倍率を掛ける。全白時の省略表現もある。
- `0x4B7A2C` 以降はMaterial+0x30 bits6–8で明示TEVの有無を分ける。非ゼロなら `0x4B7A5C` で `0x4B8790` のTEV送出へ。ゼロならtexMap使用数bits0–1で既定経路を選ぶ。texMap数1の状態切替では `0x4B7B8C..A8` が `0x97B704` から72バイト（18語）をコピーし、mat+0x10/+0x14を雛形の定数色欄へ入れる。差分が同じならこのコピーを省く。
- texMap数0の既定経路は `0x4B7A98` でmat+0x14を取り、差分時 `0x4B7B38` のヘッダ即値は **0x000F00FB**。旧F0313の「mode0でreg0x0DB」は反証。数1の差分経路 `0x4B7C18..38` はmat+0x10を0x0DB、mat+0x14を0x0F3へ出す。
- 既定雛形の末段データ `0x97B734..40` は `0x0FF00FF0 / 0x804F00F8 / 0 / 0x00010001`。色の入力・定数色・TEV経路が別であることは確認できるが、旧借用材質の全TEV設定と実画素は今回採取していない。
- `0x4B7878..0x4B78B8` はmat+0x4D bit1でMaterial状態の通常発行を省き、必要なら先行バッチをflushしてcursorを返す。呼出し元Pictureはその戻りから処理を続ける。従って「bit1でPicture全体がreturnする」は誤り。
- `0x73CD30..58` はバッチ内の要素数に対する閾値を調べ、超えそうならflushする。ここには記録managerのbase/end比較はない。コマンド領域の容量契約は [ACNL-F0701]。バッチの検査を理由に任意枚数・任意容量で安全とは言えない。

## 主張ごとの判定・訂正

| 旧記録の主張 | 判定 | 結果 |
|---|---|---|
| F0313/F0316/F0317 正規のPicture/木をゲームの記録関数へ渡す経路 | 確認 | 関数の引数・vtable・root参照・cursor連結を確認。旧外部オブジェクトが完全な契約を満たしたことまでは含めない |
| F0316 基底Layout vtableの描画/記録/投影slot、DrawSelfは+0x68 | 確認 | 実データと呼出し先が一致 |
| F0316 Pictureの30slot/Paneの28slot、DummyLayout slot16の工場 | 確認 | vtable配列の末尾と直後の0、DummyLayout+0x40の0x4B8D14を実データで確認 |
| F0316 子リスト番兵・link−4・可視bit0 | 確認 | ctor・走査・破棄と一致。親自身のalphaスキップは子を一律には隠さない |
| F0316 Layoutの必要欄は約10個、これだけで常に十分 | 一部訂正 | 記録関数の直読欄は確認。仮想呼出し先・Drawer・DrawInfo・記録manager等の前提を含めた普遍的な最小構造とは言えない |
| F0316 Picture自身はDrawInfoを使わない、他派生は別 | 確認 | 第3引数の直接不使用を命令で確認。行列計算側ではDrawInfoを読む |
| F0316 DrawInfo等にはvtableがなくRTTIだけ | 一部訂正 | この否定的な全域主張は未認定。対象のvtable/RTTIと実参照だけを採用し、全バイナリのvtable不在を主張しない |
| F0316 旧6Layoutが投影を0x5BE984で上書き、記録入口0x5686D0 | 一部訂正 | 基底/派生投影の区別は [ACNL-F0696]、NOP経由の基底記録は [ACNL-F0699]。旧個体がその派生だったとの実測は未追試 |
| F0316 mgr/vptr/寸法/RootPane/P_base_Lの旧実データ一致 | 一部訂正 | 静的構造は確認。旧ポインタ/表示/ヒープの再採取はしていない。寸法とアンカーは [ACNL-F0705]、キャッシュは [ACNL-F0706] |
| F0316 コードケーブ不要/旧実装と一致、F0317旧実装の撤去量と残存ケーブ | 一部訂正 | ゲームの記録処理の存在を確認。外部実装のコード量・撤去・最小性はゲームの事実の証拠から除外 |
| F0313 texMap数0はmat+20→reg0x0DB、数1はmat+16/20→reg0x0DB/0x0F3 | 一部訂正 | 数0のregisterは0x0FB。数1の対応と数2/3の別関数分岐は確認 |
| F0317 mat+16で変わらず頂点色で変わった、F0313借用TEVとの違いの原因 | 一部訂正 | 頂点色入力とTEV分岐は確認。任意材質で頂点色だけが支配するとは言えず、旧材質・実画像の因果は未追試 |
| F0317 mat+0x4D bit1でMaterial状態関数が早期return | 確認 | 状態発行だけを省く。旧「描画が止まる」は実画面依存の結果であり保証にしない |
| F0313 溢れ判定があるのでチャンク枚数制約が外れる | 一部訂正 | バッチ内の検査は確認。記録バッファ容量の保証ではない |
| F0317 記録長がキャッシュ次第で変わる、0x8000なら十分 | 一部訂正 | 差分により送出量が変わることは確認。旧0x3C0/0x440の値・十分との判断・安全量は未認定 |
| F0317 位置/寸法が指定画素、中央原点・1単位1画素 | 一部訂正 | [ACNL-F0696] の条件付きの式。旧画素範囲・旧投影16語・描画成功は未追試 |
| F0321 空の子リストだけが下画面不表示の原因 | 一部訂正 | 素のPane rootなら子が空で幾何追加がないことは確認。旧ノード状態・原因の唯一性・表示成立は静的IDBから再認定しない |

F0316 のゲーム側の構造・記録結論を本記録と [ACNL-F0705] [ACNL-F0706] [ACNL-F0708] [ACNL-F0696] [ACNL-F0699] に置き換え、旧実機追記を未追試として分離するため supersedes に含める。旧記録本文は変更しない。

## 訂正

旧F0313のtexMap数0の定数色送出先は0x0DBではなく0x0FB。bit1の早期returnとバッファ容量についても、状態関数・バッチ内の契約に限定する。

## 反証条件・未確認点

- 基底Layout/Pane/Pictureの経路に限る。可視フラグだけで最終画素の可視を保証せず、描画順・深度/ブレンド・テクスチャ・GPU提出も影響する。
- 旧自前木の3枚、list44、記録長、色、コード撤去後の安定、ロード後の25秒、74/110枚の表示は実機未追試。継続成功を全場面の保証へ一般化しない。
