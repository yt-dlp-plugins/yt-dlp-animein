__version__ = '2.2.8'

import itertools
from typing import Any
from collections.abc import Iterator
from yt_dlp.extractor.common import SearchInfoExtractor
from yt_dlp.utils import (
    ExtractorError,
    str_or_none,
    traverse_obj,
    url_or_none,
)

from .common import AnimeinBaseIE as Animein


class AnimeinPlaylistIE(Animein):
    """ASEP SIGMA LMAO"""

    IE_DESC = 'custom extractor for animeinweb.com'
    IE_NAME = Animein.IE_NAME
    _VALID_URL = Animein.ANIMEIN_BASE_URL_RE % r'(?P<id>\d+)$'
    _TESTS = [
        {
            'url': 'https://animeinweb.com/anime/6307',
            'info_dict': {
                'display_id': '6307',
                'title': 'Tsue to Tsurugi no Wistoria Season 2',
                'description': 'Season ke-2 dari Tsue to Tsurugi no Wistoria',
                'view_count': '73554',
                'id': '6307',
                'playlist_mincount': 3,
            },
            'params': {'skip_download': True},
        },
        {
            'url': 'https://animeinweb.com/anime/1280',
            'info_dict': {
                'display_id': '1280',
                'title': 'Black Clover',
                'description': 'Asta dan Yuno ditinggalkan di gereja yang sama pada hari yang sama. Dibesarkan bersama sebagai anak-anak, mereka mengetahui tentang “Raja Penyihir”—gelar yang diberikan kepada penyihir terkuat di kerajaan—dan berjanji bahwa mereka akan bersaing satu sama lain untuk memperebutkan posisi Raja Penyihir berikutnya. Namun, saat mereka tumbuh dewasa, perbedaan mencolok di antara mereka menjadi jelas. Sementara Yuno mampu menggunakan sihir dengan kekuatan dan kontrol yang luar biasa, Asta tidak dapat menggunakan sihir sama sekali dan berusaha mati-matian untuk membangkitkan kekuatannya dengan berlatih secara fisik.\r\n\r\nSaat mereka mencapai usia 15 tahun, Yuno dianugerahi Grimoire yang spektakuler dengan semanggi berdaun empat, sementara Asta tidak menerima apa pun. Namun, segera setelah itu, Yuno diserang oleh seseorang bernama Lebuty, yang tujuan utamanya adalah untuk mendapatkan Grimoire milik Yuno. Asta mencoba melawan Lebuty, tetapi dia kalah. Meski tanpa harapan dan di ambang kekalahan, dia menemukan kekuatan untuk melanjutkan saat mendengar suara Yuno. Melepaskan emosi batinnya dalam kemarahan, Asta menerima Grimoire semanggi lima daun, sebuah "Black Clover" memberinya kekuatan yang cukup untuk mengalahkan Lebuty. Beberapa hari kemudian, kedua sahabat itu pergi ke dunia luar, keduanya mencari tujuan yang sama—untuk menjadi Raja Penyihir!',
                'view_count': '4944043',
                'id': '1280',
                'playlist_count': 170,
            },
            'params': {'skip_download': True},
        },
    ]

    def _real_extract(self, url: str) -> dict[str, Any]:
        anime_id = self._match_id(url)
        anime_data = self._get_anime_info(anime_id)
        return self.playlist_result(
            entries=self._yield_entries(anime_id, anime_data),
            playlist_id=anime_id,
            display_id=anime_id,
            **traverse_obj(
                anime_data,
                {
                    'title': ('title', {str_or_none}),
                    'description': ('synopsis', {str_or_none}),
                    'image_poster': ('image_poster', {url_or_none}),
                    'image_cover': ('image_cover', {url_or_none}),
                    'view_count': ('views', {str_or_none}),
                },
            ),
        )


