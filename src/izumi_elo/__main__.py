from pathlib import Path
import random
import inquirer
from typing_extensions import Annotated
from izumi_elo.library import Library
from izumi_elo.config import Config

import typer

main = typer.Typer()


@main.command()
def init(
    library_path: Annotated[
        Path, typer.Option(prompt=True, file_okay=False, exists=True, dir_okay=True)
    ],
):
    config = Config(library_path=library_path)
    config.save()


@main.command()
def play():
    config = Config.load()
    library = Library(config)
    # library.play()
    # library.elo(4)


@main.command()
def elo():
    config = Config.load()
    library = Library(config)
    library.elo()


if __name__ == "__main__":
    main()
