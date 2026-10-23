---
id: ACNL-F0723
aliases: []
title: "SELECTとSTARTの条件付き統合と読み替え前のSELECT除去"
summary: "0x003533D0は0x009778D8が0のときだけ0x00483020を呼び、SELECTをSTARTへ統合する。読み替え前のpad held/pressed/releasedのbit2を除去すれば、STARTと通常の読み替え呼出しを保持してSELECTだけをゲームへ渡さずに済む。"
date: 2026-10-19
category: input
build: acnl_jpn_v15
confidence: MEDIUM
tool: "関数書き出し / codebytes / 元ARMのUnicorn実行 / IDA型反映"
addresses: [0x003533D0, 0x00483020, 0x0053F550, 0x00540870, 0x009778D8]
tags: [button, sead]
supersedes: [ACNL-F0381]
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6.1-sol
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: ["ACNL-F0737"]
---
## 結論

再解析でSELECT→STARTの上流処理を確認した。ただし**条件付き呼出し**であり、edgeにも統合処理がある。
`GameInput_ReadPadState+0x110` (`0x003534E0`) は `BLEQ GameInput_MergeSelectIntoStart` (`0x00483020`)。
この呼出しを維持したまま、その前のpad `held/pressed/released` からSELECT `0x4` だけを除けば、通常のSTART `0x8` を保持できる。
MEDIUM。pad producer、読み替え命令、下流bit変換の独立した静的根拠を照合し、元ARMを用いた全16種類の新旧SELECT/START状態遷移をCPUで確認した。今回の実機検証はない。

## 根拠

### 読み替え前の場所と条件

- `sead_CtrHidDevice_Calc` (`0x0053F550`) は `0x0053F568` で `GameInput_ReadPadState(reader, device+0x15C0)` を呼ぶ。
- `GameInput_ReadPadState` (`0x003533D0`) はR4に出力pad、R5にreaderを保持する。pad先頭は `uint32 held, pressed, released; int16 circle_x, circle_y`。
- `0x0035346C..0x00353490` は現在heldとreader `+8` の前回heldからpressed/releasedを生成する。
- `0x003534C8..0x003534CC` は**読み替え前**heldをreader `+8` に保存する。その後のSELECT除去は、このreaderの保存値には遡及しない。
- `0x003534D0..0x003534D8` はbyte `0x009778D8` を読み0と比較し、`0x003534DC MOVEQ R0,R4`、`0x003534E0 BLEQ 0x00483020`（元語 `0x0B04BECE`）を実行する。
- したがって `+0x110` は**EQの場合にしか通らない**呼出し点。フラグ非0の経路でもSELECTを消す目的には、読み替え前だが条件分岐前の `+0x100` (`0x003534D0`) が共通の位置になる。ここはPC相対LDRなので、移設時も元のliteral `0x009778D8` を読む意味を保持する必要がある。
- `+0x110`を差し替える場合はEQ条件と元の読み替え呼出しを保持する。無条件化は元ゲームの分岐を変える。
- byteの用途・writerは今回未解明なので、`0x009778D8` 自体に推測名を付けない。

### 0x00483020 が実行する統合

- `0x004830AC..0x004830C0`: heldのSELECT bit2があればbit2を消しSTART bit3を立てる。
- `0x00483030..0x004830A8`: pressedとreleasedのbit3を、同時に与えられた**読み替え前held**と当該edgeのbit2/3からそれぞれ決める。
- `0x004830C4..0x004830D8`: pressed/releasedからbit2を消す。他のbitは保持する。
- edge `e` に対し、bit3を立てる条件は `(e & 0xC)==0xC || ((e & 4)!=0 && (held & 8)==0) || ((e & 8)!=0 && (held & 4)==0)`。それ以外はbit3を消す。
- SELECT単独の押下・解放はSTART edgeになる。もう一方を保持中に片方を押す/離す場合はedgeを抑える。一方、新旧がSELECTのみ→STARTのみと同時に入れ替わる遷移ではpressed STARTが出る。単純な「両ボタンのORの変化」だけでは表せない。
- 全16遷移で元ARMの結果を確認した。三語のbit2を除去したケースでは、STARTのheld/pressed/releasedのみが保たれた（`native_replay.json`）。

### SELECTだけを別用途に確保できる境界

入力形式はこのpad層でSELECT=`0x4`、START=`0x8`。後段 `sead_CtrController_UpdateFromDevice` は `0x00540938..0x0054094C` でSTART→held `0x800`、`0x00540A28..0x00540A3C` でSELECT→held `0x1000` と別々に変換する。
読み替え済みのheld `0x800` だけから、どちらが原ボタンだったかは復元できない。ここでSTART bitを消すと本物のSTARTも消える。

読み替え前padの三語からbit2を除去して元の読み替えを呼ぶと、SELECT由来のSTARTは生成されず、物理START由来のbit3は残る。
readerの前回heldにSELECTが残っていても、このフレームのreleasedからbit2を除去するのでSTART解放へ化けない。フィルターを途中から有効にした場合の既存の下流heldは別の状態問題であり、ACNL-F0721の旧状態整合と区別する。
SELECTをメニュー開閉等に使う読取りは、この加工より前の値または独立したHID値を読む必要がある。このpad出力や読み替え後のcontrollerを読むだけでは、そのSELECTを得られない。
これはゲーム側の入力境界の事実であり、特定製品の更新順や1フレームの遅延を保証するものではない。

証拠: `_local/evidence/103/exports/003533D0_sub_3533D0.txt`、`00483020_sub_483020.txt`、`0053F550_sub_53F550.txt`、`00540870_sead_CtrController_UpdateFromDevice.txt`、`manifest.json` と `native_replay.json`。

## 訂正

- ACNL-F0381の「ゲームはSELECTを完全に消す」は、`0x009778D8==0` で当該関数を通る経路に限定する。フラグ非0なら読み替え呼出しは無い。
- 旧記録の抜粋はpressed/releasedのSTART統合処理を省略していた。bit2の消去だけでは関数全体を説明できない。
- 「sead層では原理的に区別できない」は読み替え済みの場合に限る。非実行経路では下流にSELECT `0x1000` が届き得る。
- 旧プラグインの更新がゲームより後であること、利用者の実機成功報告、`0x009B7010` の制御byte割当ては今回の一次証拠では確認していない。

## 反証条件・未確認点

- byte `0x009778D8` のwriter、意味、場面ごとの値は未追跡。フラグ非0経路も含めるなら条件付き呼出し点だけでは不十分。
- 他のpad読取り経路・別ビルド・特定メニュー製品のHID読取り順は未確認。
- 実機でSELECT/STARTの単押し・重ね押し・同時入替え、加工の有効化直前/解除直後を検証していない。
