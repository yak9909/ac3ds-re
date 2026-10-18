# ACNL / CTRPFから内蔵キーボードを呼ぶ経路（F-364）

**F-382（2026-09-09）:** ゲームのキーボード入口をフックする場合の実行文脈と、
確定/取消/子画面終了の契約は[入口フック調査](system_keyboard_game_hook.md)。原本ARM12ケースPASS、実機未操作。

2026-09-08。F-359のAPT入口特定から、起動・画面受渡し・終了待ち・復帰の契約を追った。
**第一候補は、ACNLが初期化済みのAPT/GSP管理を使い、内蔵キーボードID `0x401`を渡す方法。**
関数と引数は具体化できた。安全な実機起動・取消・復帰の成功はまだ確認していない。
自前メニューやgohan.3gxへの組込みを目的とする調査ではない。

**追記 F-372: 利用者の指定により、ACNLの既存APT管理を採用して実機確認の準備を進める。**
今回の作業は静的解析とPC上の原本ARM検証のみ。実機の状態照会も行っていない。
受付位置・失敗経路の追加結果は末尾。F-364の実機読み取りは過去の記録であり、今回の確認ではない。

## どこから呼ぶか

| 経路 | 今回の判断 | 根拠と残る条件 |
|---|---|---|
| ACNLの既存APT管理を利用 | 実機確認へ進める第一候補 | Prepare/Start/WaitとGPU保存・復帰を特定。呼出し文脈と失敗時の回収を詰める必要あり |
| CTRPFからACNLの同経路を要求 | 上記を起動する方法の候補 | プラグインは要求・結果受取を担い、ゲームの管理と協調する。実行スレッド・画面pause・swap寿命を要検証 |
| CTRPFへ`aptInit`を追加して`swkbdInputText` | そのまま使えるとは未確認 | libctru側に別のAPTイベント/受信状態を作る。既存ゲームAPTとの二重管理を解決していない |
| ACNLの`BsSkb`を開く | 今回の内蔵キーボード呼出しとは別 | ゲーム自身の画面/資源を使う経路。F-358参照 |

この区別は「CTRPFからは呼べない」という結論ではない。
ゲームのAPT管理を共有する実装なら、新たに`APT_Initialize`/`APT_Enable`を実行する必要はない。
一方で、任意のCTRPFスレッドから次の3関数を呼ぶだけで安全とも結論していない。

## 呼出しの骨格

対象は日本語版ACNLの現在の`code.bin.i64`。以下はすべて**ACNLの番地**。
SWKBD本体のF-363の番地とは異なる。

| 処理 | アドレス | 引数 |
|---|---|---|
| `GameAPT_PrepareLibraryApplet` | `0x0047FBE0` | R0=`0x401` |
| `GameAPT_StartLibraryApplet` | `0x0047F3F0` | R0=`0x401`, R1=設定へのポインタ, R2=`0x400`, R3=共有メモリのハンドル |
| `GameAPT_WaitForWakeup` | `0x0012B110` | 下記の6引数。結果の設定を受信し、起床処理まで行う |

確認したABIは次のとおり。これは宣言の記録で、実機へ投入する完成コードではない。

（疑似C を省略。原本は _local/legacy-src/…）

`WaitFn`はR0..R3に最初の4引数、入口SP+0に`receivedHandle`、
**SP+8/+12に64ビットの`timeoutNs`**を置く。SP+4は8バイト整列の穴。
逆コンパイラの旧表示にあった独立した第6引数を、そのまま宣言へ写してはいけない。
既存caller `0x00489554`のSTRDと、原本ARMの局所実行で照合した。

成功経路で必要となる順序:

1. 設定構造体とページ境界に整列した共有メモリを確保し、初期値を配置する。
   `svcCreateMemoryBlock`で両側READ|WRITEの共有ハンドルを作る。
2. ゲームが他のアプレット遷移を行っていない呼出し文脈でPrepare(`0x401`)を行う。
3. Start(`0x401`, 設定, `0x400`, 共有ハンドル)を行う。
4. Waitへ同じ設定バッファと容量`0x400`を渡し、送信元・実受信サイズを取得する。
   既存callerのタイムアウトは`qword[0x0096EAE0]`で、このbootでは`-1`。
5. 通常終了を確認し、送信元・サイズ・`SwkbdResult`と共有メモリ内の範囲を検査する。
   確定時だけUTF-16LE文字列を取り出す。取消やHOME/POWER等の通知は別に扱う。
