import itertools
import math

from yt_dlp.extractor.common import InfoExtractor, SearchInfoExtractor
from yt_dlp.utils import (
    LazyList,
    float_or_none,
    int_or_none,
    parse_resolution,
    random_user_agent,
    str_to_int,
    traverse_obj,
    url_or_none,
    urljoin,
)


# pylint: disable=abstract-method
class AnimeIn(InfoExtractor):
    """ANIMEIN BASE EXTRACTOR"""

    def _call_api(
        self,
        base_url='https://animeinweb.com',
        path_url=None,
        video_id=None,
        query=None,
        fatal=True,
        note='Downloading ANIMEIN API JSON',
    ):
        """Buat manggil api animein"""
        return self._download_json(urljoin(base_url, path_url), video_id=video_id, query=query, note=note, fatal=fatal)

    def _get_episode_info(self, episode_id: str, episode: str) -> list[dict] | None:
        episode_info = self._call_api(
            path_url=f'/api/proxy/3/2/episode/streamnew/{episode_id}',
            video_id=episode_id,
            note=f'Downloading info {episode}',
        )
        return traverse_obj(episode_info, ('data', 'server'))

    @staticmethod
    def _parse_quality_string(quality_str: str | None = None) -> int | None:
        fmt_map = {360: '18', 480: '35', 720: '22', 1080: '37'}
        if not quality_str:
            return None, None
        resolution = parse_resolution(quality_str)
        if resolution and isinstance(resolution, dict):
            res = resolution.get('height')
            return res, fmt_map[res]
        return None, None

    def _build_format_entry(self, stream_data: dict) -> dict | None:
        stream_type = stream_data.get('type').lower()
        quality_str = stream_data.get('quality', '')
        stream_url = stream_data.get('link')
        height, format_id = self._parse_quality_string(quality_str)
        if stream_type != 'direct' or not stream_url or not height:
            return {}
        return {
            'url': url_or_none(stream_url),
            'format_id': format_id,
            'quality': quality_str,
            'height': height,
            'width': int_or_none((height * 16) / 9),
            'filesize': int_or_none(self._parse_filesize(stream_data.get('key_file_size'), stream_url)),
            'http_headers': {
                'User-Agent': random_user_agent(),
                'Accept-Language': 'en-US,en;q=0.8',
                'Accept-Encoding': 'identity;q=1, *;q=0',
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Host': 'storages.animein.net',
                'Sec-Fetch-Dest': 'video',
                'sec-ch-ua-mobile': '?0',
                'Referer': 'https://animeinweb.com/',
            },
        }

    def _extract_formats(self, episode_id: str, episode: str) -> list[dict]:
        streams = self._get_episode_info(episode_id, episode)
        for stream in streams:
            format_entry = self._build_format_entry(stream)
            if format_entry:
                yield format_entry

    @staticmethod
    def _get_thumbnail(base_url: str = 'https://api.animein.net', image_url: str | None = None) -> str | None:
        """Fungsi buat nyambung url kalo url nya ga jelas"""
        if not image_url:
            return None
        if image_url.startswith(('https://', 'http://')):
            if not image_url.endswith('_full.jpg'):
                return f'{image_url}_full.jpg'
        if image_url.startswith(('/assets', '/')):
            return urljoin(base_url, image_url)
        return None

    def _parse_filesize(self, size_str: str | None = None, url: str | None = None) -> int | None:  # TODO: remove
        """Buat nyari filezie ntah mb ntah gb"""
        try:
            return str_to_int(float_or_none(size_str) * 1024**2) if size_str else None
        except (ValueError, TypeError, AttributeError):
            return None

    def _get_anime_info(self, anime_id: str) -> dict[str] | None:
        """Buat ambil judul anime doang sih wkwk"""
        metadata_dict = self._call_api(path_url=f'/api/proxy/3/2/movie/detail/{anime_id}', video_id=anime_id)
        return traverse_obj(metadata_dict, ('data', 'movie'))

    def _extract_all_episodes(self, anime_id: str) -> list[str, dict] | None:
        last_page_index = self._get_the_last_page(anime_id)
        for page_num in range(last_page_index, -1, -1): # start, step, stop
            episodes = self._fetch_episode_list_page(anime_id, page_num)
            if not episodes:
                break
            yield from reversed(episodes)

    def _get_the_last_page(self, anime_id: str) -> int:
        data_eps = self._call_api(path_url=f'/api/proxy/3/2/movie/episode/{anime_id}', video_id=anime_id)
        last_eps = traverse_obj(data_eps, ('data', 'episode', 0, 'index'))
        last_page_index = math.ceil(int(last_eps) / 30) - 1
        return max(last_page_index, 0)

    def _fetch_episode_list_page(self, anime_id: str, page_num: int = 0) -> list[str, dict] | None:
        response = self._call_api(
            path_url=f'/api/proxy/3/2/movie/episode/{anime_id}',
            video_id=anime_id,
            query={'page': page_num},
            note=f'Downloading page {page_num}')
        return traverse_obj(response, ('data', 'episode'))

    def _search_anime(self, query: str, page_num: str = 0) -> list[str, dict] | None:
        response = self._call_api(
            path_url='/api/proxy/3/2/explore/movie',
            video_id=query,
            query={'page': page_num, 'sort': 'views', 'keyword': query},)
        return traverse_obj(response, ('data', 'movie'))