class AnimeinEpisodeIE(Animein):
    """Ini extractor buat episode single"""

    # XXX: jangan berharap banyak!
    IE_DESC = 'animeinweb single episode'
    IE_NAME = Animein.IE_NAME + ':episode'
    _VALID_URL = Animein.ANIMEIN_BASE_URL_RE % r'(?P<id>[^\?]+)\?ep=(?P<eps>\d+)$'
    _WORKING = False
    _TESTS = [
        {
            'url': 'https://animeinweb.com/anime/6307?ep=1',
            'info_dict': {
                'id': '315173',
                'episode_number': 1,
                'title': 'Tsue to Tsurugi no Wistoria Season 2 Episode 1',
                'series': 'Tsue to Tsurugi no Wistoria Season 2',
                'playlist_title': 'Tsue to Tsurugi no Wistoria Season 2',
                'media_type': 'episode',
                'ext': 'mp4',
                'format_note': str,
                'format_id': str,
                'height': int,
                'width': float,
                'resolution': str,
                'dynamic_range': str,
                'aspect_ratio': float,
                'series_id': '6307',
                'alt_title': 'Wistoria: Wand and Sword Season 2',
                'view_count': 73555,
                'release_year': 2026,
                'categories': ['Action', 'Fantasy', 'School'],
            },
            'params': {'skip_download': True},
        },
        {
            'url': 'ydl https://animeinweb.com/anime/1280?ep=50',
            'info_dict': {
                'id': '21247',
                'episode_number': 50,
                'title': 'Black Clover Episode 50',
                'series': 'Black Clover',
                'playlist_title': 'Black Clover',
                'media_type': 'episode',
                'ext': 'mp4',
                'format_note': str,
                'format_id': str,
                'height': int,
                'width': float,
                'resolution': str,
                'dynamic_range': str,
                'aspect_ratio': float,
                'series_id': '1280',
                'alt_title': 'Black Clover, ブラッククローバー, BC',
                'view_count': 4944046,
                'release_year': 2021,
                'categories': ['Action', 'Adventure', 'Comedy', 'Demons', 'Fantasy', 'Magic', 'Shounen', 'Super Power'],
            },
            'params': {'skip_download': True},
        },
    ]

    def _real_extract(self, url: str) -> dict[str, Any]:
        anime_id, ep_num = self._match_valid_url(url).groups()
        return self._formats(anime_id, ep_num)

    def _formats(self, anime_id: str, episode_number: str) -> dict[str, Any]:
        # TODO: refactor this into smaller functions
        anime_data = self._get_anime_info(anime_id)
        page = self._find_page(anime_id, episode_number)
        max_retries = self.get_param('retries')
        # Talk to me, ooo talk to me
        for _ in range(1, max_retries + 1):
            list_episode = self._fetch_episode_list_page(anime_id, page)
            if (episode_data := next((ep for ep in list_episode if ep.get('index') == episode_number), None)) is None:
                """coba ulang sampai nemu, kalo ga nemu ya errrrr"""
                self.to_screen(f'Retrying ({_}/{max_retries})')
                page -= 1
            if episode_data:
                return self._build_episode_entry(episode_data, anime_data)
        self.raise_no_formats(f'Episode {episode_number!r} not found after {max_retries} retries', expected=True)

    def _find_page(self, anime_id: str, target_episode: str, eps_per_page=30) -> int:
        last_page, _ = self._get_the_last_page(anime_id)
        page = last_page - ((int(target_episode) - 1) // eps_per_page)
        return max(page, 0)


class AnimeinSearchIE(SearchInfoExtractor, Animein):
    IE_DESC = 'animeinweb Search'
    IE_NAME = Animein.IE_NAME + ':search'
    _SEARCH_KEY = r'animein(?:web(?:search)?|search)?'  # opsional animein, animeinweb, animeinsearch, animeinwebsearch

    def _search_results(self, query: str) -> Iterator[dict[str, Any]]:
        for page_num in itertools.count(0):
            # anime_list = self._search_anime(query, page_num)

            if not (anime_list := self._search_anime(query, page_num)):
                if page_num == 0:
                    """Error, jika page == 0 dan tidak menemukan daftar anime,
                    loh kan mana tau nanti di page 1 ada daftar anime nya?,
                    halah nyangkem, gawe'o extractor dewe su"""
                    raise ExtractorError(f'No anime found with the title: {query!r}', expected=True)
                break  # break, jika page > 0 dan sudah tidak menemukan daftar anime lagi!

            for anime in anime_list:
                yield self.url_result(
                    url=f'https://animeinweb.com/anime/{anime.get("id")}',
                    ie=AnimeinPlaylistIE.ie_key(),
                    video_id=anime.get('id'),
                    video_title=anime.get('title'),
                )
