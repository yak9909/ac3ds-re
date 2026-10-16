# Simulator の文字・数値キーボード移植（F-349）

2026-09-07。**コード・ホスト比較試験・3DS用ビルドまで完了。実機未適用。**
現行の描画基盤は `BASELINE/gui_spec_v3/README.md`。今回、ゲームの関数やアドレスの新規解析は行っていない。

## 使うところ

- プレイヤー → 名前を変更: 通常サイズの文字入力。
- UIテスト → 文字キーボード / 小型文字キーボード。
- 数値設定 → 所持ベル / アイテムID / 移動速度: Aで数値入力。
- 通知時間（slider項目）も今回は数値キーボードを開く。専用スライダーのバーは未移植。
- 十字キーでキーを選びAで入力。タッチでも入力できる。Bまたは取消で破棄。
- 文字入力欄をタッチするとカーソルが移る。かな/カナ・ABC切替、濁点/半濁点/小字、Caps/Shift、空白、長音、削除、8文字制限。
- 数値はDEC/HEX切替、符号、小数点、削除、上下限への丸め。floatはメニュー内部の1/10単位整数へ戻す。
- 通常の数値確定は編集値だけ更新し、Xで適用。適用済みホットキーから開いたときは、確定時に適用値も更新する。取消では両方を保持。

**名前変更はSimulatorと同じUIサンプル**。入力文字列をモジュール内へ保存して次回の初期値にし、通知を出す。ゲームのプレイヤー名を書き換える処理は追加していない。

## ファイル

| ファイル | 役割 |
|---|---|
| `Plugin/CTRPluginFramework-BlankTemplate-0.8.0/Includes/GuiKeyboard.hpp` | 固定容量の状態と公開API。`Result`が確定値を返す |
| 同 `Sources/GuiKeyboard.cpp` | 入力、編集、文字変換、描画。ゲームメモリには触れない |
| 同 `Includes/GuiKeyboardLayout.h` | **生成物。手編集禁止**。通常/小型×かな/QWERTY |
| 同 `Sources/GuiMenu.cpp` | メニュー項目、入力の優先順位、確定結果、ホットキーからの接続 |
| 同 `Sources/GuiV2.cpp` | 下画面容量の拡張、描画順の添字を`u16`へ |
| `PATCHES/export_keyboard_layout.py` | Simulatorの`textKeyLayout()`をNodeで実行して配列を生成。`--check`は読み取りのみ |
| `PATCHES/verify_keyboard_port.py` | 事前検査→実C++のホスト比較試験→実描画呼出の捕獲・予算検査・PNG |
| `PATCHES/keyboard_oracle.js` / `keyboard_host.cpp` | 元のSimulator / 移植したC++を同じ入力列で動かす |
| `PATCHES/build_keyboard_plugin.py` | **全検証とARM構文検査が通ったときだけmake**。実機転送は行わない |

生成物`GuiCavesV2.h`は`PATCHES/export_gui_v2.py`から生成。今回のケーブ変更は下画面`LIST_SIZE`の設定値だけで、フックとケーブの命令列は既存のもの。

## 容量と表示上の差

| 項目 | 移植後 |
|---|---|
| アトラス借用 | **0x9000 = 36,864 B（変更なし）** |
| プラグイン側の置き場 | 0x70000。配置401,664 B |
| Picture | 上74 / 下336、合計410 |
| 文字スロット | 上69 / 下76（下は1字×50、8字×24、16字×1、28字×1） |
| 下`LIST_SIZE` | 0x2D000。80%の安全弁147,456 B |
| 下スロット・矩形をすべて使った保守見積もり | 124,224 B。安全弁の範囲内 |
| 通常かな、初期値PLAYER、カーソル表示時 | 矩形332枚、文字68本、保守見積もり110,208 B |
| 通知 | 5件のまま |
| 3gxのELF内訳 | text 648,996 / data 7,380 / bss 511,296 B |

