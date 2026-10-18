# 対象・入力・IDA環境

ゲーム側は **ARM11 MPCore / ARMv6K / 32-bit little-endian**。ARM/ThumbはTレジスタで切り替える。ARM64・NEON・ARMv7専用命令を前提にしない。浮動小数点はVFPv2として扱い、ARM9側のARM946系ファームウェアとゲームプロセスを分ける。ホスト用Windows x64 DLLと対象用ARM機械語も区別する。

根拠: [ArmのCPUとISAの説明](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/arm-fundamentals-introduction-to-understanding-arm-processors)、[devkitProの3DSビルド設定](https://github.com/devkitPro/3ds-hbmenu/blob/master/Makefile) の `-march=armv6k -mtune=mpcore`、[ArmのVFP説明](https://developer.arm.com/community/arm-community-blogs/b/embedded-and-microcontrollers-blog/posts/utilizing-vector-floating-point-of-arm-processors-in-compact-framework)。搭載構成の補助資料は [3dbrew Hardware](https://www.3dbrew.org/wiki/Hardware)。両CXIはIDAでもARM/32-bit/little-endianを確認、UnicornはARM11 MPCoreを指定して試験した。

## 入力と版の識別

- 本体TitleID `0x0004000000086200`、更新CIA TitleID `0x0004000E00086200`。無印日本版のTitleID。別パッケージのamiibo+用地域アドレスを流用しない。
- 元名・サイズ・SHAは `../inputs/manifest.json`。原本は `../inputs/cia/{base,update}.cia`。
- この2 CIAのTMDはともにTitleVersion 0。通称v1.5は旧既知コードとの全bytes一致に基づく識別で、ファイル名やversion欄から断定していない。再構築の可能性を残す。
- 更新codeは8900608 bytes、SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。旧 `NCCH/0004000E00086200.code` と全bytes一致。以前実機対応を確認した原本との照合であり、今回bootの実機を新たに全照合したものではない。
- base/updateは別コード・別配置。本体側の関数番地を更新版へコピーしない。更新RomFSにはCROがあるが、本体側に同名CROがある前提を置かない。

## ExHeaderの範囲

`index_artifacts.py` の計算結果。endは含まない。ページ確保サイズ・有効データ長・paddingを区別する。

| 入力 | segment | start | end（除外） | size |
|---|---|---|---|---|
| base | .text | 0x100000 | 0x8B6D24 | 0x7B6D24 |
| base | .rodata | 0x8B7000 | 0x9BF80C | 0x10880C |
| base | .data | 0x9C0000 | 0x9F60F8 | 0x360F8 |
| base | .bss | 0x9F60F8 | 0xB6438C | 0x16E294 |
| update | .text | 0x100000 | 0x838018 | 0x738018 |
| update | .rodata | 0x839000 | 0x93EF94 | 0x105F94 |
| update | .data | 0x93F000 | 0x97C768 | 0x3D768 |
| update | .bss | 0x97C768 | 0xAF2694 | 0x175F2C |

ExHeaderは `artifacts/<label>/exheader.bin` に2048 bytesを保持。CXI内 `0x200` からの対応範囲と全bytes一致。独立パーサのVA/page count/sizeと、ローダーのIDB範囲・権限・内容を照合した。`.bss` はdata有効末尾から始まる。
両入力のcode圧縮フラグはfalse。今回の入力ではBLZ展開経路自体を追加検証したとは主張しない。

## IDB

| IDB（project_v2基準） | 役割 |
|---|---|
| `ida/db/acnl_jpn_v15_annotated.i64` | 主IDB。旧code.bin.i64の名前・コメント・型を継承、3DS型を追加 |
| `ida/db/acnl_update_cxi.i64` | 更新CXIの新規分析、比較用 |
| `ida/db/acnl_base_cxi.i64` | 本体CXIの新規分析、比較用 |

imagebase表示は `0x0`、実セグメントは `0x00100000` 起点。今回のcodeでは `VA = offset + 0x100000`。他形式やCROへ一般化しない。
既存注釈IDBにも同じセグメント境界があった。新規ローダーの利点は正しい入力からの再現性と本体/更新比較。移行先のtext/rodata/dataも全bytes一致を確認し、古い入力パスを `artifacts/update/exefs/code.bin` へ修正した。

元 `code.bin.i64` は変更していない。関数数は本体42540、更新44311、旧注釈継承版44190（試験時点）。解析方針・境界の差を含み、真の関数数や追加関数数とは見なさない。
3 DBともLocal Typesエラー0、u8/u16/u32/u64/Handle/Resultのサイズ検査に合格。上流ヘッダの全ABIを実機確認したという意味ではない。

証拠: `work/evidence/{baseline_snapshot,exheader_layout,loader_base,loader_update,annotated_image,annotated_types}.json`（project_v2基準）。
