---
id: ACNL-F0438
aliases:
- IDA-gpt-6.1-sol-F013
title: 外観に依存せず室内の壁配置・張替え機能を判定（2026-10-09、静的MEDIUM、2026-10-10利用者実機PASS）
summary: '2026-10-10追記: F014同梱hhd_room_camera1について利用者が実機で問題なく動作と報告。提示版に対する確認として確認待ちを解消し、端末SHA/壁材質別の個別試験一覧は未再測定として扱う。'
date: '2026-10-09'
category: _product
build: acnl_jpn_v15
confidence: ''
tool: IDA
addresses:
- 5978820
- 6889676
- 7103444
- 9735660
- 5178868
- 4886780
tags: []
supersedes: []
source: IDA:work/FINDINGS.md:214-226
by: gpt-6.1-sol
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## IDA-gpt-6.1-sol-F013: 外観に依存せず室内の壁配置・張替え機能を判定（2026-10-09、静的MEDIUM、2026-10-10利用者実機PASS）

2026-10-10追記: F014同梱hhd_room_camera1について利用者が実機で問題なく動作と報告。提示版に対する確認として確認待ちを解消し、端末SHA/壁材質別の個別試験一覧は未再測定として扱う。

解析ソフトIDA（idalib-mcp）/解析モデルgpt-6.1-sol。対象は日本語版無印＋更新、原code SHA-256 `c635af8f08937b66f123b91b02391a68c034393320cdb94d603b9291383faabb`。利用者はテント外観へ改造された普通の室内で壁かけ家具が不可になると報告し、外観ではなく実機能での判定を指示。

- 旧事前ゲート`Room_IsHouseTentForWallPlacement 0x5B3AC4`はHouse+0x4の外観で拒否する。これをgohan壁配置から除去し、`Room_TryPutFurnitureAt 0x6920CC`のマップ壁属性/方向/空き/全footprint/上限を使う。壁の追加class5条件は`0x6C63D4`で、初期化された8 byte全体ではなく先頭6 byteだけを除外リストとして読む。
- 張替えの対象モデルは稼働中`g_BsCharRoomViewMgr 0x948DEC`が指す実体。床holderは+0x3834で`m_carpet`、壁holderは+0x3AE8+0x40*sideで`m_wall`。Initと別のApply/SubmitのARM、型取得と材質辞書のARM、原本6地点全bytesを照合した。`ModelInstance_GetModelNode 0x4F05F4`と`ResModel_FindMaterialByName 0x4A90FC`は読取りで、モデル型と張替え材質の存在を確認できる。
- 保存データと部屋所有権を確認し、選択面にモデル/材質がある場合だけ通常setterを呼ぶ。拒否後の下位setterは既存のオフライン制約を維持し、外観0限定を撤去。通常の通信経路は元setter、通信中の例外張替えは未対応。外観やゲーム命令は書き換えない。
- 主IDBへ9関数/1globalのrename、部分型3件、型9件、stroff、17コメントを保存。元の実名と過去コメントは保持。DB所有者なし、XML/bytes/manifest検証PASS。PC31条件とリンクARM1176の19条件、全分岐/ABI/リテラル等検査PASS。作業枝`work/decor-room-capabilities`、コードcommit `be72724`、成果物`artifacts/plugins/decor_catalog14/gohan.3gx`。実機結果が得られるまでmainへ入れない。

独立照合・全番地・hash・検査の模擬部分・反証条件は [report.md](evidence/t022_room_capabilities/report.md)。実機で実材質の有無と張替え可否が一致しない、正しい壁への配置が拒否される、配置不可の壁へ生成される、または他人の部屋へ書き込む場合は該当MEDIUM結論を再検証する。旧IDA-gpt-6.1-sol-F007の外観0例外とF012のテントゲート維持は、今回の最新指示に従い置き換えた。

