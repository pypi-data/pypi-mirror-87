import configparser
import getpass
import logging
import os
from pathlib import Path

import argparse
from mechanicus.core.executor import QueueExecutor

from yandex_music_agent import auth
from yandex_music_agent.agent import YandexMusicAgent
from yandex_music_agent.api import YandexMusicApi
from yandex_music_agent.common.storage import StorageValue, ConfigValue
from yandex_music_agent.data import YandexCookie

StorageValue.app_name = "YandexMusicAgent"


class OutputDir(StorageValue[str]):
    name = "output"
    default_value = os.path.join(Path.home(), "Music")


class Credentials(ConfigValue):
    name = "credentials"

    def _check(self):
        if self.value is None:
            login = input("yandex login: ")
            password = getpass.getpass("yandex password: ")
            auth.resolve_cookie(login, password)
            config = configparser.ConfigParser()
            config.add_section("yandex")
            config.set("yandex", "login", login)
            config.set("yandex", "password", password)
            self.value = config

    @property
    def login(self) -> str:
        self._check()
        return self.value["yandex"]["login"]

    @property
    def password(self) -> str:
        self._check()
        return self.value["yandex"]["password"]


class CookieData(StorageValue[YandexCookie]):
    name = "cookie"
    type = YandexCookie


async def run():
    output = OutputDir()
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--artist", help="Artist ID")
    parser.add_argument("-o", "--output", default=output.value,
                        help=f"Output directory, current: {output.value}")
    parser.add_argument("-p", "--parallel", default=QueueExecutor.PARALLEL,
                        help=f"Number of parallel downloads, default: {QueueExecutor.PARALLEL}",
                        type=int)
    parser.add_argument("-v", "--verbose",
                        help="Increase output verbosity",
                        action="store_true")
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    if args.output:
        output.value = args.output
    cookie_data = CookieData()
    if (
            cookie_data.value is None or
            not auth.validate_cookie(cookie_data.value)
    ):
        credentials = Credentials()
        cookie_data.value = auth.resolve_cookie(credentials.login, credentials.password)
    api = YandexMusicApi(cookie_data.value)
    agent = YandexMusicAgent(api, output.value, args.parallel)
    if args.artist:
        artist = await api.get_artist(args.artist)
        await agent.download_artist(artist)
    else:
        await agent.download_favorites(cookie_data.value.login)
