# F-402: ACNLから内蔵辞書・コードを読む実機試験

2026-09-10。SD/3gxに辞書を同梱せず、既存のfs:USERから内蔵タイトルを読む試験。
自前メニューへの組込みではない。試験用frame wrapperを使い、要求1件ごとに自動Suspendする。

## 実測結果

| 対象・操作 | 結果 |
|---|---|
| 辞書TitleID 0x0004009B00011902、RomFS kind0 | Open成功 |
| 辞書GetSize | 2,045,891 bytes |
| 辞書先頭256bytes Read | 成功、提供済みNCCHの0x1200に一意一致 |
| 辞書Close/カーネルhandle解放 | 両方成功 |
| SWKBD 0x000400300000C002、kind1、.code | Open失敗 0xE0E046BE |
| 同title、kind2、.code | Open成功 |
| code GetSize | 471,668 bytes（圧縮されたExeFSファイルと同サイズ） |
| code先頭256bytes Read | 失敗 0xE0C046F9 |
| code全471,668bytes Read | 成功、bytesReadも一致 |

通信SVCの結果とFS返信Resultを別に記録。成功は双方0を確認。
kind1とkind2はエミュレータ実装では同様に扱われるが、今回の実機では差があった。
F-401の「code kind1」案は実機成功経路として使わず、**kind2**に訂正する。
全体Readと部分Readの結果差は、ExeFSがファイル全体の読取りを要求するとの解釈を支持する。
RAMから全471,668bytesを回収し、提供NCCHの圧縮.codeと完全一致を確認。
SHA-256 `09e684ca41504af96b6548f42e8a2a159f07d3865ca7077e1d4f8356b98ec14e`。
NCCH内のExeFSエントリhashとも一致。ctrtoolで再展開した770,048bytesは従来解析対象と一致し、
SHA-256 `a0b78005b0a99116ca703bc9b7625ce1b0f2d4cc45f66fc6fb9ab8a34244d4f0`。
ctrtoolは提供NCCH headerのsignature FAILを表示したため、署名真正性の検証成功とは扱わない。
ここで確定したのは実機読取り内容・ExeFS内hash・従来解析対象のバイト同一性。

## 実装・検証

ACNL原本sub_1304C8はOpenFileDirectly IPC0x08030204。
sub_346AB8がarchive0x2345678A/16byte archive path/20byte file path/READ1で使用。
別caller sub_1290C4も同session dword_96EF28を使う。今回のsession値0x001D802A。
idalibのdecompile/assemblyとlibctru source/services/fs.cのパッキングを照合。

temporary wrapper: SYSTEM_KEYBOARD/native_fs_step.S。frame hook0x5CE29Cから入り、
既存SWKBD launcher0x838240へtail-chainする。新規コードをRAMから実行する試験ではない。
最終v3は336bytes、0x838400..0x838550（予約は0x838400..0x838600）。
scratch0x9BE800..0x9BF000は既存templateとshared pageの間で、初期ゼロを確認。
全integer register/flags、D0-D15/FPSCR、TLS command buffer256bytesを保存復元。
ソース検査→組立→全literal/branch照合→40 PCケースの保存復元検査→実機読戻し。
PC試験のOS/allocator処理はモックであり、実機FS成功は別の証拠。

## RAM確保

codeは全体Readが必要だったため、475,136bytesの一時領域を要求。
svcControlMemoryの追加確保は0xD86007F3（OutOfMemory）で失敗。
F-296で往復確認済みのゲームAllocMemory 0x4B8CF0とFree 0x569B44を、
この試験の一時バッファだけに使用。戻り値0x32DFC000（今回boot限定）。
変換エンジンの最終メモリ管理をゲーム/GUI依存に決定したものではない。

## 後片付けの状態（完了）

code全体Read成功後、Closeをarmして500msの自動停止を予約・Resumeした。
続く結果取得とReleaseの呼出しがタイムアウト。ユーザーが動作中のACNLを手動Suspendした。
保留されていた処理が進み、Close/Release成功の記録と現在値を確認。二重解放は行っていない。
全データを回収・照合後、一時game heapのFree呼出し完了を確認し、wrapperをrevertした。
frame hookは0xEB09A7E7へ戻り、追加code/scratch全域は適用前backupと一致。
既存SWKBD launcher512bytesと通常chat hookも維持。
最終ACNL state=-1、PC0x004EF364、bp0。gohan.3gxのF-394 hashは不変。
evidence/f402_step/final_restored.json、heap_free.json、code_full_close/release.json参照。

## 次の課題

キーボードを閉じた後のACNL通常frameから、内蔵辞書と圧縮コードをRAMへ取得できることは確認済み。
今回のFS試験はAPT呼出しを追加していない。SD/3gxへの辞書リソース同梱は不要な経路を実測した。
F-402時点では辞書は先頭256bytesまで。続くF-403で全2,045,891bytesの取得・SHA/全bytes照合と内部6辞書の個別照合を完了した。
F-403の試験handle/buffer/wrapperも解放・復元済み。詳細は`system_keyboard_plugin_probe.md`。
次は3gxメモリ確保の実機検証、展開・再配置、独立context作成、実機での候補取得と順位照合。
エンジン自体のネイティブ実行、最終RAM構成/処理時間は未検証。今回のgame heap利用は試験用。

## 証拠・再現

SYSTEM_KEYBOARD/evidence/f402_step/に各要求/返信JSON、生成物、バックアップ。
v1/v2は同名subdirへ保存済み。native_fs_live.pyは停止中のinstall/arm/inspect/revert。
capture_native_fs_reply.pyは要求と返信を保存し、失敗なら後続処理に進まない。
build_verify_native_fs_step.pyはビルド前のsource gateと生成後検証を含む。
最後はClose→svcCloseHandle→一時buffer Free→wrapper revert→独立読戻しを必ず完了する。
