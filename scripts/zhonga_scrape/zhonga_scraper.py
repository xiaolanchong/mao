import time

import requests
import urllib.parse
from bs4 import BeautifulSoup


def parse():
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the links on the page (example: extracting all anchor tags)
    links = soup.find_all('a')

    # Loop through the links and print their href attributes
    for link in links:
        href = link.get('href')
        if href:
            print(href)


def get_page(hanzi: str, index: int):
    # URL of the page you want to scrape
    search_url = f'https://www.zhonga.ru/search?q={hanzi}'
    # search_url = urllib.parse.quote(search_url)

    # Send a GET request to the website
    response = requests.get(search_url)

    # Check if the request was successful
    if response.status_code == 200:
        # parse()
        with open(f'hanzi/new/{index:04}-{hanzi}.html', encoding='utf-8', mode='w') as f:
            f.write(response.content.decode())
        print(f"Success: {hanzi}, {index}")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}, sym: {hanzi}")


def get_line(line_number, line_start = 0):
    with open('jun_da_3000.txt', encoding='utf8') as f:
        all_lines = f.readlines()
        hanzi_start_index = line_number * len(all_lines[0].rstrip('\n')) + line_start
        return all_lines[line_number][line_start:].rstrip('\n'), hanzi_start_index


glob_line_number = 54
line_start = 0


for loc_line_number in range(glob_line_number, 120):
    line, start_index = get_line(loc_line_number, line_start)

    for index, sym in enumerate(line[line_start:]):
        total_index = start_index + index
        get_page(sym, total_index)
        time.sleep(10)
