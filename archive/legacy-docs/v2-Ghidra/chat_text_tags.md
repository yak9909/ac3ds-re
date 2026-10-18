# 通信チャットの埋込みテキストタグ — JPN v1.5

## 結論

**Ghidra-gpt-sol-5.6-CHAT-T006で訂正。通常のstockプレイヤー間チャット経路は、埋込みLMS/MSBT tagをそのまま通さない。**

実機で、送信直前 `0x193944` の最終sourceに

```text
000E 0000 0003 0002 0006 0041 0042 0043 0000
```

が完全に残っていることを確認した一方、`Chat_SubmitLocal` 最初の `WordPtrSv` 代入後には `0041 0042 0043 0000` だけが残った。

原因は `WordPtrSv_Assign @ 0x5FC02C` のsource/destination mode変換である。

- normal submit `WordCPtr`: mode 0
- normal chat storage `WordPtrSv`: mode 1
- mode 0 -> mode 1 は conversion/sanitizer path
- conversion streamは通常文字だけをdestinationへ出力し、start/end tag callbackはno-op
- そのためtagは除去され、可視文字だけが残る

受信側も `Chat_InsertReceived @ 0x215868` で同じmode 0 -> mode 1変換を行うため、packetにraw tagを入れてもstock receiverの最終chat storageへ入る前に除去される。

従って、**stock相手へ通常chat packetだけでSize/Color装飾を反映できる、という旧T002結論は撤回する。**

Size/Colorそのものを解釈するrenderer機能は存在するが、通常chatのsanitizerを通過した後の文字列にはtagが残らない。

## control tag format

UTF-16本文へ直接埋め込まれる。

```text
u16 0x000E
u16 group
u16 type
u16 payloadSizeBytes
u8  payload[payloadSizeBytes]
```

`0x000F`はend/close control codeだが、Size/Colorのresetには明示的なsetting tagを使う方がこのchat経路では確実。

## Size

System group 0 / type 2。

`TextBox_ProcessSystemTag @ 0x5E92A8` はpayload u16をfloat化し、0.01倍してglyph X/Y scaleへ反映する。

- 100 = 0x0064: standard
- 150 = 0x0096: 150%

UTF-16 words:

```text
000E 0000 0002 0002 0096   // size 150%
000E 0000 0002 0002 0064   // size 100% reset
```

## Color

System group 0 / type 3。

Normal chat bodyの `RenderTrace_OnTag @ 0x5DE614` はgroup 0/type 3を明示的にrender bufferへ保持する。ACNL既存tag corpusとJPN側range checkを突き合わせたindex:

```text
0000 white
0001 pink
0002 blue
0003 green
0004 orange
0005 grey
0006 red
FFFF default/clear
```

例:

```text
000E 0000 0003 0002 0006   // red
000E 0000 0003 0002 FFFF   // reset
```

## end-to-end transport

### Local submit

`BsMenuChat_SubmitInput @ 0x1938EC`

- inputをcapacity `0x41` のbounded UTF-16 viewへする
- `Chat_SubmitLocal @ 0x218044`へ渡す

`Chat_SubmitLocal`:

- local chat storageへWordPtr assignment
- network activeならplayer slot別packet IDを `NetPacket_SendById @ 0x6246FC`へ送る
- packet IDs: `0x8C, 0x8D, 0x8E, 0x8F`

### Packet

player別serializer:
- 0x180C7C
- 0x180D6C
- 0x180E5C
- 0x180F4C

固定packet size `0x90`。

```text
+0x08 metadata
+0x0C message type
+0x0D participant mask
+0x0E UTF-16 fixed string, capacity 0x41 code units
```

stock serializerでは、packet text用mode1 WordPtrSvへnormal mode0 sourceをassignするため、mode変換sanitizerが動作しtagを除去する。

### Remote receive

`BsBalloonChat_ProcessIncoming @ 0x217018`:

1. remote playerの0x8C..0x8F packetを取得
2. `ChatPacket_CopyTextOut @ 0x70A4D4`
3. packet+0x0Eをcapacity 0x41のWordPtrへcopy
4. `Chat_InsertReceived @ 0x215868`
5. per-player chat bodyへassign

`ChatPacket_CopyTextOut` 自体はmode1 sourceを使うためpacket内tagを一度保持できる。しかし `Chat_InsertReceived @ 0x2158FC..0x21591C` がraw bufferをmode0 viewとして作り直してmode1 chat storageへassignするため、ここでtagが除去される。

### Remote render

`ChatBubbleNode_RenderMessage @ 0x2140CC`:

```text
source body -> node+0x0C
ChatMessageBox_EmitText(node+0x178,node+0x0C)
```

`ChatMessageBox_InitRenderTrace @ 0x5E24B0` は内部MsgStream vtableを `script::RenderTrace @ 0x903348` にする。

`RenderTrace_OnTag @ 0x5DE614`:

