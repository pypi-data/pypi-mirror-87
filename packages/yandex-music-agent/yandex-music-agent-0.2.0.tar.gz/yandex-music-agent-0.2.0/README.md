# yandex-music-agent

[![PyPI](https://img.shields.io/pypi/v/yandex-music-agent)](https://pypi.org/project/yandex-music-agent)
![Bitbucket Pipelines](https://img.shields.io/bitbucket/pipelines/shmyga/yandex-music-agent/master)

Downloads music of selected artists account:

`<artist.title>/<album.year> - <album.title>/<track.num>. <track.title>.mp3`

## Install with pip
Requires:

* python3 (>=3.7)
* python3-pip

```
pip3 install yandex-music-agent
yandex-music-agent -o <target_music_dir>
```

## Run from source
Requires:

* python3 (>=3.7)
* python3-venv

Prepare venv
```
./venv.sh
```
Run main script
```
. .venv/bin/activate
PYTHONPATH=src python src/yandex_music_agent/__main__.py -o <target_music_dir>
```
