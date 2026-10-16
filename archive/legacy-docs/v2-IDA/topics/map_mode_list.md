# 建物一覧（BsMenuMapList）とマップエディターのモード一覧

確定知見は `work/FINDINGS.md` の **IDA-opus-5.5-F062**、解析の全記録（表・状態機械・レイアウト・テクスチャの行）は
`work/evidence/map_editor/mode_list/analysis.md`。ここは使うときの要点だけ。

## ゲーム側（主 IDB で命名済み）

| 役目 | 関数 |
|---|---|
| 生成（地図の生成段 4〜6） | `BsMenuMapList_Ctor 0x22500C` → `SetupLayout 0x2247B4(一覧, Layout, 保持体, 0)` → `SetupRows 0x2245AC` → `SetupButtons 0x223D7C` |
| 項目・行 | `AddEntry 0x224700(一覧, 番号, id, 種類, アイコン)` / `UpdatePageButtons 0x224334` / `SetRow 0x224B88(一覧, 行, 項目, 語, 表示)` |
| 開いたまま（部屋 164） | `OpenFixed 0x224E4C` |
| 選択 | `SetSelected 0x2241E8(一覧, 行, on)`、`SelectById 0x22392C(一覧, 種類, id)`、行の決定は `BsMenuMapVillage_StepListTouch 0x2B3114` の 0x2B34DC〜 |
| アニメ | `BindAnim 0x224F18(一覧, i, フレーム s0)` / `UnbindAnim 0x223C74` / `ApplyAnimFrame 0x224F78`（i: 0 in / 3 in_list / 4 out_list / 5 out） |
| 片付け | `Release 0x224DE8` → `Dtor 0x225210` |
| 行のボタン | 行 BAC = 一覧 +8736、ノード = +8964 + 224i。`ButtonActionControl_Update 0x2F7744` / `IsDecided 0x722C34` / `GetDecidedIndex 0x72294C` / `ClearDecided 0x2F72C4` |
| タッチ | 構造体 0xACF6E0（`Touch_UpdateState 0x1B7874`）。+0 押している / +26 前のフレームの +0 / +10,+12 位置 |

## 見た目の変え方（gohan `Sources/Cheats/MapModeList.cpp`）

- 窓 `W_list_win_00` は子の親なので動かさない。基準点（+0xB6 下位ニブル）を下 = 7、高さ 90.5 → 上端を保ったまま 90.5 詰まる。
- 紙 `P_list_note_00` は 1 枚絵なので 2 枚に分ける（下の段は矢印の Picture のマテリアルを差し替え、`nwlyt_Pane_InsertChild 0x4B6100` で `N_slct_00` の直前へ。壊す前に戻す）。
- 数値の見本: `node tools/layout/mode_list_preview.mjs`（盤面の参考画像に重ねた PNG と、タッチの矩形 `mode_list_rect.json`）。検査は `tools/strc/verify_map_editor.py` 群 13。