6. アプレットが参照しなくなった後で共有ハンドルを閉じ、バッファを解放する。
   画面/ゲーム側の復帰完了も確認する。

**この順序だけで実機安全性が証明されたわけではない。**
特に手順2以降の失敗、通常終了以外の起床、実行スレッドの選定は下記の確認を要する。

## GPUとAPTの受渡しはどこにあるか

`0x0047F3F0`のアプリケーション側分岐は、主に以下を行う。

| 段階 | 経路 | 裏付け |
|---|---|---|
| VRAM保存 | `0x0047E490`→`0x0047E52C` | GSP IPC `0x00190000` = SaveVramSysArea |
| 画面受渡し | `0x0047EB80` | キャプチャ情報を作り、対象アプレットへparameter command 2を送信、応答ハンドルとバッファを処理 |
| GSP権限解放 | `0x0012B010(0)`→`0x0012AB78` | ReleaseRight側の処理と状態フラグ更新 |
| アプレット開始 | `0x0047FF68` | APT IPC `0x001E0084` |
| 待機通知 | Wait→`0x0012B6C4`→`0x0012BC40` | APT IPC `0x00430040` = NotifyToWait |
| 受信 | Wait→`0x00125228` | APTイベント/parameterの取得、必要なら既存callbackを実行 |
| GSP権限再取得 | Wait→`0x0012B010(1)`→`0x0012AB10` | AcquireRightと状態フラグ更新 |
| VRAM復元 | Wait→`0x00125174`→`0x0012ABCC`→`0x00131588` | GSP IPC `0x001A0000` = RestoreVramSysArea |

Waitは起床理由・遷移前状態によって復帰処理を分岐する。
従って「Start後に低位ReceiveParameterだけ呼べば十分」とはしない。
逆に上位関数を利用する場合、同じGPU処理を外側から無条件に二重実行しない。
上表以外にもStart/Waitから呼ぶサービス処理があり、全副作用の実機確認は未実施。

libctruの`aptLaunchLibraryApplet`もPrepare→VRAM保存/画面受渡し→GSP解放→Start→
起床待ち/復元という順序を持つ。関数名からの推測ではなく、ACNLのIPC語と公式実装を突き合わせた。

## APTのハンドルが0でも、未初期化とは限らない

ゲームのAPTセッションは常時開いたままではない。

```text
0x0012B088: [0x0097780C] のmutexを待つ → 0x00120610でサービスを開く
低位IPC:   [0x00977810] のハンドルでSVC 0x32
0x0012B6E8: サービスを閉じる → [0x00977810]=0 → mutexを解放
```

今回の読み取りではmutexは非0、セッションハンドルは0だった。
静的なclose/ゼロ化の処理と整合する。
`0x0048012C`/`0x0047FF68`だけを直呼びすると、ロックとセッション生成が欠ける。
libctruの`aptSendCommand`にもロック→サービス取得→通信→close→unlockの対応する処理がある。

## 内蔵キーボードへ渡す内容

公式libctru `swkbd.h`/`swkbd.c`に基づく最小の日本語文字入力用設定をデータとして作成した。

| 項目 | 値/場所 |
|---|---|
| アプレットID | `0x401` |
| パラメータ構造体 | `0x400`バイト |
| タイプ / ボタン数 | NORMAL=0 / 2ボタン（`num_buttons_m1=1`） |
| 最大入力長 | 55 UTF-16コード単位（`+0x20`） |
| 予測/漢字変換 | `predictive_input=1`（`+0x112`） |
| 初期値 | 共有メモリoffset 0にUTF-16LE「かんじ」＋終端 |
| 共有メモリ | `0x1000`バイト、`0x1000`境界。実機上の確保はまだ行っていない |
| version | 5（`+0x134`） |
| result初期値 | -1（`+0x138`） |
| 未使用の辞書/状態/学習offset | -1。callbackと学習保存は無効 |
| 確定結果 | `text_offset`=`+0x144`, `text_length`=`+0x148` |

共有メモリの容量は`2*(max_text_len+1)`を4バイト、次にページ単位へ切り上げる。
今回は追加辞書や学習領域を持たせていない。全領域・予約領域を初期化した。
`prepare_launch_fixture.py`はヘッダの配列長・宣言順と32ビットABIの配置を検査する。

終了時は`text_offset>=0`、長さが最大入力長以下、終端を含む範囲が共有メモリ内、
UTF-16の妥当性を検査してから読む。戻り値が異常な場合に負のoffsetへアクセスしない。
公開APIから得られるのは確定文字列であり、変換候補一覧ではない。

