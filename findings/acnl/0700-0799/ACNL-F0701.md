---
id: ACNL-F0701
aliases: []
title: "記録 manager の容量・保存 offset と live cursor は異なる（再解析）"
summary: "manager のbase・容量・保存offsetとglobal cursorは別である。記録/主リストに有限の領域があるが、旧クラッシュ原因と安全量は未確定。"
date: 2026-10-16
category: ui
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses: [0x1216bc, 0x121988, 0x7b01cc, 0x7b05b0, 0x7b0694, 0x7afdd0, 0x4b7864, 0x4e97cc]
tags: [layout]
supersedes: ["ACNL-F0264"]
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

再解析で確認。manager は `+4=base`、`+8=コマンド領域のバイト容量`、`+0x0C=保存offset` を持つ。実際に書き込む cursor と終端は global にあり、保存offsetと常時一致しない。未知の非ゼロIDの選択は header だけを生成する。記録リストも主リストも有限のコマンド容量と別の GX エントリ容量を持ち、capacity 欄の変更だけでは領域は増えない。

確度 MEDIUM：選択、領域確保、書込、開始/終了、独立した Layout Build と主リスト生成の命令を照合。実機なし。旧F0257の容量超過→cursorゼロという因果は再認定しない。

## 根拠

数値・未改変確認：`_local/evidence/24/verification.json`。対象11関数の現在バイトとIDB original byteに差はない。

一次証拠：`_local/evidence/24/ida-primary.txt`、`ida-followup.txt`、`ida-lifetime.txt`、`ida-storage.txt`、`ida-calls.txt`、`ida-final.txt`。

| 対象 | フィールド/式 | 命令上の役割 |
|---|---|---|
| manager | +0x00 / +0x40 | ID / 同じbucketの次manager |
| manager | +0x04 / +0x08 | buffer base / コマンド領域のバイト容量 |
| manager | +0x0C / +0x14 | 保存offset / 提出済みoffset |
| manager | +0x18 / +0x1C / +0x20 | GX配列 / GX容量（件数） / 使用件数 |
| global | g_GpuCmdPtr / g_GpuCmdEnd | 現在cursor / コマンド領域終端 |

- `0x1216C4..0x1216F0` は `id&0x1F` のbucketを exact ID まで `+0x40` で検索。未知の非ゼロ ID は `0x12171C..0x121748` で `0x44` バイトのheaderを確保・ゼロ化してID等を入れるだけ。base/capacityは0のまま。未知の0は生成しない [ACNL-F0700]。
- `0x1217C0..CC` は切替前の `cursor-base` を旧managerのoffsetへ保存。`0x1217E8..FC` は新managerから `cursor=base+offset; end=base+capacity` を復元し、manager/baseが無ければ両globalを0にする。
- `0x121988` は storage の処理。既存baseがあれば callbackで解放し、`0x1219E0..F4` で `bytes+28*GX容量` を確保する。`0x1219FC` は容量、`0x121A18` はbase、`0x121A1C..2C` は `GX配列=base+bytes` とGX容量を保存。最後にcursor/endを再設定する。単なるcapacityの値変更は実領域を確保しない。
- Layout Build `0x568630..38` は第4引数をバイト容量として storage に渡し、GX容量は1。主リスト生成側 `0x4E9818..30` も同じ生成・選択・storageを使う。この初期化では `0x4E97FC` で2本、`0x4E9800/04` で各コマンド容量 `0x96000`、GX容量10を設定する。これは生成時容量であり、任意時点の残量や全リストの共通容量ではない。両者とも独立した有限の確保領域を持つ。
- clear `0x7B0210..48` は保存offset/提出済みoffset/GX使用件数等を0にし、global cursor/endをbase/base+capacityへ戻す。
- start `0x7B05C4..D0` はpadding前の `cursor-base` をoffsetへ保存し、`0x7B05CC..0x7B0600` はoffsetのbit3が立ちend>cursorなら8バイトを足す。その後のlive位置とGX使用件数を開始位置として控える。これは単に「8バイト境界へ合わせる」という旧コメントより、bit3の実条件で表すのが正確。
- Commit `0x7B06B0..BC` もpadding前にoffsetを保存する。`0x7B06C4..E0` の同じpadding後、`0x7B06E4..0x7B0720` は開始位置、`live cursor-base-start`、GX開始位置、GX件数差を出力する。従って Commit直後もoffsetとlive位置にpadding分の差があり得る。その後のリスト切替がoffsetを更新する。
- `0x4D7174..0x4D71C8` は木の走査の戻りcursorをglobalへ書き戻す。`0x568770` の時点の書込済み範囲は、正しい選択manager・base・cursorが整合する条件で `[base,cursor)`。長さは `cursor-base` で、managerの保存offsetやLayout保存長ではない。Drawer end/Commit後には追加書込があり得る [ACNL-F0699]。
- コピー送出例 `0x7AFE00..18` は `Mem_Copy(cursor,src,bytes)` 後にglobal cursorを進めるが、この分岐にはendとの比較がない。Materialの `0x4B7BA0/A4` も渡されたcursorへ直接コピーする。このため全書込が容量境界で安全停止するとは言えない。主リストの再生/提出の終端比較・未提出範囲は [ACNL-F0695] の条件付き契約。
- F0257の旧例では `LR=0x4B7BA8, R2=0x28, src=0x97B724` としたが、対象IDBの呼出し直前 `0x4B7B8C/98/9C` は `src=0x97B704, R2=0x48` を設定する。`0x4B7BA8` はこのコピー後のcursor加算である。旧レジスタ標本を本命令列の同一状態の確定証拠にはできない。

