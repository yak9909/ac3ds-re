# 内蔵変換エンジンのネイティブ検証版（F-407、2026-09-11）

**実機で、内蔵キーボードを起動せずに変換候補を取得できた（HIGH）。**
利用者が配置・再起動したF407版をheader/全コードアンカーで照合し、
展開・再配置のみの試験成功後、「かんじ」・文章・「か」を各1回実行した。
候補数は17/6/143件、内容と順序はPCの原本実行に一致。
前の2入力は過去に取得した実機SWKBDの候補列にも一致した。

全要求で内蔵FS読取り/Close/Releaseとarena解放が完了。
変換3要求はstack guard成功、getter終端0を確認した。
最終ACNL Suspend、PC `0x0056085C`、bp0、command0、試験arena保持なし。
F407はゲームコードへフックを書かず、検証用mailboxの要求だけで動く。
正常版gohanとF404版のファイルは変更していない。
操作の再現は [検証版README](../Plugin/SwkbdEngineProbe/README.md)。

## 実機結果

| 要求 | 初回の件数 | getter列挙後 | 照合・解放 |
|---|---|---|---|
| prepareのみ | 変換なし | 0 | 展開CRC、315語、辞書配置、全FS/arena解放成功 |
| 「かんじ」 | 17 | 17 | 原本PC/保存SWKBDと候補順位一致、guard/全解放成功 |
| 「わたしはねこがすきです」 | 6 | 6 | 同上。先頭「私は猫が好きです」 |
| 「か」 | 50 | 143 | 原本PCと全順位一致、追加検索/guard/全解放成功 |

arenaは各回 `0x061BE000`、要求サイズ5 MiB。
辞書2,045,891 bytes/圧縮code471,668 bytesの全ReadとCRC、Close/Releaseが全て成功した。
展開後CRC `0x423DC1C2`、再配置315語。変換時dictionary_used=2,064,244 bytes。
各要求を1回設定し、5000msの自動Suspend付き走行後にstate2/failure0/stage10を確認。
この時間は停止予約の設定であり、変換処理自体の測定時間ではない。

証拠は `evidence/f407_engine/hardware_prepare.json` と
`hardware_kanji.json` / `hardware_phrase.json` / `hardware_ka.json`。
最後のreport全34,452 bytesを別の読取りで保存し、候補143件と構造化結果を再照合。
`hardware_final_report.bin` / `hardware_final_state.json` / `hardware_verified.json` を参照。
ソース・実行物・実機証拠は `BACKUP/plugin_f407_hardware_confirmed/` に保存。

これは独立した非学習contextによる予測候補の取得成功であり、
全入力や個人学習、文節境界を指定する別APIまで実機検証したという意味ではない。

## 目的と配置

画面やAPTを使わず、実機の内蔵タイトルから取得したコードと辞書で候補を取得する。
元SWKBDコード・辞書テーブルをSDや3gxへ同梱しない。既存メニューへの統合も行わない。
再配置情報315組だけはF401の解析結果から生成してローダーに持たせる。

F404と同じread-only FS bridgeで5 MiBを確保し、辞書RomFSと圧縮.codeを全体Readする。
サイズとCRCは既存の実機全bytes/SHA確認済みデータに固定し、違う版を実行しない。

| arena内の相対位置 | 用途 |
|---|---|
| `0x000000..0x200000` | 辞書RomFSを取得後、6辞書を前方へ詰める。prefix/handle/補助bufferもここ |
| `0x200000..0x2C6000` | 展開したimage、初期化済みdataとゼロBSS |
| `0x2C6000..0x3C6000` | 独立context |
| `0x3C6000..0x3D6000` | 呼出し用stack。下端`0x1000` bytesにguard |
| `0x3D6000..0x44A000` | 圧縮.codeの取得用。末尾は取得サイズに対する余白 |

辞書6本の配置とhandleの使用量は2,045,536 bytes、補助bufferを加えた変換時は2,064,244 bytes。
候補300件×56 UTF-16 code unitsはreport内に持ち、report全体は34,452 bytes。
単発要求ごとにFS handleをClose/Releaseし、最後にarenaをFreeする。

## 展開・初期化の根拠

