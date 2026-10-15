---
id: ACNL-F0347
aliases:
- F-320
title: 'F-320（2026-09-06）: クラッシュダンプの読み方と `threadCreate` の落とし穴'
summary: '**confidence: HIGH**（ダンプの実値 + `gohan.elf` の逆アセンブル）'
date: '2026-09-06'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:21208-21272
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
corrected_by: ["ACNL-F0006"]
---
## F-320（2026-09-06）: クラッシュダンプの読み方と `threadCreate` の落とし穴

**confidence: HIGH**（ダンプの実値 + `gohan.elf` の逆アセンブル）

### きっかけ

F-319 を実機に入れた直後にクラッシュダンプが出た。
**結論から言うと描画は無関係で、
「plugin ready の直後にチートを ON にした」ことによるもの**
（利用者が原因を特定。時間をおいて ON にすれば普通に描画される）。
ただし追跡の過程で確実な知見が 2 つ取れたので残す。

### 1. Luma3DS のクラッシュダンプは表題 0x28 バイトで全部読める

```
+0x00 magic 0xDEADC0DE/0xDEADCAFE   +0x08 版
+0x0C プロセッサ(u16)・+0x0E コア(u16)      +0x10 例外種別 3 = データ中断（F-406訂正）
+0x14 総サイズ  +0x18 レジスタ  +0x1C コード  +0x20 スタック  +0x24 付加
```

レジスタは 23 語（`R0..R12,SP,LR,PC,CPSR,DFSR,IFSR,FAR,FPEXC,FPINST,FPINST2`）。
**コード部は最後の語が `PC` の命令。** 付加データはプロセス名と TitleID。
スタックからプラグイン `.text` を指す語を拾って `addr2line` にかければ
呼び出しの連なりが出る（★古い戻り番地の残骸が混ざるので SP に近い順に読む）。
詳しい手順は `DOCS/crash_recovery.md` に書いた。

### 2. ★`threadCreate()` は libctru が初期化したスレッドからしか呼べない

今回のダンプの実値:

```
例外 3（データ中断）  DFSR=5（未マップ）  FAR=0x00000004  R3=0
PC=0x070058A0  __createThread + …
  mrc p15,0,r3,c13,c0,3   ; r3 = TLS
  ldr r3,[r3,#8]          ; r3 = reent   ★magic を確かめない
  ldr r2,[r3,#4]          ; ← ここで落ちた
呼び出し PluginMenuExecuteLoop::operator() -> MenuEntryImpl::_Execute()
         -> GuiMenu::Initialize() -> threadCreate() -> __createThread
```

TLS の並びは `initThreadVars`（`0x0701E85C`）から確定できる。

```
+0x00 magic 0x21545624   +0x04 Thread   +0x08 reent   +0x0C tls_tp
```

`__getreent`(`0x0706D494`) と `__getThreadLocalStorage`(`0x0701E7A0`) は
**magic を照合して、違えば `__ctrpf_getThreadVars`(`0x0703B16C`) へ回る**。
`__createThread` だけがそれをしない。したがって
**libctru が初期化していないスレッド（CTRPF の `ThreadEx` など）から
`threadCreate()` を呼ぶのは未定義**で、TLS の中身しだいで落ちる。

`GuiMenu::Initialize()` はメニュー項目のコールバックから `threadCreate()` を呼ぶので、
この経路に該当する。**運用では plugin ready のあと一呼吸おけば回避できる**が、
恒久対策（自前スレッドをやめる／magic を確かめてから呼ぶ）は TODO に置いた。

### やってしまったこと（記録）

ビルド前に照合器 3 本は通したが、**生成された `gohan.elf` の逆アセンブルは
していなかった**。ケーブ（ゲーム側に書き込む語）は毎回検証しているのに、
**プラグイン自身のコードは見ていない**という穴があった。
今回はそこが原因ではなかったが、穴であることは変わらない。

---