## 3種類の戻り値を混同しない

| 種類 | 例 | 用途 |
|---|---|---|
| Prepare/StartのResult | 符号付き32ビット | IPC/サービス処理の成否。ただし上位Startはエラー処理を内包する |
| `GameAPT_WaitForWakeup`の戻り値 | 生のAPT command `0xA`→2、`0xB`→3、`0xC`→4 | ゲームSDKが変換した起床理由 |
| 設定内`SwkbdResult` | 2ボタンの左=1、右=2 | キーボードの取消/確定など |

生の`0xA`はWAKEUP_EXIT、`0xB`はWAKEUP_PAUSE、`0xC`はWAKEUP_CANCEL。
例えばWaitの2と、設定内resultの2は別の列挙値である。

## 実機確認前に残る点

1. **Start失敗時の回収。** `0x0047F3F0`は失敗時に`0x00129E70`→`0x00129EA0`→`err:f`へ進む。
   単にResultを返して呼出し元が巻き戻せる関数とは扱わない。
   GPU権限解放後・開始前後の失敗、Prepare後の中止、通常終了以外の通知への方針が必要。
2. **ゲーム側の呼出し文脈。** 既存利用例`0x00489554`はエラーアプレット`0x406`用。
   ゲームの上位callerはロック、サウンド/他処理の待機、終了後の更新も行う。
   ゲーム自身が使っている文脈を参考に、通常フレームのどこから実行するかを確認する。
   エラー用構造体のIDだけ変更する方法ではない。
3. **CTRPFのpauseとswap。** 参考ソースのPauseはフレーム停止待ちと画面取得を行う。
   APTが必要とするゲーム側処理まで停止したまま同期的に待つとどうなるかは未観測。
   原作者のKeepThreadはSWAP時にhook領域のunmap/restore・サウンド解放を処理する。
   本機の内蔵キーボード起動でSWAPが起きるかは未確認。
   起きる場合には実行コード・戻り先・スタック・共有メモリがその間も有効であることを確かめる。
4. **実際の取消・復帰。** 最初は1回だけ起動→取消→ゲーム復帰を観測し、その後に確定入力を試す。
   その前に対象boot、使用領域、ABI、失敗経路を検証する。今回の読み取り/局所実行を起動成功と数えない。

## 今回の検証結果

- idalib `acnl_code` / `code.bin.i64`、ARM32、imagebase表示0、`.text`は`0x00100000`始まり。
- 実機は**既にSuspend済み**。PC=`0x0046DAF8`、SP=`0x31F468C0`、LR=`0x0046B06C`、PSR=`0x60000010`、bp=0。
- 起動関連6関数の先頭16バイトはIDBと一致。
  `[0x0096EB04]=0x300`、`[0x0096EB08]&7=0`、timeout定数は-1/0。
- debuggerのmemory mapping APIは空リストを返した。全領域が未マップという意味にはしない。
  今回新規配置領域の安全性を確認したわけではない。
- **原本ARMのIPC組立て18ケースで期待値と一致**。成功・サービスエラー・SVCエラーを比較。
  既存エラーcallerの3呼出しと64ビット引数配置も一致。
  OS/GPU等の外部処理はモックなので、アプレットの動作検証ではない。
- 設定`0x400`、共有データ`0x1000`のデータ生成/境界/予約領域検証に成功。
- 関数8件を命名、4件の型を修正、4件へコメントを追加し、静的IDB保存済み。
- **ビルド・実機へのコード/データ書込み・実機関数呼出し・再開は行っていない。**

経路・契約全体のconfidenceはMEDIUM。コード一致や現在の値を実機で読めたことを、起動成功のHIGHへ拡張しない。

## 再現物と出典

- `SYSTEM_KEYBOARD/evidence/launch_static.json` / `launch_lifecycle.json`: idalib静的根拠。
- `launch_abi_bytes.json`: IDBの原本バイト、`verification_launch_abi.json`: 局所照合結果。
- `launch_runtime_readonly.json`: 今回の実機読み取り。`read_launch_state.py`はIDA GUI用の読み取り専用スクリプト。
- `launch_fixture/{swkbd_state.bin,shared_initial.bin,manifest.json}`: 未適用の設定/共有データとハッシュ。
- `launch_sources.json`: 今回使ったローカルSDK/CTRPFソースのSHA-256。

