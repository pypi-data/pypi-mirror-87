import datetime
from hashlib import md5
from typing import List, Optional
from urllib import parse

import aiohttp
from bs4 import BeautifulSoup

from yandex_music_agent.common.headers import Headers
from yandex_music_agent.common.srcset import SrcSet
from yandex_music_agent.data import Artist, Album, Track, YandexCookie


def timestamp() -> int:
    return int(datetime.datetime.now().timestamp())


class YandexMusicApi:
    host = "music.yandex.ru"
    base_url = f"https://{host}"

    def __init__(self, cookie: YandexCookie):
        self.cookie = cookie
        self.headers = Headers(self.host, str(cookie))

    async def _request(self, end_point: str):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/{end_point}"
            async with session.request(method="GET", url=url) as response:
                assert response.status == 200
                return await response.read()

    def _extract_img_src(self, img_soup) -> Optional[str]:
        if "srcset" in img_soup.attrs:
            srcset = SrcSet.parse(img_soup.attrs["srcset"])
            return srcset.best.src

    async def get_favorite_artists(self, email: str = None) -> List[Artist]:
        if email is None:
            email = self.cookie.login
        body = await self._request(f"users/{email}/artists")
        soup = BeautifulSoup(body, "lxml")
        artists_soup = soup.find("div", class_="page-users__artists")
        if artists_soup is None:
            caption = soup.find("div", class_="page-users__caption")
            if caption:
                raise Exception(caption.contents[0])
        result = []
        for artist_soup in artists_soup.find_all("div", class_="artist"):
            title_soup = artist_soup.find("div", class_="artist__name")
            title = title_soup.attrs["title"]
            title_href_soup = title_soup.find("a")
            id_ = int(title_href_soup.attrs["href"].split("/")[-1])
            result.append(Artist(id_, title, None))
        return result

    async def get_artist(self, artist_id: int) -> Artist:
        body = await self._request(f"artist/{artist_id}")
        soup = BeautifulSoup(body, "lxml")
        artist_soup = soup.find("div", class_="page-artist")
        title_soup = artist_soup.find("h1", class_="page-artist__title")
        title = title_soup.contents[0]
        avatar_soup = soup.find("div", class_="artist-pics").find("img")
        avatar = self._extract_img_src(avatar_soup)
        return Artist(artist_id, title, avatar)

    async def get_artist_albums(self, artist_id: int) -> List[Album]:
        body = await self._request(f"artist/{artist_id}/albums")
        soup = BeautifulSoup(body, "lxml")
        albums_soup = soup.find("div", class_="page-artist__albums")
        result = []
        for album_soup in albums_soup.find_all("div", class_="album"):
            title_soup = album_soup.find("div", class_="album__title")
            title = title_soup.attrs["title"]
            title_href_soup = title_soup.find("a")
            id_ = int(title_href_soup.attrs["href"].split("/")[-1])
            year_soup = album_soup.find("div", class_="album__year")
            year = int(year_soup.contents[0])
            cover_soup = album_soup.find("div", class_="entity-cover")
            image_soup = cover_soup.find("img", class_="entity-cover__image")
            cover = self._extract_img_src(image_soup)
            result.append(Album(id_, title, year, cover))
        return result

    async def get_album_tracks(self, album_id: int) -> List[Track]:
        body = await self._request(f"album/{album_id}")
        soup = BeautifulSoup(body, "lxml")
        tracks_soup = soup.find("div", class_="page-album__tracks")
        result = []
        for index, track_soup in enumerate(tracks_soup.find_all("div", class_="d-track")):
            title_soup = track_soup.find("div", class_="d-track__name")
            title = title_soup.attrs["title"]
            title_href_soup = title_soup.find("a")
            id_ = int(title_href_soup.attrs["href"].split("/")[-1])
            result.append(Track(album_id, id_, title, index + 1))
        return result

    async def get_track_url(self, album_id: int, track_id: int) -> str:
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/api/v2.1/handlers/track/{track_id}:{album_id}/" \
                  f"web-album-track-track-main/download/m?" \
                  f"hq=0&external-domain={self.host}&overembed=no&__t={timestamp()}"
            page = f"album/{album_id}"
            headers = self.headers.build(page)
            async with session.request(method="GET", url=url, headers=headers) as response:
                body = await response.json()
                src = body["src"]
                if src.startswith("//"):
                    src = f"https:{src}"
                src += f"&format=json&external-domain={self.host}&overembed=no&__t={timestamp()}"
                result = parse.urlparse(src)
                headers = self.headers.build(page, {
                    ":authority": "storage.mds.yandex.net",
                    ":method": "GET",
                    ":path": f"{result.path}/{result.query}",
                    ":scheme": "https",
                }, True)
                async with session.request(method="GET", url=src, headers=headers) as response:
                    body = await response.json()
                    host = body["host"]
                    path = body["path"]
                    s = body["s"]
                    ts = body["ts"]
                    sign = md5(f"XGRlBW9FXlekgbPrRHuSiA{path[1::]}{s}".encode("utf-8")).hexdigest()
                    url = f"https://{host}/get-mp3/{sign}/{ts}/{path}"
                    return url
