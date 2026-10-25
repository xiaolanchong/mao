#!/usr/bin/env python3
"""Convert mao.csv to one UTF-8 JSON file per character for AJAX requests."""

import argparse
import csv
import json
from html.parser import HTMLParser
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent


def available_videos(mapping: Path | None = None) -> dict[str, str]:
    videos = read_videos(mapping)
    directory = SCRIPT_DIR.parent.parent / 'video' / 'mnemonics'
    for path in sorted(directory.rglob('*.mp4')):
        if path.is_file():
            videos[path.stem] = path.relative_to(SCRIPT_DIR.parent.parent).as_posix()
    return videos


def refresh_videos(directory: Path, videos: dict[str, str]) -> int:
    count = 0
    for path in sorted(directory.glob('[0-9][0-9][0-9][0-9]/*.json')):
        record = json.loads(path.read_text(encoding='utf-8'))
        video = videos.get(record['character'])
        if record.get('video') != video:
            record['video'] = video
            path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            count += 1
    return count


def refresh_structures(directory: Path, records: list[dict]) -> int:
    """Update structure from CSV, preserving other existing fields."""
    structures = {}
    for record in records:
        structures.setdefault(record['character'], record['structure'])
    updates = []
    for path in sorted(directory.glob('[0-9][0-9][0-9][0-9]/*.json')):
        record = json.loads(path.read_text(encoding='utf-8'))
        character = record['character']
        if character not in structures:
            raise ValueError(f'{path}: character {character!r} absent from CSV')
        record['structure'] = structures[character]
        updates.append((path, json.dumps(record, ensure_ascii=False, indent=2) + '\n'))
    for path, content in updates:
        path.write_text(content, encoding='utf-8')
    return len(updates)


def read_key_ids(path: Path) -> set[str]:
    data = yaml.safe_load(path.read_text(encoding='utf-8-sig'))
    if not isinstance(data, list):
        raise ValueError(f'{path}: expected a list of key records')
    ids = set()
    for number, record in enumerate(data, 1):
        key = record.get('key') if isinstance(record, dict) else None
        key_id = key.get('id') if isinstance(key, dict) else None
        if not isinstance(key_id, str) or not key_id:
            raise ValueError(f'{path}: key record {number} requires a nonempty id')
        if key_id in ids:
            raise ValueError(f'{path}: duplicate key id {key_id!r}')
        ids.add(key_id)
    return ids


def read_key_names(path: Path) -> set[str]:
    names = set()
    for item in yaml.safe_load(path.read_text(encoding='utf-8-sig')):
        name = item['key']['name']
        names.add(name.strip().casefold())
        for alias in name.replace(';', ',').split(','):
            if alias.strip():
                names.add(alias.strip().casefold())
    return names


def validate_key_ids(records, key_ids: set[str], key_names: set[str] | None = None) -> None:
    errors = []
    for record in records:
        if key_names is not None:
            for column, value in enumerate(record.get('_key_values', []), 1):
                if not value:
                    continue
                if value.endswith('*'):
                    if not value.rstrip('*').strip():
                        errors.append(f'{record["character"]} (CSV number {record["_number"]}), '
                                      f'Key {column}: empty ad hoc key')
                else:
                    target = value.partition('/')[2].strip() if '/' in value else value
                    if target.casefold() not in key_names and target not in key_ids:
                        errors.append(f'{record["character"]} (CSV number {record["_number"]}), '
                                      f'Key {column}: unknown key {target!r}')
        unknown = sorted({segment[2] for segment in record['mnemonic']
                          if segment[1] == 0 and segment[2] not in key_ids})
        if unknown:
            errors.append(f'{record["character"]} (CSV number {record["_number"]}): '
                          + ', '.join(repr(key_id) for key_id in unknown))
    if errors:
        raise ValueError('Key validation failed:\n' + '\n'.join(errors))


