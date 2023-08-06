import requests
from bs4 import BeautifulSoup

from my_parser.common_functions.url_processing import extract_domain


def processing_url(url):
    """Пытается получить контент сайта. Если попытка удачная,
    то возвращает объект BeautifullSoup, иначе None"""
    domain = extract_domain(url)
    try:
        response = requests.get(url)
    except Exception as e:
        print(e)
        return domain, None
    if response.ok:
        site = BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Запрос к url {url} вернул код ошибки: {response.status_code}")
        return domain, None
    return domain, site