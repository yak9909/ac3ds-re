---
id: ACNL-F0766
aliases: []
title: "共通UIの49関数の引数とVFP呼出規約"
summary: "共通UIの49関数に引数・戻り型を設定した。floatの入力はVFP S0/S1、Paneの基準位置は2成分をS0/S1で返す。未定義のオブジェクト型は理由付きvoid *とする。"
date: 2026-11-11
category: ui
build: acnl_jpn_v15
confidence: MEDIUM          # LOW / MEDIUM / HIGH
tool: IDA
addresses: [0x11da78, 0x120d54, 0x1261ec, 0x12653c, 0x133a5c, 0x13b9a8, 0x1af858, 0x1b0698, 0x1c513c, 0x1c58f4, 0x1c5a34, 0x1fa86c, 0x2939c8, 0x298018, 0x298664, 0x2987a8, 0x2f62c8, 0x2f6c28, 0x2f72c4, 0x2fd0cc, 0x4b5844, 0x4b5900, 0x4b8ecc, 0x4bacbc, 0x4d51b0, 0x567244, 0x567310, 0x567a50, 0x567da4, 0x568840, 0x568a04, 0x568c00, 0x568cac, 0x568cfc, 0x5beb4c, 0x693ee8, 0x6d1428, 0x6d3f04, 0x6d474c, 0x6d4e5c, 0x722c34, 0x73b5c4, 0x74d744, 0x74d8b0, 0x74f58c, 0x75b8a8, 0x7c6eb0, 0x7e8488, 0x8268e0]
tags: ["layout"]
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: gpt-6
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

共通UIの49関数に引数・戻り型を設定した。floatの入力はVFP S0/S1、Paneの基準位置は2成分をS0/S1で返す。未定義のオブジェクト型は理由付きvoid *とする。

確度 MEDIUM。実測なし。各関数の命令列を、別の関数の引数生産・戻り消費、または vtable の実値と照合した。既存の関数名は変更していない。void 戻りの更新関数は、全経路での有効な戻り値生成がなく、呼び元も結果を消費しないもの。命令列の最後に残る R0 や状態 PMF の2語を int/int64 の戻り型にしない。

## 根拠

ビルドは `acnl_jpn_v15`。全関数書き出しは `4914ab98f271092df116b05c38a6183939b88b16` 時点。現在名は symbols を併読した。命令位置・呼び元は書き出しから引き、実バイトは `tools/codebytes.py` の `read_bytes` と Capstone で原本 code.bin を読む。原本 SHA256 は台帳と一致。命令列は `_local/evidence/149/original-asm.txt`、直接呼出の前後は `caller-asm.txt`、vtable/状態表の実値は `data-evidence.json`。IDB は指定の作業用コピーで型の適用・保存・読み戻しにだけ使用した。

表は手作業で復元した宣言を読みやすく示し、呼出規約のキーワードを省略している。VFPの引数・戻りはレジスタ注記を残した。厳密なIDA宣言はsymbolsのprototype欄に保存する。

