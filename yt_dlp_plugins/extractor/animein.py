import itertools, re
from yt_dlp.utils import urljoin, int_or_none
from yt_dlp.extractor.common import InfoExtractor, SearchInfoExtractor

# https://animeinweb.com/anime/1280?ep1
# https://animeinweb.com/api/proxy/3/2/movie/episode/1280?page=0
# https://animeinweb.com/api/proxy/3/2/movie/detail/1280
# https://animeinweb.com/api/proxy/3/2/episode/streamnew/1280


class AnimeInWebIE(InfoExtractor):
    """ASEP SIGMA LMAO"""

    IE_NAME = 'animeinweb'
    _VALID_URL = r'https?://animeinweb\.com/anime/(?P<id>\d+)'

    def call_api(
        self,
        base_url='https://animeinweb.com',
        path_url=None,
        item=None,
        query=None,
        note='Downloading ANIMEIN API JSON',
    ):
        """Buat manggil api animein"""

        return self._download_json(
            urljoin(base_url, path_url), item, query=query, note=note
        )

    def extract_anime_info(self, anime_id):
        """Buat ambil judul anime doang sih wkwk"""
        metadata_dict = self.call_api(
            path_url=f'/api/proxy/3/2/movie/detail/{anime_id}', item=anime_id
        )
        return metadata_dict.get('data').get('movie')

    def get_filesize(self, size_str):
        if not size_str:
            return None

        if isinstance(size_str, str):
            return int(float(size_str) * 1024**2)

        return None

    def url_verification(self, link):
        if not link:
            return False

        IGNORE_PATTERNS = [
            'gdriveplayer.to',
            'new.uservideo.xyz',
            'www.blogger.com',
            'uservideo.xyz',
            'embed2.php',
            '/embed',
            '?embed=true',
            'autoplay=true',
        ]

        if any(bad_pattern in link for bad_pattern in IGNORE_PATTERNS):
            return False

        return link

    def fill_formats(self, episode_id, episode):
        if not episode_id:
            return False

        streams_info = self.call_api(
            path_url=f'/api/proxy/3/2/episode/streamnew/{episode_id}',
            item=episode_id,
            note=f'Downloading info {episode}',
        )
        streams = streams_info.get('data').get('server')

        formats = []
        for stream in streams:
            link_stream = self.url_verification(stream.get('link'))
            quality = stream.get('quality', {})

            if not link_stream:
                continue
            if not re.search(r'^\d+p?$', quality, re.IGNORECASE):
                # api ngent0t ada aja bug nya
                continue

            height = int(quality.replace('p', ''))

            formats.append(
                {
                    'url': link_stream,
                    'quality': quality,
                    'format_id': quality,
                    'height': height,
                    'width': int_or_none(((height * 16) / 9)),
                    'filesize': int_or_none(
                        self.get_filesize(stream.get('key_file_size'))
                    ),
                }
            )
        return formats

    def get_thumbnail(self, base_url='https://api.animein.net', image_url=None):
        """Fungsi buat nyambung url kalo url nya ga jelas"""
        if image_url is None:
            return None

        if image_url.startswith(('https://', 'http://')):
            if not image_url.endswith('_full.jpg'):
                return f'{image_url}_full.jpg'

        if image_url.startswith(('/assets', '/')):
            return f'{base_url}{image_url}'

        return None

    def _real_extract(self, url):
        """real extract: buat ekstrak dan kirim ke yt-dlp ☺"""
        self.to_screen('Kalo ada bug kabarin ya! 😅')
        anime_id = self._match_id(url)
        anime_info = self.extract_anime_info(anime_id=anime_id)

        entries = []
        for i in itertools.count(0):
            episode_info_dict = self.call_api(
                path_url=f'/api/proxy/3/2/movie/episode/{anime_id}',
                item=anime_id,
                query={'page': i},
                note=f'Downloading page {i}',
            )

            episode_info = episode_info_dict.get('data').get('episode')

            if not episode_info:
                break

            for idx in episode_info:
                episode_id = idx.get('id')
                episode_str = idx.get('title')
                episode_index = idx.get('index')

                entries.append(
                    {
                        'id': episode_id,
                        'title': f'{anime_info.get("title")} {episode_str} ',
                        'episode': episode_str,
                        'episode_number': int_or_none(episode_index),
                        'thumbnail': self.get_thumbnail(idx.get('image')),
                        'formats': self.fill_formats(episode_id, episode_str),
                        'webpage_url': f'{url}?ep{episode_index}',
                    }
                )

        return {
            '_type': 'playlist',
            'id': anime_id,
            'channel_url': 'https://animeinweb.com',
            'entries': reversed(entries),
        }


class AnimeInSearchIE(SearchInfoExtractor, AnimeInWebIE):
    IE_DESC = 'animein web Search'
    IE_NAME = 'animein:search'
    _SEARCH_KEY = 'animein'

    def _search_results(self, query):
        for i in itertools.count(0):
            query = {'page': i, 'sort': 'views', 'keyword': query}
            result = self.call_api(
                path_url='/api/proxy/3/2/explore/movie', item=i, query=query
            )['data'].get('movie')

            if not result:
                self.to_screen('Tidak menemukan daftar anime')
                break

            anime_id = result[i].get('id')

            self.to_screen(anime_id)

            yield self.url_result(
                f'https://animeinweb.com/anime/{anime_id}', AnimeInWebIE
            )
