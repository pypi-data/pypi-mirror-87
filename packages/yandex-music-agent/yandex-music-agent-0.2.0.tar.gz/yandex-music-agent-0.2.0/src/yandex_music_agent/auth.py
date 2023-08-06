import urllib
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar, Cookie
from http.cookies import BaseCookie
from typing import Iterable
from urllib import parse

from yandex_music_agent.common.form import FormParser
from yandex_music_agent.data import YandexCookie


class AuthException(Exception):
    pass


def resolve_cookie(login: str, password: str) -> YandexCookie:
    cookies_jar = CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookies_jar),
        urllib.request.HTTPRedirectHandler(),
    )
    response = opener.open("https://passport.yandex.ru")
    for form_data in (
            {"login": login},
            {"login": login, "passwd": password},
    ):
        doc = response.read()
        parser = FormParser()
        parser.feed(doc.decode("utf-8"))
        parser.close()
        parser.params.update(form_data)
        response = opener.open(parser.url or response.url, urllib.parse.urlencode(parser.params).encode("utf-8"))
    cookie = YandexCookie({item.name: item.value for item in cookies_jar if item.domain == ".yandex.ru"})
    if not cookie:
        raise AuthException(f"Invalid credentials: {login}")
    return cookie


def _build_cookies(source: BaseCookie, domain: str) -> Iterable[Cookie]:
    for name in source:
        value = source.get(name).value
        yield Cookie(version=0, name=name, value=value,
                     port=None, port_specified=False,
                     domain=domain, domain_specified=True, domain_initial_dot=True,
                     path="/", path_specified=True,
                     secure=True,
                     expires=None,
                     discard=False,
                     comment=None,
                     comment_url=None,
                     rest={})


def validate_cookie(cookie: YandexCookie) -> bool:
    cookies_jar = CookieJar()
    for item in _build_cookies(cookie, ".yandex.ru"):
        cookies_jar.set_cookie(item)
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookies_jar),
        urllib.request.HTTPRedirectHandler(),
    )
    response = opener.open("https://passport.yandex.ru")
    _, _, path, _, _, _ = parse.urlparse(response.url)
    if path == "/profile":
        return True
    elif path == "/auth":
        return False
    else:
        raise ValueError(f"Unsupported response path: {path}")