| 番地・既存名 | prototype | 命令列と独立根拠／未定義型の理由 |
|---|---|---|
| `0x0011DA78 graphic_MemoryMgr_CreateDefaultHeaps` | `void *graphic_MemoryMgr_CreateDefaultHeaps(void *parent_heap)` | 11DA90 R2=入力R0→2F6D7Cの親heap。11DB80 R0=生成mgr、11CA9C直後に保存。 親heapの派生種別とMemoryMgr構造未定義のためvoid *。 |
| `0x00120D54 ArcResAccReader_Ctor` | `ArcResAccReader *ArcResAccReader_Ctor(ArcResAccReader *reader)` | 120D54..DA4 thisに3サブオブジェクトを構築し元thisを返す。11DDC0は戻りthis+248。  |
| `0x001261EC UiAnim_Ctor` | `UiAnim *UiAnim_Ctor(UiAnim *anim)` | 1261F4..6224が+4..24を初期化。R0保持、11DDF0は戻りthis+28。  |
| `0x0012653C ssys_ma_lyt_Layout_Ctor` | `SsysMaLayoutNode *ssys_ma_lyt_Layout_Ctor(SsysMaLayoutNode *layout)` | 12653C→12D2BCのbase ctor、vptr変更後this返却。11DDD8で戻り+14C。  |
| `0x00133A5C ssys_ma_lyt_Layout_UnbindAllAnimations` | `void ssys_ma_lyt_Layout_UnbindAllAnimations(SsysMaLayoutNode *layout)` | 133A5Cでthis+10を4B8F24へ渡す。1339F0で戻りを使わず次要素へ。  |
| `0x0013B9A8 nwlyt_TextBox_AllocStringBuffer_0` | `void nwlyt_TextBox_AllocStringBuffer_0(NwLytTextBox *text_box, unsigned int capacity, unsigned int flags)` | 13B9A8..13BB04はR1=capacity,R2=flagsで文字器と描画器を確保する。TextBox vtable+70の実値が13B9A8、4BB084のInitFieldsが同slotへcapacity/flagsを渡す。戻りR0は確保・解放枝で不統一。  |
| `0x001AF858 InstSelect_SetSelectVisual` | `void InstSelect_SetSelectVisual(void *list, int selected, int previous)` | 1AF858..F968 R1新選択/R2旧選択からtopを引き旧行解除・新行+AE8更新。29E65Cと6EDE84は戻りを不使用。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x001B0698 SelectBase_WaitCalc` | `void SelectBase_WaitCalc(void *list)` | 1B0698でthis+A00をIsDecidedへ、1B078CでClearDecided。29ED10の戻りを使わず次操作。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x001C513C SelectBase_SetupStep` | `bool SelectBase_SetupStep(void *list, ArcResAccReader *reader, void *heap)` | 1C5144 R7=R1,1C5158 R5=R2。1C51E4にreader保存、1C52C4にheap、21CB14/2B59EC直後CMP R0,#0。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 heapの具象型は制約されずvoid *。 |
| `0x001C58F4 SelectBase_StartEnter` | `void SelectBase_StartEnter(void *list)` | 1C5900でStateMachine_ChangeTo(this,入場PMF)を呼ぶ。21B914は戻り不使用。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x001C5A34 SelectBase_StartLeave` | `void SelectBase_StartLeave(void *list)` | 1C5A40でStateMachine_ChangeTo(this,退場PMF)を呼ぶ。21BCE0は戻り不使用。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x001FA86C BsHandCursor_Hide` | `void BsHandCursor_Hide(void *cursor)` | 1FA87C/+4D1,+4D0をクリアし6アニメのboundを読む。133B00と18F304は戻り不使用。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x002939C8 BsTimeBelWindow_Init` | `int BsTimeBelWindow_Init(void *window)` | 2939C8以降thisをR4保持、スキップ枝も正常枝もR0=2。vtable BsTimeBelWindow(8EAA78)+Cの実値が2939C8である初期化コールバック。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 戻り2は状態処理の整数でありboolではない。 |
| `0x00298018 CommonScrollBar_AttachTo` | `void CommonScrollBar_AttachTo(void *scroll_bar, NwLytPane *parent)` | 298024でrootの親を解除、298038以降R1親へAppendChild。21CB3C直後戻り不使用。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x00298664 CommonScrollBar_UpdateDrag` | `void CommonScrollBar_UpdateDrag(void *scroll_bar)` | 298664..各分岐がtouch/hand状態から座標を作りvt+10へ渡す。299D6Cの呼び元は戻りR0を使わずVFPの座標処理を続ける。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x002987A8 CommonScrollBar_SetPos` | `void CommonScrollBar_SetPos(void *scroll_bar, int top)` | 2987B0でR1をthis+71Cへ保存、signed clamp。1C5444後R0を別値に上書き。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x002F62C8 ButtonActionControl_HandInput` | `void ButtonActionControl_HandInput(void *control)` | 2F62C8..thisの入力・選択node・反復カウンタを更新。ButtonActionControl vtable+20。返りR0は分岐で不統一。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x002F6C28 ButtonActionControl_Decide` | `void ButtonActionControl_Decide(void *control)` | 2F6C28..選択nodeのStartDecide、+D4 bit1と+B8のPMFを書込。ButtonActionControlのvirtual+2Cから呼ばれ、2F62C8の入力処理では戻りを消費しない。29B620は同じthisでの末尾呼出。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x002F72C4 ButtonActionControl_ClearDecided` | `void ButtonActionControl_ClearDecided(void *control)` | 2F72CCでflags、2F72EC..7308に選択ptr/flags/PMFを戻す。1B078C等でR0不使用。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x002FD0CC Heap_Alloc` | `void *Heap_Alloc(unsigned int size, void *heap, int alignment)` | 2FD0CC..D8はR0=size,R1=heapを交換、R2=alignment保持して1328D8へ。11DABCはsize20/align4で生成先を使用。 共通heapの具象クラス未固定のためvoid *。 |
| `0x004B5844 nwlyt_ArcResourceAccessor_GetTexture` | `void nwlyt_ArcResourceAccessor_GetTexture(void *texture_info_out, void *accessor, const char *name)` | 4B5848/50/54でR1 accessor,R0出力,R2名前を保存。4B5884..8Cが5wordを出力。568CFCの呼び元で20Bの出力先を渡す。 出力は20BのTextureInfo相当、accessorも構造未定義のためvoid *。隠れた集成体戻りの出力を明示したABI。 |
| `0x004B5900 nwlyt_ArcResourceAccessor_Attach` | `bool nwlyt_ArcResourceAccessor_Attach(void *accessor, void *arc_data, const char *root_name)` | 4B5904 R5=R1,4B5910 R6=R2。DARC解読失敗は0、4B595C成功は1。5672C4呼出でreader+C/arc/root。 accessorとDARC領域の構造未定義のためvoid *。 |
| `0x004B8ECC Layout_BindAnim` | `void Layout_BindAnim(SsysMaLayoutNode *layout, UiAnim *anim)` | 4B8ED0でanim+1C=1、+18を取得、layout+10へ調整し4B8EE0に連続。194304で戻り不使用。  |
| `0x004BACBC nwlyt_TextBox_SetString` | `unsigned short nwlyt_TextBox_SetString(NwLytTextBox *text_box, const unsigned short *text, unsigned int destination, unsigned int length)` | 4BACC8 R5=R2、4BAD28でR3を残容量と比較し4BAD68 UXTH R0,R6。4BB3E8は初期文字コピー。font=NULL枝もR0=0。  |
| `0x004D51B0 nwfont_CharWriter_RecomputeScale` | `void nwfont_CharWriter_RecomputeScale(void *writer@<R0>, float width@<S0>, float height@<S1>)` | 4D51BC/C0でS0/S1を保存、font vt+8/+Cの幅高さで除算、+24/+28へ。4BADA4呼出前にTextBoxの幅高さをVFPロード。 CharWriter全体型が未登録のためvoid *。 |
| `0x00567244 ArcResAccReader_LoadArcStep` | `bool ArcResAccReader_LoadArcStep(ArcResAccReader *reader, const char *path)` | 567254..読込helperへpathのSafeString、完了時+158を+8へ。192C58/70は戻り値を検査。  |
| `0x00567310 ArcResAccReader_Dtor` | `ArcResAccReader *ArcResAccReader_Dtor(ArcResAccReader *reader)` | 567318.. +15CのLoadSplit、+C accessorを破棄しSUB R0,#C。18E37Cの戻りにthis補正を加える。  |
| `0x00567A50 vc_ACSYSTEM_DATA1` | `void vc_ACSYSTEM_DATA1(SsysMaLayoutNode *unused_layout, UiAnim *anim, void *group, bool recursive)` | 567A54でR0を上書きしlayout不使用。R1=anim,R2=group,R3→Pane vt+3Cの再帰指定。18EB00はR3=0。 groupの完全型未登録のためvoid *。第1引数は読まないが既存呼出形を維持。 |
| `0x00567DA4 vc_DATA3` | `void vc_DATA3(SsysMaLayoutNode *unused_layout, UiAnim *anim, void *group, bool recursive)` | 567DA8でR0上書き。anim+1C=0、R3をPane vt+40へ、4B6600のR2は子巡回フラグ。18EF4CでR3=0。 groupの完全型未登録のためvoid *。第1引数は既存の呼出形を維持。 |
| `0x00568840 Layout_UnbindAnim` | `void Layout_UnbindAnim(SsysMaLayoutNode *layout, UiAnim *anim)` | 568844でanim+1C=0、+18をR1へ、layout+10→4B8F04。194380直後戻り不使用。  |
| `0x00568A04 UiAnim_Load` | `bool UiAnim_Load(UiAnim *anim, const char *name, ArcResAccReader *reader)` | 568A04..reader+4のaccessorからname検索。factoryの結果を検査して失敗時0/成功時1を返す。18EAECはR0=anim,R1=name,R2=readerを設定して呼ぶ。  |
| `0x00568C00 UiAnim_SetFrame` | `void UiAnim_SetFrame(UiAnim *anim@<R0>, float frame@<S0>)` | 568C00/04でS0を+C/+8へ、+18のtransform+10へ。18EFA4直前にS0=0。  |
| `0x00568CAC UiAnim_Dtor` | `UiAnim *UiAnim_Dtor(UiAnim *anim)` | 568CB4でvptrを設定し+18/+20を破棄、568CF0 MOV R0,R4。18E374以降戻りthisを補正して次のdtor。  |
| `0x00568CFC ArcResAccReader_RegisterTextures` | `bool ArcResAccReader_RegisterTextures(ArcResAccReader *reader)` | 568CFC..reader+8のDARCのtimgを巡回しreader+Cからtexture登録。対象ディレクトリなしは0、巡回後1。21C828はR0=readerを渡す。  |
| `0x005BEB4C ssys_ma_lyt_Layout_Dtor` | `SsysMaLayoutNode *ssys_ma_lyt_Layout_Dtor(SsysMaLayoutNode *layout)` | 5BEB4C→5688A0。5688C8 this+30→+10のLayoutを破棄、5688DCで元thisへ。18E384後戻り補正。  |
| `0x00693EE8 BsMenuBg_StartLeave` | `void BsMenuBg_StartLeave(void *background, int next_kind)` | 693EF0 R5=R1、693F44で+614保存、693F50は退場状態へ。6D4E84はR1=10で呼び戻り不使用。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 next_kindは退場後の種類指定。 |
| `0x006D1428 BsMenuMgr_ProcessMapCommand` | `void BsMenuMgr_ProcessMapCommand(void *manager)` | 6D1428..R0 this+1E4/1E8とcommand949D25を処理。6D367C後戻り不使用。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x006D3F04 BsMenuTab_ConsumeCommand` | `void BsMenuTab_ConsumeCommand(void *tabs)` | 6D3F0C..command949D24を読み11へ戻し、this+14の状態を変更。6D7F94後戻り不使用。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x006D474C BsMenuTab_TabSelectUpdate` | `void BsMenuTab_TabSelectUpdate(void *tabs)` | 6D474C..this+494/+618のcontrolを使う。状態表のcalc PMFから呼ぶ。通常末尾は6D7A3Cへの末尾呼出で、各分岐のR0に統一した戻り契約はない。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x006D4E5C BsMenuTab_MenuOutUpdate` | `void BsMenuTab_MenuOutUpdate(void *tabs)` | 6D4E5C..6D5110(this,10)とMenu_IsIdleAndEmptyを待ち、背景退場・MapSyncへ。BsMenuTab状態表のcalc PMFから呼ぶ。戻りR0は待ち/遷移枝で不統一。 対象クラスの全欄・型の登録を確かめていないためthisはvoid *。 |
| `0x00722C34 ButtonActionControl_IsDecided` | `bool ButtonActionControl_IsDecided(const void *control)` | 722C34..+D4 bit0またはPMF条件からR0=0/1。18F0C8/190F60直後CMP R0,#0。 Control全体型未登録。読取り専用のthisはconst void *。 |
| `0x0073B5C4 Pane_GetAnchorOffset` | `AcnlUiPoint2 Pane_GetAnchorOffset@<0:S0,4:S1>(const NwLytPane *pane@<R0>)` | 73B5C4..基準位置からS0/S1を返す。4BA048直後と4BAA34直後がVSTM {S0-S1}、出力pointerなし。  |
| `0x0074D744 sead_ExpHeap_getFreeSize` | `unsigned int sead_ExpHeap_getFreeSize(SeadExpHeapPrefix *heap)` | 74D744..free listのblock+Cを合計、lockでheapを書き得る。sead ExpHeap vtable+3Cと既存F0713。  |
| `0x0074D8B0 sead_ExpHeap_getMaxAllocatableSize` | `unsigned int sead_ExpHeap_getMaxAllocatableSize(SeadExpHeapPrefix *heap, int alignment)` | 74D8B0..R1をabs・power-of-two検査し+50 directionとsigned乗算。sead ExpHeap vtable+40。  |
| `0x0074F58C UiAnim_IsFinished` | `bool UiAnim_IsFinished(const UiAnim *anim)` | 74F58C flags=1はframe>=total-1、3はframe<=0。18EF00/18EFFCでR0検査、書込みなし。  |
| `0x0075B8A8 vc_NPC_2_SETUP` | `bool vc_NPC_2_SETUP(void *message_data, void *word, const char *label, unsigned int index)` | 75B8D4へR0 message_data,R2 label,R3 indexを保持して転送。75BBBCはindex<1000とlabel書式を使う。Word vt+14/+1Cへ代入/clear、R0=成功0/1。 WordFix38に限定せずWord基底virtualを呼ぶためwordはvoid *。message_data全体も未定義。 |
| `0x007C6EB0 InstSelect8_Ctor` | `InstSelect8 *InstSelect8_Ctor(InstSelect8 *list)` | 7C6EB4でSelectBase ctor、+AECに28*8、+BCCに224*8の配列を構築。+9C0=8、+220/+9FCを設定してthis返却。1C7A48後派生vptrと+12CC以降。  |
| `0x007E8488 nwfont_TextWriter_Ctor` | `void *nwfont_TextWriter_Ctor(void *writer)` | 7E848CでCharWriter ctor、+4C..60初期化。4B497Cの戻りからF8を引き、4BAFC4はSP上64Bへ。 TextWriterの全体型未登録のためvoid *。旧版は0x74Bを予約するが、ゲームのローカルwriterとコピー範囲は0x64B。 |
| `0x008268E0 nwfont_TextWriter_CalcStringWidth` | `float nwfont_TextWriter_CalcStringWidth@<S0>(const void *writer@<R0>, const unsigned short *text@<R1>, int length@<R2>)` | 826900/14でwriterを64Bコピー、R1文字列/R2長をCalcStringRectへ。826940でS0=右-左。5E94B8直後VFPで消費。 TextWriter構造未定義のためconst void *。原writerはコピー元のみ。 |

