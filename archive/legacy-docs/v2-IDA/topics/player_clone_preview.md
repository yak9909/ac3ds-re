# プレイヤーの複製プレビュー / IDA-opus-5.5-D003

2026-09-24、IDA / opus-5.5。利用者の依頼: 自分のプレイヤーのモデルを複製し、画面上の固定位置（ワールド座標ではない）に
カメラや環境光の影響なしで描く。複製は服・帽子・アクセをそのままに、髪型・髪色だけを変える。将来は複製の向きを自由に（正面・後ろ・回転）。
用途・組み込み先のメニューは前提にしない。

## 1. 確定したこと（IDA-opus-5.5-F028）

### モデルの持ち方

- `AcPlayer + 436` が `PlayerModel`（RTTI `11PlayerModel`、vtbl `0x008E5F74`、大きさ 624 B）。基底は `HumanModel`（vtbl `0x008E5480`）。
- 見た目: `pm+548` 髪型 / `pm+552` 髪色 / `pm+556` 目の色 / `pm+512` 服 8 枠 + 1 B（`PlayerAppearance_Set 0x3298E8`、`PlayerRender_SetOutfitBlock 0x1D37E0`）。
- 部品はバンクの枠に載る。`pm+324..+444` が `{BankTable*, 枠番号}` の組 15 個。管理役 = `*(0x94A374) + 24`（`HumanBankMgr_Get 0x1C489C`）。

| 管理役からの位置 | RTTI | 枠の大きさ | 組の位置（pm+） |
|---|---|---|---|
| 0 | `BankTable<Bank<11059,1,…>>`（体） | 20 | 324 |
| 156 | `BankTable<PlayerFaceBank,14>` | 284 | 332 / 340 |
| 4148 | `BankTable<PlayerHeadBank,7>`（髪） | 1304 | 348 |
| 13292 | `BankTable<PlayerBottomsBank,7>` | 1196 | 364 |
| 21680 | `BankTable<PlayerTopsBank,7>` | 1236 | 356 |
| 30348 | `BankTable<PlayerLegsBank,7>` | 1236 | 372 |
| 39016 | `BankTable<PlayerShoesBank,7>` | 1192 | 380 |
| 47376 | `BankTable<PlayerAcceBank,7>` | 640 | 388 |
| 51872 | `BankTable<PlayerCapBank,7>` | 1248 | 396 |
| 60624 | `BankTable<ToolBank,7>` | 2216 | 404 |
| 76152 / 76448 | `BankTable<HumanResTextureAnimBank,14>` | 20 | 412/420 と 428/436 |

- 実機（2026-09-24、村）: 7 枠テンプレートの部品バンクは**枠 4 個が確保済み**で、自分は全バンク枠 1、使用中ビット `0x02`。枠 0/2/3 は空き。
  `work/evidence/models3d/player_model.json`（`tools/models3d/probe_player_model.py`）。

### 作る・片付ける（ゲーム自身の関数）

- `PlayerModel_ctor 0x1D3854(mem)` → 毎フレーム `PlayerModel_CreateFromProfile 0x1CF090(pm, profile, a3, maskbit, a5, a6)` を
  1 が返るまで呼ぶ（内部は `PlayerModel_CreateStep 0x1CF0D8`）。人形 `AcNpcDemoDollPlayer` は `(pm, profile, 0, (profile+22286>>6)&1, 0, 4)`。
- 初回に `PlayerModel_Setup 0x1CF474` が全バンクから `BankTable_Acquire 0x2137CC` で**空き枠を自動で取る**。
  実機 BP（`0x822C28`、家に入ったとき）で `PlayerModel_Setup` → `BankTable_Acquire` → 使用中ビット、の経路を確認（`work/evidence/models3d/bp_stack.json`）。
- 片付け: `PlayerModel_DestroyStep 0x1D30D0` を 1 が返るまで呼ぶ（`BankTable_Release 0x2138FC`。部品の片付けが済むまで 0）。デストラクタ `0x1D3980` は枠を返さない。
- 姿勢: `PlayerModel_SetMatrix 0x1CEC10(pm, mtx3x4)`（vtbl[9]）が体（pm+120）と服 4 部品のノードに同じ行列を入れる。**回転の要望はここで満たせる見込み。**

### 髪型だけ変える方法（IDA-opus-5.5-F029 で訂正）