圧縮形式は [Luma公式loaderのLZSS展開](https://github.com/LumaTeam/Luma3DS/blob/master/sysmodules/loader/source/loader.c#L50)
とfooter/後方参照を突き合わせた。実装には入力/出力の境界検査を追加し、
展開した770,048 bytesを既にctrtoolで取得した原本と全bytes比較して一致した。
展開後CRC32は `0x423DC1C2`。

RomFSはインストール済みlibctru `3ds/romfs.h` と保存された公式 `romfs_dev.c` の構造に従う。
`JA_small/njcon.a` と `JA_small/32/` の5本を名前・親・子/兄弟リンクから解決。
全メタデータ・NJDC署名・範囲を調べてから、互いの未読領域を潰さない前方コピーを行う。
壊れた長さ・オフセット・循環は失敗として返す。従来の既知file offsetへの決め打ちは使わない。

315組は `f401_static_relocations.json` と原本wordを生成時/適用時に確認する。
原本初期化 `0x190408` → 辞書slot/関数型辞書slotの構成 → 日本語初期化 `0x18C628` →
予測 `0x111FD4` → getter `0x1181D0` の順で、各番地には再配置差分を足す。
引数と初期値はF398〜F401の検証済みPCモデルに対応する。

新stackへの切替えは `EngineCall.s` に分離。R4〜R11、D8〜D15、FPSCR、SPを保存/復元し、
第5/6引数を切替え後のstackへ渡す。キャッシュはF406実機成功と同じ全体SVC `0x92/0x94`。
範囲指定SVC `0x91/0x93` は使用しない。変換完了後に下端stack guardを照合する。

## 照合結果と範囲

ソース確認・ホスト検査・ARM構文確認を通してからビルドした。
生成した自前ARMコードの1301命令、213直接分岐、48PCリテラルを機械検査した。
エンジン本体の根拠はF401の静的解析と、今回の原本を含むPC実行結果。

| PC試験 | 結果 |
|---|---|
| 準備のみ、arena `0x061BE000` | 展開/辞書/315語一致、エンジン呼出し0、SVC0 |
| 「かんじ」、arena `0x061BE000` | 17候補、順序一致 |
| 「わたしはねこがすきです」、arena `0x06002000` | 6候補、順序一致 |
| 「か」、arena `0x061BE000` | 143候補、getterによる追加検索も一致 |

上の3変換は**生成したARM版ローダーから原本エンジンを実際に呼んだPC試験**。
原本VAは未マップ。キャッシュ同期後のimageは書込み禁止、エンジン向けOS mockなし。
呼出し終了時の保存対象レジスタ/FPSCR/SP、stack guard、全6辞書の本体不変を確認。
比較対象は独立した `query_candidates.py` による原本実行。
17件/6件はF398で保存実機候補との一致も確認済み。

PC上のcache SVCはmockであり、PC結果だけでは実機確認を代替しない。
その後、上記の3入力について実機の初期化・変換・帰還・全解放が成功した。
処理時間の内訳、学習/ユーザー辞書、並行利用、全入力/全間接経路は未確認。

mailbox driverは10条件を模擬し、別版・未準備の変換・要求中・bpあり・不正入力等で
実機書込みに相当する処理が0件になることを検査した。ファイル配置後は実機のアンカーを再確認する。

## 成果物・証拠

3gx: 289,985 bytes、SHA-256
`50ec21a1bde6d52f13fa916ac23aceb2f81dbb833a5ca4db8ca77c3b96368385`。
10 MiB設定、exeSize258,048 bytes、heapSize10,227,712 bytes。

- `SYSTEM_KEYBOARD/evidence/f407_engine/prebuild.json`: ソース/事前検査
- `artifact.json` / `disasm.txt`: リンク済み命令の検査と実機照合アンカー
- `emulation.json`: 原本エンジンを含むARM実行結果と候補全列
- `control_contract.json`: report/input/commandの実際のELF symbol
- `driver_tests.json`: 誤適用・再送の防止条件
- `BACKUP/plugin_f407_pc_verified/`: ソース、検証成果物、3gx/ELFの保存

現行ELFのmailboxはreport `0x07033AE0`、command `0x07033ADC`、input `0x0703212C`。
固定番地だけを信用せず、driverがartifactと実機を照合してから触る。
