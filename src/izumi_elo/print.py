from rich.console import Console
from rich.table import Table

from izumi_elo.anime import Anime, MatchResult

console = Console()


def print_match_result(
    match_result: MatchResult,
    initial_ratings: tuple[float, float],
    players: tuple[Anime, Anime],
):
    table = Table(title=f"{players[0].title} vs {players[1].title}")
    table.add_column("Anime")
    table.add_column("Initial rating")
    table.add_column("Result")
    table.add_column("Rating change")
    table.add_column("Final rating")
    match_results = [match_result, MatchResult(1 - match_result.value)]
    for i in range(2):
        table.add_row(
            players[i].title,
            str(initial_ratings[i]),
            str(match_results[i].name),
            str(players[i].elo - initial_ratings[i]),
            str(players[i].elo),
        )
    console.print(table)
