<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / time

| ID | 題 | summary | 確度 | 格付け |
|---|---|---|---|---|
| ACNL-F0098 | F-60: Vapecord の時間設定チートと、ゲーム自身の時計確定経路 | confidence: **HIGH**（静的解析。Vapecord のソースと逆コンパイルが独立に一致） | HIGH | ? |
| ACNL-F0570 | 店の営業時間判定は店・用途ごとに複製、共通の入口なし（2026-09-17、MEDIUM） | 時刻はDate_GetRaw 0x2FB3A4（&0xACF6B0を返すだけ、466 caller）の[1]>>24、条例はsub_7585A0（[garden+0x621CF] bit1）/sub_7585C4。判定はShopHours_*（IDB命名済み）に複製され、多くはCRO（ModuleDowntown/Outdoor/Indoor/Shop/NpcDt/Club）から匿名インポートで直接呼ばれる。ShopsAlwaysOpenの9語は9関数の「0を返す出口」で関数 | MEDIUM | ? |
