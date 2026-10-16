# F-401: 再配置参照の追加監査・内蔵タイトル読取り条件

2026-09-10。F-400の残件を調査。SD/3gxへの辞書・変換表同梱は行わない方針を維持。
実機への接続、コード適用、ビルドは今回行っていない。

## 結果

再配置箇所を、6入力で観測した52語から、静的に裏付けた315語へ拡張した。
25入力・2配置先で原本候補列と順序が一致（50比較）。旧52語の版も同じ25入力で成功したため、
追加263語の全てが現在の日本語予測で必須と確認されたわけではない。
追加分は、未観測分岐・別mode等にも存在する静的参照の取りこぼしを減らすもの。

内蔵タイトル読取りについては、ローダーのprogramHandleを借りず、
fs:USERのARCHIVE_SAVEDATA_AND_CONTENT（0x2345678A）へタイトルIDを渡す試験案を確定。
現在の本体上での成功はまだ観測していない。Lumaの権限処理とパスの根拠は下記。

## 静的監査の範囲と検証

入口0x190408、0x18C628、0x111FD4、0x1181D0とcallback3個を起点に、
直接分岐・直接呼出し・明示されたsub参照を再帰的に追跡した。
243アドレスの逆アセンブルを保存し、直接参照の未取得queueは0、取得エラー0。
共有コード範囲や途中入口も含むため、243を独立関数数とは呼ばない。

重要な検査上の修正: idalibは大きい出力を**先頭10命令へ省略**することがある。
cursor.doneがtrueでも完全な命令列とは限らなかった。7件で検出し、同ツールが示した
localhostの完全版JSONを取得し直した。instruction_countと保存命令数の一致を必須にした。
最初の不完全な一覧は再配置生成の旧52語包含検査で拒否され、適用には使用していない。

expand_static_relocations.pyは保存したidalib情報から次を生成する。

- literalの参照元と指す先を照合し、原本32-bit値の一致を確認。
- PCから索引する15個のswitch tableは、IDAが記録する分岐先と各要素の値を照合。
- dword_1A7DE0+2のような途中アドレスは、literal側のxrefでも独立に照合。
- 旧52語を全て包含。未解決literalと未処理switchは0。合計315語。
- 収集したコード内にSVC、MOVW/MOVTは見つからなかった。

これは**直接参照の追跡を完了した条件付き監査**であり、任意のcallbackや任意の辞書構成に
対する全実行経路の形式的証明ではない。命令表現に基づく抽出器の対象外となるアドレス生成や、
未観測のデータ内pointerについても、全て不存在と断言はしない。

## 間接呼出し

BLXを使う22箇所を別に列挙。6箇所は辞書のファイルI/O用vtable呼出し。
0x14A6F8のassembly/decompileはhandle+8のbit1/2/4で常駐データへ切り替える。
PC構築はこの欄が7のため、これらのファイルI/O経路を使わない。
他の箇所は辞書/変換状態のcallbackに関係し、実行時の登録先に依存する。

verify_relocated_callbacks.pyは22箇所すべてにPC観測用の検査を設け、
呼出し先が再配置済み0x19BECC、0x19C334、0x16B890のいずれかであることを確認する。
検査対象7入力の結果はevidence/f401_callbacks.json。未ヒット箇所まで動作確認済みとはしない。
未知のcallbackを許容する汎用エンジンとしては扱わず、日本語・未学習・常駐辞書・独立contextを
現行の利用条件とする。学習/ユーザー辞書、別言語、並行利用は別途検証が必要。

## 実機側のFS権限

Luma3DS公式ソースを取得し、commit `aef31308a7ea33601d9d21cdede1dfd8471c07b0`と
対象ファイル3本のbytes/hashを照合した。ソース根拠:

