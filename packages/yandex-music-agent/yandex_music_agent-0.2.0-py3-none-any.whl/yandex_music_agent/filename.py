import string
from typing import Callable

from yandex_music_agent.data import Artist, Album, Track


def normalize_base(name: str) -> str:
    return name.replace("/", "-")


def normalize_full(name: str) -> str:
    cyrillic_letters = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}{cyrillic_letters}"
    return "".join([c if c in valid_chars else "_" for c in name])


default_normalizer = normalize_full


class FilenameBuilder:

    def __init__(self, template: str, normalizer: Callable[[str], str] = default_normalizer):
        self._template = template
        self._normalizer = normalizer

    def build(self, **values) -> str:
        return "/".join((
            self._normalizer(item.format(**values))
            for item in self._template.split("/")
        ))


class MusicFilenameBuilder:
    ARTIST_DIR = "{artist.title}"
    ALBUM_DIR = ARTIST_DIR + "/{album.year} - {album.title}"
    AVATAR_TEMPLATE = ARTIST_DIR + "/avatar.jpg"
    COVER_TEMPLATE = ALBUM_DIR + "/cover.jpg"
    TRACK_TEMPLATE = ALBUM_DIR + "/{track.num:02d}. {track.title}.mp3"

    def __init__(self,
                 track_template: str = TRACK_TEMPLATE,
                 cover_template: str = COVER_TEMPLATE,
                 avatar_template: str = AVATAR_TEMPLATE,
                 normalizer: Callable[[str], str] = default_normalizer):
        self._track = FilenameBuilder(track_template, normalizer)
        self._cover = FilenameBuilder(cover_template, normalizer)
        self._avatar = FilenameBuilder(avatar_template, normalizer)

    def build_track_filename(self, artist: Artist, album: Album, track: Track) -> str:
        return self._track.build(artist=artist, album=album, track=track)

    def build_cover_filename(self, artist: Artist, album: Album) -> str:
        return self._cover.build(artist=artist, album=album)

    def build_avatar_filename(self, artist: Artist) -> str:
        return self._avatar.build(artist=artist)
