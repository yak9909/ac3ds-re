<!-- 生成物。編集しない（kb.py index が作り直す） -->

# acnl / input

| ID | 題 | summary | 確度 | 格付け | consolidated_into | 訂正 |
|---|---|---|---|---|---|---|
| ACNL-F0376 | F-350（2026-09-07）: ★入力の無効化 — `0x32C85A2D` の正体と、全ボタン／タッチを塞ぐ場所 | **confidence: HIGH（静的解析）/ MEDIUM（実機。読み取りのみで未適用）** | HIGH | ? |  |  |
| ACNL-F0378 | F-352（2026-09-07）: ★実機報告 2 件 — タッチのビットを消していた（修正）／ SELECT は未解決 | 利用者の報告: |  | ? |  |  |
| ACNL-F0379 | F-353（2026-09-07）: ★SELECT のビットは `0x800` — libctru の並びと違った（実測で確定） | **confidence: HIGH（実機で実測。基準値も取った）** | HIGH | ? |  |  |
| ACNL-F0380 | F-354（2026-09-07）: ★タッチは 2 か所にある — hold の中のビットも消す（実機確認済み） | **confidence: HIGH（実機で確認。利用者「誤反応が消え、ロック中は完全に無反応、 | HIGH | ? |  |  |
| ACNL-F0381 | F-355（2026-09-07）: ★★ゲームは SELECT を START に読み替えている — 真因と正しい直し方 | **confidence: HIGH（逆アセンブル + 実機で確認。利用者「START が効き、SELECT が効きません。成功です」）** | HIGH | ? |  |  |
| ACNL-F0427 | native scrollの別入力経路とstyle arc一時pool（2026-10-12） | 訂正F005: 7word差込みのうち+0はvtableであり除外、+276/+280は中心座標でなく画素。T005 identity geometry fixtureは二重変換を隠したため、scroll実機成立の証拠としない。最新sourceは6word限定で元変換/hit-testを実行する。 | MEDIUM | ? |  |  |
| ACNL-F0721 | 入力遮断点と旧状態の扱いを再解析：holdだけではreleaseが残る | sead_Controller_Calc+0x30 は生入力更新後・edge計算前だが、current holdだけを消すとreleaseが残る。旧状態R8/R9は本体とWrapperの両方へ渡されるため、遮断対象は両方の旧状態でも除去する。 | MEDIUM | A |  |  |
| ACNL-F0722 | タッチ遮断は画面ロックではなく共有入力の変更である | タッチはpointer validとheld内pointer bitの二系統で読まれる。sead入力での除去は共有TouchState・スクロール・全登録Wrapperと入力idle判定に及び、下画面UIだけを選択するロックではない。 | MEDIUM | A |  |  |
| ACNL-F0723 | SELECTとSTARTの条件付き統合と読み替え前のSELECT除去 | 0x003533D0は0x009778D8が0のときだけ0x00483020を呼び、SELECTをSTARTへ統合する。読み替え前のpad held/pressed/releasedのbit2を除去すれば、STARTと通常の読み替え呼出しを保持してSELECTだけをゲームへ渡さずに済む。 | MEDIUM | A |  |  |
