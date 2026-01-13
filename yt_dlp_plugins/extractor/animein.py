# pylint: disable=abstract-method
"""
AnimeIn Web Extractor for yt-dlp
Extracts anime videos from animeinweb.com
"""
import itertools
from yt_dlp.utils import int_or_none
from yt_dlp.extractor.common import InfoExtractor, SearchInfoExtractor


# https://animeinweb.com/anime/4347?ep=2
class AnimeInWebIE(InfoExtractor):
    """Base class for AnimeIn extractors"""

    IE_NAME = "AnimeInWeb"
    _TESTS = [
        {
            "url": "https://animeinweb.com/anime/4347",
            "info_dict": {
                "id": "4347",
                "title": "Kaifuku Jutsushi no Yarinaoshi",
                "_type": "playlist",
            },
            "playlist_count": 12,
        }
    ]

    _VALID_URL = (
        r"https?://animeinweb\.com/anime/(?P<id>\d+)"
    )

    def _get_thumbnail(self, image_url, base_url="https://api.animein.net"):
        if not image_url:
            return None

        # Case 1: URL lengkap
        if image_url.startswith(("http://", "https://")):
            # Tambahkan _full.jpg jika belum ada
            if not image_url.endswith("_full.jpg"):
                # Cek apakah sudah ada ekstensi .jpg
                if not image_url.endswith(".jpg"):
                    return f"{image_url}_full.jpg"
            return image_url

        # Case 2: Path relatif
        if image_url.startswith("/"):
            return f"{base_url.rstrip('/')}/{image_url.lstrip('/')}"

        return None

    def _get_filesize(self, size_str):
        """Simple parser untuk API animeinweb"""

        if not size_str:
            return None

        # Mapping unit ke multiplier
        unit_multiplier = {
            "KB": 1024,
            "MB": 1024 * 1024,
            "GB": 1024 * 1024 * 1024,
            "TB": 1024 * 1024 * 1024 * 1024,
        }

        # Cari unit
        for unit, mult in unit_multiplier.items():
            if unit in size_str.upper():
                num = float(size_str.upper().replace(unit, "").strip())
                return int(num * mult)

        # Tidak ada unit, asumsi MB
        try:
            return int(float(size_str) * 1024 * 1024)
        except (ValueError, TypeError):
            return None

    def _extract_anime_info(self, url, anime_id):
        # https://animeinweb.com/api/proxy/3/2/movie/detail/1234

        api_details = url.replace("/anime/", "/api/proxy/3/2/movie/detail/")

        response = self._download_json(api_details, anime_id)

        data = response.get("data", {})
        movie = data.get("movie", {})

        return {
            "type": movie.get("type"),
            "genre": movie.get("genre"),
            "title": movie.get("title"),
        }

    def _fill_formats(self, episode_id):

        api_streams = (
            f"https://animeinweb.com/api/proxy/3/2/episode/streamnew/{episode_id}"
        )

        stream_info = self._download_json(api_streams, episode_id)
        servers = stream_info.get("data", {}).get("server", {})

        formats = []
        for server in servers:
            link = server.get("link")

            if not link or "new.uservideo.xyz" in link:
                continue

            quality = server.get("quality", "")
            height = int_or_none(quality.replace("p", ""))
            formats.append(
                {
                    "url": link,
                    "format_id": quality,
                    "quality": quality,
                    "uploader_id": server.get("username"),
                    "height": height,
                    "width": int_or_none(((height * 16) / 9)),
                    "filesize": int_or_none(
                        self._get_filesize(server.get("key_file_size"))
                    ),
                    "format_note": quality,
                }
            )

        return formats

    def _real_extract(self, url):
        self.to_screen("🏴‍☠️  YARRR! Downloading pirated anime...")
        self.to_screen("⚠️  Remember: With great piracy comes great responsibility!")
        anime_id = self._match_id(url)

        # https://animeinweb.com//api/proxy/3/2/movie/episode/1234
        api_episodes = url.replace("/anime/", "/api/proxy/3/2/movie/episode/")

        episode_data = self._download_json(
            api_episodes,
            anime_id,
            headers={
                "Accept": "application/json, text/plain, */*",
                "Connection": "keep-alive",
                "Host": "animeinweb.com",
                "Referer": api_episodes,
            },
            note=f"searching {anime_id}",
            errnote=f"failed getting info for {anime_id}",
        )

        # ambil data anime
        episodes = episode_data.get("data", {}).get("episode", {}) or []
        anime_info = self._extract_anime_info(url, anime_id)
        title = anime_info.get("title")

        entries = []
        for eps in reversed(episodes):
            episode_id = eps.get("id")  # id anime per episode
            eps_index = eps.get("index")
            eps_str = eps.get("title")

            entries.append(
                {
                    "id": episode_id,
                    "episode": eps_str,
                    "episode_number": int_or_none(eps_index),
                    "view_count": int_or_none(eps.get("views")),
                    "tags": anime_info.get("genre"),
                    "title": f"{title} {eps_str}",
                    "categories": anime_info.get("type"),
                    "thumbnail": self._get_thumbnail(eps.get("image")),
                    "webpage_url": f"{url}?ep={eps_index}",
                    "playlist_title": title,
                    "formats": self._fill_formats(episode_id),
                }
            )

        self.to_screen("🎬 Enjoy your anime! - THANKS FOR USING MY EXTRACTORS")

        return {
            "_type": "playlist",
            "id": anime_id,
            "webpage_url": url,
            "channel_url": "https://animeinweb.com",
            "entries": entries,
        }


class AnimeInWebSearchIE(SearchInfoExtractor):
    """Extractor for searching anime on AnimeIn Web"""

    _SEARCH_KEY = "animein"
    _TESTS = [
        {
            "url": "animein:jujutsu kaisen",
            "info_dict": {
                "id": "51013",
                "title": "Jujutsu Kaisen (TV)",
            },
            "playlist_count": 24,
        }
    ]

    def _search_results(self, query):

        api_search = "https://animeinweb.com/api/proxy/3/2/explore/movie"

        if query.isnumeric():
            # pake return kok gabisa ya?
            yield self.url_result(
                f"https://animeinweb.com/anime/{query}", AnimeInWebIE, query
            )

        for i in itertools.count(0):
            response = self._download_json(
                api_search,
                query,
                query={"page": i, "sort": "views", "keyword": query},
                note=f"Downloading page {i}",
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "Content-Type": "application/json; charset=utf-8",
                    "Host": "animeinweb.com",
                    "Connection": "keep-alive",
                    "Referer": "https://animeinweb.com/search",
                },
            )["data"].get("movie")

            if not response:
                self.to_screen("Tidak menemukan daftar anime")
                break

            for list_id in response:
                anime_id = list_id.get("id")
                yield self.url_result(
                    f"https://animeinweb.com/anime/{anime_id}", AnimeInWebIE
                )
