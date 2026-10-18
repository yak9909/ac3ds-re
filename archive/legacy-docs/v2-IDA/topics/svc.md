# SVC（システムコール）一覧と使い道 / IDA-opus-5.5-F034

対象: 更新版 v1.5 の `artifacts/update/exefs/code.bin`（VA = ファイル + 0x100000、.text は `[0x100000, 0x838018)`）。
再現: `python tools/svc/scan_svc.py` → `work/evidence/svc/svc_sites.json`。

## 1. 調べ方と確度

- `.text` の 4 バイト境界の語で `0xEF0000nn`（ARM の SVC、条件 AL）かつ `nn <= 0x7F` のものを拾い、
  **直後の命令が SVC の包み・呼び出しとしてありえる形**（`bx lr` / `ldr` / `pop` など）のものだけ残した（753 → 745）。
  生の全走査（条件・番号を問わない）では 24,459 件になり、ほとんどはリテラルなどのデータ（使えない）。
- 名前は **devkitPro の `libctru/source/svc.s`**（`SVC_BEGIN` と `svc` 即値）から機械的に付けた。
  番号・引数・制限は 3dbrew の [SVC](https://www.3dbrew.org/wiki/SVC) と一致（外部資料なので LOW 扱いだが、2 資料が一致）。
- 呼び出し地点の関数は静的 IDB で `lookup_funcs` 済み。`0x11C7C4` と `0x14FB74` は IDB で関数になっていない（`svc; bx lr` の形なので本物と判断、MEDIUM）。
- 確度: 地点と番号は HIGH（命令語と前後の逆アセンブル）。個々の地点の「何のために呼ぶか」は未解析（下の表の用途は SVC の一般的な意味）。

## 2. ゲームが使っている SVC（32 種類・745 か所）

| 番号 | 名前（libctru） | 件数 | 主な地点 | 備考 |
|---|---|---|---|---|
| 0x01 | ControlMemory | 1 | 0x11DC48 | ヒープ・LINEAR の確保（SDK の起動処理） |
| 0x02 | QueryMemory | 1 | 0x11F430 | |
| 0x03 | ExitProcess | 3 | 0x11C7C4, 0x12B664, 0x12B880 | |
| 0x08 | CreateThread | 1 | 0x122BCC | nn::os::Thread |
| 0x09 | ExitThread | 1 | 0x12F3BC | |
| 0x0A | SleepThread | 1 | 0x128428 | |
| 0x0B | GetThreadPriority | 1 | 0x13DDA0 | |
| 0x0C | SetThreadPriority | 9 | 0x37D220 ほか | ゲーム側コード（0x37D… / 0x53A… / 0x55C…）から直接 |
| 0x13 | CreateMutex | 1 | 0x14FB80 | |
| 0x14 | ReleaseMutex | 3 | 0x12B72C（GameAPT_CloseSessionAndUnlock）ほか | |
| 0x17 | CreateEvent | 1 | 0x1283FC | |
| 0x18 | SignalEvent | 9 | 0x124E2C ほか | |
| 0x19 | ClearEvent | 16 | 0x124E50 ほか | |
| 0x1E | CreateMemoryBlock | 1 | 0x135C80 | 共有メモリ |
| 0x1F | MapMemoryBlock | 2 | 0x13B0A0, 0x34B1A8 | |
| 0x20 | UnmapMemoryBlock | 2 | 0x140658, 0x34AFA8 | |
| 0x21 | CreateAddressArbiter | 1 | 0x11F418 | |
| 0x22 | ArbitrateAddress | 1 | 0x135C54 | 軽量ロック・条件変数の土台 |
| 0x23 | CloseHandle | 164 | 各所 | インライン展開が多い |
| 0x24 | WaitSynchronization(1) | 43 | 0x137064 ほか | ★**`0x137064` は本解析で待機中スレッドの PC として何度も見た地点**（そこで止まっていると bp を付けた直後の continue が失敗した） |
| 0x25 | WaitSynchronizationN | 1 | 0x12843C | |
| 0x27 | DuplicateHandle | 1 | 0x14FB98 | |
| 0x28 | GetSystemTick | 81 | 各所 | 時間計測（268 MHz のティック） |
| 0x29 | GetHandleInfo | 1 | 0x14FBB0 | |
| 0x2B | GetProcessInfo | 1 | 0x122BE8 | |
| 0x2D | ConnectToPort | 1 | 0x1283E4 | `srv:` への接続 |
| 0x32 | SendSyncRequest | 392 | 各所 | **サービス呼び出し（IPC）すべて**。GSP（GPU）・FS・HID・APT など |
| 0x35 | GetProcessId | 1 | 0x12F3C8 | |
| 0x37 | GetThreadId | 1 | 0x13A344 | |
| 0x38 | GetResourceLimit | 1 | 0x11DC64 | |
| 0x3A | GetResourceLimitCurrentValues | 1 | 0x11D398 | |
| 0x3C | Break | 1 | 0x135C70 | 異常時の停止（`mov r0,#4` の直後） |

使っていない主なもの: 0x3D OutputDebugString、0x52〜0x54（プロセスのデータキャッシュ操作）、0x1A〜0x1D（タイマー）、0x15/0x16（セマフォ）。

## 3. Luma3DS の独自 SVC（プラグインから使える）

Luma3DS は標準の 0x7D までに加えて次を持つ（出典: Luma3DS の `sysmodules/rosalina/source/csvc.s` と `include/csvc.h`、[Standard features](https://github.com/LumaTeam/Luma3DS/wiki/Standard-features)）。
CTRPF / 3GX プラグインはゲームのプロセスの中で動くので、ゲームと同じく標準の SVC を呼べ、Luma の独自 SVC も呼べる（CTRPF 自身がこれらを使う）。

| 番号 | 名前 | 内容 |
|---|---|---|
| 0x80 | CustomBackdoor | 関数を特権モードで実行 |
| 0x90 | ConvertVAToPA | 仮想アドレス → 物理アドレス |
| 0x91 / 0x92 | FlushDataCacheRange / FlushEntireDataCache | データキャッシュ（L2 含む）の書き出し |
| 0x93 / 0x94 | InvalidateInstructionCacheRange / InvalidateEntireInstructionCache | 命令キャッシュの無効化 |
| 0xA0 / 0xA1 | MapProcessMemoryEx / UnmapProcessMemoryEx | 別プロセスのメモリを自分に写す |
| 0xA2 | ControlMemoryEx | 領域属性つきの ControlMemory |
| 0xA3 | ControlMemoryUnsafe | 検査を省いた確保（ALLOC / ALLOC_LINEAR / FREE） |
| 0xB0 | ControlService | サービスのクライアントセッションを奪う・名前を得る |
| 0xB1 / 0xB2 | CopyHandle / TranslateHandle | ハンドルの複製・カーネルオブジェクトの特定 |
| 0xB3 | ControlProcess | 全ハンドル列挙、MMU を RWX に、メモリ配置変更の通知、スレッドの一時停止（SCHEDULE_THREADS）など |

注意: プラグインは自分のヒープでの `svcCreateMemoryBlock` に制限がある（[Luma3DS issue #2078](https://github.com/LumaTeam/Luma3DS/issues/2078)）。独自 SVC の番号と引数は Luma の版で変わりうるので、使う前にプラグインのビルドに入っている CTRPF / csvc の定義と照合する。

## 4. これまでの課題に SVC で効きそうなこと（提案・未検証）

★いずれも**実機未確認の案**。採用するときは最小の 1 操作から検証する。

1. **ポインタの安全確認（0x02 QueryMemory）**: いま `IsHeap()` は番地の範囲だけで判定している。QueryMemory ならその番地が
   マップ済みか・読み書きできるかを OS に聞ける。場面の切り替えで解放された物を読んで落ちる類（F030 の SIGSEGV など）の予防になる。
   ただし毎フレーム多数回呼ぶと重いので、作成時・場面の変化時の検査に使う。
2. **★実機で確認（F035）: GPU から見えるメモリの確保**。ControlMemory / ControlMemoryEx の LINEAR は資源上限で全領域とも 0xD86007F3。
   **Luma の ControlMemoryUnsafe(0xA3) で `ALLOC_LINEAR | REGION_SYSTEM` を空き番地（例 0x10003000）へ貼ると成功**（PA 0x28C32000、
   読み書き OK、解放で使用量が戻る）。addr0 は必ず空き番地を渡す（0 だと番地 0 に貼る）。自前 GUI の g_GfxAllocator の 0x4000 上限や
   nw::lyt ヒープの借用（F-295 / F-303 / v3 仕様）を置き換えられる見込み。GPU が実際に読むことは未確認。
3. **キャッシュ操作（0x54 FlushProcessDataCache / Luma 0x91・0x93）**: ケーブやフック語を書いた後の同期。CTRPF の `FlushMemory` が
   内部でこれらを使っているはずで、いまの作法で足りている（I-cache は実測で問題になっていない）。新しく得るものは小さい。
4. **スレッド間の同期（0x13/0x14 Mutex、0x17〜0x19 Event、0x21/0x22 AddressArbiter）**: 複製の「描いてよい」印（`s_lateReady`）は
   ゲームのスレッドと描画スレッドの間の単純なフラグで、デバッガで止めると描かずに戻ることがあった。ゲームと同じ仕組み（LightLock＝ArbitrateAddress）を
   使えば確実になる。ただし描画スレッドを待たせるとフレームが遅れるので、待たずに「試す」形（try-lock）が向く。
5. **時間計測（0x28 GetSystemTick）**: フレーム制御（F-356/357）や描画の費用の測定を、フレーム数でなくティックで正確に測れる。
   ゲーム自身が 81 か所で使っている。軽いので計測用に最も手軽。
6. **スレッドを止めて安全に書き換える（Luma 0xB3 ControlProcess の SCHEDULE_THREADS）**: ゲームの全スレッドを一時停止してから
   メモリを書き換えれば、「描画スレッドが中にいるかもしれない」ための待ち（`Shutdown` の 100ms 待ちなど）や、書き換え途中を読まれる危険が無くなる。
   フックの取り付け・取り外しに向く。実機での可否は未確認。
   **→ 利用者の判断で採らない（2026-09-25）: 止めるたびに短時間でもフリーズしうるため。**
7. **デバッグ出力（0x3D OutputDebugString）**: 市販機では何もしない（3dbrew）。Luma の GDB スタブが拾うかは未確認。いまのリングバッファ方式の方が確実。
8. **他プロセス・サービス（0x32 SendSyncRequest、Luma 0xA0/0xB0）**: GSP へ直接コマンドを送る・別プロセスを覗くなど。強力だが
   ゲームの描画の順序や GSP の排他と衝突しやすく、これまでの「ゲームと同じ契約で描く」方針（F-259 以降）と合わない。当面は使わない方がよい。

利用者の選択（2026-09-25）: 1・2・5 を進める。2 から着手し、確保までは実機で確認済み。

## 5. 自前確保（svcControlMemoryUnsafe）の運用（IDA-opus-5.5-F035、2026-09-25）

**★採用しない（利用者の判断）: Luma 専用で、他の CFW・エミュレータ・Old 3DS での動作が保証できないため。自前 GUI は従来の借用に戻した（gohan ed1ffb4）。以下は記録。**

- 自前 GUI のアトラス 0x11000 B を SYSTEM 領域から取り、HOME の前後で返す・取り直す（gohan 28a80da）。
  実機: HOME の往復 5 回すべて成功。5 回目に PA が 0x28C32000 → 0x29232000 に変わり、アトラスの移し替え（RelocateAtlas）で描画が保たれた
  （`work/evidence/owngui_home_20260925/`）。
- 通知の出どころ（Luma `k11_extension/source/svc/SendSyncRequest.c`）: APT の ReceiveParameter の応答で、動作中にコマンド 3（RESPONSE）を受けると
  HOME_ENTER、HOME 中に 10〜12（WAKEUP 系）を受けると HOME_EXIT。ライブラリアプレット（キーボード・エラー表示など）も同じやり取りを通るので
  同じ通知が出る見込み（推測、MEDIUM）。
- 利点: ゲームのヒープを借りない（手紙などの場面の確保と競合しない）、大きさの上限がゲームのアロケータに縛られない、場面に依存しない。
- 欠点・危険: OS の資源の勘定の外で SYSTEM 領域を使う（HOME メニュー・アプレット・後から起動する常駐物の確保を失敗させうる。持ったまま HOME で落ちた）、
  Luma 固有（他の CFW・エミュレータでは使えない）、HOME_EXIT が来ない経路があると返したままになる、貼る番地は自分で選ぶ（ゲームの SDK の番地管理と衝突しうる）、
  O3DS では Luma がプラグインのメモリを SD へ退避するほど余裕が無い。

