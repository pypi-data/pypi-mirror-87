from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="yandex-music-agent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.2.0",
    description="Download yandex account favorites artists music",
    url="https://bitbucket.org/shmyga/yandex-music-agent",
    author="shmyga",
    author_email="shmyga.z@gmail.com",
    license="MIT",
    package_dir={"": "src"},
    packages=["yandex_music_agent", "yandex_music_agent.common"],
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "argparse>=1",
        "appdirs>=1",
        "mechanicus>=0",
        "aiostream>=0",
        "beautifulsoup4>=4",
        "lxml>=4",
        "brotlipy>=0",
        "mutagen>=1",
    ],
    entry_points={
        "console_scripts": ["yandex-music-agent=yandex_music_agent.__main__:__main__"],
    }
)
