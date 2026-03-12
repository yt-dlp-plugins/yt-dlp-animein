
from .animein_web import AnimeinWebIE


class AnimeinEpisodeIE(AnimeinWebIE):
    """Ini extractor buat episode single"""
    # XXX: jangan berharap banyak!
    # https://animeinweb.com/anime/1280?ep=165
    IE_DESC = 'animeinweb single episode'
    IE_NAME = 'animeinweb:episode'
    _VALID_URL = r'https://animeinweb.com/anime/(?P<id>\d+)\?ep=(?P<eps>\d+)$'
    _WORKING = False  # XXX: Maybe work

    def _real_extract(self, url):
        mobj = self._match_valid_url(url)
        anime_id = mobj.group('id')
        episode_number = mobj.group('eps')
        return self._formats(anime_id, episode_number)

    def _formats(self, anime_id, episode_number):
        # TODO: refactor this into smaller functions
        anime_data = self._get_anime_info(anime_id)
        page = self._find_page(anime_id, episode_number)
        max_retries = self.get_param('retries')
        # Talk to me, ooo talk to me
        for _ in range(1, max_retries):
            list_episode = self._fetch_episode_list_page(anime_id, page)
            episode_data = next((ep for ep in list_episode if ep.get('index') == episode_number), None)
            if episode_data is None:
                self.to_screen(f'Retrying ({_}/{max_retries})')
                page -= 1
            if episode_data:
                return self._build_episode_entry(episode_data, anime_data)
        self.raise_no_formats(f'Episode {episode_number} not found after {max_retries} retries', expected=True)

    def _find_page(self, anime_id, target_episode, eps_per_page=30):
        last_page = self._get_the_last_page(anime_id)
        page = last_page - ((int(target_episode) - 1) // eps_per_page)
        return max(page, 0)  # Jangan sampe Negative XP (https://open.spotify.com/track/6KpwVlibZELGYMZF2ruhGn?si=48bc4613942e4f66)
