<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / sound

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| ACNL-F0265 | F-242: `GardenSound.bcsar` を解読し、全 4,266 音の名前・ID・カテゴリを確定 — `HIGH`（独立 3 系統の一致） | `NCCH/romfs v1.5/Sound/GardenSound.bcsar`（33.2 MB, `CSAR`）を静的に解読した。 | HIGH | ? |
| ACNL-F0268 | F-245: ループ波形が音符の途中で切れていた — `HIGH`（実機録音との突き合わせで確定） | `SOUND/render.py`。**利用者が実機から録音した音との比較で発覚した。** | HIGH | ? |
| ACNL-F0271 | F-248: 包絡の換算 3 箇所を実機録音で確定 — `HIGH`（録音との数値照合＋利用者の耳） | 利用者が実機（エミュレータ）から録音した `close.wav` / `open.wav` / `pickup.wav` を | HIGH | ? |
| ACNL-F0272 | F-249: 音量・ベロシティは振幅の 2 乗側 — `HIGH`（実機録音との数値照合 0.3dB 以内） | `SE_ACT_FOOT_ERASE` の実機録音と自前の合成を 20ms 窓で突き合わせたところ、 | HIGH | ? |
| ACNL-F0273 | F-250: 未設定の変数に対する比較が 712 件を無音にしていた — `HIGH`（全件バッチで確認） | 全件バッチ（3,960 件）で 712 件が「ノート 0」になった。`SEQ_BGM_DJ01_HS_SANBIKA` を追うと: | HIGH | ? |
| ACNL-F0479 | 模様替えの音は屋外では鳴らない（GROUP_HOUSE）と、選択窓の決定音が音程を上げる仕組み（2026-09-27、HIGH: 静的＋利用者の実機確認） | 解析ソフト: IDA（主 IDB）＋ BCSAR 索引（reference/old_project/SOUND）/ 解析モデル: opus-5.5。 | HIGH | S |
