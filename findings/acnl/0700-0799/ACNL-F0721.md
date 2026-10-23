---
id: ACNL-F0721
aliases: []
title: "入力遮断点と旧状態の扱いを再解析：holdだけではreleaseが残る"
summary: "sead_Controller_Calc+0x30 は生入力更新後・edge計算前だが、current holdだけを消すとreleaseが残る。旧状態R8/R9は本体とWrapperの両方へ渡されるため、遮断対象は両方の旧状態でも除去する。"
date: 2026-10-19
category: input
build: acnl_jpn_v15
confidence: MEDIUM
tool: "関数書き出し / codebytes / 元ARMのUnicorn実行 / IDA型反映"
addresses: [0x0053CDC4, 0x00540870, 0x00542E88, 0x005475D4, 0x00542D78, 0x00543050, 0x005404AC]
tags: [button, touch, sead]
supersedes: [ACNL-F0376]
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

再解析で入力経路と欄を確認し、旧記録の「holdを削れば幻の離しも出ない」を訂正する。
`sead_Controller_Calc+0x30`（`0x0053CDF4`）は入力加工点として使えるが、現在値だけの変更では不十分。
同関数 `+0x24`（`0x0053CDE8`）は旧状態を引数へ複製する直前であり、本体と登録Wrapperへ渡す旧状態を一緒に整合させられる位置である。
確度 MEDIUM。生入力の書き手、edgeの計算、Wrapperの読取り・登録、vtableの独立した静的根拠を照合した。元ARMのCPU実行でも反例を再現したが実機測定ではない。

## 根拠

### 呼出しと順序

- `0x005404AC`（`sead_ControllerMgr_Calc`）は装置リストを仮想slot `+0x10`で更新した後、管理体 `+0xD8` のcontroller配列を同slotで更新する（`0x005404CC`、`0x00540504`）。
- CtrHidDeviceのvtable `0x008FE334+0x10` は `0x0053F550`。同関数は `0x003533D0` でpadを装置 `+0x15C0` へ、`0x00352514` でtouchを `+0x15D4` へ更新する。
- CtrControllerのvtable `0x008FE6F8+0x10` は `sead_Controller_Calc`、`+0x18` は `sead_CtrController_UpdateFromDevice`。
- Calcは `0x0053CDD0` で旧heldをR8へ、`0x0053CDD4` で旧pointer validをR9へ保存し、`0x0053CDE4 BLX R1` で生入力を更新する。
- `0x0053CDE8..0x0053CDF0` は `R2=R9, R1=R8, R0=R4`、`0x0053CDF4` は `BL sead_Controller_UpdateEdges`（元語 `0xEB001823`）。
- 後半 `0x0053CE84/0x0053CE8C` は再び `R2=R9, R1=R8` とし、登録Wrapperのslot `+0x10`を `0x0053CE90` で呼ぶ。
- Wrapperのvtable `0x008FF31C+0x10` は `0x005475D4`。`0x00549AB0` はsource `+0x14C` リストにWrapperを登録し、Wrapper `+0x144` にsourceを保存する。BsMenuMgr_Init `0x006D329C` は管理体の先頭controllerをこのsourceにする。
- Wrapperはsourceの現在heldを表 `+0x174` で写し、**引数の旧heldも同表で変換**して独自にedge/repeatを計算する（`0x00547620..0x0054764C`、`0x005476D4..0x005476F8`）。sourceのpressed/released/repeatを直接コピーしない。

### ボタン・タッチの欄（controller先頭基準）

| off | 意味・一次証拠 |
|---|---|
| `+0x00` | vtable。Calc `0x0053CDD8` がロードする。heldではない |
| `+0x04/+0x08/+0x0C` | pressed / released / repeat。UpdateEdges `0x00542F4C..0x00542F64` |
| `+0x10` | pointer flags。bit0 valid、bit1現れた瞬間、bit2消えた瞬間。bit3はSetPointerStateの座標リセット処理で消費される別フラグ |
| `+0x14/+0x18` | int画素X/Y。float `+0x114/+0x118` を切捨て変換 |
| `+0x2C` | uint32保持フレーム数[32]。押されていないbitはUpdateEdgesが0へ戻す |
| `+0xAC/+0xCC` | uint8 repeat開始遅延[32] / 間隔[32]。SetPadRepeat `0x00542B7C/0x00542B80` |
| `+0xFC` | ボタン数。初期化で最大32へ制限 |
| `+0x100/+0x104` | 2組の軸→方向bitの開始番号。CtrController ctor `0x00540B58/0x00540B5C` が両方-1にする |
| `+0x108` | pointer heldのbit番号。共通ctorは15を渡す。Wrapperは対応表に15が無ければ-1 |
| `+0x10C` | 入力idleフレーム数。Calc後半が無入力・addon判定に従って加算/クリア |
| `+0x110` | held。入力更新とSetPointerStateの両方が書く |
| `+0x114/+0x118` | float画素X/Y。無効化だけでは値の消去を保証しない |
| `+0x11C/+0x120` | 第1軸X/Y（スライドパッド）。`0x00540AB4` が正規化した値を書く |
| `+0x124/+0x128` | 第2軸X/Y。Ctr入力更新は0を書く。次の `+0x12C/+0x130` も0で、用途の断定はしない |

