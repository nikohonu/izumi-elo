from izumi_elo.anime import Anime, MatchResult


def test_play_match():
    anime1 = Anime(
        1,
        "TestAnime1",
        season_year=2010,
        format="TV",
        episodes=12,
        status="RELEASING",
        start_date=None,
        current_episode=0,
        elo=1200,
    )
    anime2 = Anime(
        2,
        "TestAnime2",
        season_year=2011,
        format="OVA",
        episodes=12,
        status="FINISHED",
        start_date=None,
        current_episode=0,
        elo=1000,
    )
    anime1.play_match(anime2, MatchResult.WIN)
    assert anime1.elo == 1208
    assert anime2.elo == 992
    anime2.play_match(anime1, MatchResult.LOSS)
    assert anime1.elo == 1215
    assert anime2.elo == 985
    anime1.play_match(anime2, MatchResult.DRAW)
    assert anime1.elo == 1206
    assert anime2.elo == 994
