# 3DS 内蔵ソフトウェアキーボードの調査（F-358 / F-359 / F-362 / F-363 / F-364）

**F-364更新:** ACNLのPrepare→Start→WaitとGPU/画面受渡し・復帰の契約を具体化。
CTRPFからもゲーム側の既存管理を利用する経路が第一候補。
原本ARMのIPC18ケース・既存caller ABI・実機の6コードアンカーを照合した。
具体的な引数、未適用の設定データ、失敗時の`err:f`等の残る条件は
[ACNL/CTRPFからの呼出し調査](system_keyboard_launch.md)。実機起動・取消・復帰の成功は未確認。

**F-363更新:** 原本ARMのPC実行で候補列挙・学習による順位変更・文節変換/境界指定を再現。
主要75,770件の頻度/品詞も全件照合して取得した。
詳細は[候補順位・文節変換](system_keyboard_conversion.md)。実機UIの順位との一致は未検証。

**F-362更新:** 利用者提供CIAをctrtoolで展開し、主要日本語辞書の読み・候補75,770件をCSVへ取得した。
全件を元のARM読取処理とPC内で照合し、不一致0件。
成果物・手順・残る範囲は **`DOCS/system_keyboard_dictionary.md`**。
辞書エントリの取得と、実機の表示候補の順位・文節処理・候補配列取得は区別する。

2026-09-08。依頼は既存作業の進捗確認と呼び出し可否の調査。
**今回、プラグインの実装変更・ビルド・実機への書き込み・再開は行っていない。**

## 利用者による目的の明確化（2026-09-08）

**目的は3DS本体に内蔵されたかな→漢字変換の辞書・変換候補を取得すること。**
そのため、内蔵ソフトウェアキーボードをとび森内またはCTRPFから呼べるかを調べる。
自前メニューへの組み込みは一切目的ではなく、`gohan.3gx`やその描画・入力設計に依存させない。
依頼されていない用途・組み込み先を前提として調査範囲を広げない。

利用者の知り合いには、とび森で内蔵キーボードを安全に呼んだ実績があるとのこと。
ゲーム側経由かCTRPF側経由かは不明。これは経路を探す手掛かりであり、呼べないと結論してはいけない。
前回の「現行CTRPFにAPT初期化がない」は初期化の相違点だけの証拠で、呼び出し不可能の証拠ではない。

## 結論

3DS 内蔵のソフトウェアキーボードには libctru の公開 API があり、文字入力と数値入力の公式サンプルもある。
とび森内またはCTRPFからの具体的な起動・結果取得・ゲーム画面復帰は、この調査では未検証。
呼び出し可否と、確定前の変換候補一覧の取得可否をそれぞれ確認する。

| 用途 | 公開 API の機能 | APIの範囲 |
|---|---|---|
| 日本語の文字入力 | `SWKBD_TYPE_NORMAL`。日本語本体で漢字入力には `SWKBD_PREDICTIVE_INPUT` が必要 | 変換機能を有効にする設定。候補一覧を返すAPIとは別 |
| 数値入力 | `SWKBD_TYPE_NUMPAD`。`swkbdSetNumpadKeys` で下段の追加キーを指定できる | 今回の漢字変換候補取得の対象外 |
| 戻り値 | `swkbdInputText` が確定/取消ボタンと UTF-8 文字列を返す | `SWKBD_BUTTON_NONE` の場合は `swkbdGetResult` を確認する |

初期値・ヒント・最大長・ボタン文言・予測入力・独自辞書を設定できる。
`maxTextLength` は UTF-16 コード単位、出力 `bufsize` は終端を含む UTF-8 のバイト容量。
「8文字だから出力バッファも8バイト」としない。言語は本体依存で、任意言語へ切り替えられるとは確認していない。
`SWKBD_FILTER_DIGITS` は数字だけを許す設定ではなく、数字の個数を制限する設定。

## 呼び出し経路と CTRPF の相違点

