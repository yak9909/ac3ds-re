---
id: ACNL-F0312
aliases:
- F-288
title: F-288 — Chokistream の画面を AI が直接見られる（動的解析の目視確認を自動化）
summary: '**結論: 見られる。** `PATCHES/grab_screen.ps1` で PNG にすれば、そのまま読める。'
date: '2026-09-04'
category: ui
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:18036-18072
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-288 — Chokistream の画面を AI が直接見られる（動的解析の目視確認を自動化）

**結論: 見られる。** `PATCHES/grab_screen.ps1` で PNG にすれば、そのまま読める。

| ウィンドウ | 位置・大きさ | 用途 |
|---|---|---|
| `Chokistream` | `0,0` `492x299` | 設定用 |
| `Chokistream - 3DS (n FPS)` | 可変 `416x519` | **画面側** |

画面側の**クライアント領域は `400x480`**。上画面 `400x240` の下に
下画面 `320x240` が中央寄せ（左右 40px の黒帯）。
`GetClientRect` + `ClientToScreen` で枠を除いて取る。
`-Screen bottom` が `320x240` ちょうどで切り出せることを実機の絵で確認した。

`-Shots n` で連写し、**直前との画素差を %** で出せるので、
F-287 のような「明滅」を客観的に測れる。

### ★実行条件（2 つとも一度落ちた）

1. **`pwsh`(7) では動かない。** `System.Drawing` が既定で参照されず
   `Bitmap`/`Graphics`/`ImageFormat` が `CS1069`/`CS0103` になる。
   **`powershell.exe`(5.1) で実行する。**
2. **`.ps1` は UTF-8 BOM 付きで保存する。** BOM が無いと 5.1 は CP932 として読み、
   日本語コメントが化けてパーサが壊れる。出力も CP932 なので冒頭で
   `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8` を設定する。

### ★誤診しないための注意

**Chokistream は数 FPS しか出ない。連写して同じ絵でも「固まった」とは限らない。**
実測で上画面 3 連写・下画面 2 連写とも差 0% だった。
**固まったかどうかはデバッガ（`LOG+0xE8` 等のカウンタ）で判定すること。**
撮れる絵は「転送が届いた最後のフレーム」であって「いまの 3DS」ではない。

詳細は `scratchpad/MEMO_f288_screen_capture.md`。

---

