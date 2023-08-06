import json
import os

from my_parser.parsers.anchor_text_parser import get_anchor_text
from my_parser.parsers.external_link_parser import extract_external_urls
from my_parser.parsers.internal_link_parser import extract_internal_urls

"""Тестируем результат работы всех parser-функций"""


def test():
    results = {}
    url = "https://devpractice.ru/python-modules-and-packages/"
    results[url] = {"anchor_texts": get_anchor_text(url)}
    results[url].update({"internal_url": extract_internal_urls(url)})
    results[url].update({"external_url": extract_external_urls(url)})
    with open("results.json", "w") as file:
        json.dump(results, file, sort_keys=True, indent=4)


if __name__ == '__main__':
    test()
