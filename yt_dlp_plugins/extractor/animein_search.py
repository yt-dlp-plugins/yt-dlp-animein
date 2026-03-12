import itertools

from yt_dlp.extractor.common import SearchInfoExtractor

from .animein_web import AnimeinBaseIE


class AnimeinSearchIE(SearchInfoExtractor, AnimeinBaseIE):
    IE_DESC = 'animeinweb Search'
    IE_NAME = 'animein:search'
    _SEARCH_KEY = 'animein'

    def _search_results(self, query: str):
        for page_num in itertools.count(0):
            anime_list = self._search_anime(query, page_num)
            if not anime_list:
                break
            for anime in anime_list:
                yield self.url_result(
                    url=f'https://animeinweb.com/anime/{anime.get("id")}',
                    ie='AnimeinWeb',
                    video_id=anime.get('id'),
                    video_title=anime.get('title'),
                )