- `Pane_GetAnchorOffset` の2成分は既存 `AcnlUiPoint2`（float x,y）で表現。IDA の正規化表示は `AcnlUiPoint2 __usercall@<S1:S0>(const NwLytPane *pane@<R0>)`。R0 の隠れた出力引数はない。4BA048/4BAA34 の直後に `VSTM {S0-S1}` がある。
- TextBox の確保関数は `0x8FC07C+0x70 → 0x13B9A8`、HandInput は `0x8EE23C+0x20 → 0x2F62C8`。ExpHeap の `+0x3C/+0x40 → 0x74D744/0x74D8B0`。直接の呼び元がないものはこれらと InitFields/仮想呼出側を使う。BsTimeBelWindow の `0x8EAA78+0xC → 0x2939C8` は初期化コールバックで、戻り 2 を保持する。
- BsMenuTab の更新関数は状態表の calc 欄（`0x850944 → 0x6D474C`、`0x850980 → 0x6D4E5C`）。`0x6D7F58` の消費側は PMF をロードして this 補正後に呼び、R0 を結果として使わない。
- `vc_ACSYSTEM_DATA1`/`vc_DATA3` の第1引数は入口で上書きされ、読まない。呼出形を保って Layout pointer として残し、unused を明記。第4引数は単なる zero 値の欄ではなく、Pane vt+0x3C/0x40 へ転送される子孫再帰指定（後者の実体 `0x4B6600` は非ゼロ時に子を巡回）。

