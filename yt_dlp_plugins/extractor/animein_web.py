
from yt_dlp.utils import (
    LazyList,
    int_or_none,
    traverse_obj,
    url_or_none,
)

from .animein import AnimeinBaseIE


class AnimeinWebIE(AnimeinBaseIE):
    """ASEP SIGMA LMAO"""
    IE_DESC = 'custom extractor for animeinweb.com'
    IE_NAME = 'animeinweb'
    _VALID_URL = r'https?://animeinweb\.com/anime/(?P<id>\d+)$'

    def _build_episode_entry(self, episode_data: dict, anime_data: dict) -> dict[str, any]:
        episode_id = episode_data.get('id')
        episode_title = episode_data.get('title', '')
        episode_index = episode_data.get('index')
        title = anime_data.get('title')
        return {
            'id': episode_id,
            'title': f'{title} {episode_title}',
            'series': title,
            'playlist_title': title,
            'media_type': 'episode',
            'ext': 'mp4',
            'episode_number': int_or_none(episode_index),
            'thumbnail': url_or_none(self._get_thumbnail(image_url=episode_data.get('image'))),
            'formats': LazyList(self._extract_formats(episode_id, episode_title)),
            **traverse_obj(
                anime_data,
                {
                    'series_id': ('id'),
                    'alt_title': ('synonyms'),
                    'view_count': ('views', {int_or_none}),
                    'release_year': ('year', {int_or_none}),
                    'categories': ('genre', {lambda g: [c.strip() for c in g.split(',')]}),
                },
            ),
        }

    def _entries(self, anime_id: str, anime_data):
        last_page_index = self._get_the_last_page(anime_id)
        for page_num in range(last_page_index, -1, -1):  # start, step, stop
            episodes = self._fetch_episode_list_page(anime_id, page_num)
            if not episodes:
                continue
            for episode in reversed(episodes):
                yield self._build_episode_entry(episode, anime_data)

    def _real_extract(self, url: str) -> dict[str, any]:
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
