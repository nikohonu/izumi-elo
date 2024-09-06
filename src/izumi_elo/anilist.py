import requests
from izumi_elo.anime import Anime


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
                }
            }
        }
    }
    """
    variables = {"search": search, "page": 1, "perPage": 10}
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})
    return [
        Anime(
            id=media["id"],
            title=media["title"]["native"],
            year=media["seasonYear"] if media["seasonYear"] else media["startDate"]["year"],
            episodes=media["episodes"],
            format=media["format"],
        )
        for media in response.json()["data"]["Page"]["media"]
    ]