- group 0/type 2: accepted/preserved
- group 0/type 3: accepted/preserved
- group 0/type 4 PageBreak: ignored in normal chat body
- group 0/type 1 Font: ignored in normal chat body
- group 0/type 0 Ruby: special branchは存在するが補助state依存のためremote effect未確定
- group 0xFF/type 6: accepted, meaning未確定

従って通常通信chatに対する確認済み文字装飾はSize/Color。

## group=0のNUL問題

Size/Color tagはheader中に `group=0x0000` を含む。一見するとNUL終端copyで切れる可能性がある。

しかしchat stringは `script::WordPtrSv` を使い、assignment `WordPtrSv_Assign @ 0x5FC02C` はplain `wcslen/wcscpy` ではなく `WordPtrSv_CopyTagAware @ 0x5D42B4` → `MsgStream_Emit` 系で処理する。

そのため `0x000E` を読んだ後のgroup=0はtag headerの一部としてconsumeされ、文字列terminatorとして扱われない。

この性質はlocal chat storage、packet serialization、remote extraction、remote chat-node assignmentに共通している。

## 実用例

red + 150% の `ABC`、その後reset:

```text
000E 0000 0002 0002 0096
000E 0000 0003 0002 0006
0041 0042 0043
000E 0000 0003 0002 FFFF
000E 0000 0002 0002 0064
```

合計23 UTF-16 code units。chat field capacityは0x41なので、tagを入れた分だけ表示文字数は減る。

## 制約

- stock software keyboardからU+000E/binary headerを普通に入力できることは確認していない。
- 従って実用にはmemory injection、submit buffer hook、plugin側string construction等が必要。
- normal chat bodyでremote effectまで静的確認したのはSize/Color。
- PageBreak/A-button wait/TalkSeq emotion等をchatへ送って相手の会話stateを動かす構造は確認できない。
- Rubyはparser branchがあるがremote decorationとしては未確定。

## Ghidra

Primary T001 parser export:
- `acnl_jpn_v15_text_tags_delta.xml/.bytes`

Remote Ghidra-gpt-sol-5.6-CHAT-T002 export:
- `acnl_jpn_v15_chat_remote_tags_delta.xml/.bytes`

Evidence:
- `work/evidence/chat_text_tags_remote_20260916.md`


## Local/self chat rendering

The same embedded Size/Color tags also apply to the sender's own displayed chat message.

`Chat_SubmitLocal @ 0x218044` first assigns the submitted `WordPtr/WordCPtr` source into local chat storage. The text is not flattened to glyphs or stripped of LMS tags before local storage. Normal chat body rendering uses the common `ChatBubbleNode_RenderMessage @ 0x2140CC -> ChatMessageBox_EmitText @ 0x5E21D8 -> MsgStream_Emit @ 0x600BD4` path, so the sender's local bubble reparses the same embedded tags.

This means decoration is not "remote only": an injected tagged string is expected to decorate both the sender's own bubble and the stock remote peer's bubble.

## Inline placement inside the chat body

Tags belong directly inside the UTF-16 body and affect the text that follows them according to the renderer state.

Example: only `ABC` red, then restore default before `DEF`:

```text
000E 0000 0003 0002 0006   // set red
0041 0042 0043             // ABC
000E 0000 0003 0002 FFFF   // reset/default
0044 0045 0046             // DEF
```

Likewise for size:

```text
000E 0000 0002 0002 0096   // 150%
0041 0042 0043             // ABC
000E 0000 0002 0002 0064   // 100%
0044 0045 0046             // DEF
```

The control words are not rendered as visible characters when the tag is structurally valid; they are consumed by `MsgStream`.

Therefore there is no separate "character-decoration field" required. Inject the control sequence at the desired code-unit position in the chat text buffer itself. A malformed/truncated tag must not be treated as equivalent: it can be ignored, misparsed, or consume the remainder incorrectly depending on where truncation occurs.

The 0x41 UTF-16 code-unit chat capacity includes the tag words and payload, so inline styling reduces the available visible-character count.


## 0x958108 pointer-slot correction

`0x958108` is **not** the UTF-16 body storage. It is a global dword that receives the backing-buffer pointer.

Chat setup at `0x193ADC..0x193AEC` stores `*(BsMenuChat+0x50)` into `*(u32*)0x958108`.

The submit path independently reads `*(BsMenuChat+0x50)` at `0x19392C`, wraps that pointer with capacity `0x41` at `0x193938`, and calls `Chat_SubmitLocal` at `0x193944`.

Therefore a direct 32-bit write such as `0x0000000E` to address `0x958108` overwrites the pointer value. To edit the body, first dereference the slot:

```text
P = *(u32*)0x958108
write UTF-16/tag data at P
```

Because the text object's virtual method is invoked again immediately before the submit pointer is read, the safest implementation is to inject/hook near `0x19392C..0x193944` if the software keyboard overwrites a direct pointee edit.

