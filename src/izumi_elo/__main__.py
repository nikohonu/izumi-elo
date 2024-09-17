import shutil
import subprocess
from pathlib import Path

import typer
from typing_extensions import Annotated

from izumi_elo.anilist import get_url
from izumi_elo.config import Config
from izumi_elo.library import Library

main = typer.Typer()


@main.command()
def init(
    library_path: Annotated[
        Path, typer.Option(prompt=True, file_okay=False, exists=True, dir_okay=True)
    ],
):
    get_url()
    access_token = typer.prompt("Please enter the access token", type=str)
    config = Config(
        library_path=library_path,
        access_token=access_token,
    )
    config.save()


@main.command()
def play():
    config = Config.load()
    library = Library(config)
    library.play_choose()


@main.command()
def random():
    config = Config.load()
    library = Library(config)
    library.play_random()


@main.command()
def elo(matches_count: int):
    config = Config.load()
    library = Library(config)
    library.adjust_elo(matches_count)


@main.command()
def impd():
    config = Config.load()
    for file in config.get_audio_path().glob("*.mkv"):
        subprocess.run(["impd", "add", "-f", file])
    shutil.rmtree(config.get_audio_path())


if __name__ == "__main__":
    main()
