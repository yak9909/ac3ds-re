# 内蔵漢字変換エンジンの現在地

2026-09-12: 明示依頼により、[gohanのチャット漢字候補表示](chat_kanji.md)を実装・ビルド・PC検証。統合版の実機表示は未確認。以下の「組込みを目的にしない」はF407調査時点の範囲。辞書/元コードをSD・3gxへ同梱しない制約は継続。

**F407で実機成功済み（HIGH）**。検証用3gxの独立スレッドから、内蔵タイトルの辞書とSWKBDコードをRAMへ読み、展開・再配置・独立contextを作って変換する。画面/キーボード起動/APTを使わず、辞書・元codeをSD/3gxへ資源として同梱しない。自前メニューや通常gohanへの組込みを目的にしない。

| 入力 | 実機候補数 | 確認 |
|---|---:|---|
| かんじ | 17 | 原本PCと全順位一致、保存済み実機SWKBD候補列とも一致 |
| わたしはねこがすきです | 6 | 同上。明示的な文節境界編集APIの確認とは別 |
| か | 143 | 初回50からgetterが追加検索。原本PCと全順位一致 |

`src/SwkbdEngineProbe/swkbd_engine_probe.3gx`: 289985 bytes、SHA-256 `50ec21a1bde6d52f13fa916ac23aceb2f81dbb833a5ca4db8ca77c3b96368385`。
独立context、5 MiB arena、315再配置、64 KiB stack。Open/Read/Close/Release/Freeとstack guardを確認。各5000ms走行後に観測したもので変換時間の測定値ではない。
バックアップ: 旧 `reference/old_project/BACKUP/plugin_f407_hardware_confirmed/`。証拠: 旧 `reference/old_project/SYSTEM_KEYBOARD/evidence/f407_engine/` の `hardware_*.json` とreport原本。

今後の残件は個人学習/ユーザー辞書、長文上限、明示的な文節境界指定APIの実機試験、並行呼出し、ロード/変換の時間内訳。成功した3入力を全入力の保証にしない。

実機を再び扱うときは、参照専用 `reference/old_project/SYSTEM_KEYBOARD/engine_probe_live_f407.py` のinspectを現行toolsへ移して検証したうえでbootと3gx header・全アンカーを確認する。mailboxのruntime addressを過去のメモから無条件流用しない。実機の現在状態は必ず取り直す。
**F405ではplugin heapに対する範囲cache SVC `0x91/0x93` 系の試験でkernel crash。F406では全体cache SVC `0x92/0x94` を検証して成功。** どちらの範囲SVCが直接原因かなど未確定事項を断定しない。古い「I-cacheは問題にならなかった」という一般論でこの実測を消さない。

詳しい設計と再現手順: [DOCS/system_keyboard_native_loader.md](../../reference/old_project/DOCS/system_keyboard_native_loader.md)、[Plugin/SwkbdEngineProbe/README.md](../../reference/old_project/Plugin/SwkbdEngineProbe/README.md)。巨大な旧handoffは必要なF番号だけ検索する。