F-347の「2枚重ね」は今回採用していない。不透明な縁の上に半透明の内地を重ねるだけでは、内側の背景透過が失われる。既存のF-323と同じ**縁4辺＋内地1枚、重なりなし**とした。これに合わせて`oIdx`とその代入キャストを`u16`へ拡張した。`oKind`は0/1だけなので`u8`のままでよい。

Simulatorの角丸は、既存GUIと同じ矩形枠で表示する。配置・ラベル・書体・色・フェードはSimulator由来。文字キーの押下色はタッチを離すと消し、十字キー操作時には選択キーを表示する。

数値バッファは20桁まで。DEC/HEX切替時には`s32`の範囲へ収めてから整数変換し、過大入力による未定義動作を避ける。通常のUI項目の範囲ではSimulatorの編集結果と一致する。

## 検証とビルド

```
python PATCHES/export_keyboard_layout.py --check
python PATCHES/verify_keyboard_port.py --preflight
python PATCHES/build_keyboard_plugin.py
```

ビルド入口は以下が全て成功した場合だけ`make`を呼ぶ。

1. 生成配列の照合、文字の網羅、添字の型、固定容量、入力と結果の接続。
2. 既存`verify_plugin_port_v2.py`の8群、`verify_spec_v3.py`、`batch_cost_exact.py`（保存済み実機23点の自己検査）。
3. **移植したC++と元Simulatorの10,943入力遷移を比較し全一致**。濁点等の往復・カーソル編集・Caps/Shift・モード切替・8文字・取消/確定・数値範囲・可変列数の移動を含む。
4. タッチの立ち上がり、押しっぱなしの二重入力防止、カーソルタップ、過大入力の保護。
5. **実C++から捕獲した15描画場面**。字形欠け・描画領域外・文字スロット不足・記録予算超過なし。かな/カナ/QWERTY/Caps/Shift×通常/小型、数値3形式、フェード中、閉じた後。
6. Simulatorの既存48テスト。
7. 実3DS用ヘッダーで`arm-none-eabi-g++ -fsyntax-only`。
8. 検証前後・ビルド後でソースのSHA-256が変わっていないこと。

MSYS2の`/tmp`にはサンドボックスから書けないため、一時ファイルは` scratchpad/keyboard_port_qa/tmp`に置く。devkitProのMSYS2ログインシェルと`make -j1`を使う。

ログ、描画呼出JSON、PNG、検証結果、ソースと成果物のSHA-256:
**`scratchpad/keyboard_port_qa/`**。`build_manifest.json`の`hardware_applied`はfalse。

成果物: `Plugin/CTRPluginFramework-BlankTemplate-0.8.0/gohan.3gx`（840,545 B）。
SHA-256: `d5a43a7313e286d3c916f01fede0c9ede0ac0b57c2e4d5900acf499cec1c9116`。
ELFは再リンクされ、`GuiKeyboard::OpenText/OpenNumber/Handle/Draw/TakeResult`のシンボルを確認した。

## 実機適用の前と後

**この作業では実機へ書いていない。デバッガ状態も取り直していない。**
適用前に上の検証を再実行し、成果物のハッシュを照合する。新しい`.bss`配置を持つため、稼働中の旧版へキーボード部分だけを注入せず、新しい3gxでゲームを起動する。

適用後は次を確認する。まだどれも実機確認済みとして扱わない。

- 通常/小型のかな・カナ・QWERTY、濁点/半濁点/小字、カーソル編集と8文字上限。
- タッチの座標と1回押下、十字キーとA/B、フェード・取消・再オープン。
- DEC/HEX/小数の入力、上下限、確定と取消、通常はX適用・ホットキーでは確定即適用。
- メニューが閉じているときにホットキーから開閉して、下画面が残らないこと。
- **キーボードを表示しながら手紙を開くこと**、表示負荷、場面転換、GUIのON/OFF。

実機確認済みの戻り先は **`BACKUP/plugin_full_20260907_f346/`**。
今回変更前のファイルとELF/3gxは`BACKUP/keyboard_port_before_20260907/`にも保存した。
実機が通るまで、この移植版を基準仕様や実機確認済みバックアップに昇格しない。