### 旧版の宣言との違い

- `CtorFn` の `void *` を UiAnim/ArcResAccReader/Layout/InstSelect8 の型付き this と戻りにした。UiAnim/ArcResAccReader/Layout の dtor もゲームの呼び元が戻り this を次の破棄先計算に使うため pointer 戻り。追加の削除フラグ引数はない。
- `ArcLoadStepFn`/`AnimLoadFn`/`AnimFinishedFn`/`RegisterTexFn`/`AttachFn` の旧 int 戻りは、命令列の 0/1 生成から bool。旧 `SetStringFn` の int はコピーした UTF-16 単位数（`UXTH R0,R6`）として unsigned short。全引数は32bitレジスタ単位で渡される。
- `AnimSetFrameFn`/`ScaleFn`/`MeasureFn` は C の見かけだけでなく S0/S1 を明示。旧 `ScaleFn(writer,sx,sy)` の二値は倍率そのものではなく要求する文字の幅・高さで、font の幅・高さで割って writer の倍率を作る。文字幅の戻りは S0。
- `SetupStepFn(list,holder,heap)` は旧版の3引数が正しく、書き出しの疑似 C の2引数は R2 の欠落。`HeapAllocFn` は GameList の `(size,heap,alignment)` が当該 0x2FD0CC に一致。DecorLayout の `(heap,size,alignment)` は仮想 heap メソッド用であり、同一宣言に混同しない。
- `GroupAnimFn` の第4引数 zero は bool recursive にした。第1引数は互換の呼出形として残す。Group の全構造体型は未登録なので void *。Word の引数も WordFix38 専用ではなく基底 virtual で代入するため void * を残す（既存 F0755 と両立）。
- 旧版の `TextWriter` 予約量は 0x74B。ゲームの `0x4BAFB0` は SP に 0x64B を用意し、`0x8268E0` は writer を 0x64B コピーする。今回全 writer 型の定義は行わず、この差を予約量から型を推定しない理由として残す。
- 冒頭の typedef に宣言がない表内の関数も、ゲーム側の命令と呼び元／仮想表で補った。既存 `UiAnim_Step`/`UiAnim_Init` など対象外の prototype は変更しない。

参考資料は依頼指定の旧版 gohan（`_local/legacy-src/gohan-legacy/Sources/Gui/GameList.cpp`・`GameLabel.cpp`・`Sources/Cheats/DecorLayout.cpp` の冒頭の型宣言。出所は依頼文、meta/references.toml の既存キーなし）。未検証の手がかりとして照合し、結論は命令列と独立したゲーム内の呼び元・消費側または vtable の実値に基づく。

## 反証条件・未確認点

- 実機・SDK ヘッダ・全派生クラスでの ABI 検証は未実施。opaque this の全構造体、TextureInfo 20B の全欄、Word 基底や message_data 全体、heap の全派生型は未確定。
- 戻り不使用の更新関数に意味のある値を要求する独立した呼び元、追加の入力レジスタ・stack 引数、異なる VFP 配置を要求する呼び元が見つかれば型を再検討する。bool は観測した0/1契約であり、失敗復旧や資源寿命の保証ではない。