CtrController内のSTART=`0x800`、SELECT=`0x1000`、pointer=`0x8000`、スライドパッド方向=`0x00F00000`。
前二者は入力更新 `0x00540938..0x0054094C`、`0x00540A28..0x00540A3C`、pointerはctorとSetPointerState、方向は `0x00540A40..0x00540A94` から確認した。

### 一括消去が成立する契約と反例

UpdateEdgesは `pressed=newHeld & ~oldHeld`、`released=oldHeld & ~newHeld`、pointer edgeも新旧validから生成する。
CtrControllerの軸開始番号は-1なので、消したheldが軸から再生成される分岐には入らない。
現在heldと旧heldの遮断対象bitをともに0、現在validと旧validをともに0とすれば、対象のheld/pressed/released/repeatとpointer edgeは0になる。
現在heldが0なら、repeat出力だけでなく対応保持カウンターも0になる。

`+0x24`ではR4がcontroller、R8が旧held、R9が旧valid。現在held・pointer状態とR8/R9を整合させた後、元命令 `MOV R2,R9` を実行する契約になる。
既存位置 `+0x30`を使う場合はR0/R1/R2だけでなく、後半で再利用するR8/R9も同じ状態に整合させる必要がある。
通常の呼出し規約でR8/R9を保存・復元するだけの呼出し差替えでは、この目的を満たさない。
R8/R9の変更はこのCalc内部の生存値に対するもの。関数末尾の元POPは呼出し元のレジスターを復元する。

元ARMによる人工状態 `oldHeld=0x8001, oldValid=1, newHeld=0, newValid=0` の結果:

| 変更した旧状態 | 本体released / flags | Wrapper released / flags |
|---|---|---|
| なし | `0x8001 / 4` | `0x8001 / 4` |
| 最初の呼出し引数R1/R2のみ0 | `0 / 0` | `0x8001 / 4` |
| 保存値R8/R9を0（後続の引数も0） | `0 / 0` | `0 / 0` |

これはボタンとpointerの入力表現の遮断であり、移動の完全停止と同義ではない。方向bitを消してもアナログ `+0x11C/+0x120` は残り、Wrapperもコピーする。
また遮断解除時に実物が押されたままなら、前フレームの0との差から新しいpressedが出る。

証拠: `_local/evidence/103/exports/` の各先頭アドレスの書き出し、`manifest.json` のcodebytes元語・vtable・hash、`native_replay.json` と再現スクリプト `verify_input.py`。

## 訂正

- ACNL-F0376の「生読み直後にholdを削ればreleaseも出ない」は反証された。旧held/validとWrapperへの再受渡しが抜けていた。
- pointerは `+0x10` bit0だけではない。SetPointerStateは `+0x108` の番号を使いheldにも書く（詳しくはACNL-F0722）。
- `0x002E08F8` はpaneの付替え関数 `CommonButtonSingle_AttachTo`。`+0xD9`はこのobjectのpane付替えで0/1になるが、これを根拠に旧実機のButtonActionNodeEx配列へ同じ意味を移すことはできない。
- 旧記録の生アドレス `0x32C85A2D` とobject先頭・個数・strideの同定、CTRPFへの非影響の断定は今回の一次証拠では確認していない。

## 反証条件・未確認点

- 適用対象は日本版v1.5の上記controller経路。全ゲームの入力読取りを網羅した保証ではない。装置の生キャッシュやHIDを別途読む経路にはこの位置の加工は遡及しない。
- 実機での場面差、遮断開始・解除時のgesture状態、全Wrapperの列挙、別ビルドは未測定。
- 既に更新済みのTouchStateやUI独自のドラッグ状態は、controllerの値を0にしても過去の状態まで自動取消にはならない。
