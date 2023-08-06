import logging
import os
from typing import AsyncIterator, NamedTuple

import aiostream
import mutagen
import mutagen.id3
from mechanicus.core.executor import QueueExecutor
from mechanicus.downloader import DownloadTask, Downloader, FileHandler
from mutagen.easyid3 import EasyID3

from yandex_music_agent.api import YandexMusicApi
from yandex_music_agent.data import Artist, Album
from yandex_music_agent.filename import MusicFilenameBuilder


class ID3Tags(NamedTuple):
    title: str
    tracknumber: str
    artist: str
    album: str
    date: str


class ID3TagsHandler(FileHandler, NamedTuple):
    tags: ID3Tags

    async def apply(self, filename: str):
        try:
            meta = EasyID3(filename)
        except mutagen.id3.ID3NoHeaderError:
            meta = mutagen.File(filename, easy=True)
            meta.add_tags()
        meta.update(self.tags._asdict())
        meta.save(filename, v1=2)


class YandexMusicAgent:
    logger = logging.getLogger("agent")

    def __init__(self, api: YandexMusicApi, target_dir: str,
                 parallel: int = QueueExecutor.PARALLEL):
        self.api = api
        self.target_dir = target_dir
        self.parallel = parallel
        self.filename_builder = MusicFilenameBuilder()

    @classmethod
    def write_tags(cls, filename: str, tags: dict):
        try:
            meta = EasyID3(filename)
        except mutagen.id3.ID3NoHeaderError:
            meta = mutagen.File(filename, easy=True)
            meta.add_tags()
        for k, v in tags.items():
            meta[k] = v
        meta.save(filename, v1=2)

    async def walk_album(self, artist: Artist, album: Album) -> AsyncIterator[DownloadTask]:
        self.logger.debug("Walk %s", album)
        tracks = await self.api.get_album_tracks(album.id)
        print(f"> {album.year} - {album.title} ({len(tracks)})")
        if album.cover:
            cover_filename = os.path.join(
                self.target_dir,
                self.filename_builder.build_cover_filename(artist, album),
            )
            if not os.path.exists(cover_filename):
                yield DownloadTask(album.cover, cover_filename)
        for track in tracks:
            target_filename = os.path.join(
                self.target_dir,
                self.filename_builder.build_track_filename(artist, album, track),
            )
            if not os.path.exists(target_filename):
                url = await self.api.get_track_url(track.album_id, track.id)
                tags = ID3Tags(track.title, str(track.num), artist.title, album.title, str(album.year))
                yield DownloadTask(url, target_filename, ID3TagsHandler(tags))

    async def walk_artist(self, artist: Artist) -> AsyncIterator[DownloadTask]:
        self.logger.debug("Walk %s", artist)
        albums = await self.api.get_artist_albums(artist.id)
        print(f"{artist.title} ({len(albums)})")
        if artist.avatar:
            avatar_filename = os.path.join(self.target_dir, self.filename_builder.build_avatar_filename(artist))
            if not os.path.exists(avatar_filename):
                yield DownloadTask(artist.avatar, avatar_filename)
        albums_walkers = [self.walk_album(artist, album) for album in albums]
        for i in range(0, len(albums_walkers), self.parallel):
            chunk = albums_walkers[i:i + self.parallel]
            async with aiostream.stream.merge(*chunk).stream() as streamer:
                async for task in streamer:
                    yield task

    async def walk_favorites(self, email: str) -> AsyncIterator[DownloadTask]:
        self.logger.debug("Walk favorites %s", email)
        artists = await self.api.get_favorite_artists(email)
        for artist in artists:
            # ToDo: get artist with avatar
            artist = await self.api.get_artist(artist.id)
            async for task in self.walk_artist(artist):
                yield task

    def build_executor(self) -> QueueExecutor:
        return QueueExecutor(Downloader(), self.parallel)

    async def download_artist(self, artist: Artist):
        await self.build_executor().execute(self.walk_artist(artist))

    async def download_favorites(self, email: str):
        await self.build_executor().execute(self.walk_favorites(email))