class MnemonicParser(HTMLParser):
    """Extract typed text segments while preserving text and key IDs."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.segments = []
        self.active = None

    def handle_starttag(self, tag, attrs):
        if tag not in ('k', 'm', 'c') or self.active is not None:
            raise ValueError(f'Unexpected mnemonic tag: <{tag}>')
        if tag in ('k', 'c'):
            key_id = dict(attrs).get('id')
            if not key_id:
                raise ValueError(f'Mnemonic <{tag}> tag requires an id')
            self.active = ['', 0 if tag == 'k' else 3, key_id]
        else:
            self.active = ['', 1]

    def handle_endtag(self, tag):
        expected = {0: 'k', 1: 'm', 3: 'c'}.get(self.active[1]) if self.active else None
        if self.active is None or tag != expected:
            raise ValueError(f'Unexpected mnemonic closing tag: </{tag}>')
        if self.active[0]:
            self.segments.append(self.active)
        self.active = None

    def handle_data(self, text):
        if not text:
            return
        if self.active is not None:
            self.active[0] += text
        elif self.segments and self.segments[-1][1] == 2:
            self.segments[-1][0] += text
        else:
            self.segments.append([text, 2])


def parse_mnemonic(text: str) -> list[list]:
    parser = MnemonicParser()
    parser.feed(text.strip())
    parser.close()
    if parser.active is not None:
        raise ValueError('Unclosed mnemonic tag')
    return parser.segments


def read_videos(path: Path | None) -> dict[str, str]:
    """Read CHARACTER PATH lines; paths may contain spaces."""
    if path is None:
        return {}
    videos = {}
    for number, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f'{path}:{number}: expected character and video path')
        character, video = parts
        if character in videos:
            raise ValueError(f'{path}:{number}: duplicate video for {character}')
        videos[character] = video
    return videos


def parse_component(value: str) -> dict:
    value = value.strip()
    ad_hoc = value.endswith('*')
    if ad_hoc:
        return {'key': value.rstrip('*').strip(), 'ad_hoc': True, 'position': None}
    name, separator, target = value.partition('/')
    component = {'key': name.strip(), 'ad_hoc': False, 'position': None}
    if separator:
        component['target'] = target.strip()
    return component


def read_characters(path: Path, videos: dict[str, str]) -> list[dict]:
    records = []
    with path.open(encoding='utf-8-sig', newline='') as source:
        reader = csv.reader(source)
        headers = next(reader, [])
        if 'MAO story' not in headers:
            raise ValueError(f'{path}: missing column \'MAO story\'')
        mnemonic_column = headers.index('MAO story')
        component_columns = []
        for number in range(1, 6):
            header = f'Key {number}'
            if header not in headers:
                raise ValueError(f'{path}: missing column {header!r}')
            component_columns.append(headers.index(header))
        structure_columns = []
        for number in range(1, 6):
            header = f'Comp{number}'
            if header not in headers:
                raise ValueError(f'{path}: missing column {header!r}')
            structure_columns.append(headers.index(header))
        for row in reader:
            if not row or not any(value.strip() for value in row):
                continue
            if len(row) < max(11, mnemonic_column + 1, max(component_columns + structure_columns) + 1):
                raise ValueError(f'{path}:{reader.line_num}: missing required columns')
            character = row[2].strip()
            if not character:
                raise ValueError(f'{path}:{reader.line_num}: empty character')
            number = int(row[0])
            if number < 1:
                raise ValueError(f'{path}:{reader.line_num}: number must be positive')
            records.append({
                '_number': number,
                '_key_values': [row[column].strip() for column in component_columns],
                'character': character,
                'pinyin': row[1].split(),
                'meaning': [part.strip() for part in row[4].split('\n')
                            if part.strip()],
                'components': [parse_component(value)
                               for column in component_columns
                               if (value := row[column]).strip()],
                'structure': {'once': [row[column].strip() for column in structure_columns
                                       if row[column].strip()], 'radical': []},
                'mnemonic': parse_mnemonic(row[mnemonic_column]),
                'video': videos.get(character),
            })
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path,
                        default=SCRIPT_DIR.parent.parent / 'src' / 'mao.csv')
    parser.add_argument('--output', type=Path,
                        default=SCRIPT_DIR.parent.parent / 'cdb',
                        help='Directory for CHARACTER.json files')
    parser.add_argument('--videos', type=Path,
                        help='UTF-8 text file containing CHARACTER PATH lines')
    parser.add_argument('--keys', type=Path,
                        default=SCRIPT_DIR.parent.parent / 'src' / 'key_list.yaml',
                        help='YAML database of valid mnemonic key IDs')
    parser.add_argument('--limit', type=int, default=600,
                        help='Maximum number of unique character files to generate (default: 600)')
    parser.add_argument('--refresh-structure', action='store_true',
                        help='Update structure in all existing NNNN/*.json files only')
    parser.add_argument('--refresh-videos', action='store_true',
                        help='Update only video paths in existing character files')
    args = parser.parse_args()
    if args.limit is not None and args.limit < 0:
        parser.error('--limit must be zero or greater')
    try:
        if args.refresh_videos:
            count = refresh_videos(args.output, available_videos(args.videos))
            print(f'Updated video fields in {count} character files')
            return
        if args.refresh_structure:
            count = refresh_structures(args.output, read_characters(args.input, {}))
            print(f'Updated structure in {count} character files in {args.output}')
            return
        key_ids = read_key_ids(args.keys)
        records = read_characters(args.input, available_videos(args.videos))
        characters = {}
        duplicates = 0
        for record in records:
            if args.limit is not None and len(characters) >= args.limit:
                break
            character = record['character']
            if character in ('.', '..') or any(c in character for c in '/\\\0'):
                raise ValueError(f'Character cannot be used as a filename: {character!r}')
            if character in characters:
                duplicates += 1
                continue  # Keep the first CSV record for each character.
            characters[character] = record
        validate_key_ids(characters.values(), key_ids, read_key_names(args.keys))
        args.output.mkdir(parents=True, exist_ok=True)
        index = {}
        for character, record in characters.items():
            record = record.copy()
            number = record.pop('_number')
            record.pop('_key_values', None)
            directory = f'{max(1, number // 100 * 100):04d}'
            destination = args.output / directory
            destination.mkdir(exist_ok=True)
            result = json.dumps(record, ensure_ascii=False, indent=2) + '\n'
            (destination / f'{character}.json').write_text(result, encoding='utf-8')
            index[character] = directory
        (args.output / 'index.json').write_text(
            json.dumps(index, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    except (OSError, UnicodeError, ValueError, csv.Error, yaml.YAMLError) as error:
        parser.exit(1, f'Error: {error}\n')
    print(f'Generated {len(characters)} character files in {args.output}')
    if duplicates:
        print(f'Skipped {duplicates} duplicate CSV records (kept first occurrence)')


if __name__ == '__main__':
    main()
