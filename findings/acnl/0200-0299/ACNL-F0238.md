---
id: ACNL-F0238
aliases:
- F-213
title: 'F-213: ★★★★CTRPF プラグインへの移植 — ケーブは書き直さずバイト列ごと移す — `HIGH`（ビルド済み・実機未検証）'
summary: '`Plugin/CTRPluginFramework-BlankTemplate-0.8.0/Sources/OwnGui.cpp`。'
date: '2026-09-01'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:12823-12915
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-213: ★★★★CTRPF プラグインへの移植 — ケーブは書き直さずバイト列ごと移す — `HIGH`（ビルド済み・実機未検証）

`Plugin/CTRPluginFramework-BlankTemplate-0.8.0/Sources/OwnGui.cpp`。

### 方針

描画本体は 225 ワードの ARM コードケーブで**実機で検証済み**。
C++ へ書き直すと「同じ挙動を再現できたか」を再検証する羽目になる。
そこで `cave_draw_topmost.py` に `MODE = "export"` を足し、
ワード列をそのまま C++ ヘッダ（`includes/GuiCaves.h`）へ吐かせて**書き込むだけ**にした。

**★書き出したバイト列が実機のものと一致することを機械的に確認した。**
ケーブ 9 個・フック 8 個・スプライト表 280 ワードすべてで**不一致 0**。
「移植したつもり」で別物になっていないことの裏付け。

### 実行時に決まるもの

| もの | 扱い |
|---|---|
| テクスチャの物理アドレス | 描画ケーブ内の 1 ワード（索引 205）を `((VA - 0x10000000) >> 3)` で差し替える |
| GPU 可視バッファ | `Render_FrameEnd` に一時フックを仕掛け、**ゲームのスレッド上で**ゲームのアロケータを呼ぶ（F-164 / F-165）。確保できたらフックを外す |
| フォントアトラス | SD の `/luma/plugins/00086200/font_atlas.bin`（64x64 LA4, 4096 バイト）があれば優先、無ければ埋め込み |

アトラスは実機のバッファから吸い出して `PATCHES/font_atlas_64x64_la4.bin` に保存し、
`includes/GuiFontAtlas.h` へ埋め込んだ（非ゼロ 204 バイト = グリフ 140 + 無地マス 64）。

### 順序

```
確保 -> アトラス転送 + svcFlushDataCacheRange
     -> ケーブとスプライト表を書く
     -> svcInvalidateEntireInstructionCache
     -> フックを有効化
```

**★逆順にしない。** 書き込む前のケーブへ飛ぶ瞬間ができる。
OFF はこの逆順。**バッファは解放しない**（Free はゲームのスレッドからでないと呼べない）。

### ★★実機で 1 回クラッシュ — `svcFlushDataCacheRange` は使えない

```
PC   FFF0324C   （カーネル内）
LR   FFF1DDF8
R0   329D8500   確保したバッファの先頭
R1   329D9500   その +0x1000（範囲の末尾）
FAR  329D8500   Access type: Write
```

カーネルのキャッシュ操作ループが**範囲の最初の番地で書き込みフォルト**した。
Luma 独自 SVC の `svcFlushDataCacheRange` を使ったのが原因。

**`DOCS/ctrpf_plugin.md` が最初からこう書いていた:**

> `GSPGPU_FlushDataCache` の失敗は別問題で回避できる。代替:
> `svcFlushProcessDataCache(CUR_PROCESS_HANDLE, addr, size);   // サービス不要`

**自分で書いた文書の指示を読み飛ばして別の関数を使ったのが誤り。**
標準 SVC の `svcFlushProcessDataCache` に変更して解決（実機再検証はこれから）。

なお `svcInvalidateEntireInstructionCache()`（範囲を取らない方）は問題なく通っている。
クラッシュ時点でバッファの確保まで完了していた（R0 に払い出しが入っている）ので、
**ゲームのアロケータをプラグインから呼ぶ部分は実機で動いたことが確定した。**

### ★★成果物が更新されない罠（一番危なかった）

**ソースを直しても `.3gx` の中身が変わらない。** `make` は `.o` を作り直し
`creating ....3gx` まで表示するので、成功したように見える。

テンプレートの Makefile が `$(OUTPUT).3gx : $(OFILES)` と書いており、
**`.elf` が `.o` に依存していなかった**。
devkitARM の `%.elf:` ルールは前提条件を持たないため、
`.elf` が一度できると二度とリンクされない。

```make
$(OUTPUT).3gx : $(OUTPUT).elf    # ★.3gx を先に書く（最初のルールが既定ターゲット）
$(OUTPUT).elf : $(OFILES)
```

**ビルドの成功は「make がエラーを出さなかったこと」では確認できない。**
`.elf` の日付と、成果物に新しい文字列が入っているかで確かめる。

### ★踏んだ落とし穴 2 つ

1. **`<cstdarg>` が要る**（`DOCS/ctrpf_plugin.md` に書いてあったのに踏んだ）
2. **3DS の `u32` は `unsigned long`。** ヘッダを `unsigned int` で吐くと型が合わない
3. **`MOV R1,#0x4000` を `0xE3A01A01` と書いて `0x1000` になっていた。**
   ARM の即値は「8bit を偶数ビットだけ右ローテート」。`0x4000 = 0x01 ror 18` なので
   rot は 9 で `0xE3A01901`。**メモリへ置いて逆アセンブルして気付いた。**
   ケーブは走らせる前に必ず実機メモリ上で逆アセンブルすること。


---

