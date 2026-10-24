Generate the character page in `site/` (requires Python 3.10+ and PyYAML):

```sh
python3 scripts/char_page/create_char_page.py
```

Open `/site/hanzi.html?h=想` on your HTTP server. The generator embeds `cdb/index.json`
and key names/symbols from `src/key_list.yaml`. Regenerate after either changes.
The page fetches only the selected `cdb/NNNN/字.json` at runtime.
Page behavior lives in `src/char_page.js`, loaded directly by the template.
The navigation band shows up to five previous and five next characters in
`src/mao.csv` order (override with `--csv`), keeping the first occurrence of
duplicates. The current character is highlighted; neighbors link to `?h=字`.
Characters without generated JSON still appear in CSV order and show the
existing unavailable message when opened. Regenerate after CSV order changes.
Use `--index`, `--keys`, or `--output` to override inputs/output; relative browser
links assume the generated page is in `site/`.

Meanings, components, typed mnemonic segments and video come from the JSON.
Pinyin numbers are converted to tone marks. Key segments link to the radical list;
meaning segments are highlighted, compound segments have a dotted underline.
Only `structure.once` is displayed, e.g. `亻 + 也`; radical decomposition is omitted.
Unavailable glyphs appear as `□`. Empty decompositions show an unavailable message.
Missing characters, stories and videos have explicit messages.

Video paths are relative to the site root (one directory above the HTML page). The database generator automatically finds `video/mnemonics/字.mp4`.
Refresh existing JSON video fields using `--refresh-videos`; the page does not read video.txt.
Serve over HTTP to allow fetch requests.
