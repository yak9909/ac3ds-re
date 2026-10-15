<!-- 生成物。編集しない（kb.py index が作り直す） -->

# hhd / render

| ID | 題 | summary | 確度 | 格付け | consolidated_into | 訂正 |
|---|---|---|---|---|---|---|
| HHD-F0001 | 慣性と、選択枠・ボタンの縞の合成（2026-10-05、MEDIUM〜HIGH: 静的 + HHD のスクショ 2 枚で合成の意味を照合） | 解析モデル opus-5.5。IDB: `DragArea_SlideDecay 0x3E86AC` に注記。 | MEDIUM | S |  |  |
| HHD-F0003 | 髪・目の形の番号 → モデルのファイル（2026-10-05、MEDIUM: 静的のみ。ACNL のファイル名と照合） | `PlayerHead_BuildPath 0x1DFA44`（命名）: 髪の番号 k → `Player/head_mdl/{boy\|girl}%02d{a\|b}.bch`。k >= 16 なら girl、番号 = k & 15（帽子の種類で a / b / bald / bald_ear）。 | MEDIUM | S |  |  |