- 毎フレームの部品更新 `PlayerModel_UpdateParts 0x1D0AEC`（Vapecord の旧ラベル `vc_UPDATETANOFFSET`）が、各バンクの枠が持つ部品と
  モデルの望む値（服 = `pm+512`、頭 = `PlayerHeadKey_Build 0x329994` が `pm+548` から作るキー）を比べ、違えば入れ替え式で読み直す。
- 頭のファイルは `PlayerHeadBank_BuildPath 0x271DD0` が `Player/head_mdl/{boy|girl}{髪型%17:02}{a|b}.bcres`（髪型 17 以上で girl、帽子の種類で a/b・msd・bald）。
- よって**複製は人形と同じく本物のプロフィールから作り、複製の `pm+548`（髪型）・`pm+552`（髪色）だけを書き換えれば、次の部品更新で髪が替わる。**
  プロフィールを写す必要は無い（F028 の「写しを渡す」は不要。見た目のレコードのポインタは顔・日焼け等の読み込みに使われる）。
- 性別・目の形を変えるときは、作成時の引数（性別 = `!(profile+21946 & 1)`）と顔のバンクの読み込み（`sub_2711AC`、見た目のレコード）が関わるので、
  その段階でプロフィールの写しを検討する。

### 毎フレームの更新（本物のプレイヤー `AcPlayer_UpdateModel 0x653AD4`）

`sub_1D2BE8(pm)` → `PlayerModel_CalcAnim 0x1CE8D8(pm, 1, 1)` → `PlayerModel` vtbl[4] `0x1D33FC`（姿勢・部品の取り付け）。
部品更新 `PlayerModel_UpdateParts` は vtbl[5] `0x1D2CCC` の先頭などから呼ばれる。描画（scene）への登録経路は未確認。

## 2. 設計（段階）

1. **複製を作る（ワールドに置いて確認）**: ゲームのスレッドのフックから、本物のプロフィールで `PlayerModel` を作り（F029）、複製の `pm+548`/`+552` だけ書き換え、
   `PlayerModel_SetMatrix` でプレイヤーの横に置く。髪型だけ違い、服・帽子・アクセが同じことを画像で確かめる。
   毎フレームの更新（アニメ・部品の取り付け）は vtbl[3] `0x1AC7D8` / vtbl[4] `0x1D33FC` / vtbl[5] `0x1D2CCC` の呼び方を人形・AcPlayer から写す（未確定）。
2. **画面固定**（IDA-opus-5.5-F031、gohan 246865a、実機未確認）: 再生直後の NOP `0x4EF1B0` の late pass で専用カメラを結び、
   複製の体と部品の全メッシュを `Scene_DrawLayers` と同じ判定で描く。Scene 0 には積まず、部品は管理役の部品の表から抜き取る。
   projection の z の行に 0.01 を掛けて世界より手前に出す。Scene 1 に積む案は記録の格納先が共有で右目が壊れるので不可。
   ★F032 で訂正: 画面固定でも Scene 0 へは積む（部品のスキニング行列は Scene の更新が計算する）。(0, -5000, 0) に置いて世界では見えなくする。
3. **環境光の影響をなくす**（IDA-opus-5.5-F033、実機未確認）: ライトは BsLightMgr の組 `dword_98529C[4]`（方向光・アンビエント・半球）。
   向きはゲームのカメラ（描画の文脈 +164）の view で送られるので、専用カメラの法線と食い違う。late pass の間だけ組の表（文脈 +64+144 の 4 本）を
   自前の組（今のライトの写し。色と向きだけ変える）へ差し替え、`sub_49AE18`（ライトの状態の初期化）→ 描く → 戻す → 再び初期化。
   Render_DrawSceneIndexed は頭で毎回同じ初期化をするので、世界の記録・再生には漏れない。
4. **向き**: `PlayerModel_SetMatrix` の回転で正面・後ろ・任意角。
5. **後片付け**: `PlayerModel_DestroyStep` → 領域を返す。場面の切り替えで先に片付ける。

## 3. 未確定・注意

- 更新・描画登録の呼び方（どの vtbl をどの順で毎フレーム呼ぶか、ModelInstance_Create の登録引数）。人形の更新経路を読む。
- 空き枠の数: オンラインで 4 人いると空きが無い。村に人形が出る場面（イベント）とも取り合う。取れなければ作らない。
- 帽子は髪のモデルの形を変える（頭のバンクの読み込みキーに帽子の Item が入る。`0x271800`）ので、帽子と髪の組み合わせはゲームの規則どおりになる。
- Mii マスクをかぶっていると頭は読み込まない（`Item_IsMiiMask`）。
