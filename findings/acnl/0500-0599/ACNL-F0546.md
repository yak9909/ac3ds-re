---
id: ACNL-F0546
aliases:
- IDA-opus-5-F004
title: 任意bcresの読み込み→ワールド描画が実機で成立（2026-09-20、HIGH、実機）
summary: '解析ソフト: IDA / 解析モデル: opus-5。**ゲームが読んでいないファイルを自分で読み、画面に出した。**'
date: '2026-09-20'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 3242272
- 3242328
- 4874016
- 5178508
- 5426648
- 5166640
- 9420032
- 4872820
tags:
- model
supersedes: []
source: IDA:work/FINDINGS.md:4017-4051
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-opus-5-F004: 任意bcresの読み込み→ワールド描画が実機で成立（2026-09-20、HIGH、実機）

解析ソフト: IDA / 解析モデル: opus-5。**ゲームが読んでいないファイルを自分で読み、画面に出した。**
`Other/book.bcres`（update romfs、7,040 B、モデル `book`）を自前ヒープへ `G3dResHolder_RequestLoad 0x00317920`
→ `Setup 0x00317958` → `FindModelByName 0x004A5F20` で取り、`ModelInstance_Create 0x004F048C` を
**木と同じ `(0, 0, 1)`** で呼び、`FieldPosition_ToRenderSpace 0x0052CDD8` で姿勢を作って
`0x004ED630(holder, 0)` へ毎フレーム提出した。上画面に本が現れたことを利用者が確認し、
Chokistream の画像を受領した（`book_visible_top.png` / `book_visible_zoom3x.png`。
拡大すると小口の平行線と右端のページが見え、ベンチではなく横倒しの本と同定できる）。

決め手になった数値:

- **GPU アドレス変換が自前資源でも成立**。メッシュの属性コマンド列で `0x0200`=`0x3000000`、
  `0x0203`=`0x08FA9CA8` → PA `0x20FA9CA8` → VA `0x30FA9CA8` ＝**自前 bcres のファイル内 offset 4008**。
  IDA-unknown-F027 が「対応外領域では黙って 0 になる」と示した箇所が、自分で確保したヒープでも通った。
- **曲面変換が実機とオフラインで一致**。実機の角度 `0x5E2E`=24110、`verify_arbitrary.py` の事前予測も
  **24110**。座標は (2184.291748, -329.921021, 360.801270) と予測 (…, -329.935760, 360.817200) で
  差 0.015 以内（ゲームの sin/cos 表と Python の三角関数の差）。**IDA-opus-5-F002 は HIGH へ。**
- 1,500 ms の走行で**ケーブ実行 49 回・提出 49 回**（2 本の計器で「走った」と「提出した」を分離）。
- `0x4F048C` 後: node `0x30FE8CF8`、vtable `0x008FBD00`=`nw::gfx::Model`、activator 非 0。
- `G3dResHolder_Setup` は `holder+12` に `0x80000006` を残す。これは各オブジェクト結果の **OR**
  （`sub_4A5A74 0x004A5A74` が `v6 |= …`）で、Setup 自身が bit1 を見て 2 回目を回す値。失敗コードではない。
  ゲーム自身の Season ホルダ `0x33109070` は同欄が 0 だが、描画は成立した。呼び出し元
  `ScStage_LoadIndoorRes` は Setup の戻り値を使っていない。

根拠: `work/evidence/models3d/arbitrary_20260920/`（`plan.md`・`preflight.json` 75項目PASS・
`arb_hook_audit.json` 8ケースPASS・`arb_state.boot1.json`・`result.json`・画像2枚・`events.jsonl`）。
手順 `tools/models3d/arbitrary_model.py`、検証 `tools/models3d/verify_arbitrary.py`、
ケーブ生成 `tools/models3d/build_arbitrary_hook.py`、事前調査 `tools/models3d/model_preflight.py`。

**未確認（重要）**: **OFF の画像を撮っていない。** 利用者が Chokistream 起動のため ACNL を再起動したので、
`enable=0` で消えることの画像証拠が無い。次回はこれを最初に撮る。資源・instance・ヒープの解放は未設計
（再起動で消えただけ）。SkeletalModel（`0x40000092`、379個）は未試験。配置・尺・部屋は各 1 通り。
反証条件: 同じ座標に何も置かずに同じ物体が見える、`enable=0` でも残る、別の部屋/尺で再現しない。

