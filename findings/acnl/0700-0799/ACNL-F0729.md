---
id: ACNL-F0729
aliases: []
title: "通常の字形シートは専用 FontHeap にあり、CMAP と状態を通して参照できる"
summary: "更新側通常フォントはA4・128×128の154枚（画素1,261,568 B）を持ち、通常は専用FontHeapからロードされる。Mgrの状態3の取得関数からResFontを無確保で参照でき、ASCIIと私用記号をCMAPで確認した。"
date: 2026-10-21
category: text
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: "全関数export・RomFS・公開ソース"
addresses: [0x00100104, 0x0012074C, 0x0052D418, 0x0052D838, 0x0052D74C, 0x0052D6A8, 0x00743768, 0x007438B4, 0x001426C8]
tags: ["font", "heap", "layout"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

通常の文字画像は2D_UI_Heapとは別のFontHeapに所有される。ロード済みResFontとそのglyph sheetを取得する経路は新しい画素確保を呼ばない。すべての時点で有効、全ての文字が揃う、という保証とは区別する。
確度 MEDIUM：実RomFSのFINF/TGLP/CMAP、独立したMgrの読込/状態付き取得、GetGlyph/descriptor生産を照合。今回の実機観測なし。

## 根拠

一次証拠は `_local/evidence/107/fonts.json`（全文字map・元ファイルSHA256）、`assets.py`、`0x00100104.txt`、`0x0012074c.txt`、`0x0052d418.txt`、`0x0052d838.txt`、`0x0052d74c.txt`、`0x0052d6a8.txt`、`0x00743768.txt`、`0x007438b4.txt`、`0x001426c8.txt`。元exportは `exports.json`。

| ファイル（更新にあれば更新側） | file B | シート寸法・枚数 | GPU書式 | 全画素 B |
|---|---:|---|---|---:|
| Garden_msg_size16 | 1,296,600 | 128×128、154 | 0xB=A4 | 1,261,568 |
| Garden_ruby | 6,888 | 32×128、3 | A4 | 6,144 |
| Garden_no | 6,404 | 128×32、3 | A4 | 6,144 |
| Garden_no_f16 | 8,468 | 256×32、1 | 0x9=LA4 | 8,192 |
| GardenPlus_JisLevel1 | 717,264 | 128×128、85 | A4 | 696,320 |

- 通常フォントのTGLP本体はcell17×24、baseline18、maxWidth16、sheetSize8,192、7列×5行。file内offset128から画素。descriptorは別に154×20=3,080 B。BCFNT/GPU書式とnw::lyt TexMapの書式番号は同じでない。
- `0x100104` はFontHeapを作って `0x94CC94` へ保存。`0x12074C` は設定判定が0なら1,331,200 B、それ以外983,040 Bを返す。`0x52D838` はheap指定なしならこれを保存し、`0x52D74C` はfileとdescriptorをそのheapから確保する。4通常ファイル+descriptorの素材量1,321,580 Bは別のUIヒープの3.37 MBに足さない。
- `0x52D418` はMgr大域 `0x94C9C8` を一度作り、通常/ルビ/数字/小数字をロードする。`0x52D6A8(mgr,index)` はindex0/1/2/3/4のslotが状態3のときだけ埋込みResFontを返し、それ以外0。通常はmgr+0x188、ルビ+0x320。このgetterは確保を呼ばない。第5slotを通常4書体と同じ常駐扱いにしない。
- `0x6D3144` のメニュー初期化も通常書体の状態付き取得を条件にする。会話TextBoxを探さなければ取れない、という実装ではない。
- `0x743768` はCMAPで文字→glyph、不在は0xFFFF。`0x7438B4` は不在を代替glyphへ置換し、TGLPのsheetを選ぶ。**GetGlyphが何か返すことは収録の証明ではない**。
- 通常CMAPには5,364コード、U+0020…007EのASCII95字を全て収録。私用領域U+E000…E07Eも127コードを収録（`fonts.json`）。原画素をMorton順から復元した `font-pua-preview.png` を目視し、E000…E005のA/B/X/Y/L/R、E006/E041の十字、E049の丸いパッド、E04AのC、E054/E055のZL/ZRの図像を確認した（左右の対応は同名json）。gohanの全文字集合は依頼にないため全充足の判定はできない。例としてU+2190…2193の矢印とU+00D7は収録、U+2713のチェック記号は不在。
- `0x1426C8` は画素を複製せず元sheetからdescriptorを作り、`0x141B48` は変換後アドレスを>>3して保存する。GetGlyphから既存sheet/UVを得る形と一致。
- `0x52D630/0x52D5E0` はMgrを破棄して大域を0にし、`0x132BC4` は各slotを破棄する。FontHeap自体も `0x100918` で破棄する。起動中の一場面でのポインタを永久固定する根拠はない。

公開資料 `STUDY107_PUBLICS`： [3dbrew BCFNT](https://www.3dbrew.org/wiki/BCFNT)、[ObsidianXのBCFNT parser](https://github.com/ObsidianX/3dstools/blob/master/bcfnt.py)、[3dsfont](https://github.com/dnasdw/3dsfont)。ヘッダとCMAP形式の照合に使用。寸法・件数・所有先は実資源/ゲーム命令から別に求めた。

## 反証条件・未確認点

- `fonts.json`は静的ファイル。現在ロード済みか、実機のフィルタ/descriptor状態、各遷移で破棄されないことは未確認。取得値0を扱える必要がある。
- 手紙中も全フォントが常駐するとの実測はない。異なる書体への置換では輪郭・幅・baseline・送りが変わる。
- 更新側のGardenPlusは別の補完書体。通常のCMAPにない漢字が自動でこのslotへfallbackする保証は本記録に含めない。
