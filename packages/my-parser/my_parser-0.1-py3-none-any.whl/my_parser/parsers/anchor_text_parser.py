from functools import partial

from my_parser.common_functions.request_processing import processing_url
from my_parser.common_functions.url_processing import not_own_url


def get_anchor_text(url):
    """Возвращает список, так называемых 'якорных' текстов.
    Текстов за которыми скрываются ссылки на другие сайты"""
    text_list = []
    domain, site = processing_url(url)
    if site is None:
        return []
    check_url = partial(not_own_url, site=domain)
    for link in site.find_all('a', {'href': check_url}):
        text_list.append(link.text)
    return text_list