#!/usr/bin/env python3
"""Generate the static radical table. Requires PyYAML (pip install PyYAML)."""

import argparse
from html import escape
from pathlib import Path
from urllib.parse import quote

import yaml


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent.parent


def image(filename: str, alt: str, *, radical: bool = False) -> str:
    directory = "../images/keys/sym/" if radical else "../images/keys/"
    src = directory + quote(filename, safe="/")
    width = ' width="40"' if radical else ''
    return (f'<img src="{escape(src)}" alt="{escape(alt)}"'
            f'{width} loading="lazy">')


def render_rows(data: list) -> str:
    if not isinstance(data, list):
        raise ValueError("Expected a YAML list of key records")
    rows = []
    seen = set()
    for number, record in enumerate(data, 1):
        try:
            key = record['key']
            key_id = key['id']
            if not isinstance(key_id, str) or not key_id or key_id in seen:
                raise ValueError("id must be a unique, nonempty string")
            seen.add(key_id)
            name = escape(key['name'])
            symbols = []
            if not isinstance(key['sym'], list) or not key['sym']:
                raise ValueError("sym must be a nonempty list")
            for index, symbol in enumerate(key['sym']):
                char = symbol['char']
                classes = 'fs-1 me-1' if index == 0 else 'fs-2 text-body-secondary me-1'
                lang = f' lang="{escape(char["lang"])}"' if 'lang' in char else ''
                if 'rad' in char:
                    content = escape(char['rad'])
                else:
                    content = image(char['rad_img'], f"Радикал: {key['name']}", radical=True)
                symbols.append(f'<span class="{classes}"{lang}>{content}</span>')
            images = key['images']
            if isinstance(images, str):
                images = [images]
            if not isinstance(images, list) or not images:
                raise ValueError("images must be a filename or a nonempty list")
            pictures = ''.join(f'<div>{image(filename, key["name"])}</div>' for filename in images)
            rows.append(
                f'    <tr id="{escape(key_id)}">\n'
                f'      <th scope="row">{number}</th>\n'
                f'      <td class="key-symbols">{"".join(symbols)}</td>\n'
                f'      <td class="key-images">{pictures}</td>\n'
                f'      <td><div>{name}</div><div>{escape(key.get("text") or "")}</div>'
                f'<div class="example">{escape(key.get("examples") or "")}</div></td>\n'
                '    </tr>'
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"Invalid key record {number}: {error}") from error
    return '\n'.join(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'src/key_list.yaml')
    parser.add_argument('--output', type=Path, default=ROOT / 'site/key_list.html',
                        help='Output page; image links assume the site/ directory')
    parser.add_argument('--template', type=Path, default=SCRIPT_DIR / 'template.html')
    args = parser.parse_args()
    try:
        data = yaml.safe_load(args.input.read_text(encoding='utf-8'))
        rows = render_rows(data)
        template = args.template.read_text(encoding='utf-8')
        if template.count('{{ rows }}') != 1:
            raise ValueError('Template must contain exactly one {{ rows }} placeholder')
        page = template.replace('{{ rows }}', rows)
        args.output.write_text(page, encoding='utf-8')
    except (OSError, ValueError, yaml.YAMLError) as error:
        parser.exit(1, f'Error: {error}\n')
    print(f'Generated {args.output} ({len(data)} keys)')


if __name__ == '__main__':
    main()
