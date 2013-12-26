# -*- coding: utf-8 -*-
import json
import random
from string import letters


LINK = '''[
    "pk": {id},
    "model": "bookmarks.link",
    "fields": [
        "url": "http://www.{domain}.{zone}/"
    ]
]'''

BOOKMARK = '''[
    "pk": {b_id},
    "model": "bookmarks.bookmark",
    "fields": [
        "folder": null,
        "title": "{title}",
        "link": {link},
        "user": 1,
        "favicon": "http://www.google.com/s2/favicons?domain_url=http://www.wnba.com/"
    ]
]'''

TAG = '''[
    "pk": {t_id},
    "model": "tags.tag",
    "fields": [
        "bookmarks": \\
            {bookmarks}
        /,
        "name": "{tag_name}"
    ]
]'''

START = 0
ITEMS = 25


def generate_links():
    links = []
    zones = ['com', 'ru', 'gov', 'su']
    k = START + 1
    while k <= ITEMS:
        id = k
        domain = ''.join([l for i in range(random.randint(4, 10))
                          for l in random.choice(letters)]).lower()
        zone = random.choice(zones).lower()
        links.append(LINK.format(**locals()).replace('[', '{').
                     replace(']', '}'))
        k += 1
    return links


def generate_bookmarks():
    bookmarks = []
    links = range(START + 1, ITEMS + 1)
    k = START + 1
    while k <= ITEMS:
        try:
            b_id = k
            title = ''.join([l for i in range(random.randint(1, 10))
                             for l in random.choice(letters)])
            link = links.pop(random.randint(0, len(links) - 1))
            bookmarks.append(BOOKMARK.format(**locals()).
                replace('[', '{').
                replace(']', '}'))
        except ValueError:
            pass
        k += 1
    return bookmarks


def generate_tags():
    count = random.randint(20, 100)
    tags = []
    bks = range(START + 1, ITEMS + 1)
    k = START + 1
    while k <= count:
        t_id = k
        tag_name = ''.join([l for i in range(random.randint(1, 10))
                           for l in random.choice(letters)]).lower()
        bookmarks = ',\n            '.join(sorted([str(random.choice(bks))
                                           for i in range(random.randint(1, 10))], reverse=True))
        tags.append(TAG.format(**locals()).
                    replace('[', '{').
                    replace('[', '{').
                    replace(']', '}').
                    replace('\\', '[').
                    replace('/', ']'))
        k += 1
    return tags


if __name__ == '__main__':
    res = []
    res.append(',\n'.join(generate_links()))
    res.append(',\n'.join(generate_bookmarks()))
    res.append(',\n'.join(generate_tags()))
    res = '[' + ',\n'.join(res)
    res += ']'
    json.dump(json.loads(res), open('bookmarks_paginated.json', 'w'), indent=4)


