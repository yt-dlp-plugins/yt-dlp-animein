import itertools
import re

from yt_dlp.extractor.common import InfoExtractor, SearchInfoExtractor
from yt_dlp.utils import int_or_none, urljoin

# pylint: disable=abstract-method

class AnimeIn(InfoExtractor):
    """ANIMEIN BASE EXTRACTOR"""

    def _call_api(
        self,
        base_url='https://animeinweb.com',
        path_url: str | None = None,
        video_id: str | None = None,
        query: dict | None = None,
        fatal: bool = True,
        note: str = 'Downloading ANIMEIN API JSON',
    ):
        """Buat manggil api animein"""

        return self._download_json(
            urljoin(base_url, path_url),
            video_id=video_id,
            query=query,
            note=note,
            fatal=fatal,
        )

    def _get_episode_info(self, episode_id: str,
                          episode: str) -> list[dict] | None:
        episode_info = self._call_api(
            path_url=f'/api/proxy/3/2/episode/streamnew/{episode_id}',
            video_id=episode_id,
            note=f'Downloading info {episode}',
        )
        return episode_info.get('data', {}).get('server', [])

    @staticmethod
    def _parse_quality_string(quality_str: str | None = None) -> int | None:
        if not quality_str:
            return None

        # Match pattern seperti '720', '720p', '1080', '1080p'
        match = re.match(r'^(\d+)p?$', quality_str, re.IGNORECASE)
        if match:
            return int(match.group(1))

        return None

    def _build_format_entry(self, stream_data: dict) -> dict | None:
        stream_type = stream_data.get('type').lower()
        quality_str = stream_data.get('quality', '')
        stream_url = stream_data.get('link')

        if stream_type != 'direct' or not stream_url:
            return None

        height = self._parse_quality_string(quality_str)

        if not height:
            return None

        return {
            'url': stream_url,
            'format_id': quality_str,
            'quality': quality_str,
            'height': height,
            'width': int_or_none((height * 16) / 9),
            'filesize': int_or_none(
                self._parse_filesize(stream_data.get('key_file_size')),
            ),
        }

    def _extract_formats(self, episode_id: str, episode: str) -> list[dict]:
        streams = self._get_episode_info(episode_id, episode)
        formats = []

        for stream in streams:
            format_entry = self._build_format_entry(stream)
            if format_entry:
                formats.append(format_entry)

        return formats

    @staticmethod
    def _get_thumbnail(base_url: str = 'https://api.animein.net',
                       image_url: str | None = None) -> str | None:
        """Fungsi buat nyambung url kalo url nya ga jelas"""
        if not image_url:
            return None

        if image_url.startswith(('https://', 'http://')):
            if not image_url.endswith('_full.jpg'):
                return f'{image_url}_full.jpg'

        if image_url.startswith(('/assets', '/')):
            return f'{base_url}{image_url}'

        return None

    @staticmethod
    def _parse_filesize(size_str: str | None = None) -> int | None:
        """Buat nyari filezie ntah mb ntah gb"""
        try:
            return int(float(size_str) * 1024**2) if size_str else None
        except (ValueError, TypeError, AttributeError):
            return None

    def _get_anime_info(self, anime_id: str) -> dict | None:
        """Buat ambil judul anime doang sih wkwk"""
        metadata_dict = self._call_api(
            path_url=f'/api/proxy/3/2/movie/detail/{anime_id}',
            video_id=anime_id,
        )
        return metadata_dict.get('data', {}).get('movie', {})

    def _extract_all_episodes(self, anime_id: str) -> list[dict] | None:
        for page_num in itertools.count(0):
            episodes = self._fetch_episode_list_page(anime_id, page_num)
            if not episodes:
                # self.to_screen('Ini page terakhir, mau kemana lagi?')
                break

            yield from episodes

    def _fetch_episode_list_page(self, anime_id: str,
                                 page_num: int = 0) -> list[dict] | None:
        response = self._call_api(
            path_url=f'/api/proxy/3/2/movie/episode/{anime_id}',
            video_id=anime_id,
            query={'page': page_num},
            note=f'Downloading page {page_num}',
        )

        return response.get('data', {}).get('episode', [])

    def _search_anime(self, query: str,
                      page_num: str = 0) -> list[dict] | None:
        response = self._call_api(
            path_url='/api/proxy/3/2/explore/movie',
            video_id=query,
            query={'page': page_num, 'sort': 'views', 'keyword': query},
        )

        return response.get('data', {}).get('movie', [])


class AnimeInWebIE(AnimeIn):
    """ASEP SIGMA LMAO"""

    IE_NAME = 'animeinweb'
    _VALID_URL = r'https?://animeinweb\.com/anime/(?P<id>\d+)'

    def _build_episode_entry(self, episode_data: dict, anime_title: str) -> dict:
        episode_id = episode_data.get('id')
        episode_title = episode_data.get('title', '')
        episode_index = episode_data.get('index')

        return {
            'id': episode_id,
            'title': f'{anime_title} {episode_title}',
            'series': anime_title,
            'playlist_title': anime_title,
            'episode': episode_title,
            'episode_number': int_or_none(episode_index),
            'thumbnail': self._get_thumbnail(image_url=episode_data.get('image')),
            'formats': self._extract_formats(episode_id, episode_title),
        }

    def _real_extract(self, url: str) -> dict:
        anime_id = self._match_id(url)
        anime_title = self._get_anime_info(anime_id).get('title')

        entries = []

        for episode_data in self._extract_all_episodes(anime_id):
            entry = self._build_episode_entry(episode_data, anime_title)
            entries.append(entry)

        return {
            '_type': 'playlist',
            'id': anime_id,
            'title': anime_title,
            'channel_url': 'https://animeinweb.com',
            'entries': reversed(entries),
        }


class AnimeInSearchIE(SearchInfoExtractor, AnimeInWebIE):
    """KALO NGEBUG AJA SENDIRI"""
    IE_DESC = 'animein web Search'
    IE_NAME = 'animein:search'
    _SEARCH_KEY = 'animein'

    def _search_results(self, query: str) -> dict:
        for page_num in itertools.count(0):
            anime_list = self._search_anime(query, page_num)

            if not anime_list:
                break

            for data in anime_list:

                yield self.url_result(
                    url=f'https://animeinweb.com/anime/{data.get("id")}',
                    ie=AnimeInWebIE,
                    video_id=data.get('id'),
                    video_title=data.get('title'),
                )
