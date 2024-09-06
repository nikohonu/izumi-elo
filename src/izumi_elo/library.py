from pathlib import Path
from typing import Any
from izumi_elo.anime_directory import AnimeDirectory
from izumi_elo.anilist import search_anime
from izumi_elo.anime import Anime
from izumi_elo.config import Config
import inquirer
import random
import typer
from pathvalidate import sanitize_filename


def calc_current_episode(anime_path, episodes):
    return episodes - len(list(anime_path.glob("*.mkv")))


def find_anime(anime_path: Path) -> Anime:
    questions_dict: dict[str, Anime] = {anime.get_key(): anime for anime in result}
    questions = [
        inquirer.List(
            "key",
            message="正しいアニメを選んでください",
            choices=questions_dict.keys(),
        ),
    ]
    answer: dict[str, Anime] | None = inquirer.prompt(questions)
    if answer:
        anime = questions_dict[answer["key"]]
        current_episode = typer.prompt(
            "現在のエピソードは？",
            default=calc_current_episode(anime_path, anime.episodes),
            type=int,
        )
        anime.current_episode = current_episode
        return anime
    else:
        raise RuntimeError("アニメオブジェクトを作成できません。")


class Library:
    def __init__(self, config: Config) -> None:
        self.collection = []
        for anime_path in config.library_path.iterdir():
            if anime_path.is_file():
                continue
            anime_directory = AnimeDirectory(anime_path)

    #         # check if anime is indexed
    #         index_path = anime_path / "index.toml"
    #         if index_path.is_file():
    #             anime = Anime.load(index_path)
    #         else:
    #             anime = find_anime(anime_path)
    #             new_anime_path = anime_path.with_name(
    #                 sanitize_filename(anime.get_key())
    #             )
    #             if typer.confirm(
    #                 f"アニメフォルダの名前を変更しますか「{new_anime_path.name}」？"
    #             ):
    #                 anime_path.rename(new_anime_path)
    #                 anime_path = new_anime_path
    #             anime.path = anime_path
    #             anime.save()
    #         self.anime.append(anime)
    #     self.anime = sorted(self.anime, key=lambda x: x.elo, reverse=True)

    # def play(self):
    #     size = len(self.anime)
    #     index = 0
    #     max_index = min(size, 4)
    #     for _ in range(0, max_index):
    #         if random.choice([True, False]):
    #             break
    #         else:
    #             index += 1
    #     if max_index == index:
    #         index = random.randint(0, size)
    #     self.anime[index].play()

    # def save(self):
    #     for anime in self.anime:
    #         anime.save()

    # def elo(self, max_matches=32):
    #     size = len(self.anime)
    #     matches = []
    #     for i in range(0, size):
    #         for j in range(i + 1, size):
    #             matches.append((i, j))
    #     max_matches = min(len(matches), max_matches)
    #     random.shuffle(matches)
    #     matches = matches[0:max_matches]
    #     for m in matches:
    #         questions = [
    #             inquirer.List(
    #                 "answer",
    #                 message="より好きなアニメを選んでください。",
    #                 choices=[
    #                     self.anime[m[0]].title,
    #                     self.anime[m[1]].title,
    #                     "Tie",
    #                     "Exit",
    #                 ],
    #             ),
    #         ]
    #         prompt_result: dict[str, str] = inquirer.prompt(questions)
    #         answer = prompt_result["answer"]
    #         result = 0
    #         if answer == "Exit":
    #             break
    #         elif answer == "Tie":
    #             result = 0.5
    #         elif answer == self.anime[m[0]].title:
    #             result = 1.0
    #         else:
    #             result = 0.0
    #         self.anime[m[0]].play_match(self.anime[m[1]], result)
    #     self.save()
    #     # for anime in self.anime:
    #     #     anime.save()
    #     # name = anime_path.name
    #     # print(search_anime(name))
    #     # break
