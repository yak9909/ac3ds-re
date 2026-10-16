# 内蔵変換エンジンの3gx検証（F-404〜F-406、2026-09-11）

F-407のネイティブ検証版は実機成功。キーボードを起動せず、17/6/143候補を原本と同順で取得し、全解放まで確認。
最新は [F-407](system_keyboard_native_loader.md) を参照。以下はF-406完了時点の記録。

最新: F-406で、確保したplugin heap上のARM関数を実行して正常に戻った。
F-404の5 MiB確保/全域照合、内蔵辞書/code全Read/CRC/Close/Release/freeも再び成功。
一時vtableフック・cave・controlを全復元し、独立した読取りでも確認した。
ACNLはSuspend、PC `0x00463E24`、bp0、command0、試験buffer保持なし。
**変換エンジン本体は未実行。** 次はRAM内の展開・再配置・独立contextでの候補取得。

- [F-406 実機結果](../SYSTEM_KEYBOARD/evidence/f406_exec/hardware_result.json)
- [F-406 復元確認](../SYSTEM_KEYBOARD/evidence/f406_exec/restored.json)
- [F-404 初回結果](../SYSTEM_KEYBOARD/evidence/f404_plugin/hardware_result.json)

## F-405のクラッシュ原因とF-406の変更

利用者提供の `Plugin/crash_dump_00000004.dmp` をLuma公式ヘッダと保存処理に従って解析。
SHA-256 `5f11fe66cb78c6dd10bb1f36d0fb03517d9d5dcb1d817eb8424be40b53349f3b`。
`parse_crash_f405.py` の結果と、ダンプ命令列を開いたidalibセッション
`f405_crash_kernel` の逆アセンブルを突き合わせた。

| 観測 | 値・意味 |
|---|---|
| 例外 | ARM11 core1、data abort、SVC mode |
| PC / 命令 | `0xFFF2B3F8`: `MCR p15,0,R1,c7,c10,1`（D-cache clean by MVA） |
| R1 / FAR | ともに `0x061BE000`、試験で確保したarenaの先頭と一致 |
| R0 | `0x061BE020`、キャッシュ操作範囲の終端 |
| DFSR | `0x805`、section translation fault、write |
| 保存された実行プロセス | `socket`、TitleID `0x0004013000002E02` |

ヒープ命令の実行ではなく、指定VAのキャッシュ処理で停止したことはHIGH。
他コアの異なるアドレス空間で処理した可能性はあるが、そこに至るdispatch経路は未確認でLOW。
`svc 0x91` と `svc 0x93` のどちらの要求中だったかはダンプだけでは判別できない。
PCのABI検査ではSVCをmockしていたため、実機カーネルのこの挙動を検出できなかった。
F-405は再実行しない。ユーザーの再起動後、旧cave/controlのゼロと元vtableを照合し、
旧試験の一時変更が消えたことを確認した。

F-406では範囲指定をやめ、`svc 0x92`（全D-cache）→`svc 0x94`（全I-cache）を使用。
根拠は保存済みLuma公式ソースの
`SYSTEM_KEYBOARD/evidence/f401_sources/luma/sysmodules/rosalina/source/gdb/mem.c`
にあるGDBメモリ書込みの処理、および `k11_extension/source/svc.c` の番号対応。
これらはユーザーVAを引数に取らない。

| 試験 | キャッシュ処理 | ヒープ関数 | 後続のFS/解放 | 一時変更の復元 |
|---|---|---|---|---|
| F-404 | ヒープ命令実行なし | 未試験 | 全成功 | 当該フックなし |
| F-405 | 範囲指定 `0x91` / `0x93` | 到達未確認 | 完了未確認 | ユーザー再起動後に確認 |
| F-406 | 全体 `0x92` / `0x94` | `0x5A` を返して復帰 | 全成功 | 全域読戻し一致 |

F-406のwrapperは120 bytes、SHA-256
`62f54d3099475eb4e6be2ee1830978c06fa9371a74599b60010e9721284bccd6`。
組立前のソース確認、全4リテラル/1直接分岐とコード境界、4条件のABI検査がPASS。
適用前にACNLの6命令アンカー、読み込まれた3gxのアンカー、Suspend/bp0、
未使用のcave/control、mailbox idleを照合した。

`TargetApi::Validate` のslot `0x07029DD8` を `0x070012B8` から
`0x00838600` のwrapperへ一時変更。元Validateが成功した場合だけarenaへ
`MOV R0,#0x5A; BX LR` を置き、キャッシュ処理後に `BLX` する。
観測用control `0x009BE840` はphase4、return `0x5A`、arena `0x061BE000`。
後続のF-404本体はstate2/failure0、touch_pass1/freed1、両ファイルの全操作成功。
5秒の自動Suspend付き走行1回による結果であり、場面転換や全入力の保証ではない。

