（ワーカーの最終の返答を司令塔が保存した）
DONE_WITH_CONCERNS

（codex-bridge taiyo、gpt-6.1-sol / high。t20261121-174250-4。全文は codex-bridge の get_result）

3 型を symbols に入れた。確度はすべて MEDIUM（生成・設定側と独立した利用側の静的照合、実測なし）。IDB・git は不使用。

- InstSelect8（4812 B、ACNL-F0773）: +0x2C layout、+0x178/+0x1A0 enter_anim/leave_anim、+0x218 frame_pane、+0x21C row_messages、+0x224 scroll_bar（CommonScrollBar）、+0x9BC scroll_kind、+0x9C4 item_count、+0x9C8 text_capacity、+0x9CC row_pitch、+0x9D0 animation_active、+0x9D1 input_disabled、+0xAE4 selection_pane、+0xAE8 selected_index。既存の row_layouts・row_count・row_nodes は維持。
- CommonScrollBar（1944 B = 0x798、ACNL-F0774）: vptr、+0x4 arc_reader、+0x24C layout、UiAnim 4 つ、+0x6F8 input_disabled、+0x6FA drag_active、+0x71C top_row、+0x720 max_top_row、+0x724 row_offset、+0x744 input_mode、+0x748 row_pitch、+0x74C row_limit、+0x750 item_count、+0x760 callback_context、+0x764 knob_pane、+0x788 all_pane。所有判定は scroll == list + 0x224。
- NwFontTextWriter（100 B、ACNL-F0775）: +0x24/+0x28 scale_x/y、+0x3C font、+0x4C width_limit、+0x50 line_spacing、+0x54 char_spacing、+0x5C draw_flags、+0x60 tag_processor。CalcStringWidth の MOV R2,#0x64 とコピーが一致。

未確認（コメントだけ）: InstSelect8 +0xAB4・+0xAEC・+0xBCC、CommonScrollBar +0x6FB、TextWriter +0x58。実機での生成・操作・破棄は未検証。8 整列が必須かは未試験。

訂正の提案: F0711 の TextBox +0xEC/+0xF0 の「行間／字間」は「字間／行間」の語順の誤り。

変更: findings ACNL-F0773〜F0775、symbols の types/local_types.h、functions・comments の 00200000/00400000/00700000/00800000.csv、索引。
確かめ: kb.py lint 794 件エラーなし、audit 1057 ファイル問題 0。