独立した証拠を突き合わせた:

1. devkitPro の公式サンプルは `swkbdInit` → 各設定 → `swkbdInputText` で文字/テンキーを呼んでいる。
2. 手元の libctru `swkbd.c` も、UTF-16 の共有メモリを確保し、
   `aptLaunchLibraryApplet(APPID_SOFTWARE_KEYBOARD, ...)`（ID `0x401`）を実行している。
   終了後は UTF-8 に変換して共有メモリを解放する。
3. 同 `apt.c` の `aptLaunchLibraryApplet` は APT 起動準備、VRAM 保存、画面転送、
   `GSPGPU_ReleaseRight`、アプレット開始、`aptWaitForWakeUp(TR_LIBAPPLET)`、結果回収を行う。
   **呼び出しは同期的で、単なる自前 UI の描画関数ではない。**
4. CTRPF 原作者の公開 `Library/source/pluginInit.cpp` の `KeepThreadMain` は
   `srvInit/acInit/amInit/fsInit/hidInitFake/cfguInit/ncsndInit/plgLdrInit` を呼ぶが、`aptInit` は呼ばない。
   HOME/スリープ等はプラグインローダーのイベントを処理している。
5. ローカル `libctrpf.a` / `libctrpfd.a` のシンボル一覧にも `aptInit` / `aptLaunchLibraryApplet` /
   `swkbdInputText` の定義・未解決参照は見つからなかった。プラグインの自前ソースにも呼び出しはない。
   公開ソースとローカルライブラリが完全に同一ビルドだと証明したわけではない。

libctru の APT は専用イベント・受信スレッド・状態フラグを持つ。
`aptInit` を足すと `APT_Initialize` / `APT_Enable` / 起床待ちまで実行される。
ゲームの既存 APT 管理と競合しない根拠がないため、**`aptInit()` を1行足せば解決とはしない**。
ゲーム側の APT 経路を利用するか、プラグインから既存状態と協調する経路を作る必要がある、というのが現時点の判断。
競合時の具体的挙動（エラー/待ち続ける等）は未観測。

内蔵アプレットの起動は画面・GPUの受け渡しを伴うため、起動と復帰を対にして確認する。

## とび森の BsSkb との区別

既存 `DOCS/catalog_outdoor.md` の画面 ID `0x23E` / `BsSkb` は、内蔵アプレットを呼べる根拠として流用しない。
`code.bin.i64`（idalib、`acnl_code`）で以下を確認した:

- `sub_21C24C` はゲームの入力設定グローバルを設定し、`0x0021C348` から `UiScreen_OpenById` を呼ぶ。
  渡す ID は `0x23E`。逆コンパイルと ARM 命令の双方で確認。
- `sub_57D444` は `Layout/Swkbd/swkbd_qwerty.arc` / `swkbd_kana.arc` /
  `swkbd_grid.arc` / `swkbd_cell.arc` を選び、`0x0057D4A4` から `sub_567244` へ渡す。
  逆コンパイル・リテラル参照・分岐と BL を照合した。
- RTTI は `ti_BsSkb = 0x008C65B0`、`vtbl_BsSkb = 0x008F1D28`。

これはゲームの画面管理とキーボード資源を使う経路の証拠。
**BsSkb の全内部処理で OS アプレットを一切使わない、とまで証明したものではない。**
BsSkb 再利用も別案だが、親画面の寿命・設定データ・結果取得先を確認せずに関数だけ呼ばない。
新しい動的観測はないため、本作の経路・統合判断の confidence は **MEDIUM**。

## 辞書・変換候補取得へ向けた確認順

以下に対応する追加の静的証拠はF-359。候補取得そのものは未達。

1. 公開APIの確定文字列、フィルタコールバック、追加辞書、学習データの受け渡しを確認し、
   内蔵辞書の読み出しや確定前の候補一覧取得と混同しない。
