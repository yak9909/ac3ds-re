---
id: ACNL-F0415
aliases:
- F-390
title: 'F-390: 破損した3gxをしずえスキップ統合前へ復元（2026-09-09）'
summary: '**ソースと成果物の復元はHIGH、実機表示の再確認は未実施。**'
date: '2026-09-09'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:24436-24479
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-390: 破損した3gxをしずえスキップ統合前へ復元（2026-09-09）

**ソースと成果物の復元はHIGH、実機表示の再確認は未実施。**

破損時の現行ツリーを調べると、`OwnGui.cpp`にF-376の診断設定
`kDiagNoHooks = true`が残り、`InstallHooks()`がA1/A2描画フックを入れず成功扱いで
returnしていた。同時に`InstallInputBlock()`の呼び出しもコメントアウトされていた。
これは「診断終了後に通常構成へ戻した」とするF-381と矛盾し、描画されない症状を直接説明する。
破損3gxのリンク一覧では`ShizueSkip::Install`/`Fire`は参照されず除去されており、
しずえ処理の実行よりも診断用変更の残留が破損の本体だった。

`BASELINE/gui_v2_ok_f322`、実機確認済み描画版F-346、入力遮断付きF-355を比較し、
後から入ったF-375の空リスト修正、現行のケーブ配置、F-365の一般機能、
文字/数値キーボードは保持した。
その上で次だけを除去・復旧した。

- `kDiagNoHooks`と早期returnを削除し、A1/A2を常に通常手順で検査・導入する。
- `InstallInputBlock()`呼び出しを復活する。
- 未検証の常駐`ShizueSkip`ソース、ヘッダ、メニュー項目、include、uninstall呼び出しを除去する。
- F-366で追加したSimulator項目と14字分のフォントを生成元から除去し、美咲362字・
  総字形390のF-355構成へ戻す。
- F-366のフォント再生成で消えていた`GetGlyph`/`NextCodepoint`の生成処理を復旧する。
- 一回限りのデバッガ実験F-361と`DOCS/skip_isabelle.md`は変更せず、3gx統合と分離する。

既存検査は破損状態でも通っていたため、再発防止として
`PATCHES/verify_restore_pre_shizue.py`を追加した。コメントを除いた実コードを読み、
診断フラグ、入力遮断の有効な呼び出し、しずえソースのwildcard混入、保存版SHA、
ビルド後の時刻とリンク一覧を検査する。修正前は5件でNG、修正後はPASS。

最初の復元後にSimulator 48件を追加実行すると12件失敗し、F-366の項目とフォントが
生成元に残っていることを検出した。これも戻して再生成した後は48/48件PASS。
さらに`verify_keyboard_port.py`でC++対Simulator 10,943状態遷移、タッチ境界、
15描画場面を全て照合し、ARM構文検査もPASSした。

最終ビルド前に同検査、`verify_plugin_port_v2.py`、`verify_spec_v3.py`、
`audit_node_cave.py`を実行し全て異常0件。その後msys2ログインシェルから
`make clean && make -j1`を行い、`linking gohan.elf`と`creating gohan.3gx`を確認した。
成果物検査もPASS。新しい`gohan.3gx`は843,892 bytes、
SHA-256 `f846109264f02e3052fdd927e5c773447b3302e211a54ea0896b317accac2f97`。

破損状態は`BACKUP/plugin_broken_shizue_20260909`、復元済み一式は
`BACKUP/plugin_restored_pre_shizue_20260909`へmanifest付きで保存し、双方の全エントリを
再計算して不一致0件。新しい3gxはまだ実機へ配置していないため、表示・入力・OFF復帰を
確認するまではSWKBD文節調査を再開しない。
