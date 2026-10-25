#!/usr/bin/env python3
"""Tag stories from the seven-column TSV export."""
import csv
from html import escape
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORDS = re.compile(r'[^\W_]+(?:[-–][^\W_]+)*', re.UNICODE)


def distance(left, right):
    previous = list(range(len(right) + 1))
    for i, a in enumerate(left, 1):
        current = [i]
        for j, b in enumerate(right, 1):
            current.append(min(current[-1] + 1, previous[j] + 1,
                               previous[j - 1] + (a != b)))
        previous = current
    return previous[-1]


def main():
    names = {}
    for item in yaml.safe_load((ROOT / 'src/key_list.yaml').read_text(encoding='utf-8-sig')):
        key = item['key']
        for name in [key['name'], *re.split('[,;]', key['name'])]:
            names[name.strip().casefold()] = key['id']
    stories = []
    with (ROOT / 'src/stories.csv').open(encoding='utf-8-sig', newline='') as source:
        reader = csv.reader(source, delimiter='\t')
        for row_number, row in enumerate(reader, 1):
            line_number = reader.line_num
            if len(row) != 7:
                raise ValueError(f'Line {line_number}: expected 7 columns')
            story = row[-1]
            words = list(WORDS.finditer(story))
            candidates = []
            for name in dict.fromkeys(value.strip() for value in row[:5]):
                if not name or name.endswith('*'):
                    continue
                if '/' in name:
                    print(f'Line {line_number}, row {row_number}: {name}: key alias')
                    continue
                key_id = names.get(name.casefold())
                if key_id is None:
                    print(f'Line {line_number}, row {row_number}: {name}: unknown key')
                    continue
                size = len(list(WORDS.finditer(name)))
                matches = []
                for i in range(len(words) - size + 1):
                    start, end = words[i].start(), words[i + size - 1].end()
                    found = story[start:end]
                    score = distance(name.casefold(), found.casefold())
                    if score <= 3:
                        matches.append((score, start, end, key_id))
                if matches:
                    best = min(match[0] for match in matches)
                    candidates.extend(match for match in matches if match[0] == best)
                else:
                    print(f'Line {line_number}, row {row_number}: {name}: not found')
            spans = []
            for score, start, end, key_id in sorted(candidates, key=lambda m: (m[0], -(m[2] - m[1]), m[1])):
                if not any(start < b and end > a for a, b, _ in spans):
                    spans.append((start, end, key_id))

            def meaning_tags(text):
                return WORDS.sub(lambda m: '<m>' + m[0] + '</m>' if m[0].isupper() else m[0], escape(text))

            parts = []
            offset = 0
            for start, end, key_id in sorted(spans):
                parts.append(meaning_tags(story[offset:start]))
                parts.append(f'<k id="{escape(key_id, quote=True)}">{meaning_tags(story[start:end])}</k>')
                offset = end
            parts.append(meaning_tags(story[offset:]))
            stories.append(''.join(parts))
    output = ROOT / 'src/stories_processed.txt'
    output.write_text('\n\n'.join(stories) + '\n', encoding='utf-8')
    print(f'Wrote {len(stories)} stories to {output}')


if __name__ == '__main__':
    main()