2. 内蔵キーボードのプログラム・辞書資源の所在を調べ、実機と同一版の資料を特定する。
   候補生成関数と結果配列の観測、または辞書資源の読み出しを調べる。自前GUIへの統合は行わない。
3. とび森内の呼び出し入口と、CTRPFから既存APTと協調して呼ぶ経路を調べる。
   起動→取消→復帰を最小確認とし、その後かな入力→変換候補列の取得を検証する。
4. **ビルド前**にソース・ABI・容量・寿命・エラー経路を検証する。
   ケーブを使うなら全 LDR/分岐・コードとリテラルの境界・実行済み領域と `.bss` 重複を監査する。
5. **実機適用前**にも成果物と対象 boot の状態・フック/領域を照合する。
   候補の文字列・順番・入力読み・学習状態を記録し、実画面の候補と独立に照合する。

## 追加調査: 変換候補と辞書（F-359）

### 公開APIで受け渡す内容

`swkbd.h` の公開API・構造体と `swkbd.c` の共有メモリへのコピー方向を照合した。

| 対象 | 方向と用途 | 内蔵変換候補との関係 |
|---|---|---|
| `swkbdInputText` | キーボードから入力文字列を受け取る | 選択して確定した文字列。候補一覧ではない |
| `swkbdSetFilterCallback` | 送信時の入力文字列を検査して許可/拒否する | 候補生成時の列挙コールバックではない |
| `swkbdSetDictionary` | 呼出し元が指定した読み/単語を共有メモリへコピーして渡す | 本体の内蔵辞書を取得するAPIではない |
| `swkbdSetLearningData` | 学習データを入出力する。不透明な構造体 | 内蔵辞書本体や、その時点の全候補配列と同一視しない |

この公開インターフェースでは、読みを渡して内蔵候補一覧を返すAPIは見つからなかった。
それは候補取得不可能という意味ではなく、キーボード内部または辞書資源の調査が必要という判断。
共有メモリの未解明領域に何があるかまでは確定していない。

### 日本語辞書の所在の手掛かり

