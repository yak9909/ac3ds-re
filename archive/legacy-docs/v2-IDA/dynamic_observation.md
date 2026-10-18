# IDA動的解析の画面観測

画面表示が結論に関わる動的解析では、IDAの値だけでなくChokistream画像を必ず保存する。旧 `reference/old_project/PATCHES/grab_screen.ps1` は使わない。デスクトップ画素を切り取るため、Chokistreamより手前のウィンドウを3DS画面として保存し得る。

## 必須の流れ

1. ida-pro-mcpで対象プロセス、停止状態、PC/SP/LR/CPSR、BP、bootを確認する。既にSuspendなら利用者へ再度Suspendを依頼しない。
2. 変更前の画面と、必要なカウンタ・メモリ値を保存する。
3. Resume前に `tools/dynamic/run_timed.py` で停止タイマーを登録する。IDA要求内でsleepしない。
4. 自動停止後、別のida-pro-mcp呼出しで `get_process_state()` がSuspendを示すことを確認する。確認前にメモリを読み書きしない。
5. Chokistreamの直接画像または非前面ウィンドウ取得を保存し、PNGを画像として確認する。hash、取得時刻、対象画面、前面状態を根拠へ残す。
6. 成功例と失敗例、画面とレジスタ/メモリの2経路を照合する。一枚の画像だけで停止・クラッシュ・明滅を断定しない。

## 一定時間だけResumeする

IDA GUIで次を実行する。既定は3000ms、上限は25000ms。

```python
py_exec_file("A:/Disassemble/acnl/project_v2/tools/dynamic/run_timed.py")
```

短くする場合:

```python
import runpy
runpy.run_path(
    "A:/Disassemble/acnl/project_v2/tools/dynamic/run_timed.py",
    init_globals={"RUN_MS_OVERRIDE": 500},
)
```

このスクリプトは `register_timer` を `continue_process` より先に呼ぶ。Resumeに失敗した場合はタイマーを解除する。BPが先に発火した場合、タイマーは停止済み状態を確認して終了する。25000msを超える必要があるときは理由と停止手段をSESSIONへ先に保存し、`MAX_RUN_MS_OVERRIDE`を明示する。

ida-pro-mcpは対象実行中に要求を処理できない場合がある。タイマー登録後に別要求で無理に停止させず、予約した時間の後で状態を読む。LumaのソフトBPは再開前に除去する。

## 用語: フリーズとSIGSEGVを使い分ける（利用者の定義、2026-09-25）

| 言葉 | 何が起きたか | IDA | 調べ方 |
|---|---|---|---|
| **SIGSEGV** | CPUの例外（不正な番地の読み書きなど）でゲームが止まった | `Warning`「got SIGSEGV signal」のダイアログが出る。PCは例外を起こした命令 | 下の「タイムアウトしたら」でダイアログを読んで閉じ、PC・レジスタから落ちた命令を調べる |
| **フリーズ** | 例外は無く、画面の更新が止まった（デッドロック・無限ループ・何かを待ち続けている） | ダイアログは出ない | 利用者がSuspendした状態で**全スレッドのPC/LR/SP**を並べ、待っている同期（`svcArbitrateAddress 0x22`・`svcWaitSynchronization`）の対象と、その持ち主のスレッドを探す |

利用者はこの2つを明確に区別して報告する。報告の言葉どおりに扱い、記録でも混ぜない。

## ida-pro-mcpがタイムアウトしたら（最初にIDAのダイアログを確認する）

**タイムアウトしたら、再送や推測より先にIDAのダイアログを確認する**（2026-09-25 利用者指示）。
ゲームがSIGSEGV等で止まると、IDAは例外通知のモーダルダイアログ（題名 `Warning`、例: `5E20A8: got SIGSEGV signal (Segmentation fault) (exc.code b, tid 703)`）を出し、それがメインスレッドを塞ぐ間はMCPの要求を一切処理しない。**タイムアウトの多くはこれ**（run_timedの自動停止も効かない）。

1. 一覧（読み取りのみ。何も押さない）。題名・文面・ボタン・PNG・JSONを `work/evidence/ida_dialogs/<日時>/` に残す。
   ```powershell
   powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools/dynamic/ida_dialog.ps1
   ```
2. 文面を記録する（例外なら番地・種類・tid）。**SESSIONへ先に書く。**
3. 閉じる。ボタン名は一覧の `buttons` から（部分一致）。読めないときは `-Enter`（既定ボタン）。複数枚あれば `-Index`。
   ```powershell
   powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools/dynamic/ida_dialog.ps1 -Press OK -NoCapture
   ```
4. **もう一度一覧を取り、`dialogs` が空になったことを確かめる。**
5. ida-pro-mcpで `get_process_state()` と PC/LR/SP・全レジスタを読み、落ちた命令を静的IDBで逆アセンブルして原因を調べる。例外で止まった対象を**そのままResumeしない**（同じ命令で再び落ちる）。
6. ダイアログが無いのにタイムアウトする場合に初めて「対象がまだ走っている」「本当に固まった」を疑う（CLAUDE.mdの4分類）。

