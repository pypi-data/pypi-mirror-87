from functools import partial

from my_parser.common_functions.request_processing import processing_url
from my_parser.common_functions.url_processing import not_own_url


def extract_external_urls(url):
    """Возвращает список всех ссылок ведущих за пределы сайта, который анализируется"""
    urls_list = []
    domain, site = processing_url(url)
    if site is None:
        return []
    check_url = partial(not_own_url, site=domain)
    for link in site.find_all('a', {'href': check_url}):
        urls_list.append(link['href'])
    return urls_list