#!/usr/bin/env python3
"""Generate site/hanzi.html with an embedded character index and key metadata."""
import argparse
import csv
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def embedded_json(value):
    return json.dumps(value, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--index', type=Path, default=ROOT / 'cdb/index.json')
    parser.add_argument('--keys', type=Path, default=ROOT / 'src/key_list.yaml')
    parser.add_argument('--csv', type=Path, default=ROOT / 'src/mao.csv',
                        help='CSV supplying character navigation order')
    parser.add_argument('--output', type=Path, default=ROOT / 'site' / 'hanzi.html')
    args = parser.parse_args()
    try:
        index = json.loads(args.index.read_text(encoding='utf-8'))
        with args.csv.open(encoding='utf-8-sig', newline='') as source:
            characters = list(dict.fromkeys(
                row['УПРОЩЕННЫЙ иероглиф'].strip() for row in csv.DictReader(source)
                if row['УПРОЩЕННЫЙ иероглиф'].strip()))
        keys = {item['key']['id']: {field: item['key'][field] for field in ('name', 'sym')}
                for item in yaml.safe_load(args.keys.read_text(encoding='utf-8'))}
        template = Path(__file__).with_name('template.html').read_text(encoding='utf-8')
        page = template.replace('{{INDEX}}', embedded_json(index)).replace('{{KEYS}}', embedded_json(keys))
        page = page.replace('{{CHARACTERS}}', embedded_json(characters))
        args.output.write_text(page, encoding='utf-8')
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        parser.exit(1, f'Error: {error}\n')
    print(f'Generated {args.output} ({len(index)} indexed characters)')


if __name__ == '__main__':
    main()
