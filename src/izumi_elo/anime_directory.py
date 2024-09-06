from pathlib import Path

from izumi_elo.anime import Anime


class AnimeDirectory:
    def __init__(self, path: Path):
        self.path = path
        self.anime = Anime.load(path)
        print("from AnimeDirectory", self.anime)