## 主張ごとの判定・訂正

| 元記録・主張 | 判定 | 結果 |
|---|---|---|
| F0264 LayoutListは子の記録slotを巡回し、Layoutは専用IDへ記録して後で再生 | 確認 | vtableデータ・巡回・生産/消費の命令で照合[ACNL-F0699] |
| F0264 未知ID選択はheaderのみ作りbufferを割り当てない | 一部訂正 | 未知の非ゼロIDに限定。未知の0はheaderも作らない |
| F0264 base/capacity/offsetとlive cursorの区別、途中のoffsetは古い | 確認 | 複数の保存点があり、Commitのpadding後さえ差があり得る |
| F0264 コピー長はcursor-base | 確認 | 選択managerとcursorが整合する瞬間の既書込範囲。最終再生長やGX配列全体の長さではない |
| F0264 NOPのraw wordと位置 | 確認 | 0xE320F000、木の記録後・end/Commit前 |
| F0264 0x1000→0x4000置換、used=0、1200ms、撤去/保持 | 一部訂正 | 旧実機/外部実装の標本は未追試。ゼロ長の成功から非ゼロコピー・表示・寿命の成立は導けない |
| F0257 記録リストには容量がある | 確認 | Buildとstorageの有限確保により確認。GX件数容量も別にある |
| F0257 容量を超えるとcursorが0になり落ちる | 一部訂正 | 境界を検査しない書込経路はあるが、超過時に必ず0にする処理は示されない。旧クラッシュの因果は未確認 |
| F0257 LR/R2/転送元の旧標本 | 一部訂正 | 指定IDBの同一呼出し直前の命令とR2/転送元が一致しない |
| F0257 19チャンク/133枚、2チャンク長時間安定、6なら安全 | 一部訂正 | 標本・安全量は再認定しない。コマンドのバイト量・GX件数・残量はその時点に依存 |
| topicsの主リスト容量・提出済みoffset・直接追記が提出に入る | 一部訂正 | 容量とoffsetの区別は確認。取り込みは[ACNL-F0695]の条件付きで、常時提出の保証ではない |

F0264のゲーム側結論を本記録と [ACNL-F0699] で置き換える。F0257は外部実装のクラッシュ原因・安全量が中心なので全体の supersedes に入れない。対象外のF0259の実機標本は新たな根拠に数えない。

## 反証条件・未確認点

- 記録/主リストの実行時容量・残量・全コマンド書込の最大量、GX配列の枯渇時挙動、旧cursorゼロの発生地点は未確認。全エミッタの境界検査を網羅した記録ではない。
- バッファ置換は実施していない。base・容量・globalだけでなくGX配列位置、所有/解放callback、再生側参照、GPU処理中の寿命も別に確認が要る。旧プローブの安全性・拡張後の表示を保証しない。
- 実機では書込の前後でbase/capacity/offset/cursor/end、GX配列/容量/件数、保存範囲・提出済みoffsetを同時に採り、最初の不整合を特定する。非ゼロ記録のコピー・再生・解放の成立も未確認。
