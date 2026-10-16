# 持ち物の再入場・チェックリスト・選択色 / IDA-gpt-6-F012・T015

担当GPT-6、idalib-mcp、2026-10-13。JPN無印更新版、原入力SHAはstatic.jsonのsurvey参照。ARM/LE32、imagebase0、T=0（原ARM・前回公式XML）。確度MEDIUM、実機未確認。

## 利用者の実機訂正と設計

- 個別checklistが開かない。GuiMenuの通常ActivateSelectedにITEM_CHECKBOX_LIST分岐が無かった。既存inline UI/bitmask編集/適用/保持を使い、通常項目のAから開く。設定のチェックリストは保持する。
- trashはONを持続してpocket再入場時も表示。native AppendIconGroupはgroupのnodesをcontrolへ移す。Detach後もlayoutが残る短い再入場ではgroupが空なので、nodeをgroupへ戻してから再登録/入場animを再生する。BsMenuItem Dispose入口でletter/controlの破棄前に解除し、actorアドレス再利用も別入場として扱う。資源不足でONを取り消さず再試行、描画を止めて3frame後の解放を保持する。
- ItemDragWindow Build原ARM0x26F1E8/0x26F1ECは背景priority0x83。LayoutMgrは昇順のintrusive list（0x56928C→0x566E68）、後が手前。trashを0x84とし選択窓より下、持ち物背景より前へ。
- trash自身のdrag/crashも同scope。真のDragIconControl vtableは0x8EABB8（0x8EE23CはButtonActionControlである）。vt+16=0x29A22Cはsource group+317が1の場合のみdrag開始を計算。group+318はクリック、+319はdrop受け取り。私有group+317のみ0にし、通常itemのdrag/dropはnativeへ任せる。以前のfixtureでcontrolをButtonActionControlへ差し替えた経路はdrag検証に使わない。
- click後の次のitem操作も真の解除関数で検証する。旧closet fixtureが0x29BAB4をmockした残りにより決定flagが残る現象を再現したが、これは製品の後片付け不具合の証拠ではない。native FinishDecided/2F72C4/ClearAllTouchesを実行して解除を確認する。
- 保持色は青。native SetTouchはtouch/select（node+32/+72）の終端であり、native InstSelect_SetSelectVisualはdecide（+112/+152）の終端を使う。後者に揃える。A取得後DPad移動で旧行が残る追加症状は、旧selected nodeの4animを戻してからnative SetSelectを呼ぶ私有vt[16]で対応。touch変更/scrollで物理rowが変わった時も旧nodeを戻す。再取得の音/anim・現在selected行1tap・他行はfocusのみを保持。
- manualクローゼットのスロット/アイテム/開くの3cheat、専用設定データ/登録を削除。chatの名前/ID検索のlist/closet切替、無限取得/持ち物操作/帰還は保持。

## 証拠・検証と限界

既存F010/F011を先に検索、主DBはroot単独。静的根拠はwork/evidence/gohan_inventory_ui_fix/static.json（原ARM＋caller/vtable/sourceを独立照合）。元DBの既存NOP patchは変更しない。新規概念はDBの名前/型/注記へ反映し、保存/公式XMLを読戻す。

実GUIの入口A→個別編集/描画/適用をlinked ARMで検証する。trashは実DragIconControlの押下/長押し/移動/離上、item受け取り、開閉/同actor再利用/短い再入場、heap失敗後再試行と元letter復元を確認する。blueの4anim開始/終端とDPad/タッチ/scroll旧row解除を検証する。GPUの実際の色・draw、音、heapの実機タイミングはPC成功から確定しない。

正常・旧13配布版を保持、専用BuildInventoryUiFixとartifacts/plugins/gohan_inventory_ui_fix1へ出力。main/実機/SD/中断整理未操作、Gitは全修正/PC/DBXML完了後に最後一括。実機で異なる結果ならF012を訂正する。
