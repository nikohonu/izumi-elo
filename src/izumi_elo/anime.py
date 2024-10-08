import datetime as dt
from enum import Enum

import msgspec
import typer
from simple_term_menu import TerminalMenu

import izumi_elo.anilist

K_FACTOR = 32.0


class MatchResult(Enum):
    WIN = 1
    DRAW = 0.5
    LOSS = 0


class Anime(msgspec.Struct, omit_defaults=True):
    id: int
    title: str
    season_year: int | None
    format: str
    episodes: int
    status: str
    start_date: dt.date | None = None
    current_episode: int = 0
    elo: int = 1000

    @classmethod
    def load(cls, path):
        """
        :return new Anime class and bool, that represent the first time load
        """
        index_path = path / "index.toml"
        if index_path.is_file():
            with index_path.open("rb") as file:
                try:
                    return msgspec.toml.decode(file.read(), type=cls), False
                except msgspec.ValidationError:
                    pass
        search: str = typer.prompt(
            "Please enter the title of the anime to search on Anilist.co",
            default=path.name,
            type=str,
        ).strip()
        candidates: list[Anime] = izumi_elo.anilist.Anilist.search_anime(search)
        terminal = TerminalMenu(
            [str(anime) for anime in candidates],
            title="Please select the correct anime.",
        )
        index: int = terminal.show()  # pyright: ignore
        return candidates[index], True

    def __str__(self):
        result = ""
        if self.season_year:
            result += f"{self.season_year} - "
        result += str(self.title)
        if self.episodes and self.episodes > 1:
            result += f" ({self.format}, {self.episodes})"
        else:
            result += f" ({self.format})"
        return result

    def play_match(self, other, result: MatchResult):
        p_self_elo: float = 1.0 / (1.0 + 10.0 ** ((other.elo - self.elo) / 400.0))
        p_other_elo: float = 1.0 - p_self_elo

        self.elo = round(self.elo + K_FACTOR * (result.value - p_self_elo))
        other.elo = round(other.elo + K_FACTOR * ((1 - result.value) - p_other_elo))
