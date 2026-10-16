# 通常チャットのキーボード入口（F-383）

## F-396更新: 現行ランチャーの配置

通常チャットからの内蔵キーボード起動・取消・「漢字テスト」確定と復帰は以前の実機で確認済み。
再起動後の再適用では、旧ケーブが現在のGUI v2 A2/Nと重なるため読み取り監査が拒否した。
SWKBDだけを次の配置へ移設し、検証後に実機へ適用済み。現行3gxはF-394のまま。

| 対象 | 現行値 |
|---|---|
| 通常チャットhook | `0x001938AC = 0xEB1A9253` → `0x00838200` |
| フレームhook | `0x005CE29C = 0xEB09A7E7` → `0x00838240` |
| ケーブ | `0x00838200..0x00838400`、512 bytes |
| control / config / template / shared | `0x009BDD00` / `0x009BE000` / `0x009BE400` / `0x009BF000` |
| ケーブSHA-256 | `9c35ea87007ed9983c07a3c9817bc6bdd5ed01ee750f44af001949c971dbd2c0` |

旧`0x00838D20`への適用・消去は禁止。保存した旧版は比較証拠としてのみ使用する。
`prebuild_verify_native_chat.py`が現在のGUIヘッダから常設/一時ケーブ6領域とBSS非重複を検査。
`verify_native_chat_relocation.py`が旧実機成功版との差を外部BL変位13語だけと確認し、宛先一致を検査。
全24分岐・12 LDR・5リテラル・12エミュレーション経路、IDB/実機6入口照合、
全書込み読み戻しと独立`verify_native_chat_live_installed.py`をPASS。
GUIコード/データ/入力/しずえhookが適用前後で不変。現在Suspend、移設後の起動は未実施。
証拠`SYSTEM_KEYBOARD/evidence/reboot_*`、詳細`scratchpad/MEMO_f396_swkbd_reapply.md`。

以下はF-383時点の入口解析記録。

2026-09-09。利用者指定により、内蔵キーボード起動の対象を通常チャットへ変更。
**フレンドチャットは使わない。第一候補は`0x001938AC`のBL。**
対象は日本語版無印、`code.bin.i64`。idalibでの静的解析とPC上の原本ARM検証のみ。
実機への接続・状態照会・適用、ビルドは行っていない。confidence MEDIUM。

## 入口

| 番地 | 役割 |
|---|---|
| `0x00193A40` | `BsMenuChat`初期化。入力mode=0、最大32 UTF-16単位、改行flag=0、出力先を設定 |
| `0x00193890` | `window In`のenter。子キーボードを生成 |
| **`0x001938AC`** | **`BL UiScreen_OpenById`。通常チャットに限定したフック候補** |
| `0x001938B0` | `STR R0,[R4,#0xDC]`。戻った`BsSkb*`を親+220へ保存 |
| `0x00528C60` | 全画面共通の`UiScreen_OpenById`。ここを無条件にフックすると他の入力も対象になる |

```text
0x00193890 PUSH {R4,LR}
0x00193894 MOV R4,R0
0x00193898 MOV R1,R0          ; parent = BsMenuChat*
0x0019389C LDR R0,[PC,#0x24]  ; literal 0x001938C8 -> 0x0088163A
0x001938A0 MOV R3,#0
0x001938A4 MOV R2,R3
0x001938A8 LDRH R0,[R0]       ; screenId = 0x23E (BsSkb)
0x001938AC BL 0x00528C60      ; original word 0xEB0E54EB
0x001938B0 STR R0,[R4,#0xDC]  ; child pointer; NOT the BL
```

呼出し時はR0=`0x23E`、R1=親、R2=0、R3=0。戻りR0は子ポインタ。
生成関数全体の戻り値は後続で上書きされるため、`0x193890`自体が子を返すとは扱わない。
`0x1938B4`以降は`[0x949D68]`のbit `0x80`だけを消す。元の処理を保つ必要がある。
フック内で同期的にAPT待機へ入る安全性は未確認。要求を記録して既存APT位置へ渡す方針は維持する。

## 通常チャットである根拠

1. **RTTIと仮想関数表**: `vtbl 0x8E5120`の直前が`TypeInfo 0x8C42A4`。
   その名前は`0x8CD6E5`の`10BsMenuChat`。init slot+12は`0x193A40`、update slot+36は`0x193BAC`。
   初期化は状態表`0x848BC8`の`window In` enter=`0x193890`を呼ぶ。
