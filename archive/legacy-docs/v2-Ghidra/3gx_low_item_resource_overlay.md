# 3GX low-ID item resource overlay design

## Provenance

Design label: **gpt-sol-5.6案**

This document records the GPT-5.6 Sol proposed architecture for implementing low-ID field-object item icons/names as a 3GX SD-backed display-resource overlay. It is a design proposal, distinct from hardware-verified reverse-engineering findings.

Date: 2026-09-17
Scope: ACNL JPN v1.5, low field-object Item IDs 0x0000..0x00FA

## Goal

Implement custom display icons and names as a 3GX cheat/plugin without changing RomFS and without remapping low IDs into the stock Item.bin gameplay domain.

## Design principle

Keep game semantics stock and virtualize only display resources.

```text
Item 0x0000..0x00FA
   |
   +-- icon resolver hook
   |      -> synthetic basename fgo_XXX
   |      -> global layout resource overlay
   |      -> SD-backed BCLIM
   |
   +-- name resolver hook
          -> plugin-side UTF-16 name table
          -> game Phrase assignment helper
```

Do not patch `Item_ToParamIndex` or `ItemParam_GetRecord`.

## Why SD loose/custom resources are better than a replacement NintendoWare .arc

A 3GX plugin already executes inside the title and can own its own SD-backed assets.

Rebuilding a stock-compatible `.arc` adds constraints that the plugin does not need:
- exact NintendoWare archive serialization;
- archive member alignment;
- preserving all stock members;
- duplicating custom BCLIMs across every archive that may be used by different UI surfaces.

Instead, use a virtual resource overlay:
- stock resource names fall through to the stock ArcResourceAccessor;
- only a private namespace such as `fgo_XXX.bclim` is intercepted;
- the overlay returns plugin-owned BCLIM bytes.

This keeps stock archives untouched.

## Icon hook layer

Existing analysis:

- `ItemParam_GetIconBaseName @ 0x535110`
- `ItemIconWidget_SetItem @ 0x2B8EAC`
- `LayoutResourceAccessor_GetTimg @ 0x4B4A18`
- `ArcResourceAccessor_GetResource @ 0x4B6D94`

Recommended split:

### Hook A: low-ID basename resolution

For `baseId = itemId & 0x7FFF`:

（疑似C を省略。原本は _local/legacy-src/…）

Fixed basename slot:

```text
"fgo_000\0" = 8 bytes
...
"fgo_0fa\0" = 8 bytes
```

251 entries = 0x7D8 bytes.

### Hook B: resource overlay

Intercept the layout resource lookup at the lowest practical function whose ABI can safely return raw BCLIM resource bytes.

Desired behavior:

```text
type != timg
    -> stock

name does not start with "fgo_"
    -> stock

name == fgo_XXX.bclim
    -> return plugin-owned cached BCLIM bytes for ID XXX
```

The best candidate is `ArcResourceAccessor_GetResource @ 0x4B6D94` if its exact return/out-size ABI allows a pointer to external resource memory.

Before implementation, verify:
- return pointer ABI;
- resource-size out parameter;
- whether callers retain the returned BCLIM pointer after texture creation;
- thread/reentrancy behavior.

Do not hook higher-level texture objects until necessary; feeding the original game the expected BCLIM lets NintendoWare perform normal decode/texture construction.

## Name hook

Use `ItemName_ResolvePhrase @ 0x56D274`.

For low IDs:
- bypass the stock empty-name / `???` fallback;
- assign a plugin-side UTF-16 string to the output Phrase with an existing game Phrase/WordPtr helper;
- for all other IDs, execute stock behavior.

This avoids:
- extending `STR_Item_name.umsbt`;
- registering a custom UMSBT;
- touching Script/Str resource tables.

A direct Phrase assignment helper must be selected/verified before implementation so that ownership/mode semantics match the destination Phrase.

## SD data layout

Recommended development layout:

```text
sd:/ACNLPlugin/
  item_display/
    jpn_v15/
      manifest.bin
      icons/
        fgo_000.bclim
        fgo_001.bclim
        ...
        fgo_0fa.bclim
      names.bin
```

Do not put game data next to the 3GX only because it is convenient. A stable plugin-data root allows plugin upgrades without replacing the user's assets and supports multiple title/build profiles.

## Manifest / name format

For 251 dense low IDs, avoid a general-purpose map.

Suggested manifest header:

（疑似C を省略。原本は _local/legacy-src/…）

Suggested name index:

（疑似C を省略。原本は _local/legacy-src/…）

Names can remain UTF-16LE to match ACNL internally and avoid runtime UTF-8 conversion ambiguity.

Icon filename is deterministic from ID, so no icon filename table is necessary.

## Loading policy

Avoid SD I/O on every render call.

Recommended lifecycle:

1. plugin initialization / title-ready phase:
   - validate build/version;
   - read manifest and name table;
   - validate files/CRC;
   - prepare fixed basename table.

2. icon resources:
   - first version: lazily load an icon once, then retain the BCLIM buffer for the rest of the game session;
   - never free/evict until exact NintendoWare pointer lifetime is proven;
   - missing/corrupt icon falls through to stock `icn_000`.

3. names:
   - preload all 251 names; memory footprint is small;
   - resolver hook performs no file I/O.

No hot reload in the first implementation. Game/UI objects may retain pointers into BCLIM data. Reload should only be added after texture/resource lifetime is understood.

## Loose files vs one custom pack

During development, loose BCLIMs are preferable:
- easy replacement;
- easy ID inspection;
- no custom packer required.

For release, if SD/FAT open overhead becomes measurable, combine assets into one plugin-owned pack, not necessarily a NintendoWare `.arc`.

Example:

```text
items.pack
  header
  0xFB-entry icon offset/size table
  0xFB-entry name offset/length table
  UTF-16 name blob
  BCLIM blobs
```

Because the 3GX owns the reader, a small versioned custom format is safer than reproducing a game archive format.

## Fallback / safety

- Apply only when `(itemId & 0x7FFF) <= 0xFA`.
- Preserve all high-bit item flags by using the masked ID only for display selection.
- If custom data is absent, return stock behavior.
- If one icon is absent/corrupt, use stock `icn_000` rather than crashing.
- If one name is absent, keep stock `???` or a plugin-defined placeholder.
- Never perform file writes from display hooks.
- Keep all hook-side data read-only after initialization.

## Why this is preferable

Compared with a custom replacement .arc:
- no need to reverse/rebuild the stock archive format first;
- no risk of dropping required stock resources;
- no need to patch multiple stock archives just to make one low-ID icon available;
- clean per-ID ownership;
- resources can be changed without rebuilding the 3GX;
- future normal-ID overrides can use the same overlay namespace.

## Next reverse-engineering steps before coding

1. Resolve exact ABI/ownership of `ArcResourceAccessor_GetResource @ 0x4B6D94`.
2. Determine whether BCLIM memory must remain live after texture creation.
3. Resolve the safest direct `script::Phrase` assignment helper for `ItemName_ResolvePhrase`.
4. Test one ID only (e.g. 0x000) before enabling the full 0xFB table.