結果保存後、slotを元値へ戻してからcave予約全 `0x200` bytesとcontrol全 `0x20` bytesを復元。
vtable全体のbackup一致と、別の読取りによるゼロ確認を保存した。
3gxファイルはF-404のまま。`plugin_exec_live_f406.py` の既定動作はinspectで、
install/revertは `builtins.SWKBD_EXEC_ACTION` で明示する。Resumeは別操作。

メモリmap APIは空のリストを返したが、これは未マップの証拠に使わない。
実際の範囲はplugin header、Validate内の `svcQueryMemory`、全域touchと
今回の関数実行結果で照合した。今回の2命令ではVFPやエンジンABIは未検証。

## F-404の準備記録（以下の待機状態は解消済み）

独立3gxは事前検証→ビルド→成果物検査が完了。
`Plugin/SwkbdProbe/README.md`に配置/操作/復元手順、`evidence/f404_plugin/artifact.json`にhashとアンカー。
284,130 bytes、SHA-256 `82b89abd667da13c56e83d8a2b8fcbfc21672ad7eb0e219345d466400595a2a4`。
PC正常+11失敗条件、ARM構文、生成517命令/67分岐/23リテラル検査PASS。
概算空き8,519,680 bytesから5 MiBを確保する試験。実機成功はまだ主張しない。
現在ACNLは従来のgohanでSuspend、PC0x0014E378/bp0。frame/chat hookは既存F396のまま。
SDの配置先はPCから見えていないため、利用者による検証用3gx配置・再起動を待つ。

利用者は、メモリ不足を解消できるなら3gxでの検証へ移行したいと指定した。
目的は画面/APTなしの変換エンジン実行。自前メニューへの統合は目的に含めない。
辞書・SWKBDコードは実機内蔵タイトルからRAMへ読み、SD/3gxへリソース同梱しない。

## 確認できたこと

- F-403: ACNLから辞書RomFS全2,045,891 bytesを8分割で取得。
  SHA-256 `03ee22fbd00d0968b2720eb56a24cff20659b3eedd1f8e596708e0a25d4c8428`。
  提供NCCHの0x1200以降と全bytes一致し、内部6本の辞書も個別一致。
  `SYSTEM_KEYBOARD/evidence/f403_step/dictionary_verified.json`。
  file handle/256 KiB bufferを解放し、一時wrapper/scratchを復元済み。
- F-403停止時: SystemHeap空き合計542,604 bytes、4096整列最大540,672 bytes。
  lyt heap空き合計982,720 bytes、4096整列最大499,576 bytes。
  2つのroot heapは直接の空きゼロ。配下heap全走査はリスト循環検出で中止し未完。
  この結果だけで全プロセスメモリ不足とは断定しない。
  `inspect_heaps_f403.py`、`heaps.json`。構造根拠はACNL静的IDBの
  0x74DAA4/0x55D050/0x74D744。以前の約2MB確保失敗はlyt allocatorでありgfx allocatorとは異なる。
- F-404実機読取り: 停止PC0x0014E378。plugin header0x07000000:
  heapVA=0x06000000, heapSize=0x003E1000, exeSize=0x0011F000。
  合計5 MiB。現行plgInfoのMemorySize: 5MiBと整合。
- Lumaの`file_loader.c`はmemoryRegionSizeに対応する5/2/10 MiB設定を持つ。
  heapSize = 総量 - exeSize。新しい総量はロード時に確保されるので再起動が必要。
  [公式ソース](https://github.com/LumaTeam/Luma3DS/blob/master/sysmodules/rosalina/source/plugin/file_loader.c)。
  ローカル固定版は`SYSTEM_KEYBOARD/evidence/f401_sources/luma/`。
- CTRPFの参考ソース`pluginInit.cpp`では内部Heapがnewlibから1 MiBを予約する。
  実機symbolに対応する値も0x100000。大きい検証bufferにはnewlibのmemalign/freeを使う。
  内部`Heap::MemAlign`の空きをnewlib全体の空きと取り違えない。

## 次の最小試験

独立プロジェクト`Plugin/SwkbdProbe`、MemorySize: 10MiB。
mailboxで指示されたときだけnewlibから5 MiBを4096整列で確保する。
全域write/readback、内蔵辞書/codeのOpen/GetSize/Read/Close、CRC32照合、全解放を行う。
結果はmailboxと短い診断ログへ。エンジン本体への分岐や実行権限変更はこの段階では行わない。
この検証に成功した後、展開・再配置・context初期化・実機候補取得へ進む。

10 MiBを実際に確保できるかは未確認。機種/ローダーの設定によっては
ゲームに渡るメモリ量も変わる（memoryblock.c）。5 MiB増量を無条件に安全・成功と断定しない。
現行の正常版gohan.3gx（F-394）は保存したまま別成果物を作る。
