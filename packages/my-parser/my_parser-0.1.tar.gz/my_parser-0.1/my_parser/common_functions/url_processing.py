import re
from functools import lru_cache
from urllib.parse import urlparse


@lru_cache(maxsize=None)
def check_url(url):
    """Проверяет, что url валиден"""
    check_regex = re.compile(r"https{,1}://")
    if not isinstance(url, str):
        return False
    if check_regex.search(url):
        return True
    return False


@lru_cache(maxsize=None)
def extract_domain(url):
    """Извлекает домен из ссылки"""
    return urlparse(url).netloc


@lru_cache(maxsize=None)
def is_own_url(url, site):
    """Проверяет ведет ли ссылка на текущий сайт"""
    if not check_url(url):
        return None
    domain = extract_domain(url)
    if domain == site:
        return True
    return False


@lru_cache(maxsize=None)
def not_own_url(url, site):
    """Проверяет ведет ли ссылка на другой сайт"""
    result = is_own_url(url, site)
    if result or result is None:
        return False
    return True