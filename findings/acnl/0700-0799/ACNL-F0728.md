---
id: ACNL-F0728
aliases: []
title: "画像キャッシュは ArcResourceAccessor 単位で、破棄時に参照が無効になる"
summary: "ArcResourceAccessor は名前でTextureInfoをキャッシュし、hitなら画素もentryも追加確保しない。missはロードと156 B entry確保を伴い、accessor/arc破棄に伴って借用画像の参照が失効する。"
date: 2026-10-21
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: "全関数export・RomFS・公開ソース"
addresses: [0x004B5844, 0x004B4C10, 0x004B4B68, 0x005676C8, 0x0056795C, 0x004B4CF4, 0x00568CFC]
tags: ["layout", "heap"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6.1-sol
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

ゲームにはアクセサごとの画像共有表がある。同じアクセサ内の同名テクスチャはTextureInfoを使い回す。表示中の画像への参照は画素コピーを要しないが、資源の所有や寿命は移らない。
確度 MEDIUM：GetTextureのhit/miss、独立した検索・挿入・破棄と、FCRAM/VRAM別ロードを照合。今回の実機での借用試験なし。

## 根拠

一次証拠は `_local/evidence/107/0x004b5844.txt`、`0x004b4c10.txt`、`0x004b4b68.txt`、`0x005676c8.txt`、`0x0056795c.txt`、`0x004b4cf4.txt`、`0x00567244.txt`、`0x00567310.txt`、`0x00568cfc.txt`。元exportは `exports.json`。

- `GetTexture`（0x4B5844）はaccessor+0x30の表を検索。`0x4B4C10` は名前を比較しentry内のTextureInfo 5語をコピーするだけで、確保を呼ばない。
- missならaccessor vslot+0x14で画像をロードし、成功時に `0x4B4B68` が156 Bの名前+TextureInfo entryをAllocMemoryから作って表へ挿入する。従ってGetTextureを呼ぶだけで無確保だとはいえない。
- これは各accessorのリストであり、全アーカイブ共通の内容hashによる画像重複排除ではない。`0x568CFC` は所属arcのtimgを列挙してGetTextureを呼ぶ。
- `0x567244` はarc読込結果をholder+8に保存して内包accessorへAttach。Attach（0x4B5900）は単一arcの基底とprefixを設定する。
- `0x5676C8` はFCRAM指定（masked type0x10000）の場合に元BCLIM画素の変換アドレスを返す。VRAMなら画素を別確保・転送し、そのCPU側返却アドレスをTexBufListへ記録する。
- `0x56795C` はVRAM画素をcallbackでfreeし、リストノードを消し、`0x4B4CF4` でcache entry群を破棄する。`0x567310` はloader資源とaccessorを破棄する。場面のroot/holderが消えれば浅いTextureInfoの写しは寿命を延ばさない。
- `arcs.json` では `ltr_win.arc` と `cmn_btn.arc` 内の `my_cbn_btn.bclim` が同じSHA256/4,096 B画素でも別arcにある。内容が同じことと、実行時にグローバル共有されることは別である。

公開資料 `STUDY107_PUBLICS` の [Clypo](https://github.com/pleonex/Clypo) と [3dbrew CLYT](https://www.3dbrew.org/wiki/CLYT_format) はレイアウトからテクスチャ名を参照する形式を説明する。実行時のcache/所有は上記のゲーム命令から確認した。

## 反証条件・未確認点

- タイトル画像がプレイ中の手紙場面にも居ること、共通ボタンが全遷移で居続けることは未確認。未読込のGetTextureで参照を得る行為は新規ロードになり得る。
- 資源の参照数を外部へ貸すためのAcquire/Releaseや、自動pinをこの経路では確認していない。解放・再確保後の同じポインタを同じ所有物とみなせない。
- 別accessor型やゲームの3D ResourceBankに共有機構がないという網羅的否定ではない。ここで確認したのはnw::lytのarc画像表。
