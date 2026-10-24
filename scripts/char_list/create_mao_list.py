#!/usr/bin/env python3
"""Generate a static square grid of character links from mao.csv."""
import argparse
import csv
from html import escape
from math import ceil, sqrt
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]


def read_characters(path: Path) -> list[str]:
    with path.open(encoding='utf-8-sig', newline='') as source:
        reader = csv.DictReader(source)
        header = 'УПРОЩЕННЫЙ иероглиф'
        if header not in (reader.fieldnames or []):
            raise ValueError(f'Missing CSV column: {header}')
        return list(dict.fromkeys(row[header].strip() for row in reader if row[header].strip()))


def render_page(characters: list[str]) -> str:
    columns = max(1, ceil(sqrt(len(characters))))
    links = '\n'.join(
        f'      <a href="hanzi.html?h={quote(char, safe="")}" aria-label="{escape(char)}">{escape(char)}</a>'
        for char in characters)
    return f'''<!doctype html>
<html lang="ru" data-bs-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Список иероглифов — МАО</title>
  <link rel="icon" href="../pagoda.png">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  <style>
    main {{ max-width: 1500px; margin: auto; }}
    .character-grid {{ display: grid; grid-template-columns: repeat({columns}, minmax(0, 1fr)); gap: 2px; }}
    .character-grid a {{ display: grid; place-items: center; aspect-ratio: 1; text-decoration: none; font-size: clamp(.9rem, 1.4vw, 1.4rem); background: var(--bs-tertiary-bg); border-radius: 2px; }}
    .character-grid a:hover, .character-grid a:focus-visible {{ background: var(--bs-primary); color: white; outline: 2px solid var(--bs-emphasis-color); outline-offset: 1px; }}
    @media (max-width: 1100px) {{ .character-grid {{ grid-template-columns: repeat(24, minmax(0, 1fr)); }} .character-grid a {{ font-size: 1.25rem; }} }}
    @media (max-width: 600px) {{ .character-grid {{ grid-template-columns: repeat(12, minmax(0, 1fr)); }} .character-grid a {{ font-size: 1.1rem; }} }}
  </style>
</head>
<body>
  <main class="px-3 py-4">
    <nav aria-label="Навигация" class="mb-4"><a href="../">МАО</a> / Иероглифы</nav>
    <h1>Список иероглифов</h1>
    <p class="text-body-secondary">{len(characters)} иероглифов в порядке mao.csv. Выберите иероглиф, чтобы открыть его страницу.</p>
    <nav class="character-grid" aria-label="Список иероглифов" lang="zh-Hans">
{links}
    </nav>
  </main>
</body>
</html>
'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'src/mao.csv')
    parser.add_argument('--output', type=Path, default=ROOT / 'site/char_list.html')
    parser.add_argument('--limit', type=int, default=1000,
                        help='Maximum number of unique characters (default: 1000)')
    args = parser.parse_args()
    if args.limit < 0:
        parser.error('--limit must be zero or greater')
    try:
        characters = read_characters(args.input)[:args.limit]
        args.output.write_text(render_page(characters), encoding='utf-8')
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f'Error: {error}\n')
    print(f'Generated {args.output} ({len(characters)} characters)')


if __name__ == '__main__':
    main()
