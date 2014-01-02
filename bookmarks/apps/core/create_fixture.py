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


def generate_links(start=START, items=ITEMS):
    links = []
    zones = ['com', 'ru', 'gov', 'su']
    k = start + 1
    while k <= items:
        id = k
        domain = ''.join([l for i in range(random.randint(4, 10))
                          for l in random.choice(letters)]).lower()
        zone = random.choice(zones).lower()
        links.append(LINK.format(**locals()).replace('[', '{').
                     replace(']', '}'))
        k += 1
    return links


def generate_bookmarks(start=START, items=ITEMS):
    bookmarks = []
    links = range(start + 1, items + 1)
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


def generate_tags(start=START, items=ITEMS):
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


def dump_fixture_data(links, bookmarks, tags, filename):
    res = []
    res.append(',\n'.join(links))
    res.append(',\n'.join(bookmarks))
    res.append(',\n'.join(tags))
    res = '[' + ',\n'.join(res)
    res += ']'
    print res
    json.dump(json.loads(res), open(filename, 'w'), indent=4)


def tag_cloud():
    # Tag foo will have 10 bookmarks
    # Tag bar will have 5 bookmarks
    # Tag buz will have 2 bookmarks
    # total 17 bookmarks
    values = {'start': 1, 'items': 18}
    links = generate_links(**values)
    bkms = generate_bookmarks(**values)
    k = 1
    tags = []
    bookmark_lb = lambda x: ',\n            '.join(map(str, x))
    for tag in ['foo', 'bar', 'buz']:
        t_id = k
        tag_name = tag
        if tag == 'foo':
            bookmarks = bookmark_lb(range(1, 11))
        elif tag == 'bar':
            bookmarks = bookmark_lb(range(11, 16))
        elif tag == 'buz':
            bookmarks = bookmark_lb(range(16, 18))
        tags.append(TAG.format(**locals()).
                    replace('[', '{').
                    replace('[', '{').
                    replace(']', '}').
                    replace('\\', '[').
                    replace('/', ']'))
        k += 1
    dump_fixture_data(links, bkms, tags, 'tag_cloud_data.json')



if __name__ == '__main__':
    tag_cloud()



