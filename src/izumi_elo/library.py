import datetime as dt
import random
import shutil
from pathlib import Path

import typer
from pathvalidate import sanitize_filename
from simple_term_menu import TerminalMenu

from izumi_elo.anilist import Anilist
from izumi_elo.anime import Anime
from izumi_elo.anime_directory import AnimeDirectory
from izumi_elo.config import Config


class Library:
    def __init__(self, config: Config) -> None:
        self.collection = []
        self.config = config
        for anime_path in self.config.library_path.iterdir():
            if anime_path.is_file() or anime_path.name == "audio":
                continue
            anime_directory = AnimeDirectory(anime_path)
            self.collection.append(anime_directory)
        self.collection.sort(key=lambda x: x.anime.elo, reverse=True)

    def move_file(self, old_path: Path, new_path: Path):
        for suffix in [".ass", ".srt"]:
            sub_file: Path = old_path.with_suffix(suffix)
            if sub_file.is_file():
                sub_file.rename(new_path.parent / sub_file.name)
        old_path.rename(new_path)

    def play(self, index: int):
        anime_directory: AnimeDirectory = self.collection[index]
        anime: Anime = anime_directory.anime
        file = anime_directory.play()
        if typer.confirm("Did you finish the episode?"):
            current_episode = typer.prompt(
                "Please enter the episode number.",
                default=anime.current_episode + 1,
                type=int,
            )
            anilist = Anilist(self.config.access_token)
            status = "CURRENT" if current_episode < anime.episodes else "COMPLETED"
            anilist.update_progress(anime.id, current_episode, status)
            anime.current_episode = current_episode
            anime_directory.anime = anime
            anime_directory.save()
            new_file = self.config.get_audio_path() / sanitize_filename(
                f"{dt.datetime.now()} - {file.name}", "_"
            )
            new_file.parent.mkdir(exist_ok=True)
            self.move_file(file, new_file)
            if status == "COMPLETED":
                shutil.rmtree(anime_directory.path)
            elif status == "CURRENT":
                self.adjust_elo_for_anime(index, 3)

    def play_random(self):
        size = len(self.collection)
        index = 0
        max_index = min(size, 4)
        for _ in range(0, max_index):
            if random.choice([True, False]):
                break
            else:
                index += 1
        if max_index == index:
            index = random.randint(0, size)
        self.play(index)

    def play_choose(self):
        self.play(
            TerminalMenu(
                [str(ad.anime) for ad in self.collection],
                title="Please select the anime.",
            ).show()  # pyright: ignore
        )

    def _adjust_elo(self, matches, max_matches):
        max_matches = min(len(matches), max_matches)
        random.shuffle(matches)
        matches = matches[0:max_matches]
        for m in matches:
            questions = [
                self.collection[m[0]].anime.title,
                self.collection[m[1]].anime.title,
                "Tie",
                "Exit",
            ]
            index = TerminalMenu(
                questions, title="Please select your preferred anime."
            ).show()
            result = 0
            match index:
                case 0:
                    result = 1.0
                case 1:
                    result = 0.0
                case 2:
                    result = 0.5
                case 3:
                    break
            self.collection[m[0]].anime.play_match(self.collection[m[1]].anime, result)
            for i in range(2):
                self.collection[m[i]].save()

    def adjust_elo(self, max_matches=32):
        size = len(self.collection)
        matches = []
        for i in range(0, size):
            for j in range(i + 1, size):
                matches.append((i, j))
        self._adjust_elo(matches, max_matches)

    def adjust_elo_for_anime(self, index, max_matches):
        matches = []
        for i in range(len(self.collection)):
            if i != index:
                matches.append((index, i))
        self._adjust_elo(matches, max_matches)
