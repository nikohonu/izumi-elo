from typing import Any, Optional
from inquirer import questions
from pathvalidate import sanitize_filename
import datetime as dt
import subprocess
from pathlib import Path

import inquirer
import msgspec
import typer

import izumi_elo.anilist


class Anime(msgspec.Struct, omit_defaults=True):
    id: int
    title: str
    year: int | None
    start_date: dt.date | None
    format: str
    episodes: int
    status: str
    current_episode: int = 0
    elo: int = 1000

    # def get_index_path(self) -> Path:
    #     return self.path / "index.toml"

    # def get_key(self):
    #     return f"{self.year} - {self.title} ({self.format})"

    @classmethod
    def load(cls, path):
        index_path = path / "index.toml"
        if index_path.is_file():
            with index_path.open("rb") as file:
                try:
                    return msgspec.toml.decode(file.read(), type=cls)
                except msgspec.ValidationError:
                    pass
        answers = inquirer.prompt(
            [
                inquirer.Text(
                    "search",
                    message=f"Anilist.coで検索するアニメのタイトルを入力してください [{path.name}]",
                )
            ]
        )
        candidates: list[Anime] = izumi_elo.anilist.search_anime(
            answers["search"].strip()
        )
        candidates_dict = {str(anime): anime for anime in candidates}
        questions = [
            inquirer.List("key", "正しいアニメを選んでください", candidates_dict.keys())
        ]
        answers = inquirer.prompt(questions)
        return answers["key"]

    def __str__(self):
        result = ""
        if self.year:
            result += f"{self.year} - "
        result += str(self.title)
        if self.episodes > 1:
            result += f" ({self.format}, {self.episodes})"
        else:
            result += f" ({self.format})"
        return result

    # def save(self):
    #     index_path = self.get_index_path()
    #     index_path.parent.mkdir(exist_ok=True)
    #     with index_path.open("wb") as file:
    #         hold = self.path
    #         self.path = None
    #         file.write(msgspec.toml.encode(self))
    #         self.path = hold

    # def play(self):
    #     files = sorted(self.path.glob("*.mkv"))
    #     file = files[0]
    #     subprocess.run(["mpv", file])
    #     if typer.confirm("より好きなアニメを選んでください。"):
    #         new_file= file.with_name(sanitize_filename(f'{dt.datetime.now()} - {file.name}', "_"))
    #         file.rename(new_file)
    #         subprocess.run(["impd", "add", new_file])
    #         new_file.unlink()

    # def play_match(self, other, result):
    #     k_factor = 32.0
    #     p_self_elo: float = 1.0 / (1.0 + 10.0 ** ((other.elo - self.elo) / 400.0))
    #     p_other_elo: float = 1.0 - p_self_elo
    #     self.elo = round(self.elo + k_factor * (result - p_self_elo))
    #     other.elo = round(other.elo + k_factor * (1 - result) - p_other_elo)
