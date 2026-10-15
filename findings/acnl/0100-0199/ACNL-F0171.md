---
id: ACNL-F0171
aliases:
- F-133
title: 'F-133: ResFont の CFNU/CFNT glyph-sheet atlas 経路を静的再監査 — `MEDIUM`（静的構造）/ `LOW`（再利用手順）'
summary: '`nwfont_ResFont_ParseAndAttachResource` (`0x4D8048`) は、既に正規化済みの'
date: '2026-08-24'
category: text
build: acnl_jpn_v15
confidence: MEDIUM
tool: IDA
addresses:
- 5079112
- 5076072
- 7616676
- 1320648
- 1317704
- 5067032
- 5079584
- 1295640
- 1325908
- 1313856
- 1324824
- 1330244
- 2031746
- 1291940
- 7616692
- 5066412
- 5080196
- 5067080
- 8028076
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:8810-8898
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-133: ResFont の CFNU/CFNT glyph-sheet atlas 経路を静的再監査 — `MEDIUM`（静的構造）/ `LOW`（再利用手順）

### 1. フォントリソースの解析と正規化

`nwfont_ResFont_ParseAndAttachResource` (`0x4D8048`) は、既に正規化済みの
`CFNU` (`0x554E4643`) または `CFNT` (`0x544E4643`) を受け取る。CFNT の場合は
ヘッダの BOM・サイズ・チャンク数を検証し、チャンク表から `FINF` / `CMAP` / `CWDH`
 / `TGLP` / `GLGR` を認識する。FINF/CMAP/CWDH/TGLP の埋め込みオフセットは
リソース先頭を加えて実ポインタへ変換し、CFNU に正規化したうえで
`nwfont_ResFont_SetResourceInfo` (`0x4D7468`) に渡す。

`ResFont+0x04` はリソース基底、`ResFont+0x08` は FINF payload、
`ResFont+0x0C` は glyph-sheet descriptor 配列、`ResFont+0x10` は filter flags である。
`ResFont+0x14/+0x16` は constructor が `0` / `-1` に初期化する内部フィールドだが、
今回の経路での用途は同定できない。alternate glyph は `FINF payload +0x02` から読むため、
これらを alternate/cache と呼ぶ旧記述は撤回する。

### 2. TGLP の確定フィールド

静的な参照先（`0x7438A4`, `0x1426C8`, `0x141B48`, `0x4D5118`）を突き合わせ、
命令が直接参照する TGLP payload のフィールドを次のように整理した。ここで「確定」は
このビルドの命令上の offset/幅を指し、実機で全資源を通過させたという意味ではない。

| offset | 型 | 内容 |
|---:|---|---|
| `+0x00` | u8 | cell width |
| `+0x01` | u8 | cell height |
| `+0x02` | u8 | baseline 系の値（符号付き getter あり。名称は未確定） |
| `+0x03` | u8 | max character width |
| `+0x04` | u32 | 1 sheet の byte stride/size |
| `+0x08` | u16 | sheet count |
| `+0x0A` | u16 | texture format |
| `+0x0C` | u16 | columns per sheet |
| `+0x0E` | u16 | rows per sheet |
| `+0x10` | u16 | sheet width (pixels) |
| `+0x12` | u16 | sheet height (pixels) |
| `+0x14` | ptr | raw glyph-sheet atlas data |

`nwfont_ResFont_GetGlyphSheetTableBytes` (`0x4D8220`) は `20 * LE16(TGLP+0x08)`
を返すため、descriptor 1 個のサイズは 0x14 bytes である。

### 3. glyph-sheet descriptor と GPU への橋渡し

`nwfont_ResFont_SetGlyphSheetTable` (`0x13C518`) が配列を保存すると、
`nwfont_ResFont_InitGlyphSheetDescriptors` (`0x1426C8`) は sheet ごとに
`nwfont_GlyphTextureDescriptor_Init` (`0x141B48`) を呼ぶ。descriptor の確定フィールドは:

| descriptor offset | 内容 |
|---:|---|
| `+0x00` | texture handle 初期値 0 |
| `+0x04` | owner `ResFont*` |
| `+0x08` | `sub_143B54(raw_sheet)>>3`。`0x143B54`→`0x140C40` のアドレス変換後に `>>3` した GPU 用表現（raw virtual pointer の単純な `>>3` ではない） |
| `+0x0C` | `LE16(TGLP+0x12)` sheet height |
| `+0x0E` | `LE16(TGLP+0x10)` sheet width |
| `+0x10` | `LE16(TGLP+0x0A)` texture format |

raw sheet は `TGLP+0x14 + index * LE32(TGLP+0x04)` で求まり、最後に
`0x143718`→`0x144C44` が全 sheet 範囲を SVC `0x32` の IPC request へ渡す。
この経路の IPC header は `0x001F0082`、helper の process-handle 引数は
`dword_8AD218 = 0xFFFF8001` である。これは既知の `GSPGPU_FlushDataCache`
(`0x13B6A4`, header `0x00080082`) と同じ SVC 形式・アドレス/サイズ引数を使うが、
header の command field が異なるため、両者を同一 API と断定しない。呼び出し側が
atlas 全体の raw 範囲を渡していることから、ここでは「range cache operation」とだけ
記録し、`0x001F` の正確な GSP command 名は未確定とする。したがって、atlas が
後続の texture 設定経路へ渡される点は支持されるが、GPU upload/bind の完了や cache API 名・
command semantics は静的には確定していない。

glyph 描画側では `nwfont_ResFont_GetGlyph` (`0x7438B4`) が CMAP/CWDH/TGLP から
一時 glyph record を作り、`nwfont_CharWriter_EmitGlyphQuad` (`0x4D4EAC`) が
glyphWidth と cell 座標から quad/UV を生成する。`0x4D5118` で sheet width/height、
format、raw sheet base、ResFont filter flags を `nwfont_CharWriter_SetGlyphTextureParams`
 (`0x4D8484`) に渡し、続いて `0x4D5148` で generic GPU draw routine
 (`0x7A7FAC`, 引数 `6,0,4`) を呼ぶ。これは自前 GPU コールバックから既存 atlas を
再利用するための最短の静的経路である。

### 4. 残る動的検証

parser・TGLP offset・descriptor layout・range cache request の関係は静的根拠が揃った（この項の confidence は、
F-129 の live `ResFont`/CFNU ヘッダ照合を除き、実機で当該関数を通過させた動的確認をまだ含まない）。
一方、実機起動ごとの live `ResFont*`、実際の texture format/stride、texture handle が
生成されるタイミング、そして自前 callback から既存 descriptor を直接使えるかは未検証である。
次段階では読み取り専用の動的観測で descriptor と `GetGlyph` の実値を採取し、
その後に最小の 1 glyph GPU コマンドへ移植する。

採取スクリプトは `scratchpad/dump_glyph_atlas.py`。毎回 live heap を再走査し、
ResFont/TGLP/descriptor の値を表示するだけで、メモリ書込みや breakpoint 操作は行わない。

---