Detailed evidence: `work/evidence/chat_buffer_pointer_20260916.md`.


## Final pre-submit injection checkpoint

Hardware test: writing a valid Color-tag sequence to the pointee read from `0x958108` did **not** change displayed chat text.

Reanalysis shows this does not fit a "tag parsing already finished before send" explanation.

At `BsMenuChat_SubmitInput`, vtable slot +8 resolves to `WordPtrSv_GetPtr @ 0x5FC31C`, which only returns `this+4`. Immediately afterward the final source pointer is read at `0x19392C`, wrapped as a bounded WordCPtr, and passed to `Chat_SubmitLocal` at `0x193944`.

The pre-send `WordPtrSv_Assign -> WordPtrSv_CopyTagAware` path structurally scans control codes, but its character/start-tag/end-tag callbacks are all no-op and the original UTF-16 span is raw-copied afterward. It is not the visual decoration pass.

The strongest injection point is therefore immediately before `0x193944`:

```text
r1 = WordCPtr*
P  = *(u32*)(r1+4)
capacity = *(u32*)(r1+8) = 0x41
```

Patch `P` at that moment and then execute `Chat_SubmitLocal` without returning to keyboard editing.

Display-time interpretation remains later at:
`ChatMessageBox_EmitText -> MsgStream_Emit -> RenderTrace_OnTag`.

Hardware diagnostic breakpoints:
- `0x193944`: exact final submit source
- `0x600CD4`: U+000E start-tag path
- `0x5DE614`: RenderTrace tag callback

Detailed evidence: `work/evidence/chat_submit_injection_20260916.md`.


## Sender mode1 bypass — hardware verified

Hardware test confirmed the mode discriminator.

Immediately before `Chat_SubmitLocal`, replacing only the temporary source object's vtable:

```text
0x00904CF4  // normal mode0 WordCPtr
->
0x00902FB8  // mode1 read-only view
```

caused the destination `WordPtrSv` to retain the complete control-tag sequence.

Therefore:

```text
mode0 -> mode1 : conversion/sanitizer, tags stripped
mode1 -> mode1 : structured copy, tags preserved
```

is now hardware-verified.

Equivalent sender constructor diagnostic remains:

```text
0x193938
stock: EB11A66C   BL 0x5FD2F0
test : EB111022   BL 0x5D79C8
```

This confirms sender-side tag preservation. It does not by itself make a stock remote peer render the tag, because the stock receiver performs another mode0->mode1 sanitizing assignment in `Chat_InsertReceived`.


## Local Color render — hardware verified

With the sender's final submit source changed from mode0 vtable `0x904CF4` to mode1 vtable `0x902FB8`, the complete Color tag survived storage and `ABC` rendered red in the sender's own chat bubble.

Therefore the full local rendering claim is hardware verified:

```text
000E 0000 0003 0002 0006 0041 0042 0043
```

renders red `ABC` when the mode0->mode1 sanitizer is bypassed.


## Stock remote peer limitation

After full message-type analysis, the ordinary player-chat protocol has no stock receive branch that both bypasses the sanitizer and forwards arbitrary incoming body text to the normal chat renderer.

Coverage:

- packet type `0x0A`: handled outside `Chat_InsertReceived`; no normal arbitrary text render.
- `Chat_InsertReceived` types 5/6/7/9: special UI/state branches; entry incoming text is not assigned to the normal body.
- all other types: `0x2158FC..0x21591C` constructs a fresh mode0 source and strips LMS tags during mode0->mode1 assignment.

Therefore sender-side mode1 preservation is sufficient for the sender's own styled bubble and for preserving tags into an outgoing packet, but an unmodified stock receiver removes them before rendering.

Detailed evidence: `work/evidence/chat_stock_remote_limit_20260916.md`.


## Player/town name tags

Scripted message insertion uses LMS group 5 for dynamic names:

- group5/type0 -> current player name
- group5/type5 -> town name
- group5/type6 -> alternate town-name context

The final insertion stage does reparse the cached Phrase with `MsgStream_Emit`, so a control tag present **inside the internal script cache** could be interpreted.

However normal player/town-name loading prevents that.

Player and town names are loaded as mode1 bounded views and assigned into mode0 `script::WordFix<9>` caches. `WordPtrSv_Assign` handles mode1->mode0 with `ContainTagEngine`. Any valid start/end control tag causes the destination WordFix cache to be cleared via virtual +0x1C -> `0x81E138 -> 0x5FC2AC`.

Therefore placing an LMS tag in the ordinary saved/runtime player-name or town-name field does not carry the tag into scripted message windows; the name is rejected/cleared before the later MsgStream pass.

A different result is possible only if the internal `script::Insert` WordFix<9> cache is patched **after** this sanitizer. Detailed evidence: `work/evidence/name_tag_insertion_20260916.md`.
