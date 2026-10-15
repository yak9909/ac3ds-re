---
id: ACNL-F0205
aliases:
- F-179
title: 'F-179: Vapecord のマップ上プレイヤー表示は OSD（フレームバッファ直描き）だった — `HIGH`（ソース確認）'
summary: '出典: `REFERENCES/CTRPF PROJECTS/Vapecord-ACNL-Plugin-master/src/features/PlayerCodes/PlayerCodes.cpp`'
date: '2026-08-30'
category: _product
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses:
- 2233776
tags:
- player
- map
supersedes: []
source: v1:RE/FINDINGS.md:10941-11007
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-179: Vapecord のマップ上プレイヤー表示は OSD（フレームバッファ直描き）だった — `HIGH`（ソース確認）

出典: `REFERENCES/CTRPF PROJECTS/Vapecord-ACNL-Plugin-master/src/features/PlayerCodes/PlayerCodes.cpp`
（`REFERENCES/` は一次情報ではない。ソースを読んだ事実として記録する）

### 1. 実装

```cpp
bool players(const Screen &screen) {
    if(screen.IsTop || !Game::IsMapOpened()) return 0;   // 下画面のマップ表示中のみ
    for(int i = 0; i < 4; ++i) {
        if(PlayerClass::GetInstance(i)->IsLoaded()) {
            PlayerClass::GetInstance(i)->CalculateMapCoordinates(XPos, YPos);
            if(playerIcon[i] != nullptr) {
                ... screen.DrawPixel(X, Y, cPix);   // 自前ビットマップを 1 px ずつ
            } else {
                screen.DrawRect(XPos-1, YPos+1, 6, 6, Player::GetColor(i));
            }
        }
    }
}
...
OSD::Run(players);
```

### 2. ★「ゲームのアイコンを複製して色を変える」ではない

**ゲームの Picture も GPU パイプラインも一切使っていない。**

- **CTRPF の `OSD::Run` でフレームバッファに直接描いている**
- アイコンは**ファイルから読み込んだ自前ビットマップ**（`playerIcon[i]`）。
  読み込めなければ **6x6 の単色矩形**（`screen.DrawRect`）で代替する
- 座標は `CalculateMapCoordinates` が
  `x = -33.0 + coords[0]/14.2f` のような**画面ピクセル空間への手計算**で求め、
  マップ枠に収まるようクランプする（`if(x < 12) x = 12;` など）
- ゲーム側へのフック `0x2215B0` → `SetPlayerIconCoordinates` は
  自機アイコンの座標更新に関わるもので、**描画そのものではない**

### 3. 含意

**実在の ACNL プラグインは、オーバーレイをゲームの GPU 経路ではなく OSD で描いている。**

| | OSD | Picture 経路への相乗り（本解析） |
|---|---|---|
| 常時性 | **100%**（ロード中も動く） | Pane 層なら 100%（F-177） |
| 見た目 | CPU 描画。ゲームのフォント・拡大縮小・ブレンドは使えない | **ゲームと同じ GPU 描画** |
| 実装コスト | **低**。解析不要 | 高い（F-163〜F-178 の積み重ねが必要） |
| 座標 | 画面ピクセルを手計算 | ゲームのレイアウト空間をそのまま使える |

### 4. ★OSD には実用上の欠点がある（ユーザーからの情報、2026-08-30）

**本プロジェクトが OSD を採らない理由は明確である。**

- **描画がチカチカして乱れる**（フレームバッファへ直接書くため、
  ゲームの描画・転送とタイミングが噛み合わない）
- **アルファブレンドが使えない**

したがって「OSD で済むのでは」という結論に安易に流れないこと。
**GPU 経路（Picture 相乗り）を追う目的は見た目の統一だけでなく、
表示品質そのものにある。**

**用途で選ぶべきもので、優劣ではない。**
ただし本プロジェクトの目標（自前 GUI）に対しては、
上記の理由から **Picture 経路が本命**である。

---

