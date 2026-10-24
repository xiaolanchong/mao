Run from any directory (Python 3.10+, PyYAML):

```sh
python3 -m pip install -r scripts/char_database/requirements.txt
python3 scripts/char_database/create_char_database.py
python3 scripts/char_database/create_char_database.py --videos path/to/videos.txt
python3 scripts/char_database/create_char_database.py --limit 10 --output /tmp/char_database_test
```

Defaults: input `src/mao.csv`, output directory `cdb/` at the site root.
Override with `--input` and `--output`. Explicit relative paths resolve from
the current working directory.

Use `--limit N` to generate only the first N unique characters in CSV order.
Omitting it generates 500 characters; `--limit 0` writes only an empty index. Negative
limits are rejected. Existing files in the output directory are retained, so
use a separate output directory for test runs.

Each character gets a JSON object in its own file, for example
`cdb/0001/一.json`. Directories use the number in CSV column 1:
1–99 → `0001`, 100–199 → `0100`, 200–299 → `0200`, and so on.
`cdb/index.json` maps each generated character to its directory, e.g.
`{"一": "0001"}`. The index covers only the current run.
Columns use the requested 1-based mapping:
character 3, pinyin 2 (array split on whitespace), meaning 5 (array split on
newlines, with whitespace trimmed and empty lines omitted).
Mnemonic text is read by header from `MAO story`.
The `mnemonic` array contains `[text, 0, key_id]` for `<k id="…">`,
`[text, 1]` for `<m>`, `[text, 2]` for ordinary text, and
`[text, 3, compound_id]` for `<c id="…">`. Compound IDs are preserved and
are not validated against the key database. Key IDs refer to
`src/key_list.yaml`. Spaces and punctuation within the story are preserved;
empty stories produce `[]`. Meaning definitions remain a separate array.
Before writing files, mnemonic key IDs in the selected characters are checked
against `src/key_list.yaml` (override with `--keys`). Unknown IDs stop generation
and are reported with their character and CSV number; existing output is retained.
Components are read by header from `Key 1` through `Key 5`,
in that order, omitting empty values. Commas and semicolons within meanings are preserved.
Component values are preserved as written, with `position: null` because no
position information is provided. The CSV header is skipped.

The optional UTF-8 video file contains one character and relative video path per
line, separated by whitespace. Blank lines are ignored; paths may contain spaces:

```text
想 videos/想.mp4
的 videos/de particle.mp4
```

Paths are preserved as supplied and should resolve relative to the consuming
HTML page. Missing video mappings produce `video: null`. Repeated characters
in the CSV use the first occurrence (the generator reports skipped duplicates).
Duplicate video mappings and
malformed records are reported as errors.

Example browser usage from a page in `site/`:

```js
const indexResponse = await fetch('../cdb/index.json');
if (!indexResponse.ok) throw new Error(`Index request failed: ${indexResponse.status}`);
const index = await indexResponse.json();
const char = '一';
if (!(char in index)) throw new Error(`Character unavailable: ${char}`);
const response = await fetch(`../cdb/${index[char]}/${encodeURIComponent(char)}.json`);
if (!response.ok) throw new Error(`Database request failed: ${response.status}`);
const character = await response.json();
```

Structure comes from the nonempty `Comp1`–`Comp5` CSV fields in order:

```json
"structure": {"once": ["白", "勹", "丶"], "radical": []}
```

The `radical` array remains empty because the CSV provides one decomposition
level. No automatic decomposition overrides the edited CSV values.
`--refresh-structure` updates only structure in all existing character files
from the same CSV, preserving other fields and the index.

Video files named `video/mnemonics/字.mp4` are automatically matched to characters
and stored as site-root-relative paths. These matches take precedence over
optional `--videos` mappings. Refresh only video fields in existing JSON with:

```sh
python3 scripts/char_database/create_char_database.py --refresh-videos
```

Unmatched characters receive `video: null` unless supplied by `--videos`.

`Key 1`–`Key 5` values are checked against key IDs or names in `key_list.yaml`
(case-insensitive for names, including comma/semicolon-separated aliases).
A trailing `*` marks an ad hoc key and bypasses lookup. JSON omits the trailing
asterisk and sets `ad_hoc: true`; the page displays it without a key-list link.
A bare `*` is invalid. Errors identify the character, CSV number and Key column.