class AnimeInWebIE(AnimeIn):  # TODO: toda todo tok tell gatel
    """ASEP SIGMA LMAO"""

    IE_NAME = 'animeinweb'
    _VALID_URL = r'https?://animeinweb\.com/anime/(?P<id>\d+)'

    def _build_episode_entry(self, episode_data: dict, anime_data: dict) -> dict[str, list] | None:
        episode_id = episode_data.get('id')
        episode_title = episode_data.get('title', '')
        episode_index = episode_data.get('index')
        title = anime_data.get('title')
        formats = LazyList(self._extract_formats(episode_id, episode_title))
        if not formats:
            self.report_warning(f'No formats found for episode {episode_index}')
            return {}
        return {
            'id': episode_id,
            'title': f'{title} {episode_title}',
            'series': title,
            'playlist_title': title,
            'media_type': 'episode',
            'ext': 'mp4',
            'episode_number': int_or_none(episode_index),
            'thumbnail': url_or_none(self._get_thumbnail(image_url=episode_data.get('image'))),
            'formats': formats,
            **traverse_obj(
                anime_data,
                {
                    'series_id': ('id'),
                    'alt_title': ('synonyms'),
                    'view_count': ('views', {int_or_none}),
                    'release_year': ('year', {int_or_none}),
                    # 'categories': [c.strip() for c in ('genre').split(',')],
                },
            ),
        }

    def _entries(self, anime_id, anime_data):
        for episode_data in self._extract_all_episodes(anime_id):
            entry = self._build_episode_entry(episode_data, anime_data)
            if not entry:
                continue
            yield entry

    def _real_extract(self, url: str) -> dict[list]:
        anime_id = self._match_id(url)
        anime_data = self._get_anime_info(anime_id)
        return self.playlist_result(
            entries=self._entries(anime_id, anime_data),
            playlist_id=anime_id,
            **traverse_obj(
                anime_data,
                {
                    'title': ('title'),
                    'description': ('synopsis'),
                    'image_poster': ('image_poster'),
                    'image_cover': ('image_cover'),
                },
            ),
        )


class AnimeInSearchIE(SearchInfoExtractor, AnimeInWebIE):
    """KALO NGEBUG AJA SENDIRI"""

    IE_DESC = 'animeinweb Search'
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
                    ie=AnimeInWebIE.ie_key(),
                    video_id=data.get('id'),
                    video_title=data.get('title'),
                )
