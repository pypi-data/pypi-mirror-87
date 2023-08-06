from http.cookies import SimpleCookie
from typing import NamedTuple


class YandexCookie(SimpleCookie):

    @property
    def uid(self) -> str:
        return self.get("yandexuid").value

    @property
    def login(self) -> str:
        return self.get("yandex_login").value

    def __bool__(self) -> bool:
        return self.get("yandex_login") is not None

    def __str__(self) -> str:
        return "; ".join(f"{k}={str(v.value)}" for k, v in sorted(self.items()))


class Artist(NamedTuple):
    id: int
    title: str
    avatar: str


class Album(NamedTuple):
    id: int
    title: str
    year: int
    cover: str


class Track(NamedTuple):
    album_id: int
    id: int
    title: str
    num: int
