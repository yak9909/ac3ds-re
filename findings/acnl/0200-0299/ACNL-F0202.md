---
id: ACNL-F0202
aliases:
- F-176
title: 'F-176: Picture はコマンドを直接吐かず、描画コンテキストに四角形を溜めて一括で流す — `HIGH`（静的解析）'
summary: '```c'
date: '2026-08-28'
category: render
build: acnl_jpn_v15
confidence: HIGH
tool: IDA
addresses: []
tags: []
supersedes: []
source: v1:RE/FINDINGS.md:10724-10787
by: unknown
original_by: ''
reviewed_by: []
state: active
consolidated_into: ''
duplicate_of: ''
superseded_by: ''
---
## F-176: Picture はコマンドを直接吐かず、描画コンテキストに四角形を溜めて一括で流す — `HIGH`（静的解析）

### 1. 構造

```c
sub_73CB58(a1 = picture(Pane), a2 = cursor, a3 = ?, a4 = drawctx)
```

**コマンドを直接吐かない。描画コンテキストの配列に四角形を蓄積する。**

| 配列 | カウンタ | 内容 |
|---|---|---|
| `drawctx+1640` | `drawctx+36` | 四角形 1 個につき 16 バイト |
| `drawctx+1644` | `drawctx+37` | 行列。`sub_135C28` が `picture+128` から複製し、**3 ずつ**増える |
| `drawctx+1648` | `drawctx+38` | 幾何・UV |

末尾で溢れ判定:

```c
if ((drawctx+36)+1 > 0x1A || (drawctx+37)+7 > 0x20 || (drawctx+38)+7 > 0x20)
    return sub_4B8360(drawctx);      // まとめて流す
return cursor;
```

**四角形 26 個たまるか行列が溢れると `sub_4B8360` が一括で吐く。**

### 2. ★これが意味すること

`sub_4B8360` は（F-170 の解析より）

```
uniform ブロック（行列）
TextDraw_EmitStatePrefix
reg 0x231 / 0x227（index buffer）/ 0x228 NUMVERTICES = 6 * (drawctx+36)
0x40 バイトの末尾ブロック
```

を積む。つまり **`drawctx+36` を 1 増やして配列に 1 エントリ足せば、
ゲーム自身の仕組みが我々の四角形も描いてくれる。**

**F-174 で断念した「GPU 状態を一から再現する」必要がまったくない。**
シェーダも頂点配列もテクスチャもブレンドも、ゲームが設定したものをそのまま使う。

### 3. Pane のレイアウトは TextBox と共通

| offset | 内容 |
|---|---|
| `+128` | Pane の行列（`sub_135C28` の入力） |
| `+181` | アルファ |
| `+316` | material |
| `+72` / `+76` | 幾何の 2 dword |

**TextBox の `+128` / `+181` と同じ配置。** F-158 / F-160 の行列の知見がそのまま使える。

### 4. 次の実験（TODO-115 の残り）

`sub_73CB58` の**戻り際**に、直前に積まれたエントリを複製して
カウンタを増やす。**これまで 3 回成功している「複製して一部だけ変える」型**
（F-157 / F-168 / F-169）と同じ。

**位置は据え置き、大きさだけ変えて始めること**（F-168 の教訓）。

---