- [PM launch.c](https://github.com/LumaTeam/Luma3DS/blob/aef31308a7ea33601d9d21cdede1dfd8471c07b0/sysmodules/pm/source/launch.c):
  loadWithoutDependenciesは通常プロセスの登録前にfs_access_infoを0xFFFFFFFFへ変更し、FSREG_Registerする。
- [SM services.c](https://github.com/LumaTeam/Luma3DS/blob/aef31308a7ea33601d9d21cdede1dfd8471c07b0/sysmodules/sm/source/services.c):
  サービスアクセスリストの照会は許可を返す。
- [ARM9 patches.c](https://github.com/LumaTeam/Luma3DS/blob/aef31308a7ea33601d9d21cdede1dfd8471c07b0/arm9/source/patches.c):
  patchP9AccessChecksが存在する。ただしここだけから個々のFS命令の成功を保証しない。

従って「ACNLの元exheaderで制限されるから内蔵タイトルは読めない」とは結論できない。
標準Lumaのこの設定下では読取り可能と考えるソース上の根拠がある（MEDIUM）。
現在の本体のLuma版・独自変更・FSセッション初期化・対象タイトルの存在はこの調査では未確認。
ソースの権限設定と、現在の実機が実際に返すResultは別の証拠である。

## 読取り専用の確認手順

prepare_builtin_content_paths.pyがbinary pathを生成し、長さと各フィールドを検査する。
結果evidence/f401_builtin_content_requests.json。
archive pathは16 bytes: TitleID(u64 LE), NAND=0(u32), 0(u32)。
file pathは20 bytes: open_type=0, content_index=0, kind, name[8]。

| 対象 | TitleID | kind | name |
|---|---|---|---|
| 日本語辞書RomFS | 0x0004009B00011902 | 0 | 全0 |
| 内蔵SWKBDのExeFS code | 0x000400300000C002 | 1 | .code と終端0 |

両方ともarchive ID=0x2345678A、PATH_BINARY=2、FS_OPEN_READ=1、attributes=0。
根拠は[libctru romfs_dev.c](https://github.com/devkitPro/libctru/blob/master/libctru/source/romfs_dev.c)の
romfsMountFromTitle、および[Azahar archive_ncch.cpp](https://github.com/azahar-emu/azahar/blob/master/src/core/file_sys/archive_ncch.cpp)・
[archive_ncch.h](https://github.com/azahar-emu/azahar/blob/master/src/core/file_sys/archive_ncch.h)。
後者はエミュレータ側実装の証拠であり、実機側の全権限挙動を再現している保証としては使わない。
辞書のTitleIDとNAND指定は、原本SWKBDの0x18C18C→0x16F13Cでも裏付ける。

初期化済みFSセッションからOpenFileDirectly→GetSize→長さ制限付きRead→Closeの順。
成功handleのみCloseし、Resultと読取りbyte数を別々に保存する。書込み/作成/サイズ変更は不要。
まず両ファイルが開けるかを確認するだけにし、取得したcodeは実行しない。
圧縮の有無を確認して必要なら展開し、原本イメージSHA-256
`a0b78005b0a99116ca703bc9b7625ce1b0f2d4cc45f66fc6fb9ab8a34244d4f0`
とセグメント配置が一致してから再配置対象とする。
失敗時はResultを根拠に切り分け、SDの辞書ファイルへ自動で切り替える設計にはしない。

## 再現物

```
python -X utf8 SYSTEM_KEYBOARD/expand_static_relocations.py
python -X utf8 SYSTEM_KEYBOARD/verify_static_relocation.py
python -X utf8 SYSTEM_KEYBOARD/verify_relocated_callbacks.py
python -X utf8 SYSTEM_KEYBOARD/prepare_builtin_content_paths.py
```

全てPCのみ。取得済みのf401_static_scan.jsonには完全版の静的証拠を保存済み。
recover_idalib_exports.pyのURLは一時出力の回収記録なので、通常の再検証で再実行する必要はない。
F-400の観測52語版は過去試験再現用として維持し、static_fixups=Trueで315語版を選ぶ。
