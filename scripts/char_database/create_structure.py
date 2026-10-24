#!/usr/bin/env python3
"""Export once and radical decompositions separated by a double tab."""

import argparse
import csv
import io
from pathlib import Path

from hanzipy.decomposer import HanziDecomposer

ROOT = Path(__file__).resolve().parents[2]


def generate_structure(source: Path) -> tuple[str, int]:
    decomposer = HanziDecomposer()
    output = io.StringIO(newline='')
    writer = csv.writer(output, delimiter='\t', lineterminator='\n')
    seen = set()
    with source.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        column = 'УПРОЩЕННЫЙ иероглиф'
        if column not in (reader.fieldnames or []):
            raise ValueError(f'Missing CSV column: {column}')
        for row in reader:
            character = row[column].strip()
            if not character or character in seen:
                continue
            seen.add(character)
            result = decomposer.decompose(character)
            once = result.get('once', []) if isinstance(result, dict) else []
            radical = result.get('radical', []) if isinstance(result, dict) else []
            # Preserve unknown component positions without inventing a radical.
            once = ['□' if part == 'No glyph available' else part for part in once]
            radical = ['□' if part == 'No glyph available' else part for part in radical]
            writer.writerow([character, *once, '', *radical])
    return output.getvalue(), len(seen)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'src/mao.csv')
    parser.add_argument('--output', type=Path, default=ROOT / 'src/structure.txt')
    args = parser.parse_args()
    try:
        text, count = generate_structure(args.input)
        args.output.write_text(text, encoding='utf-8')
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f'Error: {error}\n')
    print(f'Generated {args.output} ({count} characters)')


if __name__ == '__main__':
    main()
