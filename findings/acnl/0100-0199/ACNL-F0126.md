---
id: ACNL-F0126
aliases:
- F-88
title: 'F-88: phase 1公開中にstock previewへ戻るとtype `0xBC`を早期生成してSIGSEGVになる'
summary: 'confidence: **HIGH**（例外PC・全register・stack・actor/manager memoryと静的呼出し経路を照合）'
date: '2026-08-24'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 5373888
- 5373884
- 8066096
- 9377940
- 9378216
- 9378240
- 9378536
- 5373960
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:5192-5218
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-88: phase 1公開中にstock previewへ戻るとtype `0xBC`を早期生成してSIGSEGVになる

confidence: **HIGH**（例外PC・全register・stack・actor/manager memoryと静的呼出し経路を照合）

容量1版の再開後、thread 220が `PC=0xE1A04000` でSIGSEGVになった。`LR=0x51FFC0` は
generic create wrapper `sub_51FF8C` の `BLX R3` (`0x51FFBC`) 直後であり、stackは
`CatalogPreview_UpdateActor -> UiScreen_OpenById -> sub_51EF38 -> sub_520010 -> sub_51FF8C`
を示した。生成途中actorは `0x30C51C70`、screen typeは `+12=0xBC`、primary vptrは
`0x7B1430`。その `vptr+8` にあるARM命令語 `0xE1A04000` を関数pointerとしてloadしていた。

同時点の一時managerは `0x33133D90`、bank count `+24=1`、create flags `+19=1`、
`g_BsFtrMgr`にも同pointerが既に公開されていた。つまり容量1のphase 1は成功したが、phase 2/3は
未完了である。第3版hookはreadyでなければcacheを無効化しない一方、毎frame stock preview本体へ
戻っていたため、公開済みnonnull managerをCatalogが使用してしまった。

第4版はpreview status 1で `g_BsFtrMgr==0` の間、およびpublished managerの
`(manager[0x13]&3)!=3` の間、保存済みregisterをpopして `BsMenuCatalog_UpdatePreview` 自体から
returnする。manager生成を要求した同一frameもstock bodyへ入れない。完全ready後だけselection
cacheを1回無効化してstock actor生成へ進む。

例外回収ではderived actorが上書きした4 vptrを、constructor直後の基底 `AcFtr` 値
`0x8F1894 / 0x8F19A8 / 0x8F19C0 / 0x8F1AE8`へ戻した。次に `PC=0x520008`、`R7=1` として
generic createを失敗returnさせ、`sub_51F4D8` のstock破棄を安全に通す形で再開した。
第4版cave、private state、全hookは読戻し一致し、breakpointは0件だった。

---

