import dataclasses
import typing

import jinja2
import csv
import re
from pathlib import Path


@dataclasses.dataclass
class MaoRecord:
    number: int
    pinyin: list[typing.Tuple[str, int]]
    hanzi: str
    meaning: str
    assoc: list[typing.Tuple[bool, str]]


def split_on_all_caps(text: str) -> list[str]:
    """
    Splits text into substrings separated by ALL-CAPS wos' / f'wenrds.
    Keeps the ALL-CAPS words as separate list elements.
    """
    # Regex: match words that are fully uppercase (A-Z only)
    tokens = re.split(r'(\b[А-Я]+\b)', text)

    # Clean up spaces and empties
    return [t.strip() for t in tokens if t.strip()]


def is_meaning_in_association(parts, idx):
    #  This is not a meaning
    if idx == 0 and len(parts[idx]) == 1:
        return False
    # Prefix. T is not a meaning
    if len(parts[idx]) == 1 and idx > 0:
        assert parts
        kkk = parts[idx-1].rstrip()
        if kkk and kkk[-1] in ('.', '!', '?') and len(kkk):
            return False
        return True
    return parts[idx][-1].isupper()


def generate_mao_list(env):
    mao_tmpl = env.get_template('mao.template.html')
    pages = [   (1,  499),  (500,  999),
             (1000, 1499), (1500, 1999),
             (2000, 2499), (2500, 2999),
             (3000, 3499), (3500, None)]

    NEUTRAL_TONE = 5

    def read_lists():
        with open(Path(__file__).parent / 'mao.csv', 'r', newline='', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            for idx, (start, end) in enumerate(pages):
                end = end + 1 if end else len(rows)
                records = []
                for row in rows[start:end]:
                    number, pinyin_joined, hanzi, _, meaning, _, _, _, _, _, _, association, *_ = row
                    number = int(number)
                    if len(pinyin_joined) == 0:
                        print(row)
                    pinyin = [(pinyin, int(pinyin[-1]) if len(pinyin) and pinyin[-1].isdigit() else NEUTRAL_TONE)
                              for pinyin in pinyin_joined.split(' ')]
                    meaning = meaning.replace('\n', ' ')
                    association = association.replace('\n', ' ')
                    parts = split_on_all_caps(association)
                    association = [(is_meaning_in_association(parts, str_idx), part)
                                   for str_idx, part in enumerate(parts)]
                    #print(number, pinyin, hanzi, meaning, association)
                    records.append(MaoRecord(number=number, pinyin=pinyin, hanzi=hanzi,
                                             meaning=meaning, assoc=association))
                   # if int(number) > 10:
                    #    return
                yield records

    pages = [l for l in read_lists()]
    for idx, record_list in enumerate(pages):
        #print(len(record_list))
        html = mao_tmpl.render(entities=record_list, current_page=idx, page_total=len(pages))
        with open(Path(__file__).parent / '..' / '..' / 'site' / f'mao-{idx+1}.html', mode='w', encoding='utf8') as file:
            file.write(html)
            #return


glob_env = jinja2.Environment(
    loader=jinja2.PackageLoader('create_dashboards', package_path=Path('template')),
    autoescape=jinja2.select_autoescape(['html', 'xml'])
)

generate_mao_list(glob_env)
