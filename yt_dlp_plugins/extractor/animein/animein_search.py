import itertools

from yt_dlp.extractor.common import SearchInfoExtractor
from yt_dlp.utils import ExtractorError

from .animein_web import AnimeinBaseIE


class AnimeinSearchIE(SearchInfoExtractor, AnimeinBaseIE):
    IE_DESC = 'animeinweb Search'
    IE_NAME = 'animein:search'
    _SEARCH_KEY = 'animein'

    def _search_results(self, query: str):
        for page_num in itertools.count(0):
            anime_list = self._search_anime(query, page_num)

            if not anime_list:
                if page_num == 0:
                    '''Error, jika page == 0 dan tidak menemukan daftar anime,
                    loh kan mana tau nanti di page 1 ada daftar anime nya?,
                    halah nyangkem, gawe'o extractor dewe su'''
                    raise ExtractorError(f'No anime found with the title: {query!r}', expected=True)
                break  # break, jika page > 0 dan sudah tidak menemukan daftar anime lagi!

            for anime in anime_list:
                yield self.url_result(
                    url=f'https://animeinweb.com/anime/{anime.get("id")}',
                    ie='AnimeinWeb',
                    video_id=anime.get('id'),
                    video_title=anime.get('title'),
                )