```powershell
& 'C:/Users/<伏せ字>/anaconda3/python.exe' SYSTEM_KEYBOARD/verify_launch_abi.py
& 'C:/Users/<伏せ字>/anaconda3/python.exe' SYSTEM_KEYBOARD/prepare_launch_fixture.py
```

- [libctru swkbd.c](https://github.com/devkitPro/libctru/blob/master/source/applets/swkbd.c)
  / [swkbd.h](https://github.com/devkitPro/libctru/blob/master/include/3ds/applets/swkbd.h)
  / [apt.c](https://github.com/devkitPro/libctru/blob/master/source/services/apt.c)
  / [gspgpu.c](https://github.com/devkitPro/libctru/blob/master/source/services/gspgpu.c)。
  今回は`C:/devkitPro/libctru/`の実ファイルを使用。Web再取得は失敗したので、最新版との同一性は主張しない。
- [CTRPF原作者 pluginInit.cpp](https://gitlab.com/thepixellizeross/ctrpluginframework/-/blob/develop/Library/source/pluginInit.cpp)。
  前回保存済み`scratchpad/system_keyboard_sources/original_pluginInit.cpp`を使用。
- pause実装は`REFERENCES/CTRPF PROJECTS/AnimalBytesv0.7.4/libctrpf/source/CTRPluginFrameworkImpl/System/ProcessImpl.cpp`。
  参考実装であり、現在のローカルlibctrpfと同一ビルドとは未証明。

## F-372: ACNL既存APT管理による実機確認準備

### 採用する経路と受付位置

最初の試験は、ACNLの実行文脈で既存Prepare/Start/Waitを使う独立した一回要求とする。
要求元は設定・共有メモリ・結果記録を用意し、ゲーム側へ要求を渡す。
CTRPFの追加APT初期化や独自のイベント受信スレッドは作らない。
現段階でゲームへ投入できるランチャーを完成させたという意味ではない。

既存の呼出し順を静的IDBで確認した:

```text
0x0024EF10  GPUコマンドリストを扱う仮想関数（参照 0x008E8BCC）
  0x0024EF84 → 0x005CE28C
    0x005CE29C → 0x005CD970
      [0x009483D8] = ErrEulaMgr
      +28/+32 のmember-function pointerを実行
        既存の0x005CD9C0
          0x0034AE04(0x00ADF848)で再帰try-lock
          成功時だけ0x0058C79C(0) → エラーアプレット0x00489554
          結果に応じた処理 → 0x0058C7B0 → 0x00138D30(0x00ADF848)
```

`0x005CE29C`付近が**要求受付位置の第一候補**となる。
既存のアプレット呼出しがここを通るためで、通常フレームの任意位置から選んだものではない。
ただし、実際の実行スレッドID・同時実行・停止条件は未観測であり、安全なフック位置の確定ではない。
描画コマンド生成/終了処理の文脈を含むので、既存処理を停止したCTRPFスレッドから同期実行しない。

ErrEulaMgrの`+20/+24`にも別のmember-function pointerがあり、
`0x005CDF3C`が`0x001B6B84`内から実行する。2組を同じ受付口だと扱わない。
既存の`+28/+32`を書き換えたり、エラーアプレットのIDだけを変えたりする案ではない。
後の実装では既存dispatcherを保ち、独立要求の受付を追加する位置として検討する。

### ロックと周辺処理

- `0x0034AE04`: TLS値と所有者を比較し、同一なら再帰カウントを増やす。
  別所有者なら`0x0034A5FC`のLDREX/STREXによる取得を試みる。
  ロック値が取得可能でなければ待機せず0を返す。
- `0x00138D30`→`0x0013650C`: 再帰カウントを減らし、0で所有者を消して下位解放へ進む。
- `0x005CD9C0`はtry-lock失敗時にそのまま戻る。
  原本ARM局所実行でも、失敗側は起動や解放を呼ばず、成功側は周辺処理を挟むと確認した。
- `0x0058C79C(0)`→`0x006B28A4`は`[0x00947080]`の管理オブジェクトの
  `+0xC60`にあるbit `0x4`を使う処理。復帰側`0x0058C7B0`はbit `0x8`を先に調べ、
  その次にbit `0x4`を調べて`0x006B1954`へ渡す。
  従って、既に別理由の状態がある場合に、この2関数を無条件に呼ぶと対称になるとは限らない。
  管理状態の所有権・既存状態の保持を確認してから利用する。全サウンドの停止/復帰と断定しない。

### 失敗経路の追加検証

| 場面 | 原本で確認した動作 | 実装への制約 |
|---|---|---|
| Prepare開始 | `0x0012ACEC(4)`が遷移byte `0x0096EAFA`を書き換える | Prepareも副作用のある段階として記録する |
| Prepareの最終エラー | 同関数内で遷移値を戻さずResultを返す | 解放して即再試行する一般的なラッパーにはしない |
| Prepare/Startの特定3エラー | 10ms待って再試行、回数上限なし | 外側のタイムアウトだけでは同期呼出しを止められない |
| Start内のVRAM保存・capture関数から負値が返る | Start側に結果判定がなく、Start IPCまで進む | Startの最終Resultだけで全前処理の成功を判断しない |
| Start IPCの最終エラー | セッションを閉じた後`0x00129E70`へ進む | `err:f`が安全に戻ると仮定しない。fatal処理の無効化を回復策にしない |
| 通常終了raw command `0xA` | Waitは2を返しVRAM復元経路を通る | 設定のSwkbdResultと別に検査する |
| raw command `0xC` | Waitは4を返し、そのVRAM復元経路を通らない | 通常終了と同じ後処理を外側から無条件に足さない |

VRAM保存/captureの試験は、**そのcalleeが負値を返した場合のStart側の分岐**を検査したもの。
callee自身のエラー通知・待機などを通過した実機試験ではない。
共有メモリを解放できる時点や、失敗後にGPUを再取得するだけで復帰できることも証明していない。

キーボード画面の「やめる」（2ボタン設定のSwkbdResult=1）とAPTのWAKEUP_CANCELは別。
最初の取消試験でも、送信元・実受信サイズ・Waitの理由・SwkbdResultを別々に記録する。

### 次に作る実機試験の契約

1. **配置・実行文脈の検証。** 実機作業が指示された後で、対象bootのコード一致、使用領域、
   ゲーム側の実行スレッドとAPT状態を確認する。F-364の過去snapshotを現在値として使わない。
   実行コード・スタック・戻り先・共有メモリは、アプレット遷移中も存在する配置にする。
2. **受付。** ゲームの元dispatcherを呼び、独立した一回要求だけを受け付ける。
   既存ErrEula処理・APT遷移・上記管理状態と競合する場合は保留する。
   try-lock取得失敗時も保留する。状態フラグの一度の読取りだけを排他の代わりにしない。
3. **起動。** F-364で作った設定/共有メモリと6引数ABIを使用する。
   Prepare/Startの途中で復帰不能となる条件を解決するまで実機投入へ進めない。
   Prepare後の失敗を「未起動」として自動再試行しない。
4. **結果。** 最初は起動→画面の「やめる」→ゲーム復帰を1回観測する。
   復帰後、理由・送信元`0x401`・サイズ`0x400`・共有メモリ範囲を検査して回収する。
   解放時点が不明な異常通知では結果文字列を読まず、次の要求も発行しない。
5. **続く試験。** 取消の復帰を確認してから「かんじ」→「漢字」の確定、再起動を伴わない2回目を試す。
   これは起動と確定結果回収の試験。候補一覧の取得はF-363の目的に沿って別途扱う。

まだ残るのは、実行スレッド/常駐配置、周辺管理状態の保持、Start/Prepare失敗時の回収、
APT通知ごとのアプレット終了・共有メモリ寿命である。単純な3関数ラッパーを実機用に完成扱いしない。

### 再現と保存物

`SYSTEM_KEYBOARD/verify_acnl_lifecycle.py`を通常のPC Pythonで実行する。
デバッガやネットワークは使わず、idalibから保存した原本ARMの分岐をUnicornで実行する。
ソースのAST確認後に実行し、**33ケースPASS**。
Prepareの12ケース、Startの8ケース、Waitの9通知、既存callerの4ケースを含む。
OS・GPU・ロック・周辺管理のcalleeは明示的なモックで、未知の呼出し先やSVCは検証エラーとなる。
fatal入口では実行を止める。fatalが戻ったと偽装して成功扱いにはしない。

- `evidence/acnl_prepare_static.json`: IDB由来の擬似コード・assembly・原本バイト。
- `evidence/acnl_prepare_context.json`: callerの参照・ロック・周辺状態に関する追加根拠。
- `evidence/verification_acnl_lifecycle.json`: 全ケースの実行順、返却値、入力SHA-256。
- `scratchpad/MEMO_20260908_swkbd_acnl_prepare.md`: 今回の引き継ぎ。

confidence MEDIUM。今回、実機アクセス・ビルド・プラグイン組込みは行っていない。