[3dbrew のタイトル一覧](https://www.3dbrew.org/w/index.php?title=Title_list) は次を掲載している。

| 対象 | 日本語版TitleID | 記載 |
|---|---|---|
| 内蔵キーボード本体 | `0x000400300000C002` | Software Keyboard (`swkbd`) |
| 日本語辞書データ | `0x0004009B00011902` | `JA_small/32` dictionary、共有データアーカイブ |

**所在候補の confidence はLOW**。本体の内容を読んでおらず、キーボードがこの辞書を開く経路も未確認。
辞書が単純な読み→単語テーブルなのか、圧縮・索引・品詞/接続情報を持つのかも未確認。
候補の表示順が固定辞書のみで決まるとは扱わず、学習・直前の入力状態も記録して照合する。

作業フォルダ内の名前/拡張子検索では、この本体と辞書のダンプは見つからなかった。
`NCCH/romfs v1.5/Layout/Swkbd/` はゲーム側の資源で、内蔵キーボード本体のダンプとは扱わない。
次の直接調査には、利用者の実機から取得した両タイトルの内容・版情報が必要。
既存ダンプの保存先を利用者へ問い合わせ中。

### とび森内にあるライブラリアプレット起動経路

`code.bin.i64` のARM命令と、libctru `apt.c` のIPCヘッダー・引数配置を独立に照合。
本作の `0x00977810` は `sub_120610` が APT サービス名を用いてハンドルを取得する先。

| アドレス | 役割/証拠 |
|---|---|
| `0x0048012C` | `APT_PrepareToStartLibraryApplet_Ipc`。TLSコマンド先頭へ `0x00180040`、次の語へR0のappIdを格納し `SVC 0x32` |
| `0x0047FF68` | `APT_StartLibraryApplet_Ipc`。ヘッダー `0x001E0084`。R0=appId、R1=パラメータ、R2=サイズ、R3=共有ハンドル |
| `0x0047FBE0` | 起動準備の上位処理。上記Prepareを呼ぶ。エラーに応じた再試行などがある |
| `0x0047F3F0` | 起動の上位処理。上記Startの前後に状態管理を行う |
| `0x00489554` | 既存の利用例。準備→開始→`sub_12B110`の受信/待機処理。appIdは **`0x406`（エラー表示）**、パラメータサイズ`0xF80` |

`0x0047FF68` のIPC語は `[1]=appId, [2]=size, [3]=0, [4]=handle, [5]=(size<<14)|2, [6]=buffer`。
逆コンパイラではR0/R1を `__int64` と誤った見方にまとめているため、引数は上記ARM命令で確認した。
`0x0048015C` と `0x0047FFB0` はIPC即値であり、表示上の `sub_180040` / `sub_1E0084` への関数ポインタではない。
同じ即値 `0x001E0084` が `sub_468604` にもあるが、こちらは引数・サービスハンドルが異なる。
**即値だけでAPTと判定せず、サービスと全IPC語の配置を照合した。**

これで「本作にはライブラリアプレットの起動経路がある」ことを複数の静的証拠から確認（MEDIUM）。
**内蔵キーボード `0x401` を安全に呼べたという動的検証にはまだ到達していない。**
エラー表示のIDだけを置き換えてはいけない。パラメータ形式、共有メモリ、待機/復帰の文脈が別途必要。
低位IPCの2関数を命名し、根拠と未検証範囲を静的IDBへコメントして保存済み。実機の変更・ビルドなし。

## 前回把握した既存作業の進捗（漢字変換候補取得とは別作業）

- F-349: Simulator の文字/数値キーボードは移植・ホスト比較・3DS ビルド済みという記録。実機未確認。
- F-350〜F-355: 入力遮断と下画面暗幕を一本化。SELECT/START の区別は3gxでも確認済み。
  ボタン/タッチ遮断の残り、暗幕、GUI OFF 時復帰、キーボードは3gxでの確認が残る。
- F-357: フレーム周期調査は別作業。`+0x70` を2へ復元済みという記録。
- 今回 `verify_plugin_port_v2.py` は8群・総異常0件、`verify_keyboard_port.py --preflight` も成功。
  ホスト比較の全再実行・コンパイルは行っていない。事前検査成功を実機成功と扱わない。
- 容量は現行ソースと既存検証器の両方で、文字スロット上69/下76、Picture上74/下336、
  合計410、プラグイン領域 `0x70000`（458,752 B）、配置401,664 Bと確認。
  HANDOFF の下11/56・合計130は古い値だったため訂正。

## 出典と再調査用の保存物

- [devkitPro 文字/数値入力の公式サンプル](https://github.com/devkitPro/3ds-examples/blob/master/input/software-keyboard/source/main.c)
- [libctru swkbd.h](https://github.com/devkitPro/libctru/blob/master/libctru/include/3ds/applets/swkbd.h)
- [libctru swkbd.c](https://github.com/devkitPro/libctru/blob/master/libctru/source/applets/swkbd.c)
- [libctru apt.c](https://github.com/devkitPro/libctru/blob/master/libctru/source/services/apt.c)
- [CTRPF 原作者 pluginInit.cpp](https://gitlab.com/thepixellizeross/ctrpluginframework/-/blob/develop/Library/source/pluginInit.cpp)
- ローカル libctru: `C:/devkitPro/libctru/include/3ds/applets/swkbd.h`、
  `source/applets/swkbd.c`、`source/services/apt.c`。
- `scratchpad/system_keyboard_sources/`: 原作者 `original_pluginInit.cpp`、取得時のミラー4ファイル、
  ミラーコミット情報、ローカルのシンボル確認、出典・SHA-256 の `manifest.json`。
  原作者版とミラー版は異なる。両方で APT 初期化をしない点は一致するが、全文同一とは扱わない。
- 一時メモ: `scratchpad/MEMO_20260908_system_keyboard.md`。
