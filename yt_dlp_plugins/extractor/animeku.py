import re
import base64
import itertools
from yt_dlp.utils import int_or_none, urlencode_postdata
from yt_dlp.extractor.common import InfoExtractor, SearchInfoExtractor


class AnimeKuIE(InfoExtractor):
    IE_NAME = "AnimeKu"
    _VALID_URL = (
        r"https?://animeku\.com/anime/(?P<id>\d+)"  # fakeeeeeeeee url, biar keren anjay
    )
    _TESTS = [
        {
            "url": "https://animeku.com/anime/4347",
            "info_dict": {
                "id": "4347",
                "title": "Kaifuku Jutsushi no Yarinaoshi",
                "_type": "playlist",
            },
            "playlist_count": 12,
        }
    ]

    # source HEADERS: https://github.com/lucasbuilds/animeku-cli/blob/573a89158f628a90ea4da94d8c677c9c0d32ca18/src/ext/nontonanime/mod.rs#L18
    _HEADERS = {
        "User-Agent": "okhttp/3.12.13",
        "Conten_Type": "application/x-www-form-urlencoded",
        "Data-Agent": "New Aniplex v9.1",
        "Host": "animeku.my.id",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }

    # fungsi buat cari episode id
    def _get_episode_id(self, anime_id):
        # source api: https://github.com/lucasbuilds/animeku-cli/blob/573a89158f628a90ea4da94d8c677c9c0d32ca18/src/ext/nontonanime/anime.rs#L76
        episodses_api = "https://animeku.my.id/nontonanime-v77/phalcon/api/get_category_posts_secure/v9_1/"

        data = {
            "id": anime_id,
            "isAPKvalid": "true",
        }

        json = self._download_json(
            episodses_api,
            video_id=anime_id,
            data=urlencode_postdata(data),
            headers=self._HEADERS,
        )

        return json.get("posts")

    def _get_episode_link(self, episode_id):

        # source api: https://github.com/lucasbuilds/animeku-cli/blob/main/src/ext/nontonanime/mod.rs#L15
        episode_link_api = "https://animeku.my.id/nontonanime-v77/phalcon/api/get_post_description_secure/v9_4/"

        data = {
            "channel_id": episode_id,
            "isAPKvalid": "true",
        }

        json = self._download_json(
            episode_link_api,
            video_id=episode_id,
            data=urlencode_postdata(data),
            headers=self._HEADERS,
        )

        return json

    def _get_direct_links(self, data):

        quality_map = {
            "channel_url_ori": "360p",  # Original biasanya 360p/480p
            "channel_url_hd": "720p",  # HD biasanya 720p
            "channel_url_hd_ori": "720p",
            "channel_url_fhd": "1080p",  # FHD 1080p
            "channel_url_fhd_ori": "1080p",
        }

        # source  User-Pass: https://github.com/lucasbuilds/animeku-cli/blob/main/src/ext/nontonanime/mod.rs#L12
        User_Pass = (
            b"drakornicojanuar:DIvANTArtBInsTriSkEremeNtOMICErCeSMiQUaKarypsBoari"
        )

        formats = []
        for field, quality in quality_map.items():
            url = data.get(field)
            height = int_or_none(quality.replace("p", ""))

            if not url or "fast.nontonanimeid.box.ca" in url:
                continue

            formats.append(
                {
                    "url": url,
                    "quality": quality,
                    "format_id": quality,
                    "height": height,
                    "protocol": "http",
                    "width": (height * 16) / 9,
                    "format_note": quality,
                    "http_headers": {
                        "Authorization": "Basic "
                        + base64.b64encode(User_Pass).decode(),
                        "Connection": "keep-alive",
                    },
                }
            )
        return formats

    def _extract_episode_info(self, eps_name):
        """Extract episode number dari string apapun"""
        text = str(eps_name).lower()

        # Pattern 1: "Episode XX" atau "Ep. XX"
        patterns = [
            r"episode\s+(\d+)",  # "Episode 01"
            r"ep\.?\s*(\d+)",  # "Ep 01", "Ep.01"
            r"#(\d+)",  # "#01"
            r"(\d+)(?:\s*\[)",  # "01 [Buray Disc]" (angka sebelum bracket)
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            eps = match.group(1)
            if match:
                return int(eps), f"Episode {eps}"

        # Fallback: angka terakhir
        all_nums = re.findall(r"\d+", text)
        eps_int = int(all_nums[-1]) if all_nums else None
        eps_str = f"Episode {eps_int}"
        return eps_int, eps_str

    def _real_extract(self, url):
        self.to_screen("🏴‍☠️  YARRR! Downloading pirated anime...")
        self.to_screen("⚠️  Remember: With great piracy comes great responsibility!")
        anime_id = self._match_id(url)

        list_episode_id = self._get_episode_id(anime_id)  # semua daftar channel episode
        entries = []
        for eps_ids in list_episode_id:
            episode_id = str(eps_ids.get("channel_id"))

            episode_dict = self._get_episode_link(episode_id)
            title = episode_dict.get("channel_name")
            eps_num, eps_str = self._extract_episode_info(title)

            entries.append(
                {
                    "id": episode_id,
                    "episode": eps_str,
                    "episode_number": int_or_none(eps_num),
                    "title": title,
                    "thumbnail": episode_dict.get("img_url"),
                    "formats": self._get_direct_links(episode_dict),
                }
            )

        return {
            "_type": "playlist",
            "id": anime_id,
            "webpage_url": url,
            "entries": entries,
        }


class AnimeKuSearchIE(SearchInfoExtractor):
    _SEARCH_KEY = "animeku"
    _TESTS = [
        {
            "url": "animeku:jujutsu kaisen",
            "info_dict": {
                "id": "51013",
                "title": "Jujutsu Kaisen (TV)",
            },
            "playlist_count": 24,
        }
    ]

    # fungsi nya buat cari id anime berdasarkan title
    def _search_anime(self, search_title, page, movie=False):

        # source api: https://github.com/lucasbuilds/animeku-cli/blob/573a89158f628a90ea4da94d8c677c9c0d32ca18/src/ext/nontonanime/anime.rs#L28
        api_search = "https://animeku.my.id/nontonanime-v77/phalcon/api/search_category_collection/v7_1/"

        if movie:
            api_search = "https://animeku.my.id/nontonanime-v77/phalcon/api/search_anime_movie/v7_1/"

        # print(api_search)
        data = {
            "search": search_title,
            "page": page,
            "count": "20",
            "lang": "All",
            "isAPKvalid": "true",
        }

        response = self._download_json(
            api_search,
            search_title,
            data=urlencode_postdata(data),
            note=f"Downloading page {page}",
            headers=AnimeKuIE._HEADERS,
        )

        return response

    def _search_results(self, query):

        for i in itertools.count(1):
            search_result = self._search_anime(query, i, movie=False).get(
                "categories", []
            )

            if not search_result:
                self.to_screen(f"Tidak dapat menemukan {query}")
                break

            anime_id = search_result[i - 1].get("cid", {})

            yield self.url_result(f"http://animeku.com/anime/{anime_id}", AnimeKuIE)


# PUSING