仕組み: IDA（`ida`/`ida64`/`idat`/`idat64`）の見えている最上位窓のうち主窓（題名 `IDA -`）以外を列挙し、UI Automationで文面とボタン名を読み（QtのダイアログもQt682QTQWindowIconとして読める）、PrintWindowで前面化せずに撮る。押すのはUI AutomationのInvoke（`-Press`）か `WM_KEYDOWN/UP VK_RETURN`（`-Enter`）。旧 `inspect_ida_dialog.ps1` はプロセス番号の決め打ちと他の証拠画像の固定パス上書きがあるので使わない。

## Chokistreamの取得元

### A. Image Sequence（第一候補）

連続観測や証拠採取では、Chokistreamの `Output Format = Image Sequence` を使う。これは受信した `BufferedImage` をPNGへ直接書くため、前面、重なり、DPI、デスクトップ内容に依存しない。

`Output Settings` の保存先を `work/evidence/screens/<session>/`、prefixを試験名にする。正確な上下画面が必要なら `Layout = Separate` を使う。現行公式実装のファイル名は次のとおり。

- 上: `<prefix><連番>_top.png`
- 下: `<prefix><連番>_bototm.png`
- Separate以外: `<prefix><連番>.png`

`bototm` は現行公式実装の綴りなので、`bottom`だけを検索しない。Separate以外の合成画像は一方の最新画像を保持して再合成するため、上下が同じ時刻のフレームとは限らない。

headlessでは、jarと同じ作業ディレクトリの `chokistream.ini` に既存の接続設定と次を置き、`java -jar chokistream.jar --console` で起動できる。

```ini
outputFormat = Image Sequence
layout = Separate
sequenceDir = A:/Disassemble/acnl/project_v2/work/evidence/screens/<session>
sequencePrefix = <test-name>_
```

最新画像は次で鮮度・寸法・SHA-256を検査してから固定名へコピーする。

```powershell
python tools/dynamic/latest_chokistream_frame.py `
  --dir work/evidence/screens/<session> `
  --screen bottom `
  --max-age-sec 10 `
  --copy-to work/evidence/screens/<session>/observed_bottom.png `
  --json-out work/evidence/screens/<session>/observed_bottom.json
```

Image Sequenceはフレームごとにファイルが増える。必要区間だけ動かし、保存対象はSESSIONから参照する。

### B. Visualウィンドウの非前面取得

Visual出力を維持したい場合:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File tools/dynamic/capture_chokistream.ps1 `
  -Screen both `
  -Out work/evidence/screens/<session>/observed.png
```

`capture_chokistream.ps1` は対象HWNDへ `PrintWindow(PW_CLIENTONLY | PW_RENDERFULLCONTENT)` を送り、Chokistream自身にクライアント領域を描かせる。前面化せず、デスクトップ取得へ自動fallbackしない。隣にJSONを保存し、`target_title`、`foreground_title`、`target_was_foreground`、crop、SHA-256を記録する。

ウィンドウは最小化されていてはいけないが、他のウィンドウの後ろでよい。`uniform_sample=true`、PrintWindow失敗、寸法からcropを安全に決められない場合は画像を証拠にせず、Image Sequenceへ切り替える。上下scaleが異なる複合レイアウトでは `-Screen both` を使うかSeparate表示を使う。 `Vertical (Inv)` / `Horizontal (Inv)` を使っている場合は `-Layout vertical-inv` / `horizontal-inv` を明示する。Separateで上下両方が必要なら2回に分けて取得する。

2026-09-19にChokistreamのSwingコントロール画面で、別ウィンドウが前面の状態から正しいPNGを取得した。映像用JFrameはその時点で未接続だったため、次回接続時の最初の1枚は同時刻のImage Sequenceと目視で照合してからPrintWindow経路を採用する。公式映像部は `BufferedImage` をSwing `JComponent.paintComponent`で描く実装なので、同じ経路で取得できる見込みは高いが、未照合の実機映像をHIGH扱いしない。

Chokistream組込みの `S` スクリーンショットも内部画像をPNG化するが、キーfocusと保存先の作業ディレクトリに依存するため自動解析の第一候補にはしない。

## 鮮度と判定

- timed runの前後で別名のPNGとJSONを保存する。上書きした1枚だけを根拠にしない。
- Suspend直後は転送中だった古いフレームが残り得る。mtime/hashと試験操作に対応した画面変化を確認する。
- 同じhashが続いても、ゲーム停止、低FPS、同じ静止画を区別できない。ゲーム側カウンタやフック記録と照合する。
- 画面が黒いだけでクラッシュと判断しない。PC、例外状態、フレーム入口、ログを確認する。
- PNGを保存しただけで終えず、画像表示ツールで実際の内容を確認する。

## オフライン検証

IDA Resumeや実機操作の前に次を実行する。

```powershell
python tools/dynamic/verify.py
```

検査対象は、タイマー登録順、Suspend callback、Resume失敗時の解除、状態/時間guard、PowerShellのcrop計算、デスクトップ取得APIの不在、Image Sequenceの上下suffixとPNG判定。2026-09-19時点で全項目PASS。

調査したChokistream公式ソースは `Eiim/Chokistream` mainのcommit `c350ee8f772baad6b3ad225af4da938d62c884fd`。仕様の根拠はREADME、Options wiki、`Main.java`、`ConfigFileCLI.java`、`ImageSequenceVideo.java`、`SwingVideo.java`、`ImageComponent.java`。
