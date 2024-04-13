#!/usr/bin/env python3

import json, os, re
from lxml import etree
from bs4 import BeautifulSoup

verse_id_regex = re.compile('T(?P<verse_id>[0-9]+(-[0-9]+)?)[a-z]?')


def write_books(res, lang):
    if not os.path.exists(f"json/{lang}"):
        os.mkdir(f"json/{lang}")
    for book, _ in res.items():
        with open(f"json/{lang}/{book}.json", "w+") as outj:
            json.dump(dict(sorted(_.items())), outj, ensure_ascii=False, indent=4)





def compile_verses_for_page(page_soup, chapter):
    verses = {}
    title = None
    print("Chapter:", chapter)
    if chapter == "001":
        title = page_soup.find('div', {"class", "mt"})
        title2 = page_soup.find('div', {"class", "mt2"})
        if title2 is not None:
            title = title.get_text().strip() + ' ' + title2.get_text().strip()
        else:
            title = title.get_text().strip()

    current_verse = []
    current_verse_num = None
    head_count = 1
    for i, verse_div in enumerate(page_soup.find_all('div', {'class': ['txs', 's']})):
        try:
            verse_num = re.match(verse_id_regex,
                                verse_div.attrs['id']).group('verse_id')
        except Exception as e:
            verses[f"head_{head_count}"] = verse_div.get_text().strip()
            head_count += 1
            continue

        verse_num_span = verse_div.find('span', {'class': 'v'})
        if verse_num_span is not None:
            _ = verse_num_span.extract()

        verse_text = verse_div.text.replace(u'\xa0', u' ')
        verse_text = [_.strip() for _ in verse_text.splitlines()]
        verse_text = ' '.join([_.strip() for _ in verse_text if _ != ''])

        if current_verse_num is None:
            current_verse.append(verse_text)
            current_verse_num = verse_num

        elif verse_num == current_verse_num:
            current_verse.append(verse_text)

        else:
            verses["{:0>{}}".format(current_verse_num, 3)] = ' '.join(current_verse)
            current_verse = [verse_text]
            current_verse_num = verse_num
    return verses, title




def parse_page(doc, res, lang):
    book = doc.split('-')[1]
    chapter = doc.split('-')[2][:-5]
    with open(f"html/{lang}/{doc}") as inf:
        page = inf.read()
        page_soup = BeautifulSoup(page, "lxml")
        verses, title = compile_verses_for_page(page_soup, chapter)
        if title:
            if book not in res:
                res[book] = {}
            res[book]["000"] = title
        if verses:
            if book not in res:
                res[book] = {}
            res[book][chapter] = verses
    return res




def main():
    langs = ["nuz", "nsu", "nhx"]
    for lang in langs:
        docs = os.listdir(f"html/{lang}")
        if not os.path.exists(f"json/{lang}"):
            os.mkdir(f"json/{lang}")
        res = {}
        for doc in docs:
            res = parse_page(doc, res, lang)
        write_books(res, lang)




if __name__ == '__main__':
    main()
