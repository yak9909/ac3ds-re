---
id: ACNL-F0443
aliases:
- IDA-opus-5-F010
title: アニメ本体は g3d の自前クラス。nw::gfx::AnimEvaluator を使うと落ちる（2026-09-21、HIGH、実機・自己訂正）
summary: '解析ソフト: IDA / 解析モデル: opus-5。**F009 に「未検証の仮説」と書いた箇所を実機で突いて反証された。**'
date: '2026-09-21'
category: _triage
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 7564928
- 7564920
- 9423988
- 9424028
- 9424168
- 9424236
- 9424328
- 9424616
- 5178112
- 1798688
- 5168252
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:285-341
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F010: アニメ本体は g3d の自前クラス。nw::gfx::AnimEvaluator を使うと落ちる（2026-09-21、HIGH、実機・自己訂正）

解析ソフト: IDA / 解析モデル: opus-5。**F009 に「未検証の仮説」と書いた箇所を実機で突いて反証された。**
素の `nw::gfx::AnimEvaluator`（構築子 `sub_491450`）を作って `sub_4EBC14` へ渡したところ
**SIGSEGV（exc.code b、tid 267）**。fault は `sub_736E78 0x00736E80`:

```
0x736E78  ldr r0, [r0, #0x14]       ; r0 = *(anim + 20)
0x736E80  ldr r0, [r0, r1, lsl #2]  ; ← r0 == 0 で data abort
```

`sub_4EBC14` は `anim+20` を 0 にしてから vtable **slot 6** の build を呼ぶ。
`AnimEvaluator` の slot 6 はマテリアルアニメのメンバ表を作らないので 0 のままで、
直後の `sub_4EDC24` がそれを添字参照した。**build は非0を返しても中身を保証しない。**

### 正しいクラス（RTTI で確定）

ゲームは `nw::gfx` の evaluator を直接使わず、**`g3d` 名前空間の自前クラス**を使う。

| クラス | vtable |
|---|---|
| **`g3d::MaterialAnim`** | **`0x008FCC74`** |
| `g3d::SkeletalAnim` | `0x008FCC9C` |
| `g3d::VisibilityAnim` | `0x008FCD28` |
| `g3d::GroupSkeletalAnim` | `0x008FCD6C` |
| `g3d::GroupTransformAnim` | `0x008FCDC8` |
| `g3d::BaseAnim` | `0x008FCEE8` |

実機でプレイヤーに結線されている evaluator `0x306AE3E8` の vtable は `0x008FCDC8` ＝
**`g3d::GroupTransformAnim`**（基底 `nw::gfx::AnimObject` → `nw::gfx::GfxObject`）。

**`sub_4EBE4C(obj)` が `g3d::MaterialAnim` の構築子**（引数1個）。`+4 = 2`、vtable を
`g3d::BaseAnim` → `g3d::MaterialAnim` の順に置き、**`HeapAllocator_Ctor(obj+12)` を呼ぶ**。
`+8`・`+20`・`+24`・`+28` を 0 に。**オブジェクトは 32 バイト**。
これは `sub_4EBC14` の要求と完全に一致する（`+12` をアロケータとして `Heap_CreateNamed_0`、
`+20` を 0 に、`+24` に instance、`+28` に flag、`0x4F0300` は `*(anim+8)` を結線先へ書く）。
`AnimEvaluator`（116 B、`+12` はアロケータではない）を使ったのが誤りだった。

### 復旧

`finish_call` は PC がトラップでないので復元を拒否した（設計どおり）。`pending_call.json` に
`begin_call` が保存した**実値**（全 CORE レジスタとスタック退避）を書き戻し、トラップ BP を外して
PC を park `0x1B7220` へ戻した。**レジスタは 1 語も違わず一致**し、1500ms 走らせて復帰を確認。
book・UnitCursor・A/B 用の 3 instance、guard、park はすべて無傷。`sub_736E78` は読み取りのみで
ゲーム側のデータには触れていない。fault 記録は `anim_fault.json`。

### 併せて判明

`sub_4EDC74`（フレーム設定）は `0x004EDC7C` が `vmov.f32 s16, s0` で、**引数を VFP s0 で取る**。
現在の呼び出しハーネスは R0–R3 しか設定できないので、**この関数は今のままでは呼べない**。
フレームを進めるなら `AnimFrameController` の欄を直接書くか、ハーネスに VFP 引数を足す必要がある。

根拠: `anim_fault.json`、`events.jsonl` の `anim_ctor` / `anim_build`、
`sub_736E78` / `sub_4EDC24` / `sub_4EDC74` / `sub_4EBE4C` / `sub_491450` の逆アセンブル、
`code.bin` 全域の RTTI 走査。
反証条件: `g3d::MaterialAnim` でも `+20` が 0 のまま、`sub_4EBE4C` が別の引数を要る。

