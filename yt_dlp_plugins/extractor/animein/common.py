from collections.abc import Iterator
from typing import Any

from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import (
    ExtractorError,
    LazyList,
    parse_resolution,
    urljoin,
    str_to_int,
)


class AnimeinBaseIE(InfoExtractor):
    """ANIMEIN BASE EXTRACTOR"""

    # ==========================================
    # 1. KONFIGURASI KELAS (HEADER)
    # ==========================================
    IE_NAME = 'animein'
    _VALID_URL = False
    ANIMEIN_BASE_URL_RE = r'https://animeinweb\.com/anime/%s'
    BASE_URL = 'https://animeinweb.com/'  # || https://xyz-api.animein.net
    _HEADERS = {'x-proxy-secret': 'animein-secure-proxy-key-123'}

    # ==========================================
    # 2. BASE API METHODS (DRIVER)
    # ==========================================
    def _call_api(self, path=None, video_id=None, query=None, **kwargs) -> Any:
        """Buat manggil api animein"""
        return self._download_json(
            urljoin(self.BASE_URL, path),
            video_id=video_id,
            query=query,
            **kwargs,
            headers=self._HEADERS,
        )

    def _get_anime_info(self, anime_id: str) -> dict[str, Any] | None:
        """Buat ambil judul anime doang sih wkwk"""
        metadata = self._call_api(
            path=f'/api/proxy/3/2/movie/detail/{anime_id}',
            video_id=anime_id,
            note='Downloading anime info JSON',
        )
        return metadata.get('data', {}).get('movie', [])

    def _search_anime(self, query: str, page_num: int = 0) -> list[dict[str, Any]] | None:
        response = self._call_api(
            path='/api/proxy/3/2/explore/movie',
            video_id=query,
            query={'page': page_num, 'sort': 'views', 'keyword': query},
        )
        return response.get('data', {}).get('movie', [])

    def _get_episode_info(self, episode_id: str, episode: str) -> list[dict[str, Any]] | None:
        cache_file = f'{episode_id}_{episode}'
        if (episode_info := self.cache.load('animein', cache_file)) is None:
            episode_info = self._call_api(
                path=f'/api/proxy/3/2/episode/streamnew/{episode_id}',
                video_id=episode_id,
                note=f'Downloading info for {episode.lower()}',
            )
            self.cache.store('animein', cache_file, episode_info)
        return episode_info.get('data', {}).get('server', [])

    def _fetch_episode_list_page(self, anime_id: str, page_num: int = 0) -> list[dict[str, Any]]:
        self.write_debug(f'Fetching page {page_num} for anime {anime_id}')
        response = self._call_api(
            path=f'/api/proxy/3/2/movie/episode/{anime_id}',
            video_id=anime_id,
            query={'page': page_num},
            note=f'Downloading page {page_num}',
        )
        return response.get('data', {}).get('episode', [])

    # ==========================================
    # 3. PROCESSING HELPERS
    # ==========================================
    def _get_the_last_page(self, anime_id: str, max_eps: int = 30) -> tuple[int, list[dict[str, Any]]]:
        data_eps = self._call_api(
            path=f'/api/proxy/3/2/movie/episode/{anime_id}',
            video_id=anime_id,
            note='Getting last page',
        )

        episodes = data_eps.get('data', {}).get('episode', [])

        if not episodes:
            raise ExtractorError(
                msg=f"Unable to find episodes for {anime_id!r}; check if it's released or the ID is correct",
                expected=True,
            )
        # index pasti ada jika episodes tidak kosong;
        last_ep = str_to_int(episodes[0]['index'])

        if last_ep <= max_eps:
            return 0, episodes

        return last_ep // max_eps, episodes

    @staticmethod
    def _format_thumbnail_url(p: str) -> str | None:
        if not p:
            return None
        if 'img1.ak.crunchyroll.com' in p:
            return p if p.endswith('_full.jpg') else p + '_full.jpg'
        if p.startswith(('/assets', '/')):
            return urljoin('https://animein.net', p)
        return p

    def _yield_formats(self, episode_id: str, episode: str) -> Iterator[dict[str, any]]:
        for stream in self._get_episode_info(episode_id, episode):
            if (stream_type := stream.get('type')) != 'direct':
                continue
            quality = stream.get('quality')
            file_size_raw = stream.get('key_file_size')
            yield {
                'url': stream.get('link'),
                'format_note': f'{quality} {stream_type}' if quality else stream_type,
                'format_id': quality.replace('p', '') if quality else None,
                'filesize': int(float(file_size_raw) * 1024**2) if file_size_raw else None,
                'height': parse_resolution(quality).get('height') if quality else None,
                'width': (int(quality.replace('p', '')) * 16 // 9) if (quality and 'p' in quality) else None,
                'http_headers': {'referer': self.BASE_URL},
            }

    # ==========================================
    # 4. RESULT BUILDERS (FINAL LOGIC)
    # ==========================================
    def _build_episode_entry(self, episode_data: dict, anime_data: dict) -> dict[str, Any]:
        title = anime_data.get('title', 'animein')
        episode_id = episode_data.get('id', 'animein')
        episode_title = episode_data.get('title', 'Unknown')
        return {
            'id': episode_id,
            'title': f'{title} {episode_title}',
            'series': title,
            'playlist_title': title,
            'media_type': 'episode',
            'ext': 'mp4',
            'formats': LazyList(self._yield_formats(episode_id, episode_title)),
            'episode_number': str_to_int(episode_data.get('index')),
            'thumbnail': self._format_thumbnail_url(episode_data.get('image')),
            'series_id': anime_data.get('id'),
            'alt_title': anime_data.get('synonyms'),
            'view_count': str_to_int(anime_data.get('views')),
            'release_year': str_to_int(anime_data.get('year')),
            'categories': [c.strip() for c in anime_data.get('categories', '').split(',') if c],
        }

    def _yield_entries(self, anime_id: str, anime_data: dict) -> Iterator[dict[str, str]]:
        found_any = False  # bo'ol
        last_page_index, page_0_episodes = self._get_the_last_page(anime_id)
        for page_num in range(last_page_index, -1, -1):
            episodes = page_0_episodes if page_num == 0 else self._fetch_episode_list_page(anime_id, page_num)

            if not episodes:
                continue  # Halaman ini kosong? Skip, cari di halaman berikutnya

            found_any = True
            yield from (self._build_episode_entry(ep, anime_data) for ep in reversed(episodes))

        if found_any is False:  # Kalau sampai halaman 0 pun gak ada yang nyangkut, ya eerrrroorrr
            self.raise_no_formats('No episodes found', expected=True)
