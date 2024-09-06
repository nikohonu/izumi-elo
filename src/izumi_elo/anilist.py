import requests
import datetime as dt
import izumi_elo.anime


def search_anime(search: str):
    query = """
    query ($page: Int, $perPage: Int, $search: String) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (search: $search, type: ANIME) {
                id
                title {
                    native
                }
                seasonYear
                format
                episodes
                startDate {
                    year
                    month
                    day
                }
                status
            }
        }
    }
    """
    variables = {"search": search, "page": 1, "perPage": 10}
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})
    candidates: list[izumi_elo.anime.Anime] = []
    for media in response.json()["data"]["Page"]["media"]:
        year: int | None = None
        if media["seasonYear"]:
            year = media["seasonYear"]
        elif media["startDate"]:
            year = media["startDate"]["year"]
        start_date = None
        if media["startDate"]:
            start_date = dt.date(
                media["startDate"]["year"],
                media["startDate"]["month"],
                media["startDate"]["day"],
            )
        candidates.append(
            izumi_elo.anime.Anime(
                id=media["id"],
                title=media["title"]["native"],
                year=year,
                start_date=start_date,
                episodes=media["episodes"],
                format=media["format"],
                status=media["status"],
            )
        )
    candidates.sort(key=lambda x: x.start_date if x.start_date else dt.date.max)
    return candidates
