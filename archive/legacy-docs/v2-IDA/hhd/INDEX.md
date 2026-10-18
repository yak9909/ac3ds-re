# HHD（ハッピーホームデザイナー）資料の入口

ACNL の資料（`docs/` 直下・`work/FINDINGS.md` など）とは分けて置く。ACNL 前提の知見を HHD へ当てない。

- 対象: どうぶつの森 ハッピーホームデザイナー JPN、TitleID `0x000400000014F000`、製品コード CTR-P-EDHJ。
- **解析は v1.1（Rev 1、TitleVersion v2080、exheader remaster 2）だけを見る。** v1.0 は保管のみ（利用者指示 2026-10-05）。

## ファイルの置き場

| 物 | 場所 | 備考 |
|---|---|---|
| 原本 cci 2 本 | `inputs/hhd/cci/hhd_jpn_rev0.cci`（v1.0）/ `hhd_jpn_rev1.cci`（v1.1） | Git 管理外。大きさ・SHA-256 は `inputs/hhd/manifest.json` |
| 参考スクショ | `inputs/hhd/screenshots/`（キャラクリ 6 枚）、`inputs/hhd/screenshots/decorate_menu/`（家具・壁紙/床紙リストと模様替え画面 11 枚、2026-10-06） | 400x480（上 400x240 ＋ 下 320x240）。PNG 化 `tools/hhd/bmp_to_png.py` |
| ExeFS・ExHeader 等 | `artifacts/hhd/v1.x/`（`exefs/code.bin` は展開済み） | ctrtool v1.3.0。台帳 `artifacts/hhd/v1.x/manifest.json` |
| RomFS | `artifacts/hhd/v1.x/romfs/` | 利用者が置いたもの。ctrtool の抽出と全ファイル一致（`romfs_verify.json`）。Git 管理外 |
| CXI | `artifacts/hhd/v1.1/main.cxi` | IDB 作成用。Git 管理外 |
| IDB | `ida/db/hhd_jpn_v11.i64` | `tools/hhd/make_idb.py`（ctr_loader、セグメント全バイト照合 → `work/evidence/hhd/loader_v11.json`） |

v1.1 の配置（exheader）: .text `[0x100000, 0x637A10)`、.rodata `[0x638000, 0x7272E4)`、.data `[0x728000, 0x762188)`、.bss 0x1066E0 B。
`code.bin` は 3 つが連続するので VA − 0x100000 で読める。

## RTTI

**無い**（IDA-opus-5.5-HHD-F001）。`.code` に `__cxxabiv1`・`type_info`・`N2nw`・`_ZTV`・`_ZTI` 等が 0 件（ACNL は `N2nw` 158 件）、CRO も無い。
vtable 自体はある（offset-to-top・typeinfo の欄は 0）。クラスは役割から仮名を付ける。比較の道具 `tools/hhd/vtables.py`。

## 描画ライブラリ

レイアウトは **FLYT/FLAN 版 7.2.1.0**（`.bflyt` / `.bflan` / `.bflim` / `.bffnt`、SARC の `.arc` に入る）。ACNL の NW4C（`.bclyt`）とは別系統。
sead の文字列（`sead::TaskMgr` 等）はある。3D は `.bcres`（Npc・Puppet）。

## 道具（`tools/hhd/`）

| 道具 | 用途 |
|---|---|
| `make_idb.py` | CXI 切り出しと IDB 作成 |
| `verify_romfs.py` | RomFS フォルダと ctrtool 抽出の全ファイル照合 |
| `extract_layouts.py` | Layout の .arc を 3DSkit（`tools/vendor/3DSkit`、venv `tools/python/hhd3dskit`）で展開・JSON/PNG 化 |
| `layout_tree.py` / `flan_summary.py` / `export_palettes.py` | 3DSkit の JSON の要約（形式の解釈は 3DSkit に任せる） |
| `dis.py` / `vtables.py` | objdump による注記つき逆アセンブル、vtable の比較 |
| `bmp_to_png.py` | スクショの PNG 化 |
| `sarc.py` / `bflyt.py` | 自作の読み取り（利用者指示で 3DSkit へ切り替えた。照合用に残す） |

## トピック

- [キャラクリ画面](chara_create_screen.md)
- 状態・発見・残件: `work/hhd/STATE.md`・`FINDINGS.md`・`TODO.md`
