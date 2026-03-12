import math

from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import (
    parse_resolution,
    traverse_obj,
    urljoin,
)


# sorry baru tau ada fitur cache 😅
# pylint: disable=abstract-method
class AnimeinBaseIE(InfoExtractor):
    """ANIMEIN BASE EXTRACTOR"""
    _VALID_URL = False

    def _call_api(self, path_url=None, video_id=None, query=None, fatal=True, note=None, **kwargs):
        """Buat manggil api animein"""
        base_url = 'https://animeinweb.com'
        full_url = urljoin(base_url, path_url)
        default_note = 'Downloading ANIMEIN API JSON'
        return self._download_json(full_url, video_id=video_id, query=query, note=note or default_note, fatal=fatal, **kwargs)

    def _get_episode_info(self, episode_id: str, episode: str) -> list[dict[str, any]] | None:
        cache_file = f'{episode_id}_{episode}'
        episode_info = self.cache.load('animein', cache_file)
        if not episode_info:
            episode_info = self._call_api(
                path_url=f'/api/proxy/3/2/episode/streamnew/{episode_id}',
                video_id=episode_id,
                note=f'Downloading info for {episode.lower()}',
            )
            self.cache.store('animein', cache_file, episode_info)
        return traverse_obj(episode_info, ('data', 'server'))

    def _build_format_entry(self, stream_data: dict) -> dict[str, any]:
        stream_type = stream_data.get('type').lower()
        quality_str = stream_data.get('quality', '')
        stream_url = stream_data.get('link')
        if stream_type != 'direct' or not stream_url:
            return {}
        return {
            'url': stream_url,
            'quality': quality_str,
            **parse_resolution(quality_str),
            'http_headers': {'Referer': 'https://animeinweb.com/'},
        }

    def _extract_formats(self, episode_id: str, episode: str):
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

    def _get_anime_info(self, anime_id: str) -> dict[str, any] | None:
        """Buat ambil judul anime doang sih wkwk"""
        metadata = self._call_api(path_url=f'/api/proxy/3/2/movie/detail/{anime_id}', video_id=anime_id, note='Downloading anime info JSON')
        return traverse_obj(metadata, ('data', 'movie'))

    def _get_the_last_page(self, anime_id: str) -> int:
        data_eps = self._call_api(path_url=f'/api/proxy/3/2/movie/episode/{anime_id}', video_id=anime_id, note='Getting last page')
        episodes = traverse_obj(data_eps, ('data', 'episode'))
        if not episodes:
            self.raise_no_formats(msg=f'Tidak ada episode untuk id {anime_id} (mungkin belum rilis atau invalid ID)', expected=True)
        last_eps = traverse_obj(episodes, (0, 'index'))
        try:
            self.to_screen(f'Total episode: {last_eps}')
            last_page_index = math.ceil(int(last_eps) / 30) - 1
            return max(last_page_index, 0)
        except (TypeError, ValueError) as e:
            self.raise_no_formats(msg=f'Gagal parsing episode index: {last_eps!r} {e}', expected=True)

    def _fetch_episode_list_page(self, anime_id: str, page_num: int = 0) -> dict[str, any] | None:
        self.write_debug(f'Fetching page {page_num} for anime {anime_id}')
        cache_file = f'{anime_id}_{page_num}'
        response = self.cache.load('animein', cache_file)
        if not response:
            response = self._call_api(path_url=f'/api/proxy/3/2/movie/episode/{anime_id}', video_id=anime_id, query={'page': page_num}, note=f'Downloading page {page_num}')
            self.cache.store('animein', cache_file, response)
        return traverse_obj(response, ('data', 'episode'))

    def _search_anime(self, query: str, page_num: str = 0) -> dict[str, any] | None:
        response = self._call_api(
            path_url='/api/proxy/3/2/explore/movie',
            video_id=query,
            query={'page': page_num, 'sort': 'views', 'keyword': query},
        )
        return traverse_obj(response, ('data', 'movie'))