2. **メニューから画面生成まで**: 登録関数`0x1D3A84`と`UiScreen_Create 0x51FD2C`から、
   factory基準`0x94FDBC`、要素幅8を確認。`0x950FB4`のctor=`0x7EA97C`は224byteを確保し、
   `0x193C90`で`BsMenuChat`を構築。式`(0x950FB4-0x94FDBC)/8 = 0x23F`。
   初期化`0x787004`がメニュー表`[0x9863E4+2*5]`へ、この画面ID `0x23F`を設定する。
3. **確定文字列の消費先**: `0x1938EC`が親の文字列を`0x218044`へ渡す。
   後者はチャットオブジェクトの文字列・表示状態・プレイヤー欄を更新し、条件付きで送出関数を呼ぶ。
   `0x218044`のcode xrefは`0x193944`の1件。VapecordのSUBMIT_CHATというラベルだけを根拠にしていない。

```text
BsMenuTabの選択値6
  byte[0x85080C+6] = 5
  0x6D6338 / 0x6D7378 -> Menu_RequestOpen(menuId=5, 1)
  Menu_PollOpen 0x6D10A8 -> menu表[5] = screenId 0x23F
  UiScreen_OpenById -> factory 0x7EA97C -> ctor 0x193C90
  BsMenuChat init 0x193A40 -> window In enter 0x193890
  0x1938AC -> UiScreen_OpenById(screenId=0x23E, parent, 0, 0)
```

`0x6D6338`や共通Menu_RequestOpenは他メニューも使う。
今回の対象を限定するには、内側の`0x1938AC`が具体的。
選択値6の物理ボタン/タッチ座標との対応、全操作経路の実機発火頻度は今回観測していない。
以前調べた`0x336D38`の状態名`ChatOn`は別画面の処理で、キーボード生成入口の根拠にはしない。

## フレンドチャットと異なる返却後の動作

通常チャットもready=`0x9580E1`、result=`0xAD0278`を読むが、親の状態遷移が異なる。
出力は親+80のポインタ（構築時は親+88の内部バッファ）、文字列オブジェクトは親+76。
内部バッファ容量65と、入力設定の最大32は別の値。入力modeは**0**。

| 状態 | 通常チャットの処理 |
|---|---|
| 開く | `0x193850`がmenu flag `0x80`を待ち、子の入力フラグを戻して`Wait 0x193764`へ |
| result=2（確定） | `0x193764`→`send 0x1938EC`。enter=`0x57F890`で子の送信動作と入力フラグを設定 |
| 送信 | `0x1938EC`が子の状態を待ち、`0x218044`へ文字列を渡し、`0x522638`を呼んで次の状態へ |
| 送信後 | `send Wait 0x1939F4`で子の状態を待ち、入力フラグとreadyを戻し、再び`Wait 0x193764`へ |
| result=1（取消） | `window Out`へ。enter=`0x193988`が子vtable+0x44へ終了要求、calc=`0x1938D0`がglobal `0x94A654`の解除を待ち親を終了 |

**確定しても毎回閉じる構造ではない。** 入口`0x1938AC`は子生成時の呼出しであり、
送信後に同じ子で入力を続ける際に再度そこを通るとは言えない。
内蔵キーボードを連続入力でも開く実装には、初回生成と送信後の再入力を区別する必要がある。
前回F-382のフレンドチャット用consumer検証12ケースを通常チャットの検証済み根拠には流用しない。
`0x193988`はIDA上で独立関数未定義のため、状態表とassemblyで確認し、失敗したdecompileは根拠にしていない。

## 検証・残件

`SYSTEM_KEYBOARD/verify_normal_chat_entry.py`:
- 原本byteからRTTI、vtable、factory、メニュー対応、BL到達先、LDRリテラル2件を検査。
- 原本`0x193890`をPCで実行。子生成APIだけをモックにし、子戻り2種類×初期flag3種類の**6ケースPASS**。
  引数、LR、親+0xDC保存、flag更新、SP/R4復元を確認。OS呼出し・通信・実機アクセスなし。
- 証拠:`SYSTEM_KEYBOARD/evidence/normal_chat_static.json`。
  結果:`SYSTEM_KEYBOARD/evidence/verification_normal_chat_entry.json`（証拠SHA-256付き）。

通常チャットの全状態遷移をPC実行で検証したわけではない。
残件はフック実装、元入力との同期、文字列全置換、連続入力への対応、APT失敗回収、実機での起動/復帰確認。
実機に触れない指示を継続する。ビルド・適用を行う前には実装全体の検証が必要。
