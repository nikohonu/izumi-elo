import datetime as dt

import requests

import izumi_elo.anime


def get_url():
    query = {"client_id": 21009, "response_type": "token"}
    p = requests.Request(
        "GET", "https://anilist.co/api/v2/oauth/authorize", params=query
    ).prepare()
    print(p.url)


class Anilist:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.url = "https://graphql.anilist.co/"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.access_token,
            "Accept": "application/json",
        }

    def get(self, query: str, variables):
        return requests.post(
            self.url,
            json={"query": query, "variables": variables},
            headers=self.headers,
        )

    @staticmethod
    def static_get(query: str, variables):
        url = "https://graphql.anilist.co/"
        return requests.post(url, json={"query": query, "variables": variables})

    def get_user_id(self):
        query = """
        {
            Viewer {
                id
            }
        }"""
        variables = {}
        response = self.get(query, variables)
        return response.json()["data"]["Viewer"]["id"]

    def update_progress(self, media_id: int, progress: int, status: str):
        query = """
        mutation ($media_id: Int, $progress: Int, $status: MediaListStatus) {
            SaveMediaListEntry (mediaId: $media_id, progress: $progress, status: $status) {
              progress
            }
        }
        """
        variables = {"media_id": media_id, "progress": progress, "status": status}
        response = self.get(query, variables)
        if response.status_code != 200:
            print(
                "update_progress failed. Status code:",
                response.status_code,
            )

    @staticmethod
    def search_anime(search: str):
        query = """
        query ($page: Int, $per_page: Int, $search: String) {
            Page (page: $page, perPage: $per_page) {
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
        }"""
        variables = {"search": search, "page": 1, "per_page": 10}
        response = Anilist.static_get(query, variables)
        candidates: list[izumi_elo.anime.Anime] = []
        for media in response.json()["data"]["Page"]["media"]:
            season_year: int | None = None
            if media["seasonYear"]:
                season_year = media["seasonYear"]
            elif media["startDate"]:
                season_year = media["startDate"]["year"]
            start_date = None
            if media["startDate"] and media["startDate"]["day"]:
                start_date = dt.date(
                    media["startDate"]["year"],
                    media["startDate"]["month"],
                    media["startDate"]["day"],
                )
            candidates.append(
                izumi_elo.anime.Anime(
                    id=media["id"],
                    title=media["title"]["native"],
                    season_year=season_year,
                    start_date=start_date,
                    episodes=media["episodes"],
                    format=media["format"],
                    status=media["status"],
                )
            )

        def get_key(x: izumi_elo.anime.Anime):
            if x.start_date:
                return x.start_date
            elif x.season_year:
                return dt.date(x.season_year, 1, 1)
            else:
                return dt.date.min

        candidates.sort(key=get_key)
        return candidates
