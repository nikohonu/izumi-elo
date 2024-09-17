import subprocess
from pathlib import Path

import msgspec
import typer
from pathvalidate import sanitize_filename

from izumi_elo.anime import Anime


class AnimeDirectory:
    def __init__(self, path: Path):
        self.path = path
        self.anime, is_first_load = Anime.load(path)
        if is_first_load:
            new_path = self.path.with_name(
                sanitize_filename(str(self.anime), replacement_text="_")
            )
            if typer.confirm(
                f'Do you want to rename the anime folder to "{new_path}"?'
            ):
                self.path.rename(new_path)
                self.path = new_path

            def calc_current_episode():
                if self.anime.status == "RELEASING":
                    return 0
                return self.anime.episodes - len(list(self.path.glob("*.mkv")))

            self.anime.current_episode = typer.prompt(
                "What is the current episode?",
                default=calc_current_episode(),
                type=int,
            )
            self.save()

    def get_index_path(self) -> Path:
        return self.path / "index.toml"

    def save(self):
        index_path = self.get_index_path()
        index_path.parent.mkdir(exist_ok=True)
        print(self.anime.title, self.anime.elo)
        with index_path.open("wb") as file:
            file.write(msgspec.toml.encode(self.anime))

    def play(self):
        files = sorted(self.path.glob("*.mkv"))
        file = files[0]
        subprocess.run(["mpv", file])
        return file